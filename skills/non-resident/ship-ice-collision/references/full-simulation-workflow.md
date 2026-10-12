# Full Ship-Ice-Water-Air Workflow

## 1. Input boundary

Read case data from configuration validated against `case-config.schema.json`. Repository paths, directory conventions, hull shape/dimensions, mesh sizes, floe count/concentration/thickness/seed, material/EOS coefficients, motion, termination, solver installation/resources, numerical thresholds, and current status remain project-owned. Use a project adapter and `extensions.<namespace>` rather than altering core fields for one case.

## 2. Gates and inheritance

```text
G0  Input and deck review
 |
G1  Static water-air domain
 |
A1  Hull displacement over a short, low-speed motion
 |
A2  Hull target motion and waves
 |
B1  Single-floe flotation and migration
 |
B2  Few-floe contact, deformation, and damage
 |
C   Full ship-ice-water-air case
```

`acceptance.stages` specifies enablement, time windows, thresholds, and evidence. Explain equivalent validation for disabled stages. At every gate, preserve reproducible input and separate failed outputs; judge numerical stability and physical validity separately. Inherit only frozen, accepted parameters. A critical change returns affected upstream acceptance to `pending`.

## 3. G0: pre-run review

- **Software/units:** use `case.unit_system` without implicit conversions; record executable, version, precision, parallel mode, `ncpu`, memory, and preprocessing/mesh/postprocessing/generator versions. Match keyword fields to the actual solver.
- **Hull:** check source URI, coordinates, scale, transforms, physical versus initialization surfaces, and contact/FSI sets. Follow `geometry.hull.open_deck`; inspect normals, free edges, duplicate faces, degenerate elements, aspect ratio, warpage, and local resolution.
- **Ice:** read generator/version/configuration URI/seed from `ice.generator`. Recompute count, area/concentration, distributions, thickness, clearances, overlaps, solid-mesh quality/layers/aspect ratios, and material/failure inputs. No unrecorded manual placement in formal cases.
- **Fluid/interfaces:** check method, domain, mesh, free surface, gravity, materials/EOS, pressure reference, boundaries, initial fraction closure, and exclusion from occupied volumes. Record actual coordinates for diagnostic reduced domains and formal domains separately. When a boundary/wave gate fails, check boundary distance in the formal domain before changing thresholds. Verify hull sides, closed floe surfaces, normals, material sets, interface IDs, contact sets, and dedicated output IDs.

Do not launch a large model while G0 is unaccepted.

## 4. G1: static water-air domain

Remove hull and ice while retaining the full case's core fluid settings. Check free-surface drift, consistent hydrostatic/air pressure references, fraction closure, per-material volume/mass/energy drift, unexplained top/side/bottom reflections, and distinguishable water/air/free-surface outputs against case thresholds.

A G1 failure calls for fluid material, EOS, initialization, mesh, pressure, or boundary changes; do not compensate with hull/ice settings.

## 5. Case A: hull-water-air

### A1: displacement and shell sides

Use the full hull over a small displacement. Verify initial fluid exclusion, new-position displacement, old-position refill, no nonphysical hull flooding, local fraction-dependent outer loading, inner air/normals/pressure cancellation for open shells, and explainable FSI direction, static bias, duplicate forces, leakage, and timestep.

Start with the simplest version-supported, physically interpretable side treatment. Shared air, multiple AMMGs, or identity switching need matching manuals and small-case evidence.

For cases requiring `*ALE_FSI_SWITCH_MMG_ID`, read the applicable version's manual before applying the following inherited R10 guidance. Its numerical suggestions are starting points to verify, not cross-version defaults:

- Derive a checkable normal from monitor-node order; `XOFF` direction follows that normal, not a global-axis guess.
- Historical guidance uses `|XOFF|` at least two local ALE cell widths and `XLEN` around half the minimum cell edge; confirm validity for the selected version and topology.
- First check static identity distribution and spurious switched mass against the case threshold, then a motion that actually crosses the monitor.
- Forward/reverse exchanges use separate oppositely oriented monitors, different switch IDs, and different AMMG identities to avoid one identity on both sides of the same penalty shell.
- Compare `dbfsi.mout` with switched mass in `d3plot` at the same or nearest documented time, never an earlier force-output row against a final plot state.
- Also check switched material on the intended side, total water/air mass, fraction closure, static free surface, and timestep. A measured failure is `fail`; unresolved evidence stays `pending`. Neither permits inheritance.

