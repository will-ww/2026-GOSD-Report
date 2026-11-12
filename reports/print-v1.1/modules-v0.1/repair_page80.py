"""Simplify single-paint transparency forms without rasterizing the approved chart.

The Inkscape chart has 10,888 separate isolated groups, one per edge/node.
Each group paints exactly once, with opacity applied by its parent. Inline
those paths under the existing parent opacity; retain fonts, coordinates,
colors, all edges/nodes, and native vector output.
"""
from pathlib import Path
import json, re, hashlib, sys
import fitz
import numpy as np

R = Path(__file__).resolve().parent
OUT = R / 'output/pdf'
QA = R / 'review/page80-check'
QA.mkdir(parents=True, exist_ok=True)


def simplify(doc, page_index):
    page = doc[page_index]
    before = len(page.get_xobjects())
    candidates = []
    for xref, _, _, _ in page.get_xobjects():
        kind, raw = doc.xref_get_key(xref, 'Resources/XObject')
        refs = re.findall(r'/([A-Za-z0-9]+)\s+(\d+)\s+0\s+R', raw)
        if len(refs) > 10000:
            candidates.append((xref, refs))
    if not candidates and before < 100:
        return dict(already_simplified=True, form_objects=before)
    assert len(candidates) == 1, candidates
    parent, refs = candidates[0]
    content = doc.xref_stream(parent).decode('ascii')
    selected = set(re.findall(r'/a[12]\s+gs\s+/(Fm\d+)\s+Do', content))
    assert len(selected) == 5111 + 5777
    retained = [(name, ref) for name, ref in refs if name not in selected]
    replacements = {}
    counts = {'edges': 0, 'nodes': 0}
    for name, ref in refs:
        if name not in selected:
            continue
        ref = int(ref)
        assert doc.xref_get_key(ref, 'Matrix')[0] == 'null'
        assert doc.xref_get_key(ref, 'Resources/XObject')[0] == 'null'
        assert doc.xref_get_key(ref, 'Resources/Font')[0] == 'null'
        assert doc.xref_get_key(ref, 'Group/S') == ('name', '/Transparency')
        assert doc.xref_get_key(ref, 'Group/I') == ('bool', 'true')
        raw = doc.xref_stream(ref).decode('ascii')
        paint = re.findall(r'(?<!\S)(?:S|s|f\*?|F|B\*?|b\*?)(?!\S)', raw)
        assert len(paint) == 1 and paint[0] in ['S', 'f'], (ref, paint)
        assert re.findall(r'/([A-Za-z0-9]+)\s+gs', raw) == ['gs0', 'a0']
        assert doc.xref_get_key(ref, 'Resources/ExtGState/a0/ca') == ('int', '1')
        assert doc.xref_get_key(ref, 'Resources/ExtGState/a0/CA') == ('int', '1')
        assert doc.xref_get_key(ref, 'Resources/ExtGState/gs0/BM') == ('name', '/Normal')
        assert doc.xref_get_key(ref, 'Resources/ExtGState/gs0/SMask') == ('name', '/None')
        # Group opacity is inherited directly, rather than reset inside a group.
        flat = re.sub(r'/(?:gs0|a0)\s+gs', ' ', raw)
        replacements[name] = flat
        counts['edges' if paint[0] == 'S' else 'nodes'] += 1
    assert counts == {'edges': 5111, 'nodes': 5777}, counts
    calls = re.findall(r'/([A-Za-z0-9]+)\s+Do', content)
    assert set(replacements).issubset(set(calls)) and len(calls) == len(refs)
    content = re.sub(r'/([A-Za-z0-9]+)\s+Do', lambda m: '\n' + replacements[m[1]] + '\n' if m[1] in replacements else m[0], content)
    doc.update_stream(parent, content.encode('ascii'))
    doc.xref_set_key(parent, 'Resources/XObject', '<<' + ' '.join(f'/{n} {r} 0 R' for n, r in retained) + '>>')
    return dict(form_objects_before=before, form_objects_after=len(page.get_xobjects()),
                retained_vector_edges=counts['edges'], retained_vector_nodes=counts['nodes'],
                rasterized=False)


def main():
    # When called by rebuild.py, the assembled v0.2 already exists.
    old = OUT / ('GOSD_2026_Print_M06_Chapter5_v0.2.pdf' if '--in-place' in sys.argv
                 else 'GOSD_2026_Print_M06_Chapter5_v0.1.pdf')
    dest = OUT / 'GOSD_2026_Print_M06_Chapter5_v0.2.pdf'
    original = fitz.open(old)
    d = fitz.open(old)
    assert len(d) == 14 and d[5].get_label() == '80'
    toc, labels = d.get_toc(), d.get_page_labels()
    result = simplify(d, 5)
    meta = d.metadata
    meta['title'] = meta['title'].replace('v0.1', 'v0.2')
    d.set_metadata(meta)
    tmp = OUT / '_M06_repaired.pdf'
    d.save(tmp, garbage=4, deflate=True)
    d.close()
    after = fitz.open(tmp)
    assert after.get_toc() == toc and after.get_page_labels() == labels
    same_pages = []
    for i in range(14):
        assert after[i].get_text() == original[i].get_text(), ('text changed', i + 1)
        links = lambda p: [{k:v for k,v in link.items() if k != 'xref'} for link in p.get_links()]
        assert links(after[i]) == links(original[i]), ('links changed', i + 1)
        if i == 5:
            continue
        a = original[i].get_pixmap(matrix=fitz.Matrix(.6, .6), alpha=False)
        b = after[i].get_pixmap(matrix=fitz.Matrix(.6, .6), alpha=False)
        assert a.samples == b.samples, ('pixels changed', i + 1)
        same_pages.append(i + 1)
    a = original[5].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    b = after[5].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    x = np.frombuffer(a.samples, dtype=np.uint8).astype(np.int16)
    y = np.frombuffer(b.samples, dtype=np.uint8).astype(np.int16)
    delta = np.abs(x-y)
    # Compositing-rounding may differ by a few RGB levels; layout is identical.
    assert float(delta.mean()) < .5, float(delta.mean())
    b.save(QA / 'after.png')
    for page in after:
        for f in page.get_fonts():
            assert after.extract_font(f[0])[3], ('font not embedded', f)
    result.update(version='module 6 v0.2', page_count=14, folio=80, local_page=6,
                  changed_pages=[6], unchanged_pages=same_pages,
                  text_preserved_on_all_pages=True, links_bookmarks_labels_preserved=True,
                  fonts_embedded=True, mean_pixel_channel_difference=float(delta.mean()),
                  max_pixel_channel_difference=int(delta.max()),
                  intentionally_blank_pages=[2,14],
                  original_bytes=old.stat().st_size, file=str(dest))
    after.close(); original.close()
    tmp.replace(dest)
    result.update(size_bytes=dest.stat().st_size, sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
    (QA / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    manifest = json.loads((R / 'review/module-manifest.json').read_text())
    for m in manifest:
        if m['module'] == 6:
            m.update(file=str(dest), version='0.2', size_bytes=result['size_bytes'],
                     sha256=result['sha256'], revision='第80页单次绘制透明组扁平化；全部矢量节点、边与文字保留')
    (R / 'review/module-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
