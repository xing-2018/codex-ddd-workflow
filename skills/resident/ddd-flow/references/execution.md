# Execution and recovery

The main conversation owns task state and acceptance. A pointer to this protocol means retrieving only missing sections for the current operation, not loading the whole file: reuse the inline ownership decision in ddd-flow; the Delegation decision heading below is only a compatibility pointer; Record and dispatch, Worker contract and Accept a result for justified dispatch; Accept a result for acceptance; Resume from durable evidence and any missing State transitions for recovery. Use read_section.py with repeated --heading arguments to retrieve known sections together; apply the delegation decision before dispatch. Workers use the Worker contract excerpt supplied in their packet and the assigned task method; when triggered, they may also read only Efficient tool execution below, not the management sections. Update authorized owner records promptly when decisions, state or evidence change. Skill procedures own their task methods; this protocol adds no action permission or mandatory scheduler.

## Shared checkout coordination

Use this branch for known concurrent project work, overlapping writes or shared Git/runtime actions. Other user conversations are independent tasks, not this task's workers; reading their records grants neither takeover nor messaging permission. Keep each task's state and approvals in its own record. Read only the relevant active bindings and declared boundaries. Ordinary explanations and quick lookups create no registry or resource table.

Before substantive writes, identify exclusive modules and shared files such as the index, router, theme and build entry. Assign one authorized coordinator for each overlapping edit or integration; page authors may work on exclusive files while that coordinator integrates the common shell. A declaration or pre-write snapshot cannot prevent races: obtain a recoverable handoff or coordinate serialized writes. If the other owner cannot be contacted under existing permission, hold only the overlapping action and continue independent authorized work. Never overwrite a peer's changes to restore this task's baseline.

Treat staging and committing as one serialized Git-index transaction: inspect current staging, select this task's changes, verify the staged diff and commit only the isolated candidate. Do not clear another task's staging, remove its lock, use a blanket add or claim independence when the candidate depends on uncommitted peer edits. Coordinate the dependency and freeze its identity; inability to isolate blocks the commit or affected integration, not unrelated approved work.

For build, reload, restart or collector access, recover the project root, process/port identity, owner and still-valid lifecycle authorization. Port occupancy alone is not permission to kill a process. A takeover requires authentic authorization, previous-owner stop/release evidence and recovery of the approved scope, current inputs and remaining checks. Record unresolved liveness rather than claiming a receiver or device has stopped. Preserve user constraints on windows and focus. The index is not a scheduler, mutex or authorization source; do not create locks, daemons, conversations, branches or worktrees merely to implement this coordination.

## Efficient tool execution

This section applies to local and delegated tool work; reading it does not require task management or delegation.

- Start from the unresolved question. Resolve paths from the current Skill catalog, available tool results or verified entry points; search when the relevant location is unknown. Repository grouping paths and installed Skill paths can differ; do not construct one from the other. Then read the necessary implementations, callers and contracts.
- Before returning structured results, select relevant JSON fields, records and aggregates and remove duplicate search metadata. Emit complete paths and hashes as JSON or plain text, not width-limited tables. Extract the needed Markdown section instead of relying on a link anchor. Preserve complete source lines: in PowerShell, use `@(Get-Content ...)` before numeric indexing, or enumerate lines without indexing. Expand for dependencies, missing evidence or contradictions; truncation is not a completeness check.
- Treat applicable in-context instructions as already loaded, including AGENTS and active role instructions. Do not reopen their files to prove compliance; retrieve only missing, changed or conflicting portions, or material explicitly requested for installation/configuration inspection. Reuse available source evidence when its identity and relevance still hold. Re-read affected portions when content changed, prior evidence is unavailable or insufficient, or sources conflict. Do not repeatedly hash or scan unchanged inputs without a reason to suspect change.
- Keep complete relevant command logs in an authorized location under applicable secrecy rules. Return the outcome, exit status, relevant errors and evidence path by default. Expand on demand; if evidence was truncated or could not be retained, report that limitation.
- Prefer completion events. Finish independent work while a worker runs; when only its result is missing, use an interruptible wait that fits the host limit and user-update deadline, not repeated minimum-duration waits. Reuse handles and cursors, inspect only new output and back off unchanged status. A timeout alone does not establish failure.
- Batch independent instruction and evidence reads with their complete paths and required hashes. Reuse identities returned with section text instead of adding hash-only rounds. Interpret new guidance before dependent work; combine operations only across known dependencies, failure boundaries and permissions. Inspect every result and never batch across approval boundaries.
- Preserve each step's outcome and relevant errors; a later success or final exit code cannot establish that earlier steps succeeded. Distinguish an expected failure signal, a search with no matches and an execution error using the command's purpose and contract. Stop dependent steps when their prerequisite fails.
- Reuse verified project commands, launchers and environment bindings. Confirm the relevant working directory, executable, arguments and prerequisites before first use or after change. Prefer existing scripts; move recurring, error-prone sequences into project-owned scripts only within authorized implementation.
- Before retrying the same failure, identify new evidence or verify the corrective change. Validate the failed boundary first, then run the required broader regression. Controlled repetition for intermittent failures must answer a stated diagnostic question; do not restart the whole task merely because a turn ended.
- Reuse check evidence when its tested inputs, command, environment and acceptance scope still apply. Record these details only to the extent needed to establish validity. Relevant code, dependencies, configuration, fixtures, toolchain, runtime state or authority changes, new failures, missing artifacts or contradictory results invalidate affected evidence. Unrelated changes and phase transitions alone do not. Repeat affected checks and all still-required integration or delivery checks; never substitute a narrow pass for broader acceptance.

