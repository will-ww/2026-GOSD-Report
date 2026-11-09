#!/usr/bin/env python3
"""Validate and join UTF-8 transport parts. Does not execute restored content."""
import argparse
import hashlib
import json
from pathlib import Path


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Explicit destination; existing files are never overwritten.')
    args = parser.parse_args()
    script = Path(__file__).resolve()
    parts_dir = script.parents[1] / 'text-blocks.parts'
    index = json.loads((parts_dir / 'index.json').read_text(encoding='utf-8'))
    if index['filename'] != 'text-blocks.json':
        raise SystemExit('Unexpected original filename.')
    chunks = []
    names = set()
    for part in index['parts']:
        name = part['name']
        if Path(name).name != name or name in names or not name.startswith('part-') or not name.endswith('.txt'):
            raise SystemExit('Invalid or duplicate part filename.')
        names.add(name)
        data = (parts_dir / name).read_bytes()
        if len(data) != part['size'] or sha256(data) != part['sha256']:
            raise SystemExit('Part integrity check failed: ' + name)
        data.decode('utf-8')
        chunks.append(data)
    restored = b''.join(chunks)
    if len(restored) != index['size'] or sha256(restored) != index['sha256']:
        raise SystemExit('Reconstructed file integrity check failed.')
    restored.decode('utf-8')
    # Deployed at archive/source/chapters/05-recovered/scripts/.
    destination = args.output if args.output is not None else script.parents[4] / 'work' / index['filename']
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('xb') as stream:
        stream.write(restored)
    print('Verified and restored: ' + str(destination))
    print('SHA-256: ' + sha256(restored))


if __name__ == '__main__':
    main()
