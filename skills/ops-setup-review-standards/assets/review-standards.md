# Review policy

<!-- Output template: replace instructions and placeholders with agreed values, then remove this comment. Reuse an existing authoritative policy file when appropriate. -->

Policy status: <complete or draft>.
Repository scope: <repository identity and applicable path-specific rules>.
Execution readiness: <ready, pending runner changes, or unverified, with follow-up links>.

## Sources and responsibilities

<Link authoritative coding, architecture, testing, contribution, tracker, and workflow documents that actually exist. Identify applicable nested instructions and any agreed source precedence. Keep lifecycle and general verification rules at their existing locations.>

| Reviewer | Profile or policy brief | Authoritative inputs |
| --- | --- | --- |
| Code quality | <existing profile link or brief below> | <standards and relevant verification sources> |
| Spec fulfillment | <existing profile link or brief below> | <issue/spec discovery and explicit clarifications> |

<Add specialist reviewers only when agreed. Each core reviewer uses a separate agent and produces a separate result against the same current reviewed revision.>

## Code quality brief

<Agreed scope covering correctness, maintainability, security, test adequacy, relevant performance, and repository standards. Distinguish adopted rules from judgment calls and explain treatment of findings already reported by tooling.>

| Tier | Agreed definition and useful repository examples | Blocking? |
| --- | --- | --- |
| Major | <confirmed definition> | <yes or no> |
| Minor | <confirmed definition> | <yes or no> |
| Nit | <confirmed definition> | <yes or no> |

<Use existing severity names instead when agreed, mapping every tier to blocking behavior.>

## Spec fulfillment brief

<How to locate the applicable issue, acceptance criteria, linked spec, and operator clarifications. An issue can be the spec. Check every applicable requirement for missing, partial, incorrect, or unverified implementation and unjustified scope expansion. Record requirement-level evidence and verification limits. Unmet spec requirements are blocking.>

## Review ranges and re-reviews

Implementation base: <how the runner captures the fixed base SHA>.
Current reviewed revision: <how the runner captures the fixed current SHA>.

| Review | Required coverage |
| --- | --- |
| Initial quality | Full change from implementation base to current reviewed SHA. |
| Quality re-review | New commits since the previous quality-reviewed SHA, plus verification of earlier unresolved findings. Retain earlier coverage and dispositions. |
| Spec, every round | Full implementation change at the current reviewed SHA against all applicable requirements. |

<Agreed recovery for missing review evidence or rewritten history. Explain that changed revisions need updated coverage and affected exceptions need reconsideration.>

## Findings and verdicts

<Define the finding fields: stable ID, reviewer role, location, evidence, violated requirement or concrete risk, quality tier when applicable, blocking status, and disposition. Define fixed verification, evidence-based rejection, advisory findings left open, and operator overrides.>

<Keep separate verdicts for each role. Pass means no unresolved blockers and sufficient evidence, and can include advisory findings. Fail means blockers remain; unverified identifies insufficient assessment evidence. Not assessed applies to authorized work without a usable spec. An exception does not convert fail or not assessed into pass.>

## Operator decisions and missing requirements

<Blocking findings stop autonomous progress until resolved or explicitly overridden by the operator. State who acts as operator. Preserve the finding and record the decision, rationale, actor, time, and applicable revision/scope. A driving agent's rejection requires evidence that a finding is incorrect or inapplicable. Accepting a valid issue needs an operator override.>

<For ambiguous requirements, clarify or obtain an explicit decision. With no usable issue or spec, offer clarification or an acceptance checklist, but allow explicit authorization to proceed without either. Record the absent source and not-assessed spec result. Quality review still applies.>

## Run record and PR handoff

Run-record convention: <link to existing documentation, or state that storage is pending runner implementation>.

<Require a durable untracked run record containing task identity or description, captured criteria or source version, fixed base and reviewed SHAs, review ranges, reviewer identities, both verdicts, findings, dispositions, verification limits, and operator decisions with rationale. Link earlier rounds for incremental quality coverage. Leave general schema and storage mechanics with the implementation workflow.>

<Require PR-visible review outcomes, remaining findings and dispositions, verification limits, and operator exceptions including authorization to proceed without a spec. Include the substantive decisions and rationale in the PR; a local untracked-file link alone does not communicate them.>

## Workflow and execution follow-ups

<Agreed placement of reviews and operator decision points. Link existing verification, issue lifecycle, CI, hosted review, PR approval, and publication rules. Separate review policy from actual enforcement and unrelated merge or deployment permissions.>

| Runner capability or integration | Observed support | Follow-up |
| --- | --- | --- |
| <separate reviewers, distinct review ranges, severity policy, operator decisions, or durable evidence/PR handoff> | <verified support, gap, or unverified> | <action and owner, or none> |

## Open decisions

<None, or unresolved policy decisions with their affected operation and next action. Keep runner implementation follow-ups distinct from policy completeness.>
