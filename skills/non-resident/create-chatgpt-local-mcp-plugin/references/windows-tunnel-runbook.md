# Windows Secure MCP Tunnel runbook

Read this only for Windows Tunnel setup, troubleshooting, or automatic startup. Follow the current official Secure MCP Tunnel guide when it differs:

https://developers.openai.com/api/docs/guides/secure-mcp-tunnels

## Per-app identity

Assign unique values for:

- plugin slug and display name;
- Tunnel or confirmed shared-app Tunnel;
- profile filename;
- Windows Credential Manager target;
- scheduled task name;
- local admin/health port;
- log location, if logging is required.

Reuse the existing MCP server and Tunnel only when adding tools to the same ChatGPT app and trust boundary. For independently managed apps, use separate endpoints and identities. Do not run multiple clients against one `tunnel_id` unless current official documentation explicitly supports it.

## Secret handling

- Request explicit confirmation before storing or replacing a runtime key.
- Read the key as a masked secure value.
- Store it as a Generic Credential for the current Windows user.
- Do not write the key to source, profiles, task arguments, command history, logs, tests, or documentation.
- Decode it only at process launch, place it in `CONTROL_PLANE_API_KEY` for the child process, and release/zero temporary buffers where the platform permits.
- Provide an uninstall path that removes the task and, unless the user requests otherwise, the associated credential.

## True no-console startup

`powershell.exe -WindowStyle Hidden` alone may still produce a visible console or Windows Terminal tab through child processes. Use this process tree instead:

1. Register a current-user logon task with limited privileges and `StartWhenAvailable`.
2. Point the task action directly to the project virtual environment’s `pythonw.exe`.
3. Run a `.pyw` launcher that reads the credential and starts `tunnel-client` with Windows `CREATE_NO_WINDOW`.
4. Set child stdin, stdout, and stderr to `DEVNULL`, or to an explicitly bounded/redacted log when diagnostics are required.
5. If the Tunnel client launches another console program, wrap that child with the same no-console rule.
6. Use `MultipleInstances IgnoreNew`, no execution time limit, and a bounded restart policy.

The launcher should run `doctor --profile-file ... --explain` before `run --profile-file ...` and exit nonzero if validation fails. Avoid embedding repository-specific absolute paths in the global skill; generate them from the target project during setup.

## Installation verification

After registering or updating the task:

1. Start it once when no healthy instance exists.
2. Wait with a bounded deadline for `/readyz`.
3. Verify `/healthz` and `/readyz` return success.
4. Verify the scheduled task remains `Running` and inspect `LastTaskResult` if it stops.
5. Compare process start times and parentage to confirm no new visible terminal belongs to the task.
6. Close only a known stale tunnel tab manually; never terminate a shared Windows Terminal process that may host unrelated work.

## Safe update and removal

- Stop only the scheduled task and process tree proven to belong to this app.
- Never kill processes by executable name alone when other projects may use the same runtime.
- Re-register the task after moving the repository because task actions normally contain absolute paths.
- On removal, unregister the exact task, stop its verified descendants, and delete only its exact credential target.
