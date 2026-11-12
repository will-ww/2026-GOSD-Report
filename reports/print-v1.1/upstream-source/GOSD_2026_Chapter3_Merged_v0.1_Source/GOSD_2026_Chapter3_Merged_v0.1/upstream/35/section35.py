"""GOSD 3.5 v0.2. Three exact-data portrait compositions; source snapshots retained."""
from common import *
import shapefile, pycountry

RP=num(rows('35','new_repo.csv'),['rank','openrank','active_developers'])
PR=num(rows('35','new_project.csv'),['rank','openrank','active_developers','repo_count'])
REF=json.loads((D/'35/emerging-reference.json').read_text())
LOGOS=json.loads((D/'35/logo_row_mapping.json').read_text())
CA=json.loads((D/'source/cann-main68-aggregated.json').read_text())
CM=json.loads((D/'source/cann-monthly-repos.json').read_text())['data']
CD=json.loads((D/'source/cann-account-distribution.json').read_text())['data']
MAIN=sum(r['openrank'] for r in CA)
C.update(land='#EEF1F4',slate='#AAB4C6',gold='#9F8740',china='#A45B34',blue='#5063A7')
DOM=[('AI基础软件','AI 基础软件','violet'),('AI智能体与Agent工具','智能体与工具','blue'),('操作系统与智能终端','系统与终端','teal'),('桌面环境与开发者工具','桌面与开发工具','green'),('教育与开发者服务','教育与开发服务','gold'),('应用与游戏平台','应用与游戏','slate')]
SOURCES=[
 {'id':'E1','url':BASE+'table-3-5-1_new_repo_openrank_top30.csv','title':'新仓库前 30 位榜表；固定提交 c51e344。'},
 {'id':'E2','url':BASE+'table-3-5-2_new_project_openrank_top30.csv','title':'新项目前 30 位榜表；同一固定提交。'},
 {'id':'E3','url':BASE.split('/data/')[0]+'/preview/content/gosr/emerging-reference.json','title':'两榜逐项用途、组织和官方入口映射。'},
 {'id':'E4','url':'https://github.com/X-lab2017/open-digger/tree/master/skills','title':'OpenDigger 数据与指标说明；本轮查询及去重明细随源稿保存。'},
 {'id':'E5','url':'https://atomgit.com/cann','title':'CANN 官方首页，2026-11-10 读取：功能分层、治理、学习与算力入口。'},
 {'id':'E6','url':'https://www.huawei.com/cn/news/2025/8/ascend-summit-CANN-open-source','title':'华为 2025-08-05：宣布 CANN 全面开源开放。'},
 {'id':'E7','url':'https://www.huawei.com/cn/news/2025/9/hc-shengten-opensource','title':'华为 2025-09-20：技术指导委员会成立及与上游社区协作方向。'},
 {'id':'E8','url':'https://open-share.com/insight/companies/huawei/cann?scope=Global&unit=Project&timeType=month&time=2026-10&search=&page=1','title':'OpenShare CANN 洞察入口；本轮跳转登录，未取得页面数值。'}]

def logo(f,n,x,y,sz=21):
    a=next((r for r in LOGOS if r['name']==n),None)
    if a:img(f,R/'assets/emerging-logos/rendered'/Path(a['rendered_file']).name,x,y,sz,sz)

SHORT={'openharmony/multimedia_media_library':'OpenHarmony · 媒体库','openharmony/ability_ability_runtime':'OpenHarmony · 应用运行时','ibm-developer-skills-network/mcino-Introduction-to-Git-and-GitHub':'IBM · Git / GitHub 入门','mindspore/mindspore':'MindSpore / mindspore','NousResearch/hermes-agent':'NousResearch/hermes-agent'}
def ranking(f,data,project=False):
    f.text(0,59,'名次 / 项目' if project else '名次 / 仓库',14,'muted')
    f.text(410,59,'OpenRank',14,'muted',anchor='end');f.text(515,59,'参与账号 / 个',14,'muted',anchor='end');f.text(603,59,'仓库 / 个' if project else '平台',14,'muted',anchor='end')
    for i,r in enumerate(data[:20]):
        y=87+i*26;n=r['project'] if project else r['repo'];label=n if project else SHORT.get(n,n)
        if i%2==0:f.rect(0,y-19,607,26,'pale')
        f.text(0,y,f'{i+1:02}',15,'muted');logo(f,n,29,y-17)
        fs=min(16,275/max(1,tw(label,16))*16)
        f.text(57,y,label,fs,'ink',i<3);f.text(410,y,fmt(r['openrank'],1),16,'ink',i<3,'end')
        f.text(515,y,fmt(r['active_developers']),15.2,'muted',anchor='end')
        f.text(603,y,str(int(r['repo_count'])) if project else r['platform'],15,'violet' if project else ('teal' if r['platform']=='AtomGit' else 'blue'),project and r['repo_count']>1,'end')
    f.text(0,612,'参与账号沿用榜表字段；不等于代码作者或持续维护者。',14.4,'muted')

