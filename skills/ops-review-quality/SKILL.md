---
name: ops-review-quality
description: Review a pinned implementation for defects and repository standards. Use for initial full-diff quality reviews or incremental quality re-reviews with prior findings.
---

# Review code quality

Perform one independent, read-only quality review. Work from the pinned Git objects and supplied evidence. Return the result to the caller. Leave repository writes, commits, finding repair, additional reviewers, run records, and GitHub reporting to the caller.

## Inputs and coverage

1. Resolve the repository and read its authoritative review policy, normally `docs/agents/review-standards.md` via the agent entry point. A proposed policy edit in the reviewed diff needs operator agreement before it governs the review. Follow the quality brief and applicable path-specific instructions and project standards. Use the policy's severity tiers and blocking mapping, including on re-review. If the applicable policy is missing or ambiguous, record the gap and return `unverified` unless a known blocker already establishes failure.
2. Obtain the full implementation base and head SHAs from the caller. Resolve the supplied SHAs to commit objects and inspect those objects, for example with `git diff <start> <head> --` and `git show <head>:<path>`. If the required revision is unavailable or a supplied current-revision check shows that it moved, return `unverified` and explain the mismatch. Use verification evidence attributable to the reviewed revision.
3. For an initial review, inspect the entire base-to-head diff and relevant context. Look for concrete correctness, maintainability, security, test adequacy, and performance issues under the quality brief. Cite observable behavior or risk and affected code.
4. For a re-review, require a prior quality result and its coverage record, or a supplied copy of that record. Check that it covers the same base under the applicable policy, that coverage is complete, and that its head is an ancestor of the current head. Review the new commits and their cumulative changes from that prior head to the current head. Verify every earlier unresolved finding against the current tree, including advisory findings and valid findings with an operator exception. Preserve their IDs and update evidence and dispositions. Link the prior coverage so earlier rounds remain available. For incomplete evidence, changed policy that invalidates coverage, or rewritten history, follow the repository's recovery rule. A fresh full review starts at the implementation base. If valid coverage cannot be established, report the gap.

## Result

Return one JSON object with the fields below. `base_sha` and `head_sha` identify the requested commit objects, even if the head is stale. Use `null` for a commit you cannot resolve. `range_start_sha` is the actual comparison start and is `null` when no comparison was possible. The example shows the field names and types. Follow the repository policy for actual severity names and blocking decisions.

```json
{
  "schema_version": 1,
  "role": "quality",
  "base_sha": null,
  "head_sha": null,
  "range_start_sha": null,
  "prior_review_ref": null,
  "verdict": "unverified",
  "findings": [],
  "verification_limits": ["The caller did not supply a pinned revision."]
}
```

Set `prior_review_ref` to the caller's prior coverage reference as a string for an incremental review. Use `null` for a full or unavailable comparison. Each finding has `id`, `location`, `evidence`, `severity`, `unmet_requirement`, `blocking`, and `disposition`. Use strings for ID, location, evidence, and disposition, a Boolean for blocking, and the policy's tier string for severity. Set `unmet_requirement` to `null`. Give the finding an ID based on the issue it describes, independent of SHA or line number. Reuse that ID when rechecking it. Use a path and line at the current head when available, or describe where the behavior is expected or was checked.

Use `open`, `fixed`, `rejected`, or `advisory_left_open` as the disposition. A fixed or rejected finding needs current evidence. The blocking flag describes the finding under policy and is retained when the disposition becomes `fixed` or `rejected`. An unresolved blocking finding yields `fail` even when the operator grants an exception. Otherwise use `unverified` if evidence is insufficient to assess, or `pass` if coverage is sufficient. Open advisories can accompany `pass`. The caller tracks operator decisions separately from this verdict.
