"""Typeset native, editable Chinese text over reviewed poster artwork."""
from pathlib import Path
import json,re,subprocess,os,hashlib,shutil
from PIL import Image
import fitz

R=Path(__file__).resolve().parent
O=R/'output';A=R/'assets';V=R/'review'
O.mkdir(exist_ok=True);V.mkdir(exist_ok=True)
TOKENS=json.loads((R/'data/brand_tokens.json').read_text())
PAGES=[];BOXES=[];PN=0;SEQ=0
COLS=['blue','teal','green','gold','pink','violet']
def esc(s):
    return str(s).replace('\\',r'\textbackslash{}').replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#').replace('\n',r'\\ ')
def txt(x,y,w,s,fs=10.5,ld=17,c='ink',bold=False,serif=False,align='',mh=None,raw=False,center=False):
    global SEQ
    SEQ+=1; bid=f'p{PN}b{SEQ}'
    BOXES.append(dict(id=bid,page=PN,x=x,y=y,w=w,max_height=mh,text=s,center=center))
    content=(r'\rmfamily ' if serif else r'\sffamily ')+(r'\bfseries ' if bold else '')+rf'\fontsize{{{fs}}}{{{ld}}}\selectfont\color{{{c}}}'+align+(s if raw else esc(s))
    macro='CenterBox' if center else 'Box'
    return '\\'+macro+rf'{{{bid}}}{{{x}}}{{{y}}}{{{w}}}{{{content}}}'+'\n'
def rect(x,y,w,h,c):return rf'\Rect{{{x}}}{{{y}}}{{{w}}}{{{h}}}{{{c}}}'+'\n'
def rule(x,y,xx,c='line'):return rf'\Rule{{{x}}}{{{y}}}{{{xx}}}{{{c}}}'+'\n'
def image(x,y,w,path,h=None):
    return rf'\node[anchor=north west,inner sep=0pt] at \Pos{{{x}}}{{{y}}} {{\includegraphics[width={w}mm'+(f',height={h}mm' if h else '')+rf']{{{path}}}}};'+'\n'
def card(x,y,w,h,col='blue',accent=0):
    s=rf'\fill[{col}!9,rounded corners=3mm] \Pos{{{x+.6}}}{{{y+1}}} rectangle \Pos{{{x+w+.6}}}{{{y+h+1}}};'+'\n'
    s+=rf'\shade[top color=white,bottom color={col}!7,draw=white,line width=1pt,rounded corners=3mm] \Pos{{{x}}}{{{y}}} rectangle \Pos{{{x+w}}}{{{y+h}}};'+'\n'
    if accent:
        s+=rf'\shade[left color={col},right color={col}!60!white,rounded corners=3mm] \Pos{{{x}}}{{{y}}} rectangle \Pos{{{x+accent}}}{{{y+h}}};'+'\n'
    return s
def badge(x,y,n,c='blue',r=3.5):
    return rf'\shade[ball color={c}] \Pos{{{x}}}{{{y}}} circle[radius={r}mm];\node[text=white,font=\sffamily\bfseries\fontsize{{10}}{{10}}\selectfont,inner sep=0pt] at \Pos{{{x}}}{{{y}}} {{{n}}};'+'\n'
def emblem(x,y,w,word='GOSD'):
    return image(x,y,w,'assets/osdgs-symbol-display.pdf')+txt(x,y+w*.5,w,word,w*.42,w*.48,'navy',True,True,r'\centering\wordmark ',raw=False,center=True)
def logo(x,y,w,name):
    im=Image.open(A/name);a,b,c,d=im.getbbox();iw,ih=im.size
    return rf'\node[anchor=north west,inner sep=0pt] at \Pos{{{x}}}{{{y}}}'+'{'+rf'\includegraphics[width={w}mm,trim={a}bp {ih-d}bp {iw-c}bp {b}bp,clip]{{assets/{name}}}'+'};\n'
def logo_center(x,cy,w,name):
    im=Image.open(A/name);a,b,c,d=im.getbbox()
    return logo(x,cy-w*(d-b)/(c-a)/2,w,name)
