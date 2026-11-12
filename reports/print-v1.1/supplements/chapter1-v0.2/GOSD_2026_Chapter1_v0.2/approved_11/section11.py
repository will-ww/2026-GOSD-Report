from build import *

C.update(violet='#68509B',orange='#AD6D25',pale_blue='#EEF4FA',pale_teal='#EDF6F5',pale_violet='#F3F0F8')

SOURCES=[
 {'id':'S1','name':'GitHub Octoverse 2026','date':'2026-10-28；更新2026-11-06','url':'https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/','locator':'Developers are reshaping their workflow','scope':'PR起草：2026年3月与9月；Copilot用户：外部年度观察；9月与报告发布时的观察为期后信息。','checked':'2026-11-10'},
 {'id':'S2','name':'GitHub Copilot Agents application card','date':'读取2026-11-10','url':'https://docs.github.com/en/copilot/responsible-use/agents','locator':'Limitations / human review and testing','scope':'当前产品文档；仅用于解释协作机制及审查责任，不回填历史统计。','checked':'2026-11-10'},
 {'id':'S3','name':'DeepSeek Open Infra官方索引','date':'2025年2月开源周','url':'https://github.com/deepseek-ai/open-infra-index#202502-open-source-week','locator':'Day 1–5；FlashMLA、DeepEP、DeepGEMM、DualPipe、3FS','scope':'主统计期以前的历史组件职责，不混用当前分支的硬件支持状态。','checked':'2026-11-10'},
 {'id':'S4','name':'NVIDIA: Build Custom Reasoning Models with Advanced, Open Post-Training Datasets','date':'2025-05-14','url':'https://developer.nvidia.com/blog/build-custom-reasoning-models-with-advanced-open-post-training-datasets/','locator':'Table 2；data curation；model release list','scope':'历史案例；图中3个生成模型的原表样本记录，不作全表或国别占比推导。','checked':'2026-11-10'},
 {'id':'S5','name':'Llama-Nemotron-Post-Training-Dataset 数据集卡','date':'固定历史版本04d0854','url':'https://huggingface.co/datasets/nvidia/Llama-Nemotron-Post-Training-Dataset/blob/04d085443485c2b8e14ad5f518005c769deb4904/README.md','locator':'数据来源模型、样本数与后训练用途','scope':'历史数据集卡，用于交叉核对选定模型条目。','checked':'2026-11-10'},
]

def arrow(f,x,y,xx,yy,c='muted',sw=2):
    f.line(x,y,xx,yy,c,sw)
    a=math.atan2(yy-y,xx-x);L=9
    f.path([(xx-L*math.cos(a-.5),yy-L*math.sin(a-.5)),(xx,yy),(xx-L*math.cos(a+.5),yy-L*math.sin(a+.5))],c,sw)

def chip(f,x,y,c):
    f.rect(x-31,y-31,62,62,c,.10)
    f.path([(x-31,y-31),(x+31,y-31),(x+31,y+31),(x-31,y+31),(x-31,y-31)],c,2.5)
    for d in [-18,0,18]:
        f.line(x+d,y-43,x+d,y-31,c,2.5);f.line(x+d,y+31,x+d,y+43,c,2.5)
        f.line(x-43,y+d,x-31,y+d,c,2.5);f.line(x+31,y+d,x+43,y+d,c,2.5)
    f.text(x,y+8,'AI',24,c,True,'middle')

def network(f,x,y,c):
    for dx,dy in [(-30,-25),(30,-25),(-30,25),(30,25)]:
        f.line(x,y,x+dx,y+dy,c,2);f.rect(x+dx-10,y+dy-10,20,20,c,.16)
        f.path([(x+dx-10,y+dy-10),(x+dx+10,y+dy-10),(x+dx+10,y+dy+10),(x+dx-10,y+dy+10),(x+dx-10,y+dy-10)],c,2)
    f.circle(x,y,12,c)

