#!/usr/bin/env python3
"""Validate the reusable ship-ice-water-air YAML/JSON case interface."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = SKILL_DIR / "assets" / "case-config.schema.json"
CORE_STAGES = ("g0", "g1", "a1", "a2", "b1", "b2", "c")
MINIMUM_OUTPUTS = {"messag", "d3hsp", "glstat", "matsum"}
CORE_KEYS = {
    "schema_version",
    "case",
    "software",
    "geometry",
    "ice",
    "fluid",
    "coupling",
    "run",
    "outputs",
    "acceptance",
    "provenance",
    "extensions",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    path: str
    message: str


def load_data(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        loaded = json.loads(text)
    else:
        try:
            import yaml
        except ImportError as exc:
            raise SystemExit("YAML requires PyYAML; JSON configuration is also supported.") from exc
        try:
            loaded = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML: {exc}") from exc
    if not isinstance(loaded, dict):
        raise ValueError("The configuration root must be an object/mapping.")
    if any(not isinstance(key, str) for key in loaded):
        raise ValueError("Configuration field names must be strings.")
    return loaded


def nested(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def add(findings: list[Finding], severity: str, path: str, message: str) -> None:
    findings.append(Finding(severity, path, message))


def schema_validate(data: dict[str, Any], schema_path: Path, findings: list[Finding]) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        import jsonschema
    except ImportError:
        add(
            findings,
            "warning",
            "$schema",
            "jsonschema is unavailable; full JSON Schema validation was skipped; only built-in core checks ran.",
        )
        return

    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(
        validator.iter_errors(data), key=lambda item: "/".join(map(str, item.path))
    ):
        location = ".".join(str(item) for item in error.absolute_path) or "$"
        add(findings, "error", location, error.message)


def require_values(
    data: dict[str, Any], findings: list[Finding], allow_draft: bool
) -> None:
    required_paths = [
        "case.id",
        "case.title",
        "case.mode",
        "case.unit_system",
        "case.work_dir",
        "case.results_dir",
        "case.report_path",
        "software.solver.executable",
        "software.solver.version",
        "software.solver.precision",
        "software.solver.parallel_mode",
        "software.solver.ncpu",
        "geometry.hull.source.type",
        "geometry.hull.source.uri",
        "geometry.hull.physical_model",
        "geometry.hull.open_deck",
        "geometry.hull.mesh.strategy",
        "geometry.hull.mesh.target_size",
        "run.target_speed",
        "run.speed_curve.mode",
        "run.speed_curve.full_speed_time",
        "run.termination_time",
        "outputs.binary_interval",
        "outputs.ascii_interval",
        "outputs.contact_load.source",
        "provenance.adapter.name",
        "provenance.adapter.version",
        "provenance.adapter.output_hash",
    ]
    if nested(data, "ice.enabled") is True:
        required_paths.extend(
            [
                "ice.generator.name",
                "ice.generator.version",
                "ice.generator.config_uri",
                "ice.generator.seed",
                "ice.field.domain_min",
                "ice.field.domain_max",
                "ice.field.floe_count",
                "ice.field.target_concentration",
                "ice.deformable",
                "ice.mesh.strategy",
                "ice.mesh.target_size",
                "ice.material.model",
            ]
        )
    if nested(data, "fluid.enabled") is True:
        required_paths.extend(
            [
                "fluid.method",
                "fluid.domain_min",
                "fluid.domain_max",
                "fluid.mesh.strategy",
                "fluid.mesh.target_size",
                "fluid.still_water_level",
                "fluid.gravity",
                "fluid.pressure_reference.mode",
                "fluid.pressure_reference.ambient_value",
            ]
        )

    missing = [path for path in required_paths if nested(data, path) in (None, "")]
    if allow_draft and missing:
        preview = ", ".join(missing[:12])
        suffix = f" ({len(missing)} items in total)" if len(missing) > 12 else ""
        add(findings, "warning", "$draft", f"Awaiting project input: {preview}{suffix}.")
        return
    for path in missing:
        add(findings, "error", path, "Must be supplied by the case or project adapter.")


def core_shape_checks(data: dict[str, Any], findings: list[Finding]) -> None:
    missing = sorted(CORE_KEYS - set(data))
    unknown = sorted(set(data) - CORE_KEYS)
    if missing:
        add(findings, "error", "$", "Missing top-level fields: " + ", ".join(missing))
    if unknown:
        add(findings, "error", "$", "Unknown top-level fields: " + ", ".join(unknown))
    if data.get("schema_version") != "1.0":
        add(findings, "error", "schema_version", "Only schema version 1.0 is supported.")

    for key in CORE_KEYS - {"schema_version"}:
        if key in data and not isinstance(data[key], dict):
            add(findings, "error", key, "Must be an object/mapping.")

    case_id = nested(data, "case.id")
    if isinstance(case_id, str) and not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", case_id):
        add(findings, "error", "case.id", "Use only lowercase letters, digits, dots, underscores, and hyphens.")

    enums = {
        "case.mode": {"diagnostic", "verification", "formal"},
        "case.status": {"draft", "pending", "pass", "fail"},
        "software.solver.precision": {"single", "double"},
        "software.solver.parallel_mode": {"smp", "mpp", "hybrid"},
        "fluid.method": {"ale", "eulerian", "cfd_coupled", "none"},
        "fluid.pressure_reference.mode": {"absolute", "gauge"},
        "coupling.water_air_interface": {
            "volume_fraction_advection",
            "explicit_contact",
            "not_applicable",
        },
    }
    for path, allowed in enums.items():
        value = nested(data, path)
        if value is not None and (not isinstance(value, str) or value not in allowed):
            add(findings, "error", path, "Unsupported value: " + repr(value))

    ncpu = nested(data, "software.solver.ncpu")
    if ncpu is not None and (isinstance(ncpu, bool) or not isinstance(ncpu, int) or ncpu < 1):
        add(findings, "error", "software.solver.ncpu", "Must be a positive integer.")
    concentration = nested(data, "ice.field.target_concentration")
    if isinstance(concentration, (int, float)) and not 0 <= concentration <= 1:
        add(findings, "error", "ice.field.target_concentration", "Must be between 0 and 1.")

    for path in ("fluid.materials", "outputs.required_files", "outputs.field_outputs", "provenance.sources"):
        value = nested(data, path)
        if value is not None and not isinstance(value, list):
            add(findings, "error", path, "Must be an array/list.")


def vector_bounds(
    data: dict[str, Any], prefix: str, findings: list[Finding]
) -> None:
    minimum = nested(data, f"{prefix}.domain_min")
    maximum = nested(data, f"{prefix}.domain_max")
    if not isinstance(minimum, list) or not isinstance(maximum, list):
        return
    if len(minimum) != 3 or len(maximum) != 3:
        return
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in minimum + maximum):
        add(findings, "error", prefix, "Domain bounds must contain numeric components.")
        return
    if any(lo >= hi for lo, hi in zip(minimum, maximum, strict=True)):
        add(findings, "error", prefix, "Each domain_min component must be less than domain_max.")


def cross_checks(
    data: dict[str, Any], findings: list[Finding], allow_draft: bool
) -> None:
    mode = nested(data, "case.mode")
    if mode == "formal" and nested(data, "ice.enabled") is True:
        if nested(data, "ice.deformable") is not True:
            add(findings, "error", "ice.deformable", "Ice in a formal case must explicitly be deformable.")

    fluid_method = nested(data, "fluid.method")
    interface = nested(data, "coupling.water_air_interface")
    multi_material = isinstance(fluid_method, str) and fluid_method in {"ale", "eulerian"}
    if multi_material and interface != "volume_fraction_advection":
        add(
            findings,
            "error",
            "coupling.water_air_interface",
            "Multi-material ALE/Eulerian water-air interfaces must use volume_fraction_advection.",
        )

    materials = nested(data, "fluid.materials")
    if nested(data, "fluid.enabled") is True and isinstance(materials, list):
        roles = set()
        for index, item in enumerate(materials):
            if not isinstance(item, dict) or not isinstance(item.get("role"), str):
                add(findings, "error", f"fluid.materials.{index}.role", "Must be a string in a material object.")
                continue
            roles.add(item["role"])
        if multi_material and not {"water", "air"}.issubset(roles):
            add(findings, "error", "fluid.materials", "Water-air cases must declare both water and air.")
        ids = [item.get("id") for item in materials if isinstance(item, dict) and item.get("id") is not None]
        if len(ids) != len(set(map(str, ids))):
            add(findings, "error", "fluid.materials", "Fluid material IDs must be unique.")

    full_speed = nested(data, "run.speed_curve.full_speed_time")
    first_contact = nested(data, "run.expected_first_contact_time")
    termination = nested(data, "run.termination_time")
    if isinstance(full_speed, (int, float)) and isinstance(first_contact, (int, float)):
        if full_speed > first_contact:
            add(findings, "error", "run.speed_curve.full_speed_time", "Target speed is reached after expected first contact.")
    if isinstance(first_contact, (int, float)) and isinstance(termination, (int, float)):
        if termination <= first_contact:
            add(findings, "error", "run.termination_time", "Termination must be later than expected first contact.")

    contact_load = nested(data, "outputs.contact_load")
    if isinstance(contact_load, dict):
        if contact_load.get("preserve_raw") is not True:
            add(findings, "error", "outputs.contact_load.preserve_raw", "Raw loads must be preserved.")
        transformed = [name for name in ("smooth", "interpolate", "fit") if contact_load.get(name)]
        if transformed:
            add(
                findings,
                "warning",
                "outputs.contact_load",
                "Derived processing is enabled; name and report it separately from raw curves: " + ", ".join(transformed),
            )

    required_files = nested(data, "outputs.required_files")
    if isinstance(required_files, list):
        for index, name in enumerate(required_files):
            if not isinstance(name, str):
                add(findings, "error", f"outputs.required_files.{index}", "Must be a filename string.")
        missing = sorted(MINIMUM_OUTPUTS - {name for name in required_files if isinstance(name, str)})
        if missing:
            add(findings, "error", "outputs.required_files", "Missing baseline outputs: " + ", ".join(missing))

    stages = nested(data, "acceptance.stages")
    if isinstance(stages, dict):
        missing_stages = [name for name in CORE_STAGES if name not in stages]
        if missing_stages:
            add(findings, "error", "acceptance.stages", "Missing stages: " + ", ".join(missing_stages))

    sources = nested(data, "provenance.sources")
    if not isinstance(sources, list) or not sources:
        severity = "warning" if allow_draft else "error"
        add(findings, severity, "provenance.sources", "Declare at least one parameter, manual, or project source.")

    vector_bounds(data, "ice.field", findings)
    vector_bounds(data, "fluid", findings)


def local_path(value: Any, base: Path) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    parsed = urlparse(value)
    if parsed.scheme and len(parsed.scheme) > 1:
        return None
    path = Path(value).expanduser()
    return path if path.is_absolute() else (base / path).resolve()


def check_paths(data: dict[str, Any], config_path: Path, findings: list[Finding]) -> None:
    checks = [
        ("software.solver.executable", nested(data, "software.solver.executable"), "file"),
        ("geometry.hull.source.uri", nested(data, "geometry.hull.source.uri"), "any"),
        ("ice.generator.config_uri", nested(data, "ice.generator.config_uri"), "file"),
    ]
    manuals = nested(data, "software.solver.manual_paths")
    if isinstance(manuals, list):
        checks.extend((f"software.solver.manual_paths[{index}]", value, "file") for index, value in enumerate(manuals))

    for key, value, kind in checks:
        path = local_path(value, config_path.parent)
        if path is None:
            continue
        exists = path.is_file() if kind == "file" else path.exists()
        if not exists:
            add(findings, "error", key, f"Path does not exist: {path}")


def result_payload(config_path: Path, findings: list[Finding]) -> dict[str, Any]:
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]
    return {
        "config": str(config_path),
        "status": "fail" if errors else "pass",
        "errors": [asdict(item) for item in errors],
        "warnings": [asdict(item) for item in warnings],
        "manual_checks": [
            "Review geometry, mesh, and keywords against the actual solver version",
            "Independently verify the static water-air domain",
            "Verify hull and ice FSI with independent cases",
            "Provide dynamic fractions, flotation, waves, contact, and energy evidence required by acceptance",
        ],
        "说明": "Interface acceptance does not establish physical acceptance.",
    }


def print_text(result: dict[str, Any]) -> None:
    print(f"Configuration: {result['config']}")
    print(f"Interface validation: {result['status']}")
    for item in result["errors"]:
        print(f"[Error] {item['path']}: {item['message']}")
    for item in result["warnings"]:
        print(f"[Warning] {item['path']}: {item['message']}")
    print("\nStill requires case evidence:")
    for index, item in enumerate(result["manual_checks"], start=1):
        print(f"{index}. {item}")
    print(f"\nNote: {result['说明']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--allow-draft", action="store_true", help="Downgrade null/empty required values to warnings")
    parser.add_argument("--check-paths", action="store_true", help="Check local input and solver paths")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    config_path = args.config.expanduser().resolve()
    schema_path = args.schema.expanduser().resolve()
    findings: list[Finding] = []
    try:
        data = load_data(config_path)
        schema_validate(data, schema_path, findings)
        core_shape_checks(data, findings)
        require_values(data, findings, args.allow_draft)
        cross_checks(data, findings, args.allow_draft)
        if args.check_paths:
            check_paths(data, config_path, findings)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        add(findings, "error", "$", str(exc))

    result = result_payload(config_path, findings)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
