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

## Setup review standards

Use [`ops-setup-review-standards`](skills/ops-setup-review-standards/SKILL.md) to establish or revise code quality and spec fulfillment review policy for a new or existing repository. Install it with:

```sh
npx skills add tomaskub/agent-ops --skill ops-setup-review-standards
```

The skill discovers existing standards and reviewer profiles, then helps you agree reviewer briefs, severity definitions, blocking thresholds, and operator exceptions. It writes or reuses an authoritative policy, defaulting to `docs/agents/review-standards.md`, and connects both `AGENTS.md` and `CLAUDE.md`. It works without requiring the other setup skills.

The policy requires separate quality and spec reviewers. Initial quality review covers the full change; quality re-reviews cover new commits and earlier unresolved findings. Spec review covers the full change every round. Proposed quality tiers are major, minor, and nit, with only major blocking by default. The setup interview confirms or changes those definitions and thresholds.

The operator can explicitly authorize proceeding with blockers or without an issue or spec. The local run record and PR capture those decisions and rationale alongside the original verdicts. It identifies runner compatibility gaps without implementing a runner or changing CI and hosting settings.

Example request after installation, from the target project:

```text
Use ops-setup-review-standards to clarify this repository's code review policy.
Inspect existing standards and help me define the quality and spec reviews.
```

## Review a change

Install and invoke [`ops-review-quality`](skills/ops-review-quality/SKILL.md) and [`ops-review-spec`](skills/ops-review-spec/SKILL.md) independently. Each skill works in a local subagent or a separate container worker with read access to the pinned commits and review inputs.

```sh
npx skills add tomaskub/agent-ops --skill ops-review-quality
npx skills add tomaskub/agent-ops --skill ops-review-spec
```

Give each reviewer the repository, exact implementation base and head SHAs, and verification evidence for that head. Provide the issue criteria and applicable parent constraints to the spec reviewer. On a quality re-review, supply the prior result and coverage history, including unresolved findings. If tracker access is unavailable in a worker, supply captured criteria with source references and versions.

Each reviewer returns JSON with its role, reviewed SHAs and range, verdict, findings, and verification limits. The caller retains the results and operator decisions in the local run record or reports them in the GitHub PR, as configured. Check both SHAs against the intended revision before using a result to decide readiness or posting it as current.

### Example review rounds

An issue requires well-formed CSV, including quoted commas, and a usage example in the README. Its parent requires export to work offline. The example repository treats major quality findings as blocking and minor findings as advisory. In the table, `B` is the pinned implementation base and `H1`, `H2`, and `H3` are successive heads. In a real invocation, use full commit SHAs.

| Round | Quality | Spec |
| --- | --- | --- |
| Initial review at `H1` | Review `B` to `H1`. `fail` with a major finding for broken CSV escaping and a minor finding for an unclear variable name. | Review `B` to `H1`. `fail` on CSV quoting and the missing README example. Record the evidence for offline behavior. |
| Re-review at `H2` after a quoting fix | Review `H1` to `H2` and recheck both findings. Mark the quoting finding `fixed` under its original ID. The naming advisory can stay open with a `pass`. | Review `B` to `H2`. Mark quoting fixed, recheck the parent constraint, and keep `fail` for the missing example even though the fix touched only the exporter. |
| Head moves to `H3` before handoff | Keep the `H2` result in history. Use its coverage for an `H3` re-review if the policy and history still permit it. | Keep the `H2` result in history. Assess `B` to `H3` before treating the spec review as current. |

If verification evidence for a requirement is missing at the reviewed head, record that criterion as `unverified`. A confirmed blocker still yields `fail`. If the operator accepts the missing README example at `H2`, record their rationale and scope alongside the `fail` verdict. Check whether that decision still applies at `H3`.

## Setup development environment

Use [`ops-setup-dev-environment`](skills/ops-setup-dev-environment/SKILL.md) to prepare a repository or selected area for development in fresh clones and worktrees. Install it with:

```sh
npx skills add tomaskub/agent-ops --skill ops-setup-dev-environment
```

The skill discovers existing tooling, interviews you about unresolved choices, and implements a repeatable setup command using the repository's conventions. It covers dependencies, local configuration, generated files, and required services while preserving existing local state and supporting concurrent worktrees. Host prerequisites and secret sources are agreed during the interview.

It reuses an authoritative setup guide or writes `docs/agents/dev-environment.md`, then connects both `AGENTS.md` and `CLAUDE.md` to it. Validation runs setup in a fresh checkout and repeats it with a cheap readiness check. Missing prerequisites or credentials are reported as verification limits.

Example request after installation, from the target project:

```text
Use ops-setup-dev-environment to set up the backend in this repository.
Inspect existing tooling and help me agree a command a new worktree can run to become ready for development.
```

This skill supplies the environment preparation used by [`ops-implement`](skills/ops-implement/SKILL.md).

