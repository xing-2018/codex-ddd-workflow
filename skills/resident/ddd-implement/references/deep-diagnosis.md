# Deep Diagnosis

Read when the cause is unproven, a reliable failure signal is missing, minimization or instrumentation is needed, behavior is intermittent, or performance needs measurement. Apply the authorization, redaction and reporting rules in [the entry](../SKILL.md); this method grants no additional write permission.

## Phase 1: Build a feedback loop

This is the core of the skill. Build a tight pass/fail signal that goes red on **this bug** before developing a theory.

In diagnosis-only mode, use an existing signal or a disposable probe outside tracked project files. Creating a project-local test, harness, or instrumentation requires write authorization.

Choose a low-cost, reliable signal for the reported symptom using existing evidence and the available environment. Options include:

1. failing test at the highest seam that reaches the bug;
2. curl / HTTP script against a running dev server;
3. CLI invocation with fixture input and known-good output;
4. headless browser script that asserts DOM, console, or network behavior;
5. replay of a captured request, payload, trace, or event log;
6. throwaway harness around the smallest real code path;
7. property / fuzz loop for intermittent wrong output;
8. `git bisect run` only when the regression lies between known states and the checkout is already authorized for revision switching and writes; otherwise use read-only revision comparison or other evidence;
9. differential loop comparing old/new versions or configurations;
10. a human-in-the-loop script only when a human action is unavoidable: use [Windows HITL template](../scripts/hitl-loop.template.ps1) on native Windows and [POSIX HITL template](../scripts/hitl-loop.template.sh) on POSIX systems.

Tighten the loop until it is as fast, deterministic, and specific as practical. For non-deterministic bugs, raise the reproduction rate by repetition, controlled stress, or timing instrumentation instead of pretending the bug is deterministic.

If a red-capable loop is unavailable, state what you tried and continue feasible static tracing, log analysis or independent evidence checks. Ask only for the environment, artifact or instrumentation permission that blocks further proof. Do not guess a business-logic fix or claim runtime verification without running it.

**Completion criterion:** identify an executed symptom-specific reproduction, or document why execution is unavailable and the strongest independent evidence obtainable. In the latter case, keep runtime verification explicitly unverified; advance only work supported by the evidence.

## Phase 2: Reproduce and minimise

Run the loop and confirm it produces the user's failure, not a nearby one. Then simplify the disposable reproduction by removing inputs, callers, configuration, data, and steps one at a time, rerunning after each cut. Do not delete or rewrite the user's original evidence.

Stop minimising when the reproduction is small enough to distinguish causes and validate a fix; do not prove every remaining element indispensable. Preserve the original unminimised reproduction for final verification.

## Phase 3: Hypothesise

When the cause is not proven, rank only plausible competing hypotheses and run the cheapest discriminating check; do not invent hypotheses to meet a quota. Each must be falsifiable:

> If X is the cause, then changing or observing Y will make the bug disappear, worsen, or produce Z.

Discard hypotheses that cannot make a prediction. Show the ranked list to the user before testing when their domain knowledge could cheaply rerank it; do not block if they are AFK.

## Phase 4: Instrument

Map every probe to a prediction from Phase 3. Change one variable at a time.

Prefer:

1. debugger / REPL inspection;
2. targeted logs at boundaries that distinguish hypotheses;
3. never "log everything and grep".

Tag temporary logs with a unique prefix such as `[DEBUG-a4f2]` so cleanup is mechanical.

Adding logs or other project-local instrumentation is a write. In diagnosis-only mode, use existing observability, a debugger, or an external probe; ask for authorization if those cannot distinguish the hypotheses.

For performance regressions, measure first: establish a baseline timing, profiler result, or query plan and use differential or bisection evidence rather than log volume.

## Phase 5: Fix and regression test (diagnosis-and-fix mode only)

Skip this phase in diagnosis-only mode.

Before the fix, reuse or extend an existing regression test that exercises the real bug pattern at the call site. Apply [testing and test maintenance](testing.md); add a durable test only when that protection is missing and test creation is authorized. A shallow test that cannot reproduce the chain gives false confidence. This regression workflow does not require invoking TDD.

If no correct seam exists, record that as an architectural finding instead of inventing a misleading test.

When a seam exists:

1. reuse or extend the existing regression test, or promote the minimised repro into a behavior test only for the identified coverage gap;
2. confirm it fails for the reported bug, reusing valid failure evidence;
3. apply the smallest root-cause fix;
4. watch it pass;
5. verify the original Phase 1 feedback loop; reuse the regression result if it is the same check with unchanged inputs, otherwise run the original reproduction separately.

Repair the earliest proven wrong boundary or shared cause. Reject unsupported states explicitly; keep errors visible and retries bounded. Do not substitute silent fallback, repeated validation, or speculative framework code for a root-cause fix.

## Phase 6: Cleanup

Remove disposable probes or artifacts created during diagnosis. In diagnosis-and-fix mode, before declaring done:

- require the entry's valid passing evidence for the original reproduction and regression check, reusing fix-phase results when cleanup did not invalidate them; report the original runtime symptom as unverified when execution is unavailable, or explain why no truthful regression seam exists;
- remove all temporary `[DEBUG-...]` instrumentation;
- complete the shared test policy's affected-test maintenance;
- remove throwaway debug code; keep explicitly required diagnostic artifacts separate from the permanent test suite;
- state the proven root cause in the final report or commit message;
- recheck the approved design and task scope.

For a product repair, complete the shared increment/no-increment decision and applicable version bindings before final validation or requested artifact construction. Apply its delivery checks when delivery is authorized; report pending evidence for source-only work. A passing bug reproduction alone does not complete requested artifact delivery.
