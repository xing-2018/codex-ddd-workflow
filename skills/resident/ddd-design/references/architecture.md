# Module and interface design

Read for a real responsibility boundary, public interface, testability seam or module-depth decision. Do not add an abstraction merely because a design document has an architecture section.

A module is a unit with an interface and implementation at any scale. Its interface includes signatures, invariants, ordering, errors, configuration and material performance guarantees. A deep module hides useful behavior behind a small stable interface: that useful behavior per unit of interface knowledge is its leverage. A seam permits a real variation without editing its caller; an adapter is a concrete implementation at that seam. Identify existing callers and variation points before creating one. Prefer an existing solution and a small surface over a pass-through layer.

Ask whether removing the proposed boundary would scatter complexity among callers; whether tests can exercise the public contract without reaching inside; and whether dependencies can be accepted at a real seam rather than created internally. One hypothetical adapter does not justify a new seam. Return important outcomes rather than burying them in side effects when the domain permits.

Read [deepening](architecture-deepening.md) for dependency categories and a safe deepening path. Read [design alternatives](architecture-alternatives.md) only when competing interface designs are explicitly needed. The selected architecture must trace each material requirement to a responsibility, interface, state owner, failure behavior and verification approach. Changing observable semantics or a costly dependency remains a design choice for approval.
