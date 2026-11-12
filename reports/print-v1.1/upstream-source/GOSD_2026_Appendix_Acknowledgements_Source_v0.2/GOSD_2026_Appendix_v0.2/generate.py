"""Rebuild the GOSD 2026 appendix and acknowledgements review PDF.
All diagrams are schematic and all text/table cells are editable source.
"""
from pathlib import Path
import json, os, shutil, subprocess, sys
import vector as v

R=Path(__file__).resolve().parent
for p in ['.build/fonts','.build/assets','.build/texmf-var','figures','output','review']:
    (R/p).mkdir(parents=True,exist_ok=True)
v.R=R;v.B=R/'.build';v.F=R/'figures';v.O=R/'output'
v.C.update(ink='#19314A',muted='#667785',teal='#487B88',blue='#426B9B',line='#D5E0E4',pale='#F0F6F7',gold='#9C7734',violet='#70598E')
v.ensure_fonts()
if not (v.B/'assets/osdgs-compact.pdf').exists():
    v.export(R/'assets/osdgs-symbol-compact.svg',v.B/'assets/osdgs-compact.pdf')

def arrow(f,x,y,xx,yy,c='teal',sw=2):
    import math
    f.line(x,y,xx,yy,c,sw)
    a=math.atan2(yy-y,xx-x)
    pts=[(xx-8*math.cos(a-.48),yy-8*math.sin(a-.48)),(xx,yy),(xx-8*math.cos(a+.48),yy-8*math.sin(a+.48))]
    f.path(pts,c,sw)

def diagrams():
    f=v.Figure(160)
    labels=[('提出问题','OI'),('讨论完善','ID'),('发起变更','OPR'),('评审反馈','PRR'),('变更合入','MPR')]
    for i,(name,code) in enumerate(labels):
        x=i*202
        f.rect(x,14,182,112,'pale');f.rect(x,14,4,112,'teal')
        f.text(x+91,52,code,23,'teal',True,'middle')
        f.text(x+91,91,name,22,'ink',True,'middle')
        if i<4:arrow(f,x+185,70,x+199,70,'soft',1.8)
    f.text(0,153,'协作过程示意：事件可以往返、并行，并非每次讨论都必然进入合入环节。',17,'muted')
    f.save('five-actions')

    f=v.Figure(220)
    f.rect(0,4,1000,200,'pale');f.rect(0,4,5,200,'blue')
    f.text(22,40,'平台活跃账号',22,'blue',True);f.text(22,71,'Active developers',17,'muted')
    f.text(22,106,'按来源规定的活动计入',18);f.text(22,135,'可含关注、复制与代码提交',18)
    f.rect(310,26,672,159,'#DFECEF');f.rect(310,26,5,159,'teal')
    f.text(332,65,'协作参与者',22,'teal',True);f.text(332,95,'Participants',17,'muted')
    f.text(332,131,'围绕问题与修改方案协作',18)
    f.rect(640,48,324,114,'white');f.rect(640,48,5,114,'gold')
    f.text(662,86,'已合入 PR 的作者',21,'gold',True)
    f.text(662,116,'Contributors',17,'muted');f.text(662,145,'本图为集合关系，面积不表数量',15,'muted')
    f.save('participant-sets')

    f=v.Figure(530)
    f.text(282,27,'社区视角 · 项目内部',23,'teal',True,'middle')
    f.text(751,27,'全域视角 · 跨项目网络',23,'blue',True,'middle')
    f.rect(78,48,423,211,'pale');f.rect(518,48,482,211,'#EEF3F9')
    f.rect(78,276,423,211,'#F6F7F8');f.rect(518,276,482,211,'#EEF3F9')
    f.text(0,105,'开发者',21,'ink',True)
    f.text(0,333,'仓库',21,'ink',True);f.text(0,364,'／项目',21,'ink',True)
    f.text(103,84,'社区 OpenRank 贡献度',23,'teal',True)
    f.text(103,116,'参与者在项目协作网络中的相对贡献',18)
    # Small community graph: people, issues and PRs. All nodes are schematic.
    nodes=[(132,164),(204,211),(272,155),(357,209),(446,163)]
    for a,b in [(0,1),(0,3),(1,2),(2,3),(3,4),(1,4)]:f.line(*nodes[a],*nodes[b],'soft',2)
    for i,(x,y) in enumerate(nodes):
        if i in (1,3):f.rect(x-11,y-11,22,22,'teal')
        else:f.circle(x,y,10,'teal')
    f.text(103,245,'圆点：开发者；方点：Issue / PR（示意）',17,'muted')
    f.text(543,84,'开发者全域 OpenRank 影响力',23,'blue',True)
    f.wrap(543,118,'从开发者与仓库的协作关系，观察跨项目的连接位置及长期积累。',420,18,leading=28)
    f.text(543,209,'个人／群体 → 组织或地域聚合',20,'blue',True)
    f.text(543,244,'合计时明确身份、观察范围与时期',17,'muted')
    f.text(103,317,'过程与影响，提供不同视角',21,'teal',True)
    f.wrap(103,354,'议题、评审与合入记录说明项目怎样协作；右侧的项目影响力说明它在更大网络中的位置。',366,19,leading=30)
    f.text(543,317,'仓库／项目全域 OpenRank 影响力',22,'blue',True)
    f.wrap(543,354,'在同一协作网络中，观察仓库或项目与开发者之间的相互连接。',420,19,leading=30)
    f.text(543,445,'组织／国家地区／技术生态',20,'blue',True)
    f.text(543,475,'按明确名录和归属关系形成观察单元',17,'muted')
    f.text(78,519,'分类关系示意；项目内部贡献与跨项目影响分别理解。',17,'muted')
    f.save('openrank-matrix')

    f=v.Figure(225)
    f.text(0,27,'历史比较',21,'muted',True);f.text(350,27,'主统计期 · 12 个月',23,'teal',True)
    f.text(813,27,'期后观察',21,'gold',True)
    f.rect(0,59,268,66,'#EEF1F4');f.rect(300,59,460,66,'teal');f.rect(792,59,208,66,'#F6F0E3')
    for i in range(1,12):f.line(300+i*460/12,110,300+i*460/12,119,'white',.6)
    f.text(530,102,'2025.07.01 — 2026.06.30',23,'white',True,'middle')
    f.text(134,102,'各期采用可比窗口',19,'muted',False,'middle')
    f.text(896,102,'单列快照日期',19,'gold',False,'middle')
    f.text(0,160,'事件发生时间',18,'ink',True);f.text(0,191,'说明活动发生在哪一期',18,'muted')
    f.text(365,160,'数据获取时间',18,'ink',True);f.text(365,191,'说明何时采集并回看历史',18,'muted')
    f.text(745,160,'复核时间',18,'ink',True);f.text(745,191,'说明本次查证状态',18,'muted')
    f.save('time-windows')

    f=v.Figure(200)
    cols=[(0,190,'仓库','模型／数据载体'),(237,215,'版本与家族','具体成果／相关版本'),(499,214,'来源关系','在已有模型上改进'),(760,240,'应用情况','获取／改进／运行')]
    for i,(x,w,a,b) in enumerate(cols):
        f.rect(x,10,w,102,'pale');f.text(x+15,48,a,23,'teal',True)
        f.text(x+15,83,b,17)
        if i<3:arrow(f,x+w+7,61,cols[i+1][0]-10,61,'soft')
    f.rect(0,137,1000,49,'#EEF3F9');f.text(20,170,'资源数量、版本关系和使用情况分别观察；可下载，不代表已经用于实际业务。',18,'blue')
    f.save('model-units')

    (R/'review/figure-qa.json').write_text(json.dumps(v.QA,ensure_ascii=False,indent=2))

