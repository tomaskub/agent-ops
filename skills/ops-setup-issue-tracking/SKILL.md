---
name: ops-setup-issue-tracking
description: Set up or revise a repository's durable issue tracking in Linear, Jira, GitHub Issues with optional Projects, or local Markdown. Interview the user, configure the agreed setup, and document it for coding agents. Use for tracking configuration, not routine issue execution.
---

# Setup issue tracking

Establish one authoritative tracking backend for the selected repository. Keep all project-specific choices in that repository, outside this installed skill.

Produce these documents and connect both root agent entry points to them:

- `docs/agents/issue-tracking.md`: verified platform identity, IDs, keys, exact values, and access method.
- `docs/agents/issue-scopes.md`: work levels, meanings, decomposition, and supported relationships.
- `docs/agents/issue-rules.md`: lifecycle, labels, required metadata, automation, and agent operating rules.

## 1. Discover

Resolve the target repository from the request and environment. Inspect its instructions, existing tracking documents, issue templates, and relevant automation. Verify the Git root and selected remote. Use the existing configuration as the starting proposal on reruns.

Prefer `origin` as the proposed remote. Derive the remote repository name from its final path component, removing a trailing slash and `.git`. For `git@host:owner/B.git` or `https://host/owner/B.git`, the name is `B`, even when the checkout is named `A`. Confirm fork/upstream ambiguity, multiple candidate remotes, or absent remote identity with the user. Store a credential-free canonical remote identity.

Discover available tracker connectors and use their relevant read capabilities first. Use an authenticated CLI or API when connectors lack a needed operation; inspect current tool schemas or official documentation rather than inventing commands. Record capabilities and access gaps. Never store credentials in the generated documents.

Read [interview.md](references/interview.md) for the decision checklist and defaults. Once the backend is selected, read only its guide:

- [Linear](references/linear.md)
- [Jira](references/jira.md)
- [GitHub Issues and Projects](references/github.md)
- [Local Markdown](references/local.md)

Discovery is complete when existing choices, live configuration that can be inspected, and unresolved decisions are identified. Inaccessible configuration remains explicitly unverified.

## 2. Agree the setup

Interview in small rounds, asking related decisions together and giving a recommended answer for each. Present existing settings for confirmation or change, even when all three documents already exist. Earlier explicit choices in this setup session count as answers; avoid asking the same decision again.

Cover every applicable item in the interview checklist. Offer defaults as proposals, adapting them to the selected backend's actual capabilities. Show a concise configuration summary containing repository identity, backend/container, scopes, statuses, labels, custom fields, and automation. Distinguish observed values, proposed changes, and unresolved items.

Before applying changes, obtain agreement on this concrete setup. Identify the scope and consumers of shared team, project, organization, or workspace changes. If the user already authorized the exact changes, proceed within that scope. Treat tracker migrations, destructive changes, and changes to existing work items as separate operations; setting up tracking does not authorize moving or rewriting the backlog.

Agreement is complete when the user has confirmed the configuration or explicitly chosen an incomplete draft with named open decisions.

## 3. Apply and verify

Create or update only agreed configuration. Reuse matching existing resources by verified identity and scope. After an ambiguous write result, read back before retrying so a retry does not create duplicates. If a capability, permission, or platform limitation prevents an operation, retain the successful configuration and report the missing operation precisely. Offer an actionable draft or instructions for the user; never silently substitute another backend.

Read back changed resources and capture returned IDs, keys, option IDs, and exact names. A proposed name is not a verified identifier. Local setup establishes storage and its format without creating a fictitious issue. Setup defines future feature creation rules; it creates a feature project or parent issue only when an actual feature and that creation are part of the user's request.

Do not enable automation by default. Apply only agreed automation changes, and document existing automation that agents must respect.

## 4. Write the repository documents

Use these templates as output starting points, replacing the instructions and placeholders with confirmed values:

- [issue-tracking.md](assets/issue-tracking.md)
- [issue-scopes.md](assets/issue-scopes.md)
- [issue-rules.md](assets/issue-rules.md)

For an existing setup, update the relevant sections while preserving unrelated instructions and intentional custom policies. Keep each fact or rule authoritative in one document and link to it from the others. Store configuration, not a duplicate inventory of current tickets or ticket statuses. Include source and verification date for identifier inventories.

Mark setup `complete` only when all required decisions, resources, and identifiers have been verified and the documents agree. Otherwise mark it `draft` and list each open decision, failed or unverified operation, its affected scope, and the next verification action. Distinguish user-confirmed policy from verified external configuration. Use `unresolved` for missing required data and `not applicable` for inapplicable data; never fabricate IDs. Optional absent configuration should be stated explicitly, such as no custom fields or no GitHub Project.

## 5. Wire the agent entry points

Ensure root `AGENTS.md` and `CLAUDE.md` both reach all three documents. Preserve existing symlinks, imports, and delegation. A working delegation from one entry file to the other can carry the references once; verify the complete chain and avoid circular delegation. Create minimal entry files if absent. If either is shared outside this repository, keep shared content intact and establish a repository-local reference using the supported entry mechanism.

Suggested pointer, adjusted for the entry file's relative location:

```markdown
## Issue tracking

Before planning tracked work, creating issues, or changing issue state or metadata, read:

- [Tracking configuration](docs/agents/issue-tracking.md) for backend identity and exact values.
- [Issue scopes](docs/agents/issue-scopes.md) for work levels and relationships.
- [Issue rules](docs/agents/issue-rules.md) for workflow and metadata requirements.
```

## 6. Check and report

Check that both entry points resolve to all three documents, required identities and mappings are present or explicitly unresolved, and policies use only supported configured values. Confirm local storage is included in Git when local tracking is selected. Review the diff for unrelated changes and unresolved template instructions.

Report the selected repository/backend, files changed, configuration changes made, verification performed, and outstanding actions. Describe draft setup as incomplete. Do not create demonstration tickets, commit, or publish merely to prove setup works.
