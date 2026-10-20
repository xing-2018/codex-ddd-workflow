# Testing and test maintenance

Use this policy when selecting, adding, changing or reviewing tests. It does not activate TDD or grant test creation/execution permission. Follow target-project required checks and still-valid authorization; keep repository-specific opt-in rules local and do not invent per-test approvals inside authorized work.

User limits apply to all verification, including probes, smoke and "runtime checks." Do not relabel a test to evade a no-test instruction or add another restart after the requested result is established. For an uninterrupted desktop, inspect launch, interaction and capture paths: no visible windows, focus changes or system input. If a method cannot meet the constraint, report missing evidence and continue permitted work.

## Select necessary evidence before running it

Each check must answer an unresolved approved-behavior question, protect a concrete regression risk, or satisfy a project requirement. Inspect relevant existing coverage and valid results first; reuse them when they answer the question. Being able to run a check, reaching a phase, changing a file or wanting extra confidence is not a reason.

For wording, formatting and mechanical changes, start with the exact affected diff and relevant mapping or structure. Add runtime checks only for a concrete loading, wiring or behavior risk that inspection cannot resolve. Do not append generic suites, builds or captures that do not cover the changed claim; project-required checks still apply.

Start from available evidence on the real product path. For a reported failure, recover original inputs, operation and failed outcome, then verify the missing repair evidence on that path when feasible and authorized. Add a probe only for a specific question existing observations cannot answer. If it conflicts with the real path, check its environment and assumptions before treating it as a product defect or extending diagnosis. Neither a nearby fixture pass nor a probe failure establishes the original outcome; report an unavailable original-path check as a gap.

Choose the narrowest reliable boundary. A stable public contract may belong to an internal module or pure function. Use independently justified expected outcomes, not the implementation's calculation or private structure. A behavior-preserving refactor should leave tests valid. Check relevant result, state and effects; several assertions may protect one coherent behavior.

Prefer existing checks, real implementations or faithful fakes at the subject's dependency boundaries. Keep interaction assertions only when contractual, and real integration checks for risks a fake cannot exercise. Do not replace the subject or redesign approved architecture for mocking. Do not add wording/source-text assertions duplicating static checks. Integrity and structure checks may protect their own contracts; do not report them as functional or visual evidence.

Add a durable test only for missing long-term protection; reuse or update an existing case first. Create a reusable harness only when the deliverable requires it or existing methods cannot cover a concrete durable gap. Setup serves that gap rather than becoming another implementation project.

Expand beyond direct checks only for project requirements, explicit user requests or identified shared-contract risks affecting additional consumers. Name the affected protection first; broad directory membership or uncertainty alone is insufficient. Inspect the relevant dependency when impact is unclear. Do not replace required integration or delivery evidence with a narrow pass.

## Select visual evidence

Identify whether the unresolved claim concerns function, state, performance or appearance. Results, saved data and timings do not automatically need screenshots; font, clipping, occlusion and layout claims need actual visual evidence. Capture and model inspection are separate actions: keep a required artifact without emitting it when existing evidence already answers the question. Consider automatic image returns before invoking a tool; honor its return protocol rather than bypassing it.

