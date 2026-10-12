# Modeling and Keywords

## 1. Units and versions

Use the case's consistent unit system; assume neither SI nor a fixed scale. Check field order/options against the actual solver's official manual. Newer material may explain concepts but cannot override older card syntax. Record each nontrivial keyword decision with solver version, official source, deck choice, solver echo, visual check, and status.

## 2. Hull

### Geometry and mesh

Accept project-selected parametric, CAD, STL, or existing FE sources with source URI, coordinates, scale, and transforms. Keep physical shell, initialization surface, and coupling/contact sets separately traceable. For `open_deck=true`, inspect deck free edges, inner/outer sides, and internal air; for closed geometry, check closure and normals. Preserve smooth curvature and mesh transitions in contact regions, avoiding nonphysical sharp features and narrow strips.

Use the case's rigid shell, deformable shell, or full structure and qualified quad-dominant, all-quad, or other mesh strategy. Check duplicates, free edges, normals, aspect ratios, warpage, minimum edges, and contact resolution against case thresholds. A rigid hull may serve a case that permits it, but cannot support hull-strength conclusions. Stricter project requirements remain binding.

### Motion

Read speed, curves, constraints, and degrees of freedom from configuration. Independently estimate first contact and compare it with the motion curve and actual load onset. Choose startup behavior for the physical objective and numerical stability; no universal constant-speed or smoothing default.

## 3. Broken ice

Use the configured deterministic generator and seed. Preserve generator version, full configuration, original polygons/geometry, and manifest. Audit count, concentration, sizes, thickness, compactness, short edges, overlaps, and boundary clearance. No unrecorded manual changes to alter contact sequence.

Formal ice must be deformable; rigid ice is limited to explicitly labeled diagnostics. Choose solid layers appropriate to thickness/in-plane dimensions and avoid extreme aspect ratios or poor transitions. Materials, plasticity, pressure failure, erosion, and rate effects come from case sources and matching manuals. Erosion represents defined failure; it must not conceal penetration, negative volume, or bad mesh.

## 4. Water-air domain

For multi-material ALE/Eulerian cases, water and air share the background mesh with distinct material groups. Fraction reconstruction/advection advances their interface; do not add explicit water-air contact. Mixed-cell fractions must close and remain distinguishable in outputs.

Check version-specific sections/controls, fluid material/EOS, multi-material groups, initial fractions, hydrostatics/initial pressure, advection, history variables, boundaries, and binary/ASCII outputs. Do not prescribe a universal water/air EOS or coefficient set.

Initialize the complete background domain and case free surface/materials. Use independent closed helper geometry for open-hull interiors or other exclusion regions. Exclude fluid from hull/floe occupied volumes, then check fraction closure, deep cores, and free-surface transition cells. Helpers must not contribute physical mass, structure, contact, or FSI.

## 5. FSI

### Interface selection

Use solver-supported coupling between Lagrangian hull/ice and ALE. Separately verify fluid material selection, shell side, segment normals/quadrature, penalty/damping/leakage, IDs, outputs, and force direction. Coupling all materials and observing a nonzero force does not replace material/side evidence.

### Open hull and floes

The hull's outer medium follows local fractions, generally water below the waterline and air above. Inspect inner air independently so one-sided absolute pressure does not create spurious net load. Shared air on both shell sides requires a minimal side-specific gate; compare multiple groups, identity switching, or another validated route only when matching documentation and tests establish identity ambiguity.

Closed floes also follow local water/air fractions, not permanently assigned wet/dry surfaces. Check freeboard, attitude, vertical speed, buoyancy/weight, and material migration.

### Precontact failure with `CTYPE=5`

If irregular floes fail before physical contact, do not first blame contact or material parameters. Use bounded differential gates:

1. Locate the first failed element, time, and floe; confirm it predates geometric contact.
2. Disable only ice-ice contact for a short comparison. Unchanged failure location/time argues against contact as the direct cause.
3. Disable only ice FSI. If failure disappears, investigate coupling discretization, normals, and initialization.
4. For corners or multiple closed bodies, compare nodal/segment normals using options supported by the selected solver and coupling type. If `NORMTYP=1` removes that failure, treat it as a case-local candidate.
5. Restore full contact/FSI and check leakage, fractions, warnings, energy, and a longer interval. Absence of failure is not physical acceptance.

Configure `NORMTYP` per case/interface, not globally. Regular plates or isolated flotation gates may perform better with nodal normals; do not overwrite accepted single-floe settings based on multi-floe evidence. Interpret initial coupling spikes with mesh resolution and geometric complexity.

Strong leakage control requires leakage evidence. Hold `PFAC/FRCMIN/NORMTYP` constant and compare `ILEAK=0` with stronger control only where supported. If strong control creates a precontact interface-energy pulse while the alternative removes errors/failure and restores energy, retain that alternative as a candidate and verify deep-core fractions and wake refill over a longer gate. Neither a leak-free image nor low interface energy substitutes for the other acceptance checks.

## 6. Contact

Select ship-ice and ice-ice keywords for erosion, shell/solid type, solver version, and case needs. Check mandatory cards, surface/node set types, friction, search/soft options, and newly exposed eroded surfaces. Fix initial overlap through geometry/mesh, not compensating contact parameters. Nonzero force needs corroborating logs, energy, and multiple-state penetration checks.

## 7. Boundaries and pressure

Use consistent references for water/air, initial pressure, ambient top pressure, and open/nonreflecting boundaries. Absolute pressure requires cancellation of ambient pressure across thin shells; gauge pressure requires consistent conversion of EOS, initialization, and boundary loads. Verify static boundaries first, then distinguish waves from reflections with a no-ice hull case.

## 8. Outputs

Typical minimum run evidence is `messag`, `d3hsp`, `glstat`, `matsum`, and `d3plot`. Add case-specific FSI forces, contact/sliding energy, ALE fractions/history variables, wave probes, pressure/velocity/free surface, and ice stress/plasticity/failure/erosion/energy. Output cards show intent only: verify nonempty files, complete time coverage, correct IDs, and known variable meanings.
