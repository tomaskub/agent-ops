# Local Markdown

## Storage and identity

Propose Git-tracked `issues/` at the repository root. Confirm the path, filename and ID convention with the user. The default is `issues/<uuid>.md`, using a new UUID v4 per record. Generate UUIDs with a standard local facility; preserve existing IDs and files on reruns. Check for an existing path before writing and use exclusive creation when creating new records. Regenerate on a collision instead of overwriting.

An ID remains unchanged when a title or status changes. Resolve relationships by ID rather than title or directory nesting. For cross-repository references, include the canonical repository identity or URL along with the record ID. Avoid machine-specific absolute paths.

Inspect existing records before choosing a schema. Treat any conversion of existing IDs or records as a separate migration. A repository without a remote can still use local tracking; confirm a durable repository identity for references.

## Proposed record format

Document the confirmed schema and a reusable example in `docs/agents/issue-tracking.md`. This is an example, not a work item to create during setup:

```markdown
---
id: "<uuid-v4>"
type: "task"
title: "<title>"
status: "backlog"
labels: []
parent: null
depends_on: []
---

## Description

<Problem and intended outcome.>

## Acceptance criteria

- <An observable completion condition.>

## References

<Specification, related records, and PR links when applicable.>
```

Quote free-text YAML strings, and serialize values safely. Use `null` for no parent and an empty list for no dependencies/labels. `type` defaults to the confirmed subset of `feature`, `issue`, `task`, and `bug`; explain any chosen story/flow level. Include the confirmed exceptional status values and optional duplicate-link field from the interview in the schema. Add only agreed custom fields, with explicit types and unset behavior. An optional assignee uses the repository's chosen identity convention.

Use parents for scope containment and dependencies for blocking relationships. Check that local references resolve and do not create parent or dependency cycles. A feature record can link a specification and child records without duplicating their changing status in a separate index.

## Setup verification

Create the agreed storage directory. If it is empty, include `.gitkeep` so Git can retain it; this is not a demonstration issue. Check Git ignore rules for both the directory and Markdown records. Resolve ignored storage with the user before calling setup complete. Git-tracked storage is the durability mechanism; actual commits follow the user's normal workflow rather than being created automatically by this skill.

Record the path, ID convention, schema, allowed values and how agents find a record by ID. Required platform IDs are not applicable. Apply the agreed status and metadata rules to Markdown fields just as with a hosted tracker.
