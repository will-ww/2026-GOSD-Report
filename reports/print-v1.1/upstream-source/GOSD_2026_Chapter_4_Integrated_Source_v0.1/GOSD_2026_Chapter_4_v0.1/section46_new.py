from common import *
from section41 import fitted,rounded
P=R/'inputs/46';ROWS=json.loads((D/'research/rankings.json').read_text())['46'];BY={p['repo']:p for p in ROWS};TOTAL=sum(p['score'] for p in ROWS);CORE=BY['pytorch/pytorch']['score']
CAT={'Training':'训练框架','Compilers & Runtimes':'编译与运行','Distributed Training':'分布式训练','Optimization':'计算优化','Computer Vision':'计算机视觉','Audio':'音频','Reinforcement Learning':'强化学习','Domain Applications':'领域应用','Data':'数据处理','Privacy':'隐私保护','MLOps':'作业与运行管理','Core Infrastructure':'工程基础设施','Documentation & Community':'文档与社区','pending':'待核'}
GROUPS=[('模型与任务',['Computer Vision','Audio','Reinforcement Learning','Domain Applications','Data','Privacy'],'teal'),('训练与执行',['Training','Distributed Training','Compilers & Runtimes','Optimization'],'blue'),('工程与协作',['MLOps','Core Infrastructure','Documentation & Community'],'violet')]
LOGOS={x['repo']:P/'assets/projects'/Path(x['logo']).name for x in json.loads((P/'assets/projects/mapping.json').read_text())}
ALIASES={'pytorch/pytorch':'PyTorch','pytorch/executorch':'ExecuTorch','pytorch/torchtitan':'TorchTitan','pytorch/ao':'torchao','pytorch/vision':'TorchVision','pytorch/audio':'TorchAudio','pytorch/rl':'TorchRL','pytorch/TensorRT':'Torch-TensorRT','meta-pytorch/compile-graph-break-site':'compile-graph-break','pytorch-fdn/accelerator-integration-wg':'accelerator-integration WG','pytorch/pytorch-integration-testing':'integration-testing','pytorch-fdn/wg-ospo-and-academic-outreach':'OSPO & academic outreach WG','meta-pytorch/meta-pytorch.github.io':'meta-pytorch website'}
def lab(p):return ALIASES.get(p['repo'],p['name'])
def logo(f,p,x,y,s=20):
 path=LOGOS.get(p['repo']);sy=P/'assets/symbols'/path.name if path else None
 if sy and sy.exists():path=sy
 if not path or not path.exists():path=R/'assets/owners'/(p['owner']+'.png')
 img(f,path,x,y,s,s)
def title(f,x,y,n,t,fs=21,col='teal'):f.title(x,y,str(n),t,col,fs)
def atlas():
 f=Figure(900);logo(f,BY['pytorch/pytorch'],0,0,35);f.text(47,26,'PyTorch Ecosystem Landscape',27,'teal',True);f.text(1000,26,'82 项 / 13 类 · 另 1 项待核',18,'muted',anchor='end')
 for j,(head,cats,co) in enumerate(GROUPS):
  x=j*342;rounded(f,x+1,54,314,807,co);f.rect(x+2,55,312,44,'pale');title(f,x+12,84,j+1,head,21,co)
  y=124;step=18.5 if j==1 else 19 if j==2 else 22
  for cat in cats:
   a=[p for p in ROWS if p['category']==cat];f.text(x+12,y,CAT[cat],18.3,co,True);f.text(x+300,y,str(len(a))+' 项',15,'muted',anchor='end');y+=25
   for p in sorted(a,key=lambda p:-p['score']):
    logo(f,p,x+12,y-14.5,17);fitted(f,x+37,y,lab(p),266,16.5,bold=p['repo']=='pytorch/pytorch',minfs=13.5);y+=step
   y+=10
  if j==0:
   f.line(x+12,704,x+302,704);f.text(x+12,733,'一个框架，多种任务入口',19,'teal',True)
   f.wrap(x+12,763,'任务库、数据组件与隐私工具，把通用计算能力连接到具体应用。',285,17.6,'muted',leading=26)
 f.text(0,893,'待核：PytorchForge/client。图标优先为项目标识，其余为仓库所属组织；不代表基金会托管。',16.2,'muted')
 f.save('4-6-1-atlas')
