# Mermaid diagram method

Read for a standalone Mermaid request or when a document or DDD design genuinely needs a diagram. An independent diagram uses the `diagram-only` route in [Chinese Docs](../SKILL.md); DDD design may read this reference directly without loading the document workflow. Preserve the user's requested language, terminology, type and destination conventions. A diagram describes documented facts or clearly marked proposals; it does not own approval state.

## Establish the question and destination

Identify the audience, the one relationship or behavior the figure should explain, the authoritative input, and whether editable source, rendered asset or insertion is requested. A business, educational or research diagram does not require a software repository. Distinguish facts, assumptions and examples; do not invent actors, transitions, cardinality, dates or outcomes to fill a layout. Resolve missing dimensions by a stated reasonable assumption unless they materially change meaning.

Choose the smallest useful representation:

| Question | Mermaid type |
| --- | --- |
| Process and branching | `flowchart`; label decisions and distinguish control, data and dependency edges |
| Exchanges across people or components | `sequenceDiagram`; preserve causal order and alternatives |
| Events and allowed states | `stateDiagram-v2`; states are not action steps |
| Persisted entities and known cardinalities | `erDiagram` |
| Classes, interfaces and inheritance | `classDiagram` |
| Dated tasks and dependencies | `gantt`; do not infer dates |
| Chronology without duration | `timeline` |
| Topic hierarchy | `mindmap`; use a flowchart for executable order |

Use a table or plot for quantitative comparisons when better, but do not silently replace an explicit Mermaid request. A simple linear explanation may need no diagram. For less familiar syntax, loops, grouping or responsibility boundaries, read [patterns](mermaid-patterns.md).

## Compose and verify

Choose direction for the actual medium: wide slide or short chain may suit `LR`; narrow column or branching flow may suit `TB`. Inspect rendered bounds rather than treating either as a universal default. Use concise labels, stable ASCII IDs with quoted display text, explicit branch conditions and identifiable exits. Groups represent actual boundaries. Keep prose near the diagram for relationships the user must approve; Mermaid code alone is not an approval explanation.

For slide/report styling, accessibility or image export, read [presentation and export](mermaid-export.md). Retain editable Mermaid source. Do not install or upgrade project dependencies merely to render. When a permitted renderer exists, use the destination configuration and inspect clipping, glyphs, overlaps, arrows and final-size readability; parsing is not visual acceptance. If rendering is unavailable or forbidden, deliver the authorized source and report the unverified stage within the requested output format. Source-only requests do not require image export or a whole document workflow.

For source-only delivery, check the source against the supplied facts and syntax. Distinguish that inspection from an executed parser or rendered visual check. If a validation receipt is requested and source comments are permitted, a brief Mermaid `%%` comment can report actual checks and the unverified render stage. Honor a strict code-only request that excludes commentary; do not add a receipt solely to satisfy an unstated evaluation expectation or imply that rendering occurred.

When inserted into a document or slide, the owning container workflow verifies the final placement and format. A status node in a diagram does not update a task record or imply user acceptance.
