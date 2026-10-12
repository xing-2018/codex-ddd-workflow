"""Windows package inventory and file integrity checks."""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
from pathlib import Path, PurePosixPath

NAME = 'codex-ddd-workflow'
SEMVER = re.compile(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)')


class DistributionError(ValueError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def identity(value: object) -> str:
    return sha256(json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':')).encode())


def linked(path: Path) -> bool:
    return path.is_symlink() or (path.exists() and bool(getattr(path.lstat(), 'st_file_attributes', 0)
                                                      & stat.FILE_ATTRIBUTE_REPARSE_POINT))


def contained(path: Path, root: Path) -> Path:
    path, root = path.absolute(), root.absolute()
    if '..' in path.parts or '..' in root.parts or not path.is_relative_to(root):
        raise DistributionError('Path leaves its approved boundary')
    for entry in (root, *root.parents):
        if linked(entry):
            raise DistributionError('Linked boundary is not supported')
    for part in path.relative_to(root).parts:
        root = root / part
        if linked(root):
            raise DistributionError('Linked path is not supported')
    return path


def relative_path(value: str) -> str:
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise DistributionError('Invalid relative file path')
    parts = PurePosixPath(value).parts
    if (value.startswith('/') or any(p in {'..', '.'} or p.endswith(('.', ' ')) for p in parts)
            or PurePosixPath(value).as_posix() != value
            or any(re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', p, re.I) for p in parts)):
        raise DistributionError('Unsafe Windows file path')
    return value


def inventory(path: Path) -> dict[str, str] | None:
    contained(path, path.parent)
    if not path.exists():
        return None
    if path.is_file():
        return {'': sha256(path.read_bytes())}
    result = {}
    for directory, dirs, files in os.walk(path):
        for name in dirs + files:
            contained(Path(directory) / name, path)
        for name in files:
            entry = Path(directory) / name
            result[entry.relative_to(path).as_posix()] = sha256(entry.read_bytes())
    return dict(sorted(result.items()))


def component_files(files: dict[str, str], component: dict) -> dict[str, str]:
    prefix = component['path']
    if component['kind'] == 'role':
        return {'': files[prefix]}
    return {name[len(prefix) + 1:]: value for name, value in files.items() if name.startswith(prefix + '/')}


def validate_components(components: list, files: dict[str, str]) -> None:
    seen = set()
    for component in components:
        kind, name, path = component['kind'], component['name'], component['path']
        fields = {'kind', 'name', 'path'} | ({'version'} if kind != 'role' else set())
        if set(component) != fields:
            raise DistributionError('Unsupported component fields')
        if not re.fullmatch(r'[a-z][a-z0-9-]*', name) or (kind, name) in seen:
            raise DistributionError('Duplicate or invalid component')
        seen.add((kind, name))
        if kind in {'resident', 'non-resident'}:
            if path != f'skills/{kind}/{name}' or not SEMVER.fullmatch(component['version']):
                raise DistributionError('Invalid Skill identity')
            expected = component_files(files, component)
            if 'SKILL.md' not in expected or 'VERSION.txt' not in expected:
                raise DistributionError('Incomplete Skill component')
        elif kind == 'role':
            if path != f'subagents/{name}.toml' or path not in files:
                raise DistributionError('Invalid role identity')
        else:
            raise DistributionError('Unknown component kind')
    for name in files:
        parts = PurePosixPath(name).parts
        if parts[0] == 'skills' and (len(parts) < 4 or (parts[1], parts[2]) not in seen):
            raise DistributionError('Unregistered Skill payload')
        if name.startswith('subagents/') and name.endswith('.toml') and ('role', Path(name).stem) not in seen:
            raise DistributionError('Unregistered role payload')


def load_package(root: Path) -> dict:
    """Discover the chosen checkout and snapshot all delivered files."""
    root = contained(root.absolute(), root.absolute().parent)
    allowed = {'VERSION.txt', 'README.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md',
               'AGENTS.md', 'AGENTS_zh.md', 'AGENTS.global.md', 'AGENTS.global_zh.md',
               '.gitignore', 'docs', 'scripts', 'skills', 'subagents'}
    ignored = {'.git', '.local-artifacts', '.venv', '__pycache__'}
    files = {}
    for directory, dirs, names in os.walk(root):
        for name in dirs + names:
            contained(Path(directory) / name, root)
            if Path(directory) == root and name not in allowed | ignored:
                raise DistributionError(f'Unexpected package entry: {name}')
        dirs[:] = [name for name in dirs if name not in ignored]
        for name in names:
            if name in ignored:
                continue
            path = Path(directory) / name
            relative = relative_path(path.relative_to(root).as_posix())
            if relative.split('/')[0] not in allowed:
                raise DistributionError(f'Unexpected package file: {relative}')
            files[relative] = sha256(path.read_bytes())
    if len({name.casefold() for name in files}) != len(files):
        raise DistributionError('Case-insensitive path collision')
    release = contained(root / 'VERSION.txt', root).read_text(encoding='utf-8').strip()
    if not SEMVER.fullmatch(release):
        raise DistributionError('Invalid package version')
    components = []
    for kind in ('resident', 'non-resident'):
        base = root / 'skills' / kind
        if not base.exists():
            continue
        for directory in sorted(base.iterdir()):
            if not directory.is_dir() or directory.name == '__pycache__':
                raise DistributionError('Unexpected Skill directory entry')
            version = contained(directory / 'VERSION.txt', root).read_text(encoding='utf-8').strip()
            components.append({'kind': kind, 'name': directory.name,
                               'path': directory.relative_to(root).as_posix(), 'version': version})
    roles = root / 'subagents'
    if roles.exists():
        for path in sorted(roles.iterdir()):
            if not path.is_file() or path.suffix != '.toml':
                raise DistributionError('Unexpected role directory entry')
            components.append({'kind': 'role', 'name': path.stem,
                               'path': path.relative_to(root).as_posix()})
    if not any(c['kind'] == 'resident' for c in components):
        raise DistributionError('No resident Skills found')
    validate_components(components, files)
    commit = None
    if (root / '.git').exists():
        env = os.environ.copy()
        env['GIT_OPTIONAL_LOCKS'] = '0'
        def git(*args: str) -> bytes:
            result = subprocess.run(['git', '-C', str(root), *args], env=env,
                                    capture_output=True, timeout=30)
            if result.returncode:
                raise DistributionError('Checkout is not clean or Git is unavailable')
            return result.stdout
        if Path(git('rev-parse', '--show-toplevel').decode().strip()).resolve() != root.resolve():
            raise DistributionError('The package must be its own checkout')
        git('diff', '--no-ext-diff', '--exit-code', '--cached', 'HEAD', '--')
        git('diff', '--no-ext-diff', '--exit-code', '--')
        tracked = set(git('ls-files', '-z').decode('utf-8').rstrip('\0').split('\0'))
        if tracked != set(files):
            raise DistributionError('Tracked files differ from the chosen package')
        commit = git('rev-parse', 'HEAD').decode().strip()
    return {'name': NAME, 'release': release, 'platform': 'Windows',
            'files': dict(sorted(files.items())), 'payload_sha256': identity(files),
            'components': components, 'checkout_commit': commit}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
