# Issue tracking

<!-- Output template: replace guidance and placeholders; remove these comments. -->

Setup state: <complete or draft>

## Authority and repository

This document is authoritative for tracking identities and configured values. Read [Issue scopes](issue-scopes.md) for decomposition and [Issue rules](issue-rules.md) for operating policy. The selected backend is authoritative for work records and their current state.

| Setting | Confirmed value |
| --- | --- |
| Backend | <linear, jira, github, or local> |
| Canonical repository identity | <credential-free host/owner/repository or confirmed local identity> |
| Remote used for identity | <remote name, or not applicable> |
| Remote repository name | <name independent of checkout directory> |
| Repository membership selector | <label/component/field/repository identity, with its scope> |
| Access method | <available connector, authenticated CLI/API, or local files; no secrets> |

## Backend identifiers

<!-- Include only applicable rows: workspace/site; team ID/key; project ID/key/owner/number;
repository ID; repository label/component/field ID and scope; existing feature containers.
For future feature containers, record the creation/selection rule, not a fabricated ID.
Record source and verification date for each inventory or group. -->

| Resource | Exact name/key | Stable ID or canonical path | Scope/URL | Verification source and date |
| --- | --- | --- | --- | --- |
| <resource> | <name/key> | <ID/path> | <scope/URL> | <read-back source and date, or unverified> |

## Workflow mappings

<!-- Keep type-specific workflows, project lifecycle and issue state distinct. Include
native transition IDs where required. Semantic criteria belong in issue-rules.md. -->

| Semantic stage | Object/workflow | Exact native value | Status/option ID | Transition ID or mechanism |
| --- | --- | --- | --- | --- |
| <stage> | <object/type> | <native value> | <ID or not applicable> | <transition/mechanism> |

Verification source and date: <source/date or unverified>.

## Label and field registry

<!-- Exact configured values and native schema live here. Label meanings and field
population requirements belong in issue-rules.md. Explicitly state when no fields exist. -->

| Label | Native ID if exposed | Scope | Verification source and date |
| --- | --- | --- | --- |
| <label> | <ID or not applicable> | <scope> | <source/date or unverified> |

| Field/key | Target and scope | Native ID | Type | Allowed values and option IDs | Default/unset behavior |
| --- | --- | --- | --- | --- | --- |
| <field> | <object/scope> | <ID or not applicable> | <type> | <values or unrestricted> | <default/unset> |

Field verification source and date: <source/date or not applicable>.

## Local storage

<!-- Local backend only: confirmed path, Git inclusion, UUID/filename convention,
frontmatter schema, example, and ID lookup. Remove for hosted backends. -->

<Confirmed local storage contract.>

## Open decisions and verification

<None, or each unresolved decision/resource, observed versus proposed value, failed or unverified operation, affected work, and next action.>
