# Design proposal review

Read only for `design-proposal` mode after the [common review contract](../SKILL.md#common-review-contract); reuse valid supplied fragments. Assess whether the proposed design satisfies approved requirements and is sound enough to inform a design decision; implementation need not exist. The [Chinese review copy](design-proposal_zh.md) is for human review only.

## Freeze inputs and authority

Identify the reviewed draft's exact scope and revision, or current hashes plus recoverable content. Include applicable approved requirements, constraints, exclusions, relevant prototype entry/assets and existing research or experiment evidence at identifiable versions. A review-only task can identify inputs in the conversation without writing a record. Separate approved facts, proposed choices, assumptions and unknowns. Code can establish feasibility but cannot narrow approved targets.

An unfixed draft blocks both axes. Missing substantive requirements makes Design `NOT_ASSESSABLE`; conflicting approved requirements make it `BLOCKED`. Continue Standards on a fixed draft and name the missing authority. Missing implementation or code tests alone is not a defect or blocker. Missing evidence for a material feasibility or quality claim remains a specific gap, not a blanket PASS.

Workers use the supplied common contract/report fragments, this mode method and Worker contract. Obtain only missing fragments before dependent work; no other mode or management sections apply.

## Design axis

Trace each material requirement to the actual draft paragraphs, diagrams or scenario. Check the same normal and failure path across user actions, domain objects, inputs/units, transformations, state transitions and outputs. Inspect missing coverage, contradictory responsibility or ownership, unsupported defaults, ordering/concurrency assumptions and scope expansion. UI views must preserve the task, approved states and shared data meaning; a screenshot does not settle computation or domain semantics.

For a new boundary or material interface change, compare the actual caller usage with the proposed input/output, units, state/resource ownership, cancellation, partial failure and cleanup contract using [caller usage and contract](../../ddd-design/references/architecture.md#caller-usage-and-contract).

Classify applicable requirements `PASS`, `PARTIAL`, `MISSING`, `WRONG` or `NOT_ASSESSABLE`, citing the authority and draft evidence. A design may be internally consistent while violating the user's task. Return that discrepancy without rewriting requirements to fit the draft.

## Standards axis

Use project standards and [architecture judgment](../../ddd-design/references/architecture.md) for actual boundaries and trade-offs. Check responsibility and process placement; interface/data compatibility; state and resource ownership; cancellation, retry, failure isolation and recovery; security/permissions and accessibility; dependency/runtime constraints; and verification or migration where relevant. Use [structural consequences](../../ddd-design/references/architecture.md#judge-structural-consequences) to identify exposed knowledge, missing/overlapping responsibility and actual effects. Select applicable questions rather than requiring a filled template, extra abstraction or diagram quota.

For material unresolved choices, assess viable alternatives, the chosen reason and negative consequences. Quality claims need a scenario, conditions and observable acceptance. Distinguish a proposed verification approach from actual evidence; calculations, self-consistency or structure checks cannot establish physical validity or target-host behavior. Identify the consequence of an unresolved claim and what evidence could settle it; do not invent metrics or run experiments without authorization.

## Return a proposal verdict

Use the [common report method](../SKILL.md#4-report-without-reranking-the-axes). Include `review_mode: design-proposal`, the frozen object and authority, Design traceability/findings, Standards findings and separate verdicts:

- Design: `PASS` | `FAIL` | `BLOCKED` | `NOT_ASSESSABLE`.
- Standards: `PASS` | `FAIL` | `BLOCKED`.

Each finding gives locatable evidence, practical impact and the smallest correction direction. Separate defects from unresolved decisions, evidence gaps and optional improvements. A covered simple draft with no defects can pass; do not manufacture findings. A material engineering claim that cannot be assessed blocks that part of Standards; still report independent findings. Do not offset failures between axes.

The result assesses this proposal only. It does not grant G2, implementation authorization, G4 or implementation PASS. Return material choices to the user through the existing approval process; read-only review changes no files or approval status. Authorized design fixes remain with the design owner and cannot silently change requirements. Changed draft or authority invalidates only affected review evidence; a proposal PASS is never reused as code-review PASS.
