---
name: "playwright-interactive"
description: "Debug and visually validate local web or Electron applications through a persistent Playwright session in `node_repl`. Use for iterative UI debugging, functional interaction checks, responsive or viewport QA, screenshots, and Electron window behavior. Do not use for ordinary web browsing or without explicit authorization to control the target UI."
---

# Playwright Interactive Skill

Use a persistent `node_repl` Playwright session to debug local web or Electron apps, keep the same handles alive across iterations, and run the applicable functional and visual checks without restarting the whole toolchain unless the process ownership changed.

## Preconditions

- The `node_repl` JavaScript tool must be callable. Its tool id is typically `mcp__node_repl__js`.
- If it is not exposed directly, use tool discovery for `node_repl js`. Do not treat a deferred tool as unavailable until discovery has been attempted.
- If Playwright is installed in a workspace-specific `node_modules` directory that the persistent kernel cannot resolve, add that absolute directory with `mcp__node_repl__js_add_node_module_dir` before importing `playwright`.
- Interactive browser or Electron control requires explicit authorization in the current request. A request to interactively debug or QA that target counts; a read-only diagnosis or review does not.
- Work within the current session's effective tool permissions and the authorized target operations. A sandbox mode name such as `workspace-write` alone does not establish whether a dependency check or connection is available; disabling sandboxing is not a prerequisite. Perform authorized checks or attachment when the tool and host allow them; do not probe an explicitly prohibited operation.
- If an operation encounters a permission denial or an explicit tool/host restriction, report the exact operation, target, error or restriction, and dependent steps that are blocked. Pause only those steps and continue independent authorized checks. A missing dependency, connection failure, or launch failure alone does not prove a sandbox restriction. Request narrowly scoped authorization only when a verified permission gap requires it and the host supports that remedy.
- Never change sandbox settings or configuration, restart with broader permissions, or bypass restrictions automatically. UI control, process startup/shutdown, and configuration changes retain their existing authorization requirements; this Skill grants none of those permissions.
- Run setup from the same project directory you need to debug.
- Treat `mcp__node_repl__js_reset` as a recovery tool, not routine cleanup. Resetting the kernel destroys your Playwright handles.

## Dependency preflight

Check that `node_repl` is callable, the project's locked Playwright dependency can be resolved and imported, and the required runtime is available. Register the existing workspace `node_modules` directory with the kernel if needed.

Missing dependencies use the project's installation or rebuild workflow under the current authorization. Do not initialize an established project or install packages merely for a read-only review. When no project workflow exists and dependency setup is authorized, choose the minimum setup for the required runtime; attaching to Electron over CDP does not require installing a separate Chromium browser.

## Core Workflow

1. Write a brief QA inventory scoped to this change, affected shared paths, and the claims in the final response. A whole-product inventory is needed only for whole-product QA; report unrelated existing defects without expanding implementation scope. Before testing:
   - Build one shared functional and visual coverage list from the user's requirements, implemented user-visible behavior, and intended final claims. List each claim, meaningful control or mode, and the state or view changes it can cause; each must map to a QA check before signoff.
   - Distinguish functional/state/performance claims from visual claims. For each relevant claim or control-state pair, select the necessary check and evidence; only visual claims need visual inspection. One inspected image can support several related claims. Turn visually central subjective requirements into observable checks; do not create another image ledger.
   - Add exploratory or off-happy-path scenarios only for concrete risks in the affected behavior; there is no fixed scenario quota.
2. Run the bootstrap cell once.
3. Determine the project startup path and whether this task owns the runtime or only attaches to it.
4. Start or attach through that path and keep reusing the same Playwright handles.
5. After each code change, reload for renderer-only changes or relaunch for main-process/startup changes.
6. Run functional QA with normal user input.
7. Run visual QA when an unresolved visual claim or required visual acceptance needs it; retain valid unaffected evidence.
8. Verify viewport fit when the contract or a concrete layout risk requires it, and capture only evidence needed for unresolved claims.
9. Clean up the Playwright session only when the task is actually finished.

## Runtime references

Read only the branch needed for this task; reuse loaded instructions while the session is healthy.

