# Conditional merge flows

Use only the sections that apply to the selected policy. These are proposed flows; adapt them to established repository rules and confirmed release requirements.

## Gitflow

Use the chosen branch names in the output. The following defaults use `main` and `develop`.

| Source role | Starts from | PR destination | Proposed method | Completion |
| --- | --- | --- | --- | --- |
| Ordinary issue | `develop` | `develop` | Squash | Required issue acceptance and merge gates. |
| Issue belonging to an epic | Its epic branch | Its epic branch | Squash | Required implementation acceptance and merge gates. |
| Epic | `develop` | `develop` | Merge commit | The grouped outcome meets the parent acceptance rules. |
| Release | Selected `develop` revision | `main`, then `develop` | Merge commit into each | Release fixes reach both histories and release gates pass. |
| Hotfix | Affected production branch or release tag | `main` and the applicable ongoing-development destination | Merge commit into each | Production fix and required propagation are verified. |

Confirm the ordering and any supported-version exceptions. Tagging, publishing, and deploying a release remain separate authorized operations. A merge into `main` is not evidence that deployment happened.

A release branch receives stabilization changes while `develop` can continue future development. Deliver the release to `main` and return its stabilization fixes to `develop`. Record who verifies both destinations before release-branch cleanup.

A hotfix starts from the affected released revision, not an arbitrary unshipped `develop` head. Deliver it to production history and back to ongoing development. With an active release branch, include the fix there so finishing that release cannot lose it. That release can subsequently carry the fix into `develop`; propagate it there sooner when needed. With multiple active or maintained lines, enumerate every affected destination and choose merge or deliberate backport according to compatibility. A hotfix is complete only after all required destinations are accounted for.

List any direct synchronization between persistent branches as an explicit source/target pair using merge commits. Name its purpose, such as returning production fixes to `develop`. Merging all of `develop` into `main` is a release operation, not routine synchronization.

For an epic, identify its maintainer and update it from `develop` using merge commits. Child PRs target the epic. Merge the completed epic into `develop` with preserved ancestry. Intermediate child merges do not by themselves complete the parent; defer to `issue-scopes.md` and `issue-rules.md`.

## Temporary integration branches with trunk

Use a temporary integration branch only when related changes must be validated together before entering trunk. Agree its name, keyed parent, owner, lifespan, and acceptance gate. Propose starting it from current trunk, sending its child issue PRs there with squash, and returning the completed integration branch to trunk with a merge commit. Bring trunk updates into the shared integration branch with merge commits.

If the repository instead requires squash for the final integration PR, account for lost ancestry: retire the integration branch after merge and rebuild any remaining dependent work from the new trunk. Do not continue a shared integration branch after squashing it without a specific reconciliation plan.

Validate each child against its immediate target and validate the combined result against trunk's requirements. A partial merge into an integration branch does not prove the full outcome is ready for trunk. Delete the branch only after final integration and after handling all remaining dependents.

## Stacked PRs

Stacks model dependencies between individually reviewable changes. They are separate from a shared integration branch and can be used with either branching strategy when explicitly selected.

Agree the stack's final integration destination, responsible owners, merge method, tooling, and required checks. Default each PR to one implementation issue. The bottom PR targets the final destination; each higher PR targets its immediate prerequisite. Merge bottom-up, satisfying the final destination's requirements for each change.

Discover whether the repository uses native linked stacks, another stack tool, or ordinary dependent PRs. Use verified capabilities rather than assuming every platform supports the same operations. Tooling may automate rebasing and retargeting; verify the resulting bases, commit sets, check results, and review state. If the tool's merge method or history constraints conflict with policy, resolve the mismatch before declaring that stack path usable.

For ordinary dependent PRs, record the old parent boundary before merging the parent. After a squash or rebase merge, the destination can contain the parent's changes under different commit IDs. Retargeting alone does not transplant the child commits and can leave old parent commits in the PR.

When a history rewrite is agreed, replay only the child's own commits onto the updated destination, using the recorded parent boundary. Git's `rebase --onto <new-base> <old-parent-boundary> <child>` illustrates this operation; it is not a command for the setup skill to execute. Reconcile higher descendants in dependency order. Inspect the resulting diff and rerun required checks and review before the next merge.

When the parent merges with preserved ancestry, retarget the next PR and verify its base and diff; a rebase may be unnecessary. In either case, coordinate shared history changes and obtain force-push authorization where required. Preserve branches needed by descendants until the stack is reconciled. If that cannot be done safely, pause the dependent change and record a recovery plan rather than merging duplicated parent changes.

## Technical references

Consult current official documentation when platform behavior affects the selected policy. These references explain the history and dependency considerations; they are not a promise that a target repository has a capability enabled.

- [GitHub merge methods](https://docs.github.com/en/pull-requests/reference/pull-request-merges) explains squash and rebase history behavior.
- [Git rebase](https://git-scm.com/docs/git-rebase) documents transplanting a topic branch with `--onto`.
- [Changing a PR base](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/changing-the-base-branch-of-a-pull-request) describes effects on commits and review context.
- [GitHub stacked PRs](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests) describes native stack behavior, subject to the target environment's actual capabilities.
- [Original Gitflow model and later reflection](https://nvie.com/posts/a-successful-git-branching-model/) describes release and hotfix propagation and when simpler flows fit better. The issue-branch squash default here is an explicit policy choice rather than a claim that original Gitflow required squash.
