# Planning and task records

Load only for a planning request or work needing a graph or durable execution record. Apply ddd-flow authority and write boundaries. Planning alone never authorizes execution.

1. **Organize only the work needed.** Register a narrow research question or pending decision directly. Split implementation into vertical slices only when scale or real blocking dependencies require a graph. Each implementation task must:

   - deliver a narrow but complete path through every required layer;
   - be independently demonstrable or verifiable;
   - fit one fresh implementation context;
   - point to the exact approved design sections it delivers;
   - preserve approved architecture; and
   - declare only tasks that genuinely block it.

   Do not split by database, backend, frontend and tests when those layers are useful only together. Use expand–migrate–contract only for a wide mechanical shape change that cannot stay green as vertical slices.

2. **Maintain one execution owner per change.** Use `.planning/changes/<change>/record.md` and its conversation binding in the `STATE.md` index under [project adaptation](project-adaptation.md). Necessary initialization and lossless structural migration accompany authorized project writes; read-only or explicitly excluded writes use a conversational checkpoint and report the gap. Existing task trackers remain evidence owners linked from this entry, without copying their histories or deleting them. Keep tasks out of design documents.

   Add a Tasks table only for real dependencies and Attempt sections only for delegation, retries or retained execution history. Preserve attempt identity, scope and acceptance evidence under [execution's recovery rules](execution.md#resume-from-durable-evidence). Use [plan](../assets/plan.md) only for multiple slices; one slice belongs in `record.md`. Create [brief](../assets/brief.md) and [design](../assets/design.md) only when the task needs those approval objects, linking existing facts where applicable. Do not manufacture documents or approvals merely to fill a template.

A planning request is complete when verifiable slices cover its requested scope with real dependencies. Execution and acceptance follow [execution.md](execution.md).
