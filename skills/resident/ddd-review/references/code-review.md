# Code review

Read only for `code` mode after the [common review contract](../SKILL.md#common-review-contract); reuse valid supplied fragments. The [Chinese review copy](code-review_zh.md) is for human review only. A proposal PASS cannot replace this method.

## Freeze the review surface

For a change, verify the comparison point and record the diff command, changed files and commit list. For standalone review, record explicit paths at a revision or current content hashes; do not invent a diff. Without a fixed surface, both axes are `BLOCKED`. Include tests relevant to the reviewed behavior, even when unchanged, at the same revision or recorded hashes. Respect explicitly fixed read scope and report any resulting test-evidence gap.

Reuse the common authority rules. For UI changes, include the approved prototype revision and applicable local assets in the frozen design baseline; an unapproved screenshot is evidence, not a replacement design.

## Design axis

Trace each applicable requirement to the fixed implementation and validation evidence. For changes focus on the diff; for snapshots assess the selected paths. Check:

- missing, partial or semantically wrong behavior;
- algorithms, formulas, units, thresholds, data, interfaces, state, ordering, timing and failure behavior;
- configuration, persistence, concurrency, deployment and security drift;
- unrequested behavior, fallback, compatibility paths, extension points and explicit scope exclusions;
- implementation and tests sharing the same wrong assumption.

For a new boundary or material interface change, trace actual caller usage against the implemented contract using [caller usage and contract](../../ddd-design/references/architecture.md#caller-usage-and-contract).

Classify requirements `PASS`, `PARTIAL`, `MISSING`, `WRONG` or `NOT_ASSESSABLE`, citing authority and implementation. A Standards-only request may have no applicable design requirements. Report technical verification and applicable G4 user acceptance separately: passing tests or both review axes do not set `user_acceptance` to accepted. Give the user the actual version, entry point, implemented scope and a short check path when acceptance is due.

For UI changes, compare the latest approved entry and dependent assets with the implemented target page and affected shared consumers using the same scenario, data, interaction state and product-window dimensions. Include retained navigation/selection/draft state, defaults and disabled-versus-hidden behavior. Visual and operable-path claims require actual corresponding evidence; build, DOM structure or algorithm tests cannot substitute. Missing evidence must remain a traceable gap rather than a blanket PASS. Temporal or native behavior needs its own evidence when claimed. Do not add captures to a restricted prototype bundle or infer user acceptance from technical review.

Apply [ddd-design's stable-layout and content defaults](../../ddd-design/references/ui-design.md#stable-layout-and-task-focused-content) during that comparison, reusing valid loaded guidance. Assess unnecessary explanatory content and layout changes across affected empty, loading, disabled and failure states as well as useful accessible feedback. A specific approved exception remains authoritative; this reference adds no design gate or write permission.

Apply [visual evidence selection](../../ddd-implement/references/testing.md#select-visual-evidence) to actual capture and image-reading actions. Check concrete reasons for rereading or expanding scope, without requiring an image ledger or token-saving claim. Reused evidence must still cover the current visual claim; sampled or uninspected scope cannot receive a broader visual PASS. Functional results do not automatically require screenshots, and structural checks do not certify appearance.

For completion or performance claims, assess the approved metric and actual boundary: request timeout is not a total processing target, a numerical self-consistency check is not physical validation, and development mode is not the packaged entry. Reassess only affected evidence after a correction unless shared-contract changes invalidate more; preserve independent valid checks and historical failure evidence.

## Standards axis

Apply repository standards first. For substantive code quality decisions, use the shared [code-style entry](../../ddd-implement/references/code-style.md) and only relevant language sections; do not maintain a second rule set or expand the approved change to tool/configuration migrations. For structural concerns, use [architecture judgment](../../ddd-design/references/architecture.md#judge-structural-consequences) and identify the exposed knowledge, responsibility and consequence; smell names alone are not findings.

File/function length or count is a lead, never a verdict or a reason to end assessment. For an evidently complex in-scope path, locate its responsibilities or repeated knowledge, explain the maintenance consequence and assess the retained reason or smallest correction through the shared standards. For readability/structure optimization, compare the actual outcome with the requested goal: added comments, passing tests and unchanged executable structure each prove only their own claim. Report unresolved structural issues explicitly; do not call annotation-only work structural optimization.

Require a current reason for each new file, type, abstraction, interface, adapter, dependency, configuration, compatibility path and failure branch. Read [architecture](../../ddd-design/references/architecture.md) for unresolved module depth, interface, seam or locality questions. For test selection or maintenance questions, use [testing and test maintenance](../../ddd-implement/references/testing.md), without invoking TDD. Verify that checks covered the changed claim, reused valid results, expanded or repeated for concrete reasons, and stopped after original outcomes and required protection were established. Assess durable additions and the bounded reduction pass: resolve confirmed low-value in-scope tests while preserving distinct behavior, failure paths and boundaries. Keep uncertain/excluded protection visible; shared coverage or count alone does not justify deletion. Confirmed violations are Standards findings, not optional cleanup. Reuse valid architecture/test evidence; review or phase transition alone does not justify rerunning a suite.

When the reviewed candidate is intended for a local commit, handoff or push, apply the shared [Git organization and information checks](../../ddd-flow/references/git.md#commit-organization) to the proposed or staged boundaries, or to each commit in the exact range. Assess purpose, necessary dependencies, complete diff and message together. Report confirmed violations as Standards findings; passing technical checks or a supplied PASS field cannot substitute for that judgment. Missing evidence needed to assess the boundaries blocks this part of Standards; continue independent Design review. A quality finding does not authorize history rewriting or other Git mutations.

## Return the code verdict

Use the common report contract with `review_mode: code`, the frozen implementation, authority, requirement traceability, findings and separate Design/Standards verdicts. Workers use the supplied common fragments, this method and Worker contract; obtain only missing fragments before dependent work, without routing or management sections.
