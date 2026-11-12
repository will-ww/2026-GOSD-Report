"""Four traceable, portrait project-ranking compositions. Fixed data, no simulations."""
from common import *
import shapefile, pycountry

G=json.loads((D/'global100.json').read_text())
CN=num(rows('34','table-3-4-3_china_project_openrank_top30.csv'),['rank','openrank','active_developers'])
PURPOSE=rows('34','project-purpose-matched.csv')
LOGO=json.loads((D/'34/logo-manifest.json').read_text())
for r in G:
    r['org_type']='未识别' if not r['org'] else '基金会' if any(x in r['org'] for x in ['基金会','Foundation']) else '高校' if '大学' in r['org'] else '企业及其他机构'
ALL=json.loads((D/'source/project-mainperiod-all.json').read_text())['data']
MATCH=json.loads((R/'review/china30-reconciliation.json').read_text())
for r,m in zip(CN,MATCH):
    assert m['project']==r['project'] and m['score_ok']
    r['global_rank']=1+next(i for i,a in enumerate(ALL) if a['id']==m['match'][0]['id'])
    r['org']=r['initiator_zh']
    r['org_type']='未识别' if not r['org'] else '基金会' if '基金会' in r['org'] else '企业及其他机构'
COUNTS=Counter(r['country'] for r in G)
C.update(land='#EDF0F4',gold='#9F8740',slate='#AAB4C6',violet='#7253A2',china='#A45B34',blue='#5063A7')
CC={'美国':'blue','中国':'china','荷兰':'violet','德国':'teal','其他 8 国':'gold','未识别':'slate'}
def cgroup(n):return n if n in ['美国','中国','荷兰','德国','未识别'] else '其他 8 国'
def logo(f,name,x,y,size=21):
    if name in LOGO:img(f,R/'assets/project-logos'/LOGO[name]['file'],x,y,size,size)
def ranking(f,data,china=False):
    f.text(0,59,'名次 / 项目',14,'muted');f.text(395,59,'OpenRank',14,'muted',anchor='end')
    f.text(510,59,'参与账号 / 个',14,'muted',anchor='end');f.text(600,59,'全球名次' if china else '组织国别',14,'muted',anchor='end')
    for i,r in enumerate(data[:20]):
        y=87+i*26
        if i%2==0:f.rect(0,y-19,602,26,'pale')
        f.text(0,y,f'{int(r["rank"]):02}',15,'muted');logo(f,r['project'],30,y-17)
        size=min(16,230/max(1,tw(r['project'],16))*16)
        f.text(60,y,r['project'],size,'ink',i<3)
        f.text(395,y,fmt(r['openrank'],1),16,'ink',i<3,'end')
        f.text(510,y,fmt(r['active_developers']),15.5,'muted',anchor='end')
        label=str(r['global_rank']) if china else r['country']
        f.text(600,y,label,15,'china' if (china and r['global_rank']<=100) or label=='中国' else 'ink',china and r['global_rank']<=100,'end')
    f.text(0,612,'参与账号为榜表关联开发者字段；不等于员工或代码作者。',14.5,'muted')

def proj(lon,lat):
    a,b,c,d=1.340264,-.081106,.000893,.003796;t=math.asin(math.sqrt(3)/2*math.sin(math.radians(lat)))
    return 2*math.sqrt(3)*math.radians(lon)*math.cos(t)/(3*(9*d*t**8+7*c*t**6+3*b*t*t+a)),t*(a+b*t*t+c*t**6+d*t**8)
