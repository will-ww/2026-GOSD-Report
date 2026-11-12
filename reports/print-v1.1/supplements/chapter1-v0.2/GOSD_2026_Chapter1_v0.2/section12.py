from build import *

C.update(violet='#68509B',orange='#AD6D25',pale_blue='#EEF4FA',pale_teal='#EDF6F5',pale_violet='#F3F0F8',pale_gold='#FAF4E8')

SOURCES=[
 dict(id='S6',name='联合国：可持续发展目标（SDGs）',url='https://sdgs.un.org/goals',date='2030年可持续发展议程；2015年通过',locator='17个目标与全球伙伴关系',checked='2026-11-10',scope='发展目标背景，不作为本报告测量结果。'),
 dict(id='S7',name='Digital Public Goods Alliance：Digital Public Goods Standard',url='https://www.digitalpublicgoods.net/standard',date='当前公开标准；读取2026-11-10',locator='9项指标；Disclaimers & Considerations第1条',checked='2026-11-10',scope='现行资源标准参照；认可针对核心方案设计，不包含地方实施效果评价。九项要求为中文概述；标准CC BY-SA 4.0。'),
 dict(id='S8',name='Stinckwich等：AI Systems as Digital Public Goods',url='https://unu.edu/sites/default/files/2026-06/AI_Systems_as_Digital_Public_Goods_0.pdf',date='2026-06-25',locator='第14、43—46、50—52页',checked='2026-11-10',scope='UNU与ADB、UN ODET研究；主期内发布，建议为非约束性研究输入。本节不转载原图，不引用存在21/20差异的访谈百分比。'),
 dict(id='S9',name='GOSD报告宪法与第一章v0.5研究框架',url='https://github.com/will-ww/2026-GOSD-Report/tree/main/editions/insights/chapters/01/v0.5',date='2026-11-09起的现行框架；读取2026-11-10',locator='四支柱、十方向、29项候选指标；主统计期及四视角职责',checked='2026-11-10',scope='报告编制组研究设计，不是联合国认证、国家综合评分或全部已实测指标。'),
]

def arrow(f,x,y,xx,yy,c='muted',sw=2,dash=None):
    f.line(x,y,xx,yy,c,sw,dash)
    a=math.atan2(yy-y,xx-x);L=8
    f.path([(xx-L*math.cos(a-.5),yy-L*math.sin(a-.5)),(xx,yy),(xx-L*math.cos(a+.5),yy-L*math.sin(a+.5))],c,sw)

def fig4():
    f=Figure(700)
    f.title(0,27,'1','共同的发展方向，落实为不同层次的问题','blue',23)
    tops=[('SDGs · 17 个目标','希望改善什么','教育、健康、机会与可持续发展','blue'),
          ('数字公共品（DPG）标准','资源是否具备基本条件','开放、可理解、可接续与不伤害','teal'),
          ('AI 数字公共品研究 · 2026','实施还需要什么','本地能力、责任、算力与维护','violet')]
    for i,(head,q,s,c) in enumerate(tops):
        x=i*342;f.rect(x,54,315,5,c);f.text(x,88,head,19,c,True);f.text(x,122,q,24,'ink',True);f.text(x,154,s,17,'muted')
    f.line(0,176,1000,176)
    f.title(0,211,'2','开放资源成为公共能力，需要同时检验四类条件','teal',23)
    boxes=[(0,238,'可获得','代码、模型、数据能取得','版本、许可与文档说得清','blue','pale_blue'),
           (0,367,'可复用','算力与运行成本可承担','语言、任务与环境可适配','teal','pale_teal'),
           (690,238,'可维护','有人负责更新与故障处置','资金、交接与响应可持续','violet','pale_violet'),
           (690,367,'有成效','服务解决真实的使用问题','覆盖、质量与风险可验证','orange','pale_gold')]
    # Dashed undirected connectors express conditions, not measured causal effects.
    for x,y,head,l1,l2,c,pale in boxes:
        sx=x+310 if x==0 else x
        f.line(sx,y+53,382 if x==0 else 618,347,c,2,'5 5')
        f.rect(x,y,310,106,pale);f.rect(x,y,4,106,c)
        f.text(x+17,y+31,head,24,c,True);f.text(x+17,y+63,l1,18,'ink');f.text(x+17,y+88,l2,18,'ink')
    f.circle(500,349,92,'pale_blue');f.text(500,333,'可持续',29,'blue',True,'middle');f.text(500,373,'公共能力',29,'blue',True,'middle')
    f.text(500,496,'虚线表示需共同检验的条件关系，不表示已经证实的因果效应。',17,'muted',anchor='middle')
    f.line(0,515,1000,515)
    f.title(0,548,'3','DPG 的九项基本要求，为资源核对提供参照','violet',23)
    groups=[['1  与 SDGs 相关','2  开放许可','3  权属明确'],['4  平台独立性','5  提供文档','6  数据提取机制'],['7  隐私与适用法律','8  标准与最佳实践','9  不伤害：安全、内容与反骚扰']]
    for i,ls in enumerate(groups):
        for j,l in enumerate(ls):f.text(i*342,585+j*31,l,18,'ink')
    f.text(0,689,'DPG 认可针对核心方案设计；地方部署效果仍需另外验证。以上为中文概述。',17,'muted')
    f.save('figure-1-4')

