#!/usr/bin/env python3
"""Summarize LS-DYNA run files without judging physical acceptance."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_REQUIRED = ("messag", "d3hsp", "glstat", "matsum")
LOG_FILES = ("messag", "d3hsp", "run.log")
ERROR_RE = re.compile(r"\berror\s+(?:no\.?\s*)?\d+\b", re.IGNORECASE)
WARNING_RE = re.compile(
    r"(?:^\s*\*{2,}\s*warning\s+\d+|\bwarning\s+\d+\b)", re.IGNORECASE
)
NORMAL_RE = re.compile(r"normal\s+termination", re.IGNORECASE)
CODE_RE = re.compile(r"\b(error|warning)\s*(?:no\.?\s*)?(\d+)", re.IGNORECASE)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError:
        return ""
    return digest.hexdigest().upper()


def unique_lines(texts: list[str], pattern: re.Pattern[str], limit: int) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for text in texts:
        for raw in text.splitlines():
            line = " ".join(raw.split())
            if not line or not pattern.search(line) or line in seen:
                continue
            seen.add(line)
            result.append(line)
            if len(result) >= limit:
                return result
    return result


def matching_output_names(files: dict[str, Any], base_name: str) -> list[str]:
    """Resolve a normal output name and numbered full-restart variants."""
    matches: list[str] = []
    if base_name in files and files[base_name]["bytes"] > 0:
        matches.append(base_name)
    numbered = re.compile(rf"^{re.escape(base_name)}\d+$", re.IGNORECASE)
    matches.extend(
        name
        for name in sorted(files)
        if numbered.match(name) and files[name]["bytes"] > 0
    )
    return matches


def parse_timestamp(value: Any) -> float | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def current_run_output_names(
    run_dir: Path,
    files: dict[str, Any],
    candidates: set[str],
    manifest: Any,
) -> set[str]:
    """Bind output evidence to this manifest instead of trusting stale files."""
    if not isinstance(manifest, dict):
        return set(candidates)

    status = manifest.get("status")
    recorded = manifest.get("current_run_outputs")
    if status != "running" and isinstance(recorded, list):
        return {name for name in recorded if isinstance(name, str) and name in candidates}

    baseline = manifest.get("pre_run_output_signatures")
    if isinstance(baseline, dict):
        changed: set[str] = set()
        for name in candidates:
            before = baseline.get(name)
            if not isinstance(before, dict):
                changed.add(name)
                continue
            current = files[name]
            if before.get("bytes") != current["bytes"]:
                changed.add(name)
                continue
            before_hash = before.get("sha256")
            if isinstance(before_hash, str) and before_hash:
                current_hash = file_sha256(run_dir / name)
                if current_hash and current_hash.upper() != before_hash.upper():
                    changed.add(name)
                    continue
            before_mtime = parse_timestamp(before.get("modified_at_utc"))
            if before_mtime is not None and abs(before_mtime - current["modified_timestamp"]) > 1e-6:
                changed.add(name)
        return changed

    started_at = parse_timestamp(manifest.get("started_at"))
    if started_at is not None:
        return {
            name
            for name in candidates
            if files[name]["modified_timestamp"] >= started_at
        }
    return set(candidates)


def inspect(run_dir: Path, required: tuple[str, ...], line_limit: int) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    files: dict[str, Any] = {}
    for path in sorted(run_dir.iterdir()) if run_dir.is_dir() else []:
        if not path.is_file():
            continue
        stat = path.stat()
        files[path.name] = {
            "bytes": stat.st_size,
            "modified_at": datetime.fromtimestamp(
                stat.st_mtime, tz=timezone.utc
            ).astimezone().isoformat(),
            "modified_timestamp": stat.st_mtime,
        }

    all_resolved_required = {
        name: matching_output_names(files, name)
        for name in required
    }
    all_log_names = [
        actual
        for base_name in LOG_FILES
        for actual in matching_output_names(files, base_name)
    ]

    manifest_path = run_dir / "run_manifest.json"
    if not manifest_path.is_file():
        manifest_path = run_dir / "restart_manifest.json"
    manifest: Any = None
    if manifest_path.is_file():
        try:
            manifest = json.loads(read_text(manifest_path).lstrip("\ufeff"))
        except json.JSONDecodeError as exc:
            manifest = {"parse_error": str(exc)}

    candidate_names = {
        name
        for matches in all_resolved_required.values()
        for name in matches
    } | set(all_log_names)
    current_output_names = current_run_output_names(
        run_dir, files, candidate_names, manifest
    )
    resolved_required = {
        name: [actual for actual in matches if actual in current_output_names]
        for name, matches in all_resolved_required.items()
    }
    missing = [name for name, matches in resolved_required.items() if not matches]
    log_names = [name for name in all_log_names if name in current_output_names]
    log_texts = [read_text(run_dir / name) for name in log_names]
    normal_termination_evidence = [
        name
        for name, text in zip(log_names, log_texts)
        if NORMAL_RE.search(text)
        or "normaltermination" in re.sub(r"\s+", "", text).lower()
    ]
    normal_termination = bool(normal_termination_evidence)
    errors = unique_lines(log_texts, ERROR_RE, line_limit)
    warnings = unique_lines(log_texts, WARNING_RE, line_limit)

    codes: dict[str, list[int]] = {"error": [], "warning": []}
    for text in log_texts:
        for kind, code in CODE_RE.findall(text):
            key = kind.lower()
            value = int(code)
            if value not in codes[key]:
                codes[key].append(value)
    codes["error"].sort()
    codes["warning"].sort()

    manifest_status = manifest.get("status") if isinstance(manifest, dict) else None
    manifest_exit_code = manifest.get("exit_code") if isinstance(manifest, dict) else None
    manifest_parse_failed = isinstance(manifest, dict) and "parse_error" in manifest
    runtime_failed = manifest_parse_failed or bool(errors) or manifest_status == "failed" or (
        manifest_exit_code is not None and manifest_exit_code != 0
    )
    if not run_dir.is_dir() or runtime_failed:
        runtime_status = "fail"
    elif manifest_status == "running":
        runtime_status = "running"
    elif missing:
        runtime_status = "fail"
    elif manifest_status == "completed":
        manifest_normal = manifest.get("normal_termination") if isinstance(manifest, dict) else None
        runtime_status = (
            "pass"
            if manifest_exit_code == 0 and manifest_normal is not False and normal_termination
            else "incomplete"
        )
    elif normal_termination:
        runtime_status = "pass"
    else:
        runtime_status = "incomplete"

    stale_output_names = sorted(candidate_names - current_output_names)
    for details in files.values():
        details.pop("modified_timestamp", None)
    return {
        "run_dir": str(run_dir),
        "runtime_status": runtime_status,
        "physical_status": "pending",
        "normal_termination": normal_termination,
        "normal_termination_evidence": normal_termination_evidence,
        "required": list(required),
        "all_resolved_required": all_resolved_required,
        "resolved_required": resolved_required,
        "missing_or_empty": missing,
        "current_run_outputs": sorted(current_output_names),
        "stale_outputs_ignored": stale_output_names,
        "error_codes": codes["error"],
        "warning_codes": codes["warning"],
        "error_lines": errors,
        "warning_lines": warnings,
        "files": files,
        "manifest_file": manifest_path.name if manifest_path.is_file() else None,
        "manifest": manifest,
        "说明": "Only run files and logs are checked; energy, contact, FSI, deformation, and other physical gates require independent acceptance.",
    }


def print_text(result: dict[str, Any]) -> None:
    print(f"Run directory: {result['run_dir']}")
    print(f"Runtime integrity: {result['runtime_status']}")
    print(f"Normal termination: {result['normal_termination']}")
    print(f"Missing/empty files: {result['missing_or_empty'] or 'none'}")
    print(f"Error codes: {result['error_codes'] or 'none'}")
    print(f"Warning codes: {result['warning_codes'] or 'none'}")
    if result["error_lines"]:
        print("\nError lines:")
        for line in result["error_lines"]:
            print(f"- {line}")
    if result["warning_lines"]:
        print("\nWarning lines (review against the case allowlist):")
        for line in result["warning_lines"]:
            print(f"- {line}")
    print(f"\nPhysical status: {result['physical_status']}")
    print(f"Note: {result['说明']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument(
        "--require",
        action="append",
        help="Required filename; repeatable. Defaults to messag/d3hsp/glstat/matsum.",
    )
    parser.add_argument("--line-limit", type=int, default=40)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the same machine-readable JSON summary to this path, creating parent directories if needed.",
    )
    args = parser.parse_args()

    required = tuple(args.require) if args.require else DEFAULT_REQUIRED
    result = inspect(args.run_dir, required, args.line_limit)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    if result["runtime_status"] in {"pass", "running"}:
        return 0
    return 1 if result["runtime_status"] == "fail" else 2


if __name__ == "__main__":
    raise SystemExit(main())
