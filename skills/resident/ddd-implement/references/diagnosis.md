# Diagnosis and repair

Read this method after the `ddd-implement` entry selects `diagnose` or `repair`. A diagnosis request grants read-only investigation, not a repair. A repair request authorizes changes only within the existing approved behavior and project permissions.

## Establish the failure

Recover the reported symptom, expected behavior, affected environment and approved contract from available project and session evidence. Use existing real-path observations first, reproducing only missing evidence with authorized tools before asking the user to classify a visible failure; for UI failures include the relevant route, console, network or server evidence. When the failing step is unclear, inspect a bounded set of plausible paths. Follow the shared [testing policy](testing.md) when choosing additional probes or handling conflicting results. If the environment is inaccessible, continue static and log analysis and identify only the evidence or permission that blocks proof.

In `diagnose` mode, inspect existing code, logs and checks. Use disposable probes outside project files only when permitted; project-local instrumentation, tests, configuration and persistent records remain unchanged. Never interpret an available fix as permission to apply it. Redact credentials and personal data from commands, output and retained evidence; keep necessary secrets in the environment. Report observations, competing hypotheses, causal evidence, unknowns and the smallest credible correction direction.

## Choose the investigation depth

For an obvious deterministic defect, use the existing symptom-specific signal and trace the real call path. Otherwise read only the needed part of [deep diagnosis](deep-diagnosis.md) when cause remains unproven, a reliable signal is unavailable, minimization or instrumentation is needed, behavior is intermittent, or performance requires measurement. A substitute fixture must preserve causally relevant instance boundaries, shared state, lifecycle and actual error shapes; a local regression pass does not establish the original runtime outcome.

Use the shared [testing policy](testing.md) before selecting or changing automated checks. An executed symptom-specific failure signal is preferred. When execution is unavailable, state what was attempted and what remains unverified rather than guessing a cause.

## Repair only when authorized

In `repair` mode, correct the proven root cause within the existing contract, verify the original failure path and relevant retained checks, and review the frozen diff on both axes with `ddd-review`. A material change to behavior, interface, data or approval scope returns to `ddd-flow` before dependent edits. Do not weaken a test or rewrite design to justify a divergent implementation. Remove only task-created disposable probes after preserving relevant evidence. Complete applicable Git, version and delivery obligations. Report what the original path actually proved and any unavailable runtime check; a nearby synthetic pass does not establish full repair. Technical checks and repair evidence do not confer user acceptance or external-action permission.

An explicitly delegated evidence worker uses [the read-only worker entry](../SKILL.md#delegated-evidence-worker-entry) and its packet, not the main-conversation repair path. It answers its assigned exploration or causal question and returns locatable observations, inferences, unknowns and an explicit no-write result.
