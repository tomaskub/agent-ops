#!/usr/bin/env python3
"""Exercise the distributed coordinator through the documented subprocess interfaces."""

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
COORDINATOR = ROOT / "skills/ops-workflow-distributed/scripts/coordinator.py"
ISSUE = "PER-900"
REPOSITORY = "fixture/agent-ops-pilot"
BRANCH = "per-900/distributed-fixture"
APP_ACTOR = "hermes-bot-fixture[bot]"
CHECK = ["python3", "-B", "check.py"]
PINS = {
    "implement": "ops-implement@43a7852b2ed926794094022b87b72c8dc608b161",
    "quality-review": "ops-review-quality@18b6f427cd4ca55bf80068b796e2be667aa5ada4",
    "spec-review": "ops-review-spec@18b6f427cd4ca55bf80068b796e2be667aa5ada4",
    "verification": "container-worker-review@1.0.0",
}
PINS["repair"] = PINS["implement"]


def load(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def git(repo, *args):
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, stderr=subprocess.PIPE,
        env={**os.environ, "GIT_AUTHOR_DATE": "2026-11-23T12:00:00Z",
             "GIT_COMMITTER_DATE": "2026-11-23T12:00:00Z"},
    ).rstrip("\n")


class Fixture:
    def __init__(self, root):
        self.root = root.resolve()
        self.trusted = self.root / "trusted"
        self.trace = self.root / "trace.jsonl"
        self.data = self.root / "fixture.json"

    def log(self, action, **fields):
        with self.trace.open("a") as stream:
            print(json.dumps({"action": action, **fields}), file=stream)

    def prepare(self):
        self.trusted.mkdir()
        git(self.trusted, "init", "-q", "--initial-branch=main")
        git(self.trusted, "config", "user.name", "Fixture Host")
        git(self.trusted, "config", "user.email", "fixture@example.invalid")
        (self.trusted / "check.py").write_text(
            "from pathlib import Path\n"
            "assert Path('feature.txt').read_text().strip() == 'passing', 'sample required check'\n"
            "print('sample check passed')\n"
        )
        (self.trusted / "feature.txt").write_text("passing\n")
        git(self.trusted, "add", "check.py", "feature.txt")
        git(self.trusted, "commit", "-qm", "fixture main")
        base = git(self.trusted, "rev-parse", "HEAD")
        write(self.data, {"base": base, "state": "Todo", "approved": [], "jobs": [],
                          "remote": {}, "pr": None, "commits": {}, "posts": []})
        config = {"state_dir": str(self.root / "runs"), "base_branch": "main", "app_actor": APP_ACTOR,
                  "skills": PINS}
        for key, mode in (("host", "host"), ("launcher", "launcher"), ("github_app", "app")):
            config[key] = [sys.executable, "-B", str(Path(__file__).resolve()), mode, str(self.root)]
        write(self.root / "config.json", config)
        return base

    def host(self, operation, request):
        data = load(self.data)
        assert request["key"]["repository"] == REPOSITORY
        if operation == "inspect":
            eligible = request["key"]["issue"] == ISSUE
            return {"eligible": eligible, "message": "Expected one unblocked implementation issue.",
                    "proposal": {
                        "issue_id": "fixture-issue-900", "issue_url": "https://linear.example/issue/PER-900",
                        "scope": "Deliver the fixture sample.",
                        "requirements": {"usage": "Include a usage example."},
                        "worker_context": {"review_policy": "Treat the fixture quality finding as major."},
                        "policy_version": "fixture-policy-v1", "source_version": "fixture-issue-v1",
                        "project": "scripted-pilot", "branch": BRANCH, "target": "main",
                        "base_sha": data["base"], "checkout": str(self.trusted),
                        "verification_argv": CHECK, "required_checks": ["sample"],
                        "title": "PER-900 Deliver the fixture sample",
                        "transitions": {"from": "Todo", "start": "In Progress", "review": "In Review"},
                        "return_to_start_for_repair": True,
                    }}
        assert request["key"]["issue"] == ISSUE
        if operation == "authorize":
            response = request["response"] or {}
            if request["grant"] == "review_exception":
                if not data.get("allow_exception"):
                    return {"approved": False}
                assert request["head_sha"] == data["pr"]["head_sha"] and request["base_sha"] == data["base"]
                assert set(request["review_jobs"]) == {"quality", "spec"}
                assert {f["id"] for f in request["findings"]} == {"unclear-output", "missing-usage"}
                if response.get("request_id") == request["request_id"] and response.get("answer") == "approve":
                    return {**response, "approved": True, "mode": data.get("exception_mode", "explicit"),
                            "rationale": "The operator accepts both fixture findings."}
                return {"approved": False, "wait": True}
            if (request["grant"] == "publish" and response.get("request_id") == request["request_id"]
                    and response.get("answer") == "revise" and response.get("actor") == "fixture-operator"):
                return {"approved": False, "revised_draft": {
                    "title": request["draft"]["title"] + " with usage",
                    "body": request["proposal"]["issue_url"] + "\n\nRevised fixture scope.",
                }}
            if (response.get("request_id") != request["request_id"] or response.get("answer") != "approve"
                    or response.get("actor") != "fixture-operator"):
                return {"approved": False, "message": f"Approve {request['grant']} for this fixture."}
            if request["grant"] == "publish":
                assert "review pending" in request["draft"]["body"].lower()
            data["approved"].append(request["grant"])
            write(self.data, data)
            self.log("authorize", grant=request["grant"])
            return {**response, "approved": True, "mode": "explicit"}
        assert "execute" in data["approved"]
        if operation == "pr_target":
            pr = data["pr"]
            assert request["number"] == pr["number"]
            return {key: pr[key] for key in ("number", "base_ref", "base_sha", "head_sha")}
        if operation == "branch_ref":
            assert request["ref"] == "refs/heads/" + BRANCH
            if data.get("ref_lookup_error"):
                raise RuntimeError("Fixture exact ref lookup unavailable")
            return {"ref": request["ref"], "sha": data["remote"].get(BRANCH)}
        if operation == "post_lookup":
            if data.get("post_lookup_uncertain"):
                return {"status": "unknown"}
            matches = [post["receipt"] for post in data["posts"]
                       if post["operation"] == request["operation"] and post["payload"] == request["payload"]
                       and post["number"] == request["pr"]["number"]
                       and post["receipt"]["author"] == request["app_actor"]]
            assert len(matches) <= 1
            return {"status": "found", "receipt": matches[0]} if matches else {"status": "absent"}
        if operation == "recover":
            response = request["response"]
            assert request["kind"] == "job" and response["action"] == "retry_job"
            assert response["actor"] == "fixture-operator" and request["job"]["status"] == "succeeded"
            return {**response, "approved": True}
        if operation == "issue":
            phase = request["operation"]
            if phase == "start":
                assert data["state"] in {"Todo", "In Progress"} and not data["pr"]
                data["state"] = "In Progress"
            else:
                assert data["pr"] and data["pr"]["number"] == request["pr"]["number"]
                assert data["pr"]["head_sha"] == request["head_sha"]
                if phase.startswith("handoff-"):
                    assert request["evidence"]["author"] == APP_ACTOR
                data["state"] = "In Progress" if phase.startswith("repair-") else "In Review"
            write(self.data, data)
            self.log("issue", phase=phase, state=data["state"])
            return {"confirmed": True, "status": data["state"]}
        if operation == "bootstrap":
            assert data["state"] == "In Progress"
            if git(self.trusted, "branch", "--show-current") == "main":
                git(self.trusted, "switch", "-qc", BRANCH, data["base"])
                self.log("bootstrap")
            return {"confirmed": True, "checkout": str(self.trusted), "readiness": "fixture clean Git checkout"}
        if operation == "integrate":
            job = request["job"]
            if job["id"] in data["commits"]:
                return {"confirmed": True, "head_sha": data["commits"][job["id"]]}
            source = Path(job["repository"])
            assert git(source, "rev-parse", "HEAD") == request["expected_head"]
            assert git(self.trusted, "rev-parse", "HEAD") == request["expected_head"]
            assert git(self.trusted, "status", "--porcelain") == ""
            assert Path(request["report"]).read_text() == "Fixture patch ready for host inspection.\n"
            files = [line[3:] for line in git(source, "status", "--porcelain").splitlines()]
            assert files and set(files) <= {"feature.txt", "quality.txt", "usage.txt"}
            for name in files:
                (self.trusted / name).write_bytes((source / name).read_bytes())
            git(self.trusted, "add", "--", *files)
            git(self.trusted, "commit", "-qm", "Integrate " + job["id"])
            head = git(self.trusted, "rev-parse", "HEAD")
            data["commits"][job["id"]] = head
            write(self.data, data)
            self.log("integrate", role=job["role"], head=head)
            return {"confirmed": True, "head_sha": head}
        assert operation == "checks"
        log = Path(request["log"]).read_text()
        outcome = "pass" if "sample check passed" in log else "fail"
        assert outcome == ("pass" if request["job"]["exit_code"] == 0 else "fail")
        return {"outcomes": {"sample": outcome}}

    def launcher(self, args):
        data = load(self.data)
        if args == ["status"]:
            for job in data["jobs"]:
                if job["status"] == "running":
                    job["status"] = "succeeded"
                    job["exit_code"] = 0
                    self.log("done", role=job["role"], job=job["id"], head=job["head_sha"])
            write(self.data, data)
            return data["jobs"]
        assert "execute" in data["approved"] and not any(job["status"] == "running" for job in data["jobs"])
        operation, project, *options = args
        values = dict(zip(options[::2], options[1::2]))
        jid, role, base, head = (values["--" + name] for name in ("id", "role", "base", "head"))
        assert operation == "run-role" and project == "scripted-pilot" and values["--issue"] == ISSUE
        assert base == data["base"] and values["--skill"] == PINS[role]
        assert all(jid != job["id"] for job in data["jobs"])
        clone = self.root / "jobs" / jid / "repo"
        output = clone.parent / "output"
        output.mkdir(parents=True)
        git(clone.parent, "clone", "-q", "--no-hardlinks", str(self.trusted), str(clone))
        git(clone, "switch", "-qc", "hermes/" + jid, head)
        assignment = load(Path(values["--task-file"])) if role != "verification" else {}
        job = {"id": jid, "issue": ISSUE, "project": project, "role": role, "base_sha": base,
               "head_sha": head, "skill": PINS[role], "repository": str(clone), "output": str(output),
               "status": "succeeded", "exit_code": 0}
        self.log("dispatch", role=role, job=jid, head=head, base=base, repair=assignment.get("repair"),
                 range_start=assignment.get("range_start_sha"),
                 unresolved=[finding["id"] for finding in assignment.get("prior_findings", [])])
        if role in {"implement", "repair"}:
            if role == "implement":
                assert head == base and not data["pr"]
                (clone / "feature.txt").write_text("failing\n")
            elif assignment["repair"]["type"] == "verification":
                assert data["pr"] is None and assignment["repair"]["evidence"]["exit_code"] == 1
                (clone / "feature.txt").write_text("passing\n")
                (clone / "quality.txt").write_text("unclear\n")
            else:
                assert {f["role"] for f in assignment["repair"]["findings"]} == {"quality", "spec"}
                assert data["state"] == "In Progress"
                (clone / "quality.txt").write_text("clear\n")
                (clone / "usage.txt").write_text("Run the sample check.\n")
            (output / "report.md").write_text("Fixture patch ready for host inspection.\n")
        elif role == "verification":
            assert "--task-file" not in values
            result = subprocess.run(CHECK, cwd=clone, capture_output=True, text=True, check=False)
            (output / "verification.log").write_text(result.stdout + result.stderr)
            write(output / "command.json", {"argv": CHECK, "cwd": "/workspace", "head_sha": head})
            job.update(status="failed" if result.returncode else "succeeded", exit_code=result.returncode)
            self.log("checked", head=head, exit=result.returncode)
        else:
            assert data["pr"] and data["pr"]["head_sha"] == head and data["state"] == "In Review"
            assert assignment["base_sha"] == base and assignment["head_sha"] == head
            assert assignment["verification"]["head_sha"] == head and assignment["verification"]["exit_code"] == 0
            review = self.review(role, assignment, clone)
            if role == data.get("unverified_role"):
                review.update(verdict="unverified", findings=[], range_start_sha=None,
                              verification_limits=["Fixture review policy is unavailable."])
                if role == "spec-review":
                    review["requirements"] = []
            if role == "quality-review" and assignment.get("prior_review_ref") and not any(
                j["role"] == role and j["head_sha"] == head for j in data["jobs"]
            ):
                review["head_sha"] = assignment["range_start_sha"]
                self.log("stale-result", actual=review["head_sha"], expected=head, verdict=review["verdict"])
            write(output / "result.json", review)
            assert git(clone, "status", "--porcelain") == ""
            job.update(status="running", exit_code=None)
        data["jobs"].append(job)
        write(self.data, data)
        return job

    def review(self, role, assignment, clone):
        role = role.removesuffix("-review")
        base, head = assignment["base_sha"], assignment["head_sha"]
        if role == "quality":
            filename, identifier = "quality.txt", "unclear-output"
            fixed = (clone / filename).read_text() == "clear\n"
        else:
            filename, identifier = "usage.txt", "missing-usage"
            fixed = (clone / filename).is_file()
        result = {
            "schema_version": 1, "role": role, "base_sha": base, "head_sha": head,
            "range_start_sha": assignment["range_start_sha"], "verdict": "pass" if fixed else "fail",
            "verification_limits": [],
            "findings": [{
                "id": identifier, "location": filename, "evidence": "Fixture read of the pinned tree.",
                "severity": "major" if role == "quality" else None,
                "unmet_requirement": None if role == "quality" else "usage",
                "disposition": "fixed" if fixed else "open", "blocking": True,
            }],
        }
        if role == "quality":
            result["prior_review_ref"] = assignment.get("prior_review_ref")
        else:
            result["requirements"] = [{"id": "usage", "source": "PER-900 acceptance criterion",
                                       "status": "met" if fixed else "unmet", "evidence": "Pinned usage file."}]
        return result

    def app(self, repository, operation, args, payload):
        data = load(self.data)
        assert repository == REPOSITORY and "execute" in data["approved"]
        pr = data["pr"]
        if operation == "fetch":
            checkout, branch = args
            assert checkout == str(self.trusted)
            head = data["base"] if branch == "main" else data["remote"][branch]
            ref = "refs/remotes/hermes-app/" + branch
            git(self.trusted, "update-ref", ref, head)
            return {"ref": ref, "sha": head}
        if operation == "pr-list":
            assert args == [BRANCH]
            self.log("pr-list", found=bool(pr))
            return [pr] if pr else []
        if operation == "pr-view":
            assert args == [str(pr["number"])]
            return {**pr, "merged": False, "merged_at": None, "merge_commit_sha": None}
        assert "publish" in data["approved"]
        if operation == "push":
            checkout, branch, head = args
            assert checkout == str(self.trusted) and branch == BRANCH
            assert git(self.trusted, "rev-parse", BRANCH) == head
            if data.get("fail_push") and not data["remote"]:
                raise RuntimeError("Fixture push failed before creating the task ref")
            git(self.trusted, "merge-base", "--is-ancestor", data["remote"].get(branch, data["base"]), head)
            data["remote"][branch] = head
            if pr:
                pr["head_sha"] = head
            write(self.data, data)
            self.log("push", head=head)
            return {"ref": "refs/heads/" + branch, "sha": head}
        if operation == "pr-create":
            assert pr is None and args == [BRANCH] and set(payload) == {"title", "body"}
            head = data["remote"][BRANCH]
            assert head in payload["body"] and "review pending" in payload["body"]
            assert "Required verification passed" in payload["body"] and json.dumps(CHECK) in payload["body"]
            assert payload["title"].endswith(" with usage") and "Revised fixture scope." in payload["body"]
            pr = {"number": 41, "html_url": f"https://github.com/{repository}/pull/41",
                  "author": APP_ACTOR, "state": "open", "head_sha": head, "base_sha": data["base"],
                  "base_ref": "main"}
            data["pr"] = pr
            write(self.data, data)
            self.log("pr-create", number=41, head=head)
            # The publication exists, but the caller is interrupted before receiving its response.
            os.kill(os.getppid(), signal.SIGKILL)
            return pr
        assert args == [str(pr["number"])]
        assert operation in {"pr-review", "pr-comment"}
        if operation == "pr-review":
            assert set(payload) == {"body", "commit_id"} and payload["commit_id"] == pr["head_sha"]
        else:
            assert set(payload) == {"body"} and "human merge" in payload["body"]
            if data.get("fail_comment"):
                raise RuntimeError("Fixture comment failed before posting")
        self.log(operation, head=pr["head_sha"], body=payload["body"], number=pr["number"])
        receipt_id = len(data["posts"]) + 1
        receipt = {"id": receipt_id, "html_url": pr["html_url"] + "#" + str(receipt_id), "author": APP_ACTOR}
        data["posts"].append({"operation": operation, "payload": payload, "number": pr["number"], "receipt": receipt})
        write(self.data, data)
        if data.get("lose_review_receipt") and receipt_id == 1:
            raise RuntimeError("Fixture lost the response after posting a review")
        return receipt

    def call(self, command, issue=ISSUE, *, response=None, after=0, exit_code=0):
        args = [sys.executable, "-B", str(COORDINATOR), "--config", str(self.root / "config.json"),
                command, issue, REPOSITORY, "--after", str(after)]
        if response:
            path = self.root / "response.json"
            write(path, response)
            args += ["--response", str(path)]
        process = subprocess.run(args, capture_output=True, text=True, check=False)
        assert process.returncode == exit_code, (args, process.stderr, process.stdout)
        return json.loads(process.stdout) if exit_code == 0 else None

    def reply(self, snapshot, answer="approve", *, action=None, **options):
        return self.call("resume", response={"request_id": snapshot["clarification"]["id"],
                                              "actor": "fixture-operator", "reference": "fixture-approval",
                                              "answer": answer, "action": action}, **options)

    def configure(self, **fields):
        data = load(self.data)
        data.update(fields)
        write(self.data, data)

    def start(self):
        base = self.prepare()
        ineligible = self.call("start", "PER-901")
        assert ineligible["status"] == "blocked" and not self.trace.exists()
        waiting = self.call("start")
        assert waiting["status"] == "waiting_approval" and not self.trace.exists()
        assert waiting["clarification"]["grant"] == "execute"
        self.call("resume", response={"request_id": "obsolete"}, exit_code=2)
        assert self.call("start", after=waiting["cursor"])["events"] == []
        assert git(self.trusted, "branch", "--show-current") == "main"
        prepublication = self.reply(waiting)
        assert prepublication["status"] == "waiting_approval" and prepublication["stage"] == "publish", prepublication
        assert prepublication["clarification"]["grant"] == "publish"
        assert prepublication["head_sha"] in prepublication["clarification"]["draft"]["body"]
        assert load(self.data)["pr"] is None and load(self.data)["remote"] == {}
        revised = self.reply(prepublication, "revise")
        assert revised["status"] == "waiting_approval"
        assert revised["clarification"]["id"] != prepublication["clarification"]["id"]
        assert revised["head_sha"] in revised["clarification"]["draft"]["body"]
        self.reply(prepublication, exit_code=2)
        return base, revised

    def run(self):
        base, revised = self.start()
        self.configure(fail_push=True, lose_review_receipt=True, fail_comment=True)
        failed = self.reply(revised)
        assert failed["stage"] == "publish" and "push failed" in failed["clarification"]["message"]
        assert load(self.data)["remote"] == {}
        self.configure(fail_push=False, ref_lookup_error=True)
        blocked_ref = self.call("resume")
        assert "branch_ref exited" in blocked_ref["clarification"]["message"]
        assert load(Path(failed["record"]))["pushes"][failed["head_sha"]]["attempts"] == 1
        self.configure(ref_lookup_error=False)
        self.call("resume", exit_code=-signal.SIGKILL)
        interrupted = self.call("status")
        assert interrupted["stage"] == "publish" and interrupted["pr"] is None
        assert load(self.data)["pr"]["number"] == 41
        assert self.call("start", after=interrupted["cursor"])["events"] == []
        progress = self.call("resume", after=interrupted["cursor"])
        assert progress["status"] == "waiting_worker" and progress["pr"]["number"] == 41
        current = self.call("status", after=progress["cursor"])
        assert current["events"] == [] and current["worker"] == progress["worker"]
        assert current["worker"]["role"] == "quality-review" and current["worker"]["status"] == "running"
        assert [event["seq"] for event in progress["events"]] == list(
            range(interrupted["cursor"] + 1, progress["cursor"] + 1)
        )
        pr = load(self.data)["pr"]
        self.configure(pr={**pr, "base_ref": "same-commit-target"})
        wrong_target = self.call("resume")
        assert wrong_target["status"] == "blocked" and "target branch" in wrong_target["clarification"]["message"]
        assert load(self.data)["posts"] == []
        self.configure(pr=pr)
        lost_receipt = self.call("resume")
        assert lost_receipt["stage"] == "quality" and "pr-review failed" in lost_receipt["clarification"]["message"]
        assert len(load(self.data)["posts"]) == 1
        progress = self.call("resume")
        assert progress["stage"] == "spec" and len(load(self.data)["posts"]) == 1
        simulated_drift = False
        for _ in range(8):
            if progress["status"] != "waiting_worker":
                break
            if (progress["stage"] == "quality" and progress["head_sha"] != interrupted["head_sha"]
                    and not simulated_drift):
                original = load(self.data)
                drifted = load(self.data)
                head = progress["head_sha"]
                tree = git(self.trusted, "rev-parse", head + "^{tree}")
                new_head = git(self.trusted, "commit-tree", tree, "-p", head, "-m", "Human update")
                drifted["remote"][BRANCH] = new_head
                drifted["pr"]["head_sha"] = new_head
                write(self.data, drifted)
                before = self.trace.read_bytes()
                blocked = self.call("resume", after=progress["cursor"])
                assert blocked["status"] == "blocked" and "differs" in blocked["clarification"]["message"]
                assert load(self.data)["pr"]["head_sha"] == new_head and self.trace.read_bytes() == before
                write(self.data, original)
                simulated_drift = True
            progress = self.call("resume", after=progress["cursor"])
        assert simulated_drift and progress["stage"] == "finalize", progress
        assert "pr-comment failed" in progress["clarification"]["message"]
        self.configure(fail_comment=False, post_lookup_uncertain=True)
        uncertain = self.call("resume")
        assert "uncertain receipt" in uncertain["clarification"]["message"] and len(load(self.data)["posts"]) == 4
        self.configure(post_lookup_uncertain=False)
        progress = self.call("resume")
        assert progress["status"] == "handoff", progress
        assert self.call("resume", after=progress["cursor"])["events"] == []
        self.assert_trace(base, progress)

    def assert_trace(self, base, progress):
        events = [json.loads(line) for line in self.trace.read_text().splitlines()]
        actions = [event["action"] for event in events]
        assert actions[:3] == ["authorize", "issue", "bootstrap"]
        relevant = [event for event in events if event["action"] not in {"pr-list", "done"}]
        assert [event["action"] for event in relevant] == [
            "authorize", "issue", "bootstrap", "dispatch", "integrate", "dispatch", "checked",
            "dispatch", "integrate", "dispatch", "checked", "authorize", "push", "pr-create",
            "issue", "dispatch", "pr-review", "dispatch", "pr-review", "issue", "dispatch",
            "integrate", "dispatch", "checked", "push", "issue", "dispatch", "stale-result",
            "dispatch", "pr-review", "dispatch", "pr-review", "pr-comment", "issue",
        ]
        checks = [event for event in events if event["action"] == "checked"]
        bad, first, final = [event["head"] for event in checks]
        assert [event["exit"] for event in checks] == [1, 0, 0]
        assert [event["head"] for event in events if event["action"] == "push"] == [first, final]
        create = next(i for i, event in enumerate(events) if event["action"] == "pr-create")
        assert events[create + 1] == {"action": "pr-list", "found": True}
        assert [event["number"] for event in events if event["action"] in {"pr-create", "pr-review", "pr-comment"}] == [41] * 6
        reviews = [event for event in events if event["action"] == "dispatch" and event["role"].endswith("-review")]
        assert [(event["role"], event["head"], event["base"], event["range_start"], event["unresolved"])
                for event in reviews] == [
                    ("quality-review", first, base, base, []), ("spec-review", first, base, base, []),
                    ("quality-review", final, base, first, ["unclear-output"]),
                    ("quality-review", final, base, first, ["unclear-output"]),
                    ("spec-review", final, base, base, ["missing-usage"]),
                ]
        for earlier, later in zip(reviews, reviews[1:]):
            done = next(event for event in events if event["action"] == "done" and event["job"] == earlier["job"])
            assert events.index(earlier) < events.index(done) < events.index(later)
        record = load(Path(progress["record"]))
        assert record["pr"]["number"] == 41 and record["head_sha"] == final and record["create_attempts"] == 1
        assert record["pushes"][first]["attempts"] == 2
        assert record["post_attempts"]["handoff:" + final]["count"] == 2
        rejected, = record["rejected_reviews"]
        assert rejected["result"]["head_sha"] == first and rejected["expected_head"] == final
        assert rejected["result"]["verdict"] == "pass"
        assert load(self.data)["state"] == "In Review"
        print("Ineligible and unapproved requests left the tracker, checkout, workers and GitHub untouched.")
        print(f"Verification exits 1, 0, 0 at {bad}, {first}, {final}.")
        print(f"One PR #41 at the first passing head {first}. Resume adopted it after client interruption.")
        print(f"Sequential review pairs pinned base {base}. One combined repair advanced the same PR to {final}.")
        print("A stale passing quality result was rejected. Fresh quality covered the delta and prior finding.")
        print("A human-moved PR head paused the run without a write.")
        print("Same-SHA retargeting paused publication. Push and post retries required confirmed absence.")
        print("A lost review receipt was recovered from the existing post without reposting.")
        print("Fresh spec covered the full base-to-head change. Four App review receipts and one handoff comment.")
        print("Final state: In Review, ready for human merge.")

    def run_review_exceptions(self):
        base, revised = self.start()
        self.configure(unverified_role="quality-review", allow_exception=True)
        self.reply(revised, exit_code=-signal.SIGKILL)
        quality = self.call("resume")
        head = quality["head_sha"]
        for role in ("quality", "spec"):
            waiting = self.call("resume")
            assert waiting["stage"] == role and waiting["status"] == "blocked"
            assert "Fixture review policy is unavailable." in waiting["clarification"]["message"]
            assert self.call("resume", after=waiting["cursor"])["events"] == []
            record = load(Path(waiting["record"]))
            saved = record["reviews"][head][role]
            assert saved["result"]["verdict"] == "unverified" and saved["receipt"]["id"]
            assert record["rejected_reviews"] == []
            self.configure(unverified_role="spec-review" if role == "quality" else None)
            progress = self.reply(waiting, action="retry_job")
            record = load(Path(progress["record"]))
            job = next(job for job in record["jobs"] if job["id"] == saved["job_id"])
            assert job["superseded_review"] == saved
            assert progress["status"] == "waiting_worker"
            if role == "quality":
                assert self.call("resume")["stage"] == "spec"
        waiting = self.call("resume")
        assert waiting["status"] == "waiting_approval" and waiting["stage"] == "spec"
        scope = waiting["clarification"]
        assert scope["grant"] == "review_exception" and scope["base_sha"] == base
        assert scope["head_sha"] == head and len(scope["findings"]) == 2
        self.configure(exception_mode="preauthorized")
        blocked = self.reply(waiting)
        assert "explicit operator approval" in blocked["clarification"]["message"]
        self.configure(exception_mode="explicit")
        waiting = self.call("resume")
        assert waiting["clarification"]["id"] == scope["id"]
        progress = self.reply(waiting)
        assert progress["status"] == "handoff" and progress["head_sha"] == head
        record = load(Path(progress["record"]))
        assert [record["reviews"][head][role]["result"]["verdict"] for role in ("quality", "spec")] == ["fail", "fail"]
        decision, = [d for d in record["decisions"] if d["grant"] == "review_exception"]
        assert decision["head_sha"] == head and decision["findings"] == scope["findings"]
        assert not record["attempts"].get("review_repairs")
        comment = load(self.data)["posts"][-1]
        assert comment["operation"] == "pr-comment"
        assert all(text in comment["payload"]["body"] for text in (
            "Quality: fail", "Spec: fail", decision["rationale"], "quality/unclear-output", "spec/missing-usage",
        ))
        print("Both unverified results and their reasons were retained, then retried with operator approval.")
        print("Only explicit approval let the pinned review failures proceed to handoff with their original verdicts.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep", type=Path, help="Write trace and run records to a new directory.")
    known, subprocess_args = parser.parse_known_args()
    if subprocess_args:
        mode, root, *args = subprocess_args
        fixture = Fixture(Path(root))
        if mode == "host":
            result = fixture.host(args[0], json.load(sys.stdin))
        elif mode == "app":
            repository, operation, *args = args
            result = fixture.app(repository, operation, args, json.loads(sys.stdin.read() or "null"))
        else:
            assert mode == "launcher"
            result = fixture.launcher(args)
        print(json.dumps(result))
    elif known.keep:
        known.keep.mkdir()
        run_fixtures(known.keep)
        print(f"Fixture retained at {known.keep.resolve()}.")
    else:
        with tempfile.TemporaryDirectory(prefix="agent-ops-distributed-") as directory:
            run_fixtures(Path(directory))


def run_fixtures(directory):
    Fixture(directory).run()
    exceptions = directory / "review-exceptions"
    exceptions.mkdir()
    Fixture(exceptions).run_review_exceptions()


if __name__ == "__main__":
    main()
