---
name: three-js
description: Vanilla Three.js development, review, and optimization for scenes, geometry, cameras, materials, lighting, GLSL shaders, postprocessing, picking, and resource lifecycle. Use for imperative Three.js code; do not infer React Three Fiber usage merely from a React host.
---

# Three.js Complete Reference (Vanilla)

## Version and project boundary

Read the target project's locked Three.js version and renderer backend before using examples. This reference spans releases; verify version-sensitive APIs against that release's official source or documentation. Skill installation does not authorize a dependency upgrade, renderer migration, new visual effects, or changes to data and color semantics. Keep existing project startup and validation commands.


> **React Three Fiber users**: This reference is for vanilla Three.js. For an actual
> R3F/Drei task, use `r3f-best-practices` only if the target host exposes that skill.
> Otherwise check the official documentation for the project's locked versions and
> report any remaining capability gap. Do not install an external skill automatically
> or infer R3F merely from a React host. Three.js concepts here still apply to R3F.

## Quick Start

```javascript
import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

scene.add(new THREE.AmbientLight(0xffffff, 0.5));
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
scene.add(light);

camera.position.z = 5;

function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();
```

## Reference Index

Load the appropriate reference file based on task:

### Core Foundation
| Reference | Use When |
|-----------|----------|
| `references/01-fundamentals.md` | Scene setup, renderer config, Object3D hierarchy, coordinate systems |
| `references/02-geometry.md` | Creating shapes, BufferGeometry, instancing, points, lines |
| `references/06-cameras.md` | Camera types, frustum, viewport, projection |
| `references/13-math.md` | Vector3, Matrix4, Quaternion, Euler, Color, MathUtils |

### Visual Appearance
| Reference | Use When |
|-----------|----------|
| `references/03-materials.md` | PBR materials, shader materials, all material types |
| `references/04-textures.md` | Texture loading, UV mapping, render targets, environment maps |
| `references/05-lighting.md` | Light types, shadows, IBL, light probes |
| `references/11-shaders.md` | Custom GLSL shaders, uniforms, varyings, shader patterns |

### Motion & Interaction
| Reference | Use When |
|-----------|----------|
| `references/08-animation.md` | Keyframe animation, skeletal, morph targets, procedural motion |
| `references/09-interaction.md` | Raycasting, selection, drag, coordinate conversion |
| `references/10-controls.md` | OrbitControls, FlyControls, PointerLockControls, etc. |

### Assets
| Reference | Use When |
|-----------|----------|
| `references/07-loaders.md` | GLTF, FBX, textures, HDR, Draco compression, async patterns |

### Effects
| Reference | Use When |
|-----------|----------|
| `references/12-postprocessing.md` | Bloom, DOF, SSAO, custom effects, EffectComposer |

### Advanced
| Reference | Use When |
|-----------|----------|
| `references/14-performance.md` | Optimization, profiling, LOD, culling, batching |
| `references/15-node-materials.md` | TSL (Three Shading Language), node-based materials |
| `references/16-physics-vr.md` | Physics engines, WebXR, VR/AR integration |
| `references/17-webgpu.md` | WebGPU renderer, compute shaders, WGSL |
| `references/18-patterns.md` | Architecture patterns, asset management, cleanup, state |

## Common Patterns Quick Reference

### Resize Handler
```javascript
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

### Cleanup/Dispose
```javascript
function dispose(obj) {
  obj.traverse(child => {
    if (child.geometry) child.geometry.dispose();
    if (child.material) {
      if (Array.isArray(child.material)) {
        child.material.forEach(m => m.dispose());
      } else {
        child.material.dispose();
      }
    }
  });
}
```

### Animation Loop with Clock

For existing Clock-based code, sample once per frame and share the result.
`getElapsedTime()` also calls `getDelta()` internally. For new code, prefer
[Timer](https://threejs.org/docs/pages/Timer.html) when supported by the locked
release: call `update()` once per frame, then read `getDelta()` and `getElapsed()`.
Clock was deprecated in r183; its deprecation does not require a dependency upgrade.

```javascript
const clock = new THREE.Clock();

function animate() {
  const delta = clock.getDelta();
  const elapsed = clock.elapsedTime; // Read after the single getDelta() call

  // Use delta for frame-rate independent animation
  mixer?.update(delta);

  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
```

## Import Patterns

```javascript
// Core
import * as THREE from 'three';

// Addons (controls, loaders, effects)
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';

// Compression support
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';
```

## Version Notes

This reference targets Three.js r150+ with notes for:
- WebGPU support (r150+)
- Node materials / TSL
- Modern ES module imports

For version-specific APIs, check the Three.js migration guide.
