# Issue rules

<!-- Output template: replace guidance and placeholders; remove these comments. -->

Policy decisions: <confirmed or draft, with unresolved decisions listed below>.

Use [Issue tracking](issue-tracking.md) for exact configured values and IDs and [Issue scopes](issue-scopes.md) for work levels. Apply these rules only to the configured repository scope.

## Lifecycle

<!-- List only agreed semantic stages; native value mappings live in issue-tracking.md. -->

| Stage | Entry/readiness criterion | Exit/completion evidence |
| --- | --- | --- |
| <stage> | <criterion> | <evidence> |

Initial stage: <stage and any type-specific exception>.

| Allowed transition | Trigger | Responsible actor or automation | Required evidence or human decision |
| --- | --- | --- | --- |
| <from → to> | <event> | <actor> | <condition> |

<How blocked, canceled, duplicate, reopened and review-returned work is represented. Preserve cancellation versus successful completion. State any human gates.>

## Allowed labels

| Label | Meaning | Apply when | Remove when | Requirements/conflicts |
| --- | --- | --- | --- | --- |
| <label from registry> | <meaning> | <trigger/actor> | <trigger/actor> | <constraints> |

<Repository-label requirement if applicable, and the process for agreeing additions to the allowed set.>

## Required content and metadata

<Minimum issue content by scope: intended outcome, boundaries, acceptance criteria, specification and dependency links as applicable.>

| Field or native property | Applies to | Required when | Set/change responsibility |
| --- | --- | --- | --- |
| <field from registry or native property> | <types> | <stage/event or optional> | <actor/value selection rule> |

<Assignee, priority and estimate policies, including explicit optional/unassigned choices. Custom field types, defaults and value inventories live in issue-tracking.md.>

## Automation and human intervention

<Existing and agreed automation, exact triggers and effects, PR references/closing behavior, and which transitions agents perform themselves. Explain how hitl pauses dependent action and how to request and record human input using the existing authorized process.>

## Configuration drift and incomplete setup

When the live tracker disagrees with a documented identifier, mapping, or rule needed for an operation, verify the discrepancy and reconcile it with the user before that operation. Continue unaffected work. Preserve established choices until a revision is agreed.

Required unresolved configuration in [Issue tracking](issue-tracking.md) blocks operations that depend on it. Report the missing decision or access and the next action rather than inventing a value or silently switching backends.

## Open decisions

<None, or unresolved policies and their effect on agents.>
