from build import *
from section12 import render as render12, SOURCES as sources12
import importlib.util

for p in [B/'assets',B/'fonts',O,R/'review',D,F]:p.mkdir(parents=True,exist_ok=True)
ensure_fonts();export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
pages=render12();sources=list(sources12)
if (R/'section13.py').exists():
    from section13 import render as render13, SOURCES as sources13
    pages+=render13();sources+=sources13

def linked(t):
    for s in sources:t=t.replace('［'+s['id']+'］',r'\href{'+s['url'].replace('#',r'\#')+'}{［'+s['id']+'］}')
    return t

tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
for i,p in enumerate(pages):
    tex+=rf'\begin{{canvas}}\Header{{第一章 · 开源与 AI}}{{blue}}\Footer{{{i+14:02}}}'+'\n'
    tex+=rf'\pdfbookmark[1]{{{p["title"]}}}{{page{i+1}}}'+'\n'
    tex+=box(15,27,180,p['title'],p.get('title_size',19.7),25,'ink',True)
    tex+=box(15,39,180,p['subtitle'],10.7,14.5,'teal',True)
    tex+=box(15,47.5,180,p['intro'],10.3,15.5,'ink')
    fy=p.get('figure_y',66)
    tex+=rf'\Box{{15}}{{{fy}}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
    tex+=linked(box(15,p.get('caption_y',195),180,p['caption'],8,11.6,'muted',False,True))
    if p.get('type')=='catalogue':
        tex+=box(15,265,180,p['closing'],9.5,14,'ink')
    else:
        for j,(title,body) in enumerate(p['analyses']):
            x=15 if j!=1 else 108;y=213 if j<2 else 250;w=87 if j<2 else 180
            tex+=box(x,y,w,title,10.5,15,'blue',True)+box(x,y+6,w,body,10.2,15.4)
    tex+=r'\end{canvas}'+'\n'
tex+=r'\end{document}'
(R/'report.tex').write_text(tex)
(D/'content-12-13.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2))
(D/'sources-12-13.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
(R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
compile_tex()

baseline=R.parent/'GOSD_2026_Section_1-1_v0.1'
baseline_pdf=R/'assets/approved-11.pdf'
if not baseline_pdf.exists():baseline_pdf=baseline/'output/GOSD_2026_Section_1-1_Review_v0.1.pdf'
cover=R/'assets/approved-cover.pdf';cover_page=0
if not cover.exists():
    cover=R.parent.parent/'tmp/ch1-review/input/2026 全球开源发展报告/GOSD_2026_精要版_可读性与内容深化评审稿_v0.6.pdf';cover_page=9
doc=fitz.open()
with fitz.open(cover) as old:doc.insert_pdf(old,from_page=cover_page,to_page=cover_page)
with fitz.open(baseline_pdf) as s:doc.insert_pdf(s)
with fitz.open(O/'report.pdf') as s:doc.insert_pdf(s)
doc.set_metadata({'title':'2026全球开源发展报告｜第一章1.1—1.3重构合稿｜v0.2','author':'全球开源发展报告编制组','subject':'1.1沿用已评审样节；1.2与1.3为本轮评审内容；2026-11-10'})
toc=[[1,'第一章　开源与AI',1],[2,'1.1　人工智能时代的开源协作：双向重塑',2],[2,pages[0]['title'],5]]
for i,p in enumerate(pages):
    if p['title'].startswith('1.3'):toc.append([2,p['title'],i+5])
doc.set_toc(toc)
out=O/'GOSD_2026_Chapter1_Review_v0.2.pdf';doc.save(out,garbage=4,deflate=True);doc.close()
doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.8,1.8)).save(R/'review'/f'page-{i+1:02}.png')
print('BUILT',out,len(doc));print(json.dumps(QA,ensure_ascii=False))
