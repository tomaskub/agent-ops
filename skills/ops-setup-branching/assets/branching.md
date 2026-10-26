# Branching policy

<!-- Output template: replace guidance and placeholders; remove these comments. Omit sections and rows that do not apply. -->

Policy status: <complete or draft>.
Repository scope: <verified repository identity and any path-specific scope>.
Effective from: <agreed point; include transition exceptions below when applicable>.

Use [Issue tracking](issue-tracking.md) for tracker identifiers, [Issue scopes](issue-scopes.md) for work and parent relationships, and [Issue rules](issue-rules.md) for review gates, PR references, automation, and issue completion.

## Strategy

<Selected strategy, rationale, integration destination, release cadence, and any supported release lines. State whether integration branches and stacks are enabled, conditional, or unused.>

Hosting default branch: <observed value, planned value for a fresh repository, or unverified>.
Normal PR target: <agreed branch>.

## Branch names and roles

Ordinary work pattern: <agreed pattern>.
Identifier mapping: <configured backend's exact branch-safe identifier rule>.
Summary and collision rules: <case, separators, length, existing-name checks, and suffix policy>.

| Prefix or structural name | Purpose | Identifier requirement |
| --- | --- | --- |
| <agreed prefix or name> | <purpose> | <canonical identifier or structural exception> |

<Illustrative valid names using the configured identifier format. Explain how missing identifiers are resolved through the configured issue workflow.>

| Branch role or pattern | Starts from | PR destinations | Owner | Completion and retention or cleanup |
| --- | --- | --- | --- | --- |
| <persistent or temporary role> | <base or initial establishment> | <targets or not applicable> | <responsible actor> | <completion criteria and dependencies to preserve> |

## Merge methods and updates

| Source role | Target role | Merge method | Required validation and follow-up |
| --- | --- | --- | --- |
| <allowed source> | <allowed target> | <squash, merge commit, or rebase merge> | <existing gate reference and propagation requirement> |

<Allowed branch update methods, shared-history coordination, conflict responsibility, force-push authorization, and validation after target or history changes. Identify the allowed flows; resolve exceptions before using an unlisted source/target pair.>

## Dependent work

<Whether work normally waits for merged prerequisites. If stacks are used, state final destination, immediate PR targets, tooling, merge order, parent-boundary handling, retarget/replay rules, final-target checks, and branch retention.>

## Integration and release flows

<For selected integration or epic branches, describe child integration, updates from the persistent integration branch, final acceptance, and final merge. For Gitflow, also give release and hotfix origins, every required destination, synchronization order, and how active or maintained release lines receive fixes. Reference existing release authorization rather than implying deployment permission.>

## Cleanup

<When completed branches can be removed, who does so, and how open PRs, descendants, releases, and worktrees are checked. Identify branches that remain persistent or supported.>

## Enforcement observations and actions

<Distinguish agreed policy from actual hosting enforcement. An unavailable observation is unverified; an unapplied recommendation is planned. These statuses are separate from policy completeness.>

| Setting or capability | Agreed requirement | Observed state | Source and verification date | Follow-up and owner |
| --- | --- | --- | --- | --- |
| <merge options, branch protections, CI target, stack tooling, or default branch> | <policy> | <verified, mismatch, unverified, or not applicable with detail> | <credential-free source and date, or unavailable> | <action or none> |

## Transition

<Include only for a strategy change. State which work follows old or new rules and when. Existing branch names remain valid during transition. Preserve current policy separately from temporary exceptions.>

| Affected branch, PR, stack, or release class | Transition action | Owner | Verification or retirement condition |
| --- | --- | --- | --- |
| <affected work> | <finish under old rules, retarget, replay, propagate fixes, or retire later> | <actor> | <evidence> |

<Hosting and CI follow-ups, dependencies, and recovery plan. Mark inaccessible open-work inventory explicitly rather than claiming it is empty. This document does not execute the migration.>

## Open decisions

<None, or each unresolved decision, its affected operation, and the next action. Enforcement actions already listed above need not be duplicated as unresolved policy.>
