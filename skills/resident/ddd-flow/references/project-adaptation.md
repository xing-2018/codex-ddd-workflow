# Project adaptation

Read for missing or outdated `.planning` structure, changed project bindings or a migration uncertainty. DDD project tasks use this unified specification; ordinary explanation and quick lookups do not create records. Inspect only the named project. A read-only survey reports gaps without initializing files, installing dependencies or running the product.

## Unified workflow and migration

The current workflow schema is **2**, with schema 1 still supported for legacy single-change lookup. Its authority is this reference, the verified current Skill source and its templates, not a remotely fetched latest branch. `.planning/PROJECT.md` declares `workflow_schema: 2` and a recoverable `workflow_source` identity. A source version change alone does not require rewriting every record; compare only changed requirements and affected structure.

For the first authorized project write, initialize `.planning/PROJECT.md`, `STATE.md` and `changes/<change>/record.md` as necessary. This record maintenance belongs to the same approved task scope, unless user or project rules exclude it; no separate adoption approval is required. Create `brief.md` or `design.md` only for facts or approval objects the task needs, using a concise pointer when an existing document owns them. Use `plan.md` only for real multiple-slice dependencies, and `skills.lock.json` only for explicitly selected project Skills. Templates and placeholders are not evidence or consent.

On entry or recovery, read the project schema/source identity, the relevant conversation binding in STATE and that record's current summary. When absent or outdated, compare the current installed specification with existing owners and facts. Within authorized record writes, automatically repair deterministic field names, supported status values, paths, pointers and missing structure. Preserve the original approval replies, recoverable content identities, pending decisions, user data and unrelated modifications; keep historical documents intact and link them from the active record. Use Git or an authorized project-local recovery copy before replacing existing content; do not delete the old owner as part of migration.

Do not infer approval, reinterpret a product requirement, reset acceptance or choose between contradictory facts merely to satisfy the new schema. Unknown provenance, ambiguous state mappings, conflicting authority, an unsupported newer schema or an excluded write boundary stops only the dependent migration and returns a concrete difference to the user. Complete independent authorized work. A read-only task uses the same structure for lookup but only reports missing or outdated records.

After a structural migration, inspect the actual changed records and affected local links, then use [workflow_check.py](../scripts/workflow_check.py) for the applicable active change. It is a read-only structural checker, not a migration writer or proof of user approval. Report the before/after schema, affected paths, preservation evidence and remaining gaps in the active record; update the source identity only after comparison. Do not repeat onboarding or bulk-scan other projects.

## Conversation index

Schema 2 keeps an index, not a project-wide current-task selector. Each entry uses two consecutive fields:

```markdown
- active_record: .planning/changes/example/record.md
  owner_thread: observed-conversation-id
```

Use a recoverable observed conversation ID; use `unresolved` for an inherited record whose owner cannot be established. Each project-relative record occurs once. The record owns phase, status, approval and evidence; do not copy them into STATE. An explicitly requested change selects its record; otherwise select the unique entry bound to this conversation. Multiple matches or unknown ownership requires resolving that selection, not choosing the latest timestamp. A read-only lookup never edits the binding. Transfer ownership only from authentic authorization and evidence that the previous owner stopped the relevant work; an index declaration is not that evidence.

Within approved record writes, migrate schema 1 by preserving its original pointer and all historical content, adding its verified owner or `unresolved`, then adding this task's own entry. Preserve the prior entry even when another task starts; do not infer that it was accepted or closed. Known field normalization and index updates must retain unrelated entries. Re-read immediately before a coordinated update, merge current entries and verify the result. The index supplies no mutual exclusion; use [shared checkout coordination](execution.md#shared-checkout-coordination) for actual overlapping writes. Do not bulk-migrate other projects or historical packages.

Run `workflow_check.py --project <root> --change .planning/changes/<change-id>` for schema 1 or 2. `--project` is the project root; `--change` is the directory containing `record.md`, relative to that root or an absolute directory inside it. Do not pass `record.md` itself. For schema 2, add `--thread <observed-id>` when asserting conversation ownership. It checks membership, safe local paths, duplicate record bindings and the supplied owner; an unresolved owner blocks that ownership claim, not independent work in another known record. Schema 1 remains valid without `--thread`; requesting an ownership claim on schema 1 reports a review gap. Unsupported schema, structural success and declared ownership do not prove authorization, resource release or design quality.

## Establish facts and authority

Identify effective AGENTS rules, approved write scope, repository root and subworkspace. Inspect the working tree, README entry, dependency declarations and locks, deployment files, relevant source entry and existing project decisions. Stop at enough evidence to answer what the project does, how it starts, how this task can be checked, what is risky and which material choice remains open. Do not treat an unread file as evidence of absence.

Record each important statement as **observed**, **approved**, **verified** or **candidate**, with a source pointer and applicable version. A dependency declaration is an allowed range, a lock is a resolved snapshot, the actual environment is an observed installation, and the design target is a proposed or approved choice. State differences instead of collapsing these four identities. Prefer static metadata for read-only version checks; importing modules or invoking package scripts can have side effects.

For an existing project, retain its approved stack unless the task includes a migration decision. For a new project, derive one recommended stack from product shape, deployment, offline and local-file needs, scale, concurrency, precision, maintenance, distribution, security and license constraints. Compare an alternative only for a real trade-off. State added runtime and operational burden, the risk needing independent evidence, and the exact decision for approval. A technology Skill is guidance for a matching stack, not a reason to select that stack.

Use [project.md](../assets/project.md), [state.md](../assets/state.md) and [record.md](../assets/record.md) for necessary authorized records. Keep source pointers rather than duplicating locks or architecture. Record the maintenance scope, any excluded record writes, allowed checks and whether project Skills are authorized. Project AGENTS changes and Skill installation retain their separate permissions. Reuse unchanged bindings on recovery.

## Risk-shaped scope

For a script or algorithm, emphasize units, boundaries and an independent reference value. For an API, cover interfaces, authentication, persistence and compatibility. For desktop or native tools, cover startup, file permissions, window and process behavior. For simulation or real devices, include reference cases, resource and failure isolation, and separate authorization for real operations. An AI feature needs output structure and tool authority; ordinary AI-assisted development does not imply an agent runtime. Do not invent numeric targets absent requirements or measurements.

When project-specific technical guidance may help, read [project Skills](project-skills.md). A missing compatible Skill does not block ordinary development with project methods or version-matched primary documentation.
