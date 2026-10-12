# Legacy embedded or solver Python

Read for a legacy host interpreter, including Python 2.7. Keep the host's API, startup contract and supported syntax. Inspect the changed subproject's supported interpreter and existing checks; keep management and product/solver interpreters separate. Do not load modern Python guidance for this task.

Follow project names and supported conventions. Prefer functions; use classes when state and behavior share a lifecycle. Do not propagate a management tool's Python 3.11+ prerequisite, modern typing syntax or automatic syntax upgrades into the solver script. Isolate independently maintained computation only when responsibility or current verification requires it; no framework migration follows from this guidance.

Release resources with context managers supported by the host. Catch exceptions where they can be handled, translated or given useful context; preserve original error information using supported syntax. Identify blocking I/O, solver work, cancellation and ownership through the host's existing execution model. Numerical contracts state units, shapes, precision, tolerance and valid inputs, retaining independent reference values when verification needs them.
