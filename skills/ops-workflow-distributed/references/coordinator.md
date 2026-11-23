# Distributed coordinator interface v1

The portable coordinator requires Python 3.10+ on a Unix host, Git, and three configured command prefixes. The host adapter supplies approved issue routing, access, lifecycle and trusted Git integration. PER-66 supplies worker execution. PER-73 supplies the GitHub App operations. Keep installation paths, project registry entries, worker images, and credentials in host configuration.

## Manual entry points and PER-71

Run the following with the installed skill directory in `$skill` and the host configuration in `$config`. Manual Hermes or Telegram requests and the PER-71 adapter use the same entry points.

```sh
python3 -B "$skill/scripts/coordinator.py" --config "$config" start PER-123 owner/repo
python3 -B "$skill/scripts/coordinator.py" --config "$config" status PER-123 owner/repo --after 0
python3 -B "$skill/scripts/coordinator.py" --config "$config" resume PER-123 owner/repo --after 12
python3 -B "$skill/scripts/coordinator.py" --config "$config" resume PER-123 owner/repo --response "$answer"
```

- `start` claims one run for a canonical uppercase PER issue key and lowercase GitHub repository. Repeated calls return the existing snapshot. Use `resume` to advance its first incomplete gate. PER-71 should validate the workspace, team, requester and route before calling `start`. Bind repeated events and follow-ups for that issue to the same approved repository and run. Optionally pass `--request FILE` with string fields `kind`, `actor` and `reference` identifying the authenticated request for host verification.
- `status` reads the most recent committed snapshot without querying external services. `start`, `resume` and `status` print one JSON snapshot. Exit 75 means another caller holds the run lock. Exit 2 covers an invalid invocation or obsolete response. A successful command can return a blocked or waiting snapshot.
- Snapshots contain `schema_version`, `key`, `stage`, `status`, `proposal_id`, `proposal`, `head_sha`, `pr`, `clarification`, `worker`, `record`, `cursor` and `events`. When a job is outstanding, `worker` includes its ID, role, SHAs and last observed status, independent of event replay. Treat snapshots as host data. Expose the relevant progress, question, approval proposal and PR link in Linear activities.
- Each event has a stable increasing `seq`, a `kind`, `stage` and `message`. Use `--after` with the last delivered sequence to replay missing progress. A request for a decision has `request_id`. `waiting_approval` includes the specific grant and the full proposed PR draft when applicable. `blocked` includes a clarification ID and diagnostic. `waiting_worker` indicates that PER-71 can resume after launcher completion. `handoff` ends coordination.
- Send an authenticated reply to `resume --response` as a JSON file with `request_id`, `actor`, `reference`, `answer`, and optional `action`. Use the authenticated provider event as the actor and reference source. The host adapter verifies the actor and response against the current proposal and outstanding request. A matching ID provides correlation. Authorization comes from the host's verified decision.
- PER-71 owns the agent session acknowledgment, activity delivery, follow-up routing, and the scheduling of approved resumes. For an operator stop, suspend automatic resumes and use the launcher's existing `cancel JOB_ID` where appropriate. Reconcile the terminal job before an authorized fresh attempt. A downstream integration owns any Done transition based on a verified human merge.

## Host configuration

```json
{
  "state_dir": "/configured/run-state",
  "host": ["/configured/host-adapter"],
  "launcher": ["python3", "/configured/worker.py"],
  "github_app": ["/configured/github-app"],
  "base_branch": "main",
  "app_actor": "configured-app[bot]",
  "skills": {
    "implement": "ops-implement@approved-pin",
    "repair": "ops-implement@approved-pin",
    "verification": "container-worker-review@1.0.0",
    "quality-review": "ops-review-quality@approved-pin",
    "spec-review": "ops-review-spec@approved-pin"
  },
  "limits": {
    "verification_repairs": 2,
    "review_repairs": 2,
    "review_retries": 1,
    "job_retries": 1,
    "dispatch_attempts": 2,
    "push_attempts": 2,
    "create_attempts": 2
  }
}
```

The limits shown are the defaults. Review retries apply per role and head. Operator-authorized job retries apply per role and head, and they also count toward the review retry limit for review jobs. Dispatch attempts apply per reserved job ID. The coordinator waits for one current job before dispatching another, and the launcher enforces the host-wide limit. Set the host worker limit to one for the initial rollout.