def start(title='',en='',num=None,small=False,institute=False,white=False):
    global PN
    PN+=1
    s='\\begin{canvas}\n'
    if not white:s+=image(0,0,210,'assets/inner-background.png',297)
    s+=txt(14,7.7,25,'GOSD',12,14,'navy',True,True)+txt(41,9.1,127,'2026 全球开源发展报告  ·  精要版',7.8,11,'navy')
    s+=rule(14,17.3,136)
    for i,d in enumerate(TOKENS['dimensions']):
        c='brand'+str(i);s+=rf'\definecolor{{{c}}}{{HTML}}{{{d["hero_color"][1:]}}}'+rect(139+i*5.4,16.9,4.7,.65,c)
    if title:
        if institute:
            s+=rf'\shade[left color=navy,right color=blue!75!navy,rounded corners=3mm] \Pos{{14}}{{27}} rectangle \Pos{{116}}{{51}};'+'\n'
            s+=logo(19,31,91,'siri.png')
            s+=txt(14,55,154,en,9.5,14,'navy',False,False,mh=10)
        else:
            s+=emblem(13,24,34)
            s+=txt(54,27,142,title,22 if small else 29,31 if small else 39,'navy',True,True,mh=20)
            s+=txt(55,45 if not small else 47,141,en,10.8,15,'navy',False,True,mh=12)
            s+=rule(55,58,78,'blue')
    if num is not None:
        s+=rule(14,284,196)
        s+=txt(14,287,150,'GOSD  /  OPEN SOURCE · A SHARED INTELLIGENT FUTURE',7.0,10,'navy')
        s+=txt(182,286.2,14,str(num),11,14,'navy',True,False,r'\raggedleft ')
    return s
def finish(s):PAGES.append(s+'\\end{canvas}\n')
def institute_start(title,subtitle,num,first=False):
    global PN
    PN+=1
    s='\\begin{canvas}\n'
    s+=rect(0,0,210,297,'white')
    if first:
        s+=logo(15,17,115,'siri-color.png')
        s+=txt(15,52,180,title,20,29,'siriink',True,True,mh=15)
        s+=txt(15,67,180,subtitle,11.8,18,'siriteal',True,mh=10)
    else:
        s+=logo(15,12,58,'siri-color.png')
        s+=txt(117,17,78,'RESEARCH  /  STRATEGY  /  PRACTICE',7.4,11,'siriink',False,False,r'\raggedleft ',mh=7)
        s+=rule(15,32,195,'sirifaint')+rect(15,31.5,15,1,'siriorange')
        s+=txt(15,40,180,title,22.5,31,'siriink',True,True,mh=17)
        s+=txt(15,57,180,subtitle,11.1,17,'siriteal',True,mh=11)
    s+=rule(15,284,195,'sirifaint')+rect(15,283.5,15,1,'siriorange')
    s+=txt(15,288,165,'SINGULARITY INTELLIGENCE RESEARCH INSTITUTE',7.2,10,'siriink',mh=5)
    s+=txt(182,286.5,13,num,10.5,14,'siriink',True,False,r'\raggedleft ',mh=7)
    return s
def two_cols(y,heads,bodies,mh=42,fs=10.3,ld=16.5):
    s=''
    for x,c,t,b in zip([15,110],['siriteal','siriink'],heads,bodies):
        s+=txt(x,y,85,t,11.1,16.5,c,True,mh=8)
        s+=txt(x,y+9,85,b,fs,ld,'ink',False,True,mh=mh)
    return s

# 01. Cover: institution logos directly over the continuous artwork.
PN+=1;s='\\begin{canvas}\n'+image(0,0,210,'assets/cover-background.png',297)
s+=emblem(65,15,80)
s+=txt(14,98,182,'2026',40,45,'blue',True,True,r'\centering ',mh=19)
s+=txt(10,119,190,'全球开源发展报告',46,52,'navy',True,True,r'\centering ',mh=20)
s+=txt(13,141,184,'Global Open Source Development Report',13.0,19,'navy',False,True,r'\centering ',mh=13)
s+=txt(15,158,180,'精要版  /  ESSENTIAL EDITION',12.3,18,'navy',True,False,r'\centering ',mh=12)
s+=rect(15,175,180,.35,'blue!25')
s+=txt(15,180,180,'参与  ·  供给  ·  复用  ·  治理  ·  公共价值',10.5,16,'navy',False,False,r'\centering ',mh=10)
s+=logo_center(21,280.4,36,'xlab-ai.png')+logo_center(72,280.4,72,'siri-white.png')+logo_center(160,280.4,27,'ccosi.png')
for i,d in enumerate(TOKENS['dimensions']):
 c='brand'+str(i);s+=rf'\definecolor{{{c}}}{{HTML}}{{{d["hero_color"][1:]}}}'+rect(21+i*16.7,291,15,0.7,c)