- Before the first session, read [shared bootstrap](references/bootstrap.md).
- For a Web session, read [Web startup and viewport modes](references/web-session.md).
- For Electron launch or attachment, read [Electron sessions](references/electron-session.md). Identify the requested window from observed URLs/titles; never substitute a different window when selection is ambiguous.
- Before starting a server, reloading, restarting or cleaning up, read [lifecycle and cleanup](references/lifecycle.md). Record whether the task owns or borrows the process; uncertainty requires investigation, not restart.
- Before emitting screenshot evidence, read [capture and normalization](references/screenshots.md). Electron captures must use the BrowserWindow corresponding to the selected Playwright page.

## Checklists

### Session Loop

- Bootstrap `node_repl` once, then keep the same Playwright handles alive across iterations.
- Start or attach using the selected lifecycle path.
- Make the code change.
- Reload or relaunch using the correct path for that change.
- Update the shared QA inventory if exploration reveals an additional control, state, or visible claim.
- Re-run functional checks whose results the change can invalidate.
- Re-run visual checks for affected states and shared layout; retain unaffected evidence.
- Capture final artifacts only after the current state is the one you are evaluating.

### Reload Decision

- Renderer-only change: reload the existing page or Electron window.
- Main-process, preload, or startup change: relaunch Electron.
- Unknown process ownership or startup path: inspect provenance first. Do not restart, close, or launch a replacement until ownership and the permitted lifecycle path are established.

### Functional QA

- Use real user controls for signoff: keyboard, mouse, click, touch, or equivalent Playwright input APIs.
- Verify at least one end-to-end critical flow.
- Confirm the visible result of that flow, not just internal state.
- For realtime or animation-heavy apps, verify behavior under actual interaction timing.
- Work through the shared QA inventory rather than ad hoc spot checks.
- Cover the controls and states in the scoped QA inventory, including affected shared behavior beyond the happy path; do not expand to unrelated visible controls.
- For reversible controls or stateful toggles in the inventory, test the full cycle: initial state, changed state, and return to the initial state.
- After the scripted checks pass, explore with normal input only if a concrete risk remains in the scoped inventory. Choose a proportionate duration instead of a fixed time quota.
- Add newly discovered states, controls or claims to the inventory only when they affect the change or a promised result. Report unrelated defects separately.
- `page.evaluate(...)` and `electronApp.evaluate(...)` may inspect or stage state, but they do not count as signoff input.

### Visual QA

