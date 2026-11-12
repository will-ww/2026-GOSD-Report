"""Reflow the updated cross-reference as a complete paragraph, preserving its font size."""
from pathlib import Path
import os,subprocess,json,fitz
from print_config import R
M=72/25.4
master=R/'master';review=R/'review'
original=fitz.open(R/'inputs/chapter2.pdf')
block=next(b for b in original[23].get_text('blocks') if b[4].startswith('单位均为万'))
area=fitz.Rect(block[:4]);area.x0=15*M;area.x1=195*M;area.y1=56*M
text='单位均为万 OpenRank。根据各行历史首末值及第 10 节方法可复算端点；报告年度（2022→2026）与自然年（2021→2025）分别计算，覆盖不同，不用于相互换算。'
prepared=R/'master/prepared/chapter2.pdf';d=fitz.open(prepared)
d[23].add_redact_annot(area,fill=(1,1,1),cross_out=False);d[23].apply_redactions(images=0,graphics=0,text=0)
expected=d[23].get_text(clip=fitz.Rect(10*M,24*M,200*M,281.5*M))
tmp=prepared.with_suffix('.tmp.pdf');d.save(tmp,garbage=4,deflate=True);d.close();tmp.replace(prepared)
tex=r'\documentclass[11pt,a4paper]{article}\usepackage{layout}\begin{document}\begin{canvas}'+'\n'
tex+=rf'\Box{{methodintro}}{{19}}{{{area.y0/M}}}{{180}}{{\rmfamily\fontsize{{9.6}}{{14}}\selectfont\color{{muted}}'+text+'}\n'
tex+=r'\end{canvas}\end{document}'
(master/'method-intro.tex').write_text(tex)
env=os.environ.copy();env['TEXMF']='{/usr/share/texmf,/usr/share/texlive/texmf-dist}'
env['TEXMFVAR']=str((R.parent/'front-v0.8/.texmf-var').resolve());env['TEXFORMATS']=env['TEXMFVAR']
for i in range(2):
 with (master/'output'/f'method-intro-build-{i}.txt').open('w') as f:subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory=output','method-intro.tex'],cwd=master,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
path=sorted((R/'output/pdf').glob('*M08_*.pdf'))[-1];d=fitz.open(path);dest=area+fitz.Rect(4*M,0,4*M,0)
d[12].add_redact_annot(dest,fill=(1,1,1),cross_out=False);d[12].apply_redactions(images=0,graphics=0,text=0)
overlay=fitz.open(master/'output/method-intro.pdf');d[12].show_pdf_page(d[12].rect,overlay,0)
tmp=path.with_suffix('.tmp.pdf');d.save(tmp,garbage=4,deflate=True);d.close();tmp.replace(path)
retention=json.loads((review/'body-retention.json').read_text())
for entry in retention:
 if entry['module']==8 and entry['local_page']==13:entry['expected_text']=expected
(review/'body-retention.json').write_text(json.dumps(retention,ensure_ascii=False,indent=2))
patches=json.loads((review/'pdf-text-patches.json').read_text())
patches=[p for p in patches if p['tag']!='chapter2-appendix-paragraph-reflow']
patches.append(dict(tag='chapter2-appendix-paragraph-reflow',page=24,old=block[4],new=text,count=1))
(review/'pdf-text-patches.json').write_text(json.dumps(patches,ensure_ascii=False,indent=2))
(review/'method-intro.json').write_text(json.dumps(dict(module=8,page=13,x=19,y=area.y0/M,width=180,font_size=9.6,leading=14,text=text),ensure_ascii=False,indent=2))
print('Appendix 11 introduction reflowed at its original font size.')