## Setup verification

Use [`ops-setup-verification`](skills/ops-setup-verification/SKILL.md) to establish or revise executable checks for a repository or selected area. Install it with:

```sh
npx skills add tomaskub/agent-ops --skill ops-setup-verification
```

The skill inspects existing checks and helps you agree which ones are required, where they run, and what evidence they produce. It reuses an adequate command or implements the smallest repository-native change to make the agreed checks repeatable. It documents the command in `docs/agents/verification.md` and connects both `AGENTS.md` and `CLAUDE.md` to that guide.

The command runs in a prepared checkout. The skill checks a fresh worktree or clone, repeats the run, and exercises failure handling with a disposable fixture. The guide defines what implementation agents and reviewers record for the tested revision, including skipped or unavailable checks and any operator exceptions.

Example request after installation, from the target project:

```text
Use ops-setup-verification to set up repeatable checks for this repository.
Inspect our existing tooling and help me agree which checks are required.
```

## Implement or repair an issue

Use [`ops-implement`](skills/ops-implement/SKILL.md) for one assigned issue in a prepared checkout. Local and distributed orchestrators invoke the same skill. Install it with:

```sh
npx skills add tomaskub/agent-ops --skill ops-implement
```

Pass the issue scope and acceptance criteria, repository identity, prepared checkout path, approved branch and base SHA, and any retry limits. For a repair, also pass the current revision or patch and the blocking findings tied to it. For example:

```text
Use $ops-implement to implement APP-12 in the prepared checkout at /path/to/app-worktree.
The target is owner/app on work/APP-12, based on <base SHA>.
Scope: reject blank display names when saving a profile.
Acceptance: blank or whitespace-only names return a validation error, and valid names still save.
Run the repository's required checks and return the patch and verification evidence.
```

For a repair, use the same invocation and give the starting revision and the agreed findings to address. The handoff covers the changed files, tested revision or patch, checks and evidence, acceptance criteria, and remaining blockers. The orchestrator uses it to track revisions, decide when to dispatch review, and publish the PR.

## Deliver an issue locally

Use [`ops-workflow-local`](skills/ops-workflow-local/SKILL.md) in Codex or Claude Code to take one selected issue through implementation, verification, independent reviews and GitHub publication. Install it with the shared role skills:

```sh
npx skills add tomaskub/agent-ops --skill ops-workflow-local --skill ops-implement --skill ops-review-quality --skill ops-review-spec
```

From the target project, request `ops-workflow-local APP-12` with your actual issue key. The coordinator reads the repository's setup and review policies, then asks you to approve the pinned base, branch, isolated worktree and In Progress transition. It runs the repository's checks and uses separate quality and spec reviewers on the verified commit. It asks for approval of the complete PR draft before pushing, confirms publication and leaves the issue In Review for human handoff.

Use the same issue key to resume from the saved local run record. The workflow uses the repository's own setup and verification commands and runs without Hermes or Docker.

## Deliver an issue with distributed workers

Use [`ops-workflow-distributed`](skills/ops-workflow-distributed/SKILL.md) from a configured Hermes host. Install it alongside the shared role skills:

```sh
npx skills add tomaskub/agent-ops --skill ops-workflow-distributed --skill ops-implement --skill ops-review-quality --skill ops-review-spec
```

Start or resume an authorized Linear issue and repository with the [coordinator interface](skills/ops-workflow-distributed/references/coordinator.md). After the first passing required verification, the host publishes one PR through the PER-73 GitHub App helper. Separate quality and spec workers review the pinned revision in sequence. Verified repairs update the same PR, and final evidence goes to a human for merge.

Start the Hermes PR description with the non-closing Linear reference `Refs <issue-key>` and keep that line when editing the description. After the owner merges the reviewed head, Hermes verifies the merge before moving the Linear issue to Done.

Run the local scripted exercise with `python3 -B tests/distributed_fixture.py`. The fixture uses a disposable Git repository, a scripted worker launcher and an App publication fixture.

### Resume an interrupted distributed run

On the configured Hermes host, use the installed skill directory in `$skill` and the original host configuration in `$config`. Use the same issue key and repository as the original run.

```sh
python3 -B "$skill/scripts/coordinator.py" --config "$config" status PER-123 owner/repo
python3 -B "$skill/scripts/coordinator.py" --config "$config" resume PER-123 owner/repo
```

`status` reads the saved snapshot. Check its stage, worker, and recent events before using `resume` to advance the first incomplete gate.

- `waiting_worker` means a worker job is outstanding. Wait for the launcher to report completion, then resume the run.
- `blocked` needs operator action. Read the diagnostic and resolve the reported issue before resuming. Follow the [coordinator reference](skills/ops-workflow-distributed/references/coordinator.md) for approvals, authenticated replies, and recovery.
