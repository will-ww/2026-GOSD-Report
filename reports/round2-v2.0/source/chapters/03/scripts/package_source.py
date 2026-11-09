from pathlib import Path
import hashlib, json, zipfile

R = Path(__file__).resolve().parents[1]
out = R / 'output/GOSD_2026_第三章_清洁整理_v0.1_源码与核查.zip'
exclude_top = {'output', 'work', '.build_fonts'}
exclude_suffix = {'.aux', '.log', '.out', '.toc', '.synctex.gz', '.pyc'}
paths = []
for path in R.rglob('*'):
    if not path.is_file():
        continue
    rel = path.relative_to(R)
    if rel.parts[0] in exclude_top or '__pycache__' in rel.parts:
        continue
    if rel.parts[:2] == ('review', 'pages'):
        continue
    if rel.parts[0] != 'sources' and path.suffix in exclude_suffix:
        continue
    if rel.as_posix() == 'review/package_manifest.json':
        continue
    paths.append(path)
manifest = [{'path': str(p.relative_to(R)), 'bytes': p.stat().st_size,
             'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]
mf = R / 'review/package_manifest.json'
mf.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=7) as archive:
    for path in sorted(paths) + [mf]:
        archive.write(path, 'GOSD_Chapter3_Clean_v0.1/' + str(path.relative_to(R)))
with zipfile.ZipFile(out) as archive:
    assert archive.testzip() is None
    source_files = [x for x in archive.namelist() if '/sources/' in x]
    assert len(source_files) == 1668, len(source_files)
print(json.dumps({'zip': str(out), 'files': len(paths) + 1,
                  'bytes': out.stat().st_size, 'source_files': len(source_files),
                  'sha256': hashlib.sha256(out.read_bytes()).hexdigest()}, ensure_ascii=False))
