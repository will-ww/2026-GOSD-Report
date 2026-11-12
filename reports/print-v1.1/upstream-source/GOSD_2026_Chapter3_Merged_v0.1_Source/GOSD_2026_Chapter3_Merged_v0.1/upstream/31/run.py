from build import *
from rankings import render

for folder in [B/'assets',B/'fonts',O,R/'review']:
    folder.mkdir(parents=True,exist_ok=True)
ensure_fonts()
export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
PAGES=render()
BASE='https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/c51e3441361407b68f10b339d97eff288319b503/data/processed/chapter3/'
FILES=['table-3-1-1_global_division_openrank_top30.csv','table-3-1-2_division_country_entry_counts.csv','table-3-1-3_china_province_openrank_top30.csv','table-3-1-4_china_city_openrank_top30.csv']
SOURCES=[{'id':f'R{i+1}','url':BASE+n,'file':n} for i,n in enumerate(FILES)]
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
for i,p in enumerate(PAGES):
    tex+=rf'\begin{{canvas}}\Header{{第三章 · 全球开源影响力排行榜}}{{violet}}\Footer{{{i+1:02}}}'+'\n'
    tex+=box(15,27,180,p['title'],20,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
    tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
    cap=box(15,199,180,p['caption'],7.6,10.7,'muted',False,True)
    for s in SOURCES:cap=cap.replace('［'+s['id']+'］',r'\href{'+s['url']+'}{［'+s['id']+'］}')
    tex+=cap
    for j,(title,body) in enumerate(p['analyses']):
        x=15+(j%2)*93;y=212+(j//2)*34
        tex+=box(x,y,87,title,10.3,14.2,'violet',True)+box(x,y+6,87,body,9.9,15)
    tex+=r'\end{canvas}'+'\n'
tex+=r'\end{document}'
(R/'report.tex').write_text(tex);(D/'content.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2));(D/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2))
(R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
compile_tex()
doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':'GOSD 2026 精要版｜3.1 全球行政区划影响力排行榜｜修订稿 v0.2','author':'全球开源发展报告编制组','subject':'2026-11-10；A4竖版三页修订稿；待作者评审'})
doc.set_toc([[1,p['title'],i+1] for i,p in enumerate(PAGES)])
out=O/'GOSD_2026_Section_3-1_Review_v0.2.pdf';doc.save(out,garbage=4,deflate=True);doc.close();doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.85,1.85)).save(R/'review'/f'page-{i+1}.png')
print('BUILT',out,len(doc));print(json.dumps(QA,ensure_ascii=False))
