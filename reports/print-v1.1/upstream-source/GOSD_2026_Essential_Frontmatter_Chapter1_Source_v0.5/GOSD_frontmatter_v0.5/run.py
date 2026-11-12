"""GOSD v0.5: restore the approved cover composition and redesign four institute pages."""
from build import *
from PIL import Image

for p in [B/'assets',B/'fonts',O,F,R/'review',D]:p.mkdir(parents=True,exist_ok=True)
ensure_fonts()
export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
C.update(violet='#6146A5',orange='#AD4E22',navy='#13253D',gold='#8E6500')

def curve(f,d,c='teal',sw=2,fill='none',opacity=1):
    f.items.append(f'<path d="{d}" fill="{cl(fill)}" stroke="{cl(c)}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>')
def arrow(f,x,y,xx,yy,c='teal',sw=2):
    f.line(x,y,xx,yy,c,sw)
    a=math.atan2(yy-y,xx-x)
    f.path([(xx-10*math.cos(a-.4),yy-10*math.sin(a-.4)),(xx,yy),(xx-10*math.cos(a+.4),yy-10*math.sin(a+.4))],c,sw)
def icon(f,x,y,kind,c='blue',s=1):
    # Small editorial line icons, exact vectors rather than generated symbols.
    f.items.append(f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{cl(c)}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">')
    paths={
      'research':'<circle cx="21" cy="20" r="12"/><path d="M30 29L40 39M15 20h12M21 14v12"/>',
      'chart':'<path d="M6 39h36M9 35V26h7v9M22 35V18h7v17M35 35V8h7v27M8 18L20 9l10 4 12-10"/>',
      'practice':'<path d="M7 15h33v27H7zM15 15V7h17v8M7 24h33M20 21h7v7h-7z"/>',
      'compute':'<rect x="11" y="11" width="27" height="27" rx="3"/><path d="M18 3v8M26 3v8M34 3v8M18 38v8M26 38v8M34 38v8M3 18h8M3 26h8M3 34h8M38 18h8M38 26h8M38 34h8M19 19h11v11H19z"/>',
      'code':'<path d="M16 12L5 24l11 12M34 12l11 12-11 12M29 7L21 41"/>',
      'dialog':'<path d="M5 7h37v27H24L14 43v-9H5zM13 16h20M13 23h14"/>',
      'network':'<circle cx="25" cy="24" r="6"/><circle cx="7" cy="8" r="4"/><circle cx="43" cy="8" r="4"/><circle cx="7" cy="41" r="4"/><circle cx="43" cy="41" r="4"/><path d="M10 11l11 10M39 11L29 21M10 38l11-10M39 38L29 28"/>',
      'shield':'<path d="M25 4L42 11v13c0 10-9 18-17 22C17 42 8 34 8 24V11zM16 24l7 7 12-15"/>',
      'target':'<circle cx="25" cy="25" r="20"/><circle cx="25" cy="25" r="12"/><path d="M25 25L44 6M35 6h9v9"/>',
      'method':'<path d="M6 7h36v36H6zM6 18h36M18 7v36M30 18v25M6 30h36"/>',
      'check':'<path d="M14 8H6v36h36V8h-8M16 4h16v9H16zM14 27l8 8 15-16"/>'}
    f.items.append(paths[kind]+'</g>')

# 01. Three-way research relationship: concrete questions, evidence and outputs.
f=Figure(560)
f.rect(0,0,1000,560,'pale')
f.text(500,34,'核心命题：大模型驱动的智能化范式变革',24,'ink',True,'middle')
curve(f,'M 656,158 C 716,193 755,244 765,294','blue',3)
arrow(f,762,279,765,294,'blue',3)
curve(f,'M 672,420 C 570,490 430,490 336,420','teal',3)
arrow(f,348,431,336,420,'teal',3)
curve(f,'M 240,294 C 240,240 285,200 337,180','violet',3)
arrow(f,322,187,337,180,'violet',3)
f.circle(500,300,83,'white')
f.text(500,288,'人工智能',27,'ink',True,'middle')
f.text(500,322,'× 开源创新',23,'teal',True,'middle')
for x,y,n,title,c,ic,q,out in [
    (345,66,'01','范式研究','blue','research','技术与工作方式如何改变？','形成问题与分析框架'),
    (672,300,'02','产业洞察','teal','chart','变化发生在哪里、影响谁？','形成生态诊断与战略判断'),
    (17,300,'03','实践转化','violet','practice','什么方法能进入真实场景？','形成方案，并以实践修正研究')]:
    f.rect(x,y,311,141,'white');f.rect(x,y,311,4,c)
    icon(f,x+15,y+17,ic,c,.8)
    f.text(x+66,y+47,title,25,c,True)
    f.text(x+285,y+46,n,18,c,True,'end')
    f.text(x+15,y+84,q,19,'ink')
    f.text(x+15,y+117,out,17,'muted')
f.text(792,238,'以证据识别结构',16,'blue')
f.text(500,506,'以场景检验方法',16,'teal',False,'middle')
f.text(58,246,'以反馈修正问题',16,'violet')
f.text(500,536,'高校与科研机构 · 产业企业 · 开发者社区',19,'muted',False,'middle')
f.save('institute-research-system')

# 02. Five paradigms: a compact comparative visual, with technical and institutional layers.
f=Figure(744)
for x,t in [(70,'观察维度'),(180,'既有基础'),(466,'扩展方向'),(755,'研究重点')]:f.text(x,28,t,19,'muted',True)
f.line(0,47,1000,47)
rows=[
 ('01','计算','compute','blue','通用处理与指令执行','CPU 等通用计算架构','异构算力与神经网络','训练、推理与并行计算','架构与调度','算力怎样高效协同？'),
 ('02','开发','code','teal','逐行编码与工具操作','开发者组织研发流程','意图表达与智能体协同','生成、测试与交付衔接','目标与验证','怎样定义任务并检验结果？'),
 ('03','交互','dialog','violet','菜单、表单与图形界面','用户逐步操作功能','自然语言与任务委托','以对话组织复杂服务','体验与边界','怎样降低门槛并保留控制？'),
 ('04','协作','network','gold','组织内部积累与开发','知识和资源分散管理','开放资源与全球共建','共享、复用与社区接续','生态与激励','谁能参与、贡献和维护？'),
 ('05','治理','shield','orange','机构规则与事后审计','围绕单一责任主体','透明、可追溯的共同治理','规则、工具与多方参与','信任与责任','风险怎样被识别和处置？')]
for i,(n,t,ic,c,a,aa,b,bb,h,q) in enumerate(rows):
    y=64+i*128
    f.rect(0,y,1000,113,c,.04)
    f.rect(0,y,4,113,c)
    icon(f,18,y+18,ic,c,.7)
    f.text(71,y+43,t,25,c,True);f.text(74,y+77,n,17,'muted')
    f.wrap(180,y+39,a,213,19,'ink',True,27)
    f.wrap(180,y+78,aa,213,17.2,'muted',False,24)
    arrow(f,414,y+56,448,y+56,c,2.3)
    f.wrap(466,y+39,b,268,20,c,True,27)
    f.wrap(466,y+78,bb,268,17.2,'muted',False,24)
    f.text(755,y+39,h,20,'ink',True)
    f.wrap(755,y+78,q,224,17.2,'muted',False,24)
f.text(0,735,'研究观察方向：既有架构与新方式并存，变化速度取决于场景、资源与治理条件。',17,'muted')
f.save('institute-five-paradigms')

# 03. Six directions, organised by related questions rather than a decorative six-spoke wheel.
f=Figure(708)
f.text(317,30,'技术与组织能力',25,'blue',True,'middle')
f.text(792,30,'开放协作与信任',25,'teal',True,'middle')
f.line(135,47,500,47,'blue',2);f.line(610,47,975,47,'teal',2)
groups=[
 ('系统落地',3,'AI 系统级重构','与智能跃迁','组织决策 · 业务流程 · 商业模式','提炼可复用的智能转型方法',6,'关键系统的','可信开源治理','许可合规 · AI 物料清单 · 供应链','让责任、过程和风险可追溯','业务','与责任'),
 ('协作过程',2,'AI 原生研发','与智能体协同','意图驱动 · 知识激活','内生安全 · 自适应演化',5,'开发者体验','与智能化运营','愿参与 · 易贡献 · 有成长','开发者体验度量（DXM）','研发','与参与'),
 ('技术与证据',1,'AI 基础软件','与开发者生态','工具 · 文档 · 社区 · 协作机制','生态可开发性与全球对标',4,'全球开源洞察','与认知引擎','生态数据 · 发展框架 · 评估模型','区域生态诊断与企业开源评估','数据','与方法')]
for i,(layer,n,a,b,c1,c2,m,d,e,f1,f2,l1,l2) in enumerate(groups):
    y=72+i*204
    f.rect(0,y,116,177,'pale')
    for j,ch in enumerate(layer):f.text(58,y+53+j*28,ch,22,'muted',True,'middle')
    for x,num,title1,title2,desc1,desc2,col in [(135,n,a,b,c1,c2,'blue'),(610,m,d,e,f1,f2,'teal')]:
        f.rect(x,y,365,177,col,.055);f.rect(x,y,365,4,col)
        f.circle(x+28,y+33,16,col);f.text(x+28,y+39,f'{num:02}',16,'white',True,'middle',False)
        f.text(x+57,y+39,title1,23,col,True)
        f.text(x+57,y+70,title2,23,col,True)
        f.text(x+18,y+119,desc1,17.3,'ink')
        f.text(x+18,y+151,desc2,17.3,'muted')
    f.line(500,y+87,610,y+87,'line',2)
    f.circle(555,y+87,4,'soft')
    f.text(555,y+49,l1,17,'muted',False,'middle')
    f.text(555,y+71,l2,17,'muted',False,'middle')
f.text(0,701,'技术、协作与治理相互支撑；各方向通过具体场景、数据与方法形成联系。',17,'muted')
f.save('institute-six-directions')

# 04. Research-to-practice matrix: who uses the evidence, what can be done, what is checked.
f=Figure(700)
stages=[('01','需求定义','target','blue','明确对象与问题','场景、约束、责任主体'),('02','数据诊断','chart','teal','识别现状与差距','生态数据、行为与案例'),('03','方法设计','method','violet','形成可执行路径','模型、路线图与工具'),('04','实践检验','check','gold','观察结果并修正','成本、本地化与维护')]
for i,(n,t,ic,c,a,b) in enumerate(stages):
    x=i*252
    f.rect(x,0,244,182,c,.055);f.rect(x,0,244,4,c)
    icon(f,x+13,22,ic,c,.85)
    f.text(x+70,54,t,24,c,True)
    f.text(x+15,108,a,21,'ink',True)
    f.text(x+15,146,b,17.2,'muted')
    if i<3:arrow(f,x+225,83,x+265,83,c,2.5)
curve(f,'M 882,193 L 882,221 L 123,221 L 123,193','muted',1.5)
arrow(f,123,214,123,193,'muted',1.5)
f.rect(362,207,277,29,'white')
f.text(500,229,'实践反馈，返回研究问题',18,'muted',False,'middle')
for x,t in [(0,'使用者'),(175,'关键问题'),(475,'研究与咨询的切入点'),(790,'可检验的结果')]:f.text(x,286,t,19,'muted',True)
f.line(0,305,1000,305)
for i,(who,q1,q2,a1,a2,o1,o2,c) in enumerate([
 ('政府与公共机构','开放资源如何形成','本地公共能力？','区域生态诊断、技术风险图谱','人才与维护机制的建设路径','本地适配能力','持续服务结果','blue'),
 ('企业与研发团队','怎样将 AI 接入研发','与业务流程？','AI 原生研发成熟度、系统重构','开发者生态与供应链治理','成本与质量','安全与可维护性','teal'),
 ('项目与开发者社区','怎样让参与转为','长期贡献？','开发者体验度量、贡献路径','社区运营与协作机制','贡献能否持续','维护责任是否清楚','violet')]):
    y=322+i*111
    f.rect(0,y,1000,94,c,.04);f.rect(0,y,4,94,c)
    f.text(15,y+34,who,18.7,c,True)
    for x,aa,bb,fs in [(175,q1,q2,19),(475,a1,a2,17.6),(790,o1,o2,19)]:
        f.text(x,y+33,aa,fs,'ink');f.text(x,y+65,bb,fs,'muted')
f.text(0,696,'共同尺度：成本是否可承受、能否本地适配、谁来维护、服务结果是否持续。',16.7,'muted')
f.save('institute-practice-path')

def raw(x,y,w,t):return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{{t}}}'+'\n'
def bx(x,y,w,t,fs=10.5,lead=17,c='ink',bold=False,sans=False):return box(x,y,w,t,fs,lead,c,bold,sans)
def begin(n,kicker):return rf'\begin{{canvas}}\Header{{奇点智能研究院 · {kicker}}}{{teal}}\Footer{{{n:02}}}'+'\n'
def head(title,sub):return bx(15,28,180,title,21.5,29,'navy',True)+bx(15,44,180,sub,11.4,16,'teal',True)
def fig(y,name):return raw(15,y,180,rf'\includegraphics[width=180mm]{{.build/assets/{name}.pdf}}')
def sub(x,y,w,title,body,c='teal'):
    return bx(x,y,w,title,11.4,17,c,True)+bx(x,y+9,w,body,10.5,17)
