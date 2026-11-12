"""Centered institutional identity with a native-vector three-stage research loop."""
from pathlib import Path
import os, json, re, subprocess, shutil
from PIL import Image
import fitz

R=Path(__file__).resolve().parent
O=R/'output';Q=R/'review'
O.mkdir(exist_ok=True);Q.mkdir(exist_ok=True)
if not (R/'source/fonts/NotoSansCJKsc-Regular.otf').is_file():
    subprocess.run(['python3',str(R/'source/prepare_fonts.py')],check=True)
for name in ['fonts','assets']:
    p=R/name
    if not p.exists():p.symlink_to(R/'source'/name,target_is_directory=True)
layout=(R/'source/layout.sty').read_text()
layout+=r'''
\definecolor{bodyink}{HTML}{24434B}
\definecolor{softink}{HTML}{5D757B}
\definecolor{stageone}{HTML}{246276}
\definecolor{stagetwo}{HTML}{087A80}
\definecolor{stagethree}{HTML}{AC5A2A}
\definecolor{outline}{HTML}{D7E5E5}
\definecolor{wash}{HTML}{F3F8F7}
\definecolor{loop}{HTML}{8EB8B8}
'''
(R/'layout.sty').write_text(layout)
boxes=[]
def esc(t):return t.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('\n',r'\\ ')
def text(x,y,w,t,fs=10,leading=15,color='bodyink',bold=False,serif=False,align='',height=None,center=False):
    ident='siri'+str(len(boxes)+1)
    boxes.append(dict(id=ident,x=x,y=y,w=w,text=t,max_height=height,center=center))
    style=(r'\rmfamily ' if serif else r'\sffamily ')+(r'\bfseries ' if bold else '')
    return '\\'+('CenterBox' if center else 'Box')+rf'{{{ident}}}{{{x}}}{{{y}}}{{{w}}}{{{style}\fontsize{{{fs}}}{{{leading}}}\selectfont\color{{{color}}}{align}{esc(t)}}}'+'\n'
def rect(x,y,w,h,color,rounded=0):
    return rf'\fill[{color},rounded corners={rounded}mm] \Pos{{{x}}}{{{y}}} rectangle \Pos{{{x+w}}}{{{y+h}}};'+'\n'
def line(x,y,x2,y2,color='outline',width=.5):
    return rf'\draw[{color},line width={width}pt] \Pos{{{x}}}{{{y}}} -- \Pos{{{x2}}}{{{y2}}};'+'\n'
def icon(kind,x,y,col):
    style=rf'\draw[{col},line width=.7pt,line cap=round,line join=round] '
    def pos(a,b):return rf'\Pos{{{x+a}}}{{{y+b}}}'
    def path(points):return style+' -- '.join(pos(a,b) for a,b in points)+';\n'
    def frame(a,b,c,d):return style+pos(a,b)+' rectangle '+pos(c,d)+';\n'
    if kind=='research':
        return style+pos(2.7,2.7)+r' circle[radius=2.3mm];'+'\n'+path([(4.4,4.4),(7.2,7.2)])+path([(1.5,2.7),(3.9,2.7)])+path([(2.7,1.5),(2.7,3.9)])
    if kind=='insight':
        return path([(0,7.2),(7.5,7.2)])+frame(.8,4.1,2.1,6.4)+frame(3.1,2.8,4.4,6.4)+frame(5.4,.8,6.7,6.4)+path([(.4,3.1),(2.9,1.2),(4.3,1.8),(7,0)])
    return frame(.2,2.1,7.2,7.1)+path([(2,2.1),(2,.3),(5.4,.3),(5.4,2.1)])+path([(.2,4),(7.2,4)])+frame(3.1,3.5,4.4,4.8)

im=Image.open(R/'assets/siri-color.png')
a,b,c,e=im.getbbox();ink_width=110
image_width=ink_width*im.width/(c-a)
image_x=(210-ink_width)/2-a*ink_width/(c-a)
image_y=17-b*ink_width/(c-a)
s=r'\begin{canvas}'+'\n'
# Use the supplied transparent logo unchanged. Position its visible ink, not its canvas.
s+=rf'\node[anchor=north west,inner sep=0pt,outer sep=0pt] at \Pos{{{image_x}}}{{{image_y}}} {{\includegraphics[width={image_width}mm]{{assets/siri-color.png}}}};'+'\n'
s+=line(85,45.7,99,45.7,'outline',.6)+line(111,45.7,125,45.7,'outline',.6)
s+=rect(102.5,45.1,5,1.2,'siriorange',.6)
s+=text(18,53,174,'人工智能产业的“范式孵化器”',22,30,'siriink',True,True,r'\centering ',height=12)
s+=text(18,68.4,174,'连接前沿研究、产业洞察与实践转化。',10.8,16,'siriteal',False,False,r'\centering ',height=7)

s+=rect(18,85.5,174,21.5,'wash',2.5)
s+=text(18,89,174,'核心命题',8.2,12,'siriteal',True,False,r'\centering ',height=5)
s+=text(18,95.2,174,'大模型驱动的智能化范式变革',14.1,20,'siriink',True,True,r'\centering ',height=9)
s+=text(18,113.6,174,'人工智能  ×  开源创新',11.2,16,'siriteal',True,False,r'\centering ',height=7)

