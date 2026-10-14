# Optional lifecycle adapters

These read-only adapters move deterministic lookup and structural checks into
[workflow_hooks.py](../scripts/workflow_hooks.py). They do not route tasks, grant
permission, choose a phase, update records or run product tests. Registration,
trust, installation and configuration changes require their own authorization.
Shipping this Skill does not enable hooks. No hook configuration is bundled.

## Recovery

The `session-start` command accepts Codex `SessionStart` JSON on stdin. Only
`source: resume` or `compact` triggers lookup; startup/clear and explicit subagent
markers produce no output. It finds the nearest ancestor with `.planning`, reads
schema 2's project entry and conversation index, then selects the unique safe
`record.md` whose `owner_thread` exactly equals `session_id`. No binding produces
no output; ambiguous bindings, unsafe paths, unknown schemas or unreadable files
return a short lookup warning and require the existing manual recovery path.

The recovery context contains local entry/record pointers, the selected record's
SHA-256 and whitelisted declared state fields. It does not inject record prose,
approval replies, transcripts or a generated memory. The main conversation reads
missing summaries and authority and decides whether those facts still apply.
The adapter does not scan historical records or fall back to the newest entry.

Before enabling on a host, verify the identity mapping and event coverage there.
Subagent lifecycle events are unsupported: Codex can share the parent's
`session_id` with subagents. Explicit subagent markers are ignored, but their
absence does not prove root identity. Do not register this recovery adapter on
`SubagentStart`/`SubagentStop` or assume source checks certify every host.

Manual recovery uses the same lookup without enabling hooks:

```text
python -B <ddd-flow>/scripts/workflow_hooks.py recover --project <root> --thread <observed-id>
```

When this conversation has several indexed records, add `--change` with the
explicitly selected change directory or record. Schema 1 remains supported by
the Skill's existing single-pointer method and `workflow_check.py`; this adapter
does not invent schema 1 ownership or migrate it.

## Record checking

The `post-tool-use` command accepts Codex `PostToolUse` JSON on stdin. It recognizes
explicit file paths from canonical `apply_patch` commands (including move/delete)
and `Write`/`Edit` `file_path` inputs. Other tools and arbitrary shell commands are
ignored; script/shell writers use the manual checker. Only a write naming the
uniquely selected active `record.md` calls the existing checker in-process.
Successful checks produce no output; problems return bounded issue codes and the
selected record pointer as informational context. The hook returns no blocking,
continuation, permission or input-rewrite decision and cannot undo a write.

The checker also reads the project/index and declared local dependencies; its
scope and verdict remain structural. An intermediate multi-step write can be
incomplete. Resolve findings within authorized maintenance, or report the gap;
the adapter never fixes files or changes semantic phase/acceptance decisions.
Before claiming structural validity after the complete write, reuse identifiable
hook/check evidence for those exact inputs, or run the existing manual command:

```text
python -B <ddd-flow>/scripts/workflow_check.py --project <root> --change <change-directory> --thread <observed-id>
```

Silence alone does not establish that a hook was configured, trusted or ran.
Do not repeat a valid check merely because a phase ended; recheck changed inputs
and still-required project checks. Missing/disabled/untrusted adapters use the
same manual method, not a second validation policy.

## Runtime and delivery boundary

Resolve the actual Python and Skill absolute paths; the commands above are
unregistered entry points, not installation instructions. Adapters use only the
standard library, disable local import bytecode, do not launch subprocesses and
never read `transcript_path`. Reads and context are bounded; unrelated calls exit
without reading workflow files. There are no persistent caches or new state stores.

For later authorized activation, use only the two documented events, short
explicit timeouts and a positive context limit, and verify loading, root identity,
path coverage, partial writes and failure feedback on the actual host. Do not
enable a `Stop` continuation hook or automatically approve tool operations.
The host's trust and tool coverage constraints remain effective; see the
[official Hooks documentation](https://learn.chatgpt.com/docs/hooks).

Source static checks do not certify runtime events, model behavior or token/time
savings. Compare complete task paths, including hook output, only under a separate
evaluation authorization. Preserve the manual path until equivalent behavior is
established; do not shorten away policy or semantic safeguards.
