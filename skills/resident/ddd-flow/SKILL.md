---
name: ddd-flow
description: Route project design, implementation, diagnosis, repair, recovery and substantive read-only codebase exploration; standalone code review uses ddd-review.
---

# DDD Flow

Own routing, progress, delegation, acceptance and recovery in the main conversation. First classify the requested action: ordinary explanation needs no DDD package; an independent document or diagram uses its specialist method; standalone code review uses `ddd-review`. For project design, implementation, diagnosis, repair or workflow recovery, select the applicable phase and permission mode; that Skill owns its method. Substantive read-only project exploration can reach execution ownership without inventing a defect or design phase. Do not create routing-only agents, preload phases or repeat completed work. Load auxiliaries only for unresolved questions. Linked phases remain readable without changing their implicit-invocation policy.

## 1. Recover authority

Use applicable AGENTS and relevant requirements, designs, CONTEXT and ADRs. Inspect code, callers, tests, configuration and data flow as evidence, not approval. Establish and reuse these task-local guards without requiring a new tracker:

- **Authority Baseline:** starting revision, authority-owning paths and identifiable approval evidence. Before persistent edits, record hashes and approved/uncertain provenance for staged, modified or untracked authority files.
- **Change Envelope:** requested behavior, interfaces, domain algorithms, data semantics, concurrency guarantees, constraints, acceptance and exclusions. File lists and execution order are forecasts unless explicitly locked.
- **Persistent Write Boundary:** before the first write, identify the detailed plan, authentic user execution authorization and covered targets/actions. Without explicit change authorization or bounded autonomy, investigate and propose read-only; uncertain intent, scope or approval returns to the user. Include authority documents, records, previews and temporary artifacts, not just product code. Optional support documents need both a task purpose and covered write permission. Never fabricate approval or certification records.

Identify the project and workspace. DDD project tasks use `.planning/PROJECT.md`, the `STATE.md` conversation index and the selected `changes/<change>/record.md`; ordinary explanations and quick lookups create no package. Select the requested change or this conversation's unique observed binding, never the newest pointer; compare relevant records with the verified current specification and reuse unchanged evidence. Reuse valid recovery-adapter pointers as declared facts, not authority. Use [recovery](references/recovery.md) for missing/stale facts and [project adaptation](references/project-adaptation.md) for structure, binding or migration gaps. First authorized writes cover necessary initialization and lossless migration within scope; read-only work only reports gaps. Existing owners retain requirements, design and approval; link them instead of duplicating content. Read [project Skills](references/project-skills.md) only for a concrete lifecycle question; initialization installs no Skills and changes no configuration.

## Design approval

Before changes, apply [design approval](references/design-approval.md) to recover the detailed plan and explicit execution authorization or valid bounded autonomy. A desired result or corrected requirement is not that authorization. Obtain approval before implementing an initial design or semantic delta, including edits to authoritative requirements, design or acceptance. Reuse identifiable approval across phases and turns; missing design files alone do not invalidate it. Code, tests and experiments cannot redefine approved behavior or acceptance.

Material decisions change outcomes, interfaces, domain/data semantics, security, dependency commitments, cost or hard-to-reverse constraints. Investigate facts; escalate unresolved material choices, not equivalent private implementation details.

Read [design approval](references/design-approval.md) when preparing a design/delta, resolving authority or persistence uncertainty, or preparing temporary evidence outside authorized implementation. Read it before a design-only UI preview. Pause only dependent actions.

