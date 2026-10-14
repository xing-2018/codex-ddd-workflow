"""Read-only DDD lifecycle adapters; registration and trust are separate actions.

No transcript parsing, writes, model calls, command execution or state repair.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# The adapters must not leave import caches in an installed Skill directory.
sys.dont_write_bytecode = True
import workflow_check

MAX_INPUT = 1024 * 1024
MAX_DOCUMENT = 256 * 1024
MAX_CONTEXT = 1800
RECORD_FIELDS = {
    "phase": workflow_check.PHASES,
    "status": workflow_check.STATUSES,
    "technical_verdict": {"PASS", "FAIL", "BLOCKED", "NOT_CHECKED"},
    "user_acceptance": {"pending", "accepted", "rejected"},
}


class LookupGap(ValueError):
    """A bounded lookup needs manual recovery, not an automatic choice."""


def read_document(root: Path, path: Path) -> bytes:
    if not workflow_check.safe_path(root, path) or not path.is_file():
        raise LookupGap("WORKFLOW_PATH_UNAVAILABLE")
    with path.open("rb") as stream:
        content = stream.read(MAX_DOCUMENT + 1)
    if len(content) > MAX_DOCUMENT:
        raise LookupGap("WORKFLOW_DOCUMENT_TOO_LARGE")
    return content


def project_root(cwd: Path) -> Path | None:
    """Use the nearest existing workflow entry, never scan sibling projects."""
    location = cwd.resolve(strict=True)
    if not location.is_dir():
        raise LookupGap("WORKING_DIRECTORY_UNAVAILABLE")
    for candidate in (location, *location.parents):
        if (candidate / ".planning").exists():
            return candidate
    return None


def selected_record(root: Path, thread: str, requested: Path | None = None) -> Path | None:
    project = read_document(root, root / ".planning/PROJECT.md").decode("utf-8-sig")
    schemas = re.findall(r"^\s*-?\s*workflow_schema:\s*(\S+)\s*$", project, re.M)
    if schemas != ["2"]:
        raise LookupGap("CONVERSATION_SCHEMA_REQUIRES_MANUAL_LOOKUP")
    index = read_document(root, root / ".planning/STATE.md").decode("utf-8-sig")
    rows, problems = workflow_check.index_rows(index)
    if problems:
        raise LookupGap("CONVERSATION_INDEX_INVALID")
    owned = [raw for raw, owner in rows if owner == thread and owner != "unresolved"]
    if requested is not None:
        target = requested if requested.is_absolute() else root / requested
        target = target.absolute()
        if target.name != "record.md":
            target = target / "record.md"
        owned = [raw for raw in owned if (root / raw).absolute() == target]
        if not owned:
            raise LookupGap("REQUESTED_BINDING_UNAVAILABLE")
    if not owned:
        return None
    if len(owned) != 1:
        raise LookupGap("CONVERSATION_BINDING_AMBIGUOUS")
    pointer = Path(owned[0])
    record = (root / pointer).absolute()
    if pointer.is_absolute() or record.name != "record.md":
        raise LookupGap("CONVERSATION_RECORD_UNSAFE")
    if not workflow_check.safe_path(root, record) or not record.is_file():
        raise LookupGap("CONVERSATION_RECORD_UNAVAILABLE")
    return record


def recovery_context(root: Path, record: Path) -> str:
    raw = read_document(root, record)
    text = raw.decode("utf-8-sig")
    facts = {
        "project_root": str(root),
        "project_entry": ".planning/PROJECT.md",
        "record": record.relative_to(root).as_posix(),
        "record_sha256": hashlib.sha256(raw).hexdigest(),
    }
    for field, allowed in RECORD_FIELDS.items():
        values = re.findall(rf"^\s*-?\s*{field}:\s*(\S+)\s*$", text, re.M)
        facts[field] = values[0] if len(values) == 1 and values[0] in allowed else "UNKNOWN"
    context = ("DDD recovery pointers and declared facts, not approval or acceptance: "
               + json.dumps(facts, ensure_ascii=True, sort_keys=True)
               + " Read only missing record summary and applicable authority. "
                 "The main conversation resolves permission, relevance and the next action.")
    if len(context) > MAX_CONTEXT:
        raise LookupGap("RECOVERY_POINTER_TOO_LARGE")
    return context


def edited_paths(event: dict, cwd: Path) -> set[Path]:
    """Recognize explicit file edits only; arbitrary shell commands stay manual."""
    inputs = event.get("tool_input")
    if not isinstance(inputs, dict):
        return set()
    tool = event.get("tool_name")
    if not isinstance(tool, str):
        return set()
    names: list[str] = []
    if tool == "apply_patch":
        command = inputs.get("command")
        if not isinstance(command, str):
            return set()
        names = re.findall(r"^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)$", command, re.M)
    elif tool in {"Write", "Edit"}:
        filename = inputs.get("file_path")
        if isinstance(filename, str):
            names = [filename]
    paths = set()
    for name in names:
        candidate = Path(name.strip())
        paths.add((candidate if candidate.is_absolute() else cwd / candidate).absolute())
    return paths


def hook_output(event: dict) -> dict | None:
    kind = event.get("hook_event_name")
    if not isinstance(kind, str) or kind not in {"SessionStart", "PostToolUse"}:
        return None
    if event.get("agent_id") or event.get("subagent_type"):
        return None
    if kind == "SessionStart":
        source = event.get("source")
        if not isinstance(source, str) or source not in {"resume", "compact"}:
            return None
    cwd_value, thread = event.get("cwd"), event.get("session_id")
    if not isinstance(cwd_value, str) or not isinstance(thread, str) or not thread or thread == "unresolved":
        raise LookupGap("HOOK_IDENTITY_UNAVAILABLE")
    cwd = Path(cwd_value)
    if not cwd.is_absolute():
        raise LookupGap("HOOK_WORKING_DIRECTORY_NOT_ABSOLUTE")
    # Avoid even opening workflow files for unrelated tool calls.
    paths = edited_paths(event, cwd) if kind == "PostToolUse" else set()
    if kind == "PostToolUse" and not any(path.name == "record.md" for path in paths):
        return None
    root = project_root(cwd)
    if root is None:
        return None
    record = selected_record(root, thread)
    if record is None:
        return None
    if kind == "SessionStart":
        return {"hookSpecificOutput": {"hookEventName": kind,
                                       "additionalContext": recovery_context(root, record)}}
    if record not in paths:
        return None
    result = workflow_check.check_project(root, record.parent, thread, read_limit=MAX_DOCUMENT)
    if result["status"] == "PASS":
        return None
    codes = sorted({entry["code"] for entry in result["issues"]})
    feedback = json.dumps({"project_root": str(root), "record": record.relative_to(root).as_posix(),
                           "structural_status": result["status"], "issue_codes": codes},
                          ensure_ascii=True, sort_keys=True)
    context = ("DDD record structure feedback (not authorization or whole-task acceptance): "
               + feedback + " Resolve in-scope issues or use workflow_check.py for details. "
                 "A partial write may be incomplete; do not repair automatically or rerun product tests.")
    if len(context) > MAX_CONTEXT:
        raise LookupGap("RECORD_FEEDBACK_TOO_LARGE")
    return {"hookSpecificOutput": {"hookEventName": kind, "additionalContext": context}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("session-start", "post-tool-use", "recover"))
    parser.add_argument("--project", type=Path, help="Explicit project root for manual recovery only")
    parser.add_argument("--thread", help="Observed conversation ID for manual recovery only")
    parser.add_argument("--change", type=Path, help="Explicit record or change directory for manual recovery only")
    args = parser.parse_args()
    sys.stdin.reconfigure(encoding="utf-8")
    if args.mode == "recover":
        if args.project is None or not args.thread:
            parser.error("recover requires --project and --thread")
    elif args.project is not None or args.thread is not None or args.change is not None:
        parser.error("hook modes read their project and identity from stdin")
    try:
        if args.mode == "recover":
            root = args.project.resolve(strict=True)
            record = selected_record(root, args.thread, args.change)
            if record is None:
                raise LookupGap("CONVERSATION_BINDING_UNAVAILABLE")
            print(recovery_context(root, record))
            return 0
        raw = sys.stdin.read(MAX_INPUT + 1)
        if len(raw) > MAX_INPUT:
            raise LookupGap("HOOK_INPUT_TOO_LARGE")
        event = json.loads(raw)
        if not isinstance(event, dict):
            raise LookupGap("HOOK_INPUT_NOT_OBJECT")
        expected = "SessionStart" if args.mode == "session-start" else "PostToolUse"
        if event.get("hook_event_name") != expected:
            raise LookupGap("HOOK_EVENT_MISMATCH")
        output = hook_output(event)
        if output is not None:
            print(json.dumps(output, ensure_ascii=True, sort_keys=True))
        return 0
    except (LookupGap, OSError, UnicodeError, ValueError) as error:
        # Never leak raw documents, OS errors or malformed input into developer context.
        code = str(error) if isinstance(error, LookupGap) else "HOOK_LOOKUP_UNAVAILABLE"
        message = f"DDD lookup gap: {code}. Use the Skill's manual recovery/check path; no files were changed."
        if args.mode == "recover":
            print(message, file=sys.stderr)
            return 2
        print(json.dumps({"systemMessage": message}, ensure_ascii=True))
        return 0


if __name__ == "__main__":
    sys.exit(main())
