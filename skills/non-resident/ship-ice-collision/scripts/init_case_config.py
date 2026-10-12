#!/usr/bin/env python3
"""Copy the reusable ship-ice case template to the requested path."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL_DIR / "assets" / "case-config.template.yaml"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="Output YAML path")
    parser.add_argument("--force", action="store_true", help="Allow overwriting an existing file")
    args = parser.parse_args()

    output = args.output.expanduser().resolve()
    if output.exists() and not args.force:
        raise SystemExit(f"Output exists; use --force to overwrite: {output}")
    if not TEMPLATE.is_file():
        raise SystemExit(f"Template not found: {TEMPLATE}")

    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(TEMPLATE, output)
    print(f"Created case configuration template: {output}")
    print("Next: supply project data, then run validate_case_config.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