Use an operator-owned state directory outside the implementation checkout and worker mounts, on a local filesystem with advisory locks and atomic rename. The coordinator keeps one JSON record per issue and repository. It records proposal versions, approval provenance, stage, reserved job IDs and assignments, checks and review rounds keyed by SHA, superseded results, retries, attempted mutations and confirmed receipts. Evidence stays in launcher output or approved host storage. Use the same state directory across resumes and keep it available until handoff. A single installed route should own the checkout and job namespace for that run. Keep secrets out of all request, state, and worker files.

### Hermes enrollment defaults

The operator enrolls each repository in Hermes and grants the GitHub App access to it. Hermes maps the enrolled repository to the PER-66 project key and prepares or reuses its isolated trusted checkout. The project key is a launcher registry name that selects the Git source, worker image and verification command. Hermes supplies it at dispatch.

For an enrolled repository with confirmed App access, an authenticated delegation from an authorized requester on an eligible issue preauthorizes both `execute` and `publish`. Record the delegation and the approved route. Proceed through checkout setup and early PR publication without separate approvals for the branch plan or PR draft. The existing verification and review gates apply, and a human owns the merge. Default to `main` and check that the repository route and helper agree on the target. An explicit repository policy can configure a different target.

### Trusted host adapter

The coordinator calls `host OPERATION` with JSON on stdin and reads one JSON object on stdout. Every request includes `key: {issue, repository}`. Return a nonzero status for unavailable operations. Send concise diagnostics through operator-controlled logs.

| Operation | Inputs and expected result |
| --- | --- |
| `inspect` | Read the live issue and repo policy. Inputs include stage, saved proposal, optional initiating request, clarification and any reply. Return `{eligible: false, message}` for a blocked route, or `{eligible: true, proposal}`. Confirm eligibility, approval policy and continuity after activation. Include a material source version that ignores coordinator lifecycle writes. Before an approved bootstrap, use a read-only exact base observation. Ref updates start after authorization. |
| `authorize` | Receives `proposal`, `proposal_id`, `grant` (`execute` or `publish`), `request_id`, optional initiating request, PR `draft` and any reply. Confirm the authenticated actor and approved policy. Return `{approved: true, mode, request_id, actor, reference}` with mode `explicit` or `preauthorized`. The latter requires an operator-approved route and a qualifying request. Return `{approved: false, message}` to wait. On accepted PR draft feedback, return `revised_draft` with complete `title` and `body` for renewed approval. Keep the issue link. The coordinator retains the first passing verification evidence and review-pending note in the revised draft. |
| `issue` | Reconcile the issue and apply `start`, `review-<sha>`, `repair-<sha>` or `handoff-<sha>` with a stable `operation_id`, proposal, PR and current head. Sync only the selected issue. Use expected-state transitions and preserve human changes. At the first review transition, link the confirmed PR. At handoff, record readiness with the final PR comment receipt in `evidence`. Return `{confirmed: true, status}` only after readback. |
| `bootstrap` | Idempotently prepare or reuse the authorized branch and isolated checkout at the approved base. Inspect the task ref and preserve existing work. Run the repository's readiness procedure. Ensure the launcher project registry maps to this trusted Git source or an equivalent source containing the pinned objects. Return `{confirmed: true, checkout, readiness}` with the proposed path and sanitized evidence. |
| `integrate` | Receive the proposal, trusted PER-66 job record, report path and expected trusted head. Verify the job's source revision, checkout isolation, intended files and patch against approved scope. Inspect untracked files and symlinks as well as the diff. Apply only the inspected delta to the clean trusted branch, commit locally and record which job produced the commit. Reconcile using job ID and expected starting SHA before replay. Return `{confirmed: true, head_sha}` for the exact successor. |
| `checks` | Receive the proposal, job, command record and log path. Translate the repository's actual output to `{outcomes: {check_name: result}}`. Use `pass`, `fail`, `skipped`, `unavailable`, or `not run`. A successful process alone is insufficient evidence. An incomplete required check pauses the run. Repair starts after the required checks have all produced actual pass or fail outcomes. |
| `recover` | For an authenticated reply with `action: "retry_job"`, reconcile the terminal job and return `{approved: true, request_id, actor, reference}` for a bounded fresh attempt. For `action: "confirm_receipt"`, verify the exact App post against the PR, commit and payload and return the same decision fields plus `receipt` with `id`, `html_url` and `author`. |

