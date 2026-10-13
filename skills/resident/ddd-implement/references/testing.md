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

## Diagnose failures and stop when evidence is sufficient

Control relevant time, randomness, shared state and dependencies at the selected boundary. Use bounded condition-based synchronization for asynchronous work; preserve real timing, concurrency and integration when they are the subject, and disclose environmental limits.

Reuse the project's verified test entry and last successful invocation, resolving only missing or changed host, working directory, executable and arguments before execution. In combined commands, preserve each check's exit status; a later success cannot mask an earlier failure. Distinguish behavior failures from entry/fixture/environment/infrastructure failures, skips and unperformed checks. Correct a broken entry or prerequisite before rerunning; it is not a TDD red unless the target behavior expectation was reached.

After an entry, fixture or individual case fix, rerun the failed boundary first. A shared implementation change widens that scope only to identified affected protection. Keep still-required final integration and delivery checks, and reuse their valid results; do not rerun the surrounding group merely because one case remains red. Preserve the first failure and retry reason/result; a retry pass alone does not establish stability.

Reuse passing evidence while relevant code, inputs, dependencies, environment and acceptance remain unchanged. Bind shared evidence to the actual dependency revision or dirty-content identity, not merely HEAD; peer changes invalidate only affected claims. Rerun invalidated checks and still-required integration/delivery checks, coordinating the latter on a frozen shared candidate. Do not rehash or recheck all unchanged inputs solely to demonstrate reuse.

Repeat an unchanged failed check only for a stated diagnostic or flakiness question. Once original outcomes and required protection have sufficient evidence, stop: no extra suite, probe, restart or new test at phase transition, report cleanup or commit. A relevant change, new concrete failure or unmet required check reopens only affected work.

## Reduce existing tests without losing protection

Projects with many tests must arrange one bounded reduction pass using existing entry points, source and available failure/duration records. Do not start by running or reviewing every case. Put confirmed low-value cases into the authorized change: merge or remove redundant protection, rewrite tests coupled to incidental internals, and retire tests for explicitly withdrawn or replaced behavior. Resolve confirmed in-scope cases before delivery, rather than leaving an optional cleanup suggestion.

For each merge, removal or rewrite, identify retained behavior, relevant inputs, failure paths and boundaries. Shared code coverage, a lower count, age or slowness does not prove redundancy. Preserve distinct numerical, security, concurrency, integration and actual-regression protection. Narrow costly setup or assertions when possible; never weaken or skip a valid test to obtain a pass. Source/structure assertions remain valid when the structure itself is contractual. If protection or authority is uncertain, retain the case and report the specific gap.

Keep reduction within approved write scope; present concrete out-of-scope candidates for separately scoped cleanup. After the pass, maintain tests affected by later changes, including relevant unchanged tests, without restarting whole-project cleanup each task. No deletion quota or fixed coverage/E2E ratio is required; a justified retained suite is valid.

Separate disposable probes from durable regressions. Remove authorized task-created disposable artifacts before delivery, preserving user evidence and requested diagnostics. Promote a reproduction only for missing long-term protection. Check affected retained tests, reusing evidence cleanup has not invalidated.

## Ownership and reporting

Implementers complete necessary maintenance before freezing the diff; workers stay in assigned scope and return shared/excluded candidates. Reviewers verify selection, stopping and retained protection on the frozen surface, reusing valid implementation evidence. Confirmed unjustified additions, unresolved in-scope redundancy or lost protection are actionable findings.

Use the existing completion report or return: protected behavior, coverage choice and independent expectation, relevant isolation, checked inputs, actual command/results/retries and gaps, plus material test changes and retained protection. Keep it proportional: no per-test form, extra tracker or report merely to say nothing changed. Report established facts rather than assertion totals. Efficiency assessment includes preparation, fixture repair and orchestration as well as execution; fewer tests or shorter text alone does not prove faster development.
