from common import *
from section41 import fitted,rounded
RANK=json.loads((D/'research/rankings.json').read_text());PUBLIC=json.loads((D/'research/public-countries.json').read_text());P=R/'inputs/43-45';CONTENT=json.loads((P/'content.json').read_text())
def title(f,x,y,n,t,fs=21,col='teal'):f.title(x,y,str(n),t,col,fs)
def atlas(f,sec):
 kind={'43':'cloud','44':'database','45':'riscv'}[sec];groups=CONTENT[kind]['groups'];title(f,0,25,1,'功能全景 · 代表项目与技术分工');f.text(1000,25,'固定清单选列 16 项',17,'muted',anchor='end')
 if sec!='44':
  for i,g in enumerate(groups):
   x=i*255;co=['teal','blue','violet','teal'][i];rounded(f,x+1,51,234,292,co);f.rect(x+2,52,232,42,'pale');f.text(x+13,80,g['name'],19,co,True)
   for j,r in enumerate(g['entries']):
    y=107+j*58;img(f,P/r['local_logo'],x+12,y,25,25);fitted(f,x+45,y+20,r['label'],178,18.2,bold=True,minfs=13.2)
    role=r['role'].replace('编译工具链*','编译工具链').replace('K8s 发行版','容器平台发行版').replace('WASM 运行时','WebAssembly 运行时')+(' · 机构/上游' if r['logo_kind']!='project' else '');fitted(f,x+12,y+45,role,211,15.1,c='muted',minfs=13.2)
 else:
  for i,g in enumerate(groups):
   x=i*342;co=['blue','teal','violet'][i];rounded(f,x+1,51,314,292,co);f.rect(x+2,52,312,42,'pale');f.text(x+13,80,g['name'],19,co,True)
   for j,r in enumerate(g['entries']):
    xx=x+12+(j%2)*151;y=107+(j//2)*57
    img(f,P/r['local_logo'],xx,y,22,22);fitted(f,xx+28,y+18,r['label'],117,16.5,bold=True,minfs=13)
    fitted(f,xx,y+42,r['role'],142,14.4,c='muted',minfs=13)
   if i==2:
    f.wrap(x+13,196,'时序描述随时间变化的记录；空间处理位置及几何关系。',287,18,'muted',leading=27)
    f.wrap(x+13,272,'标签描述观察维度，不能替代具体版本的能力测试。',287,16.5,'violet',leading=24)
 f.text(0,371,'按功能选列；区块面积不表示影响力。主展示分类只计一次，跨节重复项目不相加。',16.5,'muted')
def ranking(f,sec):
 ps=sorted(RANK[sec],key=lambda p:-p['score']);title(f,0,417,2,'样本项目前 15 位');f.text(0,446,'主要仓库',15,'muted');f.text(407,446,'OpenRank',15,'muted',anchor='end');f.text(483,446,'月数',15,'muted',anchor='end')
 for i,p in enumerate(ps[:15]):
  y=473+i*25;co='teal'
  if i%2==0:f.rect(0,y-18,483,25,'pale')
  f.text(0,y,f'{i+1:02}',14,'muted');nm=p['repo'] if sec=='45' else p['name']
  fitted(f,28,y,nm,275,17,bold=i<3,minfs=14.3)
  f.text(407,y,fmt(p['score'],1),17,co,i<3,'end');f.text(483,y,str(p['months']),16,'muted',anchor='end')
 full=sum(p['months']==12 for p in ps);f.text(0,872,f'主期已记录月累计 · {full}/{len(ps)} 项有 12 个月记录',16,'muted');f.text(0,895,'缺月未补零；分值衡量协作网络影响，不等同技术性能。',15.9,'muted')
def group_stats(f,sec):
 ps=RANK[sec];a=defaultdict(lambda:{'score':0,'n':0})
 for p in ps:a[p['group']]['score']+=p['score'];a[p['group']]['n']+=1
 a=sorted(a.items(),key=lambda x:-x[1]['score']);total=sum(p['score'] for p in ps);title(f,520,417,3,'功能组：仓库数与分值份额')
 if sec=='45':a=[x for x in a if x[0]!='分类与样本待核']
 f.text(520,446,'以本节固定样本的已记录分值之和为分母',15,'muted')
 step=43 if sec!='45' else 28
 for i,(name,z) in enumerate(a):
  y=477+i*step;nm=name.replace('RISC-V 规范与计划','规范与计划').replace('设计工具与编译验证','设计与编译验证')
  fitted(f,520,y,nm,194,17,minfs=15);f.text(775,y,str(z['n'])+' 项',15,'muted',anchor='end');f.text(1000,y,f"{z['score']/total*100:.1f}%",17,'teal',True,'end')
  f.rect(790,y-12,133*z['score']/total,11,'teal',.75)
 if sec=='45':f.text(520,681,'另有分类待核 3 项，占样本分值 0.5%。',15,'muted')
def country(f,sec):
 d=PUBLIC[sec];title(f,520,659,4,'公开子样本：国别贡献前六位');f.text(520,686,f"期后读取 · {d['coverage']['labels']} 个不重叠项目标签",15.7,'muted')
 for i,p in enumerate(d['total']['countries'][:6]):
  y=713+i*26;co='china' if p['name']=='中国' else 'blue'
  f.text(520,y,p['name'],17,co,p['name'] in ['美国','中国']);f.rect(622,y-11,235*p['share']/50,11,co,.7);f.text(1000,y,f"{p['share']:.1f}%",17,co,True,'end')
 f.text(520,883,'分母仅含已识别地域；不是全样本年度国家榜。',15.5,'muted')
def boundary(f):
 ps=RANK['45'];cal=[p for p in ps if 'caliptra' in p['repo'].lower()];ot=next(p for p in ps if p['repo']=='lowRISC/opentitan');title(f,520,721,4,'从仓库边界理解体系能力')
 for i,(name,n,v) in enumerate([('OpenTitan',1,ot['score']),('Caliptra 家族',len(cal),sum(p['score'] for p in cal))]):
  y=757+i*49;f.text(520,y,name,19,'teal',True);f.text(1000,y,f'{n} 仓库 / '+fmt(v,1),18,anchor='end');f.rect(520,y+13,480*v/1100,9,'teal',.65)
 f.wrap(520,857,'同一硬件系统可拆成多仓库；这里只比较记录边界，不能据合计值判断系统优劣。',480,16,'muted',leading=23)
def render_one(sec):
 f=Figure(900);atlas(f,sec);f.line(0,388,1000,388);f.line(500,403,500,899);ranking(f,sec);group_stats(f,sec)
 if sec=='45':boundary(f)
 else:country(f,sec)
 name=f'4-{sec[1]}-overview';f.save(name);ps=contents(sec,name);save_pages(sec,ps);return ps
def contents(sec,figure):
 data={
 '43':('4.3 云基础设施技术全景','AI 服务需要运行、连接、调度与观测共同支撑。云基础设施全景按功能呈现这些公共底座，再通过项目、功能组与贡献地域识别协作集中在哪里。','图 4-8　云基础设施功能全景与分层排名。来源：2026 版 86 项固定清单、OpenDigger 主期月值；国家图为 2026.11.10 读取的 37 个公开项目标签。LLVM 作为通用编译底座纳入“观测与扩展”；清单不是全部云市场或 CNCF 托管目录。',[
 ('① AI 部署依赖多层公共底座','运行代理、身份管理、调度与观测承担不同职责。图中以 16 项示例呈现功能位置，不能把区块邻接理解为已经验证的部署依赖。'),
 ('② 通用工具链改变综合排名','LLVM 占样本已记录分值的 26.5%，Grafana 为 6.1%。综合榜受到基础工具体量影响，采用决策仍需回到对应类别比较。'),
 ('③ 仓库数量与协作分值不同序','应用与开发有 29 项，数量最多；观测与扩展仅 15 项，却占分值的 42.4%。分类观察揭示共同底座的权重，不能只按仓库数量配资源。'),
 ('④ 国家份额需要明确观察范围','公开子样本中美国、中国居前。国家图按贡献者所在地汇总，而非项目发起方；它提供跨境协作线索，不能代表全部 86 项的年度格局。')]),
 '44':('4.4 数据库系统技术全景','AI 扩大了检索需求，也依赖稳定的事务、分析和专用数据处理。数据库全景以工作负载组织观察，避免把向量检索视为对全部数据库能力的替代。','图 4-9　数据库功能全景与分层排名。来源：2026 版 93 项固定清单、OpenDigger 主期月值；国家图为 2026.11.10 读取的 62 个公开标签，关联 65 项。主展示类别去重，完整标签另存；地域份额仅以已识别贡献为分母。',[
 ('① 工作负载比单一热词更有解释力','事务与分析、文档与向量、时序与空间承担不同工作。图中按报告主展示类别排列，项目可同时具备多个标签，实际能力仍需按版本验证。'),
 ('② 项目影响分布相对分散','前 15 项合计占样本已记录分值的 43.8%；首位 Elasticsearch 为 5.7%。这说明样本内协作分布于多个系统，不能等同市场占有率。'),
 ('③ 传统数据底座仍有重要位置','通用与结构化组占分值的 70.9%，检索与关联为 20.2%。AI 数据方案需要组合查询、可靠存储和检索能力，而不是只追逐单一类别。'),
 ('④ 中国参与放在全球协作中观察','国别子样本中中国位列第二，荷兰等地区也有显著份额。与项目榜联合阅读有助于定位合作对象；本页不由国别合计推断项目控制权。')]),
 '45':('4.5 RISC-V 技术生态全景','RISC-V 是开放的处理器指令集架构。规范、芯片实现、编译验证、系统移植与软件分发共同构成生态；“开放指令集”并不等于所有芯片和配套代码都已开放。','图 4-10　RISC-V 功能全景、项目排名与仓库组织方式。来源：2026 版 78 项固定清单及 OpenDigger 主期月值；75 项已归入七类，3 项待核。标识为项目或注明的机构/上游；19 项连续 12 个月有记录，其他按已记录月份累计。',[
 ('① 从规范到可用系统需要完整链条','指令集说明接口规则，编译和验证检查软件与实现，操作系统和软件分发帮助实际采用。AI 相关应用仍要落实到设备和软件栈的兼容测试。'),
 ('② 头部协作同时围绕规范与实现','OpenTitan 居样本首位，规范手册、Caliptra 软件与 Sail 实现也在前列。月数列保留数据完整性，缺月的分值不能解释为全年不活跃。'),
 ('③ 规范与实现合计占约三分之二','两类共有 39 条记录，占已记录分值的 65.9%。共用规范和实际实现同时需要持续维护，项目数量不能直接换算为芯片或系统数量。'),
 ('④ 中国与全球接续应看具体工作','openEuler RISC-V 和 PLCT 持续集成出现在功能图中。系统移植、软件包和验证环境是可追踪的协作对象；本页不推算缺少证据的国别贡献。')])}
 title_,intro,caption,analyses=data[sec]
 return [page('4.'+sec[1],title_,intro,figure,caption,analyses,[],['I02','I03','I05','I06'])]
if __name__=='__main__':
 import sys
 sec=sys.argv[1];render_one(sec);(R/'review'/f'{sec}-figures.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2));print(json.dumps([q for q in QA if q['out_of_bounds'] or q['overlaps']],ensure_ascii=False))