def fig_repos():
    f=Figure();panel(f,0,27,1,'新仓库影响力前 20 位');ranking(f,RP);f.line(620,0,620,805)
    panel(f,638,27,2,'技术构成：底层组件居多',19)
    f.text(638,58,'前 30 仓 · 每仓按主要用途归入一类',14.5,'muted')
    counts=Counter(REF['repos'][r['repo']]['domain'] for r in RP)
    for i,(key,label,col) in enumerate(DOM):
        yy=98+i*39;v=counts[key];f.text(638,yy,label,15.5);f.rect(781,yy-12,162*v/18,13,col);f.text(998,yy,str(v),18,col,True,'end')
    f.text(638,346,'22 / 30',33,'violet',True);f.text(786,343,'AI 基础软件与智能体',14.8,'muted')
    f.text(638,375,'两类合计占 73.3%，覆盖计算与使用入口。',14.6,'muted')
    panel(f,638,431,3,'平台与组件群的协作位置',18.5)
    for i,r in enumerate(RP):f.rect(638+(i%10)*19,456+(i//10)*19,15.5,15.5,'teal' if r['platform']=='AtomGit' else 'blue')
    for i,(n,v,c) in enumerate([('AtomGit',20,'teal'),('GitHub',10,'blue')]):
        yy=472+i*34;f.rect(853,yy-12,11,11,c);f.text(873,yy,n,15.5);f.text(998,yy,v,21,c,True,'end')
    f.text(638,542,'每格 1 仓，依榜单顺序；平台不代表国别。',13.8,'muted')
    f.text(638,579,'AtomGit 的 20 个入榜仓库分属',15.5,'ink',True)
    for i,(n,v) in enumerate([('CANN',8),('Ascend',8),('OpenHarmony',3),('MindSpore',1)]):
        yy=618+i*38;f.text(638,yy,n,16);f.rect(790,yy-12,154*v/8,13,'teal',.8);f.text(998,yy,v,18,'teal',True,'end')
    f.wrap(638,777,'多个组件可以属于同一软件体系；\n仓库席位不等于独立项目个数。',360,14.1,'muted',leading=21)
    panel(f,0,651,4,'头部影响集中，也有多种建设入口',19)
    total=sum(r['openrank'] for r in RP)
    pieces=[sum(r['openrank'] for r in RP[a:b])/total for a,b in [(0,1),(1,5),(5,10),(10,30)]]
    f.text(0,694,f'{sum(pieces[:2]):.1%}',34,'violet',True);f.text(157,691,'前 5 仓 / 30 仓 OpenRank 合计',16,'muted')
    xx=0;cols=['#554779','#587E80','#9F8740','#ACB7C9']
    for v,c in zip(pieces,cols):f.rect(xx,718,607*v,32,c);f.text(xx+607*v/2,740,f'{v:.1%}',16,'white',False,'middle');xx+=607*v
    for i,(n,c) in enumerate(zip(['第 1 名','第 2—5 名','第 6—10 名','第 11—30 名'],cols)):
        xx=i*152;f.rect(xx,775,11,11,c);f.text(xx+17,786,n,14,'muted')
    f.save('fig-3-14-emerging-repositories')

def proj(lon,lat):
    a,b,c,d=1.340264,-.081106,.000893,.003796;t=math.asin(math.sqrt(3)/2*math.sin(math.radians(lat)))
    return 2*math.sqrt(3)*math.radians(lon)*math.cos(t)/(3*(9*d*t**8+7*c*t**6+3*b*t*t+a)),t*(a+b*t*t+c*t**6+d*t**8)
def world(f,x,y,w,h):
    xmin,xmax,ymin,ymax=-2.72,2.72,-1.08,1.32;sc=min(w/(xmax-xmin),h/(ymax-ymin));ox=x+(w-sc*(xmax-xmin))/2;oy=y+(h-sc*(ymax-ymin))/2
    def pt(lon,lat):
        a,b=proj(lon,lat);return ox+(a-xmin)*sc,oy+(ymax-b)*sc
    for s in shapefile.Reader(str(D/'naturalearth_lowres.shp')).iterShapeRecords():
        n=s.record.as_dict()['name']
        if n=='Antarctica':continue
        color='china' if n in ['China','Taiwan'] else 'blue' if n=='United States of America' else 'land'
        inds=list(s.shape.parts)+[len(s.shape.points)]
        for i in range(len(inds)-1):f.path([pt(*p) for p in s.shape.points[inds[i]:inds[i+1]]],'white',.5,color)
    return pt

def fig_projects():
    f=Figure();panel(f,0,27,1,'新项目影响力前 20 位');ranking(f,PR,True);f.line(620,0,620,805)
    panel(f,638,27,2,'组织国别：已识别与未识别',18.4)
    f.text(638,58,'30 项中 13 项可识别；17 项未识别',14.7,'muted')
    pt=world(f,633,76,367,176)
    for lon,lat,tx,ty,label,col in [(-100,38,645,95,'美国 6 项','blue'),(105,35,890,255,'中国 7 项','china')]:
        xx,yy=pt(lon,lat);f.circle(xx,yy,3,col);f.line(xx,yy,tx,ty-4,'soft',.8);f.rect(tx-3,ty-17,tw(label,15)+6,23,'white',.96);f.text(tx,ty,label,15,col,True)
    groups=[('中国',7,'china'),('美国',6,'blue'),('未识别',17,'slate')]
    for i,r in enumerate(PR):
        n='中国' if '中国' in r['country_zh'] else '美国' if '美国' in r['country_zh'] else '未识别'
        f.rect(638+(i%10)*17,285+(i//10)*17,13,13,dict((a,c) for a,b,c in groups)[n])
    for i,(n,v,c) in enumerate(groups):
        yy=299+i*23;f.rect(826,yy-11,10,10,c);f.text(842,yy,n,14.5);f.text(998,yy,v,18,c,True,'end')
    f.wrap(638,375,'每格 1 项，按排名排列；国别按组织标签，\n不表示贡献者位置或未识别项缺乏组织。',360,13.8,'muted',leading=20)
    panel(f,638,441,3,'新项目的主要用途',19)
    cats=[('智能体与工具',25,'blue','Hermes Agent、DeepAgents','执行任务、记忆与工作流协作'),('AI 基础软件',4,'violet','CANN、vLLM-Omni、RLinf','计算支撑、多模态推理与训练'),('教育与开发服务',1,'gold','GitHub Spec Kit','规范驱动的开发工具')]
    for i,(n,v,c,ex,why) in enumerate(cats):
        yy=491+i*104;f.text(638,yy,n,17,'ink',True);f.text(998,yy,f'{v} 项',23,c,True,'end');f.rect(638,yy+12,360*v/30,12,c);f.text(638,yy+48,ex,14.8,'muted');f.text(638,yy+71,why,14.5,'muted')
    f.text(638,797,'项目榜平台：GitHub 29 项、AtomGit 1 项。',14.1,'muted')
    panel(f,0,651,4,'项目聚合改变了观察尺度',19.5)
    single=sum(r['openrank'] for r in PR if r['repo_count']==1)/sum(r['openrank'] for r in PR)
    for yy,label,v,tx1,tx2 in [(700,'项目数',20/30,'单仓 20 项','多仓 10 项'),(750,'分值占比',single,f'{single:.1%}',f'{1-single:.1%}')]:
        f.text(0,yy+7,label,15,'muted');x=94;w=513
        f.rect(x,yy-13,w*v,29,'blue');f.rect(x+w*v,yy-13,w*(1-v),29,'violet')
        f.text(x+w*v/2,yy+7,tx1,15,'white',False,'middle');f.text(x+w*v+w*(1-v)/2,yy+7,tx2,15,'white',False,'middle')
    f.text(0,797,'多仓项目包括 CANN（68 仓）、CLIProxyAPI（9 仓）、Paperclip（7 仓）。',13.8,'muted')
    f.save('fig-3-15-emerging-projects')

def smallbox(f,x,y,w,h,title,body,col='violet',fs=15):
    f.rect(x,y,w,h,mix(col,'white',.94));f.rect(x,y,3,h,col);f.text(x+12,y+22,title,fs,col,True);f.wrap(x+12,y+46,body,w-23,13.8,'ink',leading=20)

def fig_cann():
    f=Figure();f.line(545,0,545,805);f.line(0,408,1000,408)
    panel(f,0,27,1,'68 仓构成：从头部组件到长尾',19)
    f.text(0,63,'14,719.47',31,'violet',True);f.text(197,61,'主期项目 OpenRank',14,'muted')
    f.text(0,95,'前 12 仓占 77.4% · 其余 56 仓占 22.6%',15,'muted')
    for i,r in enumerate(CA[:12]):
        yy=124+i*22;n=r['repo_name'].split('/',1)[1]
        fs=min(14.5,219/max(1,tw(n,14.5))*14.5);f.text(0,yy,n,fs,'ink',i<2)
        f.rect(225,yy-11,200*r['openrank']/CA[0]['openrank'],11,'violet',.85)
        f.text(527,yy,f"{r['share']:.1%}",14.5,'violet',i<2,'end')
    f.text(0,397,'按仓库 ID 去重；改名记录合并，分母为完整 68 仓。',13.8,'muted')
    panel(f,563,27,2,'软件栈：让模型连接算力',19)
    f.wrap(563,58,'CANN 连接 AI 框架与昇腾处理器；\n下面呈现主要功能分工及代表仓库。',435,14.5,'muted',leading=21)
    f.rect(563,97,437,30,'pale');f.text(781,118,'上层框架与应用：PyTorch、vLLM 等',15,'ink',True,'middle')
    smallbox(f,563,139,437,63,'加速库｜复用计算与通信组件','算子 ops-nn / ops-transformer；通信 hcomm / hccl','violet')
    smallbox(f,563,213,437,63,'编程与编译｜支持定制计算','asc-devkit / pypto / pto-isa','blue')
    smallbox(f,563,287,437,63,'图、运行时与驱动｜组织程序执行','ge / runtime / driver','teal')
    f.rect(563,362,437,29,'ink');f.text(781,382,'昇腾 AI 处理器',16,'white',True,'middle')
    panel(f,0,446,3,'影响扩大与参与入口增多',19)
    month=defaultdict(lambda:{'score':0,'repos':set()})
    for r in CM:month[r['month']]['score']+=r['openrank'];month[r['month']]['repos'].add(r['repo_id'])
    keys=sorted(month);x0,x1=51,519;y0,y1=487,633
    px=lambda i:x0+i/(len(keys)-1)*(x1-x0);py=lambda v:y1-v/5500*(y1-y0)
    cut=keys.index('2026-06');boundary=(px(cut)+px(cut+1))/2
    f.rect(boundary,471,x1-boundary+8,287,'#F2EEF7')
    f.text(x0,476,'月度 OpenRank',13,'muted');f.text(x1,476,'7—10 月：期后观察',12.7,'violet',anchor='end')
    for v in [0,2000,4000]:
        yy=py(v);f.line(x0,yy,x1,yy,'line',.8);f.text(x0-8,yy+4,str(v),12.5,'muted',anchor='end')
    pts=[(px(i),py(month[k]['score'])) for i,k in enumerate(keys)]
    f.path(pts[:cut+1],'violet',2.7);f.path(pts[cut:],'violet',2.7,dash='5 4')
    for i in [0,4,cut,len(keys)-1]:f.circle(*pts[i],3.4,'violet')
    f.text(px(cut)-5,py(month['2026-06']['score'])-11,'3,520',14.5,'violet',True,'end');f.text(x1,py(month['2026-10']['score'])-12,'4,856',14.5,'violet',True,'end')
    f.text(0,662,'有影响力记录的仓库数 / 个',13,'muted')
    for i,k in enumerate(keys):
        v=len(month[k]['repos']);h=v/100*61;f.rect(px(i)-8,739-h,16,h,'teal',.85)
    for i in [0,4,cut,len(keys)-1]:f.text(px(i),739-len(month[keys[i]]['repos'])/100*61-6,len(month[keys[i]]['repos']),13,'teal',True,'middle')
    for i,l in [(0,'25.08'),(4,'25.12'),(8,'26.04'),(cut,'26.06'),(14,'26.10')]:f.text(px(i),759,l,12.6,'muted',anchor='middle')
    f.text(0,792,'6 月 → 10 月：OpenRank +37.9%；月度仓库 63 → 90。',14.2,'ink',True)
    panel(f,563,446,4,'跨仓协作如何接续公共能力',18.2)
    f.text(563,486,'5,282',31,'violet',True);f.text(683,483,'主期去机器人协作账号',14.2,'muted')
    f.text(998,513,'其中 1,868 个参与 ≥2 仓，占 35.4%',14.2,'ink',True,'end')
    vals=[3414,1313,555];cols=['#AAB4C6','#7253A2','#5063A7'];xx=563
    for v,c in zip(vals,cols):f.rect(xx,530,437*v/5282,23,c);xx+=437*v/5282
    for i,(lab,v,c) in enumerate(zip(['1 仓','2—3 仓','≥4 仓'],vals,cols)):
        xx=563+i*149;f.rect(xx,568,10,10,c);f.text(xx+16,578,f'{lab}  {v:,}',13.8,'muted')
    f.text(563,608,'连续建设还需要可进入、可验证、可维护',14.7,'ink',True)
    for i,(n,b) in enumerate([('使用入口','CANNLab 免费算力；Samples 示例'),('质量反馈','CANNBench 评测；Issue / PR 协作'),('共同治理','技术指导、项目管理、特别兴趣组')]):
        yy=642+i*40;f.text(563,yy,n,15,'violet',True);f.text(654,yy,b,14.1,'ink')
    f.wrap(563,774,'主页设施为 2026-11-10 观察；开放入口不等于\n已经实现普惠，仍需跟踪成本、维护和复用结果。',435,13.8,'muted',leading=21)
    f.save('fig-3-16-cann-multirepository')

def render():
    assert len(RP)==len(PR)==30 and len(CA)==68 and abs(MAIN-14719.47)<.01
    assert sum(int(r['accounts']) for r in CD)==5282
    fig_repos();fig_projects();fig_cann()
    pages=[
      page('3.5','3.5 全球新势力开源仓库与项目排行榜','“新”按本期榜表的创建记录界定，可能包含迁入或拆分，不等于技术首次出现。OpenRank 衡量协作网络影响；以仓库为单位，能看见 AI 底座和应用工具各自的建设入口。','fig-3-14-emerging-repositories','图 3-14　新仓库前 20 位、前 30 位技术与平台结构。来源：固定榜表［E1］、用途映射［E3］；分值窗口 2025.07—2026.06。仓库分值已用公开 OpenDigger 序列复算，复算最大差异为 0.02；“新”的历史资格另见附录 1。',[
       ('① 头部同时出现应用与计算组件','OpenClaw 位居首位，随后是 CANN 算子、昇腾框架适配和 MindSpore 仓库。智能体的快速迭代与计算基础软件的开放在同一名单中出现，提示产业应同时关注应用入口和持续支撑它的工程组件。'),
       ('② AI 供给的增长有清晰的层次','30 仓中，AI 基础软件占 18 仓，智能体与工具占 4 仓，合计 73.3%。算子是执行数学运算的基础组件，框架适配则帮助已有程序使用不同硬件；理解这些分工，才能判断可复用的资源究竟增加在哪里。'),
       ('③ 平台让不同协作体系变得可见','20 个 AtomGit 条目集中于 CANN、Ascend、OpenHarmony 和 MindSpore。多仓库拆分提供了具体参与入口，但 20 个席位并非 20 个独立技术体系；平台分布也不能直接当作国家贡献分布。'),
       ('④ 影响力识别重点，维护连接价值','前五仓占榜内分值的 43.9%，其余 25 仓仍构成较广的建设基础。支持新势力既要跟踪头部资源的复用，也应观察文档、测试和版本协同。短期排名说明网络位置，持续维护才决定资源能否长期使用。')],SOURCES[:4],['I02','I05','I10']),
      page('3.5','3.5.1 新势力项目：从组件走向整体供给','项目可以聚合多个仓库，形成面向使用者的较完整资源。本页以项目为单位观察排名、组织与用途，并与上一页衔接：统计单位和纳入范围改变后，看到的技术结构也会改变。','fig-3-15-emerging-projects','图 3-15　新项目前 20 位、前 30 位组织国别、用途和聚合结构。来源：固定榜表［E2］、逐项映射［E3］；主统计期同前。国别按榜表组织标签；未识别单列。分值份额以本页 30 项合计为分母，不代表全球市场份额。',[
       ('① 多仓体系与轻量工具并列出现','CANN 位列第一，Hermes Agent 与 DeepAgents 随后。CANN 聚合 68 仓，后两项各为单仓，说明新供给既可以来自软件体系的整体开放，也可以来自聚焦任务的工具。分值须与对象范围一同理解。'),
       ('② 中国贡献覆盖底座与应用工具','已识别的中国组织有 7 项，包含 CANN、OpenViking、Astron、Nanobot、QwenPaw 等，跨越计算支撑、企业工具与高校研发。另有 17 项组织国别未识别，因此当前地图呈现的是已知布局，不能推断完整全球格局。'),
       ('③ 项目入口更集中于智能体工作流','25 项主要用于智能体与相关工具，占 83.3%；AI 基础软件为 4 项。与仓库榜的组件结构对照，可见从计算支撑到任务执行的两层供给。两榜平台与纳入范围不同，这一差异也不能全部归因于仓库聚合。'),
       ('④ 聚合能力要接受协作质量的检验','多仓项目为 10 项，占项目数的三分之一，却占榜内分值的 67.5%。这提示比较新势力时要兼看组件范围、接口配套与跨仓协作。仓库多并不自动代表体系成熟；CANN 为进一步观察提供了具体案例。')],SOURCES[:4],['I02','I05','I10']),
      page('3.5','3.5.2 CANN：把多仓供给组织为体系能力','CANN（神经网络计算架构）是华为面向 AI 的异构计算软件栈，连接框架与昇腾处理器。其价值不仅在于开放组件的数量，还在于计算、编程、运行与社区维护能否共同接续。','fig-3-16-cann-multirepository','图 3-16　CANN 完整 68 仓画像与期后延伸。来源：OpenDigger 只读查询［E4］、CANN 官方首页［E5］及开放与治理公告［E6—E7］。主期为 2025.07—2026.06；曲线右侧为 2026.07—10，主页设施为 11-10 观察。仓库依 ID 去重，账号口径见附录 1。',[
       ('① 完整范围使结构性贡献可被识别','68 仓汇总分值与原榜一致，前 12 仓占 77.4%。Transformer 与神经网络算子居前，编程、通信及推理实践也进入头部。中国 AI 开源的贡献因而可以落实到可协作的软件层次，而不止停留在模型名称。'),
       ('② 分层开放为上游协作提供接口','官方资料将加速库、编程编译、图引擎和运行时等分层呈现，并提出与 PyTorch、vLLM 等社区协作。接口开放为适配与性能改进提供条件；是否形成跨境复用，还应继续核对版本兼容、上游接纳和实际采用。'),
       ('③ 影响力增长伴随组件范围扩展','主期末 6 月月度 OpenRank 为 3,520，10 月升至 4,856；有影响力记录的仓库由 63 个增至 90 个。增长体现协作网络与组件范围的共同扩展，不能直接解释为单仓效率、代码质量或商业采用提高。'),
       ('④ 从开放入口走向持续公共能力','主期 5,282 个去机器人协作账号中，1,868 个跨仓参与；另有 1,869 个在至少三个月出现。免费算力、示例和评测为参与提供条件，后续应以适配成本、跨组织维护与复用结果，检验其对 AI 普惠的实际支持。')],SOURCES[3:],['I03','I05','I06','I10'])]
    save_pages('35',pages)
    checks={'period':'2025-07-01/2026-06-30','repo_n':len(RP),'project_n':len(PR),'repo_total':sum(x['openrank'] for x in RP),'project_total':sum(x['openrank'] for x in PR),'cann_repo_ids':len(CA),'cann_score':MAIN,'cann_top12_share':sum(x['share'] for x in CA[:12]),'cann_accounts':5282,'cann_multirepo_accounts':1868,'cann_3plus_month_accounts':1869,'unknown_project_country':17}
    (R/'review/data-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
    return pages
