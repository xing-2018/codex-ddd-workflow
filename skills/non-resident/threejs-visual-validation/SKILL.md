---
name: threejs-visual-validation
description: Validate advanced Three.js graphics as authored systems rather than subjective screenshots. Use for fixed-view visual contracts, field and pass diagnostics, no-post baselines, seed sweeps, camera-scale tests, temporal stability checks, GPU budgets, and regression evidence for procedural scenes.
---

# Visual Validation

## Application boundary

Apply checks to mechanisms that exist and are affected by the authorized task,
or are needed to substantiate its acceptance claims. Explain material exclusions;
missing evidence for an applicable check remains unverified. Preserve temporal
evidence for motion or flicker claims and deterministic inputs for comparisons.

Use existing authorized inspection tools or an isolated test surface for diagnostic controls and captures. This skill does not authorize adding product UI, visual effects, dependencies, changing renderer backends, deleting product files, or publishing results. Reuse the project's approved visual contract and startup workflow.


Evaluate the mechanism that creates the image. A beautiful hero screenshot can hide unstable fields, broken depth, seed failures, or post-processing dependence.

## Validation sequence

Select the sequence, evidence, and failure conditions below by the application
boundary; they are not an unconditional checklist for every scene.

1. Freeze deterministic inputs.
2. Capture the no-post baseline.
3. Capture system-specific diagnostic views.
4. Test the intended camera-distance envelope.
5. Sweep representative seeds and parameter extremes.
6. Test motion and temporal stability.
7. Record image, geometry, memory, and timing budgets.
8. Keep a small regression set tied to visual invariants.

Read [references/graphics-validation-protocol.md](references/graphics-validation-protocol.md)
for visual contracts, required inspection controls, mechanism-specific
evidence, temporal checks, budgets, and explicit rejection criteria.

## Required evidence

- fixed-camera and reproducible-input manifest, including seed when applicable;
- final captures and a no-post baseline when relevant image effects exist;
- field/pass diagnostics needed to substantiate the affected mechanism;
- near, design, and far camera views;
- representative and stress seeds when affected behavior is stochastic;
- frame-time and render-target inventory;
- written invariants and known compromises.

## Failure conditions

- a motion or flicker claim relies on a single frame;
- a relevant post-processing contribution cannot be isolated sufficiently to substantiate the claim;
- stochastic inputs needed for comparison are not reproducible;
- GPU time is inferred only from CPU frame time;
- temporal artifacts are judged from still images;
- comparison thresholds ignore intentional stochastic pixels without stabilizing them.

## Routing boundary

This skill evaluates an implementation; it does not supply the implementation
mechanism. Load the subject or image-effect skill first, then use this protocol
to decide whether the result is acceptable.
