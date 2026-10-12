# Case Data Interface

## 1. Ownership

The skill owns the reusable workflow and the generic case schema, template, and validators. This interface applies to workflows that explicitly use it; it does not replace a repository's native configuration contract. The project owns facts, geometry, materials, parameters, paths, current status, and evidence. Core field names use English snake_case; user-supplied descriptions may follow project language. Paths may be absolute, relative to the configuration file, or project-defined URIs. A schema constrains the interface, not physical acceptance.

## 2. Files and initialization

```text
assets/case-config.schema.json
assets/case-config.template.yaml
scripts/init_case_config.py
scripts/validate_case_config.py
```

The current `schema_version` is `1.0`. YAML and JSON are supported; YAML requires PyYAML.

```powershell
python <skill-dir>/scripts/init_case_config.py --output <project-path>/case-config.yaml
python <skill-dir>/scripts/validate_case_config.py --config <case-config.yaml> --allow-draft
```

Template `null` values await case input. `--allow-draft` downgrades missing required values to warnings; it does not waive other shape or cross-field errors. Before production execution, fill the required values, omit `--allow-draft`, and use `--check-paths` where applicable.

## 3. Project adapter

For repository engineering or diagnosis, use the project's documented native loader and checks. Do not pass a native configuration to this validator unless its conformance or adapter binding is established, and do not interpret missing generic fields as missing engineering parameters.

When an independent case workflow needs this interface and native project data does not match it, identify a real, project-owned adapter entry point and its supported schema version:

```text
project facts/configs
  -> project-owned adapter
  -> normalized case-config.yaml/json
  -> ship-ice-collision skill
```

The diagram and CLI below describe an adapter contract, not an installed implementation. If no adapter is provided, report the integration gap and continue independent authorized work; creating an adapter requires corresponding implementation scope. The adapter must:

1. Use project-selected input paths and authorities.
2. Produce output conforming to `case-config.schema.json`.
3. Retain source IDs, transformations, and assumptions.
4. Leave unknown physical parameters unresolved rather than silently inventing them.
5. Produce stable output for identical inputs.
6. Record its version and output hash in provenance.
7. Stay in the project, outside the reusable skill.

An example CLI shape is:

```powershell
python <project-adapter> --source <project-config> --output <normalized-config>
```

## 4. Field groups

| Group | Contents |
| --- | --- |
| `case` | ID, title, mode, status, units, work/results directories, report path |
| `software` | Executable, version, precision, parallel mode, resources, manuals, preprocessors/postprocessors |
| `geometry` | Hull source, structural model, open/closed geometry, transforms, mesh strategy and thresholds |
| `ice` | Enablement, deterministic generator/seed, domain, count, concentration, sizes, thickness, mesh, material, failure |
| `fluid` | Method, domain, mesh, free surface, gravity, materials/EOS, pressure reference, initialization, boundaries |
| `coupling` | Water-air interface, hull/ice FSI, ship-ice and ice-ice contact |
| `run` | Motion/speed curve, expected events, termination and relevant time scales |
| `outputs` | Required files, intervals, contact/FSI loads, fractions, waves, structural fields |
| `acceptance` | G0/G1/A1/A2/B1/B2/C enablement, thresholds, sample times, regions, required evidence |
| `provenance` | Manuals, papers, experiments, datasets, project authorities, adapter, assumptions |

Schema values such as `cfd_coupled` describe possible project data, not a supplied implementation. This skill's detailed fluid procedure covers multi-material ALE/Eulerian cases. Other routes need their own verified project implementation and applicable acceptance evidence.

## 5. Extensions and versions

Use `extensions.<namespace>`, for example `extensions.company_x`, for project-specific additions. Do not add single-project fields to core objects. Breaking schema changes require a major schema version; compatible additions require a minor version. Adapters declare supported schema versions. Stop on an unknown major version rather than guessing; the current validator accepts only `1.0`. Skill package versions in `VERSION.txt` are separate from the case schema version.

## 6. Validation and output compatibility

The validator loads YAML/JSON, checks JSON Schema when `jsonschema` is installed, performs built-in shape/required-value checks, handles draft values, optionally checks local paths, and checks cross-field constraints such as event timing, formal deformable ice, and raw-load preservation. Missing `jsonschema` produces a warning and leaves only built-in checks; do not describe that as full Schema validation. Nonlocal URIs are not verified by `--check-paths`.

It outputs `pass|fail`, errors, warnings, and manual checks; exit status is 0 or 1 respectively. The legacy JSON key `说明` remains unchanged for consumers; its explanatory value is English. CLI options, configuration keys, status values, and finding paths remain stable. Diagnostic wording is human-readable text, not a machine identifier.

Interface success does not establish that geometry, mesh, keywords, coupling, or physical results pass their stage gates.
