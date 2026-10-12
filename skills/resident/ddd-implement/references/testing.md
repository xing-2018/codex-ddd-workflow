# Testing and test maintenance

Apply this policy when selecting, adding, changing or reviewing automated tests, whether work uses ordinary testing or TDD. Reading it does not activate either DDD or TDD, authorize test creation/execution, or override project rules and required checks. TDD is a separate test-first development method, not the owner of routine testing.

Apply the active target project's rules and still-valid user authorization. A repository-specific opt-in restriction stays with that repository; do not export it to other projects or invent per-test approval gates for already-authorized work.

Treat the user's current scope and operating constraints as conditions for running a check. A request for validation does not authorize a more intrusive method. When the user requires an uninterrupted desktop, a check must neither display windows in their workspace nor take focus or send system input; preventing focus alone is insufficient. Inspect the launch, interaction and capture paths before running it. If the available method cannot meet the constraint, do not run that method; report the missing runtime evidence and continue with permitted checks.

## Select the smallest sufficient evidence

Start from the approved behavior, contract or material regression risk and inspect existing coverage before writing a test. Reuse or update an existing case or fixture when it can express the missing protection without losing distinct assertions. Add a durable test only for a concrete gap; a new function, file, fix or development cycle alone is not a reason.

For a reported failure, identify the original inputs, operation and failed outcome before selecting checks. Verify the repaired outcome on that path when it is feasible and authorized. A changed fixture, a successful harness run or a count of completed scenarios does not establish that the user's original failure is fixed. State any remaining gap without substituting a nearby success.

Choose the test subject and its stable public contract: an internal domain module or pure function can be a subject, not only the product's outermost API. Test observable outcomes with independently justified expected results, not private structure or the implementation's own calculation. A behavior-preserving refactor should not break tests merely because internals changed. One coherent behavior may need several assertions about its result, state and effects; do not split it merely to enforce one assertion per test.

Prefer real implementations or faithful fakes at the chosen subject's dependency boundaries. Repository ownership does not define that boundary. Preserve the dependency contract and the real integration checks needed for risks a fake cannot exercise; do not replace the behavior under test or redesign approved architecture solely for easier mocking. Use interaction assertions only when the interaction is itself part of the contract. Do not add wording/source-text assertions that merely duplicate existing static checks.

Choose the narrowest reliable checks that exercise the affected failure boundary, while preserving required integration and delivery checks. Mechanical changes need proportionate verification, not automatic permanent test additions. Do not optimize for test counts, a fixed E2E ratio or an invented coverage target; different levels may protect different failures even when they share a requirement.

Prefer an existing check over a new harness. Create a reusable harness only when the requested deliverable requires it or existing checks cannot cover a concrete, durable gap. Run a broad suite when the target project requires it, the user requests it, or an identified cross-cutting risk needs it; do not make it a routine step after every local change.

## Execute and interpret checks

Make checks repeatable at the chosen boundary: control relevant time, randomness, shared state and external dependencies; isolate test data and clean up owned resources. For asynchronous behavior, prefer bounded condition-based synchronization to arbitrary sleeps. Preserve real timing, concurrency or integration behavior when it is the subject of the check, and disclose environmental limits that cannot be controlled.

Distinguish behavior assertion failures from setup or infrastructure failures, skipped cases and checks not run. Preserve the initial failure and reasons and outcomes of retries; a retry pass alone does not establish stability. Report unresolved flakiness and missing required evidence instead of treating them as a clean pass.

Reuse a passing check while the code, inputs and environment relevant to its claim remain unchanged. With concurrent tasks, bind reused checks to the actual shared input/dependency revision or dirty-content identity, not just this task's commit; peer changes invalidate only claims they affect. Coordinate still-required integration checks on a frozen shared candidate rather than independently repeating the same unchanged evidence. After a change, rerun the checks whose evidence it invalidates, plus still-required integration or delivery checks. Repeat an unchanged failed command only to investigate a concrete uncertainty or intermittent result; do not use repeated runs as a substitute for diagnosing its failure. Stop expanding validation once the original outcome and required risk boundaries have sufficient evidence.

## Maintain affected tests before delivery

Inspect tests related to the changed behavior, including unchanged tests, rather than scanning the whole repository by default. Within authorized implementation or repair scope, decide which need to be retained, updated, consolidated or removed. Related test maintenance is part of the change, not unrelated refactoring.

Remove an obsolete case only when its expected behavior has been explicitly retired or replaced by approved authority. Consolidate redundant or implementation-coupled cases only after identifying the retained behavioral protection, including relevant inputs, failure paths and boundaries. Preserve distinct numerical, security, concurrency and regression guarantees. Age, slowness, shared line coverage or a lower test count alone does not justify deletion. Never delete, weaken or skip a valid test to make checks pass. If protection or authority is uncertain, retain the test and report the specific uncertainty.

Separate task-created disposable probes and temporary checks from durable regression tests. Remove disposable artifacts before delivery, preserving user evidence and explicitly requested diagnostic artifacts. Promote a reproduction into the permanent suite only for a missing long-term safeguard; otherwise reuse existing coverage. Run authorized checks for the retained affected tests, reusing valid evidence when cleanup has not invalidated it.

## Completion and ownership

Implementers complete this maintenance before freezing their diff; workers do so within their write scope and return shared or out-of-scope candidates to the main conversation without editing them. Reviewers inspect the same affected test surface and report unjustified additions, confirmed obsolete/redundant cases or lost protection as actionable findings. Resolve confirmed in-scope violations before acceptance; retain and disclose uncertain or unauthorized items rather than silently discarding them or claiming cleanup.

Use the existing completion report or worker return and linked requirements, tests and logs to make these acceptance facts recoverable for the affected change:

| Fact | Sufficient evidence |
| --- | --- |
| Contract | Approved behavior or requirement being protected |
| Coverage choice | Concrete gap, reused coverage, or why a durable test is unnecessary |
| Expected result | An independent oracle, worked example or requirement |
| Execution reliability | Relevant isolation and dependency controls, with unresolved limits |
| Result | Checked revision and scope, command or run reference, actual outcome, retries and unperformed required checks |
| Existing tests | Material additions, updates, consolidations or removals, their reasons and retained protection; unchanged coverage may be referenced |

Keep the report proportional; reuse evidence instead of filling a form for each test. Do not create a separate tracker or require a cleanup quota. Repository-wide historical cleanup requires its own scope.
