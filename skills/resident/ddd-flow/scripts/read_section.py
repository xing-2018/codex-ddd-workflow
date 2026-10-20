"""Read exact ATX Markdown sections without returning the rest of the file."""
from pathlib import Path
import argparse
import hashlib
import re
import sys


def headings(lines):
    fence = None
    for index, line in enumerate(lines):
        delimiter = re.fullmatch(r' {0,3}(`{3,}|~{3,})(.*)', line)
        if fence:
            if delimiter and delimiter[1][0] == fence[0] and len(delimiter[1]) >= len(fence) and not delimiter[2].strip():
                fence = None
            continue
        if delimiter and (delimiter[1][0] == '~' or '`' not in delimiter[2]):
            fence = delimiter[1]
            continue
        match = re.fullmatch(r' {0,3}(#{1,6})(?:[ \t]+(.*))?', line)
        if match:
            title = match[2] or ''
            title = '' if re.fullmatch(r'#+[ \t]*', title) else re.sub(r'[ \t]+#+[ \t]*$', '', title).strip()
            yield index, len(match[1]), title


def read_sections(path, titles):
    raw = path.read_bytes()
    lines = re.split(r'\r\n?|\n', raw.decode('utf-8-sig'))
    if not lines[-1]:
        lines.pop()
    entries = list(headings(lines))
    source = f'SOURCE {path} sha256={hashlib.sha256(raw).hexdigest()}'
    ranges = []
    failures = []
    for heading in titles:
        matches = [entry for entry in entries if entry[2] == heading]
        if not matches:
            failures.append(f'ATX heading {heading!r} not found')
            continue
        if len(matches) > 1:
            numbers = ', '.join(str(index + 1) for index, _, _ in matches)
            failures.append(f'Heading {heading!r} is ambiguous at lines {numbers}')
            continue
        start, level, _ = matches[0]
        end = next((index for index, depth, _ in entries if index > start and depth <= level), len(lines))
        ranges.append((start, end))
    merged = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return source, lines, entries, merged, failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path, nargs='?')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--heading', action='append', help='Exact, case-sensitive ATX heading text; repeat for multiple sections; inline Markdown is literal')
    mode.add_argument('--list-headings', action='store_true', help='List ATX headings and line numbers only')
    mode.add_argument('--section', nargs=2, action='append', metavar=('PATH', 'HEADING'),
                      help='Read sections across files; repeat pairs instead of supplying a positional path')
    args = parser.parse_args()
    if args.section and args.path is not None:
        parser.error('--section cannot be combined with a positional path')
    if not args.section and args.path is None:
        parser.error('path is required with --heading or --list-headings')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    requests = {}
    pairs = args.section or [(args.path, title) for title in (args.heading or [None])]
    for filename, title in pairs:
        try:
            path = Path(filename).resolve()
        except OSError as error:
            parser.error(f'Cannot read {filename}: {error}')
        titles = requests.setdefault(path, [])
        if title is not None:
            titles.append(title)
    documents = []
    for path, titles in requests.items():
        try:
            documents.append(read_sections(path, titles))
        except (OSError, UnicodeError) as error:
            parser.error(f'Cannot read {path}: {error}')
    # Validate the complete request before emitting any source body.
    if any(failures for _, _, _, _, failures in documents):
        for source, _, entries, _, failures in documents:
            if not failures:
                continue
            print(source, file=sys.stderr)
            for failure in failures:
                print(f'ERROR {failure}', file=sys.stderr)
            print('Available exact headings (no section body was returned):', file=sys.stderr)
            for index, level, title in entries:
                print(f'{index + 1}: {"#" * level} {title}', file=sys.stderr)
        return 2
    for source, lines, entries, ranges, _ in documents:
        if args.list_headings:
            print(source)
            for index, level, title in entries:
                print(f'{index + 1}: {"#" * level} {title}')
        else:
            spans = ','.join(f'{start + 1}-{end}' for start, end in ranges)
            print(f'{source} lines={spans}')
            for start, end in ranges:
                for index in range(start, end):
                    print(f'{index + 1}: {lines[index]}')


if __name__ == '__main__':
    sys.exit(main())
