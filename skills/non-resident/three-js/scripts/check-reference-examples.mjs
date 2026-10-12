// CPU contract checks; pass an existing official Three.js r180 package directory.
// This script does not download dependencies, start a browser, or validate GPU output.
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

if (!process.argv[2]) throw new Error('Usage: node check-reference-examples.mjs <three-r180-directory>');
const root = path.resolve(process.argv[2]);
const load = relative => import(pathToFileURL(path.join(root, relative)).href);
const THREE = await load('build/three.module.js');
assert.equal(THREE.REVISION, '180', 'Use the verified r180 baseline');
const GPU = await load('build/three.webgpu.js');
const TSL = await load('build/three.tsl.js');
const { SimplifyModifier } = await load('examples/jsm/modifiers/SimplifyModifier.js');
const { EXRLoader } = await load('examples/jsm/loaders/EXRLoader.js');
const refs = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../references');
const read = name => readFile(path.join(refs, name), 'utf8');
function block(text, heading) {
  const start = text.indexOf(heading);
  assert.ok(start >= 0, `Missing heading: ${heading}`);
  const match = text.slice(start).match(/```javascript\r?\n([\s\S]*?)```/);
  assert.ok(match, `Missing code: ${heading}`);
  return match[1].replace(/^import .*;\r?\n/gm, '');
}
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;

// Real modifier: preserve near detail and monotonically reduce distant topology.
const lodCode = block(await read('14-performance.md'), '### Automatic LOD Generation');
const createLOD = new Function('THREE', 'SimplifyModifier', 'material',
  lodCode.slice(0, lodCode.indexOf('const lod = createLOD')) + '\nreturn createLOD;'
)(THREE, SimplifyModifier, new THREE.MeshBasicMaterial());
for (const source of [new THREE.SphereGeometry(1, 12, 8), new THREE.SphereGeometry(1, 12, 8).toNonIndexed()]) {
  const before = Array.from(source.attributes.position.array);
  const lod = createLOD(source, [1, .5, .25, .1].map((ratio, i) => ({ ratio, distance: i * 50 })));
  const counts = lod.levels.map(({ object }) => object.geometry.attributes.position.count);
  assert.equal(counts[0], source.attributes.position.count);
  assert.ok(counts.every((count, i) => count >= 3 && (i === 0 || count < counts[i - 1])));
  assert.deepEqual(Array.from(source.attributes.position.array), before);
  console.log('LOD vertex counts:', counts.join(', '));
  lod.levels.forEach(({ object }) => object.geometry.dispose());
  source.dispose();
}
assert.throws(() => createLOD(new THREE.BufferGeometry(), [{ ratio: 0 }]), RangeError);

const webgpu = await read('17-webgpu.md');
// Real renderer readback method, with a backend seam returning GPU values unlike CPU values.
const renderer = Object.create(GPU.WebGPURenderer.prototype);
const buffer = new GPU.StorageBufferAttribute(1, 3);
renderer.backend = { getArrayBufferAsync: async attribute => {
  assert.equal(attribute, buffer);
  return new Float32Array([7, 8, 9]).buffer;
} };
const output = await new AsyncFunction('renderer', 'buffer', 'console',
  block(webgpu, '### Reading Buffer Data') + '\nreturn array;'
)(renderer, buffer, { log() {} });
assert.deepEqual(Array.from(output), [7, 8, 9]);
assert.deepEqual(Array.from(buffer.array), [0, 0, 0]);

// Build the actual TSL graph and geometry command; no GPU dispatch is simulated as rendering.
let dispatches = 0;
const scene = new THREE.Scene();
new Function('THREE', 'IndirectStorageBufferAttribute', 'Fn', 'storage', 'uniform', 'select', 'uint',
  'scene', 'camera', 'renderer', block(webgpu, '## Indirect Drawing'))(
  GPU, GPU.IndirectStorageBufferAttribute, TSL.Fn, TSL.storage, TSL.uniform, TSL.select, TSL.uint,
  scene, new THREE.PerspectiveCamera(), {
    compute(node) { assert.equal(node.count, 1); dispatches++; },
    render(value) { assert.equal(value, scene); }
  });
