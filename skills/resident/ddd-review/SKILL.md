---
name: ddd-review
description: Review a frozen code diff or explicit code-path snapshot for design or spec fidelity and engineering quality, after implementation or for standalone code, complexity, or scope-creep review.
---

# Review

Review a frozen surface in separate **Design** (approved behavior) and **Standards** (engineering quality) passes. Passing one never compensates for failing the other. Default to read-only; fixes require an explicit request or surrounding implementation authorization.

For product changes, versions or delivery, apply [Versioning and delivery](../ddd-flow/references/versioning-and-delivery.md), retrieving only unresolved guidance; reuse valid project binding and decisions. An explicitly disposable fixture with no product or artifact changes has no version/delivery work. Assess compatibility, confirmed baseline, applicable version/artifact bindings and evidence on the frozen surface. Source-only delivery checks may remain pending; standalone review neither bumps versions nor builds artifacts. Keep these findings on the two existing axes.

## 1. Freeze the review surface

For a change, verify the comparison point and record the diff command, changed files and commit list. For standalone review, record explicit paths at a revision or current content hashes; do not invent a diff. Without a fixed surface, both axes are `BLOCKED`. Include tests relevant to the reviewed behavior, even when unchanged, at the same revision or recorded hashes. Respect explicitly fixed read scope and report any resulting test-evidence gap.

Use applicable AGENTS, domain context and approved designs already available; retrieve only missing or invalidated authority, including specialized and upstream authority when relevant. For UI changes, include the approved prototype revision and applicable local assets in the frozen design baseline; an unapproved screenshot is evidence, not a replacement design. Current user requirements, conversation approvals and the router's Authority Baseline are valid authority; cite recoverable decisions even without design files. Tasks, configuration, code and passing tests are evidence, not approval. Missing substantive authority makes Design `NOT_ASSESSABLE`; conflicting approved clauses make it `BLOCKED`. Continue Standards in either case. Never rewrite design or lower acceptance to legitimize drift.

Keep small reviews local and reuse an existing ownership decision. A direct substantial bounded review without one retrieves only [ddd-flow's Choose execution ownership](../ddd-flow/SKILL.md#choose-execution-ownership), without traversing the full workflow. For justified, permitted independent review, dispatch the bounded Worker contract excerpt with this method. Workers use only this method and the contract, without loading dispatch, state, acceptance or recovery sections. A worker obtains a missing excerpt before dependent work, stays read-only, does not delegate or repeat management decisions, and returns findings for main-conversation acceptance. The main conversation verifies evidence and coordinates authorized fixes. Revalidate superseded diff/design evidence before reusing PASS; repeat affected checks unless shared changes invalidate wider evidence. One worker may review both axes.

## 2. Design axis

Trace each applicable requirement to the fixed implementation and validation evidence. For changes focus on the diff; for snapshots assess the selected paths. Check:

- missing, partial or semantically wrong behavior;
- algorithms, formulas, units, thresholds, data, interfaces, state, ordering, timing and failure behavior;
- configuration, persistence, concurrency, deployment and security drift;
- unrequested behavior, fallback, compatibility paths, extension points and explicit scope exclusions;
- implementation and tests sharing the same wrong assumption.

Classify requirements `PASS`, `PARTIAL`, `MISSING`, `WRONG` or `NOT_ASSESSABLE`, citing authority and implementation. A Standards-only request may have no applicable design requirements. Report technical verification and applicable G4 user acceptance separately: passing tests or both review axes do not set `user_acceptance` to accepted. Give the user the actual version, entry point, implemented scope and a short check path when acceptance is due.

For UI changes, compare the latest approved entry and dependent assets with the implemented target page and affected shared consumers using the same scenario, data, interaction state and product-window dimensions. Include retained navigation/selection/draft state, defaults and disabled-versus-hidden behavior. Visual and operable-path claims require actual corresponding evidence; build, DOM structure or algorithm tests cannot substitute. Missing evidence must remain a traceable gap rather than a blanket PASS. Temporal or native behavior needs its own evidence when claimed. Do not add captures to a restricted prototype bundle or infer user acceptance from technical review.

Apply [ddd-design's stable-layout and content defaults](../ddd-design/references/ui-design.md#stable-layout-and-task-focused-content) during that comparison, reusing valid loaded guidance. Assess unnecessary explanatory content and layout changes across affected empty, loading, disabled and failure states as well as useful accessible feedback. A specific approved exception remains authoritative; this reference adds no design gate or write permission.

For completion or performance claims, assess the approved metric and actual boundary: request timeout is not a total processing target, a numerical self-consistency check is not physical validation, and development mode is not the packaged entry. Reassess only affected evidence after a correction unless shared-contract changes invalidate more; preserve independent valid checks and historical failure evidence.

## 3. Standards axis

Apply repository standards first. For substantive code quality decisions, use the shared [code-style entry](../ddd-implement/references/code-style.md) and only relevant language sections; do not maintain a second rule set or expand the approved change to tool/configuration migrations. Use these smell categories as judgment heuristics, not automatic violations:

| Smell | Question |
| --- | --- |
| Mysterious Name | Does the name reveal its meaning? |
| Duplicated Code | Is the same logic repeated? |
| Feature Envy | Does behavior depend more on another module's data? |
| Data Clumps | Do fields repeatedly travel together? |
| Primitive Obsession | Does a primitive hide a domain concept? |
| Repeated Switches | Does the same type-based branch recur? |
| Shotgun Surgery | Does one change scatter across modules? |
| Divergent Change | Does one module change for unrelated reasons? |
| Speculative Generality | Is this variation point needed now? |
| Message Chains | Must callers know a long object path? |
| Middle Man | Does delegation hide meaningful complexity? |
| Refused Bequest | Does inheritance honor its inherited contract? |

Require a current reason for each new file, type, abstraction, interface, adapter, dependency, configuration, compatibility path and failure branch. Read [architecture](../ddd-design/references/architecture.md) for unresolved module depth, interface, seam or locality questions. For test selection or maintenance questions, use [testing and test maintenance](../ddd-implement/references/testing.md), without invoking TDD. Verify that checks covered the changed claim, reused valid results, expanded or repeated for concrete reasons, and stopped after original outcomes and required protection were established. Assess durable additions and the bounded reduction pass: resolve confirmed low-value in-scope tests while preserving distinct behavior, failure paths and boundaries. Keep uncertain/excluded protection visible; shared coverage or count alone does not justify deletion. Confirmed violations are Standards findings, not optional cleanup. Reuse valid architecture/test evidence; review or phase transition alone does not justify rerunning a suite.

When the reviewed candidate is intended for a local commit, handoff or push, apply the shared [Git organization and information checks](../ddd-flow/references/git.md#commit-organization) to the proposed or staged boundaries, or to each commit in the exact range. Assess purpose, necessary dependencies, complete diff and message together. Report confirmed violations as Standards findings; passing technical checks or a supplied PASS field cannot substitute for that judgment. Missing evidence needed to assess the boundaries blocks this part of Standards; continue independent Design review. A quality finding does not authorize history rewriting or other Git mutations.

## 4. Report without reranking the axes

Report Design findings and requirement traceability, then Standards findings, followed by separate verdicts:

- Design: `PASS` | `FAIL` | `BLOCKED` | `NOT_ASSESSABLE`.
- Standards: `PASS` | `FAIL` | `BLOCKED`.

Every finding cites evidence, practical impact and the smallest correction direction. Do not combine scores or hide an unassessable Design axis. Delegated reviews return the result fields in the supplied Worker contract excerpt with both conclusions; the main conversation accepts current evidence.
