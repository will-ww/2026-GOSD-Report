from build import *
from section32_v3 import render, BASE, GF, CF, GMF, CMF, GYF, CYF

for folder in [B/'assets',B/'fonts',O,R/'review',F]:folder.mkdir(parents=True,exist_ok=True)
ensure_fonts();export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
PAGES=render()
SOURCES=[{'id':id,'url':BASE+n,'file':n} for id,n in [('C1',GF),('C2',GMF),('C3',GYF),('C4',CF),('C5',CMF),('C6',CYF)]]
SOURCES.append({'id':'C7','url':'https://github.com/X-lab2017/open-digger/blob/5c2ffc4f5b3dd37ebcb20514c7abfee6853bd830/src/metrics/indices.ts','file':'company-top100-mainperiod.csv'})
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
for i,p in enumerate(PAGES):
    tex+=rf'\begin{{canvas}}\Header{{第三章 · 全球开源影响力排行榜}}{{violet}}\Footer{{{i+4:02}}}'+'\n'
    tex+=box(15,27,180,p['title'],20,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
    tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
    captext=p['caption'].replace('；总部据企业官网［H1］核对','；总部据企业官网（图中企业名可点击）核对').replace('及企业官网［H2］','及企业官网（图中企业名可点击）')
    cap=box(15,199,180,captext,7.6,10.7,'muted',False,True)
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
doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':'GOSD 2026 精要版｜3.2 全球开源企业影响力排行榜｜修订稿 v0.3','author':'全球开源发展报告编制组','subject':'2026-11-10；A4竖版四页；总部例证、年度/月度位次、中国企业结构；待评审'})
doc.set_toc([[1,p['title'],i+1] for i,p in enumerate(PAGES)])
# Headquarters citations attach directly to the company names in both maps.
refs=json.loads((D/'headquarters-sources.json').read_text())
for item in refs['links']:
    p=doc[item['page']+1 if item['page']==2 else item['page']];x,y,w,h=item['rect'];s=180/1000*72/25.4
    rect=fitz.Rect(15*72/25.4+x*s,53*72/25.4+y*s,15*72/25.4+(x+w)*s,53*72/25.4+(y+h)*s)
    p.insert_link({'kind':fitz.LINK_URI,'from':rect,'uri':item['url']})
out=O/'GOSD_2026_Section_3-2_Review_v0.3.pdf';doc.save(out,garbage=4,deflate=True);doc.close();doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.85,1.85)).save(R/'review'/f'page-{i+1}.png')
print('BUILT',out,len(doc));print(json.dumps(QA,ensure_ascii=False))