assert.equal(dispatches, 1);
assert.deepEqual(Array.from(scene.children[0].geometry.getIndirect().array), [36, 1, 0, 0]);

// Exercise timestamp feature/rejection branches through real renderer delegation methods.
for (const supported of [true, false]) {
  class CpuRenderer {
    constructor(options) {
      assert.equal(options.trackTimestamp, true);
      const instance = Object.create(GPU.WebGPURenderer.prototype);
      instance._initialized = true;
      instance.backend = {
        hasFeature: name => name === 'timestamp-query' && supported,
        resolveTimestampsAsync: async type => { assert.equal(type, 'render'); return 1.25; }
      };
      instance.init = async () => {};
      instance.render = () => {};
      return instance;
    }
  }
  const run = new AsyncFunction('THREE', 'scene', 'camera', 'console', block(webgpu, '## Timestamp Queries'));
  const result = run({ WebGPURenderer: CpuRenderer }, scene, {}, { log() {} });
  if (supported) await result;
  else await assert.rejects(result, /unavailable/);
}

// Keep the official Rapier adapter's scheduling/returned API, isolating WASM and timers.
let tick;
let steps = 0;
const rapier = (await readFile(path.join(root, 'examples/jsm/physics/RapierPhysics.js'), 'utf8'))
  .replace(/^import .*;\r?\n/gm, '')
  .replace('let RAPIER = null;', 'let RAPIER = injectedRapier;')
  .replace(/export\s*\{\s*RapierPhysics\s*\};?/, '');
const factory = new Function('Clock', 'Vector3', 'Quaternion', 'Matrix4', 'injectedRapier', 'setInterval',
  rapier + '\nreturn RapierPhysics;')(
  THREE.Clock, THREE.Vector3, THREE.Quaternion, THREE.Matrix4,
  { World: class { step() { steps++; } } }, callback => { tick = callback; });
const physics = await factory();
assert.equal(typeof physics.step, 'undefined');
tick();
assert.equal(steps, 1);
const physicsCode = block(await read('16-physics-vr.md'), '### Rapier Physics');
let renders = 0;
new Function('physics', 'requestAnimationFrame', 'renderer', 'scene', 'camera',
  physicsCode.slice(physicsCode.indexOf('function animate()')) + '\nanimate();')(
  physics, () => {}, { render() { renders++; } }, {}, {});
assert.equal(renders, 1);
assert.equal(steps, 1, 'The render loop must not advance physics a second time');

// Actual EXRLoader class, with only I/O replaced: prove dispatch, caching and error propagation.
const assetsCode = block(await read('18-patterns.md'), '### Asset Loader');
const AssetLoader = new Function('EXRLoader', assetsCode.slice(0, assetsCode.indexOf('// Usage')) +
  '\nreturn AssetLoader;')(EXRLoader);
const assets = Object.create(AssetLoader.prototype);
assets.cache = new Map();
assets.loading = new Map();
const originalLoad = EXRLoader.prototype.load;
let calls = 0;
try {
  EXRLoader.prototype.load = function (url, success, progress, failure) {
    calls++;
    if (url.includes('bad')) failure(new Error('invalid EXR fixture'));
    else success({ source: url, isDataTexture: true });
  };
  assert.deepEqual(await assets.load('sky', '/sky.exr'), { source: '/sky.exr', isDataTexture: true });
  await assets.load('sky', '/sky.exr');
  assert.equal(calls, 1);
  await assert.rejects(assets.load('bad', '/bad.exr'), /invalid EXR fixture/);
  assert.equal(assets.loading.size, 0);
} finally {
  EXRLoader.prototype.load = originalLoad;
}
console.log('PASS: LOD, WebGPU CPU contracts, Rapier scheduling, EXR dispatch. GPU/WASM/EXR decoding remain untested.');
