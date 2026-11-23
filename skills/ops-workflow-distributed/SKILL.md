---
name: ops-workflow-distributed
description: Coordinate one authorized Linear implementation issue through isolated worker jobs, required repository verification, early PR publication, and independent PR-based quality and spec reviews. Use from a configured Hermes host or with the scripted fixture.
---

# Deliver one issue with distributed workers

Use `ops-workflow-distributed start <issue-key> <owner/repo>` for an explicit operator request or authorized delegation. Use `ops-workflow-distributed resume <issue-key> <owner/repo>` after a worker finishes, an interruption, or an authenticated clarification. Invoke [the coordinator](scripts/coordinator.py) with the configured host paths. Follow the [coordinator interface](references/coordinator.md) for status, approval and recovery.

## Resolve and authorize the issue

1. Read the selected Linear issue, criteria, relevant parent constraints, dependencies and applicable repository instructions. Confirm an eligible implementation scope and the exact approved repository. Use the repository's issue, branch, development environment, verification and review policies. Resolve any ambiguity with the operator.
2. Present the proposed issue transition, target branch, pinned starting commit, task branch and isolated host checkout. Identify any existing resources that would be reused. Persist the proposal and its authorization before changing Linear, provisioning the checkout or dispatching a job.
3. Use an authenticated operator decision or a documented, operator-approved delegation policy. The approved route can cover routine execution and early PR publication. A route requiring explicit publication approval waits with the first passing commit and the proposed PR title and body. Apply feedback to the proposal or draft, then ask for approval of the revised version.

## Verify and publish the first passing commit

1. Move the approved issue to In Progress. Prepare or reconcile its isolated checkout and follow the repository's documented environment and readiness commands. Confirm the target SHA through the PER-73 host helper.
2. Dispatch the PER-66 `implement` role with the pinned `ops-implement` skill. Host-side inspection determines the intended patch. Record it as a local candidate commit on the approved task branch.
3. Run the repository's required verification through the launcher on that exact committed state. Retain the commands, exit, per-check outcomes and evidence. A failed required check gets a focused `ops-implement` repair within the configured budget, then fresh verification. Pause for missing prerequisites or incomplete required evidence.
4. Reconcile the branch and PR through the host helper. Push the first passing SHA and create one PR with the issue link, actual check evidence and the initial review marked pending. Confirm the PR before linking it in Linear and moving the issue to In Review.

## Review, repair and hand off

1. Start a fresh `ops-review-quality` worker, then a fresh `ops-review-spec` worker. Pass both the same pinned PR base and head and current verification evidence. Review jobs receive read-only assignments. Publish role-labeled COMMENT reviews as the host App, with each review attached to the exact reviewed commit.
2. Collect both results before deciding on repair. The first quality review covers the full diff. A quality re-review covers the delta since its last valid head and rechecks unresolved findings. Spec covers the full assigned scope, including applicable parent constraints, every round. Keep findings and dispositions with their actual verdicts. A missing or stale verdict leaves the gate open.
3. Give both sets of actionable blockers to one `ops-implement` repair worker. Verify the corrected commit, push to the same PR and repeat both review gates. If policy permits and the operator explicitly approves an exception for the current revision and findings, retain the original verdicts and include the decision in the handoff. Pause if the target, head or source requirements move, a review is unverified, checks are unavailable or an attempt budget runs out.
4. When the checks and reviews cover the current PR, post final evidence on that PR and signal readiness in Linear. Leave the issue In Review and hand the merge decision to a human.

## Recover a run

Use the existing record for the exact issue and repository. Reconcile the saved job ID through launcher status and use trusted GitHub readbacks for the PR target, task ref and any pending post. Retry a write within its budget after confirming its absence. Preserve human changes and pause on conflicting or inconclusive evidence. Keep App credentials on the trusted host and use the configured launcher for workers. Recovery and fixture details are in the [coordinator interface](references/coordinator.md).
