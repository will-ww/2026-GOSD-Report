"""Restore the approved centered GOSD mark to the clean back cover."""
import os, json, subprocess, hashlib
from pathlib import Path
import fitz
import build_modules as b

b.back_cover()
master = b.MASTER
review = b.REVIEW / 'backcover-v03'
review.mkdir(exist_ok=True)
(master/'back-cover-v03.tex').write_text(r'\documentclass[11pt,a4paper]{article}\usepackage{layout}\begin{document}'+'\n'+''.join(b.TEX_PAGES)+r'\end{document}')
env = os.environ.copy()
env['TEXMF'] = '{/usr/share/texmf,/usr/share/texlive/texmf-dist}'
env['TEXMFVAR'] = str((b.R.parent/'front-v0.8/.texmf-var').resolve())
env['TEXFORMATS'] = env['TEXMFVAR']
for i in range(2):
    with (master/'output'/f'back-cover-v03-build-{i}.txt').open('w') as log:
        subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory=output','back-cover-v03.tex'],cwd=master,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
old = b.OUT/'GOSD_2026_Print_M08_Appendix_Acknowledgements_v0.2.pdf'
new = b.OUT/'GOSD_2026_Print_M08_Appendix_Acknowledgements_v0.3.pdf'
original = fitz.open(old)
d = fitz.open(old)
toc, labels, meta = d.get_toc(), d.get_page_labels(), d.metadata
cover = fitz.open(master/'output/back-cover-v03.pdf')
d.delete_page(23)
d.insert_pdf(cover)
d.set_toc(toc)
d.set_page_labels(labels)
meta['title'] = meta['title'].replace('v0.2','v0.3')
d.set_metadata(meta)
d.save(new,garbage=4,deflate=True)
d.close()
d = fitz.open(new)
assert len(d) == len(original) == 24
for i in range(23):
    assert d[i].get_text() == original[i].get_text()
    assert d[i].get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False).samples == original[i].get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False).samples
assert d.get_toc() == toc and d.get_page_labels() == labels
t = d[-1].get_text()
assert set(x.strip() for x in t.splitlines() if x.strip()) == {'GOSD','共同创造','开放的智能未来','OPEN SOURCE, A SHARED INTELLIGENT FUTURE'}
assert len(d[-1].get_images()) == 1
for f in d[-1].get_fonts():
    assert d.extract_font(f[0])[3]
logo_text = d[-1].search_for('GOSD')
assert len(logo_text) == 1 and abs((logo_text[0].x0+logo_text[0].x1)/2 - 105*b.M) < .3
d[-1].get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(review/'after.png')
result = dict(version='module 8 v0.3',changed_pages=[24],unchanged_pages=list(range(1,24)),
              page_count=24,bookmarks_preserved=True,page_labels_preserved=True,
              back_cover_text=t,gosd_mark_restored=True,fonts_embedded=True,
              file=str(new),sha256=hashlib.sha256(new.read_bytes()).hexdigest())
(review/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
manifest=json.loads((b.REVIEW/'module-manifest.json').read_text())
for m in manifest:
    if m['module']==8:
        m.update(file=str(new),size_bytes=new.stat().st_size,sha256=result['sha256'],version='0.3',revision='简洁封底恢复居中的 GOSD 标识')
(b.REVIEW/'module-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False),flush=True)
