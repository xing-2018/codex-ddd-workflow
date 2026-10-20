# Content review and reading without chat context

Review substantial or formal documents once before delivery. Multiple formats share this content review; each format adds only its own layout or structural checks. The synchronized [Chinese review copy](review_zh.md) is for human review, not additional execution guidance.

## Whole-document review

Recover the complete applicable document contract from the relevant conversation and project owners: purpose, audience, coverage, structure, earlier corrections, prohibited content and facts that must remain. New feedback changes only affected clauses. Reuse established decisions and guidance; do not create another tracker or ask again for settled choices.

Compare actual paragraphs and scenarios with that contract before treating the content as ready. Check:

- The title, overview, body and conclusion answer the same question; purpose, audience, scope and exclusions agree.
- Required coverage is present. An explicitly complete result has not become an undisclosed sample; any approved subset remains within its stated boundary.
- Earlier corrections still hold in newly added or rewritten content. Prohibited content has not returned under different wording.
- Sections follow the reader's understanding and action, rather than the order in which the chat generated them.
- Key claims have evidence; inference, assumptions and unknowns are distinct. Terms, abbreviations, units, symbols, state names and interfaces are consistent.
- Apply [detail and information selection](chinese-writing.md#详略与信息取舍): identify passages removable without affecting the reader's task and critical relationships the reader must otherwise guess. Remove substantive redundancy and fill in-scope gaps from available facts; distinguish missing material from unnecessary detail. There are no contradictions, empty formulas of speech or unsupported additions.
- Concrete operation steps match applicable product behavior and approved design. Inputs, choices and references carry through later steps; a connected conversation has dependent follow-ups rather than unrelated single questions. Missing implementation does not remove approved design targets, and expected replies do not prove implemented capability.
- Peer sections do not mechanically repeat the same definition/list/praise pattern or rely on stock transitions and preview conclusions.
- Figures, formulas, code and citations have a clear function in the body. Markdown follows [portability rules](markdown.md).

For software design documents, use the already applicable [developer-facing content boundary](../../ddd-design/references/design-documents.md#developer-facing-content); retrieve it only if missing or invalid. Keep authoring and maintenance narratives in their existing task/evidence owner while preserving sources, applicability and unresolved facts needed for implementation. Judge each passage's role, not a blacklist of words such as “source” or “file”.

Correct content deviations within existing write authorization before delivery; review-only work reports them. Return unresolved semantic choices to their owner. Then finish applicable static and format checks. Links, formatting, counts and hashes establish those properties only; they cannot replace this comparison or certify content conformity.

Technical reports state concrete constraints and limitations rather than generic risk language.

Authorized drafting and local revision may fix identifiable repetition, awkward or translated phrasing and critical jumps without a full style rewrite. When the user requests naturalization or review finds systemic structural or stylistic problems, read [natural Chinese](natural-chinese.md) for the deeper method. Preserve facts, terminology, steps and genre; format-only work preserves content. Do not add a separate naturalization review pass.

## Source conversion review

Use this branch only when converting or restructuring source-backed material. Compare the final reading content with the source in complete clauses or other units that carry one coherent meaning, including cross-page continuations when needed. Use existing source locations and review evidence; do not re-extract or render everything by default. Preserve the approved structure and coverage. A representative unit can expose a method defect but does not verify the remaining content; approved sampling supports only its stated coverage.

- Keep formulas with the clause or table relationship required by the approved structure, including their numbers, variable definitions, units, conditions and cases. A collected formula appendix, a link to extraction evidence or a formula embedded in an image does not complete required editable body content. Preserve an expressly approved reference structure rather than imposing a new one.
- Check table headers, row/column associations, merged-cell meaning and footnotes against the source. Preserve every required flow branch and outcome, and keep a common explanation attached to all items it qualifies rather than only the last item.
- Check necessary illustrations and crop boundaries. Do not leave required editable text, formulas or ordinary tables only inside an illustration; retain the labels and context needed to interpret genuine graphical content.
- Preserve source identity, applicability and unresolved issues. Distinguish faithful transcription from interpretation or engineering applicability; do not silently repair uncertain source meaning or promote an unresolved item to confirmed.
- Read the promised final package in order. The reader must be able to follow the complete unit without fetching hidden extraction layers to recover missing content. File presence, identifier coverage and mathematical parsing do not prove correct placement, relationships or meaning.

Record coverage, concrete gaps and evidence in the existing review or task owner, without a new checklist platform. For managed batches, apply [result acceptance](../../ddd-flow/references/execution.md#accept-a-result) when a later defect contradicts earlier accepted content; retrieve only that missing method. Review-only work reports gaps, and repairs or rechecks remain within existing authorization.

## Reading without chat context

For important documents, read deliberately as someone who has only the file and cannot see the chat or hidden context. An independent reviewer may help but is not required.

Answer at least these questions:

1. What decision, understanding or action does this document support?
2. What is its central conclusion or proposal?
3. What premises, constraints and assumptions does it depend on?
4. Where is the evidence for its key claims?
5. What should the reader do next, if the document type calls for an action?
6. Which terms or missing steps would confuse a new or external reader?
7. Do three consecutive peer sections follow a mechanical pattern, or does each structure serve its own function?

Classify each answer as `direct`, `indirect` or `missing`. Fill an in-scope `missing` answer from available facts or identify the actual source gap; make an `indirect` answer explicit when it forces the reader to infer a critical connection. Also remove passages that add nothing to this reading task. Use concrete passages and reasons internally without printing per-paragraph labels or creating a scoring ledger.

## Visual inspection

Use this branch for requested DOCX/PDF layout inspection. Preserve the complete content contract and required structural checks. Default visual acceptance is risk-based sampling, not an assertion that every page is visually correct. Explicit user/project full-page acceptance remains full-page; pass the approved scope to specialist tools and Skills rather than silently adopting a broader default.

- For a local revision with unchanged layout and pagination, inspect affected pages and reuse valid evidence elsewhere. Compare content and pagination mappings before reuse; a changed page count does not prove which pages remain valid.
- For a new document or first conversion, inspect representative distinct layouts and relevant table, formula and pagination boundaries. Select by concrete layout risk, without a fixed page or image count.
- For font, template, page-width or other global changes, expand across affected layouts and pagination boundaries. Inspect all pages when influence cannot be bounded, defects are widespread or full coverage is explicitly required. Do not deliver known layout defects.

Separate successful construction, generated page images and pages actually viewed. Rendering all pages locally does not require sending all images to the model. Keep actual inspected page numbers and content identity in the existing summary/report; partial visual coverage remains partial even when it meets the approved sampled acceptance. Never mark a sampled document as all-page visually complete or let a structural pass stand in for fonts, clipping, page numbers or pagination. After correction, recheck only invalidated evidence when the unaffected mapping is supported. Missing required visual capability remains a stated gap, not a fabricated pass. Use existing task authorization; no per-image approvals or new checklist platform.

## Stop condition

Stop when the document fulfills the complete purpose and coverage, key claims remain traceable, earlier corrections hold, there are no material contradictions, redundancies or systemic mechanical phrasing, terminology agrees and a reader without chat context can understand the main conclusion. Do not add useless sections for completeness or decorative phrasing for naturalness.
