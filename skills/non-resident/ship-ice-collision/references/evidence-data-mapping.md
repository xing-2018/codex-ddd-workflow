# Mapping Papers, Experiments, and Empirical Data

## 1. Traceable inputs

Convert external evidence into case input without turning a paper's parameter set into skill defaults. Each `provenance.sources` record contains `id`, `type` (`manual|paper|experiment|dataset|project|assumption`), `citation`, `uri`, `retrieved_at`, `supported_fields`, and `limitations`.

## 2. Classify adopted values

- `direct`: explicitly reported with known units;
- `converted`: reproducible unit conversion only;
- `derived`: an explicit formula or data-processing step;
- `calibrated`: experimental or numerical calibration;
- `assumed`: a project assumption where the source is silent;
- `unsupported`: insufficient basis for a formal physical conclusion.

The adapter retains original value/unit, conversion formula, target field, and source ID.

## 3. Materials and keywords

A paper may provide density, modulus, strength, or failure criteria without a complete LS-DYNA card. Keep separate evidence for physical parameters (paper/experiment), keyword fields/options (official manual), material implementation (element benchmark), and parsed input (`d3hsp`/`messag`). Do not infer missing EOS, ALE, contact, or FSI fields from an incomplete table.

## 4. Geometry and ice field

Record similarity between the source hull/specimen and current geometry, scaling, transforms, draft, ice domain, count, concentration, thickness, size distributions, generation method, seed, generator version, and geometry cleanup. State noncomparable aspects. With a different hull, domain, or boundary, limit validation to trends unless similarity and scale effects are established.

## 5. Trends and curves

Before comparing speed, concentration, thickness, or other trends, compare hull/draft, floe size/thickness distributions, water-air domain/boundaries, materials/contact, travel distance, sampling window, statistics, and raw-load processing. Where these are not comparable, report qualitative trends without claiming reproduction of absolute curves.

## 6. Example mapping

```yaml
parameter_map:
  - target: ice.material.density
    value: 0.0
    unit: <case-unit>
    source_id: <source-id>
    evidence_type: direct
    original_value: 0.0
    original_unit: <source-unit>
    conversion: <formula-or-none>
    limitation: <text>
```

This is a mapping sketch, not a conforming case object. `target` is illustrative; map it to the actual material parameter field, for example under `ice.material.parameters`. `0.0` is a structural placeholder, never a physical default. Replace and validate it in the project adapter.
