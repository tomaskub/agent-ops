# Review policy decisions

Use this checklist during discovery and agreement. Defaults are proposals, not requirements to impose on an established repository. Confirm or revise definitions and thresholds during setup, including when the operator accepts all defaults together.

## Reviewer roles and sources

Require separate code quality and spec fulfillment agents with separate briefs and verdicts. They can run concurrently against the same pinned current revision. Keep their results distinguishable when aggregating. Allow additional specialist reviewers without replacing either core role.

For each role, agree whether to use an existing repository profile, a workspace profile, or the brief in the repository policy. Reference existing profiles and their applicable overrides. Keep reusable execution procedures in shared skills; provider-specific agent configuration is needed only when the operator requests it.

Code quality covers correctness, maintainability, security, test adequacy, relevant performance risks, and documented conventions. Identify applicable architecture, language, testing, contribution, and path-specific standards. Link authoritative sources. Heuristics and observed practices remain judgment calls unless adopted as policy. A material defect can be reported without a written rule; its evidence must establish the risk. Avoid repeating mechanical findings already reported by tooling, while assessing behavior that passing tools cannot establish.

Spec fulfillment uses the actual issue, its acceptance criteria, linked spec, and explicit task clarifications. An issue can itself be the spec. Agree how to resolve conflicting requirements and recover the relevant source through the configured tracker or local files. The reviewer checks every applicable requirement for missing, partial, incorrect, or unverified implementation and identifies unjustified scope expansion. Requirement changes require an explicit operator decision, not a reviewer silently rewriting the task.

## Quality severity and blocking

Offer these defaults and ask the operator to confirm or change both meanings and thresholds:

| Tier | Proposed meaning | Default effect |
| --- | --- | --- |
| Major | A demonstrated defect, material security or reliability risk, or substantial maintainability problem with a concrete impact. | Blocking. |
| Minor | A bounded quality problem with limited impact. | Advisory. |
| Nit | A cosmetic preference or small readability improvement. | Advisory. |

Ask for repository-specific examples when the boundary is unclear. An unsupported stylistic preference does not become major because a reviewer dislikes it. Preserve established severity names if they are already useful, with an explicit mapping to blocking behavior.

Spec failures are blocking independently of the quality tier. Missing evidence yields an explicit unverified result and an operator decision, rather than a pass. Keep configured test/check gates in their existing verification or issue-rules documents; review policy links their treatment of unavailable, flaky, or preexisting failures.

## Revision coverage

Use pinned commit SHAs for the implementation base, the current reviewed revision, and the previous quality review. Compare the exact agreed endpoints rather than moving branch names.

- Initial quality review covers the implementation base to the current reviewed revision.
- Quality re-reviews cover the previous quality-reviewed revision to the current one and verify earlier unresolved findings. Context may be read to assess a change; a full quality re-review is not required on every round.
- Spec review always assesses the full implementation change at the current reviewed revision against all current requirements, including behavior outside the latest fix diff.

Carry forward quality coverage and finding dispositions from earlier rounds; a clean latest diff alone does not erase an earlier blocker. Agree how to recover when prior review evidence is missing or rewritten history prevents a valid incremental range. Propose a new initial quality review for such a gap. A changed head needs new coverage; exceptions apply to the recorded scope and revision and require reconsideration when affected code or requirements change.

For an unborn repository, document handling of the first root-commit comparison as a runner follow-up. Policy setup can finish without creating a commit or fabricating review endpoints; execution readiness depends on the runner establishing valid coverage.

## Missing spec and operator authority

Keep these cases separate:

- A usable issue or spec exists: perform the spec review. A formal standalone spec is optional.
- Requirements exist but are ambiguous: ask for clarification or present the uncertainty for an explicit operator decision.
- Neither a usable issue nor spec exists: offer clarification or a small acceptance checklist, while allowing the operator to authorize proceeding without either. Record spec review as `not assessed`, the missing source, and the operator's decision. Keep quality review required.

Blocking means autonomous progress stops for resolution or an explicit operator decision. The operator may authorize proceeding with any review blocker. Record who decided, when, what finding or missing assessment was accepted, the applicable revision/scope, and the rationale. Preserve failed or unassessed review results separately from permission to proceed.

The driving agent can reject a finding with evidence that it is incorrect or inapplicable. Retain the finding and rejection rationale for PR visibility. Accepting a valid known defect or unmet requirement is an operator override, not a rejection. Lower-tier advisory findings can be left unresolved under the agreed policy without prompting for an override on each nit.

## Review evidence and handoff

Require enough information in the durable untracked run record to resume review and explain readiness:

- Repository and task identity, or task description when no issue exists; requirement sources and the version or captured criteria reviewed.
- Implementation base, current reviewed SHA, each review's exact range, reviewer role/profile, and links to earlier rounds.
- Separate quality and spec verdicts: `pass`, `fail`, or `unverified`; use `not assessed` for an explicitly authorized absent spec. Advisory findings can accompany a pass.
- Findings with stable identifiers, role, location at the reviewed revision or missing-behavior location, evidence, violated requirement or concrete risk, quality tier where applicable, and blocking status.
- Dispositions such as open, fixed with verification, rejected with evidence, advisory left open, or accepted by operator override. Link each exception to its decision and retain its scope and rationale.
- Verification evidence and limits, remaining blockers, and the decision governing progression.

Link an existing run-record convention instead of defining another schema. If none exists, identify durable untracked storage and PR handoff as a runner prerequisite without inventing a path or implementing storage in this setup. Do not use chat history as the only record. PR content must carry both review outcomes, outstanding findings and dispositions, verification limits, and operator exceptions with rationale. An untracked local path alone is insufficient for PR readers.

## Workflow placement and readiness

Agree where these reviews inform the implementation workflow and where blocking findings stop autonomous progress. Proposed placement is after relevant verification and before PR creation. The operator retains the explicit exception authority described above. Inspect existing CI, hosted reviews, issue transitions, and publication rules; document their relationship and preserve their own gates and permissions.

Review setup changes documentation. Configuring external enforcement and implementing the runner are separate tasks. Policy can be complete with named runner follow-ups; execution is ready only when the selected runner can honor it.

When considering Matt Pocock's `code-review` skill, inspect the installed version. Its two-axis parallel review design is useful, but the version inspected during this skill's design allowed skipping Spec without an operator decision, used a whole-change range for both roles, and did not define this severity, verdict, or durable evidence contract. Treat these as compatibility checks, not assumptions about every version. Do not modify the installed copy or claim compatibility merely because it has two reviewers. A maintained runner adaptation is a separate deliverable.