The proposal contains `issue_id`, `issue_url`, `scope`, `requirements` keyed by stable criterion ID, `source_version`, `policy_version`, `project`, `branch`, `target`, `base_sha`, the absolute `checkout` path, `verification_argv`, `required_checks`, `title`, and `transitions` with the exact `from`, `start` and `review` states. Use `worker_context` for sanitized parent constraints, environment, repository instructions and role policies. Set `return_to_start_for_repair` when the configured policy calls for that transition. The proposal pins the exact issue, repository and setup. A material change after activation requires human reconciliation.

The `execute` grant covers issue activation, checkout preparation and implementation. The `publish` grant covers the first verified draft and routine updates, reviews and final comment on that same PR. Explicit approval is tied to the specific draft. A fully preauthorized route can grant both operations without a second approval round. The portable run pauses at a gate if the required result is missing or fails beyond the budget. Handle any policy-permitted exception as a separate operator decision with exact scope, revision and rationale, retaining the actual verdict.

### PER-66 launcher

The configured launcher prefix receives `status` or `run-role PROJECT --id JOB --issue ISSUE --role ROLE --base BASE --head HEAD --skill PIN`. Add `--task-file FILE` for each Codex role. The verification role uses the project's configured `role_runtime.verification` argv in `/workspace`. Match that argv to the repository's verification policy. Initial implementation starts at `BASE == HEAD`.

Use the documented project registry, role pins and digests. The launcher owns job isolation, Codex device auth, resource limits, job status and cleanup. The worker skill returns its usual handoff in `output/report.md` or review JSON in `output/result.json`. Fresh verification returns `output/command.json`, `output/verification.log` and the actual launcher exit status. The coordinator reserves the job ID before dispatch and queries `status` before submitting it. `logs`, `cancel` and `cleanup` remain launcher operations. Preserve job artifacts referenced by the run.

### PER-73 GitHub App helper

The coordinator calls the configured helper directly with `OWNER/REPO` followed by the operation below. The App installation scopes the repository and permissions. Use the helper's configured base as the PR target. Task branches must match `per-[1-9][0-9]*/[a-z0-9][a-z0-9-]*` and begin with the selected issue key in lowercase. Push takes the full verified SHA and uses a fast-forward update. Fetch updates `refs/remotes/hermes-app/BRANCH` in the trusted checkout.

| Operation | JSON stdin |
| --- | --- |
| `fetch CHECKOUT BRANCH` | |
| `push CHECKOUT TASK_BRANCH EXPECTED_SHA` | |
| `pr-list TASK_BRANCH` | |
| `pr-view NUMBER` | |
| `pr-create TASK_BRANCH` | `{"title":"…","body":"…"}` |
| `pr-review NUMBER` | `{"body":"…","commit_id":"FULL_SHA"}` |
| `pr-comment NUMBER` | `{"body":"…"}` |

The helper also supports `pr-update NUMBER` with title or body and reports merge fields via `pr-view`. The coordinator appends the final evidence with `pr-comment` to preserve any edits to the PR body. `pr-review` submits a COMMENT at the exact commit. The PR record keeps the App author and receipt for each published result. Use the existing helper setup for token issuance and rotation.

An ambiguous create is recovered through `pr-list` and `pr-view`. Require a previously persisted create intent, one matching PR, the approved source branch lookup, repository URL, App author, both SHAs, open state and matching remote head. Multiple, closed or unexpected matches pause the run. The helper exposes both SHAs and the first page of PRs for the task branch.

- If the PR target is ambiguous or a same-SHA retarget is suspected, use an authorized GitHub readback of the base branch name and compare it with the configured target. Use the same trusted readback if exact PR content needs confirmation.
- After an uncertain review or comment write, find the exact App-authored post on the PR. Match its job or handoff evidence and the reviewed commit for a review. Use the confirmed post URL, ID and author as the receipt.
- After a failed task-branch fetch, confirm repository access and look up the exact ref. Only a successful lookup that confirms absence establishes a missing branch. An access, transport or other lookup error leaves the ref unresolved. Pause and surface the error.

## Controlled verification

From the Agent Ops checkout:

```sh
python3 -B tests/distributed_fixture.py
python3 -B tests/distributed_fixture.py --keep /path/to/new-fixture-output
```

The fixture uses local Git commits and the sample repository's executable check. It scripts the PER-66 job and PER-73 App interfaces and stores a trace, job outputs, operation receipts and run records in the fixture directory. It asserts authorization before mutations, exits `1, 0, 0` on three exact revisions, one PR before reviews, and recovery after killing the caller between create and readback. It asserts separate sequential reviewer jobs, one combined repair, stale passing review rejection, a pause when a human moves the PR head, incremental quality and full spec re-review, and a human merge handoff on PR #41.
