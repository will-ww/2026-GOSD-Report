"""Verify and export corrected modules, not a complete book or a PDF.

Latest frontmatter and annual-change sources are inherited via changes.json.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[5]


def source_path(root, relative):
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()) or target == root.resolve():
        raise ValueError('Unsafe source path: ' + relative)
    return target


def verify_overlay():
    manifest = json.loads((ROOT / 'changes.json').read_text(encoding='utf-8'))
    base = source_path(REPO, manifest['source_archive'])
    inherited = source_path(REPO, str((ROOT / manifest['previous_content_manifest']).relative_to(REPO)))
    previous = json.loads(inherited.read_text(encoding='utf-8'))
    if previous['content_id'] != manifest['previous_content_id']:
        raise ValueError('Inherited content ID mismatch')
    if manifest['content_id'] == previous['content_id']:
        raise ValueError('A source revision needs a new content ID')
    entries = manifest['files']
    seen = set()
    for item in entries:
        rel = Path(item['path'])
        if rel.is_absolute() or '..' in rel.parts or item['path'] in seen:
            raise ValueError('Unsafe overlay path: ' + str(rel))
        seen.add(item['path'])
        for directory, field in [(base, 'before_sha256'), (ROOT / 'source-updates', 'after_sha256')]:
            # These are UTF-8 text sources; Git may check them out with CRLF on Windows.
            actual = hashlib.sha256(source_path(directory, str(rel)).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
            if actual != item[field]:
                raise ValueError('Source fingerprint mismatch: ' + str(directory / rel))
    actual = {p.relative_to(ROOT / 'source-updates').as_posix()
              for p in (ROOT / 'source-updates').rglob('*') if p.is_file()}
    if actual != seen:
        raise ValueError('Source manifest does not cover exactly the corrected files')
    return manifest, base


def prepare(target):
    manifest, base = verify_overlay()
    target = target.resolve()
    if not target.is_relative_to(ROOT / 'work') or target == ROOT / 'work':
        raise ValueError('Output must be a new subdirectory of this revision work/')
    if target.exists():
        raise ValueError('Working copy already exists; no files overwritten: ' + str(target))
    target.mkdir(parents=True)
    modules = {Path(item['path']).parts[:2] for item in manifest['files']}
    for parts in sorted(modules):
        rel = Path(*parts)
        shutil.copytree(base / rel, target / rel, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for item in manifest['files']:
        shutil.copy2(str(ROOT / 'source-updates' / item['path']), str(target / item['path']))
    (target / 'source-revision.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared corrected modules (not a complete book): ' + str(target))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify sources without writing output')
    parser.add_argument('--output', type=Path, default=ROOT / 'work' / 'corrected-modules')
    args = parser.parse_args()
    if args.check:
        manifest, _ = verify_overlay()
        print(f"PASS: {manifest['content_id']}; {len(manifest['files'])} corrected source files")
    else:
        prepare(args.output)
