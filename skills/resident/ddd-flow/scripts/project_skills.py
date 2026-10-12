"""Audit, plan and apply fixed-source project Skill copies.

The caller must verify the user's approval before apply. CLI arguments and lock
records are consistency evidence, not an authorization service.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path, PurePosixPath

try:
    import tomllib  # Python 3.11+ standard library
except ModuleNotFoundError:  # pragma: no cover - depends on the management runtime
    tomllib = None

SCHEMA = 1
EXIT = {"UNCHANGED": 0, "PLANNED": 0, "APPLIED": 0, "NEEDS_APPROVAL": 2,
        "CONFLICT": 2, "UNAVAILABLE": 3, "RESTORE_FAILED": 4, "INVALID": 1}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class ToolError(Exception):
    def __init__(self, status: str, detail: str):
        super().__init__(detail)
        self.status = status


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def report(status: str, **fields: object) -> int:
    print(json.dumps({"schema_version": SCHEMA, "status": status, **fields}, ensure_ascii=False, sort_keys=True))
    return EXIT[status]


def git(source: Path, *args: str) -> bytes:
    try:
        result = subprocess.run(["git", "-C", str(source), *args], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, check=False)
    except OSError as exc:
        raise ToolError("UNAVAILABLE", f"Git executable unavailable: {exc}") from exc
    if result.returncode:
        raise ToolError("UNAVAILABLE", f"fixed Git source unavailable for {' '.join(args[:2])}")
    return result.stdout


def fixed_commit(source: Path, revision: str) -> str:
    if not SHA40.fullmatch(revision):
        raise ToolError("INVALID", "source_commit must be a full 40-character SHA-1")
    actual = git(source, "rev-parse", "--verify", revision + "^{commit}").decode().strip()
    if actual != revision:
        raise ToolError("INVALID", "source_commit did not resolve exactly")
    return actual


def safe_relative(value: str, prefix: str | None = None) -> PurePosixPath:
    if "\\" in value or value.startswith("/") or ":" in value:
        raise ToolError("INVALID", f"unsafe relative path: {value}")
    path = PurePosixPath(value)
    if not value or any(part in {"", ".", ".."} for part in path.parts):
        raise ToolError("INVALID", f"unsafe relative path: {value}")
    if prefix and not value.startswith(prefix + "/"):
        raise ToolError("INVALID", f"path must be below {prefix}: {value}")
    return path


def linked(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


def safe_target(project: Path, value: str, name: str) -> Path:
    rel = safe_relative(value, ".agents/skills")
    if rel.parts != (".agents", "skills", name):
        raise ToolError("INVALID", f"target must be .agents/skills/{name}")
    current = project
    for part in rel.parts:
        if current.is_dir() and any(child.name.casefold() == part.casefold() and child.name != part
                                    for child in current.iterdir()):
            raise ToolError("CONFLICT", f"case-insensitive path collision below {current}")
        current = current / part
        if linked(current):
            raise ToolError("CONFLICT", f"linked path component: {current}")
    if not current.resolve(strict=False).is_relative_to(project):
        raise ToolError("CONFLICT", "target resolves outside project")
    parent = current.parent
    if parent.is_dir():
        for sibling in parent.iterdir():
            if sibling.name.casefold() == name.casefold() and sibling.name != name:
                raise ToolError("CONFLICT", f"case-insensitive name collision: {sibling.name}")
    return current


def file_tree(path: Path) -> tuple[str | None, dict[str, bytes]]:
    if not path.exists() and not linked(path):
        return None, {}
    if linked(path) or not path.is_dir():
        raise ToolError("CONFLICT", f"target is linked or not a directory: {path}")
    entries: dict[str, bytes] = {}
    for base, dirs, files in os.walk(path, followlinks=False):
        parent = Path(base)
        for dirname in list(dirs):
            child = parent / dirname
            if linked(child):
                raise ToolError("CONFLICT", f"linked target directory: {child}")
        for filename in files:
            child = parent / filename
            if linked(child) or not child.is_file():
                raise ToolError("CONFLICT", f"linked or irregular target file: {child}")
            rel = child.relative_to(path).as_posix()
            if rel.endswith(".pyc") and "__pycache__" in PurePosixPath(rel).parts:
                continue
            entries[rel] = child.read_bytes()
    return tree_digest(entries), entries


def tree_digest(entries: dict[str, bytes]) -> str:
    rows = [{"path": name, "sha256": digest(data), "kind": "file"}
            for name, data in sorted(entries.items())]
    return digest(json_bytes(rows))


def source_tree(source: Path, commit: str, source_path: str) -> tuple[str, dict[str, bytes]]:
    safe_relative(source_path, "skills/non-resident")
    raw = git(source, "ls-tree", "-r", "-z", commit, "--", source_path).split(b"\0")
    entries: dict[str, bytes] = {}
    prefix = source_path + "/"
    for line in raw:
        if not line:
            continue
        header, raw_name = line.split(b"\t", 1)
        mode, kind, object_id = header.decode("ascii").split()
        name = raw_name.decode("utf-8")
        if kind != "blob" or mode not in {"100644", "100755"} or not name.startswith(prefix):
            raise ToolError("CONFLICT", f"unsupported source object: {name}")
        rel = name[len(prefix):]
        safe_relative(rel)
        entries[rel] = git(source, "cat-file", "blob", object_id)
    if not entries or "SKILL.md" not in entries or "VERSION.txt" not in entries:
        raise ToolError("INVALID", f"source Skill is incomplete: {source_path}")
    for name, data in entries.items():
        if not name.endswith(".md"):
            continue
        text = data.decode("utf-8", errors="replace")
        for target in re.findall(r"(?<!!)\[[^]]*]\(([^)]+)\)", text):
            target = target.split("#", 1)[0].strip("<>")
            if (not target or "://" in target or target.startswith("mailto:") or
                    " " in target or "," in target or ("/" not in target and "." not in target)):
                continue
            resolved = (PurePosixPath(name).parent / target)
            parts: list[str] = []
            for part in resolved.parts:
                if part == "..":
                    if not parts:
                        raise ToolError("CONFLICT", f"cross-Skill source link: {name} -> {target}")
                    parts.pop()
                elif part != ".":
                    parts.append(part)
            if "/".join(parts) not in entries:
                raise ToolError("CONFLICT", f"missing local source link: {name} -> {target}")
    return tree_digest(entries), entries


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ToolError("INVALID", f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema_version") != SCHEMA:
        raise ToolError("INVALID", f"unsupported JSON schema: {path}")
    return value


def numeric_version(value: str) -> tuple[int, ...]:
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)*", value):
        raise ToolError("UNAVAILABLE", f"unsupported version syntax: {value}")
    parts = list(map(int, value.split(".")))
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


def marker_applies(marker: str, environment: dict | None) -> bool:
    """Evaluate a bounded marker grammar without guessing the target runtime."""
    if environment is not None and not isinstance(environment, dict):
        raise ToolError("INVALID", "marker_environment must be an explicit target environment object")
    try:
        tree = ast.parse(marker, mode="eval")
    except SyntaxError as exc:
        raise ToolError("UNAVAILABLE", "unsupported dependency marker syntax") from exc
    allowed = {"python_version", "python_full_version", "os_name", "sys_platform",
               "platform_release", "platform_system", "platform_version", "platform_machine",
               "platform_python_implementation", "implementation_name", "implementation_version", "extra"}
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    if not names <= allowed or any(not isinstance((environment or {}).get(name), str) for name in names):
        raise ToolError("UNAVAILABLE", f"explicit target marker_environment required for: {sorted(names)}")

    def operand(node):
        if isinstance(node, ast.Name):
            return environment[node.id]
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        raise ToolError("UNAVAILABLE", "unsupported dependency marker operand")

    def evaluate(node):
        if isinstance(node, ast.BoolOp) and isinstance(node.op, (ast.And, ast.Or)):
            values = [evaluate(value) for value in node.values]
            return all(values) if isinstance(node.op, ast.And) else any(values)
        if not isinstance(node, ast.Compare) or len(node.ops) != 1:
            raise ToolError("UNAVAILABLE", "unsupported dependency marker expression")
        left, right, op = operand(node.left), operand(node.comparators[0]), node.ops[0]
        if isinstance(op, (ast.In, ast.NotIn)):
            result = left in right
            return not result if isinstance(op, ast.NotIn) else result
        version_names = {"python_version", "python_full_version", "implementation_version"}
        numeric = r"[0-9]+(?:\.[0-9]+)*"
        if (re.fullmatch(numeric, left) and re.fullmatch(numeric, right)) or any(
                isinstance(value, ast.Name) and value.id in version_names for value in (node.left, node.comparators[0])):
            left, right = numeric_version(left), numeric_version(right)
        elif re.match(r"[0-9]", left) or re.match(r"[0-9]", right):
            raise ToolError("UNAVAILABLE", "unsupported non-release version in dependency marker")
        operations = {ast.Eq: lambda: left == right, ast.NotEq: lambda: left != right,
                      ast.Lt: lambda: left < right, ast.LtE: lambda: left <= right,
                      ast.Gt: lambda: left > right, ast.GtE: lambda: left >= right}
        if type(op) not in operations:
            raise ToolError("UNAVAILABLE", "unsupported dependency marker operator")
        return operations[type(op)]()

    return evaluate(tree.body)


def explicit_fastapi_version(project: Path, environment: dict | None = None) -> set[str]:
    versions: set[str] = set()
    declarations = []
    pyproject = project / "pyproject.toml"
    if pyproject.is_file():
        if tomllib is None:
            raise ToolError("UNAVAILABLE", "Python 3.11+ management runtime is required for pyproject.toml")
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ToolError("UNAVAILABLE", f"cannot read pyproject.toml: {exc}") from exc
        requirements = data.get("project", {}).get("dependencies", [])
        declarations.extend(map(str, requirements))
    for requirement in project.glob("requirements*.txt"):
        for line in requirement.read_text(encoding="utf-8").splitlines():
            declarations.append(re.split(r"\s+#", line, maxsplit=1)[0])
    constraints, mentioned, applicable = [], False, False
    for declaration in declarations:
        if not re.match(r"\s*fastapi(?=\s|\[|[=<>!~;@]|$)", declaration, re.I):
            continue
        mentioned = True
        requirement, separator, marker = declaration.partition(";")
        if separator and not marker_applies(marker.strip(), environment):
            continue
        applicable = True
        match = re.fullmatch(r"\s*fastapi\s*(?:\[[\w., -]+\])?\s*(.*?)\s*", requirement, re.I)
        if match is None:
            raise ToolError("UNAVAILABLE", "unsupported FastAPI requirement syntax")
        spec = match.group(1)
        if not spec:
            continue  # A lock may resolve an otherwise unconstrained declaration.
        for part in spec.split(","):
            parsed = re.fullmatch(r"\s*(==|!=|>=|<=|>|<)\s*([0-9]+(?:\.[0-9]+)*)\s*", part)
            if not parsed:
                raise ToolError("UNAVAILABLE", f"unsupported FastAPI version constraint: {spec}")
            operator, version = parsed.groups()
            constraints.append((operator, version))
            if operator == "==":
                versions.add(version)
    for filename in ("uv.lock", "poetry.lock"):
        lockfile = project / filename
        if not lockfile.is_file():
            continue
        if tomllib is None:
            raise ToolError("UNAVAILABLE", f"Python 3.11+ management runtime is required for {filename}")
        try:
            packages = tomllib.loads(lockfile.read_text(encoding="utf-8")).get("package", [])
        except (OSError, ValueError) as exc:
            raise ToolError("UNAVAILABLE", f"cannot read {filename}: {exc}") from exc
        for package in packages:
            if isinstance(package, dict) and str(package.get("name", "")).lower() == "fastapi":
                if not mentioned or applicable:
                    version = str(package.get("version", ""))
                    numeric_version(version)
                    versions.add(version)
    if applicable and not versions:
        raise ToolError("UNAVAILABLE", "FastAPI range is unresolved; an applicable exact pin or lock is required")
    for version in versions:
        actual = numeric_version(version)
        for operator, expected in constraints:
            target = numeric_version(expected)
            matches = {"==": actual == target, "!=": actual != target, ">=": actual >= target,
                       "<=": actual <= target, ">": actual > target, "<": actual < target}[operator]
            if not matches:
                raise ToolError("CONFLICT", f"FastAPI version {version} conflicts with {operator}{expected}")
    return versions


def validate_manifest(project: Path, source: Path, manifest: dict) -> tuple[str, list[dict]]:
    commit = fixed_commit(source, str(manifest.get("source_commit", "")))
    if not manifest.get("project_id") or not manifest.get("source_repository"):
        raise ToolError("INVALID", "project_id and source_repository are required")
    skills = manifest.get("skills")
    if not isinstance(skills, list) or not skills:
        raise ToolError("INVALID", "manifest requires selected skills")
    seen: set[str] = set()
    for item in skills:
        if not isinstance(item, dict):
            raise ToolError("INVALID", "skill entry must be an object")
        name = item.get("name")
        if not isinstance(name, str) or not NAME.fullmatch(name) or name.casefold() in seen:
            raise ToolError("INVALID", f"invalid or duplicate skill name: {name}")
        seen.add(name.casefold())
        if item.get("source_path") != f"skills/non-resident/{name}":
            raise ToolError("INVALID", f"source path mismatch for {name}")
        fixed_commit(source, str(item.get("source_commit", commit)))
        safe_target(project, str(item.get("target_path", "")), name)
        if not SHA64.fullmatch(str(item.get("tree_sha256", ""))):
            raise ToolError("INVALID", f"tree_sha256 missing for {name}")
        if not item.get("skill_version") or not item.get("approval_ref"):
            raise ToolError("NEEDS_APPROVAL", f"fixed version and real approval reference required for {name}")
        compatibility = item.get("compatibility")
        if not isinstance(compatibility, dict) or compatibility.get("status") != "verified" or not compatibility.get("evidence"):
            raise ToolError("NEEDS_APPROVAL", f"compatibility evidence required for {name}")
        if name == "fastapi":
            current = explicit_fastapi_version(project, compatibility.get("marker_environment"))
            if current != {"0.136.3"} or compatibility.get("project_version") != "0.136.3":
                raise ToolError("CONFLICT", f"FastAPI target version is not verified as ==0.136.3: {sorted(current)}")
    return commit, skills


def lock_path(project: Path) -> Path:
    result = project / ".planning" / "skills.lock.json"
    for part in (project / ".planning", result):
        if linked(part):
            raise ToolError("CONFLICT", f"linked lock path: {part}")
    return result


def resolved_backup_root(project: Path, global_skills: Path, value: Path) -> Path:
    root = value.resolve(strict=False)
    discovery = (project / ".agents" / "skills").resolve(strict=False)
    if root.is_relative_to(discovery) or root.is_relative_to(global_skills.resolve(strict=False)):
        raise ToolError("INVALID", "backup root must be outside Skill discovery")
    if linked(value) or (root.exists() and not root.is_dir()):
        raise ToolError("CONFLICT", "linked or non-directory backup root")
    return root


def build_plan(project: Path, source: Path, manifest: dict, global_skills: Path,
               backup_root: Path | None = None) -> dict:
    commit, skills = validate_manifest(project, source, manifest)
    lockfile = lock_path(project)
    original_lock = lockfile.read_bytes() if lockfile.is_file() else None
    lock = read_json(lockfile) if original_lock is not None else None
    if lock and (lock.get("project_id") != manifest["project_id"] or
                 lock.get("source_repository") != manifest["source_repository"]):
        raise ToolError("CONFLICT", "existing project Skill lock belongs to a different project or source")
    locked = {item["name"]: item for item in lock.get("skills", [])} if lock else {}
    items = []
    for item in skills:
        name = item["name"]
        item_commit = str(item.get("source_commit", commit))
        target = safe_target(project, item["target_path"], name)
        source_hash, source_files = source_tree(source, item_commit, item["source_path"])
        version = source_files["VERSION.txt"].decode("utf-8").strip()
        if source_hash != item["tree_sha256"] or version != item["skill_version"]:
            raise ToolError("CONFLICT", f"fixed source differs from manifest for {name}")
        target_hash, _ = file_tree(target)
        global_name = global_skills / name
        global_collision = (global_skills.is_dir() and any(
            child.name.casefold() == name.casefold() for child in global_skills.iterdir()))
        if linked(global_name) or global_name.exists() or global_collision:
            raise ToolError("CONFLICT", f"global Skill name also exists: {name}")
        old = locked.get(name)
        if old:
            if (old.get("source_path") != item["source_path"] or
                    old.get("target_path") != item["target_path"]):
                raise ToolError("CONFLICT", f"locked source or target path changed for {name}")
            old_identity = (old.get("source_commit"), old.get("tree_sha256"), old.get("skill_version"))
            if old_identity[0] is None:
                old_identity = (lock.get("source_commit"), old.get("tree_sha256"), old.get("skill_version"))
            if target_hash is not None and target_hash != old.get("tree_sha256"):
                raise ToolError("CONFLICT", f"local target drift for {name}")
            if old_identity == (item_commit, source_hash, version):
                if (old.get("compatibility") != item["compatibility"] or
                        old.get("approval_ref") != item["approval_ref"]):
                    raise ToolError("CONFLICT", f"locked compatibility or approval reference changed for {name}")
                operation = "UNCHANGED" if target_hash == source_hash else "RESTORE"
            else:
                operation = "UPGRADE"
        else:
            if target_hash is not None and target_hash != source_hash:
                raise ToolError("CONFLICT", f"unlocked same-name target for {name}")
            operation = "ADOPT" if target_hash == source_hash else "ADD"
        items.append({"name": name, "source_path": item["source_path"], "target_path": item["target_path"],
                      "source_commit": item_commit, "skill_version": version, "source_tree_sha256": source_hash,
                      "target_tree_sha256": target_hash, "operation": operation,
                      "requires_exact_approval": operation in {"ADD", "ADOPT", "UPGRADE"},
                      "approval_ref": item["approval_ref"], "compatibility": item["compatibility"]})
    plan = {"schema_version": SCHEMA, "project": str(project), "project_id": manifest["project_id"],
            "source": str(source), "source_repository": manifest["source_repository"],
            "source_commit": commit, "lock_sha256": digest(original_lock) if original_lock is not None else None,
            "global_skills": str(global_skills), "items": items,
            "recovery": "Back up previous targets and lock outside Skill discovery; restore exact old state on failure"}
    if backup_root is not None:
        plan["backup_root"] = str(resolved_backup_root(project, global_skills, backup_root))
    plan["status"] = "NEEDS_APPROVAL" if any(x["requires_exact_approval"] for x in items) else "PLANNED"
    plan["plan_sha256"] = digest(json_bytes(plan))
    return plan


def write_lock(project: Path, plan: dict) -> None:
    path = lock_path(project)
    existing = read_json(path) if path.is_file() else None
    previous = {item["name"]: item for item in existing.get("skills", [])} if existing else {}
    other = ([{**item, "source_commit": item.get("source_commit", existing["source_commit"])}
              for item in existing.get("skills", []) if item.get("name") not in {x["name"] for x in plan["items"]}]
             if existing else [])
    selected = [{**previous.get(x["name"], {}), "name": x["name"], "source_path": x["source_path"],
                 "target_path": x["target_path"],
                 "source_commit": x["source_commit"], "skill_version": x["skill_version"],
                 "tree_sha256": x["source_tree_sha256"], "compatibility": x["compatibility"],
                 "approval_ref": x["approval_ref"]} for x in plan["items"]]
    value = {**(existing or {}), "schema_version": SCHEMA, "project_id": plan["project_id"],
             "source_repository": plan["source_repository"], "source_commit": plan["source_commit"],
             "skills": sorted(other + selected, key=lambda x: x["name"])}
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("wb", dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
    os.replace(temporary, path)


def apply_plan(plan: dict, approved: set[str], backup_root: Path) -> dict:
    expected_status = "NEEDS_APPROVAL" if any(x["requires_exact_approval"] for x in plan.get("items", [])) else "PLANNED"
    if plan.get("status") != expected_status:
        raise ToolError("INVALID", "plan status does not match its operations")
    identity = plan.get("plan_sha256")
    unsigned = {key: value for key, value in plan.items() if key != "plan_sha256"}
    if identity != digest(json_bytes(unsigned)):
        raise ToolError("INVALID", "plan content identity is invalid")
    project = Path(plan["project"]).resolve(strict=True)
    source = Path(plan["source"]).resolve(strict=True)
    manifest = {"schema_version": SCHEMA, "project_id": plan["project_id"],
                "source_repository": plan["source_repository"], "source_commit": plan["source_commit"],
                "skills": [{"name": x["name"], "source_path": x["source_path"], "target_path": x["target_path"],
                            "source_commit": x["source_commit"], "skill_version": x["skill_version"],
                            "tree_sha256": x["source_tree_sha256"],
                            "compatibility": x["compatibility"], "approval_ref": x["approval_ref"]}
                           for x in plan["items"]]}
    planned_backup = plan.get("backup_root")
    if not isinstance(planned_backup, str):
        raise ToolError("INVALID", "plan lacks a reviewed backup root; prepare a new plan")
    selected_backup = resolved_backup_root(project, Path(plan["global_skills"]), backup_root)
    if str(selected_backup) != planned_backup:
        raise ToolError("CONFLICT", "backup root differs from reviewed plan")
    current = build_plan(project, source, manifest, Path(plan["global_skills"]), selected_backup)
    if current != plan:
        raise ToolError("CONFLICT", "source, target, lock or plan context drifted; prepare a new plan")
    for item in plan["items"]:
        if item["requires_exact_approval"] and item["name"] not in approved:
            raise ToolError("NEEDS_APPROVAL", f"exact plan approval required for {item['name']}")
    operations = [x for x in plan["items"] if x["operation"] != "UNCHANGED"]
    if not operations:
        return {"status": "UNCHANGED", "items": plan["items"]}
    backup_root = selected_backup
    session = backup_root / ("project-skills-" + uuid.uuid4().hex)
    session.mkdir(parents=True, exist_ok=False)
    lockfile = lock_path(project)
    old_lock = lockfile.read_bytes() if lockfile.is_file() else None
    if old_lock is not None:
        (session / "skills.lock.json.before").write_bytes(old_lock)
    changed: list[tuple[Path, Path | None]] = []
    try:
        for item in operations:
            target = safe_target(project, item["target_path"], item["name"])
            source_hash, files = source_tree(source, item["source_commit"], item["source_path"])
            if source_hash != item["source_tree_sha256"]:
                raise ToolError("CONFLICT", f"source changed for {item['name']}")
            hold = None
            if target.exists():
                copied = session / (item["name"] + ".before")
                shutil.copytree(target, copied)
                if file_tree(copied)[0] != item["target_tree_sha256"]:
                    raise ToolError("CONFLICT", f"backup verification failed for {item['name']}")
                hold = project / ".agents" / (".skill-hold-" + uuid.uuid4().hex)
                os.replace(target, hold)
            changed.append((target, hold))
            target.mkdir(parents=True, exist_ok=False)
            for rel, data in files.items():
                output = target.joinpath(*PurePosixPath(rel).parts)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(data)
            if file_tree(target)[0] != source_hash:
                raise ToolError("CONFLICT", f"copy verification failed for {item['name']}")
        if any(x["operation"] != "RESTORE" for x in operations):
            write_lock(project, plan)
    except Exception as exc:
        restore_errors = []
        for target, hold in reversed(changed):
            try:
                if target.exists():
                    failed = project / ".agents" / (".skill-failed-" + uuid.uuid4().hex)
                    os.replace(target, failed)
                    try:
                        shutil.move(str(failed), str(session / (target.name + ".failed")))
                    except OSError as error:
                        restore_errors.append(f"failed-copy retention {failed}: {error}")
                if hold is not None:
                    os.replace(hold, target)
            except OSError as error:
                restore_errors.append(f"{target}: {error}")
        try:
            if old_lock is None:
                if lockfile.exists():
                    lockfile.unlink()
            else:
                lockfile.write_bytes(old_lock)
        except OSError as error:
            restore_errors.append(f"lock: {error}")
        if restore_errors:
            raise ToolError("RESTORE_FAILED", "; ".join(restore_errors)) from exc
        raise ToolError("CONFLICT", f"apply stopped and restored previous state: {exc}") from exc
    cleanup_pending = []
    for _, hold in changed:
        if hold is not None:
            try:
                shutil.rmtree(hold)
            except OSError:
                cleanup_pending.append(str(hold))
    return {"status": "APPLIED", "backup": str(session), "items": plan["items"],
            "cleanup_pending": cleanup_pending}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("audit", "plan", "apply"):
        command = sub.add_parser(action)
        command.add_argument("--project", required=True, type=Path)
        command.add_argument("--source", required=True, type=Path)
        command.add_argument("--global-skills", type=Path, default=Path.home() / ".agents" / "skills")
        if action == "plan":
            command.add_argument("--manifest", required=True, type=Path)
            command.add_argument("--backup-root", required=True, type=Path)
        if action == "apply":
            command.add_argument("--plan", required=True, type=Path)
            command.add_argument("--approved-change", action="append", default=[], metavar="NAME")
            command.add_argument("--backup-root", type=Path)
    args = parser.parse_args()
    try:
        project = args.project.resolve(strict=True)
        source = args.source.resolve(strict=True)
        if not project.is_dir() or not source.is_dir():
            raise ToolError("UNAVAILABLE", "project and source must be existing directories")
        if args.action == "apply":
            plan = read_json(args.plan)
            if str(project) != plan.get("project") or str(source) != plan.get("source"):
                raise ToolError("CONFLICT", "plan project or source differs from CLI target")
            if str(args.global_skills.resolve(strict=False)) != plan.get("global_skills"):
                raise ToolError("CONFLICT", "global Skill discovery path differs from plan")
            if not isinstance(plan.get("backup_root"), str):
                raise ToolError("INVALID", "plan lacks a reviewed backup root; prepare a new plan")
            result = apply_plan(plan, set(args.approved_change),
                                args.backup_root or Path(plan["backup_root"]))
            return report(**result)
        manifest_path = args.manifest if args.action == "plan" else lock_path(project)
        if args.action == "audit" and not manifest_path.is_file():
            return report("UNCHANGED", items=[], detail="no project Skill lock")
        manifest = read_json(manifest_path)
        plan = build_plan(project, source, manifest, args.global_skills.resolve(strict=False),
                          args.backup_root if args.action == "plan" else None)
        if args.action == "audit":
            status = "UNCHANGED" if all(x["operation"] == "UNCHANGED" for x in plan["items"]) else "PLANNED"
            return report(status, items=plan["items"], source_commit=plan["source_commit"])
        return report(**plan)
    except ToolError as exc:
        return report(exc.status, detail=str(exc))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return report("INVALID", detail=str(exc))


if __name__ == "__main__":
    sys.exit(main())
