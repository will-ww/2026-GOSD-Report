from common import *
import shapefile,pycountry
C.update(land='#EBF0F3',gold='#A78332',slate='#9BAABA')
FD=num(rows('33','table-3-3-1_global_foundation_openrank.csv'),['rank','openrank','active_developers'])[:20]
ST=json.loads((D/'33/foundation-statistics.json').read_text()); LF=json.loads((D/'33/lf-subgroups.json').read_text()); MON=json.loads((D/'33/foundation-monthly.json').read_text())['data']
H={r['id']:r for r in json.loads((D/'33/all-label-hierarchy.json').read_text())['data']}
TOP=json.loads((D/'33/foundation-top-repos-raw.json').read_text())['data']
LOGOS=json.loads((D/'33/logo-manifest.json').read_text())
SHORT={'Linux Foundation':'Linux 基金会及子基金会','OpenAtom Foundation':'开放原子开源基金会','Apache Software Foundation':'Apache 软件基金会','Stichting NixOS Foundation':'NixOS 基金会','Python Software Foundation':'Python 软件基金会','Connectivity Standards Alliance':'连接标准联盟（CSA）','Free EBook Foundation':'Free EBook 基金会','Zig Software Foundation':'Zig 软件基金会','Rust Foundation':'Rust 基金会','Ruby Foundation':'Ruby 基金会','PHP Foundation':'PHP 基金会','Godot Foundation':'Godot 基金会','DuckDB Foundation':'DuckDB 基金会','Bevy Foundation':'Bevy 基金会','Gentoo Foundation':'Gentoo 基金会','Trino Foundation':'Trino 基金会','Anoma Foundation':'Anoma 基金会','Eclipse Foundation':'Eclipse 基金会','farama':'Farama 基金会'}
LS={'cncf':'CNCF','pytorch':'PyTorch','openjs':'OpenJS','lfai':'LF AI & Data','aaif':'AAIF','riscv':'RISC-V','openssf':'OpenSSF','hyperledger':'Hyperledger¹','lfed':'LF Edge','presto':'Presto','o3d':'Open 3D','lfne':'LF Networking','finops':'FinOps'}
ISO={'美国':'us','中国':'cn','荷兰':'nl','日本':'jp','瑞士':'ch','比利时':'be'}
for r in FD:
 r['country']=r['country_zh'][2:] if r['country_zh'] else '荷兰'
 if r['foundation']=='Eclipse Foundation':r['country']='比利时'
def fname(r):return SHORT.get(r['foundation'],r['foundation'])
def logo(f,name,x,y,size=22):
 if name in LOGOS:img(f,R/'assets/foundation-logos'/LOGOS[name]['filename'],x,y,size,size)
def flag(f,c,x,y):img(f,R/'assets/flags'/f'{ISO[c]}.svg',x,y,21,15)
def proj(lon,lat):
 a,b,c,d=1.340264,-.081106,.000893,.003796;t=math.asin(math.sqrt(3)/2*math.sin(math.radians(lat)))
 return 2*math.sqrt(3)*math.radians(lon)*math.cos(t)/(3*(9*d*t**8+7*c*t**6+3*b*t*t+a)),t*(a+b*t*t+c*t**6+d*t**8)
def world(f,x,y,w,h):
 vals=Counter(ISO[r['country']].upper() for r in FD);xmin,xmax,ymin,ymax=-2.72,2.72,-1.08,1.32;sc=min(w/(xmax-xmin),h/(ymax-ymin));ox=x+(w-sc*(xmax-xmin))/2;oy=y+(h-sc*(ymax-ymin))/2
 def point(lon,lat):a,b=proj(lon,lat);return ox+(a-xmin)*sc,oy+(ymax-b)*sc
 for s in shapefile.Reader(str(D/'naturalearth_lowres.shp')).iterShapeRecords():
  r=s.record.as_dict();n=r['name']
  if n=='Antarctica':continue
  try:iso={'France':'FR','Norway':'NO','Taiwan':'CN'}.get(n) or pycountry.countries.get(alpha_3=r['iso_a3']).alpha_2
  except:iso='ZZ'
  v=vals.get(iso,0);col=mix('#ECE6F3','violet',.2+.8*math.sqrt(v/13)) if v else 'land';inds=list(s.shape.parts)+[len(s.shape.points)]
  for i in range(len(inds)-1):f.path([point(*p) for p in s.shape.points[inds[i]:inds[i+1]]],'white',.45,col)
 return point