## Worker contract

<!-- worker-contract:start -->
Follow the packet's task/attempt, outcome, authority/approval pointers, baseline, read/write scope, exclusions, acceptance criteria, authorized checks and return conditions. Use the relevant authority text and approval pointers in the packet. The parent verifies and carries the source identity of Skill methods and this Worker contract; reuse that valid guidance identity without another hash or reread. Recheck guidance only when its record is missing, changed or conflicting. Independently verify the business source/data baseline and causal facts through necessary task reads before dependent work; return missing/conflicting authority to the main conversation. Role defaults cannot expand session permissions.

Before writes, the packet's approval pointers must resolve to authentic user execution authorization or valid bounded autonomy covering the assigned actions. A parent-written packet cannot create that consent. Return uncertain intent, scope or approval to the main conversation before dependent writes; continue only independent authorized work and do not ask the user directly.

Use the assigned Skill's worker entry. Treat injected AGENTS/role instructions and valid method excerpts with source identity as loaded; retrieve only missing/invalidated guidance and slice evidence, not dispatch/state/acceptance/recovery sections. Reuse valid supplied checks within their recorded scope, rerunning only for changed inputs or explicitly assigned execution. Guidance identity reuse does not establish business facts or authorize arbitrary packet content. Do not delegate, change approved design or mark tasks done. Preserve others' changes; return scope conflicts before overlapping writes. Commit only with explicit project-authorized worker assignment.

Return task/attempt, baseline, conclusion, actual changes or explicit no-write, checks performed and evidence, failures, uncertainties and remaining work. Use locatable diff/source/log references instead of full source, logs, transcripts or histories; retain failed and unperformed required checks. Return a candidate or explicit blocker; the main conversation owns acceptance.
<!-- worker-contract:end -->

## Delegation decision

