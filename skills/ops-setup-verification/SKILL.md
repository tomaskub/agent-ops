---
name: ops-setup-verification
description: Establish or revise executable verification for a repository or selected area. Discover existing checks, agree the required checks with the operator, and exercise a repository-native verification command on a prepared checkout.
---

# Setup verification

Leave the target repository with a working verification command and instructions that implementation agents and reviewers can follow. Use this skill to establish or change those checks. Once the setup is ready, use the documented command for routine verification.

## 1. Discover existing checks

Confirm the repository, selected scope, and applicable agent and contributor instructions. Inspect manifests, task runners, test and tool configuration, environment and verification guides, and CI workflows. Trace build, test, lint, and static analysis commands to what they actually run. For a selected area, include shared dependencies when they affect the checks.

Identify each check's scope, platform and tool prerequisites, output, and failure behavior. Compare the documented requirements with what runs locally and in CI. Separate working mechanisms from missing checks, unavailable prerequisites, and proposed changes. Use existing policy and commands as the starting point on reruns.

## 2. Agree what verification covers

Use discovery and prior operator decisions to propose the scope, command and working directory, required and optional stages, and a meaningful baseline for coverage. Settle which checks can run in a prepared local checkout or a distributed worker and which require a separate supported environment. Agree evidence locations, what blocks progress, and who may authorize exceptions and under what conditions.

Show what will be reused or changed, including any missing tooling, before editing. Ask only about decisions the operator has yet to settle. Existing authorization covers the agreed changes. Treat changes to CI or hosting enforcement as a separate decision.

## 3. Establish the command

Use an adequate existing command as the entry point. Where it falls short, implement the smallest addition or change using the target repository's conventions, such as a task target or package script. Keep executable logic and project-specific configuration in that repository.

- Run the agreed checks for the selected scope and propagate any executed check failure with a nonzero exit. Use output or an existing report to identify each check's outcome. If a failed stage prevents later stages from running, make that visible.
- Distinguish an intentional skip, an unavailable prerequisite, and a check that ran and failed. Exit nonzero if a required check assigned to this invocation cannot run. Verify that a required test stage actually discovers and runs tests, even when its tool exits zero on an empty suite. Where a required mechanism or meaningful test baseline is missing, add the smallest applicable check within the agreed scope or record the setup as incomplete with a concrete next action.
- Resolve paths from the checkout or documented working directory. Run on an already prepared checkout and use the same command for a given scope and supported environment in local and distributed execution. Link to the existing setup instructions or use `ops-setup-dev-environment` for missing preparation. Keep normal local verification independent of Docker and Hermes. Document checks that need another supported environment and how to obtain their results.

## 4. Write the guide and connect agent instructions

Use [the verification guide template](assets/verification.md) to write or update `docs/agents/verification.md`. If another guide already owns the policy, use `docs/agents/verification.md` to route to it and fill any gaps at the authoritative source. Preserve existing guidance for other scopes.

Ensure root `AGENTS.md` and `CLAUDE.md` both reach the guide. Preserve working imports and delegation, and verify the full chain. Create minimal local entry files when absent. Keep shared targets outside the repository intact and use the repository's supported mechanism for a local pointer.

Define the evidence handoff for `ops-implement` and reviewers in the guide. Use the existing durable run record when available. Capture the command as run, working directory, actual exit status, tested revision, per-check results, and references to logs or reports. Record exceptions separately from observed results.

## 5. Exercise the setup and report

Use a disposable fresh clone or worktree of the target repository that includes the verification changes. Prepare it through the documented environment process. Run the exact invocation, then rerun it and check for unintended changes to tracked files, configuration, or local data. If setup is already adequate, confirm that a second setup pass finds no duplicate automation, documentation, or links.

Use a disposable example or safe test fixture to make a check fail through the real entry point. Confirm the check appears as failed and the command exits nonzero. Verify any agreed skip and unavailable behavior that can be reproduced safely. Restore only the fixture changes and confirm the successful baseline again. Leave existing checkouts, local data, and configuration intact.

Check both agent instruction paths and review the diff. Report the tested revision and evidence for the fresh run, rerun, and controlled failure. Name any unavailable prerequisite, platform, or check that could not be exercised. Mark setup incomplete if required checks are missing or their behavior remains unverified, and give the next action.
