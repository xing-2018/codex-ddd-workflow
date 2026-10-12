# ADR Format

ADRs live in `docs/adr/`. Preserve an existing repository naming convention; otherwise use sequential numbering and a descriptive decision name: `0001-<决策名称>.md`, `0002-<决策名称>.md`, and so on.

Create the `docs/adr/` directory lazily: only when the first ADR is needed. Create a thin `docs/adr/README.md` at the same time. The ADR remains the authority for its status, context, decision, and rationale; the index contains only each ADR's number, linked title, and mirrored current status.

```md
# 架构决策记录

| 编号 | 决策 | 状态 |
| --- | --- | --- |
| NNNN | [<决策名称>](NNNN-<决策名称>.md) | 拟议/已接受/已废弃/已替代 |
```

## Template

```md
# {Short title of the decision}

**Status:** Proposed

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. A short ADR can consist only of a title, a status, and one paragraph. Change the status to `Accepted` or `Deprecated` when appropriate; use `Superseded by [ADR NNNN](NNNN-<decision-name>.md)` when a replacement exists. The value is in recording *that* a decision was made and *why*, not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Considered Options**: only when the rejected alternatives are worth remembering
- **Consequences**: only when non-obvious downstream effects need to be called out

## Numbering

Scan `docs/adr/` for the highest existing number and increment by one.

Keep each ADR's status and its `README.md` row synchronized. When a decision is superseded, create a new ADR, change the old ADR status to link to the replacement, and mirror that status in the index; do not rewrite the old rationale. Update the design documents affected by the new decision and cross-link the ADR and those fact owners without copying their content.

For ADR admission and persistence authorization, follow [the domain method](domain.md).
