---
name: ship-ice-collision
description: Configure, build, review, and accept LS-DYNA ship-broken-ice-water-air simulations using external case data. Covers deformable floes, multi-material ALE, hull/ice FSI, contact, staged verification, and reproducible physical evidence. Geometry, materials, solver settings, and acceptance thresholds remain project-owned.
---

# Ship-Broken-Ice-Water-Air Simulation

## 1. Separate the workflow from the case

Read the nearest `AGENTS.md` and project authorities. Keep repository paths, ship dimensions, paper-specific values, solver installations, and current results outside this skill. Never silently fill unknown physical parameters.

Select the branch before preparing configuration or running gates:

- **Repository engineering or diagnosis:** use the project's native configuration loader, validation commands, and authorized scope. Consult the relevant physical references; do not require a new generic case file, adapter, or full physical workflow merely to inspect logs or repair the product.
- **Independent case configuration or physical certification:** use the standard case interface, or the project's explicitly documented equivalent and adapter. Normalize data only when this branch needs it; confirm the actual adapter entry point before relying on it. An interface mismatch is not evidence of invalid engineering parameters.

Read [Case data interface](references/case-data-interface.md) when creating or adapting configuration. The detailed fluid workflow covers multi-material ALE/Eulerian modeling. Other schema method values describe case data; they do not imply a supplied CFD coupling implementation or automatic physical qualification.

## 2. Prepare and validate configuration

This step applies when the selected workflow uses the generic case interface. Reuse an existing conforming case file; initialize a new file only when case creation is authorized. Use the project's required Python runtime for the commands below.

```powershell
python <skill-dir>/scripts/init_case_config.py --output <case-config.yaml>
python <skill-dir>/scripts/validate_case_config.py --config <case-config.yaml> --check-paths
```

Fill the template from project data before the second command. [The template](assets/case-config.template.yaml) and [schema](assets/case-config.schema.json) define the stable interface. `null` means required case input is missing, not a recommended value. Put namespaced project additions in `extensions`.

## 3. Advance through independent gates

For physical certification, read [Full simulation workflow](references/full-simulation-workflow.md) for stage inputs, inheritance, and stopping conditions. For repository changes, run only the gates triggered by the affected behavior under project rules:

1. `G0`: software, units, sources, geometry, mesh, materials, keywords, and outputs;
2. `G1`: water-air domain without hull or ice; free surface, pressure, boundaries, mass, energy;
3. `A1/A2`: hull without ice; displacement, inner/outer coupling, motion, waves;
4. `B1/B2`: single/few floes without hull; flotation, migration, contact, deformation, damage;
5. `C`: complete case using frozen, accepted G1/A/B parameters.

Do not inherit failed or unverified settings into a higher gate. Disabled stages require an explicit equivalent evidence basis. Changing a critical parameter invalidates the affected upstream acceptance.

## 4. Apply the physical rules

- **Hull:** preserve traceability among source geometry, physical shell, initialization surfaces, and contact surfaces. Follow the case's open/closed geometry and structural model; check inner air, normals, pressure cancellation, shell quality, and contact resolution.
- **Ice:** use the declared deterministic generator, seed, and saved configuration. No unrecorded manual movement, addition, or deletion. Formal ice remains deformable; source material, failure, and erosion choices from case evidence and matching manuals. Verify single and few floes before a full field.
- **Water/air:** in multi-material ALE, volume-fraction reconstruction and advection advance the interface; do not define water-air contact. Verify version-supported FSI material selection, shell side, normals, and pressure reference separately. Local fractions determine the outer medium; inspect inner air independently for open hulls.
- **Material identities:** shared air, multiple AMMGs, and identity switching require small-case evidence for the selected version, not a universal default.
- **Displacement:** check initial exclusion, displacement at new positions, refill at old positions, and material conservation throughout motion.

For implementation choices or a failed model gate, read [Modeling and keywords](references/modeling-and-keywords.md).

## 5. Run and collect evidence

1. Use the case's solver, version, units, deck, run directory, and output intervals.
2. Record configuration/deck hashes, generator version and seed, solver banner, precision, SMP/MPP, `ncpu`, and command before execution.
3. Use the companion `$lsdyna` skill for deck execution and diagnosis. Locate its installed `SKILL.md` before relying on it. If unavailable, continue independent configuration/model review and report the missing execution dependency; do not silently install it, invent its behavior, or claim a solver gate passed.
4. Inspect at least `messag`, `d3hsp`, `glstat`, and `matsum`; add `d3plot`, `dbfsi`, `rcforc`, `sleout`, and other case outputs.
5. Compare volume fractions, pressure, mass, energy, contact, flotation, waves, and damage at the configured times and regions.
6. Preserve raw loads. Derived smoothing, interpolation, or fitting requires explicit case permission and must also satisfy stricter project rules; name and label it separately. Select `rcforc` by target contact input ID and slave/master side, without cross-interface or double-sided summation. For live exports, record size and SHA-256 from one byte snapshot.

Read [Acceptance and reporting](references/acceptance-and-reporting.md) before judging or reporting results. Passing the configuration checker proves only interface structure and selected cross-field rules, never physical acceptance.

## 6. Use evidence appropriate to the version

- For keywords, EOS, ALE/FSI, or version questions, read [Official sources](references/official-sources.md). Use `scripts/official_docs.py` with supplied or discovered matching manuals.
- For papers, experiments, and empirical data, read [Evidence mapping](references/evidence-data-mapping.md). Separate direct values, conversions, derivations, calibration, assumptions, and unsupported fields.
- Adopted values enter through case configuration and provenance. A published parameter set is not a cross-case default. Version-specific observations in references are historical guidance requiring case-specific verification, not evidence that a new run passed.
