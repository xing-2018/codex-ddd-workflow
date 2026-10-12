# Preview contract

Use the smallest preview that lets the user judge the real design decision. Distinguish the artifact the user can operate from evidence used to inspect it. `ddd-design` owns the preview mode and approval threshold. A routed specialist may produce or verify evidence but cannot lower the threshold or approve the design.

Before creating or modifying preview files or supporting evidence, apply [design approval](../../ddd-flow/references/design-approval.md): present the concrete preview plan and identify explicit write authorization or valid bounded autonomy. A request for UI design, a format conversion or feedback alone does not grant that permission. Resolve uncertain interpretations before dependent writes; the operable-preview requirement does not bypass approval.

## Preview modes

| Design question | Minimum review artifact and verification |
| --- | --- |
| Local information hierarchy, grouping, density or wording with settled interaction | Rendered static screen at the target size |
| A complete user workflow or new interaction design | Operable prototype with core inputs, actions, feedback and results connected end to end |
| Tabs, panes, selection persistence or progressive disclosure | Clickable or runnable preview |
| Validation, loading, stale data, success or failure in the core workflow | Runnable transitions with visible feedback; separate rendered states may supplement but cannot replace the affected interaction |
| Resize and overflow behavior | Runnable target-platform preview exercised at representative sizes |
| Modification of an existing UI | Current-state evidence plus a proposed preview at the interaction level required by the affected workflow, using the existing visual language |

A prototype request defaults to an operable path through core inputs, actions, feedback and results unless the question is clearly limited to settled layout or visuals. Current-state captures and screenshots can support comparison but cannot replace a workflow artifact; honor a user restriction on screenshots.

Before expanding a candidate, identify what the user needs to do in the preview to decide whether the interaction works. If a material choice about placement, sequence or input method requires hands-on evaluation, start with one representative, complete task path. Show the choice in the product context and request focused feedback before adding variants. If phrases such as "run the case" could mean an interactive walkthrough, live computation or read-only replay, resolve that difference before building the more costly path. User feedback on one aspect does not settle unrelated choices; a formative check is distinct from final design approval.

## Independent HTML delivery