### A2: motion and waves

Use `run.speed_curve` and case termination criteria. Hold/ramp/constant-speed junctions must not duplicate times. Verify strictly increasing times, target motion, speed established before estimated first contact when required, interpretable bow/side/wake waves, fixed and moving probes distinguishing near-field waves from reflections, and continued hull-interior fraction, mass, and energy acceptance.

Visible waves support this gate but do not establish coupling validity alone.

## 6. Case B: ice-water-air

### B1: single-floe flotation and migration

Use a small fluid domain and few elements while retaining the formal ice material type and core FSI settings. Verify initial exclusion, theoretical/numerical freeboard and attitude, bounded vertical velocity/heave/roll, fraction-dependent loading during motion, new-position displacement, old-position refill, material mass, and vertical force balance. Write the run manifest before the solver starts; reconstructed provenance supports diagnosis only.

For version-dependent erosion, AMMG switching, or leakage diagnosis, use matching manuals and isolated tests. Inherited R10 observations below are not fresh acceptance evidence:

- Erodible solid ice with `CTYPE=5` uses part/part-set slaves unless the target reader explicitly accepts `SSTYP=2` segment sets. Do not substitute a generator's exterior segments without testing.
- For identity switching around closed ice, verify monitor normals, the locally appropriate `XOFF` distance, and identical MAT/EOS for pre/post-switch dummy identities. The inherited two-cell starting distance is conditional; reject an `XOFF=0` gate that switches material inside the structure.
- Test mapped water/air identities, reverse-side FSI, and leakage controls separately. Opposite-side coupling may cancel buoyancy. Historical R10 mapped-AMMG runs reported `Error 41267` with `ILEAK=2`; ordinary three-AMMG evidence does not qualify that topology.
- Vary `NQUAD`, `FRCMIN`, `PFAC`, and `PLEAK` one principal factor at a time. Compare core water/air peaks, freeboard, refill, mass, and energy together; improving one phase's leakage can worsen the other or change net buoyancy.
- In a small open-air domain, buffer height and nonreflecting boundary distance can influence raw air-mass drift. Domain enlargement is a boundary-independence test, not permission to dilute the denominator. Report absolute/relative changes and boundary flux/reflection evidence.

### B2: few floes

Use the same deterministic generator. Verify ice-ice search/friction, deformation, plasticity, failure, erosion, contact/hourglass energy, deleted material and mass loss, and continued per-floe fraction/flotation behavior.

## 7. Case C: full collision

Freeze G1/A/B configuration fragments and hashes, generator/version/config/seed, deck/mesh fingerprints, solver information, acceptance results, inheritable settings, and known limits before merging.

Cover the configured precontact motion, first ship-ice contact, sustained ship-ice/ice-ice interaction, floe motion/deformation/damage, free surface/waves, fractions at selected times/regions, raw contact/FSI loads, mass, energy, added mass, timestep, and warnings.

Map `dbfsi` surface IDs from the current deck's `*DATABASE_FSI` to outer/inner hull, ice, and any AMMG switch. Do not assume consecutive IDs or `1/2`; distinguish integer-ID rows from floating-point continuations and retain the ID-to-physical-surface mapping.

`outputs` and `acceptance` own durations, sampling, screenshots, and reports. The skill supplies no fixed run duration or interval.

## 8. Failure routing

| Symptom | Return to or inspect |
| --- | --- |
| Static-fluid drift | G1 |
| Hull failure after accepted G1 | Inner/outer sides, pressure reference, normals, material sets, FSI |
| Incorrect single-floe flotation | Density, gravity, freeboard, initial fractions, vertical interface force, boundaries |
| Fluid in occupied structure | Initialization geometry, displacement, leakage, variable meaning |
| Ice damage before contact | Startup pressure waves, initial clearances, failure model, FSI penalty |
| Timestep collapse | Small/distorted elements, negative volume, contact stiffness, ALE advection, mass scaling |
| Missing direct evidence | Keep `pending`; do not infer acceptance from termination or one image |