stages=[('01','范式研究','技术与工作方式如何改变？','形成问题与分析框架','以证据识别结构','stageone','research'),
        ('02','产业洞察','变化发生在哪里、影响谁？','形成生态诊断与战略判断','以场景检验方法','stagetwo','insight'),
        ('03','实践转化','什么方法能进入真实场景？','形成方案，并以实践修正研究','以反馈修正问题','stagethree','practice')]
for x,(n,title,question,result,relation,col,kind) in zip([18,79,140],stages):
    s+=rect(x,126,52,57,col+'!4!white',2.4)
    s+=line(x+4.5,126,x+47.5,126,col,.9)
    s+=text(x+4.7,130.3,31,n,22,26,col+'!55!white',True,height=12)
    s+=icon(kind,x+40,131.3,col)
    s+=text(x+4.7,143,42.6,title,13.5,18,col,True,height=8)
    s+=text(x+4.7,153,42.6,question,9.1,13,'bodyink',height=10)
    s+=text(x+4.7,162,42.6,result,8.6,12.6,'softink',height=10)
    s+=line(x+4.7,173.8,x+47.3,173.8,col+'!18!white',.45)
    s+=text(x+4.7,176.3,42.6,relation,8.1,11.7,col,True,height=5)
for x in [71.1,132.1]:
    s+=rf'\draw[draw=loop,line width=.8pt,-{{Stealth[length=1.7mm,width=1.5mm]}}] \Pos{{{x}}}{{150.5}} -- \Pos{{{x+6.6}}}{{150.5}};'+'\n'
# Close the loop underneath the three stages, outside all text and card boundaries.
s+=r'\draw[draw=loop,line width=.65pt,rounded corners=3mm,-{Stealth[length=1.8mm,width=1.5mm]}] \Pos{166}{183.4} -- \Pos{166}{195} -- \Pos{44}{195} -- \Pos{44}{183.4};'+'\n'
s+=rect(62,191.8,86,6.5,'white')
s+=text(62,192.8,86,'研究体系：问题、证据与实践相互反馈',8.3,12,'softink',False,False,r'\centering ',height=5)
s+=text(18,203,174,'高校与科研机构  ·  产业企业  ·  开发者社区',9,13,'siriteal',False,False,r'\centering ',height=6)

paragraphs=[('由技术变化出发','奇点智能研究院由专业开发者社区 CSDN 与 IT 技术咨询平台 Boolan 联合发起，定位于创新型研究机构、科技智库与战略咨询平台。研究院联结高校、科研机构、产业企业与开发者社区，开展跨学科研究。'),
 ('以产业与社会价值为方向','研究院关注人工智能与开源创新如何共同改变技术底座、产业生态和社会治理。其使命是理解范式转换的逻辑，打通技术突破与产业应用的路径，使研究能够回应真实问题。')]
for x,(heading,body) in zip([18,109.5],paragraphs):
    s+=text(x,218,82.5,heading,11,16,'siriink',True,height=8)
    s+=text(x,227,82.5,body,9.7,15.2,'bodyink',False,True,height=31)
s+=line(105,218,105,255,'outline',.45)
s+=rect(18,263.5,174,17.5,'wash',2.5)
s+=text(23,272.3,15,'愿景',10.5,15,'siriorange',True,height=8,center=True)
s+=text(42,272.3,144,'孕育思想、发展方法，推动智能技术成为普惠、可信、可持续的全球公共品。',9.6,14.2,'siriink',False,True,height=12,center=True)
s+=line(18,285,192,285,'outline',.5)+line(18,285,26,285,'siriorange',.9)
s+=text(18,289,160,'SINGULARITY INTELLIGENCE RESEARCH INSTITUTE',6.8,9.5,'softink',height=5)

report_s=s+text(179,288,13,'iii',10.3,14,'siriink',True,False,r'\raggedleft ',height=7)
base=r'\documentclass[11pt,a4paper]{article}\usepackage{layout}\hypersetup{pdftitle={奇点智能研究院｜机构介绍 v1.1},pdfauthor={奇点智能研究院},pdfsubject={机构定位、研究体系与愿景},pdfkeywords={人工智能,开源创新,奇点智能研究院},pdfpagemode=UseNone}\begin{document}'+'\n'
for name,body in [('standalone',s),('report-page',report_s)]:
    (R/(name+'.tex')).write_text(base+body+r'\end{canvas}\end{document}')
(Q/'text-box-plan.json').write_text(json.dumps(boxes,ensure_ascii=False,indent=2))
env=os.environ.copy();env['TEXMF']='{/usr/share/texmf,/usr/share/texlive/texmf-dist}'
var=R/'.texmf-var';var.mkdir(exist_ok=True)
env['TEXMFVAR']=str(var);env['TEXFORMATS']=str(var)
if not (var/'xelatex.fmt').exists():
    with (O/'format-build.txt').open('w') as log:
        subprocess.run(['xelatex','-ini','-etex','-interaction=nonstopmode','-jobname=xelatex',f'-output-directory={var}',r'\input xelatex.ini'],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
for name in ['standalone','report-page']:
    for attempt in range(2):
        with (O/f'{name}-build-{attempt}.txt').open('w') as log:
            subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory=output',name+'.tex'],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    pdf=fitz.open(O/(name+'.pdf'));assert len(pdf)==1
    pdf[0].get_pixmap(matrix=fitz.Matrix(1.8,1.8),alpha=False).save(Q/(name+'.png'))
shutil.copyfile(O/'standalone.pdf',O/'SIRI_Institute_Introduction_v1.1.pdf')
print('Two one-page layouts compiled',flush=True)