def world(f,x,y,w,h):
    codes={'美国':'US','中国':'CN','荷兰':'NL','德国':'DE','俄罗斯':'RU','比利时':'BE','日本':'JP','冰岛':'IS','南非':'ZA','以色列':'IL','挪威':'NO','保加利亚':'BG'}
    vals={codes[k]:v for k,v in COUNTS.items() if k in codes};xmin,xmax,ymin,ymax=-2.72,2.72,-1.08,1.32
    sc=min(w/(xmax-xmin),h/(ymax-ymin));ox=x+(w-sc*(xmax-xmin))/2;oy=y+(h-sc*(ymax-ymin))/2
    def pt(lon,lat):
        a,b=proj(lon,lat);return ox+(a-xmin)*sc,oy+(ymax-b)*sc
    for s in shapefile.Reader(str(D/'naturalearth_lowres.shp')).iterShapeRecords():
        r=s.record.as_dict();n=r['name']
        if n=='Antarctica':continue
        try:iso={'France':'FR','Norway':'NO','Kosovo':'XK','Somaliland':'SO','N. Cyprus':'CY','Taiwan':'CN'}.get(n) or pycountry.countries.get(alpha_3=r['iso_a3']).alpha_2
        except:iso='ZZ'
        v=vals.get(iso);color=mix('#EDE6F4','violet',.2+.8*math.sqrt(v/69)) if v else C['land']
        inds=list(s.shape.parts)+[len(s.shape.points)]
        for i in range(len(inds)-1):f.path([pt(*p) for p in s.shape.points[inds[i]:inds[i+1]]],'white',.5,color)
    return pt