def storage(f,x,y,c):
    for j in [0,1,2]:
        yy=y-35+j*25
        f.rect(x-40,yy,80,20,c,.10)
        f.path([(x-40,yy),(x+40,yy),(x+40,yy+20),(x-40,yy+20),(x-40,yy)],c,2)
        f.circle(x+27,yy+10,3,c)

def fig1():
    f=Figure(700)
    f.title(0,27,'1','更多变更由智能体起草','blue',23)
    f.text(0,61,'以智能体草稿启动的 PR，占 GitHub PR 的比例',18,'muted')
    f.line(505,5,505,334)
    # Two discrete observations; the second bar ends with an arrow to encode >40%.
    f.text(0,130,'2026.03',20,'ink',True);f.text(0,155,'主统计期内',16,'blue')
    f.text(0,227,'2026.09',20,'ink',True);f.text(0,252,'期后观察',16,'orange')
    x=130;scale=6
    f.rect(x,107,17*scale,31,'blue');f.text(x+17*scale+15,132,'17%',32,'blue',True)
    f.rect(x,204,40*scale,31,'orange',.82);arrow(f,x+40*scale,219,x+40*scale+12,219,'orange',3)
    f.text(495,230,'>40%',32,'orange',True,'end')
    f.line(x,280,430,280)
    for v in [0,25,50]:
        f.line(x+v*scale,280,x+v*scale,286);f.text(x+v*scale,308,f'{v}%',17,'muted',anchor='middle')
    f.text(0,334,'两个时点分列；期后值不计入主统计期。',17,'muted')

    f.title(535,27,'2','从问答走向任务委托','teal',23)
    f.text(535,61,'Copilot 月活用户中，使用智能体功能的比例',18,'muted')
    f.text(535,86,'外部年度观察；2026 报告值属于期后信息',16,'muted')
    bx=595;bottom=286;scale2=2.55
    for v in [0,20,40,60]:
        yy=bottom-v*scale2;f.line(bx,yy,985,yy,'line',1)
        f.text(bx-12,yy+6,f'{v}%',16,'muted',anchor='end')
    for xx,v,col,label in [(655,35,'soft','上年观察值'),(845,55,'teal','2026 报告值')]:
        f.rect(xx-42,bottom-v*scale2,84,v*scale2,col)
        f.text(xx,bottom-v*scale2-12,f'{v}%',32,col,True,'middle')
        f.text(xx,315,label,18,'muted',anchor='middle')
    f.text(535,334,'两图描述不同对象：PR 与 Copilot 用户。',17,'muted')

    f.line(0,354,1000,354)
    f.title(0,389,'3','从生成草稿到可用成果，协作责任仍需接续','blue',23)
    f.text(0,421,'同一任务示意：修复一项用户反馈的问题',18,'muted')
    steps=[
      ('人设定目标','说清要改什么',['说明错误场景','约定验收标准'],'blue','pale_blue'),
      ('智能体执行','起草代码与测试',['读取项目资料','提交修改方案'],'teal','pale_teal'),
      ('维护者验收','确认可以采用',['核对功能与安全','审查后再合并'],'blue','pale_blue'),
      ('社区持续接续','形成可用版本',['维护文档与依赖','接收后续反馈'],'violet','pale_violet')
    ]
    for i,(role,title,lines,c,pale) in enumerate(steps):
        xx=i*255;f.rect(xx,448,235,155,pale);f.rect(xx,448,235,5,c)
        f.text(xx+18,483,role,18,c,True)
        f.text(xx+18,521,title,23,'ink',True)
        for j,l in enumerate(lines):f.text(xx+18,554+j*28,l,19,'muted')
        if i<3:arrow(f,xx+239,525,xx+251,525,'muted',2)
    f.path([(882,611),(882,636),(115,636),(115,611)],'soft',2)
    arrow(f,115,628,115,611,'soft',2)
    f.rect(329,620,344,31,'white');f.text(501,642,'使用反馈进入下一轮改进',20,'teal',True,'middle')
    f.text(0,685,'Agent：按目标调用工具、分步执行任务的智能体。PR：向项目提出的一组修改。',17.5,'muted')
    f.save('figure-1-1')

