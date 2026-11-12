"""Data-driven complete landscapes and evidence compositions; GOSD 4.1 v0.2."""
from common import *
DATA=json.loads((R/'source/analysis/data.json').read_text())
CLASS=json.loads((D/'classification.json').read_text())
PROJECTS={p['repo']:p for p in DATA['projects']}
NAMES={p['repo']:p['name'] for p in CLASS['PROJECTS']}
CATS={c['id']:c for c in DATA['categories']}
ASSETS={a['repo_name']:a for a in json.loads((R/'source/assets/project_asset_mapping.json').read_text())}
SELECTED=[];CELL_QA=[]
C.update(teal_light='#E1F1ED',blue_light='#E4EEF8',teal_mid='#72ACA2',frame='#527778')
SHORT={'Coding workflows & harnesses':'编码工作流与工具链','Multi-agent orchestration':'多智能体编排','Workflow & agent builders':'工作流构建','Code-first frameworks':'代码框架','Memory, knowledge & context':'记忆与知识','Protocols & interoperability':'协议互操作','Tools, web & computer use':'工具与计算机操作','Pre-Train · Framework & parallel':'训练框架与并行','Pre-Train · Compiler & accelerator':'编译与加速','Post-Train · RL & environments':'强化学习与环境','Pre-Train · Evaluation & observability':'训练评估与观测'}
def cn(key):return SHORT.get(key,CATS[key]['name_zh'])
def avatar(f,repo,x,y,size=23):
    a=ASSETS.get(repo)
    if a and (R/'source/assets'/a['asset_relative_path']).is_file():img(f,R/'source/assets'/a['asset_relative_path'],x,y,size,size)
    else:
        f.circle(x+size/2,y+size/2,size/2,'soft');f.text(x+size/2,y+size*.72,NAMES[repo][0],size*.7,'white',True,'middle')
def badge(f,x,y,n,t,color='teal',fs=22):f.title(x,y,str(n),t,color,fs)
def rounded(f,x,y,w,h,stroke='frame',fill='white',radius=9,sw=1.8):
    f.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{cl(fill)}" stroke="{cl(stroke)}" stroke-width="{sw}"/>')
def frame(f,x,y,w,h,n,title,color='teal'):
    rounded(f,x,y,w,h,color)
    rounded(f,x+12,y-15,tw(title,21,True)+53,31,color,'teal_light' if color=='teal' else 'blue_light',5,0)
    badge(f,x+18,y+7,n,title,color,21)
def subhead(f,x,y,title,count=None,color='teal',fs=18.5):
    f.text(x,y,title,fs,color,True)
    if count is not None:
        aliases={c['name_zh']:c['id'] for c in CATS.values()}
        aliases.update({v:k for k,v in SHORT.items()});aliases['工作流与智能体构建']='Workflow & agent builders'
        key=aliases[title];count=sum(p['section']==key for p in CLASS['PROJECTS'])
        f.text(x+tw(title,fs,True)+9,y,str(count)+' 项',15,'muted')
def split_name(name,maxw,fs):
    if tw(name,fs,True)<=maxw:return [name]
    words=name.split(' ')
    if len(words)==1 and '-' in name:words=[x+('-' if i<len(name.split('-'))-1 else '') for i,x in enumerate(name.split('-'))]
    lines=[];line=''
    for word in words:
        sep='' if line.endswith('-') else ' ';add=word if not line else line+sep+word
        if line and tw(add,fs,True)>maxw:lines.append(line);line=word
        else:line=add
    if line:lines.append(line)
    return lines
