#!/usr/bin/env python3
"""Locate and search supplied or environment-discovered official LS-DYNA manuals."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


MANUAL_DIR_ENV = ("LSDYNA_MANUAL_DIRS", "LS_DYNA_MANUAL_DIRS")
MANUAL_NAME_RE = re.compile(r"ls[-_ ]?dyna.*manual.*\.pdf$", re.IGNORECASE)


def environment_manual_dirs() -> list[Path]:
    directories: list[Path] = []
    for name in MANUAL_DIR_ENV:
        value = os.environ.get(name)
        if value:
            directories.extend(Path(item) for item in value.split(os.pathsep) if item)
    for name, value in os.environ.items():
        if re.fullmatch(r"AWP_ROOT\d+", name) and value:
            directories.append(Path(value) / "ansys" / "docu")
    return directories


def manuals_in_directory(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return [path.resolve() for path in directory.glob("*.pdf") if MANUAL_NAME_RE.search(path.name)]


def select_manuals(
    explicit: list[Path] | None,
    manual_dirs: list[Path] | None,
    version_pattern: str | None,
) -> list[Path]:
    candidates: list[Path] = []
    if explicit:
        candidates.extend(path.expanduser().resolve() for path in explicit if path.is_file())
    directories = list(manual_dirs or [])
    if not explicit and not directories:
        directories = environment_manual_dirs()
    for directory in directories:
        candidates.extend(manuals_in_directory(directory.expanduser()))

    unique = sorted(set(candidates), key=lambda path: str(path).lower())
    if version_pattern:
        pattern = re.compile(version_pattern, re.IGNORECASE)
        unique = [path for path in unique if pattern.search(path.name)]
    return unique


def extract_text(path: Path) -> str:
    pdftotext = shutil.which("pdftotext")
    if pdftotext:
        result = subprocess.run(
            [pdftotext, "-layout", str(path), "-"],
            check=True,
            capture_output=True,
            text=True,
            errors="replace",
        )
        return result.stdout
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit("PDF text extraction requires pdftotext or pypdf.") from exc
    return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)


def compact_excerpt(text: str, start: int, end: int, context: int) -> str:
    excerpt = text[max(0, start - context) : min(len(text), end + context)]
    excerpt = re.sub(r"[ \t]+", " ", excerpt)
    return re.sub(r"\n{3,}", "\n\n", excerpt).strip()


def locate(manuals: list[Path]) -> int:
    if not manuals:
        print("No manuals found; use --manual, --manual-dir, or a manual-directory environment variable.", file=sys.stderr)
        return 2
    for manual in manuals:
        print(manual)
    return 0


def search(manuals: list[Path], query: str, max_matches: int, context: int) -> int:
    if not manuals:
        return locate(manuals)
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    count = 0
    for manual in manuals:
        try:
            text = extract_text(manual)
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"Could not read {manual}: {exc}", file=sys.stderr)
            continue
        for match in pattern.finditer(text):
            count += 1
            print(f"\n--- Match {count} | Official manual: {manual}")
            print(compact_excerpt(text, match.start(), match.end(), context))
            if count >= max_matches:
                return 0
    if count == 0:
        print(f"No match: {query}", file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manual", action="append", type=Path, help="Manual PDF; repeatable")
    parser.add_argument("--manual-dir", action="append", type=Path, help="Manual directory; repeatable")
    parser.add_argument("--version-pattern", help="Filter versions by filename regex, e.g. R14|R15")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("locate", help="List discovered manuals")
    search_parser = subparsers.add_parser("search", help="Search manuals")
    search_parser.add_argument("query", help="LS-DYNA keyword or phrase")
    search_parser.add_argument("--max", type=int, default=5, dest="max_matches")
    search_parser.add_argument("--context", type=int, default=700)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manuals = select_manuals(args.manual, args.manual_dir, args.version_pattern)
    if args.command == "locate":
        return locate(manuals)
    return search(manuals, args.query, args.max_matches, args.context)


if __name__ == "__main__":
    raise SystemExit(main())
