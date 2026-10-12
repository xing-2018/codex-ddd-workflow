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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--heading', action='append', help='Exact, case-sensitive ATX heading text; repeat for multiple sections; inline Markdown is literal')
    mode.add_argument('--list-headings', action='store_true', help='List ATX headings and line numbers only')
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    try:
        path = args.path.resolve()
        raw = path.read_bytes()
        text = raw.decode('utf-8-sig')
        lines = re.split(r'\r\n?|\n', text)
        if not lines[-1]:
            lines.pop()
    except (OSError, UnicodeError) as error:
        parser.error(f'Cannot read {args.path}: {error}')
    entries = list(headings(lines))
    source = f'SOURCE {path} sha256={hashlib.sha256(raw).hexdigest()}'
    if args.list_headings:
        print(source)
        for index, level, title in entries:
            print(f'{index + 1}: {"#" * level} {title}')
        return
    ranges = []
    for heading in args.heading:
        matches = [entry for entry in entries if entry[2] == heading]
        if not matches:
            parser.error(f'ATX heading {heading!r} not found in {path}; use --list-headings to inspect titles')
        if len(matches) > 1:
            numbers = ', '.join(str(index + 1) for index, _, _ in matches)
            parser.error(f'Heading {heading!r} is ambiguous at lines {numbers} in {path}')
        start, level, _ = matches[0]
        end = next((index for index, depth, _ in entries if index > start and depth <= level), len(lines))
        ranges.append((start, end))
    merged = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    spans = ','.join(f'{start + 1}-{end}' for start, end in merged)
    print(f'{source} lines={spans}')
    for start, end in merged:
        for index in range(start, end):
            print(f'{index + 1}: {lines[index]}')


if __name__ == '__main__':
    main()
