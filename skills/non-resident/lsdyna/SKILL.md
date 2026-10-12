---
name: lsdyna
description: Run, inspect, and diagnose Ansys LS-DYNA keyword decks (.k, .key, .dyn). Use for local solver and license checks, explicit-run gates, output integrity, timestep, energy and contact diagnosis, and reproducible run provenance. The bundled runner launches a local Windows executable; MPI launch setup is project-owned.
---

# LS-DYNA Execution and Diagnosis

## 1. Establish the task and environment

Classify the request as an environment/license check, static deck review, minimal gate or production run, output diagnosis, or modeling advice. Read the nearest `AGENTS.md`; project units, solver version, executable, output directories, acceptance rules, and permissions take precedence.

Before execution, state the objective, units, absolute solver path and version, precision, SMP/MPP mode, input deck, run directory, `ncpu`, memory, termination time, required outputs, and pass/fail criteria. Use a pinned executable explicitly. If no version is specified and several candidates exist, list them and resolve the selection before launching.

The supplied PowerShell runner directly invokes a Windows executable with `i=`, `ncpu=`, and optional `memory=` and `mcheck=y`. It does not configure MPI or a scheduler. MPP/hybrid runs need the project's verified launcher and equivalent provenance; do not present the bundled runner as a universal MPP launcher. The Python inspector can inspect available outputs independently of the launch method.

## 2. Review the deck

- Resolve the deck and every `*INCLUDE` from the run directory.
- Check the dimensions of density, modulus, velocity, time, pressure, mass, and energy in the declared unit system.
- Verify nontrivial keyword field order with the matching official manual.
- Check missing/duplicate IDs, negative volumes, degenerate elements, initial penetration, contact surfaces, constraints, and initial conditions.
- Request `GLSTAT` and the problem's required `MATSUM`, `RCFORC`, `SLEOUT`, `NODOUT`, `d3plot`, and FSI/ALE outputs explicitly.
- Before a large calculation, run the smallest independent gate that exercises the relevant behavior.

## 3. Execute with provenance

For a compatible local Windows run:

```powershell
& "<lsdyna-skill>/scripts/run_lsdyna.ps1" `
  -InputDeck "<case-dir>/main.k" `
  -Solver "<solver-executable>" `
  -Ncpu <ncpu> `
  -Memory "<memory>" `
  -RequireNormalTermination
```

The deck and run directory must coincide so relative includes retain their meaning. Use separate production run directories and preserve failed cases. The optional `-Clean` deletes only exact known output-family names in that directory, without recursion, and excludes `.k`, `.key`, and `.dyn`; its availability does not authorize cleanup.

Preserve `run.log` and the pre-run `run_manifest.json`. Runner schema v5 records the entry `input_sha256`, all `.k/.key/.dyn` files beneath the run directory with relative paths, sizes and SHA-256, prior top-level file signatures (except the manifest itself), current-run file changes, and normal-termination evidence. The top-level snapshot supports custom inspector `--require` filenames and hashes binary outputs too; allow for this I/O cost on large result directories. The keyword inventory is not a resolved include graph: account separately for inputs outside that tree or with other extensions. Store license-source categories, never license argument or environment values. Old logs cannot establish completion of the current run; a manifest reconstructed afterward is diagnostic provenance only.

Earlier schema-v5 manifests may cover only `messag`, `d3hsp`, `glstat`, `matsum`, and `run.log`. An extra file absent from their current-run list remains unproven; this update cannot reconstruct missing pre-run evidence. Preserve those manifests and assess additional provenance separately. A new authorized run with the updated runner is needed to establish the additional files through this automatic check; do not relabel old files as newly proven.

For a reader/initialization gate, full restart, or result-family reconstruction, read [Version-specific execution notes](references/explicit-run-acceptance.md#9-version-specific-execution-notes). These modes can advance cycles or write large files; they are not read-only checks.

## 4. Diagnose outputs

Start with the read-only summary:

```powershell
python <lsdyna-skill>/scripts/inspect_lsdyna_run.py <run-dir>
```

Use `--json --output <evidence.json>` when an evidence file is requested. The inspector distinguishes `running`, `incomplete`, `pass`, and `fail`, resolves numbered restart outputs, and leaves `physical_status` as `pending`. A `running` manifest does not establish that the process is alive; also inspect process state and output timestamps. Exit codes are 0 for `pass`/`running`, 1 for `fail`, and 2 for `incomplete`. The legacy JSON key `说明` is retained for compatibility; its value and human-readable messages are English.

Review at least:

- `messag`: license, warnings/errors, timestep, termination;
- `d3hsp`: version, parsed keywords, model statistics, contact/FSI initialization;
- `glstat`: total energy, energy ratio, external work, contact/sliding/hourglass terms;
- `matsum`: part/material/MMG momentum and energy, with any mass recovery subject to the [energy and mass checks](references/explicit-run-acceptance.md#4-energy-and-mass);
- `d3plot`: deformation, motion, penetration, free surface, and fields;
- problem-specific `rcforc`, `sleout`, and `dbfsi`: actual interface IDs, side, units, time coverage, and provenance.

For timestep collapse, investigate units, small/distorted elements, stiffness/density, contact initialization, ALE advection, and mass scaling. Do not conceal the cause with a forced timestep. If the process disappears without solver error or termination evidence, record a suspected external interruption and investigate before attributing it to numerical failure.

## 5. Bound the conclusion

`Normal termination` is necessary for a completed run, but not sufficient for physical acceptance. Nonzero contact force does not establish nonpenetration; nonzero FSI force does not establish correct materials, side, or pressure. The automatic summary checks files and logs, not physical credibility.

Before an engineering conclusion, read [Explicit-run acceptance](references/explicit-run-acceptance.md) and apply the case's predeclared thresholds. Keep runtime, input, energy, contact, FSI, visualization, and physical status separate.
