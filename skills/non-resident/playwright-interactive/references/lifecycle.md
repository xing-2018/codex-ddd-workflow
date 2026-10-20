## Reuse Sessions During Iteration

Keep the same session alive whenever you can.

Web renderer reload:

```javascript
await reloadWebContexts();
```

Electron renderer-only reload:

```javascript
await appWindow.reload({ waitUntil: "domcontentloaded" });
console.log("Reloaded Electron window");
```

Electron restart after main-process, preload, or startup changes:

```javascript
await electronApp.close().catch(() => {});
electronApp = undefined;
appWindow = undefined;

electronApp = await electronLauncher.launch({
  args: [ELECTRON_ENTRY],
});

await electronApp.firstWindow();
var candidates = electronApp.windows();
if (candidates.length !== 1) throw new Error("Reidentify the requested window after restart");
appWindow = candidates[0];
console.log("Relaunched Electron window:", await appWindow.title());
```

If your launch requires an explicit `cwd`, include the same `cwd` here.

Default posture:

- Keep each `node_repl` cell short and focused on one interaction burst.
- Reuse the existing top-level bindings (`browser`, `context`, `page`, `electronApp`, `appWindow`) instead of redeclaring them.
- If you need isolation, create a new page or a new context inside the same browser.
- For Electron, use `electronApp.evaluate(...)` only for main-process inspection or purpose-built diagnostics.
- Fix helper mistakes in place; do not reset the REPL unless the kernel is actually broken.

## Dev Server

For local web debugging, keep the app running in a persistent TTY session. Do not rely on one-shot background commands from a short-lived shell.

Use the project's normal start command, for example:

```bash
npm start
```

Before `page.goto(...)`, verify the chosen port is listening and the app responds.

For tool-owned Electron debugging, launch through `_electron.launch(...)` so the same session owns the process. If this tool-owned renderer depends on a separate dev server (for example Vite or Next), keep that server running in a persistent TTY session and then relaunch or reload the Electron app from `node_repl`. Project-managed runtimes use their existing lifecycle and the attachment branch.

## Cleanup

Only run cleanup when the task is actually finished.

For an attached runtime, detach the automation connection without closing existing pages, contexts or the application. Stop an application started by this task only through its project lifecycle path. Do not apply the close-all cell below to a borrowed runtime. The cell is for sessions whose browser/application lifecycle is owned by the tool:

- This cleanup is manual. Exiting Codex, closing the terminal, or losing the `node_repl` session does not implicitly run `electronApp.close()`, `context.close()`, or `browser.close()`.
- For Electron specifically, assume the app may keep running if you leave the session without executing the cleanup cell first.

```javascript
if (electronApp) {
  await electronApp.close().catch(() => {});
}

if (mobileContext) {
  await mobileContext.close().catch(() => {});
}

if (context) {
  await context.close().catch(() => {});
}

if (browser) {
  await browser.close().catch(() => {});
}

browser = undefined;
context = undefined;
page = undefined;
mobileContext = undefined;
mobilePage = undefined;
electronApp = undefined;
appWindow = undefined;

console.log("Playwright session closed");
```

If you plan to exit Codex immediately after debugging, run the cleanup cell first and wait for the `"Playwright session closed"` log before quitting.

## Common Failure Modes

- `Cannot find module 'playwright'`: run the dependency preflight in the current workspace, add its absolute `node_modules` directory with `mcp__node_repl__js_add_node_module_dir` when needed, and verify the import before using `node_repl`.
- A required runtime is missing: follow the dependency preflight and project rebuild path; do not download an unrelated browser for an Electron attachment.
- `page.goto: net::ERR_CONNECTION_REFUSED`: make sure the dev server is still running in a persistent TTY session, recheck the port, and prefer `http://127.0.0.1:<port>`.
- `electron.launch` hangs, times out, or exits immediately: verify the local `electron` dependency, confirm the `args` target, and make sure any renderer dev server is already running before launch.
- `Identifier has already been declared`: reuse the existing top-level bindings, choose a new name, or wrap the code in `{ ... }`. Use `mcp__node_repl__js_reset` only when the kernel is genuinely stuck.
- `browserContext.newPage: Protocol error (Target.createTarget): Not supported` while working with Electron: do not use `appWindow.context().newPage()` or `electronApp.context().newPage()` as a scratch page; use the Electron-specific screenshot normalization flow in the model-bound screenshots section.
- `node_repl` timed out or reset: rerun the bootstrap cell and recreate the session with shorter, more focused cells.
- Browser launch or network operations fail immediately: inspect the actual error and the tool/host restrictions under [Preconditions](../SKILL.md#preconditions). Do not infer a sandbox restriction from the failure alone or require a different sandbox mode before diagnosis. A permission restriction blocks only dependent operations; continue independent authorized checks and preserve the existing process and configuration authorization boundaries.