def board():
 f=Figure();panel(f,0,27,1,'全球基金会榜前 20 位')
 f.text(0,59,'名次 / 基金会',14,'muted');f.text(353,59,'所属国 / 标签',13.5,'muted');f.text(608,59,'OpenRank',14,'muted',anchor='end')
 for i,r in enumerate(FD):
  y=91+i*32
  if i%2==0:f.rect(0,y-20,614,32,'pale')
  f.text(0,y,f'{i+1:02}',15,'muted');logo(f,r['foundation'],28,y-19,22);f.text(59,y,fname(r),15.2,'ink',i<3);flag(f,r['country'],353,y-14);f.text(381,y,r['country'],14,'muted');f.text(608,y,fmt(r['openrank'],2),16,'ink',i<3,'end')
 f.wrap(0,748,'原榜数值保留；LF 为含子基金会的汇总，标签可能重叠，不以榜内相加值推算全球份额。',613,15,'muted',leading=23)
 f.line(630,0,630,805)
 panel(f,653,27,2,'基金会的国别分布',19)
 f.text(653,66,'20',31,'violet',True);f.text(696,65,'个榜单条目',15,'muted');f.text(868,66,'6',31,'violet',True);f.text(895,65,'个国别',15,'muted')
 pt=world(f,647,77,353,184)
 for lon,lat,n,tx,ty in [(-99,39,'美国 13',656,282),(105,35,'中国 1',904,282),(5,52,'荷兰 3',748,104)]:
  px,py=pt(lon,lat);f.circle(px,py,3,'violet');f.line(px,py,tx+18,ty-10,'soft');f.text(tx,ty,n,15,'violet',True)
 f.text(653,310,'日本、瑞士、比利时各 1；灰色为未入榜。',13.8,'muted')
 f.text(653,333,'机构国别不代表项目贡献者的地理来源。',13.8,'muted')
 panel(f,653,380,3,'标签识别的项目组合',18.8)
 vals=[('LF 标签族',len(set().union(*[{k for k in descendants(r['id']) if H.get(k,{}).get('type')=='Project'} for r in ST if r['id'].startswith(':foundations/linux_foundation')]))),('开放原子',41),('Apache',25)]
 for i,(n,v) in enumerate(vals):
  y=423+i*47;f.text(653,y,n,16);f.rect(760,y-13,174*v/vals[0][1],13,'violet',.78);f.text(998,y,v,19,'violet',True,'end')
 f.wrap(653,564,'按项目标签去重；仅为数据库已识别项目，不是各基金会官方托管总数。',347,14.2,'muted',leading=22)
 panel(f,653,638,4,'主期仓库覆盖的差异',18.8)
 for i,(n,v) in enumerate([('开放原子',19043),('LF 标签族',2981),('Apache',1322)]):
  y=678+i*34;f.text(653,y,n,16);f.text(998,y,fmt(v)+' 个',20,'violet',True,'end')
 f.wrap(653,789,'平台＋仓库 ID 去重；仓库数不等于项目数。',347,13.3,'muted',leading=20)
 f.save('fig-3-7-foundations')

def descendants(k,seen=None):
 if seen is None:seen=set()
 for c in H.get(k,{}).get('children',[]):
  if c not in seen:seen.add(c);descendants(c,seen)
 return seen