def esc(s):
    for a,b in [('\\',r'\textbackslash{}'),('&',r'\&'),('%',r'\%'),('_',r'\_'),('#',r'\#')]:s=s.replace(a,b)
    return s

def table(headers,rows,widths,fs=9.2,leading=14.1):
    spec=''.join('Y' if w is None else f'L{{{w}mm}}' for w in widths)
    s=rf'{{\sffamily\fontsize{{{fs}}}{{{leading}}}\selectfont\rowcolors{{2}}{{paper}}{{white}}\begin{{tabularx}}{{\linewidth}}{{{spec}}}\rowcolor{{teal}}'+' & '.join(r'\HeadCell{'+esc(h)+'}' for h in headers)+r'\\'+'\n'
    for row in rows:s+=' & '.join(esc(t) for t in row)+r'\\'+'\n'
    return s+r'\end{tabularx}}\par'+'\n'

def heading(s):return '\\vspace{7pt}\\Heading{'+s+'}\n'
def para(s):return s+'\n\n'
def note(s):return '\\Small{'+s+'}\\par\n'
def img(name):return '\\includegraphics[width=\\linewidth]{.build/assets/'+name+'.pdf}\\par\n'
def title(a,b=None):
    s='{\\sffamily\\bfseries\\fontsize{20}{27}\\selectfont\\color{navy}'+a+'}\\par\\vspace{5pt}\n'
    if b:s+='{\\sffamily\\fontsize{10.5}{16}\\selectfont\\color{teal}'+b+'}\\par\\vspace{6pt}\n'
    return s

PAGES=[]
def page(name,body,fs=10.8,lead=18.2):PAGES.append((name,body,fs,lead))

def content():
    from content import populate
    populate(sys.modules[__name__])

def build():
    diagrams();content()
    tex=r'\documentclass{article}\usepackage{layout}\begin{document}'+'\n'
    for i,(name,s,fs,lead) in enumerate(PAGES,1):
        tex+=rf'\begin{{canvas}}\Header{{{name}}}\Footer{{{i:02}}}\pdfbookmark[0]{{{name}}}{{p{i}}}'+'\n'
        tex+=rf'\Box{{17}}{{29}}{{176}}{{\fontsize{{{fs}}}{{{lead}}}\selectfont {s}}}'+'\n'+r'\end{canvas}'+'\n'
    tex+=r'\end{document}'
    (R/'report.tex').write_text(tex)
    v.compile_tex()
    dest=R/'output/GOSD_2026_Appendix_Acknowledgements_Review_v0.2.pdf'
    shutil.copy2(R/'output/report.pdf',dest)
    print(dest)

if __name__=='__main__':build()