def rankings():
 f=Figure(900);title(f,0,26,1,'项目影响力前 20 位');f.text(0,55,'主要仓库 / 项目',15,'muted');f.text(411,55,'OpenRank',15,'muted',anchor='end');f.text(483,55,'月数',15,'muted',anchor='end')
 for i,p in enumerate(sorted(ROWS,key=lambda p:-p['score'])[:20]):
  y=83+i*23
  if i%2==0:f.rect(0,y-17,483,23,'pale')
  f.text(0,y,f'{i+1:02}',14,'muted');logo(f,p,27,y-16,18);fitted(f,52,y,lab(p),265,17,bold=i<3,minfs=15)
  f.text(411,y,fmt(p['score'],1),17,'teal',i<3,'end');f.text(483,y,str(p['months']),15,'muted',anchor='end')
 f.line(500,0,500,547);title(f,520,26,2,'13 类功能：聚合类内协作影响');f.text(520,55,'类别',15,'muted');f.text(829,55,'OpenRank',15,'muted',anchor='end');f.text(1000,55,'全样本份额',15,'muted',anchor='end')
 cs=[]
 for cat in CAT:
  if cat=='pending':continue
  ps=[p for p in ROWS if p['category']==cat];cs.append((cat,sum(p['score'] for p in ps),len(ps)))
 for i,(cat,v,n) in enumerate(sorted(cs,key=lambda x:-x[1])):
  y=85+i*31.8
  if i%2==0:f.rect(520,y-20,480,31.8,'pale')
  f.text(520,y,f'{i+1:02}',14,'muted');f.text(549,y,CAT[cat],17);f.text(829,y,fmt(v,1),17,'blue',False,'end');f.text(1000,y,f'{v/TOTAL*100:.2f}%',17,'blue',True,'end')
 f.text(520,521,'类别按主功能去重；待核 1 项单列，不推定功能。',16,'muted')
 f.line(0,550,1000,550);title(f,0,586,3,'同一中心，三类互补工作');title(f,520,586,4,'去掉核心，再看外围结构')
 for i,(name,cats,co) in enumerate(GROUPS):
  ps=[p for p in ROWS if p['category'] in cats];v=sum(p['score'] for p in ps);y=635+i*69
  f.text(0,y,name,20,co,True);f.text(483,y,f'{len(ps)} 项 / {v/TOTAL*100:.1f}%',20,co,True,'end');f.rect(0,y+14,483*v/TOTAL,15,co)
 f.text(0,867,'主统计期：2025.07—2026.06；83 项均有记录，17 项满 12 月。',15.2,'muted')
 other=TOTAL-CORE;engine=sum(p['score'] for p in ROWS if p['category'] in ['Compilers & Runtimes','Optimization']);f.text(520,637,'PyTorch 核心',20,'teal',True);f.text(1000,637,f'{CORE/TOTAL*100:.1f}%',31,'teal',True,'end')
 f.rect(520,655,480,23,'pale');f.rect(520,655,480*CORE/TOTAL,23,'teal')
 f.text(520,717,'其余 82 项合计',20);f.text(1000,717,fmt(other,1),24,'blue',True,'end')
 f.text(520,765,'其中：编译运行与计算优化',20,'blue',True);f.text(1000,803,f'{engine/other*100:.1f}%',31,'blue',True,'end');f.text(520,803,'20 项 / 分母为其余 82 项',17,'muted')
 f.text(520,867,'核心外的设备执行、性能适配和优化仍占重要位置。',16,'muted')
 f.save('4-6-2-rankings')