finish(s)

# 02. White title page / reference details provide a quiet transition into content.
s=start(num='i',white=True)
s+=emblem(15,31,31)
s+=txt(15,83,180,'2026',38,44,'blue',False,True,mh=20)
s+=txt(15,107,180,'全球开源发展报告',29,38,'navy',True,True,mh=20)
s+=txt(15,130,180,'Global Open Source Development Report',16,23,'navy',False,True,mh=15)
s+=rule(15,152,195,'blue')
s+=txt(15,163,180,'精要版  /  ESSENTIAL EDITION',14,21,'navy',True,mh=13)
s+=txt(15,189,180,'关于本报告',15,22,'navy',True,True,mh=12)
about=[('研究问题','开放资源怎样转化为可持续公共能力？'),('主要对象','人才、组织、项目，以及代码、模型、数据及其协作关系。'),('主统计期','2025 年 7 月 1 日至 2026 年 6 月 30 日。'),('阅读口径','历史材料、外部窗口和期后快照分别标注；以各图说明为准。'),('主要读者','政府与国际组织决策者，兼顾产业、基金会、学术与社区。')]
for j,(t,b) in enumerate(about):
 y=207+j*12;s+=txt(15,y,25,t,9.5,15,'blue',True,mh=10)+txt(44,y,151,b,10.0,15.3,'ink',False,True,mh=11)
finish(s)

# 03. Preserve every name, grouping and order from v0.6.
s=start('编委会','Editorial Board','ii')
for y,h,title,names,w in [(84,29,'主编',['王伟','李建忠'],65),(120,29,'联合主席',['王建民','张延川'],65),(156,34,'副主席',['陈钟','胡春明','黄韬','高跃','堵俊平','蒋涛'],27)]:
 s+=card(14,y,182,h,'blue' if y==84 else 'teal' if y==120 else 'green')
 s+=txt(20,y+5,165,title,11,16,'navy',True,mh=8)
 for i,n in enumerate(names):s+=txt(20+i*w,y+16,26,n,10.5,16.5,'ink',mh=10)
s+=card(14,197,182,79,'violet')+txt(20,203,170,'编委',11,16,'navy',True,mh=9)
names=[['吴发国','崔鹤鸣','于仕琪','周明辉','胡钰','黄向东','王博','余跃','彭煜玮','陈阳'],['顾荣','金耀辉','游兰','王莹','张宇霞','何海洋','杨丽蕴','张俊霞','郭雪','任旭东'],['许哲平','姜宁','边思康','马红伟','郭炜','谭中意','林旅强','江波','陈阳','陈绪'],['贾开','郑宏威','竺彩华','刘广','隆云滔','乔嘉林','吴咏炜','瞿晶晶','于晓轶','邹慧'],['夏小雅','赵生宇','武剑凌','方心雨','王哲','汤文泰','董超','彭佳恒','张震','李沫南']]
for j,row in enumerate(names):
 for i,n in enumerate(row):s+=txt(20+i*17.2,218+j*10.3,17.2,n,10.5,16.5,'ink',mh=9)
finish(s)

# 04-07. Self-contained institute section, with transparent vector diagrams.
s=institute_start('人工智能产业的“范式孵化器”','连接前沿研究、产业洞察与实践转化。','iii',first=True)
s+=image(16,86,178,'assets/institute-research-system.pdf')
s+=txt(15,192,180,'研究体系：问题、证据与实践相互反馈',8.3,12.5,'muted',mh=7)
s+=two_cols(207,['由技术变化出发','以产业与社会价值为方向'],['奇点智能研究院由专业开发者社区 CSDN 与 IT 技术咨询平台 Boolan 联合发起，定位于创新型研究机构、科技智库与战略咨询平台。研究院联结高校、科研机构、产业企业与开发者社区，开展跨学科研究。','研究院关注人工智能与开源创新如何共同改变技术底座、产业生态和社会治理。其使命是理解范式转换的逻辑，打通技术突破与产业应用的路径，使研究能够回应真实问题。'],39)
s+=rule(15,260,195,'sirifaint')+txt(15,270.4,20,'愿景',10.5,16,'siriteal',True,mh=9,center=True)+txt(37,270.4,158,'孕育思想、发展方法，推动智能技术成为普惠、可信、可持续的全球公共品。',10.2,15.6,'ink',False,True,mh=13,center=True)
finish(s)