def lf_page():
 f=Figure();panel(f,0,27,1,'LF 旗下 13 个可观测子标签')
 f.text(0,59,'名次 / 子标签',14,'muted');f.text(470,59,'OpenRank',14,'muted',anchor='end');f.text(608,59,'仓库 / 个',14,'muted',anchor='end')
 for i,r in enumerate(LF):
  y=91+i*32
  if i%2==0:f.rect(0,y-20,615,32,'pale')
  k=r['id'].split('/')[-1];f.text(0,y,f'{i+1:02}',15,'muted');f.text(33,y,LS[k],16,'ink',i<3);f.rect(204,y-12,135*r['openrank']/LF[0]['openrank'],12,'violet',.8);f.text(470,y,fmt(r['openrank'],1),16,'violet',i<3,'end');f.text(608,y,fmt(int(r['repositories'])),16,'muted',anchor='end')
 f.wrap(0,527,'¹ Hyperledger 沿用数据库标签名称。按当前标签回溯主期；AAIF 含期后加入项目，不能解释为全年托管绩效。',615,14.2,'muted',leading=22)
 panel(f,649,27,2,'中位层：安全标签前移',18.5)
 f.text(649,58,'固定 13 标签样本内的月度名次',14,'muted')
 x0,x1,y0,y1=673,960,103,280
 for rank in [6,7,8]:
  yy=y0+(rank-6)*(y1-y0)/2;f.line(x0,yy,x1,yy);f.text(661,yy+5,rank,13.5,'muted',anchor='end')
 groups=defaultdict(list)
 for r in MON:
  if r['id'].startswith(':foundations/linux_foundation/'):groups[r['month']].append(r)
 months=sorted(groups)
 for key,col in [('riscv','gold'),('openssf','teal'),('hyperledger','violet')]:
  vals=[next(i+1 for i,r in enumerate(sorted(groups[m],key=lambda r:-r['openrank'])) if r['id'].endswith('/'+key)) for m in months]
  pts=[(x0+i*(x1-x0)/11,y0+(v-6)*(y1-y0)/2) for i,v in enumerate(vals)];f.path(pts,col,2.8)
  for px,py in pts:f.circle(px,py,2.7,col)
  f.text(980,pts[-1][1]+5,vals[-1],16,col,True)
 for i in [0,3,6,8,11]:f.text(x0+i*(x1-x0)/11,310,['07','08','09','10','11','12','01','02','03','04','05','06'][i],13,'muted',anchor='middle')
 for i,(key,col) in enumerate([('riscv','gold'),('openssf','teal'),('hyperledger','violet')]):
  y=346+i*30;f.line(649,y-6,674,y-6,col,3);f.text(686,y,LS[key].rstrip('¹'),16,col)
 f.text(649,450,'2025.07—2026.06；第 1 名更靠前。',13.8,'muted')
 rule(f,578)
 panel(f,0,613,3,'核心仓库在不同组合中的分量')
 f.text(0,643,'标签内分值构成',14,'muted');f.text(610,643,'首位仓库',14,'muted',anchor='end')
 for i,key in enumerate(['cncf','pytorch','openjs','lfai','aaif']):
  r=next(r for r in LF if r['id'].endswith('/'+key));rs=[t for t in TOP if t['id']==r['id']];vals=[rs[0]['openrank'],sum(t['openrank'] for t in rs[1:]),r['openrank']-sum(t['openrank'] for t in rs)];yy=674+i*25
  f.text(0,yy,LS[key],14.8);xx=126
  for v,col in zip(vals,['violet','soft','#DCE5EC']):ww=245*v/r['openrank'];f.rect(xx,yy-13,ww,14,col);xx+=ww
  f.text(422,yy,f'{vals[0]/r["openrank"]:.0%}',14.5,'violet',True,'end');name=rs[0]['repo_name'].split('/')[-1];f.text(610,yy,name[:24],13.5,'muted',anchor='end')
 for xx,lab,col in [(0,'首位','violet'),(94,'第 2—3 位','soft'),(242,'其余仓库','#DCE5EC')]:f.rect(xx,789,10,10,col);f.text(xx+16,798,lab,13,'muted')
 panel(f,649,515,4,'项目与仓库：两个尺度',18)
 f.text(649,548,'已识别项目标签 / 主期仓库数量',14,'muted')
 f.text(649,582,'子标签',13.5,'muted');f.text(848,582,'项目',13.5,'muted',anchor='end');f.text(998,582,'仓库',13.5,'muted',anchor='end')
 for i,key in enumerate(['cncf','openjs','lfai','pytorch','aaif']):
  r=next(r for r in LF if r['id'].endswith('/'+key));yy=617+i*31;f.text(649,yy,LS[key],16);f.text(848,yy,r['projects'],18,'violet',True,'end');f.text(998,yy,fmt(int(r['repositories'])),18,'teal',True,'end')
 f.wrap(649,780,'项目可包含多个仓库；项目标签尚未覆盖全部组织实体。',347,14,'muted',leading=21)
 f.save('fig-3-8-lf-subfoundations')

