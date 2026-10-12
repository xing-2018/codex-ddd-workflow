# Requirements and bounded stress testing

Read when a new or changed need is unclear, when a requirements-only result is requested, or when the user explicitly asks to stress-test a plan. Recover approved product facts and inspect the actual product before asking. Code and tests are evidence of current behavior, not proof that the user accepted it.

Describe the user or caller, task entry and end, input meaning and units, required output, important state and failure behavior, constraints, preserved behavior, scope exclusions and observable acceptance. Give each material need an ID only when it helps trace design and verification. The active change's authorized `brief.md` owns new requirements or links their existing owner and content identity. The design references requirements rather than copying them; unified record migration does not rewrite approved facts.

Separate a fact to discover from a choice the user must make. Use the same concrete scenario for the desired action, cancellation or failure, and later technical and UI design. Investigate repository facts first. Present the smallest unresolved material choice with a recommended option when evidence supports one; do not conduct a fixed interview for ordinary clarification.

When the user explicitly asks for an interview or stress test, map the decision and its dependent choices. Ask a manageable set of currently answerable consequential questions in rounds; later dependent questions wait for their prerequisites. Provide a reasoned recommendation for each choice and stop when critical assumptions and risks have been tested. An interview does not itself authorize implementation.

Requirements-only work stops with a reviewable what-and-why contract and explicit unknowns. A new or changed requirement needs G1 approval under the applicable workflow; a prior approval remains valid for unaffected clauses.
