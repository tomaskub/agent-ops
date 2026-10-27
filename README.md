# Agent operations

Reusable skills for setting up and running development workflows across repositories.

## Install

Install an individual skill with the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add tomaskub/agent-ops --skill ops-setup-issue-tracking
```

Add `-g` for installation across projects, or select agents with `-a codex -a claude-code`. To inspect the available skills first:

```sh
npx skills add tomaskub/agent-ops --list
```

To use a local checkout before publishing changes, run this from the target project:

```sh
npx skills add /path/to/agent-ops --skill ops-setup-issue-tracking
```

## Setup issue tracking

Use [`ops-setup-issue-tracking`](skills/ops-setup-issue-tracking/SKILL.md) to configure or revise a repository's durable tracking in Linear, Jira, GitHub Issues with optional Projects, or local Markdown.

The skill inspects the current setup and asks you to confirm or change its repository identity, work scopes, statuses, labels, custom fields, and workflow rules. It applies agreed configuration changes and writes:

- `docs/agents/issue-tracking.md` for platform identities, keys, and exact configured values.
- `docs/agents/issue-scopes.md` for work levels and relationships.
- `docs/agents/issue-rules.md` for workflow and metadata policy.

Both `AGENTS.md` and `CLAUDE.md` lead agents to those documents. Local tracking defaults to Git-tracked Markdown in root `issues/`. When required access or configuration is missing, the skill writes an incomplete draft with next steps.

Example request after installation, from the target project:

```text
Use ops-setup-issue-tracking to set up this repository's issue tracking.
Inspect what exists and help me confirm or change the configuration.
```

Project-specific settings stay in the target repository. Installing the skill does not configure tracking until you run it.

## Setup branching

Use [`ops-setup-branching`](skills/ops-setup-branching/SKILL.md) after `ops-setup-issue-tracking` to define or revise branch naming, trunk-based or Gitflow development, and merge strategy. Install it with:

```sh
npx skills add tomaskub/agent-ops --skill ops-setup-branching
```

The skill reads the issue-tracking documents, inspects existing conventions, and helps you agree a policy. Fresh repositories default to `main`, short-lived issue branches named `<prefix>/<issue-id>-<summary>`, direct PRs, and squash merges. Established repositories retain their conventions unless a change is agreed.

It writes `docs/agents/branching.md` and connects both `AGENTS.md` and `CLAUDE.md` to it. The policy covers branch roles, merge methods, dependent stacks, integration branches, cleanup, and release or hotfix flows when applicable. Strategy changes include a transition plan for existing work. Hosting enforcement is recorded separately; the skill changes documentation without executing Git operations or changing hosting settings.

Example request after installation, from the target project:

```text
Use ops-setup-branching to set up this repository's branching policy.
Inspect the issue-tracking documents and existing conventions, then propose defaults.
```
