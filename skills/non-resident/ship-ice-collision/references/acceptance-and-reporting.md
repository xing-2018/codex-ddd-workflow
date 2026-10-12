# Acceptance and Reporting

## 1. Status

- `pass`: input, runtime, numerical, and physical evidence meets the case's predeclared gates.
- `fail`: direct contrary evidence, such as unstable fluid, nonphysical fluid ingress, sustained sinking, clear penetration, or solver error.
- `pending`: not run, insufficient evidence, indistinguishable variables, or outstanding manual review.

`Normal termination` alone establishes no physical gate. Project reporting labels may be more specific; preserve the case interface's status values.

## 2. Stage acceptance

| Stage | Main evidence | Meaning of acceptance |
| --- | --- | --- |
| G0 | Configuration, sources, deck, mesh, manifest | Runnable, traceable inputs |
| G1 | Fractions, pressure profile, mass, energy, boundary probes | Usable static water-air domain |
| A1 | Hull inner/outer fractions, FSI, pressure, timestep | Displacement and shell-side treatment |
| A2 | Motion, bow/side/wake waves, reflections | Interpretable dynamic hull-water-air response |
| B1 | Freeboard, attitude, vertical velocity, fractions, force balance | Single-floe flotation and migration |
| B2 | Contact, deformation, damage, fractions, energy | Few-floe multibody response |
| C | Full-window collision, waves, fractions, loads, energy | Full case meets its own objective |

Thresholds come from `acceptance.stages` and the project adapter, not skill defaults.

## 3. Numerical evidence

### Runtime integrity

Match solver path/version/precision/parallel mode to configuration. Explain errors/warnings in `messag`; check keywords, IDs, and fields in `d3hsp`. Cover the target interval, explain timestep collapse, and exclude old outputs from current-run evidence.

### Energy and mass

Check total energy against initial energy plus external work; kinetic/internal energy over each phase; hourglass, contact/sliding, interface, and damping energy; added/eroded mass and per-material changes; and fraction closure plus volume/mass drift against the case thresholds.

When `matsum` lacks direct mass but the same material/MMG block contains `x/y/z-mom` and `x/y/z-rbv` verified as mean velocity, recover positive `mass_i=momentum_i/mean_velocity_i` only from components exceeding a predeclared absolute-velocity floor. Report component dispersion and require consistency. Zero-velocity or unusable-ratio states remain unavailable, without interpolation or carry-forward. Sum switchable MMG identities by physical water/air material before drift analysis; never add the ALE aggregate and its MMG children twice. This checks grouped mass only, not fraction closure or control-volume flux.

Inherited R10 guidance cites Volume I Appendix E for the momentum/mean-velocity relationship. Verify that reference and output labels for the actual version before using it; historical notes are not current-run evidence. Fraction integration gives occupied volume, not density-weighted mass. Without density integration and boundary-flux audit, small volume drift cannot negate excessive mass drift. If a frozen whole-history maximum mass-drift limit is exceeded after precision/component checks, record `fail`; an authorized run may continue to its target to collect full failure evidence.

### Interfaces and contact

Distinguish hull, ice, and required inner/outer interface IDs. Explain force directions, offsets, double counting, and impulses. Separate ship-ice/ice-ice outputs. Check penetration initially and during motion with logs/images. Failure should follow explainable loading, not initialization or artificial startup waves.

## 4. Fractions and waves

Read sample times and regions from `acceptance.stages.<stage>`. Typical times include initial, pre-event, first post-event, sustained interaction, and final states; typical regions include inner/outer hull, floe cores and old/new positions, near free surface, wake, and top/side/bottom boundaries.

Separate the penalty/advection numerical interface band from the deep structural core:

- Report interface-band peaks, unique exceeding-cell counts, consecutive exceedance duration, integrated mixed-material volume, and recovery. A single boundary-cell spike does not establish persistent internal flooding.
- Define the deep core outside the case's interface band and apply the frozen exclusion threshold there.
- Growing, persistent, or deep-core ingress, especially with mass/energy/attitude/pressure anomalies, is contrary evidence. Brief interface mixing with an excluded core is recorded as numerical mixing.
- Set band widths from local ALE mesh and actual FSI support before interpreting results; do not widen the excluded band after viewing failures.

Preserve bow/side/wake images, fixed probes, and moving profiles. Compare far-field reflection with near-field waves; waves alone are insufficient without pressure, fractions, mass, and energy. Compare boundary pressure with the deck's hydrostatic/reference function and establish when loading becomes active. If the `t=0` plot predates applied boundary stress, use the first verified loaded positive-time state for dynamic pressure differences while retaining `t=0` for initial geometry/fractions. Do not label the startup load step as reflection or long-term drift.

## 5. Images and data

Record case ID, state, time, view, variable, part/material group, units, and legend. Batch images retain command files and input paths; manual images retain the operator's judgment. Separate diagnostic candidates from acceptance images. A fringe plot without a legend does not establish a particular material fraction; a deck-card image is not a GUI parameter panel. Link raw files, parsed CSV/JSON, images, and reports.

Historical LS-PrePost 4.5 notes report `fcomp history N` rejected as `Invalid command fcomp!` under `-nographics`. Do not infer batch commands from GUI labels. Even a nonempty PNG after such an error is not AMMG-fraction evidence. Preserve `lspost.msg`; where no validated selector is available, use a qualified background d3plot reader with array/channel mapping and closure checks. Record closed-file evidence, state, color scale, units, and source hashes, and label it as reader-generated rather than a native LS-PrePost screenshot. Verify behavior for the actual version instead of treating this observation as a universal restriction.

## 6. Loads

Preserve original contact/FSI output. Select the interface via `outputs.contact_load.source`, not inferred ice force from total force. Record axes, interface ID, units, and interval. `preserve_raw` must be true. Produce separately labeled smoothing/interpolation/fitting only with explicit case permission and within project constraints.

Select `rcforc` by the target contact input ID from the deck/legend and the specified slave/master side. The number following that side participates in entity selection. Do not sum same-time records across unrelated contact IDs or double-count action/reaction sides. Prove the selected load represents the intended physical interface.

During an active run, derive CSV/JSON/plots from one byte read, record its size/SHA-256, and label the package `interim`. Generate a separate `final` full-history package after completion. Raw-curve CSV retains times, three force components, resultant magnitude, and axial force from an explicit coordinate convention; document derived-column formulas. Plot lines connect raw samples without generating/exporting resampled points.

## 7. Report contents

Use `case.report_path` and include the applicable items:

1. Case ID, objective, and conclusion.
2. Units, software, solver, and hardware.
3. Sources, adapter, normalized configuration, and hashes.
4. Hull geometry, structure, and mesh.
5. Ice generation, mesh, material, and failure.
6. Water-air domain, initialization, pressure, and boundaries.
7. FSI/contact, motion, solver controls, and outputs.
8. G1/A/B parameter inheritance.
9. Logs, timestep, mass, and energy.
10. Dynamic fractions, flotation, waves, contact, and damage.
11. Raw loads and separately labeled processed curves, if permitted.
12. Failure records, limits, residual risks, and a `pass|fail|pending` matrix.

Link every material conclusion to raw files or reproducible derived evidence in the case results directory.
