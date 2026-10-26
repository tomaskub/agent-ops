# Jira

## Discover

Confirm the Jira site and deployment type, project ID and key, actual issue types and hierarchy, applicable workflows/transitions, resolutions, field contexts, and automation. Use the selected installation's current capabilities; Cloud examples are not a promise about another deployment.

Ask how repository membership is represented within a shared Jira project, such as an existing component, label, or field. Prefer an existing convention; otherwise propose a repository label based on the remote name and confirm it. Keep repository identity separate from the Jira project key.

## Proposed scopes

| Semantic scope | Proposed native representation |
| --- | --- |
| Complete feature | Epic |
| User flow | Story |
| Standalone technical change | Task |
| Work inside a story/task | Sub-task, when enabled |
| Defect | Bug, with an optional feature parent |

In Jira's default hierarchy, Story, Task, and Bug are peers beneath Epic; a Task is not a child of a Story. If the user calls story implementation work a "task," map that semantic level to Sub-task where available, or agree an explicit issue link. Record semantics and native type separately. Verify any custom hierarchy before promising parentage.

Confirm specification placement and the parent-completion rule. A feature normally uses its Epic as its record; create an additional container only when the user chooses it.

## Workflow and metadata

Map semantic stages to actual statuses and allowed transitions for each applicable issue type. Record both status and transition identifiers where exposed: changing an issue's status may require executing a valid transition. Capture required fields and resolution behavior for closing, cancellation, duplication, and reopening.

Identify whether workflows, schemes, custom fields, contexts, or option sets are shared. Propose a repository convention or an appropriate existing configuration before changing shared administration. Create fields only within the agreed scope and verified capability. Record native field IDs, types, contexts, allowed values and option IDs, distinguishing display names from API keys.

Record project ID/key/site, issue type IDs and hierarchy, repository selector, status and transition inventories, and custom field/context identities. Sprint or board configuration is optional; inspect it only when the chosen process uses it.

## Official references

- [Default issue types and hierarchy](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/)
- [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)

Use the deployment's matching documentation for non-Cloud installations.