end='\\end{canvas}\n';pages=[]

# Keep the original artwork as vectors and the original globe bitmap. Edit text layers only.
with fitz.open(R/'assets/approved-front-cover.pdf') as src, fitz.open() as base:
    base.insert_pdf(src)
    p=base[0]
    for b in p.get_text('blocks'):
        if 'Open Source Development Goals' in b[4] or '从普惠到质量' in b[4]:p.add_redact_annot(fitz.Rect(b[:4]),fill=False)
    p.apply_redactions(images=0,graphics=0,text=0)
    base.save(B/'assets/cover-base.pdf',garbage=4,deflate=True)
s='\\begin{canvas}\n'+r'\node[anchor=north west,inner sep=0pt] at (current page.north west){\includegraphics[width=210mm,height=297mm]{.build/assets/cover-base.pdf}};'+'\n'
s+=raw(22,182.4,166,r'\centering\sffamily\bfseries\fontsize{11.8}{15}\selectfont\color{white}精要版\hspace{4mm}{\digits\fontsize{9.6}{12}\selectfont ESSENTIAL EDITION}')
s+=raw(22,191.0,166,r'\centering\sffamily\fontsize{9.2}{12}\selectfont\color{white}从普惠到质量，从参与到影响')
for filename,x,width in [('xlab-ai.png',27,29),('siri.png',78,56),('ccosi.png',155,30)]:
    im=Image.open(R/'assets'/filename);xx,yy,x2,y2=im.getbbox();iw,ih=im.size
    trim=f'{xx}bp {ih-y2}bp {iw-x2}bp {yy}bp'
    s+=rf'\node[anchor=west,inner sep=0pt] at \Pos{{{x}}}{{279.9}}{{\includegraphics[width={width}mm,trim={trim},clip]{{assets/{filename}}}}};'+'\n'
