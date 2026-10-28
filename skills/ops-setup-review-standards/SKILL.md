---
name: ops-setup-review-standards
description: Set up or revise a repository's code quality and spec fulfillment review policy, reviewer briefs, severity levels, and operator exceptions. Use to clarify review standards for new or existing repositories, not to review a particular change.
---

# Setup review standards

Agree and document repository policy for at least two separate reviewer agents: code quality and spec fulfillment. Keep repository choices in the target repository, defaulting to `docs/agents/review-standards.md`, and connect both root `AGENTS.md` and `CLAUDE.md` to it.

This skill writes documentation. Running reviews, implementing a review runner, configuring CI or branch protections, and installing or editing reviewer tools are separate tasks.

## 1. Discover existing policy

Resolve the target repository and read applicable instructions. Verify its Git root and available remote identity. An unborn branch or absent remote is valid for a new repository; resolve ambiguity about the target before writing.

Inspect agent entry points, contribution and coding standards, architecture and testing guidance, reviewer profiles, and local review automation. Follow links to authoritative documentation. Distinguish documented requirements from observed practices, tooling rules, and proposed defaults. Include applicable nested instructions and path-specific standards.

When present, read the repository's issue-tracking and implementation workflow documents. In this skill family, `docs/agents/issue-tracking.md` identifies the tracker and `docs/agents/issue-rules.md` owns lifecycle, checks, PR references, and completion. Reuse those sources without making prior setup skills prerequisites. A small repository can agree review policy without a configured tracker or a formal spec.

Identify the current review runner, reviewer selection, run-record convention, and relationship to CI or hosted reviews. Inspect installed review instructions when available; availability alone does not establish compatibility with the agreed policy. Discovery is complete when current rules, conflicts, missing decisions, and execution gaps are identified.

## 2. Agree the review policy

Read [policy-decisions.md](references/policy-decisions.md) for the interview checklist and proposed defaults. Prefill decisions from discovery and earlier explicit answers. Ask only unresolved questions, in related rounds with recommendations. Existing conventions are the starting proposal on reruns; change them only by agreement.

Settle the reviewer briefs and sources, severity definitions and blocking thresholds, review ranges, spec absence, operator decisions, evidence, and workflow placement. At least two distinct reviewer roles remain required. Additional specialist reviews can be included when the repository needs them.

The agreed design supports full-change spec review and incremental quality re-reviews. Spec failures block autonomous progress. Quality blocking depends on repository severity policy. The operator can explicitly authorize proceeding with blockers or without a spec; preserve the actual review result and the exception separately in the run record and PR. Repository policy cannot bypass higher-level authorization requirements or externally enforced protections.

Show the concrete policy and proposed documentation changes before writing. Proceed on agreement already supplied in the session; ask again only when new information changes the scope. If the operator chooses a draft, name each unresolved decision. Agreement is complete when every applicable checklist item is settled or explicitly left open in an agreed draft.

## 3. Write the authoritative policy

Use [review-standards.md](assets/review-standards.md) as the output starting point. Replace its instructions and placeholders with agreed values. Reuse an existing authoritative policy location when appropriate; create additional standards documents only for agreed rules that have no suitable home.

Keep review mechanics, reviewer briefs, severity policy, and exception handling together. Link coding standards, verification, issue lifecycle, and general run-record documentation at their existing authoritative locations. Document a missing run-record convention as a runner follow-up, including the required durable untracked record and PR handoff; this skill does not implement its storage.

Within the agreed scope, reconcile conflicting review instructions through narrow edits and replace duplicated policy with pointers. Preserve unrelated content, imports, symlinks, and shared files outside the repository. If a higher-level conflict prevents operation, report it as a gap rather than declaring the setup ready.

Distinguish policy status from execution readiness. Policy is `complete` when its decisions are settled and local documentation agrees, even if runner implementation is pending. Otherwise use `draft` with named open decisions. Record runner capability gaps and required follow-ups separately; installing this skill does not enforce the resulting policy.

## 4. Connect agent entry points

Ensure root `AGENTS.md` and `CLAUDE.md` both reach the policy. Preserve working delegation between them and verify the entire reference chain without creating a cycle. Create minimal local entry files when absent. For a shared external entry file, keep the shared target intact and establish a repository-local pointer using the existing supported mechanism.

Suggested pointer, adjusted for the authoritative location:

```markdown
## Code review

Before preparing reviewer instructions, reviewing changes, responding to findings, or deciding review readiness for a PR, read [Review policy](docs/agents/review-standards.md).
```

## 5. Verify and report

Check both entry-point chains and all policy links. Remove output-template instructions and resolve contradictions within the agreed scope. Check that every reviewer has a brief, standards or requirement sources, a review range, a verdict contract, and disposition rules.

Walk the agreed policy through an initial review, a fix followed by incremental quality and full spec re-review, an advisory finding, an operator override of a blocker, and work without an issue or spec. Confirm that earlier unresolved findings remain visible, exceptions reach the PR, and an unassessed requirement cannot become a pass. A changed revision needs updated review coverage and applicable exception decisions.

Report files changed, agreed reviewer roles and thresholds, verification, policy status, and runner follow-ups. This setup configures future reviews; it does not certify a particular implementation or create demonstration runs, commits, or PRs.
