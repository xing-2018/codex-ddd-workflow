"""Freeze commit messages and check actual Git delivery metadata; no commit or push."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


class DeliveryError(ValueError):
    pass


def validate_message(data: bytes) -> str:
    """Check mechanical subject constraints; human review still owns meaning."""
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise DeliveryError('Message must be UTF-8') from exc
    if not text or '\x00' in text:
        raise DeliveryError('Message must be nonempty and contain no NUL')
    subject = text.splitlines()[0]
    match = re.fullmatch(r'[a-z][a-z0-9-]*(?:\([^()\r\n]+\))?!?: (\S(?:.*\S)?)', subject)
    if not match:
        raise DeliveryError('Subject must use a conventional type and a nonempty summary')
    if not re.search(r'[\u3400-\u9fff]', match[1]):
        raise DeliveryError('Subject summary must contain Chinese text; manual Simplified Chinese review still required')
    return subject


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inventory(data: bytes, *, index: bool) -> str:
    entries = []
    for entry in filter(None, data.split(b'\0')):
        metadata, path = entry.split(b'\t', 1)
        mode, middle, last = metadata.split(b' ')
        if index and last != b'0':
            raise DeliveryError('Unmerged index cannot be frozen')
        oid = middle if index else last
        entries.append((path, mode, oid))
    return sha256(b''.join(path + b'\0' + mode + b'\0' + oid + b'\0'
                           for path, mode, oid in sorted(entries)))


class DeliveryGate:
    def __init__(self, repository: Path, runner=None):
        self.repository = repository.resolve()
        self.runner = runner or self.run_git
        actual = Path(self.git('rev-parse', '--show-toplevel').decode().strip()).resolve()
        if actual != self.repository:
            raise DeliveryError('Use the resolved repository root')

    def run_git(self, *arguments: str) -> bytes:
        result = subprocess.run(['git', '-C', str(self.repository), *arguments], capture_output=True)
        if result.returncode:
            detail = result.stderr.decode('utf-8', errors='replace').strip()
            raise DeliveryError(f'Git {arguments[0]} failed ({result.returncode}): {detail}')
        return result.stdout

    def git(self, *arguments: str) -> bytes:
        return self.runner(*arguments)

    def resolve(self, reference: str) -> str:
        value = self.git('rev-parse', '--verify', '--end-of-options', reference + '^{commit}').decode().strip()
        if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', value):
            raise DeliveryError('Expected a full commit identity')
        return value

    def freeze(self, message: Path, output: Path) -> dict:
        output = output.resolve()
        if (output == self.repository or not output.is_relative_to(self.repository)
                or '.git' in output.relative_to(self.repository).parts):
            raise DeliveryError('Freeze output must be an authorized task directory inside the repository')
        if output.exists():
            raise DeliveryError('Freeze output exists; preserve it and choose a new attempt')
        data = message.read_bytes().decode('utf-8').replace('\r\n', '\n').encode('utf-8')
        if not data.endswith(b'\n'):
            data += b'\n'
        subject = validate_message(data)
        receipt = {'schema': 1, 'repository': str(self.repository), 'head': self.resolve('HEAD'),
            'index_sha256': inventory(self.git('ls-files', '--stage', '-z'), index=True),
            'message_sha256': sha256(data), 'message_file': 'message.txt',
            'tool_sha256': sha256(Path(__file__).read_bytes())}
        if (self.resolve('HEAD') != receipt['head'] or
                inventory(self.git('ls-files', '--stage', '-z'), index=True) != receipt['index_sha256']):
            raise DeliveryError('HEAD or index drifted during freeze')
        output.mkdir(parents=True)
        (output / 'message.txt').write_bytes(data)
        (output / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return {'operation': 'freeze', 'subject': subject, 'receipt': str(output / 'receipt.json'),
                'message': str(output / 'message.txt'), 'head': receipt['head']}

    def read_commit(self, reference: str) -> tuple[str, dict, bytes]:
        commit = self.resolve(reference)
        headers, message = self.git('cat-file', 'commit', commit).split(b'\n\n', 1)
        tree = next(line[5:].decode() for line in headers.splitlines() if line.startswith(b'tree '))
        parents = [line[7:].decode() for line in headers.splitlines() if line.startswith(b'parent ')]
        return commit, {'tree': tree, 'parents': parents}, message

    def verify(self, receipt: Path, reference: str) -> dict:
        receipt = receipt.resolve()
        if not receipt.is_relative_to(self.repository):
            raise DeliveryError('Receipt must belong to this repository')
        frozen = json.loads(receipt.read_text(encoding='utf-8'))
        fields = {'schema', 'repository', 'head', 'index_sha256', 'message_sha256', 'message_file', 'tool_sha256'}
        if (not isinstance(frozen, dict) or set(frozen) != fields or frozen['schema'] != 1
                or frozen['repository'] != str(self.repository) or frozen['message_file'] != 'message.txt'):
            raise DeliveryError('Receipt schema or repository mismatch')
        if frozen['tool_sha256'] != sha256(Path(__file__).read_bytes()):
            raise DeliveryError('Checker changed after freeze; review the changed evidence')
        message_path = receipt.parent / 'message.txt'
        if message_path.resolve().parent != receipt.parent:
            raise DeliveryError('Frozen message path changed')
        expected = message_path.read_bytes()
        if sha256(expected) != frozen['message_sha256']:
            raise DeliveryError('Frozen message changed after freeze')
        commit, metadata, message = self.read_commit(reference)
        if message != expected:
            raise DeliveryError('Actual commit message differs from the frozen message')
        if metadata['parents'] != [frozen['head']]:
            raise DeliveryError('Actual commit parent differs from the frozen HEAD')
        actual = inventory(self.git('ls-tree', '-r', '-z', metadata['tree']), index=False)
        if actual != frozen['index_sha256']:
            raise DeliveryError('Actual commit tree differs from the frozen index')
        return {'operation': 'verify-commit', 'commit': commit, 'subject': validate_message(message),
                'message_matches': True, 'parent_matches': True, 'tree_matches': True}

    def check_range(self, baseline: str, reference: str) -> dict:
        base, head = self.resolve(baseline), self.resolve(reference)
        self.git('merge-base', '--is-ancestor', base, head)
        commits = self.git('rev-list', '--reverse', base + '..' + head).decode().splitlines()
        subjects, failures = [], []
        for identity in commits:
            commit, _, message = self.read_commit(identity)
            try:
                subjects.append({'commit': commit, 'subject': validate_message(message)})
            except DeliveryError as exc:
                failures.append(f'{commit}: {exc}')
        if failures:
            raise DeliveryError('Commit range failed:\n' + '\n'.join(failures))
        if self.resolve(reference) != head or self.resolve(baseline) != base:
            raise DeliveryError('Commit range drifted during inspection')
        return {'operation': 'check-range', 'base': base, 'head': head,
                'checked': len(subjects), 'subjects': subjects}


def main() -> int:
    # JSON transport must not inherit a Windows console code page.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    freeze = commands.add_parser('freeze', help='Bind a reviewed message to HEAD and staged entries')
    freeze.add_argument('--message', type=Path, required=True)
    freeze.add_argument('--output', type=Path, required=True)
    verify = commands.add_parser('verify-commit', help='Check a normal one-parent commit against its freeze')
    verify.add_argument('--receipt', type=Path, required=True)
    verify.add_argument('--commit', default='HEAD')
    check = commands.add_parser('check-range', help='Check every subject in the exact pending push range')
    check.add_argument('--base', required=True)
    check.add_argument('--head', default='HEAD')
    for command in (freeze, verify, check):
        command.add_argument('--repo', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        gate = DeliveryGate(args.repo)
        if args.operation == 'freeze':
            result = gate.freeze(args.message, args.output)
        elif args.operation == 'verify-commit':
            result = gate.verify(args.receipt, args.commit)
        else:
            result = gate.check_range(args.base, args.head)
    except (OSError, ValueError) as exc:
        parser.exit(2, str(exc) + '\n')
    print(json.dumps({'status': 'PASS', **result}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