pages.append(s+end)

s=begin(3,'定位与使命')+head('奇点智能研究院','Singularity Intelligence Research Institute')
s+=bx(15,57,180,'人工智能产业的“范式孵化器”：连接前沿研究、产业洞察与实践转化。',12.5,18,'ink',True)
s+=fig(74,'institute-research-system')
s+=bx(15,178,180,'图 I　研究体系：问题、证据与实践相互反馈。根据机构介绍整理。',8.1,12,'muted',False,True)
s+=sub(15,192,86,'由技术变化出发','奇点智能研究院由专业开发者社区 CSDN 与 IT 技术咨询平台 Boolan 联合发起，定位于创新型研究机构、科技智库与战略咨询平台。研究院联结高校、科研机构、产业企业与开发者社区，开展跨学科研究。','blue')
s+=sub(109,192,86,'以产业与社会价值为方向','研究院关注人工智能与开源创新如何共同改变技术底座、产业生态和社会治理。其使命是理解范式转换的逻辑，打通技术突破与产业应用的路径，使研究能够回应真实问题。')
s+=r'\Rect{15}{253}{180}{23}{paper}'+'\n'
s+=bx(20,257,170,'愿景',10.8,15,'teal',True)
s+=bx(40,256.8,150,'孕育思想、发展方法，推动智能技术成为普惠、可信、可持续的全球公共品。',10.6,16.8)
pages.append(s+end)

