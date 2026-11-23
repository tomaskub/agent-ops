---
name: ops-review-spec
description: Review a pinned implementation against its assigned issue criteria and applicable parent constraints. Use to assess the whole change on every spec review round.
---

# Review spec fulfillment

Perform one independent, read-only spec review. Work from the pinned Git objects and supplied evidence. Return the result to the caller. Leave repository writes, commits, finding repair, additional reviewers, run records, and GitHub reporting to the caller.

## Inputs and coverage

1. Resolve the repository and read its authoritative review policy, normally `docs/agents/review-standards.md` via the agent entry point. A proposed policy edit in the reviewed diff needs operator agreement before it governs the review. Obtain the assigned issue, its acceptance criteria, relevant linked specification and parent constraints, and applicable operator clarifications. Use the configured authoritative sources or a caller-supplied capture with source references and the version or criteria reviewed. Limit parent scope to constraints that govern this issue. Record gaps or conflicts for the caller to resolve. Missing policy or any other required input limits the assessment.
2. Obtain the full implementation base and head SHAs from the caller. Resolve the supplied SHAs to commit objects and inspect those objects, for example with `git diff <base> <head> --` and `git show <head>:<path>`. If the required revision is unavailable or a supplied current-revision check shows that it moved, return `unverified` and explain the mismatch. Use verification evidence attributable to the reviewed revision.
3. Review the full base-to-head change in every round. Check each applicable requirement against the implementation and relevant behavior, including behavior outside the latest fix diff. Cite the evidence for each assessment. Report missing, partial, or incorrect implementation and unjustified scope expansion as unmet requirements. For a scope finding, cite the issue or parent constraint that establishes the boundary. Distinguish a demonstrated miss from an inability to verify. If prior spec findings were supplied, retain their IDs and record any verified resolutions as part of the full review.
4. If requirements exist but evidence or clarity is insufficient, identify what is missing and leave the affected criteria `unverified`. Use `not assessed` only when no usable issue or spec exists and the caller supplies the operator's explicit authorization to proceed without one. An inaccessible issue or unresolved ambiguity calls for `unverified`. Flag any absent source in the result.

## Result

Return one JSON object with the fields below. `base_sha` and `head_sha` identify the requested commit objects, even if the head is stale. Use `null` for a commit you cannot resolve. `range_start_sha` is the base SHA for every comparison and is `null` when no comparison was possible.

```json
{
  "schema_version": 1,
  "role": "spec",
  "base_sha": null,
  "head_sha": null,
  "range_start_sha": null,
  "verdict": "unverified",
  "requirements": [],
  "findings": [],
  "verification_limits": ["The caller did not supply a pinned revision."]
}
```

Include `requirements`, an array of objects with string fields `id`, `source`, `status`, and `evidence`. Use stable requirement IDs, using existing IDs when available. Identify the exact criterion in `source` by reference or captured text. Status is `met`, `unmet`, or `unverified`. Use an empty array when there are no assessable criteria and report the reason in `verification_limits`.

Each finding has `id`, `location`, `evidence`, `severity`, `unmet_requirement`, `blocking`, and `disposition`. Use strings for ID, location, evidence, and disposition, a Boolean for blocking, and `null` for severity. Use the requirement ID for `unmet_requirement`. Give the finding an ID based on the issue it describes, independent of SHA or line number. Reuse that ID when rechecking it. Use a path and line at the current head when available, or describe where the behavior is expected or was checked.

Use `open`, `fixed`, or `rejected` as the disposition. A fixed or rejected finding needs current evidence. Unmet requirements are blocking. Retain the blocking flag on resolved findings. Only unresolved blockers affect the verdict. Use `fail` while any confirmed blocker remains, including one accepted by the operator. Otherwise use `unverified` if assessment is incomplete, `not assessed` for explicitly authorized work without a usable spec, or `pass` when a usable requirement source was assessed, all applicable requirements are met, and the scope is accounted for. The caller tracks operator decisions separately from this verdict.
