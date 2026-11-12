from build import *
from section33 import render,SOURCES
for folder in [B/'assets',B/'fonts',O,R/'review',F]:folder.mkdir(parents=True,exist_ok=True)
ensure_fonts();export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
PAGES=render()
def linked(t):
 for s in SOURCES:t=t.replace('［'+s['id']+'］',r'\href{'+s['url']+'}{［'+s['id']+'］}')
 return t
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
for i,p in enumerate(PAGES):
 tex+=rf'\begin{{canvas}}\Header{{第三章 · 全球开源影响力排行榜}}{{violet}}\Footer{{{i+8:02}}}'+'\n'
 tex+=box(15,27,180,p['title'],20,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
 tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
 cap=p['caption'].replace('［F3–F4］','［F3］［F4］').replace('［A1–A4、A7–A8］','［A1］［A2］［A3］［A4］［A7］［A8］')
 tex+=linked(box(15,199,180,cap,7.6,10.6,'muted',False,True))
 for j,(title,body) in enumerate(p['analyses']):
  x=15+(j%2)*93;y=214+(j//2)*34
  tex+=linked(box(x,y,87,title,10.1,14,'violet',True)+box(x,y+6,87,body,9.6,14.6))
 tex+=r'\end{canvas}'+'\n'
tex+=r'\end{document}'
(R/'report.tex').write_text(tex);(D/'content.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2));(D/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2));(R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
compile_tex();doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':'GOSD 2026 精要版｜3.3 全球开源基金会影响力排行榜｜修订稿 v0.2','author':'全球开源发展报告编制组','subject':'2026-11-10；三页竖版；全球基金会、LF 子标签、AAIF 公共组件；供评审'})
doc.set_toc([[1,p['title'],i+1] for i,p in enumerate(PAGES)]);out=O/'GOSD_2026_Section_3-3_Review_v0.2.pdf';doc.save(out,garbage=4,deflate=True);doc.close();doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.85,1.85)).save(R/'review'/f'page-{i+1}.png')
print('BUILT',out,len(doc));print(json.dumps(QA,ensure_ascii=False))