s=begin(4,'五大范式')+head('五大范式转换','从技术底座与研发方式，延伸到开放协作和共同治理')
s+=bx(15,57,180,'“范式”指组织技术与工作的基本方式。研究院用五个相互关联的观察方向，理解大模型带来的变化，并辨认变化真正落地所需的条件。',10.5,17)
s+=fig(77,'institute-five-paradigms')
s+=bx(15,214,180,'图 II　五大范式的观察坐标。根据机构介绍整理；箭头表示研究方向的扩展。',8.1,12,'muted',False,True)
s+=sub(15,226,86,'变化发生在不同层次','计算关注基础架构，开发与交互关注人怎样完成任务；协作与治理则把问题扩展到资源如何共享、责任怎样落实。技术进步需要与组织方式相互适配。','blue')
s+=sub(109,226,86,'开放贯穿五个方向','开放资源提供学习与复用的基础，社区连接不同主体，透明的规则支持信任。开放能否转为公共能力，还取决于使用门槛、持续维护与实际服务结果。')
pages.append(s+end)

s=begin(5,'研究布局')+head('六大研究方向','把技术能力、开发者生态与可信治理放在同一研究框架中')
s+=bx(15,57,180,'六个方向分别回应“系统怎样运行、团队怎样协作、组织怎样转型”以及“如何观察生态、改善参与、建立信任”。它们通过数据、方法和实际场景相互连接。',10.5,17)
s+=fig(77,'institute-six-directions')
s+=bx(15,207,180,'图 III　六大研究方向的关联结构。根据奇点智能研究院机构介绍整理。',8.1,12,'muted',False,True)
s+=sub(15,221,86,'让生态具备“可开发性”','基础软件的能力，需要通过工具、文档、社区与协作机制被开发者使用。研究院将生态可开发性与开发者体验联读，关注参与门槛、贡献路径和持续成长。','blue')
s+=sub(109,221,86,'让智能转型具有治理基础','研发和业务流程的变化，同时需要许可合规、供应链安全及责任机制。AI 物料清单（AIBOM）用于记录 AI 系统的组成与依赖，为追踪风险和持续维护提供基础。')
pages.append(s+end)

