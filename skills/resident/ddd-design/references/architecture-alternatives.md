# Design It Twice

When the user wants to explore alternative interfaces for a chosen deepening candidate, compare radically different interface designs before committing to the first plausible one. Based on Ousterhout's "Design It Twice" principle.

Uses the vocabulary in [architecture.md](architecture.md): **module**, **interface**, **seam**, **adapter**, **leverage**.

## Process

### 1. Frame the problem space

Write a concise explanation of:

- constraints every interface must satisfy;
- dependencies and their categories from [deepening](architecture-deepening.md);
- a small illustrative sketch that grounds the constraints without becoming a proposal.

### 2. Produce genuinely different designs

Default to the current agent. Produce at least 2, usually 3, materially different interfaces, each under a different design constraint, for example:

- minimize the interface and maximize leverage per entry point;
- maximize flexibility only where current requirements need it;
- optimize the common caller so the default case is trivial;
- use ports and adapters when a real cross-seam dependency requires them.

Use parallel first-level subagents only when the global agent policy permits it and independent context materially improves a high-impact decision. Do not dispatch agents merely because this reference describes multiple alternatives.

For each design capture:

1. interface: types, methods, params, invariants, ordering, and error modes;
2. usage example;
3. complexity hidden behind the seam;
4. dependency strategy and adapters;
5. trade-offs in depth, leverage, locality, and seam placement.

### 3. Compare and recommend

Present the alternatives, contrast them on depth, locality, and seam placement, then give a recommendation. A hybrid is valid when it is simpler and better aligned with the approved requirements than every individual option.