def organization():
 f=Figure(900);title(f,0,26,1,'仓库所属组织：观察维护边界');f.text(0,56,'固定样本仓库数；不是贡献人数或法人排名',16,'muted')
 owners=Counter(p['owner'] for p in ROWS)
 for i,(name,n) in enumerate(owners.most_common()):
  y=90+i*32;img(f,R/'assets/owners'/(name+'.png'),0,y-17,20,20);fitted(f,30,y,name,227,17.3,minfs=15.5);f.rect(266,y-12,145*n/32,12,'teal');f.text(482,y,str(n),18,'teal',True,'end')
 f.line(500,0,500,416);title(f,520,26,2,'三个项目：协作变化并不同步');f.text(520,56,'两期均有连续 12 个月记录 · OpenRank 合计',15.5,'muted')
 for i,repo in enumerate(['pytorch/pytorch','pytorch/executorch','pytorch/torchtitan']):
  p=BY[repo];y=94+i*91;logo(f,p,520,y-23,27);f.text(557,y,lab(p),20,'ink',True);gr=(p['score']/p['old_score']-1)*100
  f.text(1000,y,f'{gr:+.1f}%',25,'teal' if gr>=0 else 'china',True,'end');f.text(520,y+31,fmt(p['old_score'],1)+' → '+fmt(p['score'],1),19,'muted')
  scale=max(p['old_score'],p['score']);f.rect(520,y+45,375*p['old_score']/scale,8,'soft');f.rect(520,y+57,375*p['score']/scale,8,'teal')
 f.text(520,389,'2024.07—2025.06 → 2025.07—2026.06',16,'muted');f.text(520,415,'不同增减不等同技术兴衰，也不说明相互替代。',16,'muted')
 f.line(0,437,1000,437);title(f,0,475,3,'组织支持、技术交流与项目决策');title(f,520,475,4,'公共设施：把资源落实到维护')
 roles=[('基金会理事会','监督基金会活动与组织支持'),('技术咨询委员会（TAC）','技术沟通与议题交流；公开月会'),('项目维护者','代码评审、模块设计与技术决策')]
 for i,(a,b) in enumerate(roles):
  y=504+i*75;f.rect(0,y,482,65,'pale');f.text(14,y+26,a,19,'teal',True);f.text(14,y+52,b,17)
 f.text(0,766,'中国参与入口',20,'china',True);f.wrap(0,797,'阿里云、华为、寒武纪代表列于 TAC 名单；可继续跟踪议题、评审与兼容适配。',482,18,leading=27);f.text(0,878,'成员身份不等于技术控制权；文件为 2026.11 期后观察。',15.7,'muted')
 blocks=[('云额度或捐赠','官方计划列明 AWS 的额度供给'),('持续集成与公共基础设施','持续集成：对软件改动自动构建、测试'),('明确技术支持与服务责任','计划要求技术联系人与服务水平安排')]
 for i,(a,b) in enumerate(blocks):
  y=504+i*75;f.rect(520,y,480,65,'pale');f.text(534,y+26,a,19,'blue',True);f.text(534,y+52,b,16.7)
 f.text(520,766,'本报告建议的验收维度',20,'teal',True)
 f.wrap(520,799,'成本：资源与运行开销　　本地化：目标语言与场景\n维护：版本、责任人与周期　结果：任务效果与失败处理',480,17.2,leading=27)
 f.text(520,878,'已观察到支持机制；额度使用与维护成效尚需结果证据。',15.7,'muted')
 f.save('4-6-3-organization')
