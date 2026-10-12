# Versioning and delivery

Use this shared rule for product changes, repairs, builds, rebuilds, and delivery checks, including tasks that do not enter `ddd-flow`. Review-only and diagnosis-only tasks assess the rule without writing files or building artifacts. This reference adds no design approval or publishing permission.

## Resolve the project binding

Version increment semantics live here. The project owns its version source, current version, confirmed delivery baseline, artifact naming template and output location, change-record format, delivered-content inventory, and build/check commands. Discover those from project authority and existing tools; do not embed project names, paths, or current versions in this shared rule.

Follow an explicit existing project version policy where it differs; otherwise use the defaults below. Do not silently migrate a project's version scheme. Resolve facts from the repository before asking; ask only for a material unresolved policy, compatibility, baseline, or authorization decision. A missing version policy alone does not require approval of the default rule.

## Classify the whole change

Use the three-component `MAJOR.MINOR.PATCH` format with the following milestone-based policy for projects without another explicit scheme. These defaults are not a promise of strict Semantic Versioning:

| Delivered effect | Increment |
| --- | --- |
| Bug fixes and routine improvements to existing capabilities, including logging, UI polish, performance, and usability | `X.Y.Z -> X.Y.(Z+1)` |
| A new independently usable capability or a substantial capability expansion | `X.Y.Z -> X.(Y+1).0` |
| A major milestone explicitly confirmed by the user as a major-version release | `X.Y.Z -> (X+1).0.0` |
| Tests, comments, development tooling, or other changes with no delivered-product effect | No product increment |
| Rebuild of unchanged delivered product content | Keep the product version |

Judge the delivered capability change, not commit labels or file types. Improving an existing capability does not by itself add a new capability: log redaction or a display-unit adjustment is normally PATCH, while adding a standalone import or modeling operation is MINOR. Dependency, resource, configuration, and packaging changes also require classification when they affect the delivered product.

Assess compatibility separately. An incompatible interface, persisted-data, or workflow change does not automatically trigger MAJOR under these defaults; classify its capability effect as PATCH or MINOR unless the user has explicitly confirmed a major milestone. Record the affected contract, user impact, and migration steps or the absence of a migration path. Existing design and implementation authorization gates still apply to the incompatible behavior. Approval of that behavior is not approval of a major-version release.

Use MAJOR only for a user-confirmed major milestone; do not infer one from change size, elapsed time, or reaching a round version number. Reuse an existing explicit milestone approval rather than asking again. Routine PATCH and MINOR releases need no new milestone approval. Reset lower components as shown. Apply these defaults to `0.x` too: advancing to `1.0.0` also requires explicit milestone confirmation, unless an existing project policy specifies otherwise.

Compare the complete delivery change with the latest confirmed delivery baseline for the relevant product/release line. Use the highest applicable increment once for a combined change. Internal commits, task slices, test fixes, and repeated builds do not each cause another increment. Reuse an already selected version when it covers the complete change; if a later change raises the required level, recompute from the same baseline rather than incrementing the interim number. Do not roll back an already delivered version or silently renumber an unrelated pending release.

Record which baseline and effects justify the selected version, or why no increment applies, in the project's existing change record or task report. Do not invent past deliveries, release tags, or baseline evidence from a version string alone. Preserve a project's known initial version; do not fabricate a predecessor when there is no prior delivery.

## Apply within the authorized task

For authorized implementation or repair, routine version and change-record updates under an established rule are completion work; they need no repeated design approval. Align them before final review and artifact construction. Source-only work does not create a new delivery baseline or authorize an unsolicited build; record any pending delivery checks explicitly.

Read-only requests remain read-only. A version change does not authorize changing product semantics, creating Git tags, pushing, or publishing. Those actions retain their existing authorization rules.

## Verify the delivery

Use project-owned checks to establish:

- The selected version matches the classified change and the confirmed baseline.
- The version source, applicable artifact filename, embedded/runtime version, manifest identity, and change record agree with the project's binding.
- Delivered content matches its recorded inventory, including applicable source, resources, dependencies, and configuration. The same product version must not identify different delivered product content; block delivery on such reuse or a stale manifest. Do not relabel a changed inventory under the old version to bypass the check.
- Rebuilding the same content can keep its version. Binary hash differences caused only by timestamps or other build metadata are not by themselves evidence of a product change. Distinguish product identity from artifact-byte identity using the project's inventory and build provenance.
- Required build, regression, and artifact checks actually ran against the intended content. Missing baseline or verification evidence remains explicitly unverified; do not declare a release check passed.

Reuse existing checks. When build-system changes are authorized, encode mechanically decidable conditions in that system rather than relying only on reminders; do not introduce a new release platform or broaden a source-only task. Manifests and passing tests do not replace compatibility judgment.

Completion requires an explicit increment/no-increment decision, consistent applicable version bindings, and results for the authorized delivery checks. Report the version, relevant change, artifact when requested, and any pending checks. Reuse verified evidence while its inputs remain unchanged.
