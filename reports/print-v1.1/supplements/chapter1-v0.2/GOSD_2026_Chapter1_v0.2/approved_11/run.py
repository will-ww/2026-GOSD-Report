from build import *
from section11 import render,SOURCES,MODEL_SAMPLES
for p in [B/'assets',B/'fonts',O,R/'review',D,F]:p.mkdir(parents=True,exist_ok=True)
ensure_fonts();export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
pages=render()
def linked(text):
    for s in SOURCES:text=text.replace('［'+s['id']+'］',r'\href{'+s['url'].replace('#',r'\#')+'}{［'+s['id']+'］}')
    return text
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
for i,p in enumerate(pages):
    tex+=rf'\begin{{canvas}}\Header{{第一章 · 开源与 AI}}{{blue}}\Footer{{{i+11:02}}}'+'\n'
    tex+=rf'\pdfbookmark[1]{{{p["title"]}}}{{page{i+1}}}'+'\n'
    tex+=box(15,27,180,p['title'],19.7,25,'ink',True)
    tex+=box(15,39,180,p['subtitle'],10.7,14.5,'teal',True)
    tex+=box(15,47.5,180,p['intro'],10.3,15.5,'ink')
    tex+=rf'\Box{{15}}{{66}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
    tex+=linked(box(15,195,180,p['caption'],8,11.6,'muted',False,True))
    for j,(title,body) in enumerate(p['analyses']):
        x=15 if j!=1 else 108;y=213 if j<2 else 250;w=87 if j<2 else 180
        tex+=box(x,y,w,title,10.5,15,'blue',True)+box(x,y+6,w,body,10.2,15.4)
    tex+=r'\end{canvas}'+'\n'
tex+=r'\end{document}'
(R/'report.tex').write_text(tex)
(D/'content.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2))
(D/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2))
(D/'chart-data.json').write_text(json.dumps({'agent_pr_share':[{'period':'2026-03','value':17,'relation':'='},{'period':'2026-09','value':40,'relation':'>'}],'copilot_active_users_agentic_share':[{'period':'prior-year observation','value':35},{'period':'2026 report observation','value':55}],'nvidia_sample_records':[{'model':name,'count':v} for name,v,c in MODEL_SAMPLES]},ensure_ascii=False,indent=2))
(R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
compile_tex()
doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':'2026全球开源发展报告｜1.1人工智能时代的开源协作：双向重塑｜样节v0.1','author':'全球开源发展报告编制组','subject':'三页竖版样节；供评审；2026-11-10'})
doc.set_toc([[1,p['title'],i+1] for i,p in enumerate(pages)])
out=O/'GOSD_2026_Section_1-1_Review_v0.1.pdf';doc.save(out,garbage=4,deflate=True);doc.close()
doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(2,2)).save(R/'review'/f'page-{i+1}.png')
print('BUILT',out,len(doc));print(json.dumps(QA,ensure_ascii=False))
