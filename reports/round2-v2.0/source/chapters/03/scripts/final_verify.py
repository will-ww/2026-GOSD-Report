from pathlib import Path
import csv, hashlib, json, re, unicodedata
import fitz

R = Path(__file__).resolve().parents[1]
Q = R / 'review'
P = R / 'output/GOSD_2026_第三章_清洁整理_v0.1_评审稿.pdf'
doc = fitz.open(P)
text = unicodedata.normalize('NFKC', ''.join(p.get_text() for p in doc)).replace('‐', '-').replace('‑', '-')
layout = json.loads((Q / 'layout_checks.json').read_text())
assert len(doc) == 40 and layout['pages'] == 40
assert layout['a3_pages'] == [31, 32]
assert not layout['warnings'] and not layout['glyph_or_bounds_issues']
assert not any(s in text for s in ['方法与证据边界', '来源索引', '见章末'])
body = (R / 'content/chapter3_body.tex').read_text()
captions = [int(n) for n in re.findall(r'\}\{图3-(\d+)\b', body)]
assert sorted(captions + [32, 33]) == list(range(1, 41)), captions
normalized = re.sub(r'\s+', '', text)
assert all(f'图3-{n}' in normalized for n in range(1, 41))
assert '31.4%' in doc[25].get_text() and '兼容维护容量' in doc[25].get_text()
font_lines = (Q / 'fonts.txt').read_text().splitlines()[2:]
unembedded = [line for line in font_lines if line.strip() and line.split()[-5] != 'yes']
assert not unembedded, unembedded

preservation = json.loads((Q / 'source_preservation.json').read_text())
for item in preservation['entries']:
    path = R / 'sources' / item['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], str(path)
assert len(preservation['entries']) == 1668
matrix = json.loads((Q / 'rank_matrix_cells.json').read_text())
data_root = R / 'sources/s3.2/ch32_v03/data'
tables = {}
for cell in matrix['cells']:
    filename = cell['source']
    if filename not in tables:
        rows = list(csv.DictReader((data_root / filename).open()))
        key = 'month' if 'month' in rows[0] else 'year'
        tables[filename] = {row[key]: row for row in rows}
    raw = tables[filename][cell['period']][cell['entity']]
    assert raw == cell['raw']
    assert cell['display'] == (int(float(raw)) if raw else None)
assert len(matrix['cells']) == 460
emerging = json.loads((Q / 'emerging_rank_rows.json').read_text())
for kind in ['project', 'repo']:
    raw = list(csv.DictReader((R / f'sources/s3.5/GOSD_3.5_v0.5/data/new_{kind}.csv').open()))
    plotted = [x for x in emerging['rows'] if x['kind'] == kind]
    assert len(raw) == len(plotted) == 30
    for a, b in zip(raw, plotted):
        assert a[kind] == b['identity']
        assert float(a['openrank']) == b['openrank']
        assert int(a['active_developers']) == b['active_developers']
        assert b['logo']
        if kind == 'project':
            assert a['repo_count'] == b['repo_count']
for path in (Q / 'pages').glob('*.png'):
    if int(path.stem) > len(doc):
        path.unlink()
for path in (Q / 'contacts').glob('*.png'):
    if int(path.stem.split('_')[0]) > len(doc):
        path.unlink()
result = {
    'version': 'v0.1', 'date': '2026-11-07', 'status': 'review_not_published',
    'pdf_sha256': hashlib.sha256(P.read_bytes()).hexdigest(),
    'pages': 40, 'a3_pages': [31, 32], 'numbered_figures': 40,
    'redrawn_figures': [12, 13, 14, 34, 35],
    'all_fonts_embedded': True, 'font_objects': len(font_lines),
    'missing_glyphs_or_overfull_boxes': [], 'all_non_theme_backmatter_removed': True,
    'unchanged_source_files': 1668, 'rank_matrix_cells_preserved': 460,
    'emerging_records_preserved': 60,
    'visual_review': '40 页总览；矩阵、合并页、新势力榜单、两张 A3 及章末回望重点检查通过。',
    'verification_scope': '排版、可追溯性与固定输入一致性；不表示全部上游数据或研究主张独立核验完成。'
}
(Q / 'final_verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps(result, ensure_ascii=False, indent=2))