inst=[
 ('五大范式转换','Paradigm Shifts','iv','从技术底座与研发方式，延伸到开放协作和共同治理','“范式”指组织技术与工作的基本方式。研究院用五个相互关联的观察方向，理解大模型带来的变化，并辨认变化真正落地所需的条件。','institute-five-paradigms',154,116,'图 II　五大范式的观察坐标。根据机构介绍整理；箭头表示研究方向的扩展。',['变化发生在不同层次','开放贯穿五个方向'],['计算关注基础架构，开发与交互关注人怎样完成任务；协作与治理则把问题扩展到资源如何共享、责任怎样落实。技术进步需要与组织方式相互适配。','开放资源提供学习与复用的基础，社区连接不同主体，透明的规则支持信任。开放能否转为公共能力，还取决于使用门槛、持续维护与实际服务结果。']),
 ('六大研究方向','Research Directions','v','把技术能力、开发者生态与可信治理放在同一研究框架中','六个方向分别回应“系统怎样运行、团队怎样协作、组织怎样转型”以及“如何观察生态、改善参与、建立信任”。它们通过数据、方法和实际场景相互连接。','institute-six-directions',160,115,'图 III　六大研究方向的关联结构。根据奇点智能研究院机构介绍整理。',['让生态具备“可开发性”','让智能转型具有治理基础'],['基础软件的能力，需要通过工具、文档、社区与协作机制被开发者使用。研究院将生态可开发性与开发者体验联读，关注参与门槛、贡献路径和持续成长。','研发和业务流程的变化，同时需要许可合规、供应链安全及责任机制。AI 物料清单（AIBOM）用于记录 AI 系统的组成与依赖，为追踪风险和持续维护提供基础。']),
 ('从研究走向实践','From Research to Practice','vi','以数据理解现状，以方法组织行动，以结果修正判断','研究院面向政府、企业与开发者开展研究与咨询。不同对象的问题各有侧重，但都需要把证据、方法和实践连接起来，才能将前沿判断转为可以讨论和检验的行动。','institute-practice-path',160,113,'图 IV　研究进入实践的路径。根据机构介绍与本报告的公共能力框架整理。',['AI 原生研发：形成改进的方法','全球开源洞察：形成决策的证据'],['AI 原生软件研发成熟度模型（AISMM）白皮书已在研究院官网公开。它围绕研发全生命周期、人机协作与组织流程展开，为团队识别能力差距、选择改进路径提供框架。','本报告将生态地图、主体榜单、技术全景与模型网络联读，沿着参与、供给、复用、治理与公共价值展开，讨论开放资源怎样转化为可持续公共能力。'])]
for title,en,num,sub,intro,fig,width,hh,cap,heads,bodies in inst:
 if num=='vi':title='从研究问题走向可检验的实践'
 width=176;hh={'iv':130.944,'v':124.608,'vi':123.2}[num]
 s=institute_start(title,sub,num)
 s+=txt(15,73,180,intro,10.3,16.5,'ink',False,True,mh=17)
 s+=image((210-width)/2,95,width,'assets/'+fig+'.pdf')
 caption={'iv':'五大范式的观察坐标','v':'六大研究方向的关联结构','vi':'研究进入实践的路径'}[num]
 s+=txt(15,hh+98,180,caption,8.2,12.3,'muted',mh=7)
 if num=='vi':
  bodies[1]=bodies[1].replace('本报告','《2026 全球开源发展报告》')
 s+=two_cols(hh+108,heads,bodies,32,9.9,15.8)
 finish(s)

# 08. Contents and purposeful reading paths; avoid invented body page numbers.
s=start('目录','Table of Contents','vii')
s+=txt(15,80,115,'前置内容',12.5,18,'navy',True,True,mh=10)
front=[('编委会','ii'),('奇点智能研究院','iii—vi'),('执行摘要','viii—ix'),('全书结构与阅读路径','x'),('如何读懂一页综合图','xi'),('引言与国际合作宣言','xii—xiv')]
for j,(t,n) in enumerate(front):
 y=94+j*8.2;s+=txt(15,y,90,t,10,14.3,'ink',mh=7)+txt(110,y,22,n,9.5,14.3,'blue',False,False,r'\raggedleft ',mh=7)
