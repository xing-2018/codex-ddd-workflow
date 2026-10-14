---
name: ddd-implement
description: "Implement an approved slice, diagnose without writes, or repair within an existing contract when selected by ddd-flow or explicitly invoked."
---

# DDD Implement

## Select authorization mode

Identify the requested action before using a process below:

- **`diagnose`:** investigate a bug, failure or regression without editing source, tests, configuration or persistent project records. Read [diagnosis](references/diagnosis.md) and stop with evidence, uncertainty and a correction direction. Do not enter the implementation process or the repair step.
- **`repair`:** fix a reported defect only when the user has authorized repair within an existing approved contract. Read [diagnosis](references/diagnosis.md), prove the relevant cause and use its repair path. A material contract change returns to `ddd-flow` before dependent edits.
- **`implement`:** complete only the approved design or current ready slice. Use the implementation process below; approval of one slice does not authorize the next slice.

Reuse [ddd-flow](../ddd-flow/SKILL.md)'s established authority, change and write boundaries; direct invocation obtains them from its entry once. Before writes, verify that the detailed plan and authentic execution authorization or bounded autonomy cover the actions and necessary `.planning` maintenance. Apply the router's migration method for missing or outdated records. Return uncertain meaning or permission before dependent writes and continue independent read-only work. Existing project, test, GUI, Git and delivery permissions remain effective; technical checks do not confer user acceptance.

Reuse the router's valid execution ownership decision. Direct main-conversation invocation supplements a missing decision through the entry below; assigned workers use only their assigned entries.

## Delegated evidence worker entry

For a delegated `exploration` or `diagnosis` question, use the packet's bounded Worker contract excerpt and read scope. Verify the business source and causal evidence independently. Exploration answers one call-chain, data-flow or boundary question without inventing a defect; diagnosis tests one assigned hypothesis against supporting and contrary observations. Run only assigned, authorized discriminating checks. Stay read-only, do not delegate or claim whole-task completion, and return locatable observations, inferences, unknowns and an explicit no-write result. Use [diagnosis](references/diagnosis.md) only for an unresolved method question; the main-conversation repair and implementation processes do not apply.

## Delegated implementation worker entry

When assigned an approved implementation slice as `implementation-worker`, use the packet's approved baseline, scope and acceptance criteria and the Worker contract excerpt from [execution](../ddd-flow/references/execution.md#worker-contract). Verify the relevant authority text and implement only the assigned slice using Process steps 1–5. Then freeze the slice diff and return the candidate and authorized check evidence to the main conversation. If the contract excerpt is absent, obtain that bounded excerpt before dependent work; do not read the full management protocol.

Do not restart routing or own whole-change versioning, delivery, completion metadata or final acceptance. Read [Versioning and delivery](../ddd-flow/references/versioning-and-delivery.md) only when version or delivery work is explicitly assigned, and perform only that authorized part. Do not delegate, change approved design or commit unless the packet explicitly grants a project-authorized worker commit. Report a design conflict before dependent changes while completing independent authorized checks. The main-conversation entry and Process steps 6–8 below do not apply to ordinary worker execution.

## Main-conversation entry

Implement the approved design as the smallest coherent change using the guards recovered above. Design owns observable behavior; implementation has **no design authority**. Return a missing material fact to the router rather than silently redesigning the contract.

If an approved task graph exists, work one ready vertical slice at a time. Otherwise implement the bounded design directly. Do not create task documents merely because this phase is active.

