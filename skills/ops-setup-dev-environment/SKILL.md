---
name: ops-setup-dev-environment
description: Set up or revise development environment automation and agent documentation for a repository or selected area. Discover existing tooling, interview the user, and implement a repeatable setup command for fresh clones and worktrees. Use for configuring setup, not routine setup execution.
---

# Setup development environment

Give the next coding agent one documented command to prepare a fresh clone or worktree for development and verification in the selected scope. Produce working setup automation, an operational guide, and pointers from `AGENTS.md` and `CLAUDE.md`. Keep repository-specific choices in the target repository, outside this installed skill.

This skill stands alone. Issue-tracking, branching, and verification-policy setup are not prerequisites. It supplies environment preparation for workflows such as `ops-implement`; it does not implement those workflows or define the full verification policy.

## 1. Discover

Resolve the target repository and selected area, verify the Git root, and read applicable instructions. Inspect existing setup documentation, task runners, manifests, lockfiles, toolchain declarations, environment examples, and relevant CI or container configuration. For a selected area, follow its shared dependencies far enough to identify what setup actually requires.

Use existing commands and conventions as the starting proposal, including on reruns. Identify supported host environments, host prerequisites, dependency installation, local configuration sources, generated files, and required services. Distinguish discovered facts from decisions and unknowns. Read configuration without exposing secret values.

Discovery is complete when the scope, reusable setup mechanisms, and unresolved choices are identified. Resolve repository ambiguity before writing.

## 2. Agree the setup

Interview in small rounds. Prefill facts from discovery, ask only unresolved decisions, and give recommendations. Earlier explicit answers count. Cover the following where applicable rather than presenting a universal tooling checklist:

- The repository area and shared dependencies to prepare, supported hosts, and what must already be installed. Default to a developer machine with basic prerequisites; installing system tooling is an explicit choice.
- The setup command and its working directory. Prefer the repository's task runner, such as `make setup-env`, `just setup-env`, or a package script. Reuse an adequate existing command instead of introducing a second implementation.
- How to install dependencies, obtain local configuration, and generate required artifacts. Agree the source of secrets, such as an existing provider or a specific local file, and any manual prerequisites. Fresh clones must have an actionable path that does not depend on another checkout's private files.
- Which resources are shared and which need worktree isolation. Ask about ports, databases, containers, and other service state only when relevant. Reuse safe caches; isolate resources that could collide.
- Whether setup starts required background services. Default to a command that finishes and returns control. If services must remain running for readiness, agree their ownership, readiness check, and cleanup.
- A cheap readiness check showing the agent can run the documented development and verification commands, plus how missing prerequisites or credentials are resolved. Use existing verification guidance when present; defining it and running the full suite are separate work.

Show the concrete scope, command, host assumptions, configuration sources, resource behavior, readiness check, and planned file changes. Proceed once agreed, including authorization already given for these changes. Ask again only when new information materially changes the scope. If the user chooses an incomplete draft, name the unresolved decisions.

## 3. Implement the command

Create or extend the smallest repository-native automation needed for the agreed setup. Adapt to its languages and tools rather than prescribing a package manager, container platform, or task runner.

The command must:

- Resolve paths from the checkout or documented working directory, so a fresh clone or worktree works without the original checkout's absolute paths.
- Check host prerequisites and required configuration, fail with an actionable message and nonzero exit when readiness cannot be reached, and propagate failed setup steps.
- Follow repository version and lockfile conventions. Preserve dependency declarations and lockfiles unless their change is part of the agreed setup.
- Be safe to rerun and resume after partial failure. Preserve existing local configuration and data; routine setup must not reset databases or replace user values. Any destructive reset belongs to a separate explicit operation.
- Obtain secrets through the agreed source without embedding them in tracked files, documentation, or logs. Preserve existing ignored local configuration and keep newly generated private files out of Git.
- Support concurrent worktrees through the agreed isolation and sharing rules. Changes to shared services must respect other users and worktrees.
- Leave the environment usable by subsequent agent commands. Shell activation inside a setup subprocess does not persist in the caller; use persistent configuration or document the required command wrapper or activation step.
- Finish with the agreed readiness check. Start background services only as agreed and provide the corresponding cleanup command when needed.

Reuse existing environment examples and helpers. Add scripts, task targets, or ignore rules only as needed for this repository. A simple setup should stay simple.

## 4. Write the guide and connect entry points

Reuse an authoritative existing setup document when suitable; otherwise write `docs/agents/dev-environment.md`. Describe the selected scope explicitly. When other areas already have setup instructions, preserve them and make routing between scopes clear.

Write an operational guide for the next agent containing:

- Supported hosts and prerequisites, including how to satisfy any agreed manual steps.
- The exact setup invocation and working directory for a fresh clone or worktree.
- Configuration sources and required access, with names and retrieval instructions rather than secret values.
- Any activation or wrapper needed for later development and verification commands, linking to existing command definitions and verification guidance.
- Relevant worktree isolation, shared resources, background service ownership, and cleanup.
- Readiness criteria, actionable failure recovery, and validation evidence or remaining limits.

Keep executable logic in automation. Document decisions and operational details that the command alone cannot convey rather than duplicating its implementation or inventing instructions for unrelated platforms.

Ensure root `AGENTS.md` and `CLAUDE.md` both reach the guide for the selected scope. Preserve imports, symlinks, and delegation; a verified delegation chain can carry the pointer once. Create minimal repository-local entry files if absent, avoid circular references, and preserve shared targets outside the repository. Respect applicable nested instructions.

Suggested pointer, adjusted for scope and the entry file's location:

```markdown
Before preparing a fresh clone or worktree for development or verification, read [Development environment](docs/agents/dev-environment.md) and run its setup command for the selected area.
```

## 5. Validate and report

Exercise the actual setup in a temporary fresh worktree or clone, including the current setup changes even if uncommitted. Do not commit user work to make validation possible. Supply configuration only through the agreed source, so the check does not silently inherit a prepared checkout's dependencies or local state.

Run setup and its readiness check, then run setup again and check readiness and preservation of local configuration and state. Inspect the implementation for concurrent-worktree collisions and validate resource isolation when services apply. Use the cheap readiness check rather than the full test suite. Clean up only temporary resources created for this validation, preserving unrelated work and shared services.

If prerequisites, access, or the environment prevent a check, record exactly what was attempted, what remains unverified, and the next action. Distinguish an agreed design, implemented automation, and verified readiness; an untested command is not verified setup.

Verify the entry-point links, review the diff for unrelated changes and tracked private files, and resolve contradictions with existing setup instructions through narrow edits. Report the scope, command, files changed, fresh-checkout and rerun results, and outstanding actions. Mark incomplete setup explicitly. Do not commit, push, or publish merely to prove setup works.
