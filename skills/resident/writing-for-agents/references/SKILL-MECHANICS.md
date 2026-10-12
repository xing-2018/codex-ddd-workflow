# Skill mechanics

Use this reference for Skill metadata and routing; shared instruction review rules live in [SKILL.md](../SKILL.md).

## Metadata and invocation

- Keep `SKILL.md` frontmatter `name` and `description` valid. Make the description a short, discriminating task trigger; put procedures in the body.
- Describe the operation that needs the Skill, not every topic it touches: a migration Skill applies to creating, changing or reviewing migrations, not all database work. Check nearby descriptions for conflicting or overlapping triggers before adding stronger invocation language. Large catalogs and long descriptions can cause host shortening; no fixed safe length is assumed.
- Preserve supported UI fields and invocation policy in `agents/openai.yaml`. `policy.allow_implicit_invocation` defaults to `true`; `false` disables implicit selection, while explicit `$skill-name` invocation remains available. Do not change policy to achieve apparent context savings.
- A router names exact phase files, their entry conditions, and return or stopping criteria. Reading a linked phase as workflow instructions is distinct from host implicit selection; it grants no new permissions. Keep ordinary references as references, without adding Skills or enabling implicit selection solely to make them reachable.
- Keep metadata consistent with supported use; check local links and run the available Skill validator. Structural validity does not establish invocation or task success.

Host fields: [official Skill metadata](https://learn.chatgpt.com/docs/build-skills#optional-metadata). Verify current host behavior when the task depends on it.

## Model guidance maintenance

For an explicitly requested current-model comparison, fetch relevant [official model guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices). Separate official recommendations from local heuristics; apply only guidance relevant to the task and preserve explicit user constraints. Routine instruction review needs no model-guide lookup.

The [OpenAI article on skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), published September 11, 2026, informs the trigger, disclosure and completion review rules here. Treat it as model-specific guidance, not a new Skill format or blanket permission to remove safeguards.

For model-specific changes, identify the intended readers: shared repository instructions may also serve Sol, Luna or other models. Retain necessary domain guidance and explicit user boundaries; do not generalize an Astra recommendation into a universal capability guarantee. Report untested cross-model effects. Review whether old caution or first-implementation stops still express the user's intent; propose changes when that intent is unresolved, rather than silently relaxing them.

## Context measurement for maintenance

Measure initial catalog metadata, the selected entry body, and all references actually read on each representative task path separately. Also compare the complete changed ownership set, including new receiving references; relocation alone is not a net saving. Normalize to UTF-8 with LF and report bytes and whitespace words. Use the term model tokens only with an identified tokenizer; host usage, caching, latency and subscription consumption are separate measurements.

Compare shortest valid paths and necessary deeper branches, including direct callers outside a router. Each entry should expose its trigger, inputs, shortest valid method, conditional reference map and completion or stopping criteria. Avoid whole-reference preloads, recursive catalog scans, copied transcripts and repeated reading of unchanged material. Finishing a Skill does not establish that its text is unloaded from conversation history.

These are maintenance review signals, not runtime checklists, length quotas or limits on Skill calls. Preserve permission boundaries, domain methods and required validation even when they cost more context.