def contents():
 return [
 page('4.6','4.6 PyTorch 生态：从框架到体系','PyTorch 是训练和运行 AI 模型的开源框架。以组织型生态为切口，观察任务库、执行工具和协作设施如何围绕共同框架形成专业分工。','4-6-1-atlas','图 4-11　PyTorch 生态完整观察样本。来源：2026 版固定清单、PyTorch 上游全景和官方项目标识。82 项按主要功能分为 13 类，另 1 项待核；它是技术观察样本，不是基金会正式托管名单或全部生态目录。',[
 ('① 任务库拓展共享框架的用途','视觉、音频、强化学习和领域应用等共 16 项。数据组件和隐私工具也处于任务链条中，说明可复用能力不只表现为一个核心框架。'),
 ('② 训练与执行需要专业工具协同','33 项涉及训练、分布式协作、编译运行和优化。从算法表达走到不同设备运行，需要连续的工程适配，不能以核心仓库替代全栈观察。'),
 ('③ 工程与社区构成长期交付条件','已归类的工程协作仓库有 33 项，其中测试基础设施与文档社区合计 30 项。它们让更新可检查、知识可传递、外部参与者可接续。'),
 ('④ 生态关联与组织责任分别识别','图中保留不同仓库组织的资源。技术关联、实际维护和基金会托管不是同一关系；组织型案例的价值在于把资源对象连接到责任。')],[],['I02','I03','I06','I09']),
 page('4.6','4.6 项目与功能类别的影响力排名','核心框架十分突出，外围仍有可辨认的专业分工。把项目、类别和工作组逐层展开，再剔除核心观察其余资源，可看清协作集中在哪里。','4-6-2-rankings','图 4-12　PyTorch 样本项目、功能类别与外围结构。来源：OpenDigger，2025.07—2026.06 已记录月度 OpenRank 合计，2026.11.10 提取。83 项均有记录，17 项满 12 月；缺月未补零。类别去重，待核项保留在全样本分母。',[
 ('① 核心与执行工具共同居于前列',f"PyTorch 占样本分值的 {CORE/TOTAL*100:.1f}%，其后是 ExecuTorch、TorchTitan 与 torchao。分值衡量协作网络影响，不能替代速度、精度或部署效果。"),
 ('② 分类排名揭示专业协作位置','训练框架之外，编译运行、计算优化与分布式训练形成明显支点。这为识别共同工具和维护对象提供依据，不直接证明资金投入是否充分。'),
 ('③ 仓库数与协作权重并不对称','训练执行与工程协作各有 33 项已归类仓库，前者分值明显更高。文档与测试的公共价值不能由分值高低或仓库大小完全衡量。'),
 ('④ 外围体系不是核心的简单附属','移除核心后，编译运行与优化的 20 项仍占其余分值的 51.3%。支持策略需要覆盖设备适配与共同维护，避免只围绕单一品牌配置资源。')],[],['I02','I03','I05']),
 page('4.6','4.6 共同维护如何形成公共能力','不同项目的协作信号、仓库组织和治理职责共同构成体系观察。资源投入需要落实到可维护的设施，再以成本、本地化和使用结果检验公共价值。','4-6-3-organization','图 4-13　组织边界、年度变化与持续维护机制。①据固定样本；②据 OpenDigger 两个完整报告年度；③④据 PyTorch 基金会、治理文件、TAC 和云资源计划，查阅于 2026.11.10（期后）。末组验收维度为本报告建议。',[
 ('① 仓库组织不等于贡献归属','meta-pytorch 和 pytorch 名下分别有 32、30 项。这个结构帮助定位维护入口，但账号归属不等于企业全部贡献，更不能代替贡献者国别统计。'),
 ('② 同一体系内部可以不同步演进','TorchTitan 的年度分值增长 64.6%，PyTorch 与 ExecuTorch 分别下降 32.1%、17.1%。三个完整序列支持分层观察，不足以推断技术替代或总体能力衰退。'),
 ('③ 中国参与需落实为可追踪工作','TAC 名单提供具体交流入口，项目维护者则负责技术评审。后续应跟踪议题、兼容测试和长期维护记录，以实际工作理解跨境协作。'),
 ('④ 以公共设施与可用结果组织支持','云资源计划连接资金、测试设施和技术支持。对基金会及资助方，建议将这些任务与本地语言、成本和交付结果一起验收，形成可持续公共能力。')],[],['I03','I06','I08','I09'])]
def render46():
 atlas();rankings();organization();ps=contents();save_pages('46',ps);return ps
if __name__=='__main__':
 render46();(R/'review/46-figures.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2));print(json.dumps([q for q in QA if q['out_of_bounds'] or q['overlaps']],ensure_ascii=False))