s+=txt(15,147,117,'正文 · 六个章节',12.5,18,'navy',True,True,mh=10)
toc=[('01','从开放协作到公共价值','AI 与开源的双向重塑 · 目标与方法','01'),('02','全球开源生态地图','活跃 · 贡献 · 项目 · 人才 · 资产 · 行业',''),('03','全球开源影响力排行榜','行政区划 · 企业 · 基金会 · 项目 · 模型',''),('04','全球开源技术全景洞察','智能体 · 模型 · 云 · 数据库 · RISC-V',''),('05','全球开源大模型发展洞察','供给与贡献 · 派生网络 · 开放条件',''),('06','关键洞察、前瞻与战略建议','十二项洞察 · 十大前瞻 · 十大战略建议','')]
for j,(n,t,b,pg) in enumerate(toc):
 y=160+j*17.2;c=COLS[j]
 s+=card(14,y,119,15.2,c,18)+txt(16,y+7.6,14,n,14,17,'white',True,True,r'\centering ',mh=10,center=True)
 s+=txt(36,y+2.1,93,t,10.3,14,'navy',True,mh=7)+txt(36,y+8.5,93,b,7.6,10.8,'muted',mh=6)
s+=txt(15,267,119,'附录　指标、方法与数据来源  ｜  致谢',8.8,13.5,'navy',True,mh=8)
s+=txt(143,80,54,'阅读路径',15,21,'navy',True,True,mh=12)
paths=[('快速概览','执行摘要 → 第六章','先把握核心判断与行动方向。','blue'),('寻找合作','第二章 → 第三章','由资源位置进入具体组织、项目与模型。','teal'),('深入研究','第四章 → 第五章','联读技术全景、模型派生和开放条件。','violet')]
for j,(t,p,b,c) in enumerate(paths):
 y=100+j*52;s+=card(141,y,55,46,c)+txt(146,y+6,45,t,12.5,18,'navy',True,True,mh=10)+txt(146,y+19,45,p,9.4,14.2,c,True,mh=13)+txt(146,y+30,45,b,9.0,14.2,'ink',False,True,mh=16)
s+=txt(143,260,52,'方法与口径：第一章、附录。',8.7,13.2,'muted',mh=14)
finish(s)

# 09. Executive claims: compact poster statements from the latest reviewed chapters.
s=start('执行摘要','Executive Summary','viii')
s+=txt(15,79,180,'开放资源怎样转化为可持续公共能力？',17,24,'navy',True,True,mh=13)
s+=txt(15,95,180,'以全球协作形成体系能力，以公共价值引领开放创新。地图、榜单、技术全景与模型网络，共同解释人工智能时代的开源发展。',10.5,16.8,'ink',False,True,mh=17)
claims=[
 ('01','全球协作','把分散优势连接成体系能力','参与增长、资源供给和协作影响具有不同结构。持续的技术连接与共同维护，使不同角色的优势能够相互支撑。','多种发展位置 · 技术连接 · 再创造角色','第二、三、四章','blue'),
 ('02','中国贡献','在全球接续中理解模型开源','中国的模型和工程工具进入跨境适配与再创造。应沿具体资源、技术分层和接续关系理解贡献，而非推导单一的总体领先。','模型扩散 · 分层演进 · 可信治理','第三、四、五章','teal'),
 ('03','AI 普惠','让开放资源成为本地持续能力','较宽松的使用权限，需要训练材料、运行条件和本地维护共同支撑。合作应由当地需求、知识与参与能力共同定义。','参与路径 · 完整交付 · 基金会支持','第二、三、五章','pink'),
 ('04','中国区域','以资源互补组织产业与人才','模型、数据、企业与人才具有不同空间结构。地方投入应围绕共同项目、持续职责和实际交付，形成跨区域协作。','产业分工 · 人才成长 · 城市互补','第二、三、五章','violet')]
for j,(n,tag,t,b,keys,ref,c) in enumerate(claims):
 y=118+j*36.7;s+=card(14,y,182,33.5,c,23)
 s+=txt(15,y+5,21,n,23,29,'white',True,True,r'\centering ',mh=17)
 s+=txt(16,y+22,19,tag,8.5,12,'white',True,False,r'\centering ',mh=8)
 s+=txt(43,y+3.4,147,t,12.7,18,'navy',True,True,mh=9)
 s+=txt(43,y+13,147,b,10.0,15.3,'ink',False,True,mh=15)
 s+=txt(43,y+27,147,keys+'  ｜  '+ref,8.3,11.5,c,mh=6)
