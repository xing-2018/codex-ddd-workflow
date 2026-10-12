# Design Approval and Evidence Permission

Read when preparing an initial design or semantic delta, resolving authority or persistence uncertainty, or preparing temporary evidence outside authorized implementation. Read before a design-only UI preview. This reference elaborates applicable AGENTS permissions; it grants no exception to host or tool restrictions.

## Prepare and approve

When the user corrects or clarifies the requested behavior, carry forward the original task and still-valid authorization. Treat the correction as a requirement update, not permission to write or approval of associated behaviors. Investigate its impact read-only; if intent, scope or the execution permission is uncertain, present the interpretations and affected plan for user approval before dependent changes. Continue independent authorized work. Authorization to implement a destructive capability does not by itself authorize executing it on real user data.

Prepare a detailed change plan read-only in the conversation before writing. Recover the current flow and authority, then describe the goal, current state, concrete edits and affected targets, behavior and impact, constraints, acceptance, exclusions, validation, recovery where relevant and delivery boundaries. Scale detail to the change while retaining these decisions; file lists are forecasts unless explicitly locked. Distinguish user-stated requirements, agent proposals and unknowns. Combine related requirements, design and execution objects in one review when settled; do not manufacture separate phase approvals.

Obtain explicit approval of new design semantics and explicit authorization of the proposed execution before dependent changes. Requirements, design approval and execution authorization are different objects; one clear reply can cover all of them when the question identifies them. A desired outcome, development request, acknowledgment or instruction to continue does not alone grant write permission. For example, a request to simplify a workflow settles a direction, not the agent's merge/removal plan. Approval to modify the shown plan, implement the identified slice or act autonomously within stated boundaries can grant execution; resolve the actual object and scope from context, not a keyword test. If any remains uncertain, ask the user and wait. Missing persistent design files alone do not invalidate recoverable conversation approval.

Explicit bounded autonomy may authorize preparing the concrete plan and executing it without another approval reply. State that plan before acting, verify that each action stays within the delegated decisions and permissions, and return uncovered interpretations, semantic choices or actions to the user. Autonomy does not override an explicit review-first condition or a separate permission gate. An already approved plan and execution scope need no repeated presentation or per-file confirmation.

Within approved design and implementation scope, choose files, equivalent private algorithms, test cases and execution order autonomously. Preserve locked details. Fix implementation and review defects without renewed approval; code, tests and experiments cannot redefine the contract.

If evidence reveals infeasibility, conflict or a better material design, present only the semantic delta, reason and impact. Pause dependent actions; continue independent authorized work. Never lower acceptance or rewrite design to legitimize divergent implementation.

## Persist faithfully

Changing authoritative requirements, designs or acceptance is a semantic change even when no code changes. Writing a candidate as a current fact is not read-only planning. Task records, support documents, generated or ignored artifacts and temporary files are also writes; approval of their subject does not by itself authorize persistence.

When explicit execution authorization includes persistence, record the approved design faithfully in its existing or designated owner without another per-file confirmation. Optional ADRs or support documents must have a task purpose and covered write permission. On approval of a delta and its execution, update its owner and resume within that scope. Preserve identifiable approval evidence through the conversation or existing repository mechanism; never fabricate approval or certification records. Uncertain persistence scope returns to the user before writing.

## Temporary evidence and UI previews

A request to design or improve a UI starts with read-only investigation and a preview plan; it does not by itself authorize creating or changing preview files or supporting evidence. Obtain explicit preview-write authorization unless valid bounded autonomy already covers it. Identify the representative path, simulated behavior, artifact and supporting targets, verification and limits before acting. This permission does not approve the resulting design or authorize production implementation.

Before an authorized preview write, resolve the user's requested destination and the project's artifact, scratch and evidence locations, including OS temporary-directory restrictions; use permitted locations even when Git ignores them. Check the resolved filesystem location, not Git tracking or a clean status. If no destination convention exists, propose the location in the plan and include it in the authorization; memory-only analysis remains available without artifact writes. Read-only or no-write restrictions still apply.

Temporary experiments need corresponding task authorization. Necessary safe local checks, disposable evidence and previews may inherit an explicit implementation authorization only when the approved plan or bounded autonomy covers them and project-specific opt-in restrictions permit them. A general approval does not expand that scope. Avoid optional artifacts and preserve user data during cleanup.

Paid services, external publication, sensitive uploads, real-device control and other uncovered actions retain their separate permission boundaries. Preview permission authorizes an artifact, not a prohibited tool action. If browser/application launches are prohibited, do not bypass the restriction through a shell or another tool. Deliver the permitted preview or analysis and leave rendering explicitly unverified.

## Continue within scope

Design-only and planning-only requests end at the requested artifact or analysis. Explicitly naming a phase does not truncate an otherwise authorized implementation or delivery outcome. Keep unresolved choices and missing evidence explicit; a phase transition neither grants new authority nor revokes still-valid authorization.

## Project gates

The read-only default, detailed plan, explicit execution authorization and uncertainty stop apply to every project. DDD uses the unified `.planning` structure under [project adaptation](project-adaptation.md); necessary record initialization and lossless migration accompany authorized project writes without a separate adoption gate. A narrower user or project write boundary remains effective. Read-only tasks retain approval evidence in the conversation and report structure gaps without writing. Use the gates below to identify approval objects, not four mandatory meetings. A reply can approve several named objects; a stated requirement needs no second approval but does not itself authorize writes. Never treat a candidate file, test result or agent-written `approved` field as consent.

| Gate | Object shown to the user | What the approval permits | What it does not permit |
| --- | --- | --- | --- |
| G1 requirements | Scenario, intended outcome, scope, acceptance, constraints, exclusions and material unknowns | Prepare design and any separately permitted preview within the project | Production implementation, dependency installation or expanded features |
| G2 design | Design identity, applicable prototype identity and entry, important trade-offs and differences from the previous contract | Prepare an implementation slice and its verification approach read-only | Persisting the approved design, coding, real operations or publication without execution authorization |
| G3 implementation | One ready slice's outcome, approved design identity, affected responsibilities, permitted checks and recovery | Complete that slice, its ordinary in-scope fixes and authorized checks | Another slice, changed semantics or uncovered external actions |
| G4 acceptance | Implemented identity and scope, actual user path or algorithm result, technical verdict, unverified items and residual risk | Record acceptance and update accepted long-term facts within existing explicitly authorized persistence scope | Uncovered record writes, automatic installation, push, release or new development |

For each approval, retain the gate, object and scope, authentic user reply and recoverable location or snapshot. A Git commit identifies approved content only if the named files had no uncommitted differences at approval time. If content is uncommitted, keep its hash **and** a recoverable copy; a hash alone cannot reconstruct the baseline. G2 includes the relevant requirements, design, prototype and local resources; G3 also binds the current slice. Do not recursively hash the record that holds its own approval.

Maintain the latest effective approval, pause or withdrawal in the current record summary, with authentic sources and scope; keep earlier decisions as history. A reported defect inside an unchanged approved design and valid execution envelope is repaired under that authorization without a fresh per-file or styling gate. Feedback alone does not grant missing execution authority. Escalate only the material semantic delta and continue independent authorized actions.

Keep `technical_verdict` separate from `user_acceptance`. Checks may establish `PASS`, `FAIL`, `BLOCKED` or `NOT_CHECKED` for the technical verdict; acceptance requires a real user decision or an expressly agreed low-risk mechanical acceptance rule. If an approved object changes, compare the actual difference: an equivalent formatting or link correction can be recorded as such, while a semantic or scope change returns only the affected gate to the user. Continue unrelated authorized work.