Inspect the relevant region at a resolution sufficient for the question before expanding to a whole screen, long page or native pixels. Reuse evidence for unchanged regions, states and layout. Determine which claims a change invalidates, including shared-layout and pagination effects; expand only when the impact or observed defect extends beyond that boundary. Do not substitute bulk OCR, long DOM dumps or repeated model calls merely to avoid images. Use existing authorization for necessary in-scope checks, without image quotas, per-image approval or another tracker. Stop when the approved claim has evidence; disclose uninspected scope. Requested image analysis, explicit full coverage and genuine visual failures retain their checks. Document layout selection uses [document visual inspection](../../chinese-docs/references/review.md#visual-inspection), not automatic whole-document reading.

## Diagnose failures and stop when evidence is sufficient

Control relevant time, randomness, shared state and dependencies at the selected boundary. Use bounded condition-based synchronization for asynchronous work; preserve real timing, concurrency and integration when they are the subject, and disclose environmental limits.

Reuse the project's verified test entry and last successful invocation, resolving only missing or changed host, working directory, executable and arguments before execution. Locate the first failed boundary actually reached and distinguish behavior failures from entry, fixture, environment or infrastructure failures, skips and unperformed checks. In a dependent sequence, preserve each step's exit status and stop at a failed prerequisite such as preparation, copying, building or launching; a later command must not silently consume an older artifact or mask that failure. Confirm the required artifact or entry when exit status alone cannot establish readiness. Independent authorized checks may continue. A broken prerequisite is not a TDD red unless the target behavior expectation was reached.

Before retrying, identify the correction or new evidence. After an entry, fixture or individual case fix, rerun the narrowest check that reaches the failed boundary and establish that its prerequisite is repaired before resuming dependent checks. A shared implementation change widens that scope only to identified affected protection. Keep still-required final integration and delivery checks, and reuse their valid results; do not rerun the surrounding group merely because one case remains red. Preserve the first failure and retry reason/result; a retry pass alone does not establish stability.

Apply [Evidence validity](../../ddd-flow/references/execution.md#evidence-validity) for input, scope, dependency, integration and formal-identity rules; reuse its valid excerpt or retrieve only that missing section. Testing adds the selection, failure diagnosis, retry and maintenance rules here, without loading dispatch or task-management sections.

The main conversation's [result acceptance method](../../ddd-flow/references/execution.md#accept-a-result) still owns complete semantic review, including source-backed content; check counts or passing syntax cannot replace it. This ownership pointer does not require workers to load management sections.

Repeat an unchanged failed check only for a stated diagnostic or flakiness question. Once original outcomes and required protection have sufficient evidence, stop: no extra suite, probe, restart or new test at phase transition, report cleanup or commit. A relevant change, new concrete failure or unmet required check reopens only affected work.

## Reduce existing tests without losing protection

Ordinary implementation inspects and maintains affected protection. Arrange a bounded reduction pass only for an explicit user request, a project requirement, or concrete redundancy obstructing the current verification; a large test count alone does not trigger it. Use existing entry points, source and available failure/duration records, without first running or reviewing every case. Broader cross-module cleanup needs its own covered scope and concrete plan; a trigger grants no missing write or test permission. Put confirmed in-scope low-value cases into the authorized change: merge or remove redundant protection, rewrite tests coupled to incidental internals, and retire tests for explicitly withdrawn or replaced behavior. Resolve those cases before delivery, rather than leaving an optional cleanup suggestion.

For each merge, removal or rewrite, identify retained behavior, relevant inputs, failure paths and boundaries. Shared code coverage, a lower count, age or slowness does not prove redundancy. Preserve distinct numerical, security, concurrency, integration and actual-regression protection. Narrow costly setup or assertions when possible; never weaken or skip a valid test to obtain a pass. Source/structure assertions remain valid when the structure itself is contractual. If protection or authority is uncertain, retain the case and report the specific gap.

Keep reduction within approved write scope; present concrete out-of-scope candidates for separately scoped cleanup. After the pass, maintain tests affected by later changes, including relevant unchanged tests, without restarting whole-project cleanup each task. No deletion quota or fixed coverage/E2E ratio is required; a justified retained suite is valid.

Separate disposable probes from durable regressions. Remove authorized task-created disposable artifacts before delivery, preserving user evidence and requested diagnostics. Promote a reproduction only for missing long-term protection. Check affected retained tests, reusing evidence cleanup has not invalidated.

## Ownership and reporting

Implementers complete necessary maintenance before freezing the diff; workers stay in assigned scope and return shared/excluded candidates. Reviewers verify selection, stopping and retained protection on the frozen surface, reusing valid implementation evidence. Confirmed unjustified additions, unresolved in-scope redundancy or lost protection are actionable findings.

Use the existing completion report or return: protected behavior, coverage choice and independent expectation, relevant isolation, checked inputs, actual command/results/retries and gaps, plus material test changes and retained protection. Keep it proportional: no per-test form, extra tracker or report merely to say nothing changed. Report established facts rather than assertion totals. Efficiency assessment includes preparation, fixture repair and orchestration as well as execution; fewer tests or shorter text alone does not prove faster development.
