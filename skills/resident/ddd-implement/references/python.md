# Python

Read for a modern Python application, package or numerical module. Inspect the changed subproject's supported interpreter, dependency declarations/lock, startup and existing checks; keep management and product/solver interpreters separate. Legacy embedded/solver Python uses [its own guidance](python-legacy.md) instead of this body.

For newly authorized Python work without a narrower project target, use Python 3.11+ as the baseline and a maintained patch release. Features introduced after that minimum require a compatible declared target; do not silently raise the minimum to use newer syntax. Current default validation does not spend runs on Python 2 or obsolete interpreters; explicit existing host constraints still govern that project.

## Shared decisions

Follow project names; for new code use meaningful snake_case functions/variables and PascalCase types. Annotate public boundaries, complex records and non-obvious returns; simple locals can rely on inference. Prefer functions; use classes when state and behavior share a lifecycle. Use dataclass for suitable lightweight records, TypedDict for mapping shapes, and existing validation models at external boundaries without repeated internal conversions.

Release resources with context managers. Catch exceptions where they can be handled, translated or given useful context while preserving causes. An async keyword does not make blocking I/O, solver work or computation nonblocking; identify scheduling, cancellation and ownership. Numerical contracts state units, shapes, precision, tolerance and valid inputs, retaining independent reference values when verification needs them.

For Python 3.11+ concurrent work, TaskGroup can own related tasks and asyncio.timeout can bound a scope. Preserve cancellation and exception-group semantics rather than swallowing failures. Use the project's async I/O or an appropriate thread boundary for blocking calls; cancelling an await does not prove an underlying thread has stopped. A generator returned from a resource scope must not defer reads until after that resource closes; annotations must describe the actual return.

## Modern application or distributed package

Reuse the existing Ruff configuration and the project's chosen type checker; do not add multiple equivalent checkers. Match syntax and target-version to the minimum supported interpreter. Public package consumers and installation/import behavior may justify a src layout; a one-off script need not acquire packaging machinery.

For a newly requested personal small script, preserve a directly runnable main() and a reasonable configuration entry usable from the chosen IDE; CLI may supplement it. Do not impose this preference on established CLI projects or upstream packages.
