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
- There are no contradictions, redundant paragraphs, empty formulas of speech, unsupported additions or content irrelevant to the document's purpose.
- Concrete operation steps match applicable product behavior and approved design. Inputs, choices and references carry through later steps; a connected conversation has dependent follow-ups rather than unrelated single questions. Missing implementation does not remove approved design targets, and expected replies do not prove implemented capability.
- Peer sections do not mechanically repeat the same definition/list/praise pattern or rely on stock transitions and preview conclusions.
- Figures, formulas, code and citations have a clear function in the body. Markdown follows [portability rules](markdown.md).

For software design documents, use the already applicable [developer-facing content boundary](../../ddd-design/references/design-documents.md#developer-facing-content); retrieve it only if missing or invalid. Keep authoring and maintenance narratives in their existing task/evidence owner while preserving sources, applicability and unresolved facts needed for implementation. Judge each passage's role, not a blacklist of words such as “source” or “file”.

Correct content deviations within existing write authorization before delivery; review-only work reports them. Return unresolved semantic choices to their owner. Then finish applicable static and format checks. Links, formatting, counts and hashes establish those properties only; they cannot replace this comparison or certify content conformity.

Technical reports state concrete constraints and limitations rather than generic risk language.

When the user requests naturalization or review finds systemic mechanical prose, read [natural Chinese](natural-chinese.md) and review the document, paragraph, sentence and surface levels. Preserve facts, terminology, steps and genre. Do not rewrite style without a systemic issue.

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

Classify each answer as `direct`, `indirect` or `missing`. Fill an in-scope `missing` answer; make an `indirect` answer explicit when it forces the reader to infer a critical connection.

## Stop condition

Stop when the document fulfills the complete purpose and coverage, key claims remain traceable, earlier corrections hold, there are no material contradictions, redundancies or systemic mechanical phrasing, terminology agrees and a reader without chat context can understand the main conclusion. Do not add useless sections for completeness or decorative phrasing for naturalness.
