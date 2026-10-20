# Code style and runtime compatibility

Read only for substantive coding, refactoring or code-quality review. Project authority, supported runtime, existing configuration and adjacent conventions take precedence. This method grants no permission to format unrelated files, migrate strictness, change tools/dependencies or reorganize directories. Implementation and review share this entry.

- Name domain meaning, units and responsibility; follow existing identifier conventions. Explain reasons, assumptions, constraints and non-obvious behavior in comments using the applicable project's language; do not mandate documentation on every short private function.
- Prefer clear control flow over dense chains, nested ternaries or implicit effects. Split by responsibility and caller understanding, not fixed line/file limits.
- Inspect affected paths, or the user's specified optimization scope, for repeated computation/validation, round-trip data conversions, mixed responsibilities, dense conditions and wrappers without responsibility. Splitting or merging must improve caller understanding, ownership or maintenance cost; file/line counts only locate review attention and do not establish quality. Preserve necessary numerical, boundary and resource protection. Use the shared architecture judgment for structural consequences rather than adding another checklist or whole-project pass.
- Distinguish input validation, I/O, computation, state and presentation without requiring a layer or file for each. Validate at trust boundaries and reuse established internal invariants.
- For each added default, retry, compatibility or repeated defensive check, identify the real contractual failure state and whether a prior invariant can actually become invalid. External requests, persistence recovery, process messages, third-party outputs and concurrent state remain trust-boundary questions; internal types alone do not prove permanent validity. Preserve numerical units, applicability and stability, and resource/thread invariants. Remove branches without a justified state, not checks merely because they add lines.
- Public contracts expose input/output, errors and effects. Preserve causes; retries need conditions, limits and termination. Do not swallow errors, pretend success or silently change behavior.
- Each class, interface, dependency or configuration needs a current reason. Ordinary functions and existing concrete APIs are the starting point; small local duplication can be preferable until shared meaning stabilizes.
- Preserve generated/upstream ownership. Use existing read-only formatter/linter/type/compiler checks when authorized; tools handle mechanical checks, review handles semantics and trade-offs. Do not introduce a second tool chain merely because installed tools are available.

For requested readability or structure optimization, compare the actual result with that goal. Explain structural changes and their benefit in the existing completion report. Comments alone can be sufficient only when inspection supports that choice; give the reason and disclose structural issues still unaddressed. Passing tests or an unchanged executable AST does not establish structural simplification. Resolve confirmed in-scope issues under existing authorization; material contract changes return to design, and out-of-scope findings do not authorize a broader refactor.

Select only the relevant language or branch, reusing unchanged guidance already loaded:

| Changed surface | Reference |
| --- | --- |
| Modern Python application, package or numerical module; new baseline 3.11+ | [Python](python.md) |
| Legacy embedded/solver Python, including Python 2.7 | [Legacy Python](python-legacy.md) |
| JavaScript, including a single HTML tool | [JavaScript](javascript.md) |
| TypeScript | [TypeScript](typescript.md) |
| React where actually used | Add [React](react.md) to the applicable JS or TS guidance |
| C++ or MFC | [C++](cpp.md) |

For a JS/TS surface, read the short [shared web entry](typescript-javascript.md) once. Load only the selected language body; do not preload the other language, React or a different Python runtime. An existing supported interpreter determines the Python row, not the management tool's interpreter.

Current default validation uses modern, mature targets and excludes legacy-version scenarios. Do not expand a task into old-version testing unless the user's actual project contract requires it.

Unresolved architecture uses [architecture](../../ddd-design/references/architecture.md) and, only for project/runtime choices, [stack adaptation](../../ddd-design/references/stack-adaptation.md). Testing remains owned by [testing](testing.md); reading style does not activate TDD or authorize extra tests.

For an evidenced recurring error, prefer correcting state ownership or a single source of truth and using existing types/static checks before adding a necessary behavior test or a rule requiring human judgment. A new check needs evidence that it rejects the real error or an equivalent minimal counterexample; if execution is not authorized, report that gap. Source-wording matches do not prove model behavior. Use [architecture's structural consequences](../../ddd-design/references/architecture.md#judge-structural-consequences) for responsibility findings rather than copying a second smell checklist.