def fig_global():
    f=Figure();panel(f,0,27,1,'全球项目影响力前 20 位');ranking(f,G);f.line(615,0,615,805)
    panel(f,632,27,2,'项目组织的国别分布',19.8)
    f.text(632,58,'100 强：91 项国别可识别 · 覆盖 12 国',14.8,'muted')
    point=world(f,628,78,372,213)
    for lon,lat,tx,ty,label,a in [(-100,38,636,96,'美国 69 · 微软 / PyTorch 基金会','start'),(5,52,995,140,'荷兰 3 · NixOS 基金会','end'),(104,35,995,274,'中国 7 · 开放原子 / 华为','end')]:
        px,py=point(lon,lat);f.circle(px,py,3.1,'violet');f.line(px,py,tx+2 if a=='start' else tx-2,ty-5,'soft',.9)
        w=tw(label,15);f.rect(tx-3 if a=='start' else tx-w-3,ty-17,w+6,23,'white',.95);f.text(tx,ty,label,15,'ink',False,a)
    for i,v in enumerate([1,7,69]):
        xx=632+i*66;f.rect(xx,300,20,11,mix('#EDE6F4','violet',.2+.8*math.sqrt(v/69)));f.text(xx+26,311,v,13.5,'muted')
    f.text(998,311,'项目数 / 国别',13.5,'muted',anchor='end')
    f.wrap(632,337,'按榜表组织标签；含发起方或托管方。\n灰色为未列明，非贡献者所在地。',367,14,'muted',leading=20)
    panel(f,632,393,3,'100 强席位与排名梯次',19.8)
    for i,r in enumerate(G):f.rect(632+(i%10)*16,416+(i//10)*16,13,13,CC[cgroup(r['country'])])
    groups=['美国','中国','荷兰','德国','其他 8 国','未识别'];counts=Counter(cgroup(r['country']) for r in G)
    for i,n in enumerate(groups):
        yy=432+i*27;f.rect(808,yy-12,11,11,CC[n]);f.text(828,yy,n,15.5);f.text(998,yy,counts[n],19,CC[n],True,'end')
    f.text(632,600,'每格 1 项；按全球名次从左至右、逐行排列。',13.4,'muted')
    for x,t in [(632,'国别 / 排名'),(802,'1—10'),(896,'11—30'),(995,'31—100')]:f.text(x,635,t,13.5,'muted',anchor='start' if x==632 else 'end')
    for i,n in enumerate(groups):
        yy=663+i*26;f.text(632,yy,n,15.2,'ink',n=='中国')
        for x,lo,hi in [(802,1,10),(896,11,30),(995,31,100)]:
            v=sum(cgroup(r['country'])==n and lo<=r['rank']<=hi for r in G);f.text(x,yy,v,16,CC[n],True,'end')
    panel(f,0,651,4,'榜内分值结构 · 前十名占三分之一',19.8)
    total=sum(r['openrank'] for r in G);sh=[sum(r['openrank'] for r in G[a:b])/total for a,b in [(0,1),(1,5),(5,10),(10,30),(30,100)]]
    f.text(0,694,f'{sum(sh[:3]):.1%}',34,'violet',True);f.text(150,691,'前 10 名 / 100 强 OpenRank 合计',16,'muted')
    colors=['#554779','#587E80','#A28A45','#8697B0','#CCD3DD'];xx=0
    for v,c in zip(sh,colors):
        f.rect(xx,718,602*v,32,c);f.text(xx+602*v/2,740,f'{v:.1%}',16,'ink' if c==colors[-1] else 'white',False,'middle');xx+=602*v
    for i,(t,c) in enumerate(zip(['第 1 名','第 2—5 名','第 6—10 名','第 11—30 名','第 31—100 名'],colors)):
        xx=i*121;f.rect(xx,775,10,10,c);f.text(xx+15,785,t,12.5,'muted')
    f.save('fig-3-10-project-global')

def fig_china():
    f=Figure();panel(f,0,27,1,'中国项目影响力前 20 位');ranking(f,CN,True);f.line(615,0,615,805)
    panel(f,632,27,2,'七个百强席位的技术层次',19.5)
    f.text(632,58,'全球名次：2 项前十 · 4 项前三十',15,'muted')
    items=[('OpenHarmony',1,'操作系统','teal'),('openEuler',8,'操作系统','teal'),('CANN',13,'AI 计算栈','violet'),('Ascend',15,'AI 计算栈','violet'),('MindSpore',33,'AI 框架','violet'),('PaddlePaddle',37,'AI 框架','violet'),('Cangjie',51,'编程语言','gold')]
    f.text(632,89,'项目',14,'muted');f.text(910,89,'主领域',14,'muted',anchor='end');f.text(998,89,'全球',14,'muted',anchor='end')
    for i,(n,r,tech,c) in enumerate(items):
        yy=120+i*35;f.rect(632,yy-17,3,22,c);logo(f,n,644,yy-16,19);f.text(672,yy,n,15.8);f.text(924,yy,tech,14,c,anchor='end');f.text(998,yy,r,22,c,True,'end')
    f.wrap(632,371,'七席集中于系统、AI 计算与语言；\n应用与工具项目构成下一梯次。',367,15,'muted',leading=23)
    panel(f,632,435,3,'组织承载：头部与专业主体',19)
    orgs=[('华为',6),('开放原子',5),('字节跳动',4),('蚂蚁集团',3),('阿里巴巴',3),('其他 / 未识别',9)]
    f.text(632,466,'中国前 30 名 · 项目数 / 项',15,'muted')
    for i,(n,v) in enumerate(orgs):
        yy=505+i*38;f.text(632,yy,n,16)
        f.rect(762,yy-13,190*v/9,14,'slate' if i==5 else 'violet');f.text(998,yy,v,18,'ink',True,'end')
    f.wrap(632,751,'“其他 / 未识别”含 7 项其他机构、2 项组织未识别；按榜表组织标签汇总。',367,14.5,'muted',leading=22)
    panel(f,0,651,4,'13 / 30：AI 项目覆盖三类关键环节',19.8)
    layers=[('算力与框架','5','CANN、Ascend、MindSpore、PaddlePaddle、FlagOS'),('模型与后训练','4','魔搭、verl、ms-swift、inclusionAI'),('应用与智能体','4','RAGFlow、Coze、AgentScope、DeerFlow')]
    for i,(n,v,examples) in enumerate(layers):
        yy=690+i*47;f.text(0,yy,n,16,'ink',True);f.text(142,yy,v,21,'china',True,'end');f.wrap(162,yy,examples,440,14.6,'muted',leading=20)
    f.save('fig-3-11-project-china')

def domain_counts(scope):return Counter(r['domain'] for r in PURPOSE if r['scope']==scope)
def object_counts(scope):return Counter(r['object_type'].split('（')[0] for r in PURPOSE if r['scope']==scope)
def fig_features():
    f=Figure();f.line(615,0,615,805);f.line(0,405,1000,405)
    panel(f,0,27,1,'技术结构：AI 与基础软件共同在场',19.5)
    f.text(0,58,'按主要用途，每项只归入一类；两榜各 30 项',14.5,'muted')
    for x,n,c in [(325,'全球前 30','violet'),(466,'中国前 30','china')]:f.rect(x,78,11,11,c);f.text(x+17,89,n,14.3,'muted')
    cats=['AI 与机器学习','编程语言与运行时','开发工具与框架','云原生与基础设施','操作系统与硬件','数据与分析','可观测性与安全','企业应用与协作','物联网与边缘'];a,b=domain_counts('global'),domain_counts('china')
    for i,n in enumerate(cats):
        yy=118+i*31;f.text(0,yy+7,n,16)
        for off,co,vs in [(0,'violet',a),(12,'china',b)]:
            v=vs[n];f.rect(190,yy-10+off,v/13*355,9,co);f.text(558,yy-1+off,v,13,co,True,'end')
    f.text(600,393,'项目数 / 项',13.5,'muted',anchor='end')
    panel(f,632,27,2,'组织承载形式的对照',19.6)
    f.wrap(632,58,'按榜表组织名称归类；颜色对应下方两榜。\n横条按各榜项目数量计算占比。',366,14,'muted',leading=21)
    gt=Counter(r['org_type'] for r in G);ct=Counter(r['org_type'] for r in CN)
    for i,n in enumerate(['企业及其他机构','基金会','高校','未识别']):
        yy=116+i*66;f.text(632,yy,n,16,'ink',i==1)
        for dy,num,den,col in [(13,gt[n],100,'violet'),(32,ct[n],30,'china')]:
            f.rect(632,yy+dy,225*num/den,10,col);f.text(998,yy+dy+10,f'{num}/{den} · {num/den:.1%}',13.5,col,anchor='end')
    f.rect(632,389,10,10,'violet');f.text(648,399,'全球 100 强',13,'muted');f.rect(814,389,10,10,'china');f.text(830,399,'中国前 30',13,'muted')
    panel(f,0,441,3,'参与规模与网络影响：两个观察维度',19.4)
    f.text(0,471,'每点 1 项 · 中国 7 项突出显示；两轴均为等比刻度',14,'muted')
    x0,x1,y0,y1=65,590,501,738
    px=lambda v:x0+(math.log10(v)-math.log10(300))/(math.log10(40000)-math.log10(300))*(x1-x0)
    py=lambda v:y1-(math.log10(v)-math.log10(2300))/(math.log10(85000)-math.log10(2300))*(y1-y0)
    for v,lab in [(3000,'3千'),(10000,'1万'),(30000,'3万'),(80000,'8万')]:
        yy=py(v);f.line(x0,yy,x1,yy,'line',.8);f.text(x0-8,yy+5,lab,12.5,'muted',anchor='end')
    for v,lab in [(500,'500'),(2000,'2千'),(10000,'1万'),(30000,'3万')]:
        xx=px(v);f.line(xx,y0,xx,y1,'line',.6);f.text(xx,y1+21,lab,12.5,'muted',anchor='middle')
    for r in sorted(G,key=lambda r:r['country']=='中国'):
        f.circle(px(r['active_developers']),py(r['openrank']),4.2 if r['country']=='中国' else 2.6,'china' if r['country']=='中国' else '#A5B1C5')
    for n,tx,ty,anchor in [('OpenHarmony',368,503,'start'),('PyTorch',255,546,'start'),('VSCode',507,562,'start'),('Claude Code',477,642,'start')]:
        r=next(r for r in G if r['project']==n);xx,yy=px(r['active_developers']),py(r['openrank']);f.line(xx,yy,tx,ty-5,'soft',.8)
        w=tw(n,14.5);f.rect(tx-2,ty-16,w+4,21,'white',.93);f.text(tx,ty,n,14.5,'china' if n=='OpenHarmony' else 'ink',True,anchor)
    f.text(0,493,'OpenRank',12.2,'muted');f.text(600,790,'参与账号数 / 个 · 原榜字段',13.2,'muted',anchor='end')
    panel(f,632,441,4,'“项目”还包含不同聚合层次',18.7)
    f.wrap(632,471,'两榜各 30 项；按对象定义归类。\n横条均以 30 项为分母。',367,14,'muted',leading=21)
    go,co=object_counts('global'),object_counts('china')
    examples={'软件项目':'如 vLLM、verl','项目生态':'如 PyTorch、OpenHarmony','项目集合':'如 Azure、Ascend、魔搭'}
    for i,n in enumerate(['软件项目','项目生态','项目集合']):
        yy=538+i*77;f.text(632,yy,n,16,'ink',True);f.text(998,yy,examples[n],13,'muted',anchor='end')
        for dy,rs,col in [(13,go,'violet'),(32,co,'china')]:
            f.rect(632,yy+dy,278*rs[n]/30,11,col);f.text(998,yy+dy+11,f'{rs[n]} 项',14,col,True,'end')
    f.wrap(632,763,'规模差异须结合仓库范围理解；\n不宜用分值除以人数直接评判效率。',367,14.5,'muted',leading=22)
    f.save('fig-3-12-project-features')

def node(f,x,y,w,h,label,col='violet',fs=16):
    f.rect(x,y,w,h,mix(col,'white',.94));f.line(x,y,x+w,y,col,2);f.text(x+w/2,y+h/2+fs*.34,label,fs,col,True,'middle')
def fig_links():
    f=Figure();f.line(505,0,505,805);f.line(0,405,1000,405)
    panel(f,0,27,1,'六个社区的跨项目参与连接',19.2)
    f.text(0,58,'同月进入两个项目高活跃样本的去重账号数',14.5,'muted')
    names=['PyTorch','vLLM','SGLang','LangChain','Dify','K8s'];repos=['pytorch/pytorch','vllm-project/vllm','sgl-project/sglang','langchain-ai/langchain','langgenius/dify','kubernetes/kubernetes']
    pair=rows('34','accounts_pairwise_intersections.csv');values={frozenset([r['repository_a'],r['repository_b']]):int(r['same_month_unique_accounts']) for r in pair}
    x0,y0,step=126,112,42
    for i,n in enumerate(names):f.text(114,y0+i*step+27,n,14.5,'ink',anchor='end');f.text(x0+i*step+20,98,str(i+1),15,'muted',anchor='middle')
    for i in range(6):
        for j in range(6):
            v=values.get(frozenset([repos[i],repos[j]]),0);fill=mix('white','violet',v/21*.9) if i!=j else '#F1F3F6'
            f.rect(x0+j*step,y0+i*step,39,39,fill);f.text(x0+j*step+19.5,y0+i*step+26,'—' if i==j else v,15,'white' if v>=15 else 'muted' if v==0 or i==j else 'ink',i!=j and v>0,'middle')
    f.text(395,136,'连接较多',14,'muted')
    for i,(pairlabel,v) in enumerate([('vLLM / SGLang',21),('PyTorch / vLLM',16),('LangChain / Dify',15)]):
        yy=176+i*72;f.text(395,yy,v,29,'violet',True);f.wrap(395,yy+22,pairlabel,100,12.8,'muted',leading=18)
    f.text(0,393,'列号与行序一致；K8s 为 Kubernetes。',13.8,'muted')
    panel(f,525,27,2,'高活跃样本中的持续出现',19.2)
    f.text(525,58,'年度样本账号数及其中出现 9—12 月的占比',14.3,'muted')
    cols=['#DDE3ED','#AAB8D1','#8B77B4','#60418F']
    for i,(t,c) in enumerate(zip(['1—2 月','3—5 月','6—8 月','9—12 月'],cols)):
        xx=525+i*118;f.rect(xx,79,10,10,c);f.text(xx+15,90,t,12.7,'muted')
    f.text(525,124,'项目 / 年度样本',13,'muted');f.text(999,124,'9—12 月占比',13,'muted',anchor='end')
    summary=rows('34','accounts_repository_summary.csv')
    for i,r in enumerate(summary):
        yy=158+i*35;total=int(r['annual_unique_logins']);f.text(525,yy,names[i],14.5);f.text(662,yy,total,13,'muted',anchor='end')
        xx=677
        for k,c in zip(['months_1_2','months_3_5','months_6_8','months_9_12'],cols):
            w=int(r[k])/total*235;f.rect(xx,yy-13,w,16,c);xx+=w
        f.text(999,yy,f'{int(r["months_9_12"])/total:.1%}',16,'violet',True,'end')
    f.wrap(525,373,'每仓每月至多 100 个公开账号，经机器人过滤；\n这些占比描述样本持续出现，不是整体留存率。',474,13.6,'muted',leading=20)
    panel(f,0,442,3,'verl：把训练与生成引擎连接起来',18.5)
    f.wrap(0,473,'字节跳动发起 · 中国榜第 12；后训练指模型初步训练后进一步改善回答与任务能力。',480,14.4,'muted',leading=22)
    f.text(68,540,'训练引擎',15,'ink',True,'middle');f.text(421,540,'生成引擎',15,'ink',True,'middle')
    for i,(l,r) in enumerate(zip(['FSDP','FSDP2','Megatron-LM'],['vLLM','SGLang','Transformers'])):
        yy=560+i*44;f.line(135,yy+17,187,621,'soft',1.2);f.line(295,621,352,yy+17,'soft',1.2);node(f,0,yy,135,34,l,'blue',14.5);node(f,352,yy,135,34,r,'violet',14.5)
    node(f,187,598,108,47,'verl','china',23)
    f.text(241,672,'组织后训练流程',13,'china',False,'middle')
    f.text(0,715,'模型入口',14.5,'ink',True);f.wrap(88,715,'Qwen、Llama、Gemma、DeepSeek',395,14.5,'muted',leading=20)
    f.text(0,748,'硬件入口',14.5,'ink',True);f.text(88,748,'NVIDIA、AMD、昇腾',14.5,'muted')
    f.wrap(0,784,'为文档明确列举的支持项；具体引擎与硬件组合各有条件。',485,13.4,'muted',leading=18)
    panel(f,525,442,4,'昇腾：用适配层接入 PyTorch',19)
    f.wrap(525,473,'torch_npu 将昇腾接入 PyTorch；NPU 指用于\n神经网络计算的处理器。',474,14.4,'muted',leading=22)
    for xx,label,col in [(525,'CANN','china'),(693,'torch_npu','violet'),(861,'PyTorch','blue')]:node(f,xx,527,138,40,label,col,17)
    for x in [665,833]:f.path([(x,547),(x+24,547)],'soft',1.5);f.path([(x+19,542),(x+24,547),(x+19,552)],'soft',1.5)
    f.text(525,597,'CANN 9.0.0 对应的四组版本记录',15.5,'ink',True)
    f.text(535,632,'PyTorch',14,'muted');f.text(797,632,'torch_npu',14,'muted');f.line(525,641,999,641)
    for i,(pt,nu) in enumerate([('2.10.0','2.10.0'),('2.9.0','2.9.0.post2'),('2.8.0','2.8.0.post4'),('2.7.1','2.7.1.post4')]):
        yy=666+i*27
        if i%2==0:f.rect(525,yy-18,474,27,'pale')
        f.text(535,yy,pt,16);f.text(797,yy,nu,16)
    f.text(525,784,'官方 README 固定版本：2026-06-16。',13.7,'muted')
    f.save('fig-3-13-project-connections')

SOURCES=[
 {'id':'P1','label':'全球项目百强榜（固定报告数据）','url':'https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/c51e3441361407b68f10b339d97eff288319b503/figures/chapter3/leaderboards/projects.html'},
 {'id':'P2','label':'中国项目前 30 名（固定报告数据）','url':BASE+'table-3-4-3_china_project_openrank_top30.csv'},
 {'id':'P3','label':'OpenDigger 指标实现与主统计期数据库复算','url':'https://github.com/X-lab2017/open-digger/blob/5c2ffc4f5b3dd37ebcb20514c7abfee6853bd830/src/metrics/indices.ts'},
 {'id':'P4','label':'六仓库月度高活跃账号样本及可复算方法','url':'https://oss.open-digger.cn/github/pytorch/pytorch/activity_details.json'},
 {'id':'P5','label':'verl 官方 README，2026-05-29 固定版本','url':'https://github.com/verl-project/verl/blob/38b57931f0c4f4da1ff85a7d54c2d8bbc239163d/README.md'},
 {'id':'P6','label':'Ascend Extension for PyTorch，2026-06-16 固定版本','url':'https://github.com/Ascend/pytorch/blob/554f7cd18e52dc2f94a5715c100b7d15b7b65de0/README.md'},
 {'id':'P7','label':'项目用途及对象分类：项目官方文档逐项映射','items':[{'scope':r['scope'],'project':r['project'],'url':r['evidence']} for r in PURPOSE]}
]
def render():
    fig_global();fig_china();fig_features();fig_links()
    pages=[
      page('3.4','3.4 全球开源项目影响力排行榜','项目把组织投入转化为可使用、可维护的公共资源。OpenRank 衡量协作网络中的影响；结合组织国别、参与规模与技术用途，才能看清头部项目的结构及其连接方式。','fig-3-10-project-global','图 3-10　全球前 20 名、百强组织国别与榜内分值结构。来源：报告项目榜［P1］；OpenDigger 主统计期复算［P3］。OpenRank 为 2025.07—2026.06；组织国别沿用榜表标签，不代表贡献者来源。参与账号及对象边界说明见附录 1。',[
       ('① 头部项目横跨系统、语言与 AI','OpenHarmony、Azure、C#/.Net、PyTorch 与 NixOS 位居前五。AI 框架和推理工具已进入头部，但操作系统、语言与云基础设施仍占据重要位置。人工智能的开放发展，需要多层基础软件共同支撑。'),
       ('② 组织分布集中，协作边界跨越国别','百强中，美国标签占 69 项，中国占 7 项，荷兰与德国各 3 项；9 项国别未识别。组织标签适合观察项目承载布局，贡献者却可能来自全球。识别开放协作能力，还须连接项目参与和复用证据。'),
       ('③ 中国席位体现系统与 AI 计算支点','中国 7 个席位中，2 项进入前十、4 项进入前三十，其余位于第 33、37 和 51 位。席位数量与高位节点共同呈现结构位置；据此可以识别合作资源，但不能推导中国对全体全球项目的贡献份额。'),
       ('④ 影响分布既有头部，也有较宽支撑层','前十名占百强 OpenRank 合计的 33.6%，第 31—100 名合计占 38.7%。公共能力既依托高影响节点，也需要较广的项目支撑层。面向产业与政策的资源配置，应兼顾关键项目与专业维护团队。')],SOURCES[:3],['I01','I02','I10']),
      page('3.4','3.4.1 中国项目：从系统支点到 AI 工具','中国项目榜呈现系统底座、AI 计算、模型工具与应用框架的分层布局。全球位置说明哪些项目已进入头部网络，中国榜的技术与组织结构则展示后续协作资源从哪里形成。','fig-3-11-project-china','图 3-11　中国前 20 名、全球百强席位、组织承载与 AI 项目分层。来源：报告榜表［P1］［P2］、OpenDigger 复算［P3］及项目官方文档分类［P7］。全球名次来自同一统计期项目标签榜；技术分层为编辑分类，不将项目分值跨层加总。',[
       ('① 头部之外，专业项目已形成梯次','前七名进入全球百强；Ant Design、openGauss、魔搭、TiDB、verl 等构成其后的专业项目层。榜单不仅用于确认领先者，也可帮助识别设计工具、数据库、模型服务和训练流程中的合作入口。'),
       ('② 七个高位节点覆盖三类基础能力','OpenHarmony 与 openEuler 代表操作系统，CANN、Ascend、MindSpore 与 PaddlePaddle 涉及 AI 计算或框架，Cangjie 对应编程语言。这些资源连接应用运行、模型计算与开发过程，体现多层供给。'),
       ('③ 企业与基金会承担不同组织角色','中国前 30 名中，华为标签对应 6 项，开放原子对应 5 项，字节跳动对应 4 项。企业持续投入与基金会承载共同构成项目发展的组织条件；具体治理开放性仍应考察维护权、决策机制及外部参与。'),
       ('④ AI 供给已延伸到训练与应用流程','按主要用途归类，AI 项目占中国前 30 名的 13 项，覆盖算力与框架、模型与后训练、应用与智能体。中国贡献的观察应从模型发布延伸到这些环节，进一步追踪接口兼容、跨项目采用与持续维护。')],SOURCES[:3]+[SOURCES[-1]],['I05','I09','I10']),
      page('3.4','3.4.2 头部特征：技术、组织与协作规模','同样进入排行榜的项目，承担的技术任务、组织方式和聚合范围可能不同。将这些维度并置，可以辨认 AI 时代的结构位置，也有助于避免把“参与者更多”直接等同于“影响更大”。','fig-3-12-project-features','图 3-12　技术用途、组织承载、参与规模与对象层次。来源：榜表［P1］［P2］和项目官方文档分类［P7］。技术与对象对照各取前 30 名；组织对照为全球百强与中国前 30 名；散点为全球百强。分类逐项保留证据，见附录 1。',[
       ('① AI 的突出位置须放回全栈结构理解','全球前 30 名中，AI 与机器学习类有 8 项，中国前 30 名中有 13 项。全球榜同时包含语言、云基础设施、开发工具和系统项目。两榜技术结构不同，提示产业需要将 AI 投入与基础软件维护相互衔接。'),
       ('② 公共承载结构是体系能力的一部分','全球百强中，22 项组织标签指向基金会，4 项指向高校；中国前 30 名中，5 项指向基金会。企业之外的这些载体，为跨组织接续提供制度入口。它们是否形成开放治理，仍须以项目制度与执行记录判断。'),
       ('③ 参与规模与协作网络影响并不同步','Claude Code 的参与账号字段为 32,814，OpenRank 名次为第 25；PyTorch 为 4,806，名次为第 4。二者说明参与规模与网络影响观察的是不同方面。解释差异需回到协作行为与对象范围，不能据此评价效率。'),
       ('④ 聚合层次决定比较需要补充什么','全球前 30 名包括 5 个软件项目、18 个项目生态与 7 个项目集合；中国分别为 9、17 和 4。集合可能覆盖多个仓库，单一软件则边界较窄。深入评价应固定仓库清单，进一步比较维护、复用及治理能力。')],SOURCES[:2]+[SOURCES[-1]],['I02','I05','I09','I10','I11']),
      page('3.4','3.4.3 全球协作：中国项目如何接入与再创造','榜单给出位置，跨项目证据则说明连接怎样发生。共同参与账号揭示人员接点；工具接口与版本适配展示可使用的连接方式。中国贡献也应在这些可核验的接续与再创造中得到理解。','fig-3-13-project-connections','图 3-13　跨仓库参与、样本持续出现及中国项目接口案例。来源：OpenDigger 月度账号样本［P4］、verl［P5］、昇腾 PyTorch 扩展［P6］。账号窗为 2025.07—2026.06；两个文档版本均在主统计期内。接口支持不等于实际采用规模，详见附录 1。',[
       ('① 开放生态存在跨项目的人员接点','六个仓库的月度高活跃样本中，vLLM 与 SGLang 有 21 个同月重叠账号，PyTorch 与 vLLM 有 16 个。共同账号提供了继续研究协作网络的入口；它本身不证明正式合作、人才迁移或贡献者的国别。'),
       ('② 持续协作需要单独观察','在年度样本中，PyTorch 有 36 个账号在 9—12 个月出现，占 9.8%；Kubernetes 为 30 个，占 7.0%。一次性参与与持续出现并存。公共能力建设应跟踪长期维护，但这里的截断样本不能替代全量留存分析。'),
       ('③ 中国后训练工具在全球技术栈上再创造','verl 将训练引擎与生成引擎组织进后训练流程，官方文档列出 FSDP、Megatron-LM、vLLM 和 SGLang 等接口。其价值体现在承接已有资源并形成可组合工具，使中国项目成为全球技术网络中的连接节点。'),
       ('④ 兼容维护把本土算力接入全球框架','torch_npu 将昇腾与 PyTorch 连接起来，版本表列出 CANN 9.0.0 对应的四组配套记录。这样的接口与维护工作构成具体公共资源。后续评价可进一步跟踪兼容测试、使用成本、本地化部署与维护结果。')],SOURCES[3:6],['I02','I03','I05','I11'])
    ]
    save_pages('34',pages)
    checks={'version':'v0.2','country_counts':dict(COUNTS),'global_org_counts':dict(Counter(r['org_type'] for r in G)),'china_org_counts':dict(Counter(r['org_type'] for r in CN)),'tech_global30':dict(domain_counts('global')),'tech_china30':dict(domain_counts('china')),'objects_global30':dict(object_counts('global')),'objects_china30':dict(object_counts('china')),'top10_score_share':sum(r['openrank'] for r in G[:10])/sum(r['openrank'] for r in G),'rank31to100_score_share':sum(r['openrank'] for r in G[30:])/sum(r['openrank'] for r in G),'china_global_ranks':{r['project']:r['global_rank'] for r in CN},'no_simulated_values':True}
    (R/'review/data-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2));return pages
