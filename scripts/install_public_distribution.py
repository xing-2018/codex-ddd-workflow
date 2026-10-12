"""Codex-managed Windows installation; arguments do not constitute user consent."""
from __future__ import annotations

import argparse
import json
import os
import re
import uuid
from pathlib import Path
try:
    from scripts.public_distribution import (DistributionError, component_files, contained,
                                            identity, inventory, load_package, relative_path, SEMVER, sha256, write_json)
except ModuleNotFoundError:
    from public_distribution import (DistributionError, component_files, contained,
                                     identity, inventory, load_package, relative_path, SEMVER, sha256, write_json)


def read_receipt(path: Path, component: dict, target: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        record = json.loads(path.read_bytes())
        if (set(record) != {'schema', 'kind', 'name', 'target', 'version', 'files'}
                or record['schema'] != 1 or record['kind'] != component['kind']
                or record['name'] != component['name'] or record['target'] != str(target)
                or not SEMVER.fullmatch(record['version']) or not isinstance(record['files'], dict)):
            raise ValueError('Unsupported receipt')
        for name, digest in record['files'].items():
            if component['kind'] == 'role':
                if name != '':
                    raise ValueError('Invalid role receipt')
            else:
                relative_path(name)
            if not re.fullmatch(r'[0-9a-f]{64}', digest):
                raise ValueError('Invalid file identity')
        if not record['files'] or (component['kind'] != 'role' and 'VERSION.txt' not in record['files']):
            raise ValueError('Incomplete receipt')
        return record
    except (OSError, TypeError, KeyError, ValueError) as error:
        raise DistributionError(f'Installation receipt needs review: {path}') from error


def build_plan(package: Path, home: Path, *, mode: str = 'skills', project: Path | None = None,
               names: list[str] | None = None, codex_home: Path | None = None) -> dict:
    record = load_package(package)
    home = home.absolute()
    codex_home = (codex_home or home / '.codex').absolute()
    if mode not in {'skills', 'workflow', 'project'}:
        raise DistributionError('Unknown installation mode')
    if mode == 'project':
        if not project or not project.is_dir() or not names or len(set(names)) != len(names):
            raise DistributionError('Project mode needs an existing named project and unique Skill names')
        project = project.absolute()
        selected = [c for c in record['components'] if c['kind'] == 'non-resident' and c['name'] in names]
        if {c['name'] for c in selected} != set(names):
            raise DistributionError('Requested project Skill is unavailable')
    else:
        if project or names:
            raise DistributionError('Project selection is only available in project mode')
        selected = [c for c in record['components'] if c['kind'] == 'resident'
                    or (mode == 'workflow' and c['kind'] == 'role')]
    items = []
    for component in selected:
        role = component['kind'] == 'role'
        skill_home = project if mode == 'project' else home
        target = (codex_home / 'agents' / (component['name'] + '.toml') if role
                  else skill_home / '.agents/skills' / component['name'])
        boundary = codex_home if role else skill_home / '.agents'
        contained(target, boundary)
        expected = component_files(record['files'], component)
        before = inventory(target)
        caches = {p: h for p, h in (before or {}).items() if p not in expected
                  and '__pycache__' in Path(p).parts and p.endswith('.pyc')}
        managed = {p: h for p, h in (before or {}).items() if p not in caches}
        receipt_path = contained(boundary / 'installation-receipts' /
                                 (('role-' if role else 'skill-') + component['name'] + '.json'), boundary)
        if receipt_path.parent.exists() and not receipt_path.parent.is_dir():
            raise DistributionError('Installation receipt directory needs review')
        receipt = read_receipt(receipt_path, component, target)
        if receipt and before is not None and not role and receipt['files'] == managed:
            if (target / 'VERSION.txt').read_text(encoding='utf-8').strip() != receipt['version']:
                raise DistributionError('Installation receipt version differs from the target')
        version = record['release'] if role else component['version']
        state = 'missing' if before is None else ('same' if managed == expected else 'conflict')
        if receipt and before is not None and receipt['files'] != managed:
            state = 'conflict'
        elif state == 'conflict' and receipt and receipt['files'] == managed:
            old_version, new_version = (tuple(map(int, value.split('.')))
                                        for value in (receipt['version'], version))
            state = 'trusted-old' if new_version > old_version else 'version-conflict'
        if state == 'conflict' and not role and target.is_dir() and (target / 'VERSION.txt').is_file():
            old_version = (target / 'VERSION.txt').read_text(encoding='utf-8').strip()
            if SEMVER.fullmatch(old_version):
                before_version, after_version = (tuple(map(int, value.split('.')))
                                                for value in (old_version, version))
                if before_version >= after_version:
                    state = 'newer' if before_version > after_version else 'version-conflict'
        if mode == 'project' and inventory(home / '.agents/skills' / component['name']) is not None:
            state = 'global-name-conflict'
        items.append({'kind': component['kind'], 'name': component['name'], 'source': component['path'],
                      'target': str(target), 'boundary': str(boundary), 'expected': expected,
                      'before': before, 'caches': caches, 'state': state,
                      'version': version, 'receipt_path': str(receipt_path),
                      'receipt_before': inventory(receipt_path), 'receipt': receipt,
                      'backup_root': str(boundary / ('installation-backups' if role else 'skill-backups'))})
    plan = {'schema': 2, 'release': record['release'], 'payload_sha256': record['payload_sha256'],
            'checkout_commit': record['checkout_commit'],
            'mode': mode, 'home': str(home), 'codex_home': str(codex_home),
            'project': str(project) if project else None, 'names': names, 'items': items,
            'guards': {'AGENTS.md': inventory(codex_home / 'AGENTS.md'),
                       'config.toml': inventory(codex_home / 'config.toml')}}
    plan['plan_sha256'] = identity(plan)
    return plan


def apply_plan(package: Path, plan: dict, *, home: Path, write_file=None) -> dict:
    unsigned = {k: v for k, v in plan.items() if k != 'plan_sha256'}
    if identity(unsigned) != plan.get('plan_sha256'):
        raise DistributionError('Plan contents changed')
    current = build_plan(package, home, mode=plan['mode'],
                         project=Path(plan['project']) if plan['project'] else None,
                         names=plan['names'], codex_home=Path(plan['codex_home']))
    if current != plan:
        raise DistributionError('Source, installation targets or user configuration drifted')
    if any(i['state'] not in {'same', 'missing', 'trusted-old'} for i in plan['items']):
        raise DistributionError('Installation conflict; preserve the existing targets')
    write_file = write_file or (lambda path, data: path.write_bytes(data))
    changed = []
    receipt_changes = []
    transaction = uuid.uuid4().hex
    try:
        for item in plan['items']:
            target = Path(item['target'])
            contained(target, Path(item['boundary']))
            if inventory(target) != item['before']:
                raise DistributionError('Target drift immediately before replacement')
            if item['state'] == 'same':
                continue
            backup = contained(Path(item['backup_root']) / transaction / item['name'], Path(item['boundary']))
            backup.mkdir(parents=True, exist_ok=False)
            state = {'item': item, 'backup': backup, 'moved': False, 'created': False}
            changed.append(state)
            write_json(backup / 'installation.json', {'target': str(target), 'before': item['before'],
                                                     'release': plan['release'], 'completed': False})
            if target.exists():
                target.rename(backup / 'original')
                state['moved'] = True
                if inventory(backup / 'original') != item['before']:
                    raise DistributionError('Backup differs from original target')
            target.parent.mkdir(parents=True, exist_ok=True)
            if item['kind'] != 'role':
                target.mkdir(exist_ok=False)
                state['created'] = True
            for relative in item['expected']:
                source = item['source'] + ('/' + relative if relative else '')
                destination = target / relative if item['kind'] != 'role' else target
                contained(destination, Path(item['boundary']))
                destination.parent.mkdir(parents=True, exist_ok=True)
                if item['kind'] == 'role':
                    state['created'] = True
                write_file(destination, (package / source).read_bytes())
            if inventory(target) != item['expected']:
                raise DistributionError('Installed content differs')
        # Recheck the complete unit, including targets that did not require replacement.
        for item in plan['items']:
            after = inventory(Path(item['target']))
            if {p: h for p, h in (after or {}).items() if p not in item['caches']} != item['expected']:
                raise DistributionError('Final target drift')
        if {key: inventory(Path(plan['codex_home']) / key) for key in plan['guards']} != plan['guards']:
            raise DistributionError('User configuration changed during installation')
        for item in plan['items']:
            path = contained(Path(item['receipt_path']), Path(item['boundary']))
            if inventory(path) != item['receipt_before']:
                raise DistributionError('Installation receipt drifted')
            if item['state'] == 'same' and item['receipt'] is not None:
                continue
            backup = contained(Path(item['backup_root']) / transaction / item['name'], Path(item['boundary']))
            original = path.read_bytes() if path.exists() else None
            if original is not None:
                backup.mkdir(parents=True, exist_ok=True)
                (backup / 'receipt-original.json').write_bytes(original)
            receipt_changes.append({'path': path, 'backup': backup, 'before': original,
                                    'before_hash': item['receipt_before'], 'boundary': item['boundary']})
            write_json(path, {'schema': 1, 'kind': item['kind'], 'name': item['name'],
                              'target': item['target'], 'version': item['version'], 'files': item['expected']})
        for item in plan['items']:
            checked = read_receipt(Path(item['receipt_path']), item, Path(item['target']))
            if checked is None or checked['files'] != item['expected']:
                raise DistributionError('Final installation receipt differs')
            after = inventory(Path(item['target']))
            if {p: h for p, h in (after or {}).items() if p not in item['caches']} != item['expected']:
                raise DistributionError('Final target drift')
        if load_package(package)['payload_sha256'] != plan['payload_sha256']:
            raise DistributionError('Source changed during installation')
        if {key: inventory(Path(plan['codex_home']) / key) for key in plan['guards']} != plan['guards']:
            raise DistributionError('User configuration changed during receipt writes')
        for state in changed:
            item = state['item']
            write_json(state['backup'] / 'installation.json', {'target': item['target'], 'before': item['before'],
                                                              'release': plan['release'], 'completed': True})
    except (OSError, DistributionError) as error:
        recovery = []
        for state in reversed(receipt_changes):
            try:
                contained(state['path'], Path(state['boundary']))
                contained(state['backup'], Path(state['boundary']))
                if state['path'].exists():
                    state['backup'].mkdir(parents=True, exist_ok=True)
                    state['path'].rename(state['backup'] / 'receipt-failed.json')
                if state['before'] is not None:
                    state['path'].write_bytes(state['before'])
                if inventory(state['path']) != state['before_hash']:
                    raise DistributionError('Receipt recovery differs from original')
            except (OSError, DistributionError) as restore_error:
                recovery.append(f"{state['backup']}: {restore_error}")
        for state in reversed(changed):
            item, backup = state['item'], state['backup']
            target = Path(item['target'])
            try:
                contained(target, Path(item['boundary']))
                if state['created'] and target.exists():
                    target.rename(backup / 'failed')
                if state['moved']:
                    (backup / 'original').rename(target)
                if inventory(target) != item['before']:
                    raise DistributionError('Recovery differs from original')
                write_json(backup / 'recovery.json', {'restored': True, 'target': str(target)})
            except (OSError, DistributionError) as restore_error:
                recovery.append(f'{backup}: {restore_error}')
        suffix = 'recovery failed: ' + '; '.join(recovery) if recovery else 'unit restored; backups retained'
        raise DistributionError(f'Installation stopped: {error}; {suffix}') from error
    return {'completed': True, 'release': plan['release'], 'updated': len(changed),
            'skipped': len(plan['items']) - len(changed), 'backups': [str(s['backup']) for s in changed],
            'integrity': 'PASS'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parents[1])
    commands = parser.add_subparsers(dest='action', required=True)
    commands.add_parser('verify')
    prepare = commands.add_parser('plan')
    prepare.add_argument('--mode', choices=['skills', 'workflow', 'project'], default='skills')
    prepare.add_argument('--project', type=Path)
    prepare.add_argument('--skills', nargs='+')
    prepare.add_argument('--output', type=Path, required=True)
    apply = commands.add_parser('apply')
    apply.add_argument('--plan', type=Path, required=True)
    apply.add_argument('--plan-sha256', required=True)
    args = parser.parse_args()
    try:
        if os.name != 'nt':
            raise DistributionError('This is the Windows edition; adapt and validate it before use on another platform')
        package = args.package.absolute()
        if args.action == 'verify':
            record = load_package(package)
            print(json.dumps({'checked': True, 'release': record['release'],
                              'payload_sha256': record['payload_sha256'], 'checkout_commit': record['checkout_commit']}))
        elif args.action == 'plan':
            output = contained(args.output.absolute(), package / '.local-artifacts')
            if output.exists():
                raise DistributionError('Plan output must be a new file')
            plan = build_plan(package, Path.home(), mode=args.mode, project=args.project, names=args.skills,
                              codex_home=Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex'))
            write_json(output, plan)
            print(json.dumps({'plan': str(output), 'plan_sha256': plan['plan_sha256'],
                              'items': [{k: i[k] for k in ('kind', 'name', 'target', 'state', 'receipt_path')} for i in plan['items']]},
                             ensure_ascii=False))
        else:
            path = contained(args.plan.absolute(), package / '.local-artifacts')
            plan = json.loads(path.read_text(encoding='utf-8'))
            if plan.get('plan_sha256') != args.plan_sha256:
                raise DistributionError('Approved plan hash differs; a hash is not user consent')
            print(json.dumps(apply_plan(package, plan, home=Path.home()), ensure_ascii=False))
        return 0
    except (DistributionError, KeyError, TypeError, OSError, ValueError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
