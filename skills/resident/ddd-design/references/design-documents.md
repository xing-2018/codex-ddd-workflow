# Design document authority

Read before reviewing, planning or drafting design documents, including read-only work. Persistence still requires authorization. This reference defines a default, not a migration mandate.

The synchronized [Chinese review copy](design-documents_zh.md) is for human review, not additional execution guidance.

The unified `.planning` entry follows [project adaptation](../../ddd-flow/references/project-adaptation.md). Necessary workflow initialization or structural migration accompanies authorized project writes; it links existing long-lived requirements and designs, rather than relocating or duplicating their authority. This document's layout default does not turn workflow maintenance into a repository-wide documentation migration.

Approval of a design's content does not by itself authorize writing it. Apply [design approval](../../ddd-flow/references/design-approval.md) before changing requirements, design or acceptance owners, indexes or task records. Present the detailed plan in the conversation and retain existing authority until the user explicitly authorizes the proposed writes or bounded autonomy covers them. A candidate fact cannot replace approved current behavior merely because the change is documentation-only.

## Preserve repository authority

Read the nearest instructions and existing design index before choosing a path. Preserve a compatible established structure and approval mechanism. Do not create a parallel hierarchy or migrate documents unless the user explicitly requests that reorganization.

### Recover the writing contract

Recover the document's purpose, reader, requested coverage, established structure, prohibited content and required retained facts from applicable project guidance and the relevant conversation or existing record. Carry earlier corrections into each affected document and subsequent addition; new feedback changes only the affected clauses. Reuse these decisions and valid guidance without rereading unchanged references or adding a separate checklist or tracker. If the original decision is unavailable or conflicting, recover it before dependent work.

Follow an explicit complete-content or subset requirement. Do not silently substitute representative examples for requested complete content. If that boundary is unresolved and materially changes the result, clarify it before selecting content; state any proposed subset in the reviewable plan. This does not mandate including every supplied source in every document.

### Developer-facing content

Stable design documents describe what developers must build: goals, user actions and expected behavior, rules, parameters, interfaces, constraints and acceptance. Keep source extraction and collection narratives, authoring file paths and hashes, authoring timestamps, paragraph inventories, migration or approval history, work logs and check receipts in their existing task or evidence owner. Express a resulting requirement directly rather than narrating how the document was assembled. Retain a path or identifier when it defines a required product input, asset or interface; its mere presence is not a violation.

Preserve normative sources and versions, applicability, business citations, engineering conditions and unknown or unverified facts that affect implementation or interpretation. Evidence must remain traceable; authoring provenance does not have to appear in stable design prose. Repository-specific layouts and content conventions take precedence.

Use applicable project flows for demonstrations: distinguish dialogue input, contextual annotations and interface actions where the product makes that distinction; carry established inputs and choices through subsequent steps. Do not turn built-in defaults into extra user work or ask again for settled domain facts. Code is evidence of current implementation and gaps; approved design may precede implementation and must not be reduced merely because code is missing. Keep proposed behavior and unresolved choices distinct from approved targets.

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

## Active changes and approval

Use the repository's existing approval mechanism when present. Under the default structure, `docs/design/README.md` may carry only lightweight active-change metadata:

```markdown
## 在途变更

| 变更 | 设计事实 | 需求 | 设计 |
| --- | --- | --- | --- |
| <变更标识> | <权威文档及章节链接> | 草案/已批准 | 草案/已批准 |
```

This table is an index, not a second specification. Link to each affected fact owner and keep substantive requirements and design there or in approved upstream authority. Do not mark an entire architecture or module document as draft for one pending change. After implementation and review complete, remove the active row; Git history retains the transition and stable documents again describe the approved system.