def component(f,x,y,w,name,role,desc,c,pale):
    f.rect(x,y,w,117,pale);f.rect(x,y,4,117,c)
    f.text(x+16,y+30,name,24,c,True)
    f.text(x+16,y+58,role,17,'muted')
    f.wrap(x+16,y+89,desc,w-29,18,'ink',leading=23)

def fig2():
    f=Figure(700)
    rows=[
     (27,'1','让模型运算更高效','blue','pale_blue','计算',
      [('FlashMLA','推理执行','加快模型逐步生成回答'),('DeepGEMM','训练与推理','提高模型基础计算效率')],
      ['硬件与模型版本','计算精度与软件环境']),
     (242,'2','让多个芯片协同工作','teal','pale_teal','协同',
      [('DeepEP','数据通信','支持多芯片间交换数据'),('DualPipe','训练调度','把计算与通信交错安排')],
      ['芯片间网络条件','并行方式与任务规模'])
    ]
    for y,n,title,c,pale,kind,cs,conditions in rows:
        f.title(0,y,n,title,c,23)
        if n=='1':f.text(1000,y,'2025 年 2 月 · 历史组件职责',16,'muted',anchor='end')
        (chip if n=='1' else network)(f,55,y+90,c)
        f.text(55,y+163,kind,23,c,True,'middle')
        for j,a in enumerate(cs):component(f,135+j*278,y+34,260,*a,c,pale)
        f.line(708,y+38,708,y+157)
        f.text(735,y+65,'复用时关注',20,'ink',True)
        for j,s in enumerate(conditions):f.text(735,y+103+j*31,s,18,'muted')
        f.line(0,y+188,1000,y+188)
    y=457
    f.title(0,y,'3','让数据存取跟上训练与服务','violet',23)
    storage(f,55,y+90,'violet');f.text(55,y+163,'存取',23,'violet',True,'middle')
    component(f,135,y+34,260,'3FS','并行文件系统','支撑大规模数据存取','violet','pale_violet')
    f.text(431,y+68,'贯穿不同工作环节',20,'ink',True)
    for j,s in enumerate(['装载训练数据','保存与恢复训练进度','支持推理中的缓存存取']):
        f.circle(438,y+94+j*27,3.5,'violet');f.text(451,y+101+j*27,s,18,'muted')
    f.line(708,y+38,708,y+157)
    f.text(735,y+65,'复用时关注',20,'ink',True)
    for j,s in enumerate(['数据规模与存储架构','网络条件与运行维护']):f.text(735,y+103+j*31,s,18,'muted')
    f.rect(0,658,1000,42,'pale')
    f.text(500,686,'开放代码 → 复现环境 → 适配测试 → 持续维护',21,'teal',True,'middle')
    f.save('figure-1-2')

