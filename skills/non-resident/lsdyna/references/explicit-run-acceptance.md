# LS-DYNA Explicit-Run Acceptance

## 1. Sources and versions

Use official manuals matching the actual solver. Examples are templates: review units, materials, boundaries, contact, and simplifications before reuse. Current web syntax does not override an older deck format. Record the solver banner, precision, SMP/MPP, `ncpu`, command, deck hashes, and timestamps.

Reference entry points (verify when consulting current content):

- `https://lsdyna.ansys.com/manuals-download/`
- `https://lsdyna.ansys.com/wp-content/uploads/2025/03/LSDYNA_Explicit_Technical_Guide_v1.5.pdf`
- `https://lsdyna.ansys.com/total-energy/`
- `https://lsdyna.ansys.com/contact-types-2/`
- `https://www.dynaexamples.com/`

Version-specific observations below were inherited from earlier work. Their raw runs/manuals are not bundled here; treat them as `HISTORICAL`, not independently reproduced evidence or cross-version defaults. Confirm the applicable manual and current-run behavior before adopting a setting.

## 2. Before execution

- [ ] Explicit, consistent units for all materials/loads.
- [ ] Solver version matches the deck's manual.
- [ ] All `*INCLUDE` paths resolve from the run directory.
- [ ] Node, element, part, material, section, set, and interface IDs are consistent.
- [ ] No degenerate mesh, negative volume, or unacceptable minimum-timestep elements.
- [ ] No obvious initial penetration or missing/excess constraints.
- [ ] Strictly increasing `*DEFINE_CURVE` abscissae; retain a hold/ramp junction only once. Older readers have reported `Error 20445` for duplicate times.
- [ ] Justified hourglass, timestep, mass scaling, termination, and output settings; required `DATABASE` cards explicit.
- [ ] Manifest exists before launch, recording entry SHA-256, input inventory paths/sizes/hashes, solver, command, directory, and start time. The runner inventories `.k/.key/.dyn` under the run directory, not every possible external include; separately account for omitted dependencies. A reconstructed manifest is diagnostic only.
- [ ] Any reader/initialization gate uses a separate directory and matching executable; see [Version-specific execution notes](#9-version-specific-execution-notes).

## 3. Runtime integrity

Retain the deck/includes, `run.log`, `run_manifest.json`, `messag`, `d3hsp`, `glstat`, `matsum`, and required `d3plot`, `rcforc`, `sleout`, `dbfsi`, or other outputs. Check license, errors/warnings, target time, timestep, CPU/elapsed time, and contamination by old results.

## 4. Energy and mass

Compare total energy with initial energy plus external work, phase relationships of kinetic/internal energy, and contact/sliding, hourglass, damping, rigidwall, and interface energy. Audit added mass and its interval, per-part mass/erosion, and energy through `matsum`. Thresholds belong to the case.

Where direct mass is absent, use `mass_i=momentum_i/mean_velocity_i` only if the same material/MMG block's `x/y/z-mom` and `x/y/z-rbv` are verified as momentum and mean velocity. Use components above a predeclared velocity floor, retain positive finite ratios, take their median, and report relative dispersion. Zero or unusable states remain unavailable; do not interpolate, forward-fill, or assign zero mass.

Historical guidance cites R10.0 Volume I Appendix E (`xrbv=xm/totalm`, `yrbv=ym/totalm`, `zrbv=zm/totalm`). Check version, labels, grouping, and component consistency before applying it; report text precision and threshold uncertainty.

For AMMG switching, map and sum identities by physical material before conservation checks. ALE aggregate and MMG child rows are different views, not additive masses. Recovered mass does not replace fraction closure, integrated volume, or boundary flux. Fraction integration measures occupied volume; without density weighting and flux audit, small volume drift cannot refute excessive mass drift.

## 5. Contact

Verify types, sets, and fields in `d3hsp`; initial penetration/warnings; interface IDs and complete intervals; and multi-state evidence for penetration, sticking, chatter, missed edges, and eroded surfaces. Nonzero force shows numerical response, not correct contact geometry.

For `rcforc`, confirm target contact input ID from deck/legend and select one slave/master side. Do not combine unrelated IDs at the same time or double-count action/reaction. Live CSV/JSON/plots use one byte snapshot with size/SHA-256 and the label `interim`; regenerate a `final` package after termination.

## 6. ALE/FSI

Check material groups, initial fractions and closure, Lagrangian normals, coupling side, material sets, and interface IDs. Verify fractions in occupied structures, old/new locations, and boundaries, alongside interface energy, leakage, negative advection volume, material mass, and reflections.

Separate the deep structural core from the penalty-coupling interface band. A core exclusion threshold cannot automatically be applied to adjacent mixed cells. For the moving interface band, report maximum fraction, unique exceeding cells, consecutive duration, integrated mixed volume, and recovery. A transient interface spike with an excluded deep core does not establish sustained flooding. Region widths must follow the case's predeclared mesh/discretization basis.

Before interpreting plot pressure, determine whether it comes from initial stress, EOS state, or time-dependent boundary loading. A `t=0` state may precede applied hydrostatic stress such as `*LOAD_SEGMENT_SET`. Compare `-trace(stress)/3` cellwise with the deck's hydrostatic/boundary function; use the first verified loaded positive-time state for dynamic differences and record its time. Initial fraction/geometry evidence may still use `t=0`; do not conflate the baselines.

Match times across `d3plot`, `dbfsi`, and `rcforc`, recording nearest-sample offsets rather than comparing unrelated final rows. Map `dbfsi` surface IDs from current `*DATABASE_FSI` cards or headers, not assumed `1/2`. Integer-ID data rows differ from floating continuations; `0.0000E+00 ...` must not become surface 0. Record actual surface, structure/AMMG, and sampling interval. Total force cannot replace material, side, or per-interface evidence.

For R10 erosion, identity switching, or leakage settings, consult [Version-specific execution notes](#9-version-specific-execution-notes) and the actual manual before testing.

## 7. Visualization

Inspect motion for nonphysical deformation, rigid drift, penetration, and element distortion. Fringe images need variable, part/material group, units, state, and legend. Keep command files for batch images and views/judgments for manual images. Separate diagnostics from acceptance evidence. Never infer a batch command from a GUI menu label.

Numbered `d3plotNN` files need not be equal in size. A final tail may be shorter, but an active highest-numbered file may grow later despite stable length/`LastWriteTime` or a readable state. Reader success permits time-labeled live diagnosis, not an immutable snapshot. Wait for the next numbered file, normal completion, or equivalent rotation/closed-handle evidence. Neither fixed byte size nor short-term stability proves closure.

See the version notes for LS-PrePost 4.5 selectors and full-restart visualization.

## 8. Decision

```text
runtime_status: pass | running | incomplete | fail
input_status: pass | fail | pending
energy_status: pass | fail | pending
contact_status: pass | fail | pending
fsi_status: pass | fail | pending
visual_status: pass | fail | pending
physical_status: pass | fail | pending
```

Set physical `pass` only after every case-required gate passes. The inspector's `running` means the manifest still says running and no checked failure was found; required files may still be missing. Confirm process existence and output progress independently. `incomplete` means evidence does not establish accepted completion, a running manifest, or a detected failure under the inspector's rules; missing required files outside a running manifest are `fail`.

A missing manifest limits provenance even when logs yield runtime `pass`. The inspector is not an approval authority and always leaves physical status pending. Its legacy JSON key `说明` is preserved; messages are English.

## 9. Version-specific execution notes

### Reader and short initialization

Historical Ansys 19.2 bundled LS-DYNA SMP double R10.1.0 observations report that `mcheck=y` completes keyword reading, fraction/contact initialization, and 10 cycles before normal termination. It may write large `d3hsp/d3plot` files; do not call it read-only or substitute it for target-duration/physical acceptance. Copy the complete deck/include set into a separate diagnostic directory and use `-ModelCheck -RequireNormalTermination` with the matching solver.

### External interruption and full restart

If a process disappears without solver errors or termination, record a suspected external interruption. Preserve the original directory and check last output time, processes, Windows Application/System events where applicable, restart history, and memory pressure before assigning a cause.

Inherited guidance cites R10 Volume I, Getting Started, pages 2-20 through 2-21 for `LS-DYNA R=D3DUMPnn`. For an unchanged model, verify that route in the matching manual, use the same solver and compatible parallel settings, copy the dump into a new directory, verify its hash, and record separate command/provenance plus checkpoint time/cycle. The bundled runner has no restart flag; use a verified project command. Preserve primary/restart originals and remove overlapping physical times only in derived postprocessing. Reading the dump successfully is not physical acceptance.

Restart text outputs may be `messag01`, `d3hsp01`, etc. Map nonempty numbered variants to required base outputs while preserving actual filenames in evidence.

### Restart plot families and LS-PrePost 4.5

Historical LS-PrePost 4.5 use found that opening `d3plotNN` directly may fail when a restart lacks an unnumbered entry. In a separate snapshot directory, retain primary `d3plot` through the slice before the restart's first index, then append the restart family. Use only closed slices with the expected reader-visible times; exclude any active tail according to the closure rules above. Same-volume hard links save space only when the source is closed and will remain unchanged; links are not independent immutable copies.

Open the unnumbered `d3plot`. For the applicable 4.5 workflow, validate with `c=<absolute-command-file> -nographics`, include `exit`, confirm `Finished reading model`, and inspect `lspost.msg` for `Invalid command` or `Unknown command`. Record slice mapping, source directories, hashes, and cutoff time in a snapshot manifest or README.

Historical 4.5 notes report `fcomp history N` rejected as `Invalid command fcomp!` under `-nographics`. A later nonempty `print png` output establishes only rendering, not a selected AMMG fraction. Preserve the failed log and reject that image as fraction evidence. If a verified cfile selector is unavailable, use a qualified background reader image with slice/state, array mapping, color scale, units, and hashes; label it non-native to LS-PrePost.

### R10 erodible solids and identity switching

- Historical Ansys 19.2 bundled R10.1.0 reader evidence reports `Error 10956: Only part or part set can be used for slave side` for `*CONSTRAINED_LAGRANGE_IN_SOLID`, `CTYPE=5`, `SSTYP=2`. Use part/part sets for that combination unless the target reader establishes otherwise; a field table alone is insufficient.
- For `*ALE_FSI_SWITCH_MMG_ID`, verify monitor normals and `XOFF` direction. Historical guidance suggests at least two local ALE widths for `XOFF` and identical MAT/EOS for pre/post-switch dummy AMMGs. Verify against the actual topology/manual; `XOFF=0` can switch still-occupied interior material prematurely.
- Do not treat `NQUAD`, `FRCMIN`, `PFAC`, `ILEAK`, or `PLEAK` as monotonic leakage controls. Inherited R10 guidance discusses increasing `NQUAD`, decreasing `FRCMIN`, or tuning within `0<PLEAK<0.2`; confirm option validity, change one principal factor, and compare both phases' leakage, structural drift, FSI forces, mass, and energy.
- Historical same-MAT/EOS mapped water/air AMMG tests reported `Error 41267` (negative EOS denominator) with `ILEAK=2`. A short gate using the same topology/version is required before extrapolating ordinary-case settings.
