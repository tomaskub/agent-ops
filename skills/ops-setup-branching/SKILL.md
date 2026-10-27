---
name: ops-setup-branching
description: Set up or revise a repository's branch naming, trunk-based or Gitflow strategy, and merge policy, including integration branches and stacks. Use for initial setup or strategy changes, not routine branch creation or merging.
---

# Setup branching

Agree and document the selected repository's branching policy in `docs/agents/branching.md`. Support both an empty repository and an established one. Keep repository-specific choices in the generated document, outside this installed skill.

This skill defines policy and any required transition. Its writes are documentation only. Creating or renaming branches, changing PR targets or hosting settings, configuring CI, and executing merges or migrations are separate operations.

## 1. Discover the current policy

Resolve the target repository and read applicable instructions. Assume `ops-setup-issue-tracking` has succeeded. Read its outputs before proposing policy:

- `docs/agents/issue-tracking.md` for repository identity, tracker backend, and exact identifiers.
- `docs/agents/issue-scopes.md` for independently keyed work, parent scopes, and dependencies.
- `docs/agents/issue-rules.md` for review gates, PR references, automation, and issue completion.

If a required input is absent or inconsistent, identify the specific gap and ask for its resolution. Continue discovery that does not depend on it; do not silently replace the prerequisite setup or invent an issue identifier.

Verify the Git root and reconcile available remote identity with the prerequisite documents. Inspect existing branching documents, agent entry points, contribution guidance, branch names, and relevant local CI configuration. Use read-only hosting capabilities when available to inspect the default branch, merge options, protections, and stack tooling. Resolve identity ambiguity before writing. An unborn branch or absent remote is valid for a fresh repository; record planned branch names and unavailable configuration rather than requiring a first commit or a remote.

On established repositories and reruns, use existing conventions as the starting proposal. Preserve them unless the user chooses a change. Distinguish a documented rule, an observed practice, and a verified hosting setting. Conflicting sources require a decision rather than silently choosing whichever matches the defaults.

Discovery is complete when the repository, current policy, relevant capabilities, and unresolved choices are identified. Inaccessible hosting configuration remains unverified and need not block policy agreement.

## 2. Agree the policy

Read [policy-decisions.md](references/policy-decisions.md) for the decision checklist and proposed defaults. Read [merge-flows.md](references/merge-flows.md) when Gitflow, integration branches, stacks, or a strategy transition apply.

Prefill choices from discovery. Ask only unresolved decisions, grouping related choices and giving a recommendation. Offer fresh-repository defaults together so the user can accept or revise them as a set. Earlier explicit choices count as answers. Do not impose this skill's defaults on an established repository.

Agree the following for the repository's actual scope:

- Strategy and rationale, including release cadence and supported release lines.
- Persistent and temporary branch roles, naming, branch bases, and PR targets.
- Merge topology and merge method for every allowed source/target pair.
- Updating branches, conflicts, dependent work, required checks, and cleanup.
- For a change of strategy, treatment of existing branches, PRs, stacks, and releases.

Show a concrete policy summary and documentation changes. Proceed once the user agrees, including agreement already provided in this session. Ask again only if new information materially changes the agreed scope. If decisions remain open, write a draft only when the user chooses that outcome, naming what remains unresolved.

Agreement is complete when each applicable decision is settled or explicitly listed as open in an agreed draft. A fully specified policy can be complete even while hosting enforcement needs configuration.

## 3. Write the policy

Use [branching.md](assets/branching.md) as the output starting point. Replace its guidance and placeholders with agreed values, omit inapplicable sections, and label illustrative examples as examples. Produce one operational policy rather than a catalog of every possible strategy.

Make `docs/agents/branching.md` authoritative for branch naming and merge flow. Keep tracker identities, lifecycle, gates, PR references, and closure rules in the prerequisite documents and link to them. Incorporate their constraints, including the difference between merging implementation work and completing a parent issue. Branch prefixes do not create tracker labels or issue types.

For an existing setup, preserve unrelated policy. Within the agreed documentation scope, move overlapping branching rules into the policy and replace them with links. Resolve contradictions in contribution guides and agent instructions through narrow edits. Preserve shared files and symlink targets outside the repository; establish a repository-local pointer instead of modifying shared policy. If higher-level instructions prevent the chosen policy, report that conflict rather than declaring the policy ready to use.

Record policy status separately from enforcement status. Use `complete` only when decisions are settled and local documentation agrees; otherwise use `draft` with specific open decisions. For enforcement, distinguish verified settings, observed mismatches, unavailable inspection, and proposed configuration. Include the source and verification date for hosting observations. Missing enforcement calls for named follow-up actions, not a claim that settings were changed.

On a strategy change, update this same file and include the transition plan, its effective point, and responsibility for each remaining action. Existing branches retain their names during transition. Historical migration details can be removed once the transition is complete; retain the current policy and rationale.

## 4. Connect agent entry points

Ensure both root `AGENTS.md` and `CLAUDE.md` reach the policy. Preserve existing imports, symlinks, and delegation. Verify the whole reference chain, avoid circular delegation, and create minimal repository-local entry files if needed.

Suggested pointer, adjusted for the entry file's location:

```markdown
## Branching

Before creating or updating a branch, choosing a PR target, arranging dependent work, or merging, read [Branching policy](docs/agents/branching.md).
```

## 5. Verify and report

Check that both entry points reach the policy, its prerequisite links resolve, and no output-template instructions remain. Validate representative branch names with `git check-ref-format --branch` when Git is available, without creating branches. Check that every selected branch role has a base, target, merge method, and completion or cleanup rule; persistent branches need retention rules instead of deletion.

Walk one ordinary issue through the selected flow. Also walk a release and hotfix for Gitflow, dependent work for stacks, and the handoff for a strategy change when applicable. Confirm that merges deliver required fixes to all named destinations and that stack updates avoid replaying already merged parent changes. Review the diff for contradictory rules and unrelated changes.

Report files changed, agreed strategy and naming, verification performed, enforcement gaps, and any transition actions. Identify a draft as incomplete. Do not create demonstration issues or branches, commit, push, or publish merely to prove this setup works.
