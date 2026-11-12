from common import *
from section41 import render as render41
from section42_new import render42
from sections_compact import render_one
from section46_new import render46
from appendix import appendices
ensure_fonts();export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
pages=render41()+render42()+render_one('43')+render_one('44')+render_one('45')+render46()
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
last=None
for i,p in enumerate(pages):
 tex+=rf'\begin{{canvas}}\Header{{第四章 · 全球开源技术生态}}{{teal}}\Footer{{{i+1:02}}}'+ '\n'
 sec=p.get('section','4.1');level=1 if sec!=last else 2;last=sec;tex+=rf'\pdfbookmark[{level}]{{{esc(p["title"])}}}{{p{i}}}'+ '\n'
 tex+=box(15,27,180,p['title'],20,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
 tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+ '\n'
 tex+=box(15,217,180,p['caption'],7.6,10.7,'muted',False,True)
 for j,(head,body) in enumerate(p['analyses']):
  x=15+(j%2)*93;y=233+(j//2)*25
  tex+=box(x,y,87,head,10.3,14.2,'teal',True)+box(x,y+6,87,body,9.4,13.5)
 tex+=r'\end{canvas}'+'\n'
tex+=appendices(14)+r'\end{document}';(R/'report.tex').write_text(tex);(D/'chapter-content.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2));(R/'review/chapter-figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2));compile_tex()
d=fitz.open(O/'report.pdf');d.set_metadata({'title':'GOSD 2026 精要版｜第四章 技术生态全景｜合稿评审 v0.1','author':'全球开源发展报告编制组','subject':'4.1—4.6 全景、分层排名及地域与组织观察；主期与期后分列','keywords':'GOSD,技术全景,Agentic AI,模型,云基础设施,数据库,RISC-V,PyTorch'})
name='GOSD_2026_Chapter_4_Integrated_Review_v0.1.pdf';d.save(O/name,garbage=4,deflate=True);d.close();d=fitz.open(O/name)
for i,p in enumerate(d):p.get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(R/'review'/f'chapter-p{i+1:02}.png')
print('PAGES',len(d));print('FIGURES',len(QA));print('QA',json.dumps([q for q in QA if q['out_of_bounds'] or q['overlaps']],ensure_ascii=False))