Use recoverable conversation approval even when record writes are not permitted. G1 requirements, G2 design, G3 implementation and G4 user acceptance identify approval objects, not mandatory meetings. One reply may cover several named objects; design approval alone does not grant writes, and technical checks do not confer user acceptance. Read [project gates](references/design-approval.md#project-gates) only for the affected object.

## 2. Select one phase

- **Direct:** ordinary questions or explicitly authorized mechanical edits without unresolved behavior, interface, reference or migration consequences; exit DDD without bypassing the write boundary or detailed-plan requirement. A known-file or symbol lookup stays local. For substantive read-only project exploration, define the bounded evidence question and continue to execution ownership without inventing a defect or design phase.
- **Design, including UI:** unresolved requirements, material technical decisions, interaction, hierarchy or visible behavior; read [ddd-design](../ddd-design/SKILL.md) and only its relevant branch. Use requirements-only mode when requested. Use the same scenario across requirements, algorithms, data and UI; return contradictions to their owner.
- **Implementation:** approved authority and implementation authorization cover a coherent pass or ready slice; read [ddd-implement](../ddd-implement/SKILL.md).
- **Diagnosis:** a failure investigation without repair permission uses the `diagnose` mode of [ddd-implement](../ddd-implement/SKILL.md#select-authorization-mode); keep project files unchanged.
- **Repair:** a requested fix within the existing approved contract uses the `repair` mode of [ddd-implement](../ddd-implement/SKILL.md#select-authorization-mode); return a material contract change to design before dependent edits.

Determined nontrivial implementation is not Direct. Preserve approved facts outside the Change Envelope; route current-user deltas through approval rather than silently restoring old behavior.

After phase and permission selection, settle execution ownership below before substantially executing a bounded role candidate. An initial scan may establish scope; do not complete the candidate task merely to decide its owner.

## Choose execution ownership

After selecting the phase and permission mode, identify whether it contains one of these bounded worker tasks. A whole phase, an unresolved design decision, user interaction, integration or final acceptance is not a worker task.

| Selected work | Eligible bounded task | Role and method |
| --- | --- | --- |
| Design, or another phase blocked by an external engineering fact | One outside fact needed to settle the current decision without assigning that decision to the worker | `research-worker` using [ddd-design's research method](../ddd-design/references/research.md) |
| Project exploration, diagnosis or repair | One read-only call-chain, data-flow, boundary or causal-evidence question | `diagnosis-worker` using [ddd-implement's evidence worker entry](../ddd-implement/SKILL.md#delegated-evidence-worker-entry); exploration needs no reported defect |
| Implementation or authorized repair | One approved ready slice with settled interfaces and exclusive write scope | `implementation-worker` using [ddd-implement's worker entry](../ddd-implement/SKILL.md#delegated-implementation-worker-entry) |
| Post-implementation or standalone review | One frozen diff or explicit code-path snapshot for Design and Standards assessment | `review-worker` using [ddd-review](../ddd-review/SKILL.md) |

Default to local execution. Short deterministic checks, small reviews and known-file or symbol lookups need no protocol. For a bounded candidate beyond that path, decide before substantial execution whether its distinct result justifies preparation, dispatch, collection and verification. Role availability, a separable slice, substantial reading or fresh context alone is insufficient; do not build a fixed worker pipeline.

Delegate only for a specific independent assessment of frozen or competing evidence, bounded context isolation with locatable evidence, or useful parallel progress, when authority and host conditions permit. State the evidence or judgment sought and why local work is less suitable. For parallel work, also state what the main conversation will accomplish concurrently and what the worker returns; waiting and later review are not parallel progress. A worker opinion needs checkable authority and inputs. Honor explicit delegation requests within role, permission and independence limits.

Reuse this decision while scope, dependencies, user request and host conditions hold; phases do not reset it. Do not expand the task to manufacture a benefit or invent token prices or numeric thresholds. If delegation is justified, retrieve missing **Record and dispatch**, **Worker contract** and **Accept a result** sections of [execution](references/execution.md) together with repeated `--heading` arguments. Local execution does not load dispatch details or create another decision tracker.

## Conditional references

Reuse applicable guidance already loaded or resolved. After an explicit request to load the latest Skills or a known applicable update, retrieve the current task-relevant portions, including referenced policies, once before dependent work; rereading an entry alone does not refresh its references. Otherwise retrieve only missing, changed or conflicting portions. Reuse the refreshed guidance without per-turn version/hash scans; phase changes and context compaction alone do not require reopening whole Skills or project documents. Recover a lost binding from the active record and its relevant source, not a fresh document sweep. Resolve applicability before loading branch details.

| Condition | Reference |
| --- | --- |
| First project write or Git mutation | [Git](references/git.md) |
| Unresolved version or delivery obligations for a product change, repair, build or delivery check | [Versioning and delivery](references/versioning-and-delivery.md); reuse established project binding and decisions; an explicitly disposable fixture without product/artifact changes needs no delivery procedure |
| Background or authority missing from a referenced conversation | Extract **Conversation evidence** from [execution.md](references/execution.md#conversation-evidence) before requesting history; recover only the needed decisions and evidence |
| Test selection, creation, maintenance or review | [Testing and test maintenance](../ddd-implement/references/testing.md); does not activate TDD |
| Large tool results, long-running operations or repeated command failures | Extract only Efficient tool execution from [execution.md](references/execution.md) with [read_section.py](scripts/read_section.py) and `--heading "Efficient tool execution"` |
| Justified delegation, managed-result acceptance, changed managed dependencies/blockers or managed recovery | After the ownership decision above, retrieve only missing sections of [Execution and recovery](references/execution.md): **Record and dispatch**, **Worker contract**, **Accept a result** for dispatch; **Accept a result** for acceptance; **Resume from durable evidence** and needed **State transitions** for recovery |
| Known concurrent work or overlapping writes, Git index transactions or shared runtime actions | Read Shared checkout coordination in [execution](references/execution.md); do not infer permission to contact other conversations |
| Explicit planning, or scale, multiple sessions or actual blocking edges require a graph | [Planning](references/planning.md) |
| Project resumption, missing or stale active record, expensive fact recovery, or explicit portable handover | [Recovery](references/recovery.md); read only relevant facts and the active change when one exists |
| Writing record phase/status, including prototype-only work | Apply [State vocabulary and record checking](references/recovery.md#state-vocabulary), reusing identifiable checks for the actual inputs |
| An unresolved optional hook method, coverage or activation question | [Lifecycle adapters](references/lifecycle-hooks.md); unavailable hooks retain the manual path and activation needs separate authorization |
| Missing or outdated workflow structure, changed project binding or unresolved migration | [Project adaptation](references/project-adaptation.md); compare only relevant differences and reuse unchanged bindings |
| Matching, auditing or changing project-local managed Skills | [Project Skills](references/project-skills.md) and its fixed-source tooling; configuration changes retain their separate approval |

Resolve `<ddd-flow>` from the catalog or verified location and use `scripts/read_section.py <source> --heading <exact-title>`; repeat `--heading` for known sections. Direct phase/review callers may extract **Choose execution ownership** without traversing other phases. The helper validates all titles before returning deduplicated source lines and their path/SHA-256; reuse that identity in Worker contracts, leaving business verification with the worker. A title failure returns exact available headings without a body: choose from that output, never guess. Use `--list-headings` only when titles are still missing. Preserve failure status; failure is not loaded guidance. If unavailable, report the gap or use a bounded reader with the same section boundaries, never the whole reference.

Execution has one protocol for local and delegated managed results. The active `.planning` record links existing design, task and report owners and Git evidence; it does not duplicate them. Small work needs no graph or separate plan. Use [recovery](references/recovery.md#recover-facts-without-a-second-memory-store) for expensive facts or explicit portable handover; do not create a second state or default memory store.

## 3. Continue or stop

Before ending, compare the requested outcome with accepted results and perform each feasible authorized next action in the current turn. A progress promise, first implementation, phase boundary or worker return is not completion. Naming a phase does not narrow an authorized implementation or delivery outcome; design-only, planning-only and explicit stop requests retain their limits. Reuse settled approvals. When a real ambiguity, blocker or permission gate affects one action, finish independent authorized work and report the precise missing condition and dependent action. Apply global next-action reporting; do not manufacture an approval question or optional follow-up after completion.

## 4. Complete

`ddd-implement` invokes `ddd-review` on the frozen diff and completes checks justified by unresolved behavior, concrete regression risk or project requirements. Reuse valid results; phase transitions and commits do not trigger another validation round. Once original outcomes and required protection are established, stop probes, suites and extra restarts and continue remaining authorized delivery. Accept managed results through the execution protocol; a worker return is not acceptance. Apply versioning and Git completion rules without unsolicited builds or publication.

Use global reporting rules, identifying phases and meaningful skips, authority/approval evidence and repository actions. Complete only after the requested outcome, applicable approvals and required checks are satisfied.
