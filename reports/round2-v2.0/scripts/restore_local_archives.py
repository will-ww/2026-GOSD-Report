#!/usr/bin/env python3
"""Restore hash-pinned review packages locally; never download or execute them."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, default=ROOT/'work/external-packages')
    args = parser.parse_args()
    manifest = json.loads((ROOT/'provenance/source-manifest.json').read_text())
    validated = []
    for item in manifest['source_packages']:
        path = args.archive_dir/item['filename']
        if path.stat().st_size != item['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise SystemExit('Archive fingerprint mismatch: '+item['filename'])
        with zipfile.ZipFile(path) as zf:
            if zf.testzip():
                raise SystemExit('Invalid ZIP CRC: '+item['filename'])
            for info in zf.infolist():
                member = PurePosixPath(info.filename)
                mode = info.external_attr >> 16
                if member.is_absolute() or '..' in member.parts or '\\' in info.filename or stat.S_ISLNK(mode):
                    raise SystemExit('Unsafe ZIP entry: '+info.filename)
        validated.append(path)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    for path in validated:
        destination = args.output_dir/path.stem
        destination.mkdir()
        with zipfile.ZipFile(path) as zf:
            zf.extractall(destination)
        print('Restored verified local package:', destination)
    print('No source programs were run; restored files remain outside the committed archive.')

if __name__ == '__main__':
    main()