MODEL_SAMPLES=[('Qwen2.5-Math-7B-Instruct',19840970,'blue'),('Qwen2.5-Coder-32B-Instruct',8917167,'blue'),('DeepSeek-R1',1212994,'teal')]
def fig3():
    f=Figure(700)
    f.title(0,27,'1','模型输出成为跨组织接续的材料','blue',23)
    f.text(0,59,'历史案例 · NVIDIA 2025 年 5 月说明；箭头表示生成、整理与训练关系',17.5,'muted')
    for i,(name,c,pale) in enumerate([('Qwen 系列','blue','pale_blue'),('DeepSeek-R1','teal','pale_teal'),('Llama / Mixtral 等','muted','pale')]):
        yy=89+i*56;f.rect(0,yy,273,47,pale);f.rect(0,yy,4,47,c);f.text(17,yy+30,name,22,c,True)
    f.path([(285,112),(308,112),(308,225),(285,225)],'soft',1.7)
    arrow(f,308,168,343,168,'soft',2)
    f.text(325,93,'生成',17,'muted',anchor='middle')
    f.rect(357,89,289,159,'pale_teal');f.text(501.5,122,'NVIDIA 整理与筛选',21,'teal',True,'middle')
    f.text(501.5,166,'Llama-Nemotron',24,'ink',True,'middle')
    f.text(501.5,198,'后训练数据集',24,'ink',True,'middle')
    f.text(501.5,230,'把回答与推理过程组织成训练记录',16.5,'muted',anchor='middle')
    arrow(f,660,168,709,168,'soft',2);f.text(684,141,'训练',17,'muted',anchor='middle')
    f.rect(723,89,277,159,'pale_violet');f.text(861.5,122,'Llama-Nemotron 系列',21,'violet',True,'middle')
    for j,s in enumerate(['Nano 8B','Super 49B','Ultra 253B']):f.text(861.5,159+j*31,s,23,'ink',False,'middle')
    f.text(0,275,'复用的是生成的训练记录；这条路径不表示后续模型继承了 DeepSeek 的模型参数。',17,'muted')
    f.line(0,293,1000,293)
    f.title(0,326,'2','三个来源模型，留下可追溯的样本记录','teal',23)
    f.text(1000,360,'样本 / 万条',17,'muted',anchor='end')
    start=389;scale=420/2000
    for i,(name,num,c) in enumerate(MODEL_SAMPLES):
        yy=390+i*49;f.text(0,yy,name,18.5,'ink',name=='DeepSeek-R1')
        f.rect(start,yy-18,num/10000*scale,24,c,.9)
        f.text(1000,yy+2,f'{num/10000:,.1f}',23,c,True,'end')
    f.line(start,518,start+420,518)
    for v in [0,1000,2000]:
        xx=start+v*scale;f.line(xx,518,xx,525);f.text(xx,545,f'{v:,}',16,'muted',anchor='middle')
    f.text(0,545,'选取源表条目，不代表完整构成。',16.5,'muted')
    f.line(0,562,1000,562)
    f.title(0,594,'3','接续不止于模型发布，还包括材料与工具','violet',23)
    assets=[('训练样本','Hugging Face 数据集','blue','pale_blue'),('生成与整理工具','NeMo-Skills / NeMo-Curator','teal','pale_teal'),('后续模型','Nano / Super / Ultra','violet','pale_violet')]
    for i,(title,sub,c,pale) in enumerate(assets):
        xx=i*343;f.rect(xx,620,314,77,pale);f.rect(xx,620,314,4,c)
        f.text(xx+17,653,title,22,c,True);f.text(xx+17,680,sub,17,'muted')
    f.save('figure-1-3')

