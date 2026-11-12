from build import *
from industry import render
from appendix import make_appendix
for p in [B/'assets',B/'fonts',B/'texmf-var',O,F,R/'review']:p.mkdir(parents=True,exist_ok=True)
ensure_fonts();export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
PAGES=render()
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
for i,p in enumerate(PAGES):
 tex+=rf'\begin{{canvas}}\Header{{第二章 · 全球开源生态地图}}{{teal}}\Footer{{{i+1:02}}}'+'\n'
 tex+=box(15,27,180,p['title'],21,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
 tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
 tex+=box(15,199,180,p['caption'],7.8,10.8,'muted',False,True)
 for j,(title,body) in enumerate(p['analyses']):
  x=15+(j%2)*93;y=211+(j//2)*34
  tex+=box(x,y,87,title,10.5,14.2,'teal',True)+box(x,y+6,87,body,10.1,15.6)
 tex+=r'\end{canvas}'+'\n'
tex+=make_appendix()+r'\end{document}'
(R/'report.tex').write_text(tex);(D/'content.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2));(R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
compile_tex();doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':'GOSD 2026 精要版｜2.8 开源行业地图 v0.2','author':'全球开源发展报告编制组','subject':'A4 竖版；期后行业专题；待作者评审'})
doc.set_toc([[1,p['title'],i+1] for i,p in enumerate(PAGES)]+[[1,'附录 1｜行业地图口径与证据',len(PAGES)+1]])
out=O/'GOSD_2026_Section_2-8_Review_v0.2.pdf';doc.save(out,garbage=4,deflate=True);doc.close();doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.7,1.7)).save(R/'review'/f'page-{i+1}.png')
print('BUILT',out,len(doc));print(json.dumps(QA,ensure_ascii=False))
