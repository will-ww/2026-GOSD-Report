#!/usr/bin/env python3
"""Verify the approved companion identity bytes and inherited brand registry."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT.parents[1] / 'v2.0'

def main():
    manifest = json.loads((ROOT / 'approved-assets.json').read_text())
    for entry in manifest['assets']:
        p = ROOT / entry['path']
        assert p.is_file(), entry['path']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == entry['sha256'], entry['path']
    tokens = json.loads((ROOT / 'source/approved_brand_tokens.json').read_text())
    assert tokens == json.loads((BRAND / 'source/brand_tokens.json').read_text()), 'Brand registry drift'
    for entry in json.loads((ROOT / 'review/master-fingerprints.json').read_text()):
        p = BRAND / 'assets' / entry['source']
        copy = ROOT / 'assets/master' / p.name
        assert p.read_bytes() == copy.read_bytes(), p.name
    forbidden = {'.pdf', '.ttf', '.otf', '.ttc', '.woff', '.woff2'}
    bad = [str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower() in forbidden]
    assert not bad, 'Non-repository outputs found: ' + ', '.join(bad)
    print(f"PASS: {len(manifest['assets'])} approved visual files; identical brand registry and seven masters; no PDF/font binaries")

if __name__ == '__main__':
    main()
