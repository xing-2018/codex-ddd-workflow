# Module and interface design

Read for a real responsibility boundary, public interface, testability seam or module-depth decision. Do not add an abstraction merely because a design document has an architecture section.

The synchronized [Chinese review copy](architecture_zh.md) is for human review, not additional execution guidance.

A module is a unit with an interface and implementation at any scale. Its interface includes signatures, invariants, ordering, errors, configuration and material performance guarantees. A deep module hides useful behavior behind a small stable interface: that useful behavior per unit of interface knowledge is its leverage. A seam permits a real variation without editing its caller; an adapter is a concrete implementation at that seam. Identify existing callers and variation points before creating one. Prefer an existing solution and a small surface over a pass-through layer.

Ask whether removing the proposed boundary would scatter complexity among callers; whether tests can exercise the public contract without reaching inside; and whether dependencies can be accepted at a real seam rather than created internally. One hypothetical adapter does not justify a new seam. Return important outcomes rather than burying them in side effects when the domain permits.

For a material unresolved choice about responsibility or process placement, state ownership, data format, cancellation/retry or resource lifetime, compare only viable alternatives that could change the decision. State the shared constraints, complexity and failure consequences, the recommendation and the evidence that would require reconsideration. A settled local change needs no invented alternatives or separate ADR. Express consequential quality requirements as a concrete environment/scale, trigger, response and acceptance measure; leave unknown measures unresolved rather than inventing guarantees.

## Caller usage and contract

For a new boundary or material interface change, first show how an actual caller completes its task, then derive signatures and data structures from that usage. Check the same representative path against input/output meaning and units, observable results and side effects, error outcomes, the unique state owner, initialization and resource lifetime, cancellation, partial failure and cleanup responsibility. Select relevant questions; do not require another document, a fixed number of examples or competing designs for settled details.

Compare usage with the proposed contract: does the caller need hidden ordering, internal representation or private initialization knowledge? State what useful complexity the interface hides and what knowledge remains exposed. An unresolved ownership or failure responsibility is a design gap, even if the signatures type-check. Tie the chosen boundary to an actual constraint and name evidence that would overturn it.

## Judge structural consequences

Follow the task's representative path from input to useful result. Check whether modules, data representations, conversions and state owners serve current requirements. Prefer a direct solution using existing responsibilities; an added layer, generic editing protocol or intermediate model needs a concrete caller, invariant or lifecycle reason. When the path repeatedly converts data, coordinates internal steps across layers or computes the same result, identify who can own that work once and explain the retained need or smallest simplification. A user's description of a tool as simple does not withdraw required capabilities. Fit this judgment into the existing design or review; do not require another document, diagram, alternative or repository-wide inventory.

Use caller-coordinated internal steps, leaked representations, multiple writers of one state, forwarding without responsibility and manually duplicated facts as leads, not automatic violations. A finding identifies the exact location, exposed or repeated knowledge, missing or overlapping responsibility and practical change/failure consequence. A layer that owns protocol adaptation, resources, a compatibility contract or a domain boundary has a current reason; do not demand splitting, merging or repository-wide refactoring from a smell name alone.

Read [deepening](architecture-deepening.md) for dependency categories and a safe deepening path. Read [design alternatives](architecture-alternatives.md) only when competing interface designs are explicitly needed. The selected architecture must trace each material requirement to a responsibility, interface, state owner, failure behavior and verification approach. Changing observable semantics or a costly dependency remains a design choice for approval.
