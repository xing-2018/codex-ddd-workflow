# Design document authority

Read before reviewing, planning or drafting design documents, including read-only work. Persistence still requires authorization. This reference defines a default, not a migration mandate.

The synchronized [Chinese review copy](design-documents_zh.md) is for human review, not additional execution guidance.

The unified `.planning` entry follows [project adaptation](../../ddd-flow/references/project-adaptation.md). Necessary workflow initialization or structural migration accompanies authorized project writes; it links existing long-lived requirements and designs, rather than relocating or duplicating their authority. This document's layout default does not turn workflow maintenance into a repository-wide documentation migration.

Approval of a design's content does not by itself authorize writing it. Apply [design approval](../../ddd-flow/references/design-approval.md) before changing requirements, design or acceptance owners, indexes or task records. Present the detailed plan in the conversation and retain existing authority until the user explicitly authorizes the proposed writes or bounded autonomy covers them. A candidate fact cannot replace approved current behavior merely because the change is documentation-only.

## Preserve repository authority

Read the nearest instructions and existing design index before choosing a path. Preserve a compatible established structure and approval mechanism. Do not create a parallel hierarchy or migrate documents unless the user explicitly requests that reorganization.

### Recover the writing contract

Recover the document's purpose, reader, requested coverage, established structure, prohibited content and required retained facts from applicable project guidance and the relevant conversation or existing record. Carry earlier corrections into each affected document and subsequent addition; new feedback changes only the affected clauses. Reuse these decisions and valid guidance without rereading unchanged references or adding a separate checklist or tracker. If the original decision is unavailable or conflicting, recover it before dependent work.

Before drafting or changing a prototype, identify the affected domain object, its owning module and the user's intended result from requirements, the glossary, existing assets and callers. Distinguish actions such as creating an instance and defining a new type. A form label or mockup cannot settle that meaning. Resolve disputed scope before dependent edits; keep current implementation, approved targets and proposed additions distinct during investigation and approval.

Follow an explicit complete-content or subset requirement. Do not silently substitute representative examples for requested complete content. If that boundary is unresolved and materially changes the result, clarify it before selecting content; state any proposed subset in the reviewable plan. This does not mandate including every supplied source in every document.

