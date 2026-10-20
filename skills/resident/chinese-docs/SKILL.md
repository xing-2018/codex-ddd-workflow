---
name: chinese-docs
description: "Create, revise, review, and deliver substantial Chinese documents, repository READMEs, or standalone Mermaid diagrams."
---

# Chinese Docs

Own substantial document structure, evidence, Chinese prose and delivery, plus a standalone diagram route. Ordinary answers, tiny edits and simple summaries do not need this Skill. Software requirements and design decisions remain with `ddd-flow`; improve expression without changing behavior, domain/data semantics, scope or approval status.

Default to Markdown document delivery, in the conversation unless file persistence is authorized. Generate DOCX, PDF or multiple formats only when the user explicitly requests those formats; a formal report or an available template is not that request. For content changes, keep one reviewed Markdown source and derive only requested representations. Format-only work preserves content and loads only its requested delivery contract. Software, prototypes and necessary assets retain their own approved contracts.

## Route

For a request to draw, revise or troubleshoot one independent Mermaid diagram, read [Mermaid](references/mermaid.md) and only its applicable syntax or export reference. Complete that request under the diagram method; the document guidance below does not apply. DDD design may read the diagram method directly without starting a document task.

For a document task, identify operation (`create`, `revise`, `review`, `format-only`), document type, evidence basis and requested formats. Use [routing](references/routing.md) when type or template is unclear. Read only applicable branches:

| Condition | Required reference |
| --- | --- |
| Chinese prose drafting/revision | [Chinese writing](references/chinese-writing.md), including [detail and information selection](references/chinese-writing.md#详略与信息取舍) |
| Explicit naturalization/“去AI味”, or systemic translation-like/formulaic prose | [Natural Chinese](references/natural-chinese.md) |
| Source-backed content or repository/external claims | [Evidence](references/evidence.md) |
| Repository README, before repository inspection | [README](references/readme.md) |
| Markdown content or delivery | [Markdown](references/markdown.md) |
| Explicitly requested DOCX, including format-only | [Delivery and template selection](references/routing.md#交付路由) |
| Explicitly requested PDF, including format-only | [Delivery and template selection](references/routing.md#交付路由) |
| Substantial/formal content review and reader test | [Review](references/review.md) |

Selecting one format does not load, generate or verify others. Use evidence → draft/revise → one content review → requested delivery; expand only for an actual defect or format-specific requirement. Preserve README language conventions and the naturalization route's facts, genre, terminology and genuine enumerations.

## Work proportionately

- Small bounded revisions: read the target and evidence, edit surgically and perform a compact review.
- Routine documents: establish context/evidence, draft or revise, review and deliver.
- Substantial/formal documents: recover a compact contract (purpose, audience, scope, sources, structure, formats, acceptance), including earlier applicable corrections, prohibited content and facts that must remain. New feedback changes only affected clauses; do not silently narrow coverage or discard other settled choices. Use existing conversation/project owners, not a new tracker. Draft, review and perform the reader test. Settled user/project choices need no repeated approval.
- Format-only: preserve content and perform applicable structural/visual QA.

Use the closest existing template when useful; do not manufacture sections or unsupported facts. Preserve strong content and user-supplied terminology, framing and supported detail. Separate facts, inference, assumptions and unknowns; verify changing external claims through primary sources within authorization. Never invent data, citations, author/reviewer metadata or completion status. Mark only genuinely unresolved facts `[待补充]`.

Write the main body before the abstract for substantial reports. Use the writing references for terminology, prose and naturalization; do not imitate an author or introduce colloquial style unless appropriately requested. Before delivery, use [content review](references/review.md) to compare actual paragraphs and scenarios with the complete contract, then complete applicable static/format checks; their success does not establish semantic conformity. Repeat content review after format conversion only if it reveals a content defect.

## Deliver and complete

Before authorized generation or rendering, separate final deliverables and required assets from temporary builds, page checks and logs. Resolve the project's designated temporary location; otherwise default to a task-scoped directory inside the authorized project boundary. OS temporary or other project-external locations require explicit target/action authorization. Git tracking does not define that boundary. Inspect tool defaults and sidecars, build in the permitted temporary workspace and copy only accepted deliverables and necessary assets to the final destination. Keep needed evidence through inspection and recording.

Markdown follows relevant portability and local-link checks, without DOCX/PDF conversion or rendering. An explicitly requested DOCX needs its type/template contract, structural audit and [visual inspection](references/review.md#visual-inspection); the bundled report inherits base formatting from DOTX and applies only the personal overrides in `word.md`. Format-only work also needs content preservation evidence; structural success alone does not certify visual layout or page numbers. Requested PDF needs rendering and inspection under the same approved visual scope. Default to risk-based visual sampling; preserve explicit full-page contracts and disclose partial coverage. Pass that scope to specialist methods instead of inheriting an unconditional all-page default. Finalize shared content once before requested multiple formats, then perform only their applicable format checks. Reuse valid evidence and recheck changed portions; conversion success alone is insufficient.

Before completion, inspect the actual source and delivery directories for artifacts from this task, including Git-ignored files. A clean Git status or an ignore rule does not establish correct placement. Correct misplaced task-owned outputs within authorization; preserve pre-existing evidence and report any unresolved cleanup. Keep document-linked images as deliverable assets, not disposable checks.

Complete when the requested scope is covered, the document is accurate for its evidence, coherent and consistent, facts and critical relationships are clear without chat context, no substantive redundancy remains, and each requested format has received its required checks. Report actual results, sources and limitations needed to use the delivery, including promised deliverables, unresolved facts and validation gaps that affect it. Do not enumerate unrequested formats, nonexistent derivatives or absent pending decisions. When only revised prose is requested, deliver it directly; explain the review process only when requested. Review-only work returns findings and correction directions without unauthorized edits.
