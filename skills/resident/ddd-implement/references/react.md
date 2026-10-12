# React

Read only where React is actually used, in addition to the changed JS or TS guidance. Put state in its real owner; derive values from props/state rather than duplicating them. Handle user actions in event handlers. Effects synchronize external systems with cancellation/cleanup and protection against stale request results. Do not split components by line count, move all local state globally or replace the existing state/request stack.

Reuse the [shared web guidance](typescript-javascript.md) already loaded; this body grants no framework or request-library migration.

The current validation target is stable React 19.2.x; use the project's declared version and compatible libraries. New-major adoption or compiler enablement is a separate decision, not a prerequisite for state and effect correctness. Keep cleanup and stale-result protection under the existing rendering lifecycle; optional newer APIs do not replace these contracts automatically.
