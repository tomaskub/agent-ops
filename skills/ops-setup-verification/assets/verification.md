# Verification

<!-- Replace the placeholders with the repository's agreed values and remove this comment. Preserve guidance for other scopes. -->

Scope: <repository area and shared dependencies covered>

Setup status: <ready or incomplete, with evidence or an actionable gap>

## Run the checks

Working directory: <path relative to the checkout root>

Command: <exact invocation for this scope>

<List supported environments and link to development environment setup or existing preparation instructions. Name platform-specific prerequisites and provide the invocation, environment, and evidence source for checks that run separately.>

| Stage / check | Required or optional | Expected result and evidence location | Conditions and failure behavior |
| --- | --- | --- | --- |
| <check name and scope> | <required or optional> | <success criteria and log, report, or CI job> | <prerequisites, allowed skip conditions, and what happens on failure> |

<Describe what exit zero means, how the command reports nonzero exits, and how to tell whether later checks ran. Explain how to recover from unavailable prerequisites. Link to command definitions and relevant CI jobs when they exist.>

## Evidence for implementation and review

<Specify where ops-implement records verification and how reviewers access logs or reports. Use the repository's run-record or PR conventions. Include only evidence that can be shared without exposing secrets.>

- Tested revision: <commit SHA and whether the worktree was clean. If it was dirty, identify the tested changes and rerun on the final revision before relying on the result for review.>
- Invocation: <working directory, actual command and scope, and execution environment>
- Actual exit status: <numeric exit status, or `not run` if the command was never invoked>
- Per check: <required or optional, result, and evidence reference or reason>

Use `pass` and `fail` for checks that ran, `skipped` for an intentional omission, `unavailable` for a missing prerequisite or mechanism, and `not run` when no attempt was made for another reason. Record any reason a check could not run. Success requires evidence for all required checks, including results from their supported environment. An exception leaves the actual result and exit status intact.

## Exceptions and setup validation

<State which exceptions are permitted and who may authorize them. Record any exception separately with its approver, rationale, scope, tested revision, and follow-up.>

<Record or link the setup validation for a fresh checkout, rerun, and controlled failure. List any unverified checks or supported environments and what would be needed to exercise them.>