def aaif_page():
 f=Figure();panel(f,0,27,1,'从 3 个创始项目，到 10 个公共组件')
 f.rect(0,43,490,144,'#F2F0F8');f.rect(505,43,495,144,'#F4F8F7')
 for x,y,big,date,desc in [(20,100,'3','2025.12.09','MCP · goose · AGENTS.md'),(276,100,'4','2026.06.04','加入 agentgateway'),(525,100,'6','2026.09','A2A、Agent Router 加入'),(785,100,'10','2026.10.22','技能、模型接口、训练、沙箱')]:
  f.text(x,y,big,36,'violet' if x<500 else 'teal',True);f.text(x+64,y-13,date,17,'ink',True);f.wrap(x,y+37,desc,230,15,'muted',leading=22)
 f.text(20,174,'主统计期内',14,'violet',True);f.text(525,174,'期后观察 · 截至 2026.11.10',14,'teal',True)
 panel(f,0,226,2,'共同组件解决不同问题：功能地图')
 f.text(998,225,'● 主期已加入    ○ 期后加入',14,'muted',anchor='end')
 lanes=[('指导与技能','让经验能够携带与复用',[('AGENTS.md','OpenAI',False),('Agent Skills','Anthropic',True)]),('协议与互通','让工具、模型与 Agent 相连',[('MCP','Anthropic',False),('A2A','Google',True),('Open Responses','OpenAI',True)]),('执行与沙箱','让任务执行具备运行环境',[('goose','Block',False),('OpenSandbox','阿里巴巴',True)]),('流量与运营','统一连接、路由与访问管理',[('agentgateway','Solo.io',False),('Agent Router','Tetrate / Bloomberg',True)]),('训练与评测','让训练任务与反馈可以复用',[('OpenEnv','Hugging Face',True)])]
 for i,(cat,meaning,items) in enumerate(lanes):
  y=250+i*52;f.rect(0,y,1000,45,'pale' if i%2==0 else 'white');f.text(0,y+18,cat,17,'ink',True);f.text(0,y+39,meaning,13.5,'muted')
  for j,(name,donor,after) in enumerate(items):
   x=285+j*239;col='teal' if after else 'violet';f.circle(x+5,y+13,4,col,not after);f.text(x+17,y+19,name,16.7,col,True);f.text(x+17,y+39,donor,13.5,'muted')
 f.text(0,530,'分类为报告分析；项目名称、贡献主体和加入信息依据官方资料，不表示强制技术依赖。',14,'muted')
 panel(f,0,577,3,'项目记录：协作变化并不同步',19)
 f.text(0,608,'OpenDigger 标签 OpenRank · 2025.12 → 2026.06',14,'muted')
 core=json.loads((D/'33/aaif-core-monthly.json').read_text())['data']
 names=[('Model Context Protocol','MCP','violet'),('Goose','goose','blue'),('agentgateway','agentgateway','teal'),('AGENTS.md','AGENTS.md','gold')]
 for i,(name,label,col) in enumerate(names):
  y=643+i*37;rs={r['month'][:7]:r['openrank'] for r in core if r['name']==name};vals=[rs.get(m) for m in ['2025-12','2026-01','2026-02','2026-03','2026-04','2026-05','2026-06']];f.text(0,y,label,16,col,True);mx=max(v for v in vals if v is not None);pts=[(183+j*25,y-3-23*v/mx) for j,v in enumerate(vals) if v is not None];f.path(pts,col,2);end='未记录' if vals[-1] is None else f'{vals[-1]:.1f}';f.text(610,y,f'{vals[0]:.1f} → {end}',17,col,True,'end')
 f.wrap(0,794,'各趋势线独立尺度；AGENTS.md 末月缺记录，不补零。',610,13.5,'muted',leading=20)
 panel(f,649,577,4,'从项目接收，走向持续维护',18.2)
 stages=[('Sandbox','可运行实现、维护者与开放流程'),('Growth','至少 2 家无关联组织的生产使用'),('Impact','稳定采用与持续维护能力')]
 for i,(a,b) in enumerate(stages):
  y=620+i*55;f.text(649,y,a,18,'violet',True);f.wrap(649,y+24,b,347,14.7,'muted',leading=22)
 f.wrap(649,793,'现行生命周期政策：2026.10.15 更新。',347,13.4,'muted',leading=20)
 f.save('fig-3-9-aaif')