Use [ddd-flow's design approval](../ddd-flow/SKILL.md#design-approval) only for an unresolved approval object; settled approval adds no per-file or repeated gate.

For product changes or requested delivery, apply [Versioning and delivery](../ddd-flow/references/versioning-and-delivery.md); retrieve only unresolved guidance and reuse the router's resolved project binding, baseline and still-valid decisions. An explicitly disposable fixture with no product or artifact changes has no version/delivery work.

## Execution ownership

Only when direct invocation lacks a valid decision, retrieve [ddd-flow's Choose execution ownership](../ddd-flow/SKILL.md#choose-execution-ownership) before substantial execution of a bounded candidate. This phase adds no trigger or benefit rule. Justified dispatch and managed-result acceptance use the missing bounded sections of [execution](../ddd-flow/references/execution.md); the main conversation owns integration, external actions and final acceptance.

## Process

1. **Confirm authority.** Reuse established approved requirements, design, ADRs and optional tasks while their identity and relevance hold. Read affected portions when they changed, are unavailable or conflict; do not treat implementation as approval. Build a short checklist covering inputs, domain and asset semantics, formulas, time or state behavior, outputs and failure isolation; for UI changes include the intended page, affected shared consumers, defaults, navigation state and disabled-versus-hidden behavior; each item points to an approved clause. Record the starting Git state and protect unrelated user changes. With known concurrent work, verify the selected conversation binding, overlapping files, resource ownership and dependency identities through [shared checkout coordination](../ddd-flow/references/execution.md#shared-checkout-coordination) before substantive writes.

2. **Inspect the real data flow.** Use known paths and symbols; otherwise locate them before reading the relevant implementation, tests, configuration and callers. Read the needed function or section first, expanding only for an unresolved dependency or contradiction; do not default to whole-file or directory dumps. Resolve reversible local details from approved authority and repository patterns. Return conflicting authority or a choice meeting the router's material-decision criterion to `ddd-flow` for the earliest affected phase; apply the router's design-delta rule when the approved contract changes; adding files or choosing equivalent private algorithms is an implementation decision.

   For UI changes, including fixes to an approved existing screen, apply [ddd-design's stable-layout and content defaults](../ddd-design/references/ui-design.md#stable-layout-and-task-focused-content) against the latest approved baseline. Reuse an already-loaded valid reference; reading it does not reopen settled design or grant redesign authority.

3. **Prepare one coherent slice.** Reuse existing modules, seams, dependencies and test patterns. For substantive coding or refactoring, read the short [code-style entry](references/code-style.md) and only applicable language sections; project runtime/configuration wins. Read [architecture](../ddd-design/references/architecture.md) only for a real module or interface question not already settled by the design. Add an abstraction only for a current contract, isolation, lifecycle or variation need.

4. **Select necessary evidence, then implement.** Start with an unresolved behavior question, concrete regression risk or project-required check; reuse valid existing evidence. Mechanical changes start with the exact diff and relevant mapping, without unrelated suites, builds or captures. Before selecting or maintaining tests, use the still-valid [testing and test maintenance](references/testing.md) policy or retrieve its missing or updated task-relevant portions under [guidance reuse](../ddd-flow/SKILL.md#conditional-references); rereading this entry alone does not refresh that policy. Use `tdd` for requested test-first work or when non-trivial observable behavior has a stable public seam and an independent failing expectation that can guide implementation before it is written; otherwise use ordinary validation without retrofitting red-green. Preserve project test authorization and required checks.

5. **Keep the diff local.** Reject unsupported states explicitly; keep errors visible and retries bounded. Do not add speculative features, compatibility paths, unrelated refactors, duplicate validation or silent fallbacks. Do not edit authority-owning documents merely to make implementation appear conformant; respect the router's Persistent Write Boundary. Projects with many tests must arrange the shared policy's bounded reduction pass and resolve confirmed low-value cases inside approved scope while preserving distinct protection. Before freezing, complete necessary affected-test maintenance, including relevant unchanged tests. Return material disposition and concrete out-of-scope candidates through the existing report, without a new tracker or whole-project scan each cycle.

6. **Determine completion.** For a non-final slice, preserve shared approval and active-change state. For the final slice, update repository-owned completion metadata only when authorized and only after all approved work is complete. Never infer whole-change completion from one passing slice. Match each claim to its actual boundary: numerical consistency does not establish physical fitness; development startup does not establish packaged delivery; request timeout does not set a total preparation budget. Preserve approved metrics rather than inventing thresholds. Distinguish functional, visual, temporal and delivery evidence, and leave missing evidence unverified.

   For phase/status updates, apply the shared [State vocabulary and record-check method](../ddd-flow/references/recovery.md#state-vocabulary). Keep technical completion separate from G4 user acceptance.

   Apply the shared version decision to the complete change before final review or requested artifact construction. Routine version and change-record updates remain inside existing authorization; preserve source-only scope and report pending delivery checks.

7. **Freeze and review.** Freeze the diff against the recorded starting point. A worker returns the candidate and check evidence here; the main conversation invokes `ddd-review` with the Authority Baseline, approved deltas and complete frozen diff, optionally through an independent review worker. For a candidate to be committed, include the proposed boundaries and messages under [Git commit organization](../ddd-flow/references/git.md#commit-organization) in that review. Fix blocking implementation findings within the approved design autonomously. A semantic design change requires approval through the router; never modify design or acceptance to make divergent code appear conformant. After fixes, freeze the updated diff and reassess affected requirements, code and risks; expand to both full axes only when shared contracts or cross-cutting changes invalidate prior evidence. Then run proportionate validation. A finding that requires design change returns to `ddd-flow`.

8. **Accept and commit under repository policy.** The main conversation verifies the candidate against current authority through ddd-flow and applies the shared [Git organization and information checks](../ddd-flow/references/git.md#commit-organization) to each actual staged candidate before creating the repository-authorized local commits. Review and validation must cover that candidate; correct boundary or message findings within existing authorization before committing. Do not push or publish without separate authorization.

## Completion criterion

Worker execution finishes with a verifiable candidate or an explicit blocker; this does not complete the task. Whole implementation is complete when all requested approved slices are accepted, the frozen diff stays inside the Change Envelope, Design and Standards review pass, necessary validation and test maintenance are complete, unrelated changes remain protected, and repository completion and commit policy are satisfied. Once original outcomes and required protection are established, stop checks, probes and extra restarts; only a relevant change, new concrete failure or unmet required check reopens affected validation. Return to `ddd-flow` for remaining authorized delivery. Report unmet requirements and return actual behavior, check scope/results, review verdict, unresolved risk and commit information without relying on test counts.
