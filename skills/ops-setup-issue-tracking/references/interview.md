# Setup interview

Use this checklist for both new setups and revisions. Prefill from discovery, show existing settings for confirmation or change, and ask only unresolved decisions. Group related questions into small rounds with recommended answers. After an answer, ask dependent questions only when they become relevant. A confirmed setting can be retained without requiring the user to retype its values.

## Repository and authority

- Confirm the repository and selected remote. Resolve fork/upstream identity or a repository without a remote. Default the short name to the remote repository name, not the checkout directory.
- Choose one authoritative backend: Linear, Jira, GitHub Issues, or local Markdown. Links to other systems are references rather than synchronized copies by default.
- Confirm the workspace/site/account and team/project/container. Ask whether this container is shared across repositories and how repository membership is identified.
- For monorepos or path-specific conventions discovered in existing instructions, confirm the boundary within this repository rather than inventing a second authority.
- On a backend change, separate the new configuration from any proposed migration of existing work.

## Scopes and organization

Offer the selected backend's preset, then confirm:

- What represents a complete feature, user flow, implementation issue, technical task, and bug? Which levels are actually used?
- Which objects are containers versus individually keyed work records? Should the feature itself have a ticket, or is its project the record?
- What parent-child and dependency relationships are permitted? How are cross-repository features and standalone maintenance represented?
- Where does the specification live, how is it linked, and what completes the parent feature?
- Are milestones, iterations, sprints, or cycles used? Default to none unless existing configuration or the user calls for them.

Default decomposition: a feature groups a complete outcome. An implementation issue is independently verifiable work, normally in one repository and suitable for one PR. Use checklists for smaller steps unless separate ownership, dependencies, or tracking justify another record. Bugs and small technical changes can stand alone. A parent completes when its full outcome is accepted, not merely when one child PR merges.

## Statuses and transitions

Offer these semantic stages, mapping to existing exact platform values where possible:

| Stage | Proposed criterion |
| --- | --- |
| backlog | Captured, not yet selected for implementation. |
| todo | Ready to start, with scope and acceptance criteria. |
| in progress | Implementation has started. |
| in review | Required review is pending. |
| done | Acceptance criteria and required checks passed; merged where applicable. |

Confirm additions, omissions, exact spelling, initial status, and any type-specific workflows. Propose `backlog` as the initial stage. Ask about blocked, canceled, duplicate, and reopened work. Proposed exception defaults:

- Blocked: keep the current stage, record the blocker using the backend's dependency relation, and pause dependent work. Use `hitl` when human input is needed.
- Canceled: use the native canceled status or non-completion close reason; for local Markdown, propose an additional terminal `canceled` value outside the normal five-stage progression.
- Duplicate: link the canonical record and use the backend's duplicate mechanism or non-completion closure. For local Markdown, propose `status: canceled` with optional `duplicate_of: "<canonical UUID>"`.
- Reopened: return to `todo` if ready, otherwise `backlog`, retaining the reason and previous evidence.

Confirm each representation against actual backend capabilities. Never map canceled work to successful completion without preserving the distinction.

For each transition, confirm its trigger, responsible actor or automation, evidence required, and any human decision. Propose normal forward progression, returning review work for changes, and reopening when required; record the actual allowed transitions. Ask about PR linking/closing syntax and configured synchronization. Default to respecting existing automation without adding another synchronization mechanism. Preserve existing branch and PR conventions; configure new ones only if requested.

Proposed transition responsibility: the planning actor moves `backlog → todo` after scope, acceptance criteria and blockers are resolved; the implementing actor moves `todo → in progress` when work starts and `in progress → in review` when the change is ready for review and required pre-review checks pass. Review feedback returns work to `in progress`. The completing actor moves work to `done` only with acceptance, required review/check evidence, and merge where applicable. Use configured automation for a transition it already owns. Default to existing repository review requirements rather than introducing a new approval role. For non-code work, use an acceptance/evidence link instead of a PR. Cancellation or duplicate closure can leave any active stage after the decision and reason are recorded.

## Labels and custom fields

Offer this label set for confirmation, with the repository identity label added when the backend preset requires it:

| Label | Proposed meaning |
| --- | --- |
| needs-triage | Needs clarification or classification. |
| ready-for-agent | Sufficiently specified for autonomous implementation. |
| hitl | A human decision or action is required before dependent work continues. |
| documentation | Identifies documentation work. |

Confirm the allowed set, scope, application/removal triggers, required combinations, and conflicts. Propose resolving `needs-triage` before applying `ready-for-agent`; `hitl` pauses dependent action regardless of readiness. Ask how human input is requested using the project's existing process. Adding a label does not itself authorize sending a message.

Propose these triggers: the planning or implementing actor applies `needs-triage` when scope/classification is missing and removes it when clarified; applies `ready-for-agent` after readiness criteria pass and removes it when those criteria cease to hold; applies `hitl` when blocked on a human decision and removes it after the decision is recorded; applies `documentation` when documentation is part of the issue's scope and removes it only if that scope changes. Default to requesting human input in the current interaction and recording the decision and reason in the work record using its normal update mechanism. Follow an existing agreed escalation process when one is present.

Default additional custom fields to none. Still ask whether any are needed. For each selected field, confirm purpose, target object, native type, allowed values, default or unset behavior, when required, and who sets or changes it. Reuse suitable native fields. If the backend cannot support it, offer an explicitly agreed representation or leave it unresolved.

Confirm ownership/assignee policy and any priority or estimate requirements. Default to unassigned, with no mandatory priority or estimate. Keep existing values unless the user agrees to change them.

Propose a minimum work record containing intended outcome and observable acceptance criteria, plus a specification/parent reference for feature work and blocking links when applicable. Add implementation scope boundaries for independently tracked work. A standalone maintenance issue needs no fabricated parent. These defaults and their backend mappings belong in the configuration summary so a user can accept them together or change individual choices.

## Apply or draft

Show the proposed configuration and changes, including the shared scope of affected resources. Confirm whether to apply it or write an incomplete draft. Name access gaps and manual actions. Every existing setting remains open to revision during this review. Proceed once agreement covers the concrete changes; ask again only when new information materially changes their scope.

After applying, distinguish successful, failed, and unverified operations. Record enough information to resume without duplicating resources or repeating settled decisions.