PAGES=[
 dict(title='1.1　人工智能时代的开源协作：双向重塑',subtitle='AI 改变创造与协作的节奏，开源为 AI 提供可接续的基础',
 intro='AI 正将部分编程活动从逐行编写推进到任务委托；开源则通过公开代码、工具与训练材料，让更多团队参与改进。理解这种双向关系，需要同时看工作如何完成，以及成果如何被继续使用。',figure='figure-1-1',
 caption='图 1-1　AI 进入协作流程：工作入口、任务委托与责任分工。来源：GitHub Octoverse 2026［S1］及官方产品说明［S2］。本报告主统计期为 2025.07.01—2026.06.30；右图沿用外部年度口径。流程为机制示意，不能据此推断质量或生产率的因果变化。',
 analyses=[
 ('1　工作入口变了，观察范围也要说清','以智能体草稿发起的 PR 比例由 3 月的 17% 增至 9 月的超过 40%。前者位于主统计期，后者是期后信号。这反映修改方案的发起方式，不能直接代表开源代码总量或全部开发者。'),
 ('2　从辅助回答，走向多步骤执行','在 Copilot 月活用户中，使用智能体功能的比例升至 55%。它提示工具角色正在扩展：用户提出目标，工具组织步骤并执行。用户使用比例与 PR 起草比例分母不同，也不等同于效率提升。'),
 ('3　从生成到使用，审查与维护承接后续责任','智能体可以起草、测试并提出修改，维护者仍需核对目标、功能与安全，再决定是否采用。社区随后承担发布、文档、依赖维护与反馈处理。因而，评价 AI 时代的开源协作，应继续追踪修改是否被采纳、关系是否持续、成果是否可用；生成数量只是这条链上的一个信号。')],sources=['S1','S2'],claim_ids=['I02','I03']),
 dict(title='开放供给，从模型延伸到基础工具',subtitle='1.1 / 开源支撑 AI　｜　同一系统中的三类工程能力',
 intro='模型要进入实际运行环境，还需要高效计算、芯片协同与数据存取。DeepSeek 在 2025 年 2 月公开的一组基础组件，提供了具体例子：开放的不只是模型文件，还包括支撑训练与服务的工程方法。',figure='figure-1-2',
 caption='图 1-2　从模型能力到系统运行：DeepSeek 五个开放基础组件的工程职责。来源：DeepSeek 官方基础设施索引“2025 年 2 月开源周”［S3］。这是主统计期之前的历史案例；按功能归类，不表示完整训练系统、全部依赖关系或性能比较。',
 analyses=[
 ('1　计算优化，也是一种可复用供给','FlashMLA 与 DeepGEMM 把部分底层优化方法做成可检视的代码。后续团队可以理解、测试和改进实现。能否用于自己的系统，需要核对硬件、模型与软件版本，不能仅凭公开代码判断部署成本。'),
 ('2　多芯片能力，依赖协同而非简单叠加','DeepEP 关注芯片间的数据交换，DualPipe 关注训练中计算与通信的安排。二者对应不同瓶颈。开放这些实现，有助于其他团队沿既有方法开展适配；实际收益仍取决于网络、任务和工程条件。'),
 ('3　可持续服务，需要看见数据与维护环节','3FS 支撑数据装载、训练进度保存与恢复，以及推理中的缓存存取。它提醒我们：模型表现之外，系统能否持续运行还取决于数据和基础设施。评估开放供给，需要进一步观察采用者能否复现环境、完成适配并持续维护。这也是第四章从技术体系而非单个项目理解生态的原因。')],sources=['S3'],claim_ids=['I02','I05']),
 dict(title='中国开放模型，进入全球再创造',subtitle='1.1 / 跨组织复用　｜　从生成回答到新的训练材料',
 intro='模型的输出可以被整理为另一模型的训练材料。NVIDIA 于 2025 年 5 月公开说明：Qwen、DeepSeek-R1 等模型生成的记录，经整理进入 Llama-Nemotron 后训练数据集，并用于后续模型训练。',figure='figure-1-3',
 caption='图 1-3　开放模型输出的再利用：生成来源、样本记录与后续成果。来源：NVIDIA 技术说明（2025-05-14，表 2）［S4］及历史数据集卡［S5］。样本数选取三个生成模型的原表条目；这是历史复用案例，不作国别、市场或性能贡献份额推导。',
 analyses=[
 ('1　中国贡献，可以沿具体资源追踪','这个案例把中国模型与海外团队的后续研发联系起来。Qwen、DeepSeek-R1 与其他来源共同提供生成能力，NVIDIA 继续整理材料并训练模型。跨组织接续由可查的资源和使用关系体现。'),
 ('2　样本规模，说明供给而非效果分摊','图中的一条样本是一条训练记录；同一问题可以产生不同回答。约 121.3 万条 R1 样本说明其输出进入了后续训练过程。数量不能直接换算为模型能力提升，也不能作为整个生态的贡献比例。'),
 ('3　开放材料越完整，越有利于下一次接续','公开样本、生成与整理工具及后续模型，为其他团队复现方法和继续改进提供了条件。报告由此沿“参与、供给、复用”追踪资源流动，并继续检验治理与公共价值。要让开放成果成为可持续公共能力，还需解决接入成本、本地适配与长期维护；这构成下一节讨论发展目标的起点。')],sources=['S4','S5'],claim_ids=['I02','I03','I04'])
]

def render():
    fig1();fig2();fig3();return PAGES
