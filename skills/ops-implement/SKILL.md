---
name: ops-implement
description: Implement one explicitly assigned issue or repair its current blocking findings in an approved, prepared checkout. Run repository verification and return the patch and evidence to the orchestrator.
---

# Implement one issue

Use the same workflow for a first implementation and a repair. The orchestrator owns intake, branch and checkout authorization, bootstrap, issue status, commits and revision tracking, reviewer dispatch, and PR publication or merging. Work from the issue and evidence it supplies. Use the target repository's tooling and policies in the supplied environment.

## Confirm the assignment

- Get the issue identifier, scope and acceptance criteria, target repository identity, checkout path, approved branch and base revision, and the applicable run or retry limits. For a repair, also get the current starting revision or patch and the agreed blocking findings, including evidence and the revision or patch they refer to.
- Verify the checkout's Git root, repository identity, current branch, and relationship to the approved base. Inspect HEAD and the staged, unstaged, and untracked state before editing. Resolve a mismatch, stale finding, or overlapping work with the orchestrator before making affected edits. Keep all unrelated work intact.
- Follow the target checkout's `AGENTS.md` links and applicable nested instructions. Read its issue-tracking, issue-scopes, issue-rules, branching, dev-environment, and verification policies, including any equivalent guides at other paths. Report missing or conflicting policy to the orchestrator and identify the steps it blocks.
- Confirm the checkout is ready using the documented readiness check or supplied bootstrap evidence for the assigned scope. Follow documented activation or worktree-local preparation steps included in the assignment. Send missing prerequisites or failed readiness back to the orchestrator for bootstrap recovery.

## Implement or repair

Make the smallest changes that fulfill the assigned criteria. In repair mode, address the agreed findings together where practical and check the fix against the original acceptance criteria. Tie each finding to a fix, remaining blocker, or a discrepancy for the orchestrator to resolve. Send requirement changes and scope decisions back to the orchestrator. Keep the changes in the supplied checkout for it to record as a revision.

## Run pre-review verification

Run the configured command from the documented working directory on the resulting state. Follow repository policy for additional checks or checks assigned to another environment. Record each outcome as `pass`, `fail`, `skipped`, `unavailable`, or `not run`, with evidence or the reason. Use the actual exit status and per-check evidence. An exit of zero with missing required evidence leaves verification incomplete.

If a required check fails, capture the failing check, useful output or report location, and the next action. Apply a focused fix and rerun the configured required checks when the cause is within the assignment and the orchestrator's limits allow it. Hand back any blocked or exhausted run with the last tested state and actual results. Identify required checks that remain open before review. Record any permitted, explicitly authorized exception separately from the check outcome, including approver, rationale, scope, tested state, and follow-up.

## Return the handoff

- **Scope and changes.** Give the issue, checkout, branch, approved base SHA, and starting HEAD. List changed files and identify the resulting commit or exact patch. For uncommitted results, identify the HEAD and the tested changes, including relevant staged, unstaged, or new files. Account for any pre-existing changes present during testing. Point to a patch or artifact the orchestrator can retrieve when it cannot access the checkout. Verification for the final review revision must be tied to that exact revision. Flag when the orchestrator needs to rerun checks after recording it.
- **Verification.** Give the tested revision or patch, command, working directory, environment, actual exit status or `not run`, and each check's required or optional status, result, and accessible evidence or reason. Report missing checks and any authorized exceptions separately. Keep credentials out of the handoff.
- **Acceptance and blockers.** State which criteria the changes satisfy and the disposition of each blocking finding. List remaining blockers, operator decisions, and next actions. Mark the handoff ready for review only when all required checks have passed for the resulting state or an explicit, policy-permitted exception covers the outstanding results.
