# Three.js Skill

Comprehensive Three.js reference for 3D web graphics.

Usage and prerequisites: [SKILL.md](SKILL.md). Version: [VERSION.txt](VERSION.txt).

This Skill is distributed through [codex-ddd-workflow](https://github.com/xing-2018/codex-ddd-workflow), the Windows edition. Other platforms require user adaptation and validation. Original third-party licenses and upstream notes remain in this directory where applicable.

Install only into an explicitly named project's `.agents/skills/three-js`. Ask Codex to obtain a fixed public version and follow the [installation procedure](https://github.com/xing-2018/codex-ddd-workflow/blob/main/docs/安装与更新.md). Compare the complete source and target, preserve unknown/newer/local changes, back up before replacement, and verify the full directory hash. Installation never automatically merges AGENTS.md or changes config.toml.

Updates are user initiated. Follow the [public version rules](https://github.com/xing-2018/codex-ddd-workflow/blob/main/docs/版本与发布.md); no automatic polling, dependency changes or deletion of other copies. Runtime actions still need the current task's authorization.

Original provenance and license: [UPSTREAM.md](UPSTREAM.md) and [LICENSE](LICENSE).

## What's Included

18 reference files covering all aspects of Three.js:

| Category | References |
| --- | --- |
| Core | fundamentals, geometry, cameras, math |
| Visuals | materials, textures, lighting, shaders |
| Motion | animation, interaction, controls |
| Assets | loaders (GLTF, FBX, SVG, fonts, HDR) |
| Effects | post-processing (bloom, DOF, SSAO) |
| Advanced | performance, WebGPU, TSL, physics, VR/XR, patterns |

This Skill covers native, imperative Three.js. React Three Fiber and its ecosystem require matching project guidance; do not apply this Skill's native API advice as if it covered them.
