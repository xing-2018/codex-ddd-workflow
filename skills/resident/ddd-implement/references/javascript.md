# JavaScript

Read only for changed JavaScript. Keep JavaScript, existing ESM/CommonJS and browser API compatibility. A small browser tool or single HTML file does not automatically become React/Vite/TypeScript. JSDoc, local @ts-check or project checkJs may provide incremental protection when appropriate and authorized. Separate business computation from DOM effects as needed without forcing a directory split. Make errors, cancellation, listener removal and resource cleanup explicit.

Reuse the [shared web guidance](typescript-javascript.md) already loaded; it does not require reading TypeScript or React bodies.

For new work, target modern browser capabilities or a supported, mature Node.js LTS line; the current validation target is Node 24 LTS. Match modules and APIs to the declared runtime, not merely to syntax accepted by a compiler. AbortController can own related requests/listeners; use explicit cleanup and stale-result protection when necessary. Do not assume every proposed ECMAScript feature is available in the target.
