# TypeScript

Read only for changed TypeScript. For a new TS project, strict is a starting recommendation; existing projects retain their tsconfig during ordinary feature work. Validate external unknown values through existing project methods. Avoid unsupported as assertions, non-null assertions or any that hide an actual boundary defect; explain a necessary local escape's scope and evidence. Use inference when clear and complex generics only for real reusable semantics.

Represent mutually exclusive states with discriminated unions rather than booleans permitting impossible combinations. Evaluate noUncheckedIndexedAccess and exactOptionalPropertyTypes within project constraints; do not enable them unconditionally or manufacture assertions to make migration pass. Type checking may require the affected project's full context, not only diff files.

Reuse the [shared web guidance](typescript-javascript.md) already loaded; React is conditional on actual use.

Use a mature stable compiler compatible with the project and its dependencies; the current validation target is TypeScript 5.9.x. Do not require a newest major release for ordinary work. Type acceptance or an assertion does not validate external JSON at runtime. Features such as deferred imports also require target-runtime or bundler support; retain the project's lock and module/target declarations.