- Treat visual QA as distinct evidence from functional QA, not a mandatory new pass after every functional change. Scope it to affected regions, states and shared layout; expand for a concrete propagated effect or defect.
- Use the same shared QA inventory defined before testing and updated during QA; do not start visual coverage from a different implicit list.
- Verify scoped visual claims explicitly; functional results do not automatically need screenshots and do not prove appearance. Apply the [shared visual evidence method](../../resident/ddd-implement/references/testing.md#select-visual-evidence) to capture, model inspection and reuse.
- A user-visible claim is not signed off until it has been inspected in the specific state where it is meant to be perceived.
- Inspect the initial viewport before scrolling.
- Confirm that the initial view visibly supports the interface's primary claims; if a core promised element is not clearly perceptible there, treat that as a bug.
- Inspect all required visible regions, not just the main interaction surface.
- Inspect the states and modes already enumerated in the shared QA inventory, including at least one meaningful post-interaction state when the task is interactive.
- If motion or transitions are part of the experience, inspect at least one in-transition state in addition to the settled endpoints.
- If labels, overlays, annotations, guides, or highlights are meant to track changing content, verify that relationship after the relevant state change.
- For dynamic or interaction-dependent visuals, inspect long enough to judge stability, layering, and readability; do not rely on a single screenshot for signoff.
- For interfaces that can become denser after loading or interaction, inspect the densest realistic state you can reach during QA, not only the empty, loading, or collapsed state.
- Check additional viewport/window sizes only when the approved contract or a concrete adaptation risk requires them. Preserve fixed-window constraints; do not invent a smaller size or repeat a valid minimum-size check without relevant change.
- Distinguish presence from implementation: if an intended affordance is technically there but not clearly perceptible because of weak contrast, occlusion, clipping, or instability, treat that as a visual failure.
- If any required visible region is clipped, cut off, obscured, or pushed outside the viewport in the state you are evaluating, treat that as a bug even if page-level scroll metrics appear acceptable.
- Look for clipping, overflow, distortion, layout imbalance, inconsistent spacing, alignment problems, illegible text, weak contrast, broken layering, and awkward motion states.
- Judge aesthetic quality as well as correctness. The UI should feel intentional, coherent, and visually pleasing for the task.
- Prefer viewport screenshots for signoff. Use full-page captures only as secondary debugging artifacts, and capture a focused screenshot when a region needs closer inspection.
- If motion makes a screenshot ambiguous, wait briefly for the UI to settle, then capture the image you are actually evaluating.
- Before signoff, check whether any scoped visual claim still lacks valid evidence; stop once it is established. Do not broaden coverage because a phase ended or some unrelated part has not been inspected.

### Signoff

Apply checks to the approved change and its actual claims. A functional-only task does not acquire a new visual signoff; reuse valid visual evidence where relevant instead of rereading it automatically.

- The functional path passed with normal user input.
- Coverage is explicit against the shared QA inventory: note which requirements, implemented features, controls, states, and claims were exercised, and call out any intentional exclusions.
- Applicable visual QA covered the affected visual claims; disclose reused evidence and exclusions without claiming uninspected scope passed.
- Each visual claim has valid inspected evidence from the relevant state and viewport/window size. An image may support multiple claims; saved artifacts need not all be emitted to the model. Functional-only claims need their corresponding functional evidence.
- Applicable viewport-fit checks passed for the intended view and contractually required sizes.
- When launch geometry is affected or required, the as-launched size, placement and initial layout were checked before manual resizing or repositioning.
- Assessed visual changes are coherent and meet the approved visual quality requirements.
- Functional correctness, viewport fit and visual quality each need their own evidence when claimed; one does not imply the others.
- Any risk-triggered exploratory pass is complete; report its scope when relevant to the result.
- If screenshot review and numeric checks disagreed at any point, the discrepancy was investigated before signoff; visible clipping in screenshots is a failure to resolve, not something metrics can overrule.
- Include a brief negative confirmation of the main defect classes you checked for and did not find.
- Cleanup was executed, or you intentionally kept the session alive for further work.

## Viewport Fit Checks (When Required)

Use these checks for an approved viewport-fit requirement or concrete layout risk, reusing valid unaffected evidence. Do not assume a screenshot is acceptable just because the main widget is visible. A new fit claim needs actual screenshot review with supporting bounds, not a functional pass alone.

- Define the intended initial view before signoff. For scrollable pages, this is the above-the-fold experience. For app-like shells, games, editors, dashboards, or tools, this is the full interactive surface plus the controls and status needed to use it.
- Use screenshots as the primary evidence for fit. Numeric checks support the screenshots; they do not overrule visible clipping.
- Signoff fails if any required visible region is clipped, cut off, obscured, or pushed outside the viewport in the intended initial view, even if page-level scroll metrics appear acceptable.
- Scrolling is acceptable when the product is designed to scroll and the initial view still communicates the core experience and exposes the primary call to action or required starting context.
- For fixed-shell interfaces, scrolling is not an acceptable workaround if it is needed to reach part of the primary interactive surface or essential controls.
- Do not rely on document scroll metrics alone. Fixed-height shells, internal panes, and hidden-overflow containers can clip required UI while page-level scroll checks still look clean.
- Check region bounds, not just document bounds. Verify that each required visible region fits within the viewport in the startup state.
- For Electron or desktop apps, verify both the launched window size and placement and the renderer's initial visible layout before any manual resize or repositioning.
- Passing viewport-fit checks only proves that the intended initial view is visible without unintended clipping or scrolling. It does not prove that the UI is visually correct or aesthetically successful.

Web or renderer check:

```javascript
console.log(await page.evaluate(() => ({
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  clientWidth: document.documentElement.clientWidth,
  clientHeight: document.documentElement.clientHeight,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight,
  canScrollX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  canScrollY: document.documentElement.scrollHeight > document.documentElement.clientHeight,
})));
```

Electron check:

```javascript
console.log(await appWindow.evaluate(() => ({
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  clientWidth: document.documentElement.clientWidth,
  clientHeight: document.documentElement.clientHeight,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight,
  canScrollX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  canScrollY: document.documentElement.scrollHeight > document.documentElement.clientHeight,
})));
```

Augment the numeric check with `getBoundingClientRect()` checks for the required visible regions in your specific UI when clipping is a realistic failure mode; document-level metrics alone are not sufficient for fixed shells.