SOURCES=[{'id':'F1','url':BASE+'table-3-3-1_global_foundation_openrank.csv'}, {'id':'F2','url':'https://github.com/X-lab2017/open-digger/tree/master/labeled_data/foundations'}, {'id':'F3','url':'https://duckdb.foundation/'},{'id':'F4','url':'https://www.eclipse.org/org/foundation/annual-reports/2025/'}, {'id':'A1','url':'https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation'}, {'id':'A2','url':'https://aaif.io/blog/agentgateway-joins-aaif-as-an-open-gateway-for-agentic-ai-infrastructure'},{'id':'A3','url':'https://aaif.io/news/agentic-ai-foundation-announces-four-new-projects'},{'id':'A4','url':'https://aaif.io/projects'},{'id':'A5','url':'https://github.com/aaif/technical-committee/blob/main/governance/project-lifecycle-policy.md'},{'id':'A6','url':'https://www.linuxfoundation.org/press/agentic-ai-foundation-welcomes-the-gates-foundation-to-help-expand-the-benefits-of-agentic-ai-globally'},{'id':'A7','url':'https://aaif.io/blog/a2a-joins-aaif'},{'id':'A8','url':'https://aaif.io/blog/agent-router-joins-aaif'}]
def render():
 board();lf_page();aaif_page()
 pages=[page('3.3','3.3 全球开源基金会影响力排行榜','基金会把分散的项目、维护者与资源连接为共同建设的组织网络。从国别分布进入项目组合，才能理解开放资源由谁持续支持，以及榜单覆盖了什么。','fig-3-7-foundations','图 3-7　全球基金会榜、国别及项目与仓库覆盖。榜值沿用原表［F1］；项目与仓库按 OpenDigger 标签查询［F2］（2026.11.10 快照，回溯 2025.07—2026.06）。DuckDB、Eclipse 国别据官网补正［F3–F4］。',[
 ('① 前列是不同组织范围的共同建设网络','LF、开放原子与 Apache 位居原榜前三。LF 条目包含子基金会，其他条目的项目组合也各不相同。排名适合作为寻找合作网络的入口，不宜以分值直接评价机构效率或治理质量。'),
 ('② 组织落点集中，协作范围仍可跨越国界','前二十条目覆盖六个国别，美国占十三，荷兰占三；中国、日本、瑞士与比利时各一。这里呈现机构标签与归属资料，不能据此把其全部项目和贡献者归入同一国家。'),
 ('③ 从基金会名称继续进入具体项目','项目标签揭示组织之内的供给组合。开放原子有四十一个已识别项目，Apache 有二十五个；LF 标签族共识别一百八十一个项目。识别组合有助于把支持资金落实到具体维护对象。'),
 ('④ 仓库广度应与项目组织方式一起阅读','主期可见仓库中，开放原子为 19,043 个，LF 标签族去重为 2,981 个，Apache 为 1,322 个。同一个项目可能拆分为许多仓库，组织标签的覆盖也不均衡，数量差异不能直接解释为产出或公共价值差距。')],SOURCES[:4],['I06','I09']),
 page('3.3','3.3.1 LF 内部：多层技术供给与维护重心','LF 旗下的组织组合同时覆盖云原生、AI、Web、安全与硬件。本图从有主期记录的十三个子标签展开，观察规模、核心仓库与相对位次，而不把它们视为互不重叠的资产包。','fig-3-8-lf-subfoundations','图 3-8　LF 子标签的规模、月度位次及项目组合。来源：OpenDigger 标签与 global_openrank［F2］；2025.07—2026.06，按 2026.11.10 标签回溯。标签分值沿用原聚合方式；跨标签与组织／仓库映射可能重叠，不相加推算 LF 唯一总量。',[
 ('① 云原生与 AI 构成前列的两个重点','CNCF 与 PyTorch 分列样本前两位，OpenJS 随后。基金会提供的公共基础覆盖运行环境、计算框架和开发工具；支持 Agent 与模型应用，需要同时关注这些已有的软件基础。'),
 ('② 安全标签前移，提示持续维护的需求','OpenSSF 在固定样本中的月度名次由第八升至第六，RISC-V 则由第六至第八，Hyperledger 回到第七。这反映相对协作位置变化，可作为追踪维护重点的信号，不能直接推断技术质量或安全成效。'),
 ('③ 核心集中程度提示不同的支持任务','PyTorch 首位仓库占标签分值的 39.2%，前三位占 73.5%；CNCF 分别为 5.2% 和 10.8%。前者更应检查核心仓库的维护接续，后者更需要跨项目协调；这些结构差异是核查入口，不等于风险高低的直接结论。'),
 ('④ 项目标签与代码仓库应保持两个尺度','CNCF 的七十个项目标签对应 1,339 个主期仓库，PyTorch 的五个项目标签对应 102 个。两种数字分别回答“有哪些项目”和“观察到哪些代码单元”；它们受映射覆盖影响，不宜当作官方完整托管清单。')],[SOURCES[1]],['I02','I06','I09']),
 page('3.3','3.3.2 AAIF：Agent 协作的公共组件','Agentic AI Foundation（AAIF）于 2025 年 12 月成立于 LF 框架下。其意义不只在于聚集热门项目，更在于让连接、指引、执行与运行环境获得跨组织共同演进的空间。','fig-3-9-aaif','图 3-9　AAIF 项目扩展、功能分工、协作记录与治理条件。成立及加入资料［A1–A4、A7–A8］；OpenDigger 主期记录［F2］。期后目录截至 2026.11.10；生命周期政策为 2026.10.15 版［A5］，不回溯为主期制度。',[
 ('① 扩展发生在清楚可辨的时间边界内','主期内从三个创始项目扩至四个；A2A 与 Agent Router 以及十月的四个新项目均属期后加入。主期末的四个项目与当前十个项目分别陈述，才能看清组织扩展，而不夸大全年托管规模。'),
 ('② 中国贡献可以体现为可复用公共组件','功能地图覆盖指引、互通、执行、流量管理与训练。阿里巴巴贡献的 OpenSandbox 于十月加入，为 AI 应用提供统一沙箱接口。这是中国资源进入全球共同建设的具体例证，实际使用与维护效果仍需继续跟踪。'),
 ('③ 协作记录与使用扩散需要分别观察','十二月至六月，agentgateway 的标签分值由 20.9 至 34.5，MCP 与 goose 的可见分值则下降。协议采用、工具使用和仓库协作并非同一个量；这些变化不能直接解释为市场采用变化或基金会支持成败。'),
 ('④ 公共能力需要治理门槛与使用者参与','现行政策把可运行实现、外部生产使用和持续维护纳入分阶段要求。期后 Gates Foundation 加入并支持非洲开发者参与［A6］，提供了扩大代表性的路径；后续应跟踪本地化成本、维护接续与服务结果，而非仅统计成员增长。')],SOURCES[1:],['I06','I09'])]
 save_pages('33',pages);return pages
