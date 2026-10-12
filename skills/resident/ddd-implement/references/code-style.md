# Code style and runtime compatibility

Read only for substantive coding, refactoring or code-quality review. Project authority, supported runtime, existing configuration and adjacent conventions take precedence. This method grants no permission to format unrelated files, migrate strictness, change tools/dependencies or reorganize directories. Implementation and review share this entry.

- Name domain meaning, units and responsibility; follow existing identifier conventions. Explain reasons, assumptions, constraints and non-obvious behavior in comments using the applicable project's language; do not mandate documentation on every short private function.
- Prefer clear control flow over dense chains, nested ternaries or implicit effects. Split by responsibility and caller understanding, not fixed line/file limits.
- Distinguish input validation, I/O, computation, state and presentation without requiring a layer or file for each. Validate at trust boundaries and reuse established internal invariants.
- Public contracts expose input/output, errors and effects. Preserve causes; retries need conditions, limits and termination. Do not swallow errors, pretend success or silently change behavior.
- Each class, interface, dependency or configuration needs a current reason. Ordinary functions and existing concrete APIs are the starting point; small local duplication can be preferable until shared meaning stabilizes.
- Preserve generated/upstream ownership. Use existing read-only formatter/linter/type/compiler checks when authorized; tools handle mechanical checks, review handles semantics and trade-offs. Do not introduce a second tool chain merely because installed tools are available.

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
