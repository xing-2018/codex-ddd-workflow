# Domain language and durable decisions

Read when a term is ambiguous or conflicts with the current glossary, or when a hard-to-reverse domain choice may need an ADR. Merely reading a glossary for vocabulary does not require this method.

Resolve a term using concrete normal, boundary and failure scenarios. Compare user language with existing `CONTEXT.md`, design and code; surface contradictions rather than choosing the newest text automatically. Propose one canonical term, definition, distinction and any relevant invariant. Keep product behavior in its design owner; `CONTEXT.md` remains a glossary without implementation detail. Persist a resolved entry only with write authorization, using [context format](domain-context-format.md). If the repository uses a context map, update only the affected context and its existing map.

Create an ADR only when the decision is hard to reverse, surprising without context and the result of a real trade-off. State the alternatives, reasons and consequences using [ADR format](domain-adr-format.md). Persist it only with explicit ADR authorization or a repository requirement that records an already-approved decision. An ADR cannot grant approval or change task state. Without persistence authority, return the proposed term or trade-off in the conversation.