For Chinese drafting or revision, read [detail and information selection](../../chinese-docs/references/chinese-writing.md#详略与信息取舍) before writing, unless already validly loaded. Use that shared method directly; do not start the full document workflow or load it for unrelated worker tasks. Delivery still uses the single content review below.

### Developer-facing content

Stable design documents describe what developers must build: goals, user actions and expected behavior, rules, parameters, interfaces, constraints and acceptance. State the intended behavior and selected technical route directly, without labeling each passage as implemented or planned. Current-capability inventories, implementation-gap tables and rollout progress belong in existing task or review records unless the user explicitly requests an implementation assessment. Keep source extraction and collection narratives, authoring file paths and hashes, authoring timestamps, paragraph inventories, migration or approval history, work logs and check receipts in their existing task or evidence owner. Express a resulting requirement directly rather than narrating how the document was assembled. Retain a path or identifier when it defines a required product input, asset or interface; its mere presence is not a violation.

Preserve normative sources and versions, applicability, business citations, engineering conditions and unknown or unverified facts that affect implementation or interpretation. Evidence must remain traceable; authoring provenance does not have to appear in stable design prose. Repository-specific layouts and content conventions take precedence.

Match depth to the fact owner and requested reader. A module design explains responsibilities, contracts, key data/state, collaboration, results and failures; code-entry inventories, field-by-field persistence and transaction recipes belong only where they define a required contract. An engineering definition still needs enough composition, geometry, parameter meaning, units, connections, applicability and supported examples to understand or construct the object. Concision must not reduce it to a glossary or parameter list. Reuse suitable project diagrams and preserve the requested visual format and required figures when adding or compressing text.

Choose the organization from the module's actual problem and established project conventions: a processing chain, collaborating responsibilities, a state lifecycle, or another clearer form. These are choices, not a fixed template, required headings, component count or diagram quota. For nontrivial behavior, explain the relevant internal responsibilities, key technical methods, data transformations and reasons for consequential choices, enough to understand how the module can be implemented. A simple module may need only a short explanation. Simplicity limits unnecessary architecture and detail; it does not omit methods needed to understand the design.

An external collaboration diagram explains dependencies; a sequence of stage names explains order. Neither alone explains internal architecture or technical methods. Where a transformation matters, state its input representation, main processing method and usable output, using prose, tables or figures as appropriate. When a selected algorithm, library, protocol or runtime materially determines the route, name it and explain what operation it performs on the data and which artifact it produces. A list of technology names alone is insufficient; do not add stack detail that does not help explain implementation. Logical responsibilities need not become separate services or new components. Describe established methods and approved choices; identify unresolved methods explicitly rather than inferring them from stage names or inventing a complete route.

Use applicable project flows for demonstrations: distinguish dialogue input, contextual annotations and interface actions where the product makes that distinction; carry established inputs and choices through subsequent steps. Do not turn built-in defaults into extra user work or ask again for settled domain facts. Use code to assess feasibility, existing mechanisms and gaps during investigation; it is a reference for the design, not its authority or coverage limit. Approved design may precede implementation and must not be reduced merely because code is missing. Keep proposed behavior and unresolved design choices distinct from approved targets. Preserve genuine design boundaries, engineering conditions and unresolved feasibility risks; implementation backlog alone is not a design restriction, and target wording does not certify implemented capability.

Usage examples must fit the project's actual user role, vocabulary and information available at that point. Keep the user's goal, the system's domain interpretation and internal tool parameters distinct; do not put machine flags or unexpressed processing decisions into the user's opening line merely to complete the route. Recheck inherited examples against the recovered corrections rather than treating their existing wording as approved. A knowledgeable user may explicitly state engineering terms and decisions: preserve those choices without asking again. Surface only missing material intent, without inventing it. This is a content check, not a required three-column format or dialogue template.

### Default layout

When the repository has no design-document convention, use this default:

```text
docs/
├── design/
│   ├── README.md
│   ├── 架构.md
│   ├── 模块/
│   │   └── <模块名称>.md
│   └── 测试.md
└── adr/
    ├── README.md
    └── NNNN-<决策名称>.md
```

Create each document only when it has a fact to own. Initialize `README.md` when navigation, ownership or active-change metadata first needs persistence. Create `架构.md`, `测试.md` and `模块/` lazily when the first corresponding system-wide, test-wide or coarse-module fact is justified. Create `docs/adr/` through the [domain method](domain.md) only when the first authorized ADR is justified. Release instructions remain outside this structure.

## One owner per fact

| Fact | Owner |
| --- | --- |
| Navigation, document rules, ownership map and active-change status | `docs/design/README.md` |
| System context, boundaries, coarse modules, cross-module collaboration and system-wide constraints | `docs/design/架构.md` |
| One coarse module's responsibilities, contracts, state, internal flow and failure behavior | `docs/design/模块/<模块名称>.md` |
| Project-wide test layers, infrastructure, cross-module scenarios and quality gates | `docs/design/测试.md` |
| Rationale for a hard-to-reverse, non-obvious trade-off | `docs/adr/NNNN-<决策名称>.md` |

A change may update several owners when it changes distinct facts at different levels. Do not repeat the same fact across them; summarize only enough to link to its owner.

Do not create a design file named after a feature request, incident, bug, repair, session or implementation task. Put a module-internal protocol, state machine, subcomponent or complex flow in the owning module document as a section.

## Module granularity

A module document represents a coarse, durable responsibility boundary. Create one only when the unit:

- has a responsibility that can be explained independently;
- owns a meaningful contract, state or failure boundary;
- is more than a source directory, package, class, process, configuration area or internal component; and
- needs more detail than `架构.md` should carry.

Keep tightly coupled components in one module document. Use one Markdown file per module and no nested module directory by default. A small project may need no module documents.

## Selectable document sections

- `README.md`: scope, document map, fact ownership, active changes and maintenance rules.
- `架构.md`: system context, boundaries, overall structure, coarse modules, key collaboration, system-wide constraints and related ADRs.
- `模块/<模块名称>.md`: responsibilities and non-responsibilities, external contracts, dependencies, internal model, data and state, key flows, failure and recovery, operating constraints, observability, testing seams, source mapping and related ADRs.
- `测试.md`: test goals, layers, environments and data, cross-module scenarios, non-functional validation and quality gates.

Use these as selectable sections rather than mandatory empty headings. Keep durable observable requirements and invariants with their owning design fact. Apply the developer-facing content boundary above; request narrative, diagnosis history, implementation plans, task checklists and release procedure belong in existing task or delivery owners. Do not create a duplicate status tracker.

## Content review

Before delivery, review the affected paragraphs and scenarios against three questions: do the domain object and responsibilities match the agreed task; is the content sufficient at the requested design level without unrelated implementation detail; and are earlier corrections, engineering constraints and required figures retained? Perform this content review under existing authorization, without a separate checklist, tracker or approval gate. Correct covered deviations; report unresolved material choices. Links, counts, formatting and hashes establish only their own checks.

For usage examples, check who would say each line and whether the user's stated goal has been replaced by internal processing instructions. Apply the user-role and intent boundaries above to inherited examples as well as new ones.

For a module design, trace a representative path within its agreed scope through the actual text and diagrams as a developer reading without the chat. Can the reader explain the relevant internal responsibilities, how any consequential selected technology is used, each important step's input, processing method and output artifact, and the reasons for consequential choices? Expand passages that require guessing a key method or connection; explicitly retain unresolved design questions. Check that the body directs implementation toward the agreed target rather than treating current code coverage or rollout status as the specification. Judge whether the chosen organization makes this understandable, not whether it matches a template or has enough diagrams. This reading check does not replace explicitly required complete coverage or certify implemented capability.

## Active changes and approval

Use the repository's existing approval mechanism when present. Under the default structure, `docs/design/README.md` may carry only lightweight active-change metadata:

```markdown
## 在途变更

| 变更 | 设计事实 | 需求 | 设计 |
| --- | --- | --- | --- |
| <变更标识> | <权威文档及章节链接> | 草案/已批准 | 草案/已批准 |
```

This table is an index, not a second specification. Link to each affected fact owner and keep substantive requirements and design there or in approved upstream authority. Do not mark an entire architecture or module document as draft for one pending change. After implementation and review complete, remove the active row; Git history retains the transition and stable documents again describe the approved system.
