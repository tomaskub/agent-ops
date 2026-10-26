# GitHub Issues and Projects

## Discover

Verify the host, owner/repository identity and ID, Issues availability, labels, issue types if available, and relevant issue/PR automation. If a Project is used, identify its owner, URL, number and API ID, fields and options, repository membership filters, and workflows. A repository name or project number alone is not a globally unique identity.

## Proposed organization

- Represent a feature with a parent issue containing or linking the specification.
- Give independently tracked work its own issue; use native sub-issue relationships where supported.
- A GitHub Project is optional organization/workflow configuration. Do not copy the Linear convention that every feature must be a Project.
- Repository membership is inherent in the issue's owning repository. Shared Project views can filter by repository without adding a redundant repository label.
- Use `owner/repo#number` or a full issue URL for cross-repository references. Bare issue numbers are local to a repository.
- Draft Project items lack the repository issue identity required for implementation records. Convert or create real issues when work enters that scope, as part of an authorized work-creation request.

Confirm whether issue types are available and useful. If a desired type is unavailable, agree a label or another representation rather than promising an organization-wide type change.

## Statuses and custom fields

Distinguish the issue's open/closed state and close reason from the Project item's workflow status. Record both mappings and any automation joining them. A Project's own health/status is a third concept, not an issue lifecycle field.

With Projects, map the five semantic stages to a verified status field and its options. Field/option IDs and project item IDs differ from the issue ID; document how to obtain each identity when updating an issue's membership or field values. Custom Project fields apply to items in that Project. Where organization issue fields are available, distinguish their scope and IDs from Project fields.

Without Projects, offer a confirmed convention such as mutually exclusive `status:backlog`, `status:todo`, `status:in-progress`, and `status:in-review` labels while issues are open; issue closure with the appropriate reason represents completion or cancellation. These labels extend the allowed label set only if the user accepts them. Agree how duplicates, reopening, and closing remove or change lifecycle labels. Never imply native Issues state supports five arbitrary statuses.

Project fields and workflows affect other repositories using that Project. Expose that shared scope before editing. Discover existing PR closing behavior and Project automations before proposing any changes.

## Official references

- [Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Project fields](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields)
- [Sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)
