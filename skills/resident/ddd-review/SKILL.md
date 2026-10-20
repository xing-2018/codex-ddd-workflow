---
name: ddd-review
description: Review a frozen design proposal before implementation, or a code diff or explicit code-path snapshot, for requirement fidelity and engineering quality.
---

# Review

Review a frozen surface in separate **Design** (requirement or specification fidelity) and **Standards** (engineering quality) passes. Passing one never compensates for failing the other. Default to read-only; fixes require an explicit request or surrounding design/implementation authorization covering the reviewed object.

## Select the review mode

- **`design-proposal`:** a design draft before implementation or a reconsidered design decision. Read only [proposal review](references/design-proposal.md) and the currently needed architecture material; implementation and code tests need not exist.
- **`code`:** an implementation diff or explicit code-path snapshot, including post-implementation and standalone code review. Read only [code review](references/code-review.md) and currently needed code/test standards. A proposal PASS never replaces implementation review.

Use the requested object, not code availability, to select the mode. Resolve only ambiguity that changes the assessment. Do not preload both methods. Review does not authorize rewriting requirements, designs, approval records or implementation.

## Common review contract

Use applicable AGENTS, domain context and approved requirements/designs already available; retrieve only missing or invalidated authority, including relevant specialized and upstream authority. Current user requirements, recoverable conversation approvals and an established Authority Baseline remain valid without design files. Tasks, configuration, code and passing tests are evidence, not approval. Missing substantive authority makes Design `NOT_ASSESSABLE`; conflicting approved clauses make it `BLOCKED`; continue Standards in either case. Never rewrite design or lower acceptance to legitimize drift.

For product changes, versions or delivery, apply [Versioning and delivery](../ddd-flow/references/versioning-and-delivery.md), retrieving only unresolved guidance; reuse valid project binding and decisions. An explicitly disposable fixture with no product or artifact changes has no version/delivery work. Assess compatibility, confirmed baseline, applicable version/artifact bindings and evidence on the frozen surface. Source-only delivery checks may remain pending; standalone review neither bumps versions nor builds artifacts. Keep these findings on the two existing axes.

Reuse the main conversation's valid execution ownership decision and evidence. A small review stays local; a substantial direct review without a decision retrieves only [Choose execution ownership](../ddd-flow/SKILL.md#choose-execution-ownership), without traversing flow. For justified permitted delegation, supply the common contract/report fragments, selected mode method and bounded Worker contract with valid source identities. A worker obtains only missing fragments, stays read-only, does not delegate or repeat management decisions, and returns both axes for main-conversation verification and authorized fixes. It reads no other mode or dispatch/state/acceptance/recovery sections. One worker may review both axes.

Apply [Evidence validity](../ddd-flow/references/execution.md#evidence-validity) only for unresolved reuse/invalidation; reuse valid fragments. Mode methods own their frozen-object and claim-specific checks. Review, commit or handoff alone triggers no rerun.

## 4. Report without reranking the axes

For the main conversation's user-facing report, lead with the overall disposition and main impact, then give the separate verdicts and supporting evidence below. Keep Design and Standards findings and requirement traceability distinguishable; neither axis can offset or conceal the other:

- Design: `PASS` | `FAIL` | `BLOCKED` | `NOT_ASSESSABLE`.
- Standards: `PASS` | `FAIL` | `BLOCKED`.

Every finding cites evidence, practical impact and the smallest correction direction. Do not combine scores or hide an unassessable Design axis. A small or clean review needs no empty findings or unrelated appendix. Delegated reviews retain the result and identity fields in the supplied Worker contract excerpt with both conclusions; the main conversation accepts current evidence and organizes it for the reader.

Bind each verdict to the frozen object, covered paths and assessed claims. Passing a local change does not certify the entire implementation. Include observed out-of-scope issues and unassessed claims in the existing report without expanding the review or repair automatically.
