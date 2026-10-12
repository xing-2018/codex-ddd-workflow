# codex-ddd-workflow

## Scope and instruction sources

- This is the Windows edition. Other platforms require user adaptation. Use the user's language and resolve tools and paths from their computer.
- AGENTS.global.md is an optional global instruction source. Do not load it as additional project rules. Adoption requires the user's decision about exact content and scope; never automatically merge, replace or write user AGENTS.md or change config.toml.
- English AGENTS and Skill files are execution sources. AGENTS_zh.md, AGENTS.global_zh.md and Skill Chinese counterparts are review copies, not additional execution instructions. Reading a Skill does not authorize installing or invoking it.
- Protect existing instructions, configuration and unrelated files. Missing tools or dependencies block only the dependent action; do not install them or change settings without authorization.

## Installation and updates

- Follow README.md and docs/安装与更新.md. Obtain a fixed repository version and use scripts/install_public_distribution.py to inspect the source and targets.
- Default installation covers all resident Skills. Add bundled roles only when the user selects workflow mode. Install selected non-resident Skills only into an explicitly named project.
- Show the fixed version, resolved targets, differences, conflicts and backup locations. Execute only an explicitly authorized installation; reuse authorization for the same unchanged plan. Stop dependent writes on source or target drift.
- Updates require the local installation receipt to match the existing files. Preserve unknown, newer and locally modified targets. Keep backups outside Skill and role discovery directories, verify all copied files and report recovery failures with retained locations.
- Keep installation plans and logs under this checkout's .local-artifacts/<task>/; they contain local paths and must not be committed or shared.
- After installation, check Skill and role availability in a new Codex conversation. Use docs/使用指南.md and the selected Skill's requirements for actual tasks.