def grid(f,key,x,y,w,cols,rowh=32,fs=18.5,icon=23):
    ps=[p for p in CLASS['PROJECTS'] if p['section']==key];gap=10;cw=(w-(cols-1)*gap)/cols
    for i,p in enumerate(ps):
        xx=x+(i%cols)*(cw+gap);yy=y+(i//cols)*rowh;missing=PROJECTS[p['repo']]['trend'][-1] is None
        name=p['name']+('†' if missing else '');size=fs;maxw=cw-icon-7;lines=split_name(name,maxw,size)
        while (max(tw(z,size,True) for z in lines)>maxw or len(lines)>2 or len(lines)*(size+.5)>rowh) and size>16.4:
            size-=.2;lines=split_name(name,maxw,size)
        totalh=len(lines)*(size+.5);avatar(f,p['repo'],xx,yy+(rowh-icon)/2,icon);base=yy+(rowh-totalh)/2+size*.85
        for j,line in enumerate(lines):f.text(xx+icon+7,base+j*(size+.5),line,size,'ink',True)
        CELL_QA.append({'repo':p['repo'],'category':key,'font_px':round(size,2),'lines':lines,'cell':[xx,yy,cw,rowh],'overflow':max(tw(z,size,True) for z in lines)>maxw+.1 or totalh>rowh+1})
        SELECTED.append({'repo':p['repo'],'name':p['name'],'layer':p['layer'],'category':key,'june_observed':not missing})
def atlas_agent():
    ps=[p for p in CLASS['PROJECTS'] if p['layer']=='Agent Infra']
    f=Figure(900);f.text(0,26,'Agent Infra Landscape',28,'teal',True);f.text(1000,24,f"智能体基础设施  ·  {len({p['section'] for p in ps})} 类 / {len(ps)} 项",19,'muted',anchor='end')
    frame(f,1,56,642,284,1,'编码与执行工作流');subhead(f,14,87,'编码代理',16)
    grid(f,'Agentic coding',14,99,616,4,35,18,22)
    f.line(2,244,642,244,'soft',1.2,'5 4');subhead(f,14,266,'编码工作流与工具链',7)
    grid(f,'Coding workflows & harnesses',14,271,616,4,34.5,17,20)
    frame(f,662,56,337,172,2,'个人助手');grid(f,'Personal AI assistants',676,79,310,2,35,18.5,24)
    rounded(f,662,252,337,88,'teal');subhead(f,676,275,'聊天工作区',3);grid(f,'Chatbot workspaces',676,282,310,2,25,17,21)
    frame(f,1,371,998,226,3,'构建与编排');f.line(500,372,500,469,'soft',1.2,'5 4')
    subhead(f,14,403,'多智能体编排',5);subhead(f,515,403,'工作流与智能体构建',5)
    grid(f,'Multi-agent orchestration',14,415,471,3,25,18,22);grid(f,'Workflow & agent builders',515,415,470,3,25,18,22)
    f.line(2,477,998,477,'soft',1.2,'5 4');subhead(f,14,501,'代码优先框架',11);grid(f,'Code-first frameworks',14,510,972,3,21.5,17.7,20)
    frame(f,1,629,998,269,4,'知识、接口与运行保障')
    f.line(350,630,350,790,'soft',1.2,'5 4');f.line(700,630,700,790,'soft',1.2,'5 4')
    subhead(f,14,657,'记忆、知识与上下文',9,fs=18);subhead(f,363,657,'协议与互操作',8,fs=18);subhead(f,714,657,'工具与计算机操作',6,fs=18)
    grid(f,'Memory, knowledge & context',14,667,322,2,24,17,21);grid(f,'Protocols & interoperability',363,663,322,2,34,16.5,21);grid(f,'Tools, web & computer use',714,669,271,2,35,16.7,20)
    f.line(2,801,998,801,'soft',1.2,'5 4');f.line(500,801,500,898,'soft',1.2,'5 4');subhead(f,14,823,'开发沙箱',5);subhead(f,515,823,'可观测与评估',4)
    grid(f,'Development sandboxes',14,835,471,3,27,17,21);grid(f,'Observability & evaluation',515,835,470,2,27,18,22)
    f.save('4-1-1-agent-atlas')
def atlas_model():
    ps=[p for p in CLASS['PROJECTS'] if p['layer']=='Model Infra']
    f=Figure(900);f.text(0,26,'Model Infra Landscape',28,'blue',True);f.text(1000,24,f"模型基础设施  ·  {len({p['section'] for p in ps})} 类 / {len(ps)} 项",19,'muted',anchor='end')
    frame(f,1,56,998,194,1,'模型服务：从调用入口到运行引擎','blue')
    for x in [275,550]:f.line(x,57,x,250,'soft',1.2,'5 4')
    subhead(f,15,90,'模型 API 网关',4,'blue');subhead(f,289,90,'服务部署',3,'blue');subhead(f,564,90,'推理引擎',8,'blue')
    grid(f,'Model API gateways',15,104,246,1,33,21,26);grid(f,'Serving · Deploy',289,105,246,1,44,21,27);grid(f,'Serving · Inference',564,104,421,2,34,19.5,25)
    frame(f,1,282,998,264,2,'训练与适配：把通用能力转为任务能力','blue')
    for x in [335,610]:f.line(x,283,x,438,'soft',1.2,'5 4')
    subhead(f,15,316,'强化学习与环境',6,'blue');subhead(f,349,316,'监督微调',3,'blue');subhead(f,624,316,'训练框架与并行',6,'blue')
    grid(f,'Post-Train · RL & environments',15,330,306,2,33,19,25);grid(f,'Post-Train · Supervised fine-tuning',349,330,247,1,33,20,25);grid(f,'Pre-Train · Framework & parallel',624,330,361,2,33,19,24)
    f.line(2,440,998,440,'soft',1.2,'5 4');f.line(500,440,500,546,'soft',1.2,'5 4');subhead(f,15,468,'训练评估与观测',2,'blue');subhead(f,515,468,'机器人基础设施',2,'blue')
    grid(f,'Pre-Train · Evaluation & observability',15,488,470,2,38,21,27);grid(f,'Pre-Train · Robotics infra',515,488,470,2,38,21,27)
    frame(f,1,578,998,160,3,'数据基础：准备、流转与治理','blue')
    for x in [240,535]:f.line(x,579,x,738,'soft',1.2,'5 4')
    subhead(f,15,610,'数据标注',2,'blue');subhead(f,254,610,'数据集成',4,'blue');subhead(f,549,610,'数据治理',7,'blue')
    grid(f,'Data · Labeling',15,630,210,1,39,20,25);grid(f,'Data · Integration',254,624,267,1,26,19,23);grid(f,'Data · Governance',549,624,436,2,26,18.5,23)
    frame(f,1,770,998,128,4,'计算基础：连接算法、硬件与资源','blue');f.line(663,771,663,898,'soft',1.2,'5 4')
    subhead(f,15,802,'编译器与加速',8,'blue');subhead(f,677,802,'计算与调度',4,'blue')
    grid(f,'Pre-Train · Compiler & accelerator',15,813,633,4,38,17.5,22);grid(f,'Compute & scheduling',677,816,308,2,34,18,24)
    f.save('4-1-2-model-atlas')

RANKS=json.loads((D/'43/rankings.json').read_text())
PUBLIC=json.loads((D/'43/country-public-subset.json').read_text())
TOTAL=sum(p['score'] for p in RANKS)
RANKS=sorted(RANKS,key=lambda p:-p['score'])
RANK_CATS=[]
for key,c in CATS.items():
    ps=[p for p in RANKS if p['section']==key]
    RANK_CATS.append({'id':key,'layer':c['layer'],'score':sum(p['score'] for p in ps),'n':len(ps),'observed':sum(p['months']>0 for p in ps)})
RANK_CATS.sort(key=lambda p:-p['score'])

def fitted(f,x,y,text,maxw,fs=17,c='ink',bold=False,anchor='start',minfs=15.3):
    while tw(text,fs,bold)>maxw and fs>minfs:fs-=.1
    assert tw(text,fs,bold)<=maxw+.8,(text,tw(text,fs,bold),maxw)
    f.text(x,y,text,fs,c,bold,anchor)

def ranking_table(f,x,title,number,items,color=None):
    badge(f,x,25,number,title,color or 'teal',19.4)
    f.text(x,53,'项目 / 主要仓库',15,'muted');f.text(x+316,53,'累计 OpenRank',14.5,'muted',anchor='end')
    top=items[:20];maxscore=top[0]['score']
    for i,p in enumerate(top):
        y=80+i*23.7;col=color or ('teal' if p['layer']=='Agent Infra' else 'blue')
        if i%2==0:f.rect(x,y-18,316,23.7,'pale')
        f.text(x+1,y,f'{i+1:02}',14.6,'muted');avatar(f,p['repo'],x+25,y-16.5,18)
        fitted(f,x+50,y,p['name'],189,16.5,'ink',i<3)
        f.text(x+315,y,fmt(p['score'],1),16.2,col,i<3,'end')
        f.rect(x+50,y+3,182*p['score']/maxscore,1.5,col,.32)

def rankings():
    f=Figure(900)
    ranking_table(f,0,'Agent Infra 前 20',1,[p for p in RANKS if p['layer']=='Agent Infra'],'teal')
    ranking_table(f,342,'Model Infra 前 20',2,[p for p in RANKS if p['layer']=='Model Infra'],'blue')
    ranking_table(f,684,'全景项目前 20',3,RANKS)
    f.line(328,0,328,543);f.line(670,0,670,543)
    f.rect(0,551,1000,37,'pale')
    f.text(12,576,'Agent Infra 52.3%  /  Model Infra 47.7%',19,'teal',True)
    f.text(988,576,'143 项有主期记录 · 前 20 项合计占 51.6%',17.8,'muted',anchor='end')
    badge(f,0,621,4,'全部 25 个子类：聚合类内项目影响力',fs=21)
    f.rect(732,607,12,12,'teal');f.text(751,621,'Agent',16,'muted');f.rect(829,607,12,12,'blue');f.text(848,621,'Model',16,'muted')
    for side in range(2):
        x=side*514;f.text(x,647,'子类',15,'muted');f.text(x+352,647,'OpenRank',14.2,'muted',anchor='end');f.text(x+427,647,'全景份额',14.2,'muted',anchor='end');f.text(x+486,647,'项目数',14.2,'muted',anchor='end')
        for j,c in enumerate(RANK_CATS[side*13:(side+1)*13]):
            i=side*13+j;y=666+j*19;co='teal' if c['layer']=='Agent Infra' else 'blue'
            if j%2==0:f.rect(x,y-14.5,486,19,'pale')
            f.text(x,y,f'{i+1:02}',13.8,'muted');fitted(f,x+25,y,cn(c['id']),164,15.6)
            f.rect(x+195,y-10,72*c['score']/RANK_CATS[0]['score'],10,co,.8)
            f.text(x+352,y,fmt(c['score'],1),15.3,co,False,'end')
            f.text(x+427,y,f'{c["score"]/TOTAL*100:.1f}%',15.3,anchor='end');f.text(x+486,y,str(c['n']),15.3,'muted',anchor='end')
    f.save('4-1-3-rankings')

def country_color(name):return 'china' if name=='中国' else 'blue' if name=='美国' else 'teal'
def countries():
    f=Figure(900)
    f.rect(0,0,1000,41,'pale');f.text(13,27,'期后公开样本：96 项关联标签 / 24 个子类；尚非 145 项全景的年度国家榜',18.6,'china',True)
    badge(f,0,80,1,'样本总榜 · 前 15',fs=21);f.text(0,107,'国家 / 地区',15.6,'muted');f.text(281,107,'贡献分值',15.2,'muted',anchor='end');f.text(390,107,'样本内份额',15.2,'muted',anchor='end')
    for i,r in enumerate(PUBLIC['total']['countries'][:15]):
        y=134+i*24;co=country_color(r['name'])
        if i%2==0:f.rect(0,y-18,391,24,'pale')
        f.text(0,y,f'{i+1:02}',14.3,'muted');f.text(28,y,r['name'],16.6,co,i<2)
        f.rect(112,y-10,80*r['share_known']/PUBLIC['total']['countries'][0]['share_known'],10,co,.7)
        f.text(281,y,fmt(r['score'],1),16.1,co,False,'end');f.text(390,y,f'{r["share_known"]:.1f}%',16.2,co,i<2,'end')
    f.line(407,57,407,496)
    badge(f,430,80,2,'两大类分别排名 · 各前 10',fs=21)
    for k,layer in enumerate(['Agent Infra','Model Infra']):
        x=430+292*k;group=PUBLIC['layers'][layer];co='teal' if k==0 else 'blue'
        f.text(x,117,layer,20,co,True);f.text(x,143,f'{group["label_n"]} 项标签 · 已识别地域贡献',15.4,'muted')
        for i,r in enumerate(group['countries'][:10]):
            y=176+i*30;col=country_color(r['name'])
            if i%2==0:f.rect(x,y-18,278,30,'pale')
            f.text(x,y,f'{i+1:02}',14.1,'muted');f.text(x+28,y,r['name'],16.3,col,i<2);f.text(x+277,y,f'{r["share_known"]:.1f}%',17,col,i<2,'end')
            f.rect(x+28,y+6,210*r['share_known']/50,2,col,.55)
    f.text(0,510,'份额分母均为相应样本中已识别地域的贡献；未识别部分未包含在公开文件中。',16.9,'muted')
    f.text(0,536,'未覆盖 49 项，包括 PyTorch、OpenClaw、vLLM 等；不能据此认定全景整体领先地位。',16.9,'china')
    f.line(0,551,1000,551)
    badge(f,0,585,3,'细分类别：各类前三位及份额',fs=21)
    f.text(1000,585,'括号：标签数；份额取整',16,'muted',anchor='end')
    catgroups=[[p['id'] for p in DATA['categories'] if p['layer']==l and PUBLIC['categories'][p['id']]['countries']] for l in ['Agent Infra','Model Infra']]
    for side,keys in enumerate(catgroups):
        x=side*514
        f.text(x,616,'Agent Infra 子类' if side==0 else 'Model Infra 子类',16.5,'teal' if side==0 else 'blue',True)
        for xx,t in [(x+175,'第 1 位'),(x+280,'第 2 位'),(x+385,'第 3 位')]:f.text(xx,616,t,14.5,'muted')
        for i,key in enumerate(keys):
            g=PUBLIC['categories'][key];y=644+i*20.5
            if i%2==0:f.rect(x,y-15,486,20.5,'pale')
            label=('编码工作流' if key=='Coding workflows & harnesses' else cn(key))+' ('+str(g['label_n'])+')';fitted(f,x,y,label,169,16,minfs=15.6)
            if not g['countries']:f.text(x+175,y,'—  尚无可比标签',15,'muted');continue
            for j,r in enumerate(g['countries'][:3]):
                txt=r['name']+' '+f'{r["share_known"]:.0f}%';fitted(f,x+175+j*105,y,txt,103 if j<2 else 101,16.0,country_color(r['name']),j==0,minfs=13.5)
    f.save('4-1-4-country-rankings')

def render():
    atlas_agent();atlas_model();rankings();countries()
    assert len(SELECTED)==145 and len({p['repo'] for p in SELECTED})==145
    (D/'atlas-selection.json').write_text(json.dumps(SELECTED,ensure_ascii=False,indent=2));(R/'review/cell-qa.json').write_text(json.dumps(CELL_QA,ensure_ascii=False,indent=2))
    return json.loads((D/'content-v03.json').read_text())
