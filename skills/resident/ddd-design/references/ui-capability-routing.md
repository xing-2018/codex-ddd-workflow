# Capability routing

Route by the unresolved design question and required evidence, not tool availability alone. Use a named specialist only when it is available and its own trigger and authorization rules are satisfied. Without an explicit specialist request, produce the minimum evidence directly when suitable. If the user names a capability and it is unavailable or blocked, report the gap and affected claim; do not silently substitute another method or claim the requested workflow passed. Resolve a contract-changing fallback with the user while continuing independent authorized work.

The synchronized [Chinese review copy](ui-capability-routing_zh.md) is for human review, not additional execution guidance.

Routing does not authorize installing, updating, vendoring, patching or configuring a specialist.

| Need | Preferred capability when available | Boundary |
| --- | --- | --- |
| One external fact can change the design | [Research method](research.md), including Exa when selected | Hand off sources, applicability and the specific decision; do not broaden into general discovery. |
| The current flow needs systematic UX, visual or accessibility critique | Product Design audit | Use screenshot-backed findings; for a local approved correction preserve the existing visual baseline. The audit does not approve a design. |
| The user requests alternatives or a genuine visual trade-off remains | Product Design ideation or image generation | Explore only the disputed direction under the provider's current brief/selection rules; obtain the required selection before build work. |
| An interaction or state transition must run to answer the question | [Experiments method](experiments.md) | Test bounded behavior while keeping approved visual direction fixed. |
| A selected visual target needs an operable frontend prototype | Available frontend prototyping capability, including image-to-code when its trigger fits | Bind the exact selected source and use [Product Design handoff](product-design-handoff.md) when that provider is chosen. Deliver the independent HTML artifact under the preview contract; authoring or development preview alone is insufficient. Preserve in-memory state and predefined outcomes, without business I/O or computation. |
| A local web or Electron UI needs functional, responsive or visual verification | `playwright-interactive` | Respect its control authorization; QA evidence does not create design authority. |
| The user explicitly selects an external design environment | Available design capability | Respect provider and authorization rules; return rendered evidence here. |
| No specialist materially improves the result | Direct work in `ddd-design` | Build and verify the minimum faithful preview. |

Judge a capability by the artifact and actions it will produce, not whether its name contains code. UI design may build a safe, reversible frontend prototype within the existing preview authorization. Return requests for business implementation, real file/service/persistence integration or computation to `ddd-flow` as separate work; authorization for them does not put them inside the UI prototype. External publication and deployment retain their corresponding authorization requirements. Honor each capability's actual trigger, required visual source and tool restrictions; do not force a plugin dependency or a fixed set of alternatives into direct UI design. Do not run several specialists for reassurance.

`ddd-design` owns the complete experience prototype. Use the experiments method only for a bounded uncertainty that needs an experiment; not every clickable screen needs a separate logic experiment. A capability's output remains evidence and cannot approve a domain or UI design change.

For a selected Product Design path, read [its handoff adapter](product-design-handoff.md) before dependent writes or verification. It binds the actual host, authority, paths, QA and export evidence without replacing the provider's current workflow. No visual target means follow the provider's selection method, not invent a build target; a selected local correction does not restart whole-product ideation.

For each routed question retain only the exact question, evidence, answer and limitations, and the design decision it changes or confirms.
