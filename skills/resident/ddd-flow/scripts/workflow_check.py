"""Read-only structural check for a requested, optionally conversation-bound DDD change.

This checks paths and declared identities, not the truth of approval or design quality.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

PHASES = {"requirements", "design", "planning", "implementation", "verification", "acceptance", "closed"}
STATUSES = {"working", "awaiting_user", "blocked", "done", "cancelled"}
EXIT = {"PASS": 0, "NEEDS_REVIEW": 2, "INVALID": 1, "UNAVAILABLE": 3}
WORKFLOW_SCHEMA = 2
SUPPORTED_SCHEMAS = {1, WORKFLOW_SCHEMA}
HASH_LINE = re.compile(r"^[ \t]*[-*]?[ \t]*(?P<path>[^:\r\n]+?):[ \t]*sha256=(?P<hash>[0-9a-fA-F]{64})[ \t]*\r?$", re.M)
LINK = re.compile(r"(?<!!)\[[^]]*]\((?P<target>[^)]+)\)")
GATE_FILE = re.compile(r"`([^`\s]+\.(?:md|json|py))`")


def issue(code: str, path: str, detail: str, blocks: bool = True) -> dict[str, object]:
    return {"code": code, "path": path, "detail": detail, "blocks": blocks}


def inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def linked(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


def safe_path(root: Path, path: Path) -> bool:
    if not inside(root, path) or not inside(root, path.resolve(strict=False)):
        return False
    current = root
    for part in path.relative_to(root).parts:
        current = current.parent if part == ".." else current / part
        if not inside(root, current):
            return False
        if linked(current):
            return False
    return True


def read_bytes(path: Path, limit: int | None = None) -> bytes:
    """Keep CLI reads unchanged; lifecycle callers can bound each file read."""
    if limit is None:
        return path.read_bytes()
    with path.open("rb") as stream:
        content = stream.read(limit + 1)
    if len(content) > limit:
        raise OSError("workflow input exceeds the lifecycle read limit")
    return content


def index_rows(entry: str) -> tuple[list[tuple[str, str | None]], list[dict[str, object]]]:
    """Parse index declarations without selecting a newest or implicit owner."""
    location = ".planning/STATE.md"
    problems: list[dict[str, object]] = []
    rows: list[tuple[str, str | None]] = []
    for line in entry.splitlines():
        match = re.fullmatch(r"\s*(?:-\s*)?(active_record|owner_thread):\s*(\S+)\s*", line)
        if not match:
            continue
        key, value = match.groups()
        if key == "active_record":
            rows.append((value, None))
        elif not rows or rows[-1][1] is not None:
            problems.append(issue("OWNER_BINDING_INVALID", location,
                                  "owner_thread must follow exactly one active_record"))
        else:
            rows[-1] = (rows[-1][0], value)
    return rows, problems


def check_index(root: Path, entry: str, change: Path, schema: int,
                thread: str | None) -> list[dict[str, object]]:
    """Check declared membership; this does not lock resources or certify approval."""
    location = ".planning/STATE.md"
    rows, problems = index_rows(entry)
    if schema == 1:
        if len(rows) != 1:
            return [issue("ACTIVE_POINTER_REVIEW", location,
                          "schema 1 requires exactly one project-relative active_record", False)]
        pointer = Path(rows[0][0])
        pointed = (root / pointer).absolute()
        if pointer.is_absolute() or not safe_path(root, pointed) or pointed != change / "record.md":
            problems.append(issue("ACTIVE_POINTER_INVALID", location,
                                  "active_record must safely point to the requested change record"))
        if thread is not None:
            problems.append(issue("OWNER_BINDING_REVIEW", location,
                                  "schema 1 has no conversation binding; verify before migration", False))
        return problems
    seen: set[Path] = set()
    requested_owner = None
    found = False
    for raw, owner in rows:
        pointer = Path(raw)
        pointed = (root / pointer).absolute()
        if (pointer.is_absolute() or not safe_path(root, pointed)
                or pointed.name != "record.md" or not pointed.is_file()):
            problems.append(issue("ACTIVE_POINTER_INVALID", raw, "indexed record.md is missing or unsafe"))
            continue
        pointed = pointed.resolve()
        if pointed in seen:
            problems.append(issue("ACTIVE_POINTER_DUPLICATE", raw, "record must occur once in the index"))
        seen.add(pointed)
        if owner is None or re.search(r"<[^<>]+>", owner):
            problems.append(issue("OWNER_BINDING_INVALID", raw,
                                  "declare owner_thread, or unresolved when provenance is unknown"))
        if pointed == (change / "record.md").resolve():
            found = True
            requested_owner = owner
    if not found:
        problems.append(issue("ACTIVE_MEMBERSHIP_MISSING", location,
                              "requested change must have an index entry"))
    elif requested_owner in {None, "unresolved"}:
        problems.append(issue("OWNER_BINDING_REVIEW", location,
                              "requested record's conversation owner is unresolved", False))
    elif thread is not None and thread != requested_owner:
        problems.append(issue("OWNER_BINDING_MISMATCH", location,
                              "requested conversation does not own this change"))
    return problems


def check_project(project: Path, change_dir: Path, thread: str | None = None,
                  read_limit: int | None = None) -> dict:
    """Return the same read-only result for CLI callers and lifecycle adapters."""
    problems: list[dict[str, object]] = []
    checked: list[str] = []
    schema: int | None = None
    try:
        root = project.resolve(strict=True)
        if not root.is_dir():
            raise OSError("project is not a directory")
    except OSError as exc:
        return {"schema_version": 1, "status": "UNAVAILABLE", "checked_paths": [],
                "issues": [issue("PROJECT_UNAVAILABLE", str(project), str(exc))]}
    change = (root / change_dir).absolute() if not change_dir.is_absolute() else change_dir.absolute()
    if not safe_path(root, change):
        problems.append(issue("UNSAFE_CHANGE_PATH", str(change_dir), "change must be inside project without links"))
    elif not change.is_dir():
        problems.append(issue("CHANGE_MISSING", str(change_dir),
                              "change directory is missing; pass its directory, "
                              "e.g. .planning/changes/example, not record.md"))
    else:
        for filename in ("PROJECT.md", "STATE.md"):
            file = root / ".planning" / filename
            if not safe_path(root, file) or not file.is_file():
                problems.append(issue("WORKFLOW_FILE_MISSING", file.relative_to(root).as_posix(),
                                      "required workflow entry missing or linked"))
                continue
            checked.append(file.relative_to(root).as_posix())
            try:
                entry = read_bytes(file, read_limit).decode("utf-8")
            except (OSError, UnicodeError) as exc:
                problems.append(issue("WORKFLOW_FILE_UNAVAILABLE", file.relative_to(root).as_posix(), str(exc)))
                continue
            if filename == "PROJECT.md":
                versions = re.findall(r"^\s*-?\s*workflow_schema:\s*(\S+)\s*$", entry, re.M)
                if len(versions) == 1 and versions[0] in {str(v) for v in SUPPORTED_SCHEMAS}:
                    schema = int(versions[0])
                else:
                    problems.append(issue("WORKFLOW_SCHEMA_REVIEW", file.relative_to(root).as_posix(),
                                          "compare missing, outdated or newer schema with current specification", False))
                sources = re.findall(r"^\s*-?\s*workflow_source:\s*(.+?)\s*$", entry, re.M)
                if len(sources) != 1 or re.search(r"<[^<>\n]+>", sources[0]):
                    problems.append(issue("WORKFLOW_SOURCE_REVIEW", file.relative_to(root).as_posix(),
                                          "declare a recoverable verified Skill source identity", False))
            else:
                if schema is not None:
                    problems.extend(check_index(root, entry, change, schema, thread))
        for filename in ("record.md",):
            file = change / filename
            if not safe_path(root, file) or not file.is_file():
                problems.append(issue("REQUIRED_FILE_MISSING", str(file.relative_to(root)), "required change file missing or linked"))
            else:
                checked.append(file.relative_to(root).as_posix())
        record = change / "record.md"
        if record.is_file() and safe_path(root, record):
            try:
                content = read_bytes(record, read_limit).decode("utf-8")
            except (OSError, UnicodeError) as exc:
                problems.append(issue("RECORD_UNAVAILABLE", record.relative_to(root).as_posix(), str(exc)))
                content = ""
            fields: dict[str, str] = {}
            for key, allowed in (("phase", PHASES), ("status", STATUSES)):
                values = re.findall(rf"^\s*-?\s*{key}:\s*(\S+)\s*$", content, re.M)
                if len(values) != 1 or values[0] not in allowed:
                    problems.append(issue("STATE_INVALID", record.relative_to(root).as_posix(),
                                          f"{key} must occur once with a supported value"))
                else:
                    fields[key] = values[0]
            design = change / "design.md"
            if fields.get("phase") in {"requirements", "design", "planning", "implementation"}:
                brief = change / "brief.md"
                if not safe_path(root, brief) or not brief.is_file():
                    problems.append(issue("BRIEF_MISSING", brief.relative_to(root).as_posix(),
                                          "this phase requires a brief or a pointer to its existing owner"))
                else:
                    checked.append(brief.relative_to(root).as_posix())
            if fields.get("phase") in {"design", "planning", "implementation"}:
                if not safe_path(root, design) or not design.is_file():
                    problems.append(issue("DESIGN_MISSING", str(design.relative_to(root)),
                                          "active phase requires design.md", fields.get("phase") != "design"))
                else:
                    checked.append(design.relative_to(root).as_posix())
            for match in HASH_LINE.finditer(content):
                raw = match.group("path").strip().strip("`")
                declared = (root / raw).absolute() if not Path(raw).is_absolute() else Path(raw).absolute()
                if not safe_path(root, declared) or not declared.is_file():
                    problems.append(issue("BASELINE_PATH_INVALID", raw, "declared local baseline is missing or unsafe"))
                    continue
                checked.append(declared.relative_to(root).as_posix())
                if hashlib.sha256(read_bytes(declared, read_limit)).hexdigest() != match.group("hash").lower():
                    problems.append(issue("BASELINE_DRIFT", raw, "declared SHA-256 differs from current bytes", False))
            for match in LINK.finditer(content):
                target = match.group("target").split("#", 1)[0].strip("<>")
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                local = (record.parent / target).absolute()
                if not safe_path(root, local) or not local.exists():
                    problems.append(issue("LOCAL_LINK_INVALID", target, "linked local object is missing or unsafe"))
            for line in content.splitlines():
                if not re.search(r"\bG[123]\b", line):
                    continue
                for raw in GATE_FILE.findall(line):
                    declared = (root / raw).absolute() if raw.startswith(".planning/") else (change / raw).absolute()
                    if not safe_path(root, declared) or not declared.is_file():
                        problems.append(issue("GATE_OBJECT_MISSING", raw, "declared G1/G2/G3 object is missing or unsafe"))
                    else:
                        checked.append(declared.relative_to(root).as_posix())
            if re.search(r"<[^<>\n]{1,100}>", content):
                problems.append(issue("PLACEHOLDER_REMAINS", record.relative_to(root).as_posix(),
                                      "review placeholder fields before treating package as complete", False))
    status = "INVALID" if any(p["blocks"] and p["code"] != "BASELINE_DRIFT" for p in problems) else (
        "NEEDS_REVIEW" if problems else "PASS")
    return {"schema_version": 1, "status": status, "checked_paths": sorted(set(checked)),
            "issues": problems}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Example: --project /path/to/project --change .planning/changes/example "
               "--thread observed-id. --change selects the directory containing record.md.",
    )
    parser.add_argument("--project", required=True, type=Path, metavar="PROJECT_ROOT",
                        help="Project root directory containing .planning")
    parser.add_argument("--change", required=True, type=Path, metavar="CHANGE_DIRECTORY",
                        help="Change directory, e.g. .planning/changes/example, relative to "
                             "--project or an absolute directory inside it; do not pass record.md")
    parser.add_argument("--thread", help="Observed conversation ID; checks schema 2 ownership without changing it")
    args = parser.parse_args()
    result = check_project(args.project, args.change, args.thread)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    status = result["status"]
    return EXIT[status]


if __name__ == "__main__":
    sys.exit(main())