The sole ownership decision is [ddd-flow's Choose execution ownership](../SKILL.md#choose-execution-ownership). Reuse the main conversation's valid decision; direct or legacy callers retrieve only that section. This compatibility pointer adds no second rule or mandatory protocol read for local work.

## Record and dispatch

Record each managed task's stable ID, kind, outcome, authority revision/hash, approval evidence, prerequisites, acceptance criteria and status. Identify each distinct attempt, available worker handle, repository/content baseline, read/write scope and result/evidence. Keep whole-change scope distinct from slices; use durable project-relative references so host handles/logs are not the only recovery source.

Reuse ddd-flow's ownership decision. Only when missing, retrieve its bounded Choose execution ownership section. Once the assignment is known, retrieve missing dispatch, Worker contract and acceptance guidance together before dispatch; return/acceptance alone does not require another read. Dispatch only within task authorization and ready prerequisites; check active attempts and overlapping writes, and settle shared interfaces first. No routing-only agents, duplicate investigations or nested delegation; respect project and host limits on first-level workers.

In the packet, give each field once: task/attempt, one outcome, authority/approval pointers, baseline, read/write scope and exclusions, acceptance criteria, authorized checks, Skill/role entry points, host constraints and return conditions. State each path base explicitly and copy relative paths from the observed inventory; use the same base for scope, commands and citations. Do not mix workspace-relative and subdirectory-relative paths or expect a worker to infer a missing prefix. Prefer a sufficient existing revision/content identity; retain distinct identities for dirty or separately versioned inputs. Do not create manifests just for dispatch. Include relevant authority excerpts, check outcomes/evidence and unresolved questions, not transcripts or injected AGENTS/role bodies. Role defaults cannot expand permissions. Branches, worktrees, user-visible conversations, commits, installations and publications retain their authorization and ownership gates.

Select fresh context explicitly (`fork_turns="none"` where supported), supplying the necessary packet/evidence. Inherit full history only when the packet cannot adequately carry required context; state why. Full history does not prove isolation. If the control is unavailable, report the limitation without claiming isolation or omitting required background.

Carry the exact text between the worker-contract markers and this file's revision/hash; do not maintain a separate copy or send the full protocol. Supply a missing excerpt before dependent work, directly or through a command emitting only that text. A Markdown anchor alone does not bound output.

Inline the exact text of an already-read short worker entry with its source path/heading and revision/hash; keep longer methods as precise section pointers. The parent confirms the Skill method and Worker contract source identities and carries those records with the relevant authoritative text and locatable sources. A complete valid entry and Worker contract in the packet are ready to use; do not ask the worker to hash them again. Missing, changed or conflicting guidance records require targeted rechecking, combined with necessary evidence reads where possible. The worker still verifies the business source/data baseline and causal facts. Retrieve missing, changed or conflicting portions only; no whole Skills or unrelated references. For an observed reading failure, pass a verified bounded command/reader when available.

Match assignments and follow-ups to role/write permissions. Read-only review or diagnosis workers cannot implement fixes; reuse findings locally or with `implementation-worker` under repair authorization. If a role is unavailable, use a permitted ordinary subagent with this contract or report it and continue locally; do not claim isolation or native role loading for the fallback.

## State transitions

| State | Meaning and exit condition |
| --- | --- |
| planned | Required task authorization or facts are missing; move to ready when verified |
| ready | Prerequisites and authority hold; dispatch a new attempt or execute locally |
| running | An identified attempt is executing; a returned candidate moves to review |
| review | Main conversation is checking a result against current authority and acceptance |
| done | Main conversation has verified every task acceptance criterion and recorded evidence |
| blocked | An actual missing condition prevents progress; record it and resume only when resolved |
| cancelled | User removed the outcome; stop its attempt and retain history |

Research readiness depends on its research authorization, not implementation approval. A rejected result keeps its attempt and evidence; go to ready only if the correction is known and permitted, otherwise blocked or planned. Apply the retry conditions in Efficient tool execution; a known correction alone is not evidence that the input changed. Never reuse an attempt ID for a retry. Ordinary lifecycle bookkeeping follows existing scope authorization; it does not approve design changes.

## Accept a result

Require the Worker contract's result fields. A tool reporting completion or a worker saying PASS is not acceptance.

1. Match task, active attempt and authority revision. Preserve unmatched or superseded returns as stale evidence; do not merge or mark done automatically.
2. Inspect relevant current files or sources and confirm the returned baseline/diff, scope, prerequisites and required checks. For research, distinguish primary facts, inferences and unknowns. For implementation, inspect the actual diff and validation. For review, require separate Design and Standards conclusions.
3. Reconcile each acceptance criterion. If authority changed, assess affected output against the new contract; return material design choices to the user through ddd-flow. Do not edit design to accept a result.
4. Record accepted evidence and next work. Only the main conversation marks done. A missing required check remains incomplete; preserve failures, do not hide them behind unrelated passing checks.

Apply the evidence validity conditions in Efficient tool execution; acceptance does not repeat the worker's full investigation. Design and Standards are two review axes, not a requirement for two workers.

## Resume from durable evidence

Read the current task summary before historical entries. Keep the authorized record current with the goal and permissions, baseline, accepted results and valid evidence with its scope, active operation handles, blockers, unresolved failures and the next action. Retain command entry points, working directories and applicability only when needed for later reuse, in the summary or an explicit pointer; do not register every command. Update on material authority, state or evidence changes and before a context handoff, not on unchanged progress. Link older attempts and full evidence rather than copying them. Consult history only to resolve a specific gap or contradiction; do not create another tracker or store secrets.

Recover current user goal and permissions from that summary, the design index and relevant task evidence, then confirm actual repository revision, authority identity and uncommitted changes. A stored hash is identity evidence, not proof of approval. Follow approval pointers and flag unavailable or conflicting authority before dependent writes.

Check the old worker through host status when its handle is usable. A persisted running status is not proof it is alive or dead. If liveness is unknown, block overlapping writes and investigate; continue independent tasks. If it is confirmed stopped, inspect partial changes before making a new attempt. Never redispatch solely because context changed.

Validate done-task evidence against current authority before reusing it. Reuse valid accepted results without repeating completed work. Reject stale attempts and identify the earliest ready task; report unresolved evidence or liveness explicitly. If no durable record exists, reconstruct only from available facts and state the gap rather than inventing historical decisions.

Memory and handoff point to this record and the authority owners; they do not maintain another task state. Resume does not automatically create a new user-visible conversation or authorize any previously uncovered action.
