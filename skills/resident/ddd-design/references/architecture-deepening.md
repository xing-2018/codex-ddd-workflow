# Deepening

How to deepen a cluster of shallow modules safely, given its dependencies. Assumes the vocabulary in [architecture.md](architecture.md): **module**, **interface**, **seam**, **adapter**.

## Dependency categories

Assess responsibilities, independent reasons to change, state ownership, external failure and resource lifetime before merging modules. Dependency categories help choose verification, not decide whether a boundary is valid. Read [stack adaptation](stack-adaptation.md) only when runtime or project shape is unresolved.

### 1. In-process

Pure computation and in-memory state can still have independent numerical contracts, consumers or owners. Merge only when responsibilities belong together and callers become simpler; preserve a separate numerical module when it owns units, precision or independently maintained algorithms. Usually ordinary functions suffice.

### 2. Local-substitutable

Local test stand-ins can support checks but do not establish architectural cohesion or reproduce every production contract. Decide the boundary from responsibilities and lifetime. Keep valid integration checks for transactions, ordering, persistence or failure semantics that a stand-in cannot verify. Private seams need not appear in the public interface.

### 3. Remote but owned

A network boundary requires explicit failure, timeout and cancellation behavior. A simple call may use the project's existing concrete client directly. Introduce a port/adapter only when current caller isolation, independent lifecycle or real variation warrants it; network access alone does not require a wrapper or interface. An in-memory adapter cannot prove transport behavior.

### 4. External service, solver or device SDK

One external solver or hardware SDK can justify a stable boundary for resource ownership, blocking work, thread affinity or failures. Start with ordinary functions or the existing concrete API; use Protocol/interface/abstract base classes only for a current contract need. A faithful fake can protect caller logic, but retain required real integration evidence and real-device permissions.

## Seam discipline

- **A current reason establishes a seam.** One implementation may need isolation; two implementations with different meanings need not share an interface. Compare caller semantics, invariants, errors and lifetime before sharing. Reject meaningless forwarding layers and hypothetical future consumers, without counting adapters as an admission rule.
- **Internal seams vs external seams.** A deep module can have internal seams private to its implementation as well as the external seam at its interface. Don't expose internal seams just because tests use them.

## Testing strategy: replace, don't layer

- Preserve valid behavior coverage when moving tests to the deepened module's interface, including boundary cases, errors, and regressions. Delete old tests only after that coverage is carried over and they are redundant or depend solely on obsolete implementation details.
- Write new tests at the deepened module's interface. The **interface is the test surface**.
- Tests assert on observable outcomes through the interface, not internal state.
- Tests should survive internal refactors. If a test must change when behavior did not, it is testing past the interface.