Deliver a browser-openable HTML design artifact for both web and desktop products through the [single project prototype](#single-project-prototype-layout). Keep all pages in that application with shared navigation, theme and in-memory state. A settled local visual question may use a static screen within the same artifact; it does not create another delivery format or location. The HTML entry may contain its styles, scripts and representative data, or load packaged local assets, while preserving direct offline opening. No dependency installation, build command, product source module, backend, remote font, CDN or network request may be required for the agreed interaction path. If an authoring tool is useful, deliver its independent output. A local URL ending in `.html` does not by itself establish independence.

Reuse the affected page's information architecture, labels, controls, theme, relevant assets and interaction conventions from actual evidence. Reuse means preserving that design context. Prefer read-only authoring-time reuse of suitable production presentation components, renderers and assets when this avoids a divergent reconstruction; a faithful reconstruction remains valid when reuse is unsuitable. Mock the API/store/authentication/native boundary with scenario-consistent data and visible states, retaining relevant DTO identities, units and relationships. Only interface state and presentation logic may run in the artifact, not imported domain algorithms or business handlers. Deliver the independent built output: no production checkout, source imports, authoring toolchain or services are needed to open it. Do not change production files merely to build the preview. If real execution is explicitly requested, separate that work through the scope routing below.

For a desktop target, read its default window dimensions and platform conventions from design or configuration. A larger browser must show the product window with surrounding space, not stretch it to fill the viewport. At smaller sizes preserve the target's intended behavior through deliberate scrolling or a clearly identified scaled preview; do not confuse browser viewport dimensions with product window dimensions. If no authoritative size is recoverable, state a reasonable provisional size for review. Map proposed controls to feasible target-native controls; HTML styling does not prove native focus, keyboard or widget behavior.

### Interface-only interaction boundary

Core controls must perform the interface task: navigation, selection, edits, validation, draft confirmation/cancellation, filtering and visible feedback change in-memory UI state. Business outcomes come from embedded examples or predefined states consistent with the scenario, units and labels; arbitrary edits do not trigger a real domain calculation. Apply the [stable-layout and content defaults](ui-design.md#stable-layout-and-task-focused-content). Put simulation scope, authoring details and provenance in the required README by default; do not add a banner, card, footer or review controls to the product surface merely to explain the prototype. If a realistic action would otherwise mislead the user about its result or data, show the smallest necessary disclosure in the approved feedback or review surface while preserving the product layout. Keep required validation, errors and action feedback operable and visible; documentation does not replace them.

| Product action being designed | Prototype behavior |
| --- | --- |
| Open or import | Show a simulated selection dialog and load a chosen embedded example; do not launch an OS file picker or read user files. |
| Save or cancel | Confirm or discard a draft in memory and show the corresponding feedback; do not write files or persist browser data. |
| Export | Demonstrate confirmation, progress, success or failure using UI states; do not serialize an output file or trigger a download. |
| History | Select from embedded examples and current-session snapshots; do not use localStorage, sessionStorage, IndexedDB, cookies or other durable storage. |
| Calculate or submit | Show predefined loading, result and failure states tied to the selected example; do not invoke domain algorithms, product modules, APIs or services. |

These controls remain operable; disabling them or replacing them with generic “not implemented” alerts does not demonstrate their interface flow. The delivered prototype must contain no business file access, output-file generation, persistent storage or live service integration, even if described as local, optional or sample-only. Use UI state transformations for the visible interaction, not a feature implementation behind it. Creating and checking the HTML artifact, and loading its packaged styles, scripts, images and embedded example data, remain permitted delivery work. This boundary concerns the prototype’s runtime business actions, not reading design evidence or writing the requested design artifact.

### Multi-page state and authoring

Keep routes in the same application and retain the approved state lifetime across navigation: selected entity, drafts versus applied queries, cancellation and stale-result availability. Separate page source files for exclusive authorship without resetting state on return. One coordinator owns shared navigation/theme/build integration under [checkout coordination](../../ddd-flow/references/execution.md#shared-checkout-coordination). Do not embed old complete HTML snapshots as a substitute for current shared components. Approval covers the actual entry and dependent resources; production code and an older prototype are observational references where they conflict with the latest approved design.

### Native browser review and annotations

The project prototype must support review in the Codex in-app browser, with native annotations covering all in-scope visible design content. Use the [capability-based viewing route](#scope-routing-and-viewing-tools) to open the actual delivered entry in that host. A successful external-browser or controlled-adapter check cannot certify in-app opening or native annotations. Keep annotation tools in the host; do not add a replacement annotation toolbar, comment store or review overlay to the product surface.

Before signoff, inventory the prototype's pages/routes and material states, including dialogs, popovers, validation, loading, empty and disabled states, scrollable content and visualizations. For each content region, identify the visible review target and how it is reached. Prefer addressable elements in the application document. SVG, canvas, images or embedded content must still expose the intended review target at the granularity the design decision needs; selecting an outer container is insufficient when feedback concerns an inner control, label or plotted feature. Preserve the approved rendering and interaction rather than removing content or flattening an operable view solely to make selection easier.

Check expanded menus and individual options, not just their collapsed trigger. A native control can expose a popup outside the annotatable application document: if real host evidence shows its options cannot be selected for comments, represent that popup with addressable application-document elements in the HTML prototype. Preserve the control's label, choices, value, availability, placement and task semantics; provide appropriate accessible roles, focus, keyboard navigation, confirmation and dismissal. Do not let loss of page/window focus to the host annotation toolbar alone collapse the review target. Check that the expanded targets remain reachable during native review and that normal interaction still works afterward. This is a presentation repair to the independent prototype, not a blanket ban on native controls or evidence of target-platform native behavior; report any remaining fidelity or accessibility gap.

Exercise the real host path: enter annotation mode, select the intended visible target, create and submit a native comment, then confirm that it reaches the current conversation with the correct page, target and context. Check coverage across every inventoried page and material state, exercising each distinct target/rendering mechanism and every region with suspected selection failure. A toolbar being present, a successful click, an element ID, a DOM hit test, a screenshot or one successful comment does not establish complete annotation coverage. Check scrolled or overlaid targets where applicable, and verify that annotation mode can be exited and the interface task remains operable. Do not infer universal iframe support or failure from one observation.

Record the entry and artifact identity, exercised routes/states/targets, actual comment-return evidence and remaining gaps in the existing task evidence owner. When the permitted API does not expose host annotation controls, hand the operable entry to the user for the native selection-and-comment step; do not inject a substitute or bypass host restrictions. Missing host access or comment-return evidence leaves that operation unverified, and an unselectable in-scope region leaves annotation acceptance incomplete. Report the exact gap, preserve the review path for repair and feedback, and do not certify the prototype as fully annotatable.

### Conversion and fidelity repair

Changing the delivery format or runtime preserves the accepted design within the user's requested scope. Before conversion, recover the reference revision and its in-scope scenarios, navigation, controls, material states, information hierarchy and dimensions. Use their existing owner or a concise task note; do not create a parallel specification. Distinguish explicitly requested simplification from format conversion. A formative path used to resolve an open choice does not replace established scenario coverage. Do not silently drop cases, disable previously usable controls or replace a selectable view with an inert illustration to make the artifact independent. Preserve their visible interaction semantics using the interface-only boundary; this does not preserve the underlying business implementation. Replace legacy file/service handlers with UI simulation in the delivered artifact, and do not carry a functional server or launcher into its bundle as an optional tool. Preserve historical reference files unless their removal is separately authorized.

Predefined sample outcomes replace the business engine while preserving the interface interaction contract. A synthetic view must expose the meaningful entities and choices used by the scenario, retain selected identity, and connect selection to the corresponding input, feedback and result. Where present in the reference, preserve draft versus saved values, save/cancel behavior, in-memory selection retention, dependent-result invalidation and control availability. Fixed picks or fixed parameters cannot stand in for choices the reference lets the user make. If a material capability cannot be represented within the permitted artifact, make that specific gap and its consequence reviewable; obtain a scope decision before treating the reduced artifact as the replacement. A real backend or file operation is not a missing UI capability when its selection, confirmation and outcome states are represented.

Compare before and after using the same scenario, sample data and interaction state, with matching product-window dimensions, browser viewport and preview scale where applicable. For each materially different in-scope path, exercise its retained controls and transitions in the delivered artifact and inspect paired renderings at corresponding checkpoints. Check density, hierarchy, labels, available actions and selection/result relationships, not only the outer column layout. Record intentional differences against the approved change; repair unexplained losses. If the reference cannot be reopened or lacks a matching state, use available evidence and identify the exact comparison gap. Different-case screenshots or a successful offline smoke check cannot establish conversion fidelity. Preserve the active reference until comparison and review are complete.

### Scope routing and viewing tools

An explicit request for real file operations, persistence, computation or service integration is a separate functional experiment or implementation task: return it to `ddd-flow` with its existing authorization and intended outcome. Do not implement it inside this UI design artifact or treat generic approval of the prototype as approval of the feature. A request solely to document current native behavior may use authorized native evidence under its own verification contract. Historical approved references remain evidence; an existing prototype used for current design work follows the [migration requirements](#existing-project-migration).

Inspect an application or native harness as supplemental evidence when native behavior materially affects the decision and tool permissions allow it. If HTML cannot answer that question, explain its limit and seek the user's choice before replacing the HTML design deliverable. Correcting visual fidelity must retain the operable HTML task path; screenshots and launchers cannot replace it.

Select the viewing route from the permitted tool's documented capabilities or an observed limitation before opening the artifact. Separate an unsupported URL scheme from an unavailable browser: changing the scheme cannot restore a missing browser. Use known capability evidence directly; do not send a `file://` URL to a tool known to support only HTTP. If an attempted route is refused, do not repeat the same unsupported route or declare the artifact unviewable solely from that refusal.

For an available HTTP-only viewing tool, serve the same independent prototype files through a task-scoped static server bound only to loopback, within the authorized preview and process scope. Open the actual supported HTTP URL in that tool. Keep the server limited to those packaged files, with no business computation, data or file APIs; it is a viewing aid, never a required runtime dependency or another prototype. Reuse a suitable authorized server when available, preserve unrelated services, and manage any task-created process through viewing and cleanup without ending the review path prematurely. Report a missing server or process authorization as that specific gap rather than a defect in the HTML.

Separately verify direct offline opening, with network disabled and services absent, using another expressly permitted method if available; an HTTP viewing pass is not offline proof. If no permitted browser or offline method is available, identify the missing capability and the unverified operation precisely. Do not bypass tool restrictions, change browser or Codex configuration, or replace the required operable HTML with screenshots. Provide the actual local HTML entry as well as any temporary viewing URL and its availability, and keep the prototype available for feedback and revision.

## Required evidence

- Open the delivered HTML directly with network access disabled and product/preview services absent; exercise the complete in-scope interface paths, including simulated open/save/import/export. Observe file-picker events, file access, downloads, persistence and service requests while exercising the controls; inspect the handlers for business I/O or computation that a successful click or offline check could miss. Verify draft and current-session state behavior without storing it across reloads. Do not stop unrelated user services to perform this check. A temporary static-server pass alone does not prove direct-open behavior.
- Render an error, loading, empty, partial, stale or advanced state only when it materially affects the approved workflow.
- Use the same representative domain scenario as requirements and technical design. Check input meaning, operation, computation/data semantics, state, feedback and result against their existing owners. Label simulation and unresolved semantics; a fixed example does not validate the actual domain algorithm.
- Render the default state and keep important input, action, status and output relationships visible at the product's intended default size. Inspect larger and smaller browser viewports separately; verify that a desktop preview keeps its window dimensions in the larger viewport.
- Keep required information reachable when content does not fit through deliberate panes, tabs, scrolling or resizing.
- Show advanced or rare controls only on demand.
- Avoid repeating the same explanation in several visible regions.

## Approval evidence

Approval must refer to a rendering the user can inspect. For a scoped static visual question, this may be a rendered screen. For a workflow, provide an operable entry point and use screenshots only as permitted supplemental visual evidence. Source files, widget trees, Markdown tables and prose may supplement but cannot replace the required preview.

When presenting the preview, state:

1. what is real and interactive;
2. what is simulated;
3. which requirements and states are visible;
4. which material direction the user is approving.

For an interactive prototype, provide its usable entry point and the exercised task path, including the observed feedback and result. Build success, screenshots or an unexercised application link do not prove that path works. If a permission or capability restriction prevents verification, report that exact gap without calling the prototype verified.

Revise the project prototype in place. If comparison is needed to resolve a real trade-off, represent the alternatives inside that application rather than maintaining separate prototype entries.

## Prototype lifecycle

Before files are created, resolve the project root, covered write scope and any conflicting user or project instructions. Every written interface prototype, including formative exploration and local static previews, uses the single project layout below. Screenshots, logs and verification output belong in the project's authorized task-scoped evidence location, including ignored scratch, rather than in another prototype bundle. Use memory-only analysis when writes are not permitted. An OS temporary or other project-external evidence destination requires explicit authorization covering its resolved target and action. Prototype creation grants no broader persistence or production access. If a higher-priority user or project instruction conflicts with the fixed layout, report the exact conflict and obtain the governing decision before dependent writes; do not silently retain another path.

Keep the single review prototype available through review and revision. Preserve approved revisions through recoverable version-control identities or authorized reference copies; historical evidence is not another actively maintained prototype. Keep representative data, simulation limits and reopening instructions with the current entry, and record its reviewed identity in the existing design owner within the authorized write scope. Do not leave an approved design pointing only to deleted draft files.

### Single project prototype layout

New and existing projects must maintain exactly one evolving interface prototype at `docs/design/prototypes/`, relative to the resolved project root. Use this layout for every written prototype; there is no standalone single-HTML delivery exception. Do not add a project-name, prototype-identifier, feature, task or variant directory between this root and the review entry. Add pages and representative paths within the same application, preserving the approved surrounding workflows during local revisions.

```text
docs/design/prototypes/
  index.html       # directly openable offline interface review entry
  README.md        # review task, simulation limits, entry and reopening instructions
  交互设计.md       # approved UI design owner, or a pointer to its existing owner
  assets/          # packaged static images, styles or scripts, if any
  examples/        # supplemental example files, if any
  src/             # optional authoring source; built entry has no runtime dependency on it
  tools/           # optional maintenance or verification tools, never runtime dependencies
```

Keep the review entry, required documents, authoring source, necessary assets, representative mock data and any reproducible build instructions in Git. Do not add raw-data dumps or screenshot directories to the prototype bundle. Authorized evidence captures remain in the project's task-scoped evidence location. Existing paths are not an exemption from this layout; migrate the prototype involved in the authorized work as described below, preserving historical references and unrelated files.

`index.html`, `README.md` and `交互设计.md` are required even when the HTML entry contains all presentation code and example data. Create the listed optional subdirectories only when they have content. Keep sample data needed by the direct-open interaction embedded in `index.html` or packaged without network/file API dependencies; `examples/` is for supplementary evidence, not a required fetch target. If another document already owns the UI design facts, make `交互设计.md` a concise pointer to that owner and reviewed revision rather than duplicating its specification. Keep engineering or functional experiments outside this interface artifact, with their own stated launch and behavior contract; a server, build dependency or business handler never becomes part of the independent HTML deliverable through colocation.

### Existing-project migration

On the first authorized prototype creation, modification or directory reorganization in an existing project, inspect the current entries, approved reference revisions, relative dependencies and inbound links. Include migration of the prototype involved in that work to the fixed layout in the same concrete plan and covered write scope; an already approved plan covering that migration needs no separate per-file gate. A read-only task reports the nonconforming paths without moving files. Do not sweep other projects or historical archives, and do not infer migration permission from a prototype's existence. A narrower write scope or a conflicting location rule stops only the dependent migration until the user resolves it.

Bring the in-scope pages, cases and states into the single application; do not introduce parallel maintained entries or discard approved choices to fit the directory. If legacy references conflict about the approved design, resolve that semantic conflict before dependent consolidation. Preserve historical reference files and unrelated user data; their removal requires separate authorization. Maintain a recoverable reviewed revision while updating the current entry and all affected links and reopening commands.

For a directory-only migration, preserve the approved interface and each artifact's behavior contract. Open each affected entry by its actual launch mode and exercise the paths whose dependencies moved; verify that the new `docs/design/prototypes/index.html` opens directly offline. Apply the conversion and fidelity checks when the delivery format also changes. A directory move does not approve a design change or convert a functional experiment into an interface-only prototype. Report any unavailable operation evidence without certifying migration completion.

Before delivery, inspect the actual paths of the entry, required documents, resources and supporting output, including Git-ignored files and tool-generated sidecars; a clean Git status does not establish location compliance. Confirm the single maintained entry and fixed layout, repaired references, recoverable approved revisions and separate evidence location. Correct task-created files outside permitted locations within the authorized scope, preserving user data. If the required files or retention are outside the write scope, report that gap instead of substituting a temporary standalone HTML delivery. Remove superseded task drafts only when their cleanup is authorized and the review reference remains recoverable; preserve user data and the active review artifact.
