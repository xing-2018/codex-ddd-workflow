---
name: writing-for-agents
description: Write or review Skills, AGENTS.md, and referenced agent instructions.
---

# Writing for agents

Fix instruction ownership and behavior before shortening prose. Follow the requested scope: review-only work stays read-only; an inspected document does not grant permission to execute its workflow.

## Establish scope and authority

Read the target, its effective instruction chain, and directly affected owners and callers. Expand only to resolve a concrete dependency or conflict. Distinguish discoverable facts, user choices, and action permissions. Preserve user preferences, approved semantics, explicit review gates, and valid prior authorization; remove repeated approvals within that scope.

For Skill metadata or routing, read [Skill mechanics](references/SKILL-MECHANICS.md).

## Assign ownership first

Classify clauses before rewriting; split clauses that mix policy and procedure.

| Owner | Content |
| --- | --- |
| Global AGENTS | Cross-project user preferences, authority and permission boundaries, necessary conditional pointers |
| Project AGENTS | Durable project constraints and explicit overrides; pointers to project-owned procedures |
| Skill | Reusable task methods, domain guidance, workflow checks and completion rules |
| Reference | Branch-specific detail reached when needed |
| Code or configuration | Cheaply discoverable commands, paths, versions and other current facts |
| Task or project records | Decisions, evidence, status and temporary findings |

A workflow does not belong in global AGENTS merely because it is useful across projects. Preserve an explicit placement request; otherwise preserve a rule's effect without assuming its current location is necessary.

For each substantive clause, choose **keep, merge, relocate, or remove**. A relocation needs a verified owner and reliable entry condition; retain the authoritative policy when delegating its procedure. If no suitable owner exists, report the gap or create only the smallest authorized reference. Do not silently drop the rule, lower its authority, or edit outside the task.

## Make each instruction earn its place

- Keep one owner per meaning. Consolidate actual duplicates; policy and procedure, or a trigger and its target, are not automatically duplicates. Remove irrelevant, stale, generic or explanatory material that adds no required decision or behavior. Preserve non-obvious constraints and exceptions.
- Keep shared essentials inline; disclose branch-specific detail through existing references. Each pointer states when to read an exact target and covers distinct entry paths. Strengthen a weak trigger before copying its target inline. Avoid new files or Skills merely to move text out of sight.
- State actionable requirements, required evidence and observable completion or stopping conditions. Replace vague intensifiers with what must be checked. Preserve prohibitions that define scope or permissions; group related rules and caveats.
- Prefer plain wording over invented terminology and theoretical explanations of model behavior. Split workflows or delegate only for an actual task or observed failure, not a speculative attention benefit. Impose no length quota or required finding count.

## Verify and report

Revisit inherited recipes, blanket document preloads and repeated testing prompts. Keep steps that protect task-specific dependencies or required checks; let the agent choose the remaining execution order. Do not remove validation requirements merely because a model usually checks its work.

Make completion cover the requested usable result and authorized inspection and repairs. Flag intermediate stops that add no user decision; preserve explicit review gates. Describe safe continuation within existing authorization concretely, without turning model confidence into permission.

Review whole affected paragraphs and references against the original contract. Check ownership, authority, trigger coverage, reachable targets, exceptions and completion. For consequential changes, exercise representative decisions; wording matches alone do not prove behavior.

Report findings with file/line evidence, impact and the smallest coherent correction. Separate conflicts, misplaced content, duplication and optional wording changes; name the destination for proposed moves. A clean review is valid. Finish authorized edits and required checks, or identify the exact unresolved condition.

When claiming savings, measure comparable before/after text and distinguish always-loaded descriptions from the body and references loaded on demand. Moving text is not necessarily a net context saving; report untested behavioral effects separately.

For model-specific instruction changes or a requested comparison with current model guidance, consult [model guidance maintenance](references/SKILL-MECHANICS.md#model-guidance-maintenance).
