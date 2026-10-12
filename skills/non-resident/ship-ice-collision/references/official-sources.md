# Official Sources and Version Rules

## 1. Evidence priority

Start with the solver version declared by the case, then its matching local official manuals, then official Ansys/LS-DYNA examples and pages. Papers, experiments, and third-party material support physical context and parameters; they do not override keyword manuals. Never copy current syntax into an older deck without checking compatibility. Confirm the actual parser behavior through `d3hsp`, `messag`, and outputs.

## 2. Local manuals

Supply manual paths through `software.solver.manual_paths`, repeated `--manual <pdf>`, `--manual-dir <directory>`, `LSDYNA_MANUAL_DIRS`/`LS_DYNA_MANUAL_DIRS`, or standard `ansys/docu` directories beneath Ansys `AWP_ROOT*` variables. The CLI does not read case configuration automatically; pass its paths explicitly. Directory discovery checks matching PDF filenames in that directory, not every nested folder.

```powershell
python <skill-dir>/scripts/official_docs.py --manual <volume-I.pdf> locate
python <skill-dir>/scripts/official_docs.py --manual-dir <manual-dir> search "CONSTRAINED_LAGRANGE_IN_SOLID"
python <skill-dir>/scripts/official_docs.py --version-pattern R14 search "CONTACT_ERODING"
```

`R14` is a filename-filter example, not a recommended solver version. Text extraction uses `pdftotext` or, if unavailable, `pypdf`. Search results locate evidence; record volume, version, keyword/section, deck decision, and solver echo rather than copying long manual passages.

## 3. Official entry points

These are reference locations, not assertions that the pages match the installed solver or are currently reachable. When current page content or downloads are needed, verify the official source and record URL and retrieval date.

- Manuals: `https://lsdyna.ansys.com/manuals-download/`
- Explicit Technical Guide: `https://lsdyna.ansys.com/wp-content/uploads/2025/03/LSDYNA_Explicit_Technical_Guide_v1.5.pdf`
- ALE workflow: `https://ansyshelp.ansys.com/public/Views/Secured/corp/v252/en/lsdyna_ug/lsdyna_ug_ale_wkflw.html`
- Initial Volume Filling: `https://ansyshelp.ansys.com/public/Views/Secured/corp/v251/en/lsdyna_prepost_tut/ch27s02.html`
- Wave-Structure: `https://lsdyna.ansys.com/wavestructure-d85/`
- Contact Types: `https://lsdyna.ansys.com/contact-types-2/`
- Contact Modeling: `https://lsdyna.ansys.com/contact-modeling-in-ls-dyna-d3/`
- Initial Penetrations: `https://lsdyna.ansys.com/initial-penetrations/`
- Total Energy: `https://lsdyna.ansys.com/total-energy/`
- ALE History Variables: `https://lsdyna.ansys.com/ale-history-variables-2/`

## 4. Keyword groups to check

- **Structure/motion:** shell/solid sections; rigid/deformable materials; prescribed motion, velocity and curves; timestep, termination, energy controls.
- **Contact:** case-selected eroding surface-to-surface, single-surface, or other route; contact/solid controls; mandatory cards, surface/node sets, soft options, friction.
- **ALE/FSI:** fluid materials/EOS; ALE/multi-material controls; initial fractions/hydrostatics; Lagrangian-in-solid coupling; material groups, side/normals, leakage; boundaries/pressure. Inspect identity switching only when the version and case require it.
- **Outputs:** global/part energy and mass; contact/FSI forces; binary extent/history variables; ALE fractions, probes, required ASCII files.

## 5. Evidence record

```text
keyword:
solver_version:
official_source:
deck_decision:
d3hsp_or_messag_check:
visual_check:
status: pass | fail | pending
```

Without a matching manual or solver echo, leave the decision `pending`; do not fill missing fields from memory.
