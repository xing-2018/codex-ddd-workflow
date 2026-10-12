# Design to implementation plan

Read when a design must lead to an implementation slice or multiple dependent slices. Use the approved brief and design, including applicable prototype identity and its simulated limits. Planning does not grant implementation permission.

For one slice, put its deliverable, affected responsibilities, accepted design clauses, independent expected result, necessary checks, migration or rollback boundary and exclusions in the current record. Create a separate `plan.md` only for multiple slices or real dependencies. Split by a user-visible or otherwise independently verifiable result through the needed layers, rather than by frontend, backend and tests. A slice must be small enough to complete in one fresh context and preserve approved architecture.

G3 binds the current slice and design baseline. Name the exact approved scope and verification approach; do not mark later slices approved by association. Technical checks and user acceptance remain distinct. If feedback changes the brief or design, trace its affected prototype, interface, state, slice and check; request approval only for changed material semantics.
