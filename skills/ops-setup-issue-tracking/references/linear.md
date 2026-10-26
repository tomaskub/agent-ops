# Linear

## Discover

Read the selected workspace and team, issue status definitions, labels and their scopes, relevant project configuration, and workflow/Git integration automations. Record stable IDs plus human-readable keys/names and URLs where available. Verify the team's issue-key prefix rather than deriving it from the repository name. Resolve ambiguous teams with the user.

## Proposed organization

- Select a team for repository issues.
- Identify repository membership with an issue label named exactly after the selected remote's repository name. A checkout `A` with remote `owner/B.git` proposes label `B`.
- Reuse that label only after verifying its scope and intended repository identity. If an identical name belongs to another repository, surface the collision and agree a disambiguation rather than silently adding a prefix.
- A feature specification is a Linear project. The project can contain work for multiple repositories and teams. The project overview or linked project document holds the specification.
- The feature project is the feature's record. Do not create a duplicate feature issue for this preset.
- Each implementation issue or independently tracked task has its own Linear issue and unique issue key, the repository label, selected team, and feature project when applicable.
- Use sub-issues only when the agreed decomposition calls for an additional issue level. Standalone maintenance does not require a dummy feature project.

Setup records the feature-project creation/selection rule. Record IDs for existing relevant projects, if any; a fresh repository needs no artificial feature project to become configured.

## Workflow and metadata

Issue workflows belong to teams; labels can have team or workspace scope. Projects have their own status lifecycle. Keep project and issue status inventories separate.

A repository-specific allowed subset or mapping can be documented within a shared team. Creating or changing team statuses affects the team, not just tickets carrying this repository's label. Present that impact before applying changes. Discuss a different team only when an independent workflow is actually needed and the user wants it.

Discover available custom field support and target objects from current tools/platform documentation. Do not assume a desired issue field exists because another tracker supports it. Document agreed unsupported fields as unresolved unless the user chooses another representation.

Capture repository label ID and scope, team ID/key, issue status IDs/categories, relevant project identity, and label/field/option IDs where exposed. Parent/sub-issue and Git automations may close work automatically; record their triggers so agents do not duplicate transitions or confuse child completion with feature acceptance.

## Official references

Consult current docs for capability or API uncertainties:

- [Teams and workflow scope](https://linear.app/docs/teams)
- [Projects](https://linear.app/docs/projects)
- [Parent and sub-issues](https://linear.app/docs/parent-and-sub-issues)
