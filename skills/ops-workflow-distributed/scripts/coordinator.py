#!/usr/bin/env python3
"""Run one authorized Agent Ops issue through distributed delivery."""

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone


SKILLS = {
    "implement": "ops-implement",
    "repair": "ops-implement",
    "verification": "container-worker-review",
    "quality-review": "ops-review-quality",
    "spec-review": "ops-review-spec",
}
REVIEW_ROLES = ("quality", "spec")
OPEN_DISPOSITIONS = {"open", "advisory_left_open"}


class Pause(Exception):
    """A gate needs current evidence or an operator decision."""


def require(condition, message):
    if not condition:
        raise Pause(message)


def invoke(command, *args, payload=None):
    try:
        result = subprocess.run(
            [*command, *map(str, args)], check=False, capture_output=True,
            text=True, input=json.dumps(payload) if payload is not None else "",
        )
        require(result.returncode == 0, f"{args[0]} exited {result.returncode}. Reconcile before retrying.")
        return json.loads(result.stdout)
    except (OSError, ValueError) as error:
        raise Pause(f"{args[0]} did not return a usable JSON response.") from error


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value)


def write_json(path, data):
    temporary = path.with_suffix(".tmp")
    with temporary.open("w") as stream:
        json.dump(data, stream, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def artifact(job, name):
    path = Path(job["output"]) / name
    require(not path.is_symlink() and path.is_file(), f"{job['id']} lacks {name}.")
    require(path.parent.resolve() == Path(job["output"]), f"{job['id']} has a redirected output path.")
    return path


def review_matches(result, role, request):
    if not isinstance(result, dict) or result.get("schema_version") != 1:
        return False
    if any(result.get(key) != value for key, value in {
        "role": role, "base_sha": request["base_sha"], "head_sha": request["head_sha"],
        "range_start_sha": request["range_start_sha"],
        "prior_review_ref": request.get("prior_review_ref"),
    }.items()):
        return False
    findings = result.get("findings")
    limits = result.get("verification_limits")
    if (not isinstance(findings, list) or not isinstance(limits, list)
            or not all(isinstance(limit, str) for limit in limits)):
        return False
    ids = set()
    for finding in findings:
        if not isinstance(finding, dict) or not all(
            isinstance(finding.get(key), str) and finding[key]
            for key in ("id", "location", "evidence")
        ):
            return False
        if (finding["id"] in ids or not isinstance(finding.get("blocking"), bool)
                or finding.get("disposition") not in ("open", "advisory_left_open", "fixed", "rejected")):
            return False
        if role == "quality" and (not isinstance(finding.get("severity"), str)
                                  or finding.get("unmet_requirement") is not None):
            return False
        if role == "spec" and (finding.get("severity") is not None
                               or not isinstance(finding.get("unmet_requirement"), str)):
            return False
        ids.add(finding["id"])
    if not {finding["id"] for finding in request["prior_findings"]} <= ids:
        return False
    verdict = result.get("verdict")
    blocked = any(f["blocking"] and f["disposition"] in OPEN_DISPOSITIONS for f in findings)
    if verdict not in ("pass", "fail") or blocked != (verdict == "fail"):
        return False
    if role == "spec":
        requirements = result.get("requirements")
        if not isinstance(requirements, list) or not requirements:
            return False
        if not all(isinstance(item, dict) and all(
            isinstance(item.get(key), str) and item[key] for key in ("id", "source", "evidence")
        ) and item.get("status") in ("met", "unmet", "unverified")
                   for item in requirements):
            return False
        if verdict == "pass" and any(item["status"] != "met" for item in requirements):
            return False
        requirement_ids = {item["id"] for item in requirements}
        if (len(requirement_ids) != len(requirements)
                or not set(request["requirement_ids"]) <= requirement_ids
                or not {finding["unmet_requirement"] for finding in findings} <= requirement_ids):
            return False
    return True


class Coordinator:
    def __init__(self, config, path, issue, repository):
        self.config = config
        self.path = path
        self.state = json.loads(path.read_text()) if path.exists() else {
            "schema_version": 1, "key": {"issue": issue, "repository": repository},
            "stage": "intake", "status": "active", "events": [], "decisions": [],
            "jobs": [], "checks": {}, "reviews": {}, "rejected_reviews": [],
            "attempts": {}, "pushes": {}, "receipts": {}, "proposal_history": [],
            "policy": {key: config.get(key) for key in ("base_branch", "app_actor", "skills", "limits")},
        }
        self.response = None

    def save(self):
        write_json(self.path, self.state)

    def event(self, kind, message, **fields):
        self.state["events"].append({
            "seq": len(self.state["events"]) + 1, "kind": kind, "stage": self.state["stage"],
            "message": message, **fields,
        })
        self.save()

    def stage(self, stage, message):
        self.state.update(stage=stage, status="active", clarification=None)
        self.event("progress", message)

    def wait(self, status, message, request_id=None, **details):
        previous = self.state.get("clarification")
        clarification = {"id": request_id, "message": message, **details} if request_id else None
        if (self.state["status"] == status and previous == clarification
                and self.state["events"][-1]["message"] == message):
            return
        self.state.update(status=status, clarification=clarification)
        self.event(status, message, **({"request_id": request_id} if request_id else {}))

    def host(self, action, **fields):
        return invoke(self.config["host"], action, payload={
            "key": self.state["key"], **fields,
        })

    def app(self, operation, *args, payload=None):
        try:
            return invoke(self.config["github_app"], self.state["key"]["repository"],
                          operation, *args, payload=payload)
        except Pause as error:
            raise Pause(f"PER-73 {operation} failed. Reconcile the operation and installation access.") from error

    def inspect(self):
        result = self.host("inspect", stage=self.state["stage"],
                           proposal=self.state.get("proposal"),
                           clarification=self.state.get("clarification"), response=self.response,
                           request=self.state.get("request"))
        require(result.get("eligible") is True, result.get("message", "Issue is ineligible or needs clarification."))
        proposal = result["proposal"]
        issue = self.state["key"]["issue"]
        branch_prefix = issue.lower() + "/"
        require(re.fullmatch(r"per-[1-9][0-9]*/[a-z0-9][a-z0-9-]*", proposal["branch"])
                and proposal["branch"].startswith(branch_prefix)
                and proposal["branch"] != proposal["target"],
                "The proposed branch does not meet the PER-73 task policy.")
        require(proposal["target"] == self.config["base_branch"] and sha(proposal["base_sha"]),
                "The proposal must match the configured helper target and pin its current commit.")
        transitions = proposal["transitions"]
        require(all(isinstance(transitions.get(key), str) and transitions[key]
                    for key in ("from", "start", "review")) and transitions["start"] != transitions["review"],
                "Resolve the issue lifecycle before starting.")
        require(all(proposal.get(key) for key in (
            "issue_id", "issue_url", "scope", "requirements", "policy_version", "source_version", "project",
            "checkout", "verification_argv", "required_checks", "title",
        )), "The approved repository and issue need complete execution context.")
        require(isinstance(proposal["requirements"], dict) and all(
            isinstance(proposal[key], list) and all(isinstance(item, str) and item for item in proposal[key])
            for key in ("verification_argv", "required_checks")
        ), "Name the required checks and configure the exact verification argv.")
        require(Path(proposal["checkout"]).is_absolute(), "Configure an absolute host checkout path.")
        if self.state.get("proposal") != proposal:
            require(self.state["stage"] == "intake", "Issue requirements or repository policy changed. Reconcile the approved run.")
            identifier = digest(proposal)
            self.state["proposal_history"].append({"id": identifier, "proposal": proposal})
            self.state.update(proposal=proposal, proposal_id=identifier, head_sha=proposal["base_sha"])
            self.event("proposal", "Prepared the issue transition, branch and checkout proposal.",
                       proposal_id=self.state["proposal_id"])
        self.plan = self.state["proposal"]

    def authorization(self, grant, draft=None):
        scope = {"proposal_id": self.state["proposal_id"], "grant": grant}
        if draft is not None:
            scope["draft"] = draft
        request_id = digest(scope)
        if any(decision["grant"] == grant and decision["proposal_id"] == scope["proposal_id"]
               and (decision["request_id"] == request_id or decision["mode"] == "preauthorized")
               for decision in self.state["decisions"]):
            return True
        result = self.host("authorize", **scope, request_id=request_id, proposal=self.plan,
                           response=self.response, request=self.state.get("request"))
        if draft is not None and "revised_draft" in result and result["revised_draft"] != draft:
            replacement = result["revised_draft"]
            require(isinstance(replacement, dict) and set(replacement) == {"title", "body"}
                    and all(isinstance(value, str) and value.strip() for value in replacement.values())
                    and self.plan["issue_url"] in replacement["body"],
                    "A revised PR draft needs the issue reference.")
            evidence = self.publication_evidence()
            if evidence not in replacement["body"]:
                replacement["body"] += "\n\n" + evidence
            require(replacement != draft, "The revised draft needs a change within the approved scope.")
            self.state["pending_draft"] = replacement
            scope["draft"] = replacement
            self.wait("waiting_approval", "Approve the revised PR draft.", digest(scope), **scope)
            return False
        if result.get("approved") is not True:
            message = result.get("message", f"Approve {grant} for the recorded proposal.")
            self.wait("waiting_approval", message, request_id, **scope)
            return False
        require(result.get("request_id") == request_id and result.get("actor") and result.get("reference")
                and result.get("mode") in {"explicit", "preauthorized"},
                "Authorization needs an accountable actor, reference and exact proposal.")
        self.state["decisions"].append({
            **scope, "request_id": request_id, "mode": result["mode"], "actor": result["actor"],
            "reference": result["reference"], "recorded_at": datetime.now(timezone.utc).isoformat(),
        })
        self.state.update(status="active", clarification=None)
        self.event("authorization", f"Recorded authorization to {grant}.", request_id=request_id)
        return True

    def count(self, name, default, token):
        attempts = self.state["attempts"].setdefault(name, [])
        if token in attempts:
            return
        limit = self.config.get("limits", {}).get(name, default)
        require(len(attempts) < limit, f"{name} budget exhausted. Review the recorded evidence.")
        attempts.append(token)
        self.save()

    def issue(self, operation, **evidence):
        receipt = self.host("issue", operation=operation,
                            operation_id=f"{self.path.stem}:{operation}", proposal=self.plan,
                            pr=self.state.get("pr"), head_sha=self.state["head_sha"], **evidence)
        transition = "start" if operation == "start" or operation.startswith("repair-") else "review"
        expected = self.plan["transitions"][transition]
        require(receipt.get("status") == expected and receipt.get("confirmed") is True,
                f"Linear did not confirm {operation}. Reconcile the current issue status.")
        self.state["receipts"][operation] = receipt
        self.save()

    def git(self, *args):
        result = subprocess.run(
            ["git", "-C", self.plan["checkout"], *args],
            check=False, capture_output=True, text=True,
        )
        require(result.returncode == 0, f"Trusted checkout Git {args[0]} failed.")
        return result.stdout.strip()

    def checkout_head(self, expected):
        require(self.git("rev-parse", "--show-toplevel") == self.plan["checkout"]
                and self.git("symbolic-ref", "--short", "HEAD") == self.plan["branch"]
                and self.git("rev-parse", "--verify", "HEAD") == expected
                and not self.git("status", "--porcelain"),
                "The trusted task branch moved. Preserve it and reconcile the recorded head.")

    def fetch(self, branch):
        response = self.app("fetch", self.plan["checkout"], branch)
        require(response.get("ref") == f"refs/remotes/hermes-app/{branch}" and sha(response.get("sha")),
                "The helper returned an unexpected fetch ref or SHA.")
        return response["sha"]

    def review_budget(self, role, head, pending_rejection=0):
        if role.endswith("-review"):
            rejected = sum(job["role"] == role and job["head_sha"] == head and bool(job.get("rejected"))
                           for job in self.state["jobs"])
            require(rejected + pending_rejection <= self.config.get("limits", {}).get("review_retries", 1),
                    f"{role} retry budget exhausted. Inspect the retained results.")

    def job(self, role, **assignment):
        head = self.state["head_sha"]
        base = self.plan["base_sha"]
        jobs = self.state["jobs"]
        key = f"{role}:{head}"
        entry = next((job for job in reversed(jobs) if job["key"] == key and not job.get("rejected")), None)
        if entry is None:
            self.review_budget(role, head)
            skill = self.config["skills"][role]
            require(skill.startswith(SKILLS[role] + "@"), f"Configure the correct pinned skill for {role}.")
            entry = {
                "key": key, "id": f"ops-{self.path.stem[:24]}-{len(jobs) + 1}", "role": role,
                "base_sha": base, "head_sha": head, "skill": skill, "assignment": assignment,
            }
            jobs.append(entry)
            self.save()
        require(entry["assignment"] == assignment, "Worker inputs changed for a persisted job.")
        known = invoke(self.config["launcher"], "status")
        matches = [result for result in known if result["id"] == entry["id"]]
        require(len(matches) <= 1, "Launcher returned duplicate job records.")
        if matches:
            result = matches[0]
        else:
            require(not entry.get("observed"), "A previously observed launcher job is missing.")
            entry_attempts = entry.get("dispatch_attempts", 0)
            require(entry_attempts < self.config.get("limits", {}).get("dispatch_attempts", 2),
                    "Launcher dispatch budget exhausted.")
            entry["dispatch_attempts"] = entry_attempts + 1
            self.save()
            args = [
                "run-role", self.plan["project"], "--id", entry["id"],
                "--issue", self.state["key"]["issue"], "--role", role, "--base", base,
                "--head", head, "--skill", entry["skill"],
            ]
            if role != "verification":
                task = self.path.parent / f"{entry['id']}.assignment.json"
                write_json(task, {"scope": self.plan["scope"], "requirements": self.plan["requirements"],
                                  "context": self.plan.get("worker_context", {}), **assignment})
                args += ["--task-file", str(task)]
            result = invoke(self.config["launcher"], *args)
        expected = {field: entry[field] for field in ("id", "role", "base_sha", "head_sha", "skill")}
        expected.update(issue=self.state["key"]["issue"], project=self.plan["project"])
        require(all(result.get(key) == value for key, value in expected.items()),
                "Launcher provenance differs from the approved assignment.")
        previous = entry.get("observed")
        status = result.get("archived_from") if result["status"] == "archived" else result["status"]
        entry["observed"] = status
        if status != previous:
            self.event("job", f"{role} job {status}.", job_id=entry["id"], head_sha=head)
        if status in {"running", "created", "preparing"}:
            self.wait("waiting_worker", f"Waiting for {entry['id']}.")
            return None
        if self.recovery_requested("retry_job"):
            self.review_budget(role, head, pending_rejection=1)
            decision = self.host("recover", kind="job", proposal=self.plan, job=result,
                                 response=self.response)
            self.record_recovery(decision, "retry_job", entry["id"])
            self.count(f"job_retry:{key}", self.config.get("limits", {}).get("job_retries", 1), entry["id"])
            entry["rejected"] = True
            self.event("job", "Operator authorized one fresh attempt after reconciling the terminal job.",
                       job_id=entry["id"], head_sha=head)
            self.response = None
            return self.job(role, **assignment)
        if status not in {"succeeded", "failed"}:
            raise Pause(f"{entry['id']} ended as {status}. Reconcile the host prerequisite or job.")
        return entry, result

    def work(self):
        repair = self.state.get("repair")
        role = "repair" if repair else "implement"
        outcome = self.job(role, repair=repair, readiness=self.state["readiness"])
        if outcome is None:
            return False
        entry, result = outcome
        require(entry["observed"] == "succeeded" and result.get("exit_code") == 0,
                f"{entry['id']} failed. Inspect its evidence before retrying.")
        report = artifact(result, "report.md")
        integration = self.host("integrate", proposal=self.plan, job=result,
                                report=str(report), expected_head=self.state["head_sha"])
        candidate = integration.get("head_sha")
        require(integration.get("confirmed") is True and sha(candidate)
                and candidate != self.state["head_sha"],
                "Host did not confirm a changed, inspected candidate commit.")
        self.checkout_head(candidate)
        self.git("merge-base", "--is-ancestor", self.state["head_sha"], candidate)
        self.state.update(head_sha=candidate)
        entry["integration"] = integration
        self.stage("verify", "Host recorded the inspected candidate. Starting independent verification.")
        return True

    def verify(self):
        outcome = self.job("verification")
        if outcome is None:
            return False
        entry, result = outcome
        command = json.loads(artifact(result, "command.json").read_text())
        log = artifact(result, "verification.log")
        head = self.state["head_sha"]
        require(command == {"argv": self.plan["verification_argv"], "cwd": "/workspace", "head_sha": head},
                "Verification did not use the approved command and exact commit.")
        exit_code = result.get("exit_code")
        require(type(exit_code) is int and (exit_code == 0) == (entry["observed"] == "succeeded"),
                "Launcher verification status and exit code disagree.")
        # Only the repository knows how its command reports per-check outcomes.
        checks = self.host("checks", proposal=self.plan, job=result, command=command, log=str(log))
        required = self.plan["required_checks"]
        outcomes = checks.get("outcomes", {})
        require(all(outcomes.get(name) in {"pass", "fail", "skipped", "unavailable", "not run"}
                    for name in required),
                "Required checks need individual outcomes from repository evidence.")
        evidence = {**command, "base_sha": self.plan["base_sha"], "exit_code": exit_code,
                    "outcomes": outcomes, "log": str(log), "job_id": entry["id"]}
        self.state["checks"][head] = evidence
        self.save()
        require(all(outcomes[name] in {"pass", "fail"} for name in required),
                "Required verification is incomplete. Restore the missing evidence or prerequisites.")
        if exit_code == 0 and all(outcomes[name] == "pass" for name in required):
            self.stage("publish", "Required verification passed for the pinned commit.")
        elif any(outcomes[name] == "fail" for name in required):
            self.count("verification_repairs", 2, head)
            self.state["repair"] = {"type": "verification", "evidence": evidence}
            self.stage("work", "Required verification failed. Dispatching a focused repair.")
        else:
            raise Pause("Required verification is incomplete. Restore the missing evidence or prerequisites.")
        return True

    def publication_evidence(self):
        head = self.state["head_sha"]
        verification = self.state["checks"][head]
        return (
            f"Required verification passed at `{head}` using `{json.dumps(verification['argv'])}`. "
            f"Job `{verification['job_id']}`.\n\n"
            "Initial quality and spec review pending. See subsequent App reviews and the final handoff comment."
        )

    def draft(self):
        return {"title": self.plan["title"], "body": (
            f"{self.plan['issue_url']}\n\n{self.plan['scope']}\n\n" + self.publication_evidence()
        )}

    def check_pr(self, pr, head):
        repository = self.state["key"]["repository"]
        number = pr.get("number")
        require(type(number) is int and number > 0
                and pr.get("html_url", "").lower() == f"https://github.com/{repository}/pull/{number}"
                and pr.get("author") == self.config["app_actor"] and pr.get("state") == "open"
                and pr.get("merged") is not True and pr.get("base_sha") == self.plan["base_sha"]
                and pr.get("head_sha") == head,
                "PR identity, state, base or head differs from the pinned run. Preserve human changes.")
        return pr

    def current_pr(self, head):
        pr = self.state["pr"]
        current = self.check_pr(self.app("pr-view", pr["number"]), head)
        match = self.check_pr(self.unique_pr() or {}, head)
        require(current["number"] == match["number"] == pr["number"], "The PR number changed.")
        return current

    def push(self):
        head = self.state["head_sha"]
        branch = self.plan["branch"]
        previous = self.state.get("published_head")
        pushes = self.state["pushes"]
        attempt = pushes.get(head)
        if attempt or previous:
            observed = self.fetch(branch)
            if observed == head and attempt:
                return
            require(observed == previous, "Remote task branch moved. Reconcile before pushing.")
        self.checkout_head(head)
        attempts = attempt["attempts"] if attempt else 0
        require(attempts < self.config.get("limits", {}).get("push_attempts", 2), "Push budget exhausted.")
        pushes[head] = {"previous": previous, "attempts": attempts + 1}
        self.save()
        receipt = self.app("push", self.plan["checkout"], branch, head)
        require(receipt == {"ref": f"refs/heads/{branch}", "sha": head} and self.fetch(branch) == head,
                "Push could not be confirmed at the verified commit.")

    def unique_pr(self):
        matches = self.app("pr-list", self.plan["branch"])
        require(isinstance(matches, list) and len(matches) <= 1, "Multiple PRs or invalid branch lookup.")
        return matches[0] if matches else None

    def publish(self):
        head = self.state["head_sha"]
        current = self.state.get("pr")
        draft = self.state.get("draft") or self.state.get("pending_draft") or self.draft()
        if not self.authorization("publish", draft):
            return False
        self.state["draft"] = draft
        self.state.pop("pending_draft", None)
        self.save()
        require(self.fetch(self.plan["target"]) == self.plan["base_sha"],
                "Target branch moved. Current checks and review coverage cannot clear this base.")
        if current:
            previous = self.state["published_head"]
            # A completed push may have moved the PR before the coordinator saved the result.
            observed = self.app("pr-view", current["number"])
            allowed = head if head in self.state["pushes"] and observed.get("head_sha") == head else previous
            self.check_pr(observed, allowed)
            require(observed["number"] == current["number"], "The PR number changed.")
            self.push()
            confirmed = self.current_pr(head)
        else:
            match = self.unique_pr()
            if match:
                require(self.state.get("create_pending"), "A PR predates this run's create intent. Reconcile ownership.")
            else:
                self.push()
                match = self.unique_pr()
                require(not match or self.state.get("create_pending"),
                        "A PR appeared before the recorded create attempt. Reconcile ownership.")
            if match is None:
                require(self.fetch(self.plan["target"]) == self.plan["base_sha"],
                        "Target moved before creation. Reconcile the approved PR target.")
                attempts = self.state.get("create_attempts", 0)
                require(attempts < self.config.get("limits", {}).get("create_attempts", 2), "PR create budget exhausted.")
                self.state["create_attempts"] = attempts + 1
                self.state["create_pending"] = True
                self.save()
                match = self.app("pr-create", self.plan["branch"], payload=draft)
            self.check_pr(match, head)
            number = match["number"]
            confirmed = self.check_pr(self.app("pr-view", number), head)
            require(confirmed["number"] == number and self.fetch(self.plan["branch"]) == head,
                    "PR readback or published branch does not match the verified commit.")
        self.state.update(pr=confirmed, published_head=head, create_pending=False)
        self.stage("link_pr", "Confirmed the verified commit on the run's PR.")
        return True

    def prior(self, role, head):
        return next((round_[role] for revision, round_ in reversed(list(self.state["reviews"].items()))
                     if revision != head and role in round_), None)

    def review(self, role):
        head, base = self.state["head_sha"], self.plan["base_sha"]
        self.current_pr(head)
        round_ = self.state["reviews"].setdefault(head, {})
        previous = self.prior(role, head)
        request = {
            "pr_url": self.state["pr"]["html_url"], "base_sha": base, "head_sha": head,
            "range_start_sha": previous["result"]["head_sha"] if previous and role == "quality" else base,
            "prior_findings": [finding for finding in previous["result"]["findings"]
                               if finding["disposition"] in OPEN_DISPOSITIONS] if previous else [],
            "requirement_ids": list(self.plan["requirements"]),
            "verification": self.state["checks"][head],
        }
        if role == "quality" and previous:
            request.update(prior_review_ref=previous["job_id"], prior_coverage=previous)
        if role not in round_:
            while True:
                outcome = self.job(f"{role}-review", **request)
                if outcome is None:
                    return False
                entry, result = outcome
                review = None
                if entry["observed"] == "succeeded" and result.get("exit_code") == 0:
                    try:
                        review = json.loads(artifact(result, "result.json").read_text())
                    except (Pause, ValueError):
                        pass
                if review_matches(review, role, request):
                    break
                self.state["rejected_reviews"].append({"job_id": entry["id"], "expected_head": head,
                                                       "result": review})
                entry["rejected"] = True
                self.event("review_rejected", f"Rejected incomplete or stale {role} evidence.",
                           job_id=entry["id"], head_sha=head)
            round_[role] = {"job_id": entry["id"], "result": review}
            self.save()
        evidence = round_[role]
        if not evidence.get("receipt"):
            self.current_pr(head)
            review = evidence["result"]
            title = f"Agent Ops {role} review: {review['verdict']} at {head} (job {evidence['job_id']})"
            body = title + "\n\n```json\n" + json.dumps(review, indent=2) + "\n```"
            evidence["receipt"] = self.post("pr-review", evidence["job_id"],
                                            {"body": body, "commit_id": head})
            self.save()
        return True

    def post(self, operation, key, payload):
        entries = self.state["receipts"]
        if key in entries:
            if entries[key] is None:
                require(self.recovery_requested("confirm_receipt"),
                        f"{operation} has an uncertain receipt. Confirm publication before retrying.")
                self.current_pr(self.state["head_sha"])
                decision = self.host("recover", kind="receipt", operation=operation, key_id=key,
                                     pr=self.state["pr"], payload=payload, proposal=self.plan,
                                     response=self.response)
                receipt = self.post_receipt(operation, decision["receipt"])
                self.record_recovery(decision, "confirm_receipt", key)
                entries[key] = receipt
                self.save()
                self.response = None
            return entries[key]
        self.current_pr(self.state["head_sha"])
        entries[key] = None
        self.save()
        receipt = self.post_receipt(operation, self.app(operation, self.state["pr"]["number"], payload=payload))
        entries[key] = receipt
        self.save()
        return receipt

    def post_receipt(self, operation, receipt):
        require(receipt.get("id") and receipt.get("html_url", "").startswith(self.state["pr"]["html_url"] + "#")
                and receipt.get("author") == self.config["app_actor"], f"{operation} has no confirmed App receipt.")
        return receipt

    def recovery_requested(self, action):
        return (self.state["status"] == "blocked" and self.response
                and self.response.get("action") == action
                and self.response.get("request_id") == self.state["clarification"]["id"])

    def record_recovery(self, decision, action, target):
        require(decision.get("approved") is True and decision.get("request_id") == self.response["request_id"]
                and decision.get("actor") and decision.get("reference"),
                "Recovery needs an authenticated operator decision and reconciled evidence.")
        self.state["decisions"].append({
            "grant": action, "target": target, "proposal_id": self.state["proposal_id"],
            "request_id": decision["request_id"], "actor": decision["actor"], "reference": decision["reference"],
            "mode": "explicit", "recorded_at": datetime.now(timezone.utc).isoformat(),
        })

    def finish_review(self):
        head = self.state["head_sha"]
        round_ = self.state["reviews"][head]
        self.current_pr(head)
        findings = [
            {"role": role, **finding}
            for role in REVIEW_ROLES for finding in round_[role]["result"]["findings"]
            if finding["blocking"] and finding["disposition"] in OPEN_DISPOSITIONS
        ]
        if findings:
            self.count("review_repairs", 2, head)
            if self.plan.get("return_to_start_for_repair"):
                self.issue("repair-" + head)
            self.state["repair"] = {"type": "review", "findings": findings, "pr_url": self.state["pr"]["html_url"]}
            self.stage("work", "Both reviews are recorded. Dispatching one repair for their blockers.")
        else:
            require(all(round_[role]["result"]["verdict"] == "pass" for role in REVIEW_ROLES),
                    "Both current reviews need passing verdicts.")
            self.stage("finalize", "Both independent reviews passed for the current PR revision.")

    def advance(self, response):
        self.response = response
        if self.state["stage"] == "handoff":
            return
        try:
            require(all(self.config.get(key) == value for key, value in self.state["policy"].items()),
                    "Host policy or skill pins changed during the run. Reconcile the approved configuration.")
            self.inspect()
            while self.state["stage"] != "handoff":
                stage = self.state["stage"]
                if stage == "intake":
                    if not self.authorization("execute"):
                        return
                    self.stage("activate", "Execution authorized for the recorded proposal.")
                elif stage == "activate":
                    self.issue("start")
                    self.stage("bootstrap", "Linear confirmed In Progress.")
                elif stage == "bootstrap":
                    receipt = self.host("bootstrap", proposal=self.plan)
                    require(receipt.get("confirmed") is True and receipt.get("checkout") == self.plan["checkout"]
                            and receipt.get("readiness"), "Host checkout or readiness was not confirmed.")
                    require(self.fetch(self.plan["target"]) == self.plan["base_sha"],
                            "Target branch moved before dispatch. Reconcile the approved proposal.")
                    self.checkout_head(self.state["head_sha"])
                    self.state["readiness"] = receipt["readiness"]
                    self.stage("work", "Prepared the approved isolated checkout.")
                elif stage == "work":
                    if not self.work():
                        return
                elif stage == "verify":
                    if not self.verify():
                        return
                elif stage == "publish":
                    self.inspect()
                    if not self.publish():
                        return
                elif stage == "link_pr":
                    self.current_pr(self.state["head_sha"])
                    self.issue("review-" + self.state["head_sha"])
                    self.stage("quality", "Linked the confirmed PR in Linear and confirmed In Review.")
                elif stage == "quality":
                    if not self.review("quality"):
                        return
                    self.stage("spec", "Published the independent quality review.")
                elif stage == "spec":
                    if not self.review("spec"):
                        return
                    self.finish_review()
                elif stage == "finalize":
                    self.inspect()
                    head, base = self.state["head_sha"], self.plan["base_sha"]
                    self.current_pr(head)
                    check = self.state["checks"][head]
                    reviews = self.state["reviews"][head]
                    body = (
                        f"Ready for human merge review at `{head}` (base `{base}`).\n\n"
                        f"Required checks passed in `{check['job_id']}` "
                        f"({', '.join(self.plan['required_checks'])}).\n"
                        f"- Quality: pass ({reviews['quality']['receipt']['html_url']})\n"
                        f"- Spec: pass ({reviews['spec']['receipt']['html_url']})\n"
                    )
                    final_comment = self.post("pr-comment", "handoff:" + head, {"body": body})
                    self.current_pr(head)
                    self.issue("handoff-" + head, evidence=final_comment)
                    self.state.update(stage="handoff", status="handoff", clarification=None)
                    self.event("handoff", "Current evidence is posted. A human owns the merge decision.",
                               pr_url=self.state["pr"]["html_url"], head_sha=head)
                else:
                    raise Pause("Unknown checkpoint in the run record. Reconcile the installed workflow version.")
        except (Pause, AttributeError, KeyError, TypeError, ValueError, OSError) as error:
            stage = self.state["stage"]
            message = str(error) if isinstance(error, Pause) else f"{stage} has missing or unusable evidence."
            reference = self.state.get("proposal_id")
            self.wait("blocked", message, digest({"stage": stage, "message": message, "proposal": reference}))

    def snapshot(self, after):
        fields = ("schema_version", "key", "stage", "status", "proposal_id", "proposal", "head_sha",
                  "clarification", "pr")
        latest = self.state["jobs"][-1] if self.state["jobs"] else {}
        observed = latest.get("observed")
        worker = None
        if latest and observed in (None, "running", "created", "preparing"):
            worker = {key: latest[key] for key in ("id", "role", "base_sha", "head_sha")}
            worker["status"] = observed or "reserved"
        return {**{key: self.state.get(key) for key in fields}, "record": str(self.path),
                "worker": worker,
                "cursor": len(self.state["events"]),
                "events": [event for event in self.state["events"] if event["seq"] > after]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("command", choices=("start", "resume", "status"))
    parser.add_argument("issue")
    parser.add_argument("repository")
    parser.add_argument("--after", type=int, default=0)
    parser.add_argument("--response", type=Path)
    parser.add_argument("--request", type=Path)
    args = parser.parse_args()
    issue, repository = args.issue.upper(), args.repository.lower()
    if not re.fullmatch(r"PER-[1-9][0-9]*", issue) or not re.fullmatch(r"[a-z0-9_.-]+/[a-z0-9_.-]+", repository):
        parser.error("Use a PER issue key and exact GitHub owner/repository.")
    if args.response and args.command != "resume":
        parser.error("--response is for resume.")
    if args.request and args.command != "start":
        parser.error("--request is for start.")
    os.umask(0o077)
    config = json.loads(args.config.read_text())
    directory = Path(config["state_dir"]).resolve()
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    path = directory / (digest([issue, repository]) + ".json")
    lock_path = path.with_suffix(".lock")
    with lock_path.open("a") as lock:
        if args.command != "status":
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                parser.exit(75, "Another coordinator owns this run. Read status and retry later.\n")
        if not path.exists() and args.command != "start":
            parser.error("No run exists for this issue and repository.")
        coordinator = Coordinator(config, path, issue, repository)
        if args.command == "start" and not path.exists():
            if args.request:
                request = json.loads(args.request.read_text())
                if not (isinstance(request, dict) and set(request) == {"kind", "actor", "reference"}
                        and all(isinstance(value, str) and value for value in request.values())):
                    parser.error("--request needs kind, actor and reference strings.")
                coordinator.state["request"] = request
            coordinator.save()
            coordinator.advance(None)
        if args.command == "resume":
            response = json.loads(args.response.read_text()) if args.response else None
            if args.response and (not isinstance(response, dict) or not response.get("request_id")
                                  or response["request_id"] != (coordinator.state.get("clarification") or {}).get("id")):
                parser.error("The response does not match the outstanding clarification.")
            coordinator.advance(response)
        print(json.dumps(coordinator.snapshot(args.after)))


if __name__ == "__main__":
    main()
