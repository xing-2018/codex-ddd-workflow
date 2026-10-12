## Attach to an Existing Runtime

Use the project's startup and attachment path when it manages the process. Record whether the task started the application or merely attached to an existing one before choosing restart and cleanup actions.

For an authorized Chromium CDP endpoint, use `chromium.connectOverCDP(endpoint)` and identify the intended renderer from the observed pages and project evidence. Do not select an unrelated page merely because it is first. Keep waits bounded and report connection failures.

CDP attachment provides browser/renderer handles, not an `ElectronApplication`. Use renderer screenshots and checks with those handles; the [main-process screenshot examples](screenshots.md#electron-css-normalization) and [direct Electron restart](lifecycle.md#reuse-sessions-during-iteration) require a tool-launched Electron session. Report any unmet main-process verification requirement instead of claiming equivalent coverage.

When startup or main/preload changes require a restart, use the same project lifecycle path and reconnect. For renderer-only changes, reuse and reload the target when appropriate.

## Start or Reuse Electron Session

The following direct-launch examples apply only when the project permits the tool to own the Electron process. For a project-managed runtime, use the attachment branch above.

Set `ELECTRON_ENTRY` to `.` when the current workspace is the Electron app and `package.json` points `main` to the right entry file. If you need to target a specific main-process file directly, use a path such as `./main.js` instead.

```javascript
var ELECTRON_ENTRY = ".";

if (appWindow?.isClosed()) appWindow = undefined;

if (!appWindow && electronApp) {
  await electronApp.close().catch(() => {});
  electronApp = undefined;
}

electronApp ??= await electronLauncher.launch({
  args: [ELECTRON_ENTRY],
});

// Use the first window only for a verified single-window application.
await electronApp.firstWindow();
var candidates = electronApp.windows();
if (candidates.length !== 1) throw new Error("Identify the requested window from observed URLs/titles before proceeding");
appWindow ??= candidates[0];

console.log("Loaded Electron window:", await appWindow.title());
```

If `node_repl` is not already running from the Electron app workspace, pass `cwd` explicitly when launching.

If the app process looks stale, set `electronApp = appWindow = undefined` and rerun the cell.

If you already have an Electron session but need a fresh process after a main-process, preload, or startup change, use the [lifecycle restart cell](lifecycle.md#reuse-sessions-during-iteration) instead of rerunning this one.
