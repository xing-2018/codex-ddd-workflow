# Design document authority

Read this reference only when design persistence is authorized. It defines a default, not a migration mandate.

The unified `.planning` entry follows [project adaptation](../../ddd-flow/references/project-adaptation.md). Necessary workflow initialization or structural migration accompanies authorized project writes; it links existing long-lived requirements and designs, rather than relocating or duplicating their authority. This document's layout default does not turn workflow maintenance into a repository-wide documentation migration.

Approval of a design's content does not by itself authorize writing it. Apply [design approval](../../ddd-flow/references/design-approval.md) before changing requirements, design or acceptance owners, indexes or task records. Present the detailed plan in the conversation and retain existing authority until the user explicitly authorizes the proposed writes or bounded autonomy covers them. A candidate fact cannot replace approved current behavior merely because the change is documentation-only.

## Preserve repository authority

Read the nearest instructions and existing design index before choosing a path. Preserve a compatible established structure and approval mechanism. Do not create a parallel hierarchy or migrate documents unless the user explicitly requests that reorganization.

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

Use these as selectable sections rather than mandatory empty headings. Keep durable observable requirements and invariants with their owning design fact. Keep request narrative, diagnosis history, implementation plans, task checklists and release procedure out of stable design documents. Do not create a duplicate status tracker.

## Active changes and approval

Use the repository's existing approval mechanism when present. Under the default structure, `docs/design/README.md` may carry only lightweight active-change metadata:

```markdown
## 在途变更

| 变更 | 设计事实 | 需求 | 设计 |
| --- | --- | --- | --- |
| <变更标识> | <权威文档及章节链接> | 草案/已批准 | 草案/已批准 |
```

This table is an index, not a second specification. Link to each affected fact owner and keep substantive requirements and design there or in approved upstream authority. Do not mark an entire architecture or module document as draft for one pending change. After implementation and review complete, remove the active row; Git history retains the transition and stable documents again describe the approved system.