finish(s)

# 10. The report's distinctive scope and four decision-facing commitments.
s=start('从证据到行动','From Evidence to Action','ix',small=True)
s+=txt(15,79,180,'从中国出发观察全球，把结构性发现转为可检验的行动。',13,20,'navy',True,True,mh=13)
features=[('AI 全景与体系化观察','联读地图、排行榜、技术全景与模型网络，连接人才、组织、项目及代码、模型、数据。','blue'),('跨平台与全域数据视野','连接代码协作、模型供给与再创造，观察不同平台上的资源、主体和协作关系。','teal'),('中国出发的全球视野','将中国贡献放入全球接续，兼顾欧美积累和全球南方的参与路径。','pink'),('服务决策与 AI 普惠','用成本、本地化、维护和结果检验公共投入，识别资源转为能力的条件。','violet')]
for j,(t,b,c) in enumerate(features):
 x=14+(j%2)*94;y=99+(j//2)*39
 s+=card(x,y,88,34,c)+txt(x+5,y+5,78,t,11.4,16,c,True,mh=9)+txt(x+5,y+16,78,b,9.5,14.5,'ink',False,True,mh=17)
s+=txt(15,181,180,'四项行动主张',14,20,'navy',True,True,mh=12)
acts=[('共同建设','以接口适配、共同测试和长期维护连接全球体系。','blue'),('跨境接续','沿真实复用关系组织联合评测、工程适配和版本维护。','teal'),('本地主导','把完整材料、可承受成本与当地伙伴治理纳入合作。','pink'),('区域互补','以跨城项目和持续贡献职责连接企业、高校与社区。','violet')]
for j,(t,b,c) in enumerate(acts):
 cy=202+j*18;s+=badge(19,cy,str(j+1),c,3.4)+txt(27,cy,29,t,10.9,16,c,True,mh=9,center=True)+txt(58,cy,137,b,10.4,16,'ink',False,True,mh=13,center=True)
finish(s)

# 11. Whole-book architecture, current names and the unchanged ten-direction registry.
s=start('全书结构与阅读路径','Report Architecture','x',small=True)
for j,(t,b,c) in enumerate([('参与','谁进入协作','blue'),('供给','形成什么资源','teal'),('复用','由谁接续创造','green'),('治理','如何共同维护','gold'),('公共价值','服务哪些需要','violet')]):
 x=14+j*36.9;s+=card(x,81,34.4,22,c)+txt(x+2,84,30.4,t,11,16,c,True,False,r'\centering ',mh=8)+txt(x+2,94,30.4,b,8,11.5,'ink',False,False,r'\centering ',mh=7)
s+=rf'\draw[blue!20,line width=.7pt] \Pos{{105}}{{165}} circle[radius=30mm];\draw[teal!18,line width=.45pt] \Pos{{105}}{{165}} circle[radius=34mm];'+'\n'
s+=emblem(78,138,54)
s+=txt(79,196,52,'四个研究视角\n相互解释',10.5,16,'navy',True,True,r'\centering ',mh=17)
chapters=[(14,111,'01','共同目标与方法','从开放协作\n到公共价值','blue'),(14,150,'02','生态地图 · GOSO','参与与资源\n在哪里？','teal'),(14,189,'03','主体榜单 · GOSR','谁形成怎样的\n协作影响？','green'),(141,111,'04','技术全景 · GOSL','哪些技术共同\n支撑运行？','gold'),(141,150,'05','模型生态 · GOSM','供给怎样被复用，\n开放条件怎样？','pink'),(141,189,'06','洞察与行动','12 项洞察 · 10 项前瞻\n10 项战略建议','violet')]
for x,y,n,t,b,c in chapters:
 s+=card(x,y,55,34,c)+txt(x+4,y+3,47,'第 '+n+' 章',9,13,c,True,mh=7)+txt(x+4,y+11,47,t,10.1,15,'navy',True,mh=8)+txt(x+4,y+21,47,b,8.7,12,'ink',False,False,mh=11)
 sx=x+55 if x==14 else x;ex=76 if x==14 else 134
 s+=rf'\draw[{c}!55,line width=.6pt] \Pos{{{sx}}}{{{y+17}}} -- \Pos{{{ex}}}{{{165+(y-150)*.45}}};'+'\n'
s+=txt(15,233,180,'贯穿全书：OSDGs 四支柱 · 十个观察方向',11.2,16,'navy',True,True,mh=9)
short=['规模与\n密度','生态\n多样性','代码\n产出','模型\n开放供给','数据\n开放供给','代码\n影响力','模型\n影响力','数据集\n影响力','治理\n成熟度','公共\n福祉']
for i,d in enumerate(TOKENS['dimensions']):
 x=14+i*18.5;c='brand'+str(i)
 s+=card(x,246,16,29,c)+txt(x+1,249,14,d['id'],7.5,10,c,True,False,r'\centering ',mh=6)
 s+=image(x+5,255,6,'assets/'+d['id']+'.pdf')
 s+=txt(x+.6,263,14.8,short[i],7.6,10.4,'navy',True,False,r'\centering ',mh=10)
finish(s)

# 12. Latest genuine chapter page, with all callout connectors outside data.
s=start('如何读懂一页综合图','Reading a Composite Figure','xi',small=True)
s+=txt(15,79,180,'以第五章图 5-1 为例：先读问题，联读四区证据，再按 ①—④ 阅读解释，并核对时间、分母与样本范围。',10.4,16.8,'ink',False,True,mh=18)
s+=card(12.5,100,124.5,172,'blue')+image(14,101,122,'assets/latest-reading-example.pdf')
calls=[('A',107,102,'先读问题','标题说明观察对象；导语给出问题与背景。','blue'),('B',166,142,'联读四区证据','地图看位置，榜单找主体，结构与份额揭示差异。','teal'),('C',222,201,'核对时间与分母','平台总量、地域样本与累计下载各有口径，分别解释。','pink'),('D',251,242,'按编号读解释','①—④ 回到对应图区，读清事实、判断与行动含义。','violet')]
for lab,anchor,y,t,b,c in calls:
 s+=rf'\draw[{c},line width=.75pt] \Pos{{137}}{{{anchor}}} -- \Pos{{142}}{{{anchor}}} -- \Pos{{142}}{{{y+4}}} -- \Pos{{147}}{{{y+4}}};'+'\n'
 s+=badge(149,y+4,lab,c,3.2)+txt(155,y+4,41,t,10.4,15,c,True,mh=14,center=True)+txt(148,y+15,48,b,10,15.7,'ink',False,True,mh=27)
finish(s)

# 13-15. Declaration: retain current text and principles, use the user-requested title.
old=json.loads((R/'data/frontmatter-v05-text.json').read_text())
def clean(t):
 t=t.replace('\n','').replace('⸺','——')
 t=re.sub(r'(?<=[\u4e00-\u9fff])(?=[A-Za-z])',' ',t)
 return re.sub(r'(?<=[A-Za-z0-9])(?=[\u4e00-\u9fff])',' ',t)
p11,p12,p13=old[10:13]
sec1=clean(p11.split('I. 时代呼唤：迈向智能协作新纪元')[1].split('II. 共同愿景：构建智能共治的数字文明')[0])
sec2=clean(p11.split('II. 共同愿景：构建智能共治的数字文明')[1])
principles=[]
for i,ch in enumerate('一二三四五六'):
 lines=p12.split('原则'+ch+'：')[1].splitlines();body=re.split(r'原则[一二三四五六七]：|第[二三]层：','\n'.join(lines[2:]))[0]
 principles.append((lines[0],lines[1],clean(body)))
ls=p13.split('原则七：坚持开源普惠')[1].splitlines()
principles.append(('坚持开源普惠',ls[1],clean('\n'.join(ls[2:]).split('IV. 行动共识：')[0])))
act=clean(p13.split('IV. 行动共识：迈向全球AI 治理新格局')[1].split('结语')[0])
ending=clean(p13.split('结语')[1].split('图引1')[0])
(R/'data/declaration.json').write_text(json.dumps(dict(title='全球开源人工智能国际合作宣言',sec1=sec1,sec2=sec2,principles=principles,action=act,ending=ending),ensure_ascii=False,indent=2))

s=start('引言','Open Source · A Shared Intelligent Future','xii')
s+=txt(15,79,180,'全球开源人工智能国际合作宣言',18.5,27,'navy',True,True,mh=16)
s+=txt(15,95,180,'开源共创智能未来：迈向全球 AI 治理新纪元',9.6,15,'blue',mh=10)
s+=txt(15,109,180,'以开放协作与 AI 普惠为共同方向，以生态证据理解发展，以持续使用、改进和维护检验公共能力。',10.5,16.8,'ink',False,True,mh=19)
s+=card(14,136,182,85,'blue',10)+txt(28,141,161,'I. 时代呼唤：迈向智能协作新纪元',12.1,18,'navy',True,True,mh=10)
s+=txt(28,153,161,sec1,10.1,16.2,'ink',False,True,mh=64)
s+=card(14,228,182,50,'teal',10)+txt(28,233,161,'II. 共同愿景：构建智能共治的数字文明',12.1,18,'navy',True,True,mh=10)
s+=txt(28,245,161,sec2,10.1,16.2,'ink',False,True,mh=31)
finish(s)

s=start('合作宣言 · 核心原则','Principles for Open Cooperation','xiii',small=True)
s+=txt(15,79,180,'III. 核心原则与行动框架',13,20,'navy',True,True,mh=12)
for j,(t,q,b) in enumerate(principles[:5]):
 y=102+j*34.1;c=['blue','teal','green','gold','pink'][j]
 if j==0:s+=txt(15,92,180,'第一层  筑牢智能时代基石',8.6,12,'blue',True,mh=7)
 if j==2:s+=txt(15,y,180,'第二层  夯实伦理治理支柱',8.6,12,'green',True,mh=7)
 # Gap before the second layer is included in the last two cards' positions.
 if j>=2:y+=10
 s+=card(14,y,182,30.3,c,12)+txt(14.5,y+15.15,11,str(j+1),17,22,'white',True,True,r'\centering ',mh=13,center=True)
 s+=txt(31,y+3.5,70,'原则'+'一二三四五'[j]+'：'+t,10.7,15.5,'navy',True,mh=9)
 s+=txt(107,y+4,84,q,9.1,13.4,c,False,True,r'\raggedleft ',mh=8)
 s+=txt(31,y+13,159,b,9.8,15.2,'ink',False,True,mh=17)
finish(s)

s=start('合作宣言 · 共创未来','From Principles to Shared Value','xiv',small=True)
s+=txt(15,79,180,'第三层  共创社会价值未来',13,20,'navy',True,True,mh=12)
for j,(t,q,b) in enumerate(principles[5:]):
 y=97+j*42;c=['green','violet'][j]
 s+=card(14,y,182,37,c,14)+txt(15,y+18.5,12,str(j+6),20,25,'white',True,True,r'\centering ',mh=16,center=True)
 s+=txt(33,y+4,80,'原则'+'六七'[j]+'：'+t,11.4,17,'navy',True,mh=10)+txt(115,y+5,75,q,9.3,14,c,False,True,r'\raggedleft ',mh=9)
 s+=txt(33,y+16,157,b,10.0,15.5,'ink',False,True,mh=20)
s+=txt(15,188,180,'IV. 行动共识：迈向全球 AI 治理新格局',12.2,18,'navy',True,True,mh=11)
s+=txt(15,201,180,act,10.3,16.8,'ink',False,True,mh=30)
s+=card(14,237,182,40,'blue')+txt(20,242,170,'结语',11.2,16,'blue',True,True,mh=9)+txt(20,253,170,ending,10.4,17.2,'ink',False,True,mh=23)
finish(s)

assert len(PAGES)==15,len(PAGES)
(R/'report.tex').write_text(r'\documentclass[11pt,a4paper]{article}\usepackage{layout}\begin{document}'+'\n'+''.join(PAGES)+r'\end{document}')
(V/'text-box-plan.json').write_text(json.dumps(BOXES,ensure_ascii=False,indent=2))
env=os.environ.copy();env['TEXMF']='{/usr/share/texmf,/usr/share/texlive/texmf-dist}'
var=R/'.texmf-var';var.mkdir(exist_ok=True);env['TEXMFVAR']=str(var);env['TEXFORMATS']=str(var)
if not (var/'xelatex.fmt').exists():
 with (O/'format-build.txt').open('w') as f:subprocess.run(['xelatex','-ini','-etex','-interaction=nonstopmode','-jobname=xelatex',f'-output-directory={var}',r'\input xelatex.ini'],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
passes=1 if '--incremental' in __import__('sys').argv and (O/'report.aux').exists() else 2
for i in range(1,passes+1):
 with (O/f'build-{i}.txt').open('w') as f:subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory=output','report.tex'],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
print('Compiled',len(PAGES),'frontmatter pages.')
