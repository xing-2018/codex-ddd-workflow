# Upstream provenance

- Source: https://github.com/noklip-io/agent-skills
- Adopted commit: `319a0f1aac3b3580e736d457f217d716b356aa35`
- Adopted directory: `skills/three-js/`
- License: [MIT](LICENSE), copied from the repository root at the same commit.
- Initial managed version: `1.0.0`; no prior managed history or upstream Skill version was found.
- Local adaptations: concise invocation description, version/project boundary, Codex metadata, version and provenance files. All 18 reference documents and the upstream README are retained; UV-channel and Clock examples were subsequently corrected against official release sources.
- Scope: non-resident; install only into an explicitly selected project through the managed source repository.

## Compatibility corrections

Version 1.0.1 corrects UV selection/naming and once-per-frame Clock sampling;
adds version-aware Timer guidance without changing the target dependency.
See [Texture r180](https://github.com/mrdoob/three.js/blob/r180/src/textures/Texture.js),
[UV selection r180](https://github.com/mrdoob/three.js/blob/r180/src/renderers/webgl/WebGLPrograms.js),
[Clock r180](https://github.com/mrdoob/three.js/blob/r180/src/core/Clock.js), and
[Timer](https://threejs.org/docs/pages/Timer.html). The adopted Skill commit above is unchanged.

Version 1.0.2 corrects r180 node-function and node-material import ownership
and removes the unavailable legacy-lighting optimization. Other release-sensitive
examples still require the locked-release check; the upstream baseline is unchanged.

Version 1.0.3 restores the existing LOD, WebGPU, physics and EXR examples without
adding a capability or changing the target dependency. LOD ratios now retain
vertices after the modifier's normalization; GPU readback, indirect drawing and
timestamp queries use r180 APIs; Rapier/Ammo adapters own their simulation timers;
the asset loader dispatches EXR files to EXRLoader. Official r180 sources:
[SimplifyModifier](https://github.com/mrdoob/three.js/blob/r180/examples/jsm/modifiers/SimplifyModifier.js),
[Renderer](https://github.com/mrdoob/three.js/blob/r180/src/renderers/common/Renderer.js),
[BufferGeometry](https://github.com/mrdoob/three.js/blob/r180/src/core/BufferGeometry.js),
[WebGPUBackend](https://github.com/mrdoob/three.js/blob/r180/src/renderers/webgpu/WebGPUBackend.js),
[RapierPhysics](https://github.com/mrdoob/three.js/blob/r180/examples/jsm/physics/RapierPhysics.js),
[AmmoPhysics](https://github.com/mrdoob/three.js/blob/r180/examples/jsm/physics/AmmoPhysics.js), and
[EXRLoader](https://github.com/mrdoob/three.js/blob/r180/examples/jsm/loaders/EXRLoader.js).

When maintaining these examples, run the executable
[CPU contract checks](scripts/check-reference-examples.mjs) against an existing
official r180 package directory:

```text
node scripts/check-reference-examples.mjs <three-r180-directory>
```

The checks execute the reference snippets with real r180 geometry, modifier,
node and renderer API implementations. I/O, GPU backend results and the physics
engine are isolated at their boundaries. This verifies dispatch and data flow,
not GPU rendering/timing, WASM simulation accuracy or EXR decoding. Those checks
still require the target project's authorized runtime.
