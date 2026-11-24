# Review policy

Use separate, read-only reviewers for quality and spec fulfillment. Both are independent of the implementer and of each other. Use `ops-review-quality` and `ops-review-spec` and give both the pinned base, candidate head, and [verification results](verification.md).

Quality assesses correctness, verification coverage, maintainability, and security where relevant. A major defect or material risk blocks handoff. Minor findings and nits are advisory. The initial quality review covers the full base-to-head diff. Re-review covers changes since the last valid quality review and every unresolved finding. Restart full coverage when the previous reviewed commit is missing or is no longer an ancestor.

Spec review evaluates every applicable acceptance criterion and scope constraint against the full base-to-head diff, including on re-review. An unmet criterion blocks handoff. Ask the owner to clarify missing or ambiguous criteria. If the owner expressly authorizes work without assessable criteria, record spec as unassessed and keep quality review required.

For each role, record the verdict, base, head, comparison range, evidence, open findings and dispositions. A pass requires sufficient coverage and no unresolved blockers. Record incomplete evidence as unverified. Preserve older results and require current evidence after a head change. When the owner authorizes a specific exception, record the scope, rationale and reviewed SHA separately from the original verdict.

For local delivery, complete both reviews before publishing the PR. On an approved distributed route, initial verification precedes early publication and both independent reviews follow on that PR. Keep current verification and review receipts in the run record and PR. The owner makes the merge decision on the reviewed revision.