PILLARS=[
 ('X1','人才规模与多样性','参与机会','blue','pale_blue', [('D01','规模与密度'),('D02','生态多样性')],['谁在参与、人才分布在哪里？','新人和不同机构能否进入？']),
 ('X2','技术产出与开放供给','可用资源','teal','pale_teal',[('D03','代码产出'),('D04','模型开放供给'),('D05','数据开放供给')],['提供了什么可接续的材料？','供给是否来自多种主体？']),
 ('X3','全球连接与网络效应','接续关系','orange','pale_gold',[('D06','代码影响力'),('D07','模型影响力'),('D08','数据集影响力')],['成果与哪些协作网络相连？','谁在采用、派生或继续改进？']),
 ('X4','开源善治与公共价值','持续能力','violet','pale_violet',[('D09','治理成熟度'),('D10','公共福祉')],['维护、规则与责任由谁承担？','公共使用具备什么条件？']),
]

def fig5():
    f=Figure(700)
    f.text(0,27,'四个支柱',22,'muted',True);f.text(350,27,'十个观察方向',22,'muted',True);f.text(710,27,'连接到可回答的问题',22,'muted',True)
    for i,(code,name,tag,c,pale,dirs,qs) in enumerate(PILLARS):
        y=53+i*136;f.rect(0,y,1000,120,pale);f.rect(0,y,6,120,c)
        f.text(22,y+30,code,24,c,True);f.text(22,y+64,name,23,'ink',True);f.text(22,y+96,tag,18,c)
        f.line(316,y+16,316,y+105,'line')
        # Fixed numbering and aligned direction rows make cross-page lookup possible.
        for j,(d,t) in enumerate(dirs):
            yy=y+(36 if len(dirs)==2 else 26)+j*34
            f.text(344,yy,d,18,c,True);f.text(400,yy,t,22,'ink',True)
        f.line(676,y+16,676,y+105,'line')
        for j,q in enumerate(qs):f.wrap(704,y+41+j*43,q,280,18,'ink',leading=24)
    f.line(0,612,1000,612)
    f.text(0,650,'贯穿五段主线',20,'ink',True)
    chain=[('参与','blue'),('供给','teal'),('复用','orange'),('治理','violet'),('公共价值','blue')]
    for j,(name,c) in enumerate(chain):
        x=226+j*163;f.text(x,650,name,23,c,True)
        if j<4:arrow(f,x+99,642,x+137,642,'soft',1.8)
    f.text(0,690,'OSDGs 是本报告的研究框架；支柱相互支撑，D01—D10 用于定位内容，不代表权重。',17.5,'muted')
    f.save('figure-1-5')

PAGES=[
 dict(title='1.2　开源发展目标：从开放资源到公共能力',subtitle='目标确定方向，使用条件与实际结果检验开放的价值',
 intro='开放供给为知识共享与技术接续创造机会。本报告关注公共能力：机构与社区能否持续使用、适配并维护资源，以回应真实需求。联合国可持续发展目标（SDGs）确定共同方向，资源标准和实施证据支持具体判断。',figure='figure-1-4',
 caption='图 1-4　从开放资源到公共能力的条件关系。来源：联合国 SDGs［S6］、数字公共品联盟（DPGA）标准［S7］、联合国大学（UNU）等《AI Systems as Digital Public Goods》（2026，第14、43—46、50—52页）［S8］；条件图为本报告设计。DPG 标准概述：CC BY-SA 4.0。',
 analyses=[
 ('1　发展目标，转成具体的使用问题','教育、健康与机会平等，需要落实到具体人群和场景。报告因此同时观察资源供给和使用门槛：地方机构能否取得材料、适配语言与任务，并持续提供服务。规模增长提供线索，实施结果仍需核验。'),
 ('2　维护与本地能力，是转化的关键条件','2026 年 6 月发布的 UNU 等研究将算力、本地语言、评价能力与持续维护并列讨论。本报告据此把成本、适配、维护和结果放在同一关系图中，作为案例分析问题，而非已经成立的因果结论。'),
 ('3　资源认可与公共成效，分别留下证据','DPGA 标准考察核心方案的设计条件，不对地方实施效果作出评价。进入公共服务后，采购与实施机构仍需记录运行成本、受益群体、服务质量和问题处置；维护组织需说明版本与交接安排。这样才能判断，开放资源是否沉淀为当地可以持续使用的能力。')],sources=['S6','S7','S8']),
 dict(title='OSDGs：四个支柱共同支撑公共价值',subtitle='1.2 / 发展目标框架　｜　从参与和供给，追踪连接与持续能力',
 intro='开源发展目标（Open Source Development Goals，OSDGs）是本报告组织研究问题的框架。四个支柱、十个方向将人才、技术资源、协作连接与治理条件放在一起，帮助判断生态怎样形成和持续发展。',figure='figure-1-5',
 caption='图 1-5　OSDGs 四支柱与十个观察方向。来源：本报告研究框架［S9］，结合联合国可持续发展目标提出观察问题。OSDGs 不属于联合国官方认证体系；图中关系为分析设计，不构成统一加权评分。',
 analyses=[
 ('1　参与与供给，说明生态的基础','X1 关注参与者的规模、分布与多样性，X2 关注代码、模型和数据的开放供给。两者结合，才能区分人才基础扩张与资源产出变化；参与账号增长，也可能伴随供给主体继续集中。'),
 ('2　连接关系，说明成果如何继续生长','X3 将协作影响、模型派生和数据复用纳入观察。同样的发布数量，可能形成不同的接续网络。中国及全球南方的作用，也需要沿具体资源、伙伴与使用关系分析，兼顾供给者和采用者。'),
 ('3　治理与公共福祉，把研究引向可持续使用','X4 检查责任、维护安排与公共使用条件，并通过实施资料补充平台数据。四个支柱需交叉阅读：资源可以来自跨境协作，服务能力则需要当地人才和机构承接。下一节将这些问题转成可解释的观察对象与候选指标，分别记录规模、结构、连接和使用条件。')],sources=['S6','S9']),
]

def render():
    fig4();fig5();return PAGES
