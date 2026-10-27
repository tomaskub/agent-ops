# Policy decisions and defaults

Use this checklist for new setups and revisions. Defaults are proposals for missing policy. Existing conventions and the user's explicit choices take precedence. Ask dependent questions only when their prerequisite choice makes them applicable.

## Strategy and branch roles

Confirm release cadence, deployment constraints, supported versions, and whether incomplete work can integrate safely in small increments. Recommend trunk-based development for a new repository unless release needs justify Gitflow. Gitflow can fit coordinated, versioned releases or multiple maintained release lines; release cadence alone does not settle the choice.

Fresh-repository proposal:

- `main` is the persistent trunk and default PR target.
- One independently keyed implementation issue normally produces one short-lived branch and one PR.
- Start work from current `main`; merge its PR into `main` with squash.
- Start dependent work after its prerequisite merges by default.
- Introduce temporary integration branches or stacks only for an explicit need.
- Preserve the existing review, check, and authorization gates in `issue-rules.md`. A fresh repository without checks does not acquire configured CI through this skill.

For Gitflow, propose `main` for released history and `develop` for ongoing integration. Ordinary issue branches start from and return to `develop`, or to an agreed epic branch. Enable release branches, hotfix branches, and epic branches only for the roles actually needed. Confirm the hosting default branch and normal PR target separately; do not assume they are the same. Record both proposed and observed values without changing hosting settings.

For each persistent or temporary role, settle its exact name or pattern, purpose, base, permitted targets, responsible actor, completion criteria, and retention or cleanup. Identify any path-specific exceptions in a monorepo without inventing a separate strategy for every component.

## Naming

Default ordinary work branches to `<prefix>/<issue-id>-<summary>`.

| Prefix | Purpose |
| --- | --- |
| `feature` | New or changed functionality. |
| `bugfix` | Incorrect behavior. |
| `crashfix` | A defect that crashes the application or process. |
| `documentation` | Documentation changes. |
| `maintenance` | Dependencies, tooling, refactoring, and repository upkeep. |

Use the issue's primary purpose for mixed work. Retain existing repository vocabulary unless a change is agreed. These categories describe branches, not mandatory tracker types or labels.

Identifier rules:

- Take the actual identifier from the backend configured in `issue-tracking.md`. Preserve its case and full value, including the full UUID for local Markdown tracking.
- For GitHub Issues, use the issue number without the display marker `#`. For Jira and Linear, preserve the configured key, such as `PROJ-123`.
- If an identifier requires another transformation to be Git-safe, agree and document an unambiguous mapping back to the canonical identifier. Do not silently shorten or replace it.
- Require a real identifier for ordinary work branches. When missing, follow the configured issue workflow before creating the branch. Policy examples are illustrative, never evidence that an issue exists.

Summary rules:

- Use a short, readable description in lowercase ASCII words or digits separated by single hyphens. Remove punctuation and trim leading or trailing hyphens.
- Limit the summary to 50 characters. Shorten the wording at a word boundary where possible; retain a nonempty, meaningful summary.
- Preserve the identifier when shortening a branch name. Check the resulting name against Git's ref rules and any verified host restrictions.
- Before reusing an existing name, check whether the branch is the intended work. For a distinct branch with the same identifier and summary, append a numeric suffix such as `-2`; the identifier remains unchanged.

Illustrative examples:

```text
feature/PROJ-123-add-login
bugfix/123-fix-login
documentation/PROJ-124-explain-installation
maintenance/550e8400-e29b-41d4-a716-446655440000-update-dependencies
```

Structural exceptions:

- Persistent branches such as `main` and `develop` need no issue identifier.
- For Gitflow, propose `epic/<parent-issue-id>-<summary>` for a temporary integration branch collecting related implementation work. Confirm that the parent has an identifier under `issue-scopes.md`; a container without a key cannot supply an invented one. Reserve this default `epic` role for Gitflow.
- For Gitflow releases, propose `release/<version>`, using the project's existing version format.
- For Gitflow production hotfixes, propose `hotfix/<issue-id>-<summary>`. This names the urgent release path; `crashfix` names a defect category. A production crash using that path takes `hotfix`.
- When trunk-based work needs a temporary integration branch, agree its naming separately, for example `integration/<parent-issue-id>-<summary>`. Treat that as an explicitly enabled structural role.
- Confirm names for maintained release lines only when such lines exist. Preserve existing names during a transition.

## Merge and update rules

Decide topology separately from method. For every allowed source/target pair, specify squash, merge commit, or rebase merge explicitly. A branch pattern without a target and method leaves the policy incomplete.

Default to squash for short-lived issue PRs. For Gitflow epic completion, release and hotfix delivery, and synchronization between persistent branches, propose merge commits that preserve ancestry, using `--no-ff` semantics where a distinct integration merge is required. Rebase merge is an available choice when compatible with repository history requirements and stack tooling; it is not the default.

Agree how branches are brought up to date. Proposed default: rebase an exclusively owned issue branch onto its current target, and merge target changes into shared integration branches. Published history rewrites require coordination with affected owners, and force pushes require authorization. Record the existing authorization rule rather than granting blanket permission through policy setup.

The branch owner resolves conflicts and reruns the required checks on the resulting revision. For a shared integration branch, identify its maintainer and the affected change owners. A changed target or rewritten stack needs fresh validation and any renewed review required by the existing gates.

Before merge, apply the requirements referenced from `issue-rules.md` and the destination's actual protections. Record any enforcement gap. Confirm cleanup defaults: delete completed short-lived branches only once no open PR, stack descendant, release, or worktree still depends on them; retain persistent and supported release branches. Document deletion as a later execution action under repository authorization, not work performed by this setup skill.

## Revisions and transitions

On reruns, distinguish policy clarification from a strategy change. For a change, inspect available open work without treating an inaccessible remote as proof there are no open PRs. Agree:

- The effective point for new branches and existing work.
- Which branches and PRs finish under the old rules, and which require a new target or base.
- How stacks retain dependency boundaries during the handoff.
- How active releases, hotfixes, and supported versions receive fixes during the transition.
- Who updates hosting settings and CI targets, and what verifies the switch.
- When old integration branches can be retired and how to recover if the transition fails.

Keep existing branch names valid during the transition. List concrete actions and owners, with `unresolved` for a required unknown. Do not execute the migration. Make the current rule and any temporary exception easy to distinguish.