s=begin(6,'研究与实践')+head('从研究问题走向可检验的实践','以数据理解现状，以方法组织行动，以结果修正判断')
s+=bx(15,57,180,'研究院面向政府、企业与开发者开展研究与咨询。不同对象的问题各有侧重，但都需要把证据、方法和实践连接起来，才能将前沿判断转为可以讨论和检验的行动。',10.5,17)
s+=fig(77,'institute-practice-path')
s+=bx(15,206,180,'图 IV　研究进入实践的路径。根据机构介绍与本报告的公共能力框架整理。',8.1,12,'muted',False,True)
s+=sub(15,219,86,'AI 原生研发：形成改进的方法','AI 原生软件研发成熟度模型（AISMM）白皮书已在研究院官网公开。它围绕研发全生命周期、人机协作与组织流程展开，为团队识别能力差距、选择改进路径提供框架。','blue')
s+=sub(109,219,86,'全球开源洞察：形成决策的证据','本报告将生态地图、主体榜单、技术全景与模型网络联读，沿着参与、供给、复用、治理与公共价值展开，讨论开放资源怎样转化为可持续公共能力。')
s+=bx(15,271.7,180,'资料依据：奇点智能研究院机构介绍；《AI 原生软件研发成熟度模型》白皮书公开介绍。',7.8,11,'muted',False,True)
pages.append(s+end)

(R/'report.tex').write_text(r'\documentclass[11pt,a4paper]{article}\usepackage{layout}\begin{document}'+'\n'+''.join(pages)+r'\end{document}')
(R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
compile_tex()
new=fitz.open(O/'report.pdf');assert len(new)==5,len(new)
baseline=fitz.open(R/'assets/baseline-v0.4.pdf');doc=fitz.open()
replacements={0:0,2:1,3:2,4:3,5:4}
for i in range(len(baseline)):
    src=new if i in replacements else baseline;j=replacements.get(i,i)
    doc.insert_pdf(src,from_page=j,to_page=j)
# One-page insertion drops links to pages outside that one-page range. Restore existing TOC navigation.
for i,p in enumerate(baseline):
    if i not in replacements:
        for link in p.get_links():
            kept={k:v for k,v in link.items() if k not in ['xref','id']}
            doc[i].insert_link(kept)
doc.set_metadata({'title':'2026全球开源发展报告·精要版｜封面至第一章 v0.5','author':'全球开源发展报告编制组','subject':'附件封面基准修订；奇点智能研究院四页重构；PDF评审','keywords':'GOSD; Essential Edition; Singularity Intelligence Research Institute; Open Source'})
doc.set_toc([[1,'封面',1],[1,'编委会',2],[1,'奇点智能研究院',3],[2,'定位与使命',3],[2,'五大范式转换',4],[2,'六大研究方向',5],[2,'从研究走向实践',6],[1,'执行摘要',7],[1,'目录',9],[1,'引言与合作宣言',11],[1,'第一章　从开放协作到公共价值',14],[2,'1.1　人工智能时代的开源协作：双向重塑',15],[2,'1.2　开源发展目标：从开放资源到公共能力',18],[2,'1.3　观察方法：从生态对象到可比证据',20]])
# All page references are unchanged; preserve the live 23-page sequence.
doc.save(O/'GOSD_2026_Essential_Frontmatter_Chapter1_Review_v0.5.pdf',garbage=4,deflate=True)
print('Written',len(doc),'pages')
