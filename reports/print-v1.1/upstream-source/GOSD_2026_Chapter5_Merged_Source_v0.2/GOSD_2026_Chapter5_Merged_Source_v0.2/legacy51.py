"""Three-page section 5.1: frozen supply, publishers, and China structure."""
from common import *
D=R/'inputs/51/data'
import re

S=json.loads((D/'supply-observation.json').read_text())
A=list(csv.DictReader((D/'annual.csv').open()))
P=S['organizationProfiles']
G=json.loads((D/'map-geometry.json').read_text())
PM={r['id']:r['source_code'] for r in json.loads((D/'province-mapping.json').read_text())}
SOURCE='https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/c51e3441361407b68f10b339d97eff288319b503/'
def src(i,suffix):return {'id':str(i),'url':SOURCE+suffix}
def sources():return [src(1,'data/processed/chapter5/fig-5-1-1_hf_cumulative_models_publishers.csv'),src(2,'preview/content/gosm/supply-observation.json')]
def strip(f,items):
    f.rect(0,0,1000,74,'pale')
    for i,(v,t) in enumerate(items):
        x=18+250*i
        if i:f.line(x-18,14,x-18,60)
        f.text(x,38,v,29,'teal',True);f.text(x,61,t,17,'muted')
def head(f,x,y,n,t):f.title(x,y,str(n),t,'teal',21)
def foot(f,x,y,t,w=470):return f.wrap(x,y,t,w,17,'muted',leading=24)
def annual_plot(f,x,key,maximum,color):
    x0=x+48;x1=x+443;top=214;bottom=380
    for val in [0,maximum/2,maximum]:
        yy=bottom-(bottom-top)*val/maximum;f.line(x0,yy,x1,yy);f.text(x0-8,yy+5,fmt(val,0),16,'muted',anchor='end')
    vals=[int(r[key])/1e4 for r in A];pts=[(x0+i*(x1-x0)/4,bottom-(bottom-top)*v/maximum) for i,v in enumerate(vals)]
    f.path([(x0,bottom)]+pts+[(x1,bottom)],color,0,fill=color,opacity=.07)
    f.path(pts,color,3)
    for i,((px,py),v) in enumerate(zip(pts,vals)):
        f.circle(px,py,4,color);f.text(px,py-12,f'{v:.1f}',17,color,True,'middle')
        f.text(px,405,A[i]['date'][:4],17,'muted',anchor='middle')

def monthly_plot(f,x,asset,color):
    vals=[r for r in S['global'][asset]['monthlyNew'] if '2024-07'<=r['month']<='2026-06']
    assert len(vals)==24
    x0=x+48;x1=x+443;top=575;bottom=735;maximum=15
    # same vertical scale, same calendar; each point remains a monthly source record
    xx=lambda i:x0+i*(x1-x0)/23
    f.rect((xx(11)+xx(12))/2,top,x1-(xx(11)+xx(12))/2,bottom-top,'pale')
    f.text((xx(12)+x1)/2,563,'主统计期',16,'teal',True,'middle')
    for v in [0,5,10,15]:
        y=bottom-(bottom-top)*v/maximum;f.line(x0,y,x1,y);f.text(x0-8,y+5,str(v),16,'muted',anchor='end')
    pts=[(xx(i),bottom-(bottom-top)*(v['count']/1e4)/maximum) for i,v in enumerate(vals)]
    f.path(pts,color,2.8)
    for px,py in pts:f.circle(px,py,2.4,color)
    peak=max(range(len(vals)),key=lambda i:vals[i]['count'])
    main_peak=max(range(12,len(vals)),key=lambda i:vals[i]['count'])
    for k in sorted({peak,main_peak}):
        px,py=pts[k]
        f.text(px,py-12,f"{vals[k]['count']/1e4:.2f}",17,color,True,'middle')
    for i,t in [(0,'2024.7'),(6,'2025.1'),(12,'2025.7'),(18,'2026.1'),(23,'6 月')]:f.text(xx(i),761,t,16,'muted',anchor='middle')
    f.text(x+48,793,'月度新增记录 / 万个；同一纵轴尺度',16,'muted')

def supply_page():
    f=Figure();strip(f,[('306.22 万','模型仓库 · 2026.9.13 回溯点'),('61.33 万','发布账号 · 含个人与组织'),('+58.3%','模型仓库 · 最近同日一年'),('+48.4%','发布账号 · 最近同日一年')])
    f.line(500,96,500,417);f.line(0,435,1000,435);f.line(500,455,500,795)
    head(f,0,111,1,'模型仓库的积累');head(f,525,111,2,'发布账号同步扩大')
    f.text(0,151,'+112.73 万个',27,'blue',True);f.text(525,151,'+20.01 万个',27,'violet',True)
    foot(f,0,180,'2025.9.13 → 2026.9.13 · 仓库数 / 万个');foot(f,525,180,'2025.9.13 → 2026.9.13 · 账号数 / 万个')
    annual_plot(f,0,'models',350,'blue');annual_plot(f,525,'publishers',70,'violet')
    head(f,0,473,3,'模型发布：持续供给伴随波动');head(f,525,473,4,'数据发布：另一条积累曲线')
    f.text(0,513,'主统计期高点 12.42 万个',21,'blue',True);f.text(525,513,'主统计期高点 7.40 万个',21,'teal',True)
    monthly_plot(f,0,'models','blue');monthly_plot(f,525,'datasets','teal')
    f.save('fig-5-1-1')
    return page('5.1','5.1　供给与贡献','Hugging Face（HF）汇集文本、图像、语音等模型的公开仓库。本节观察资源积累与发布账号，并识别模型与数据的主要供给者。','fig-5-1-1',
        '图 5-1-1　模型、发布账号与数据的供给节奏。来源：HF 仓库年度回溯数据［1］、OpenGauge 观测快照［2］。上部为期后观察，据 2026.9.13 可见仓库回看各年同日，纵轴独立；下部突出主统计期 2025.7—2026.6，两组序列不拼接。',
        [('① 模型增长首先意味着选择增加','最近两个回溯点之间，模型仓库增加 112.73 万个，增长 58.3%。其中包含派生、量化和格式转换版本；规模扩张增加了可寻找的资源，不能直接当作独立原创成果增长。'),
         ('② 发布者与资源积累应分别观察','发布账号增长 48.4%，低于模型仓库增幅。平均每账号模型数由 4.68 增至 4.99，表明资源积累快于账号扩张；这是总体均值，不代表每个账号都提高了产出。'),
         ('③ 月度节奏揭示持续供给与起伏','在所示主统计期内，模型月度新增记录约为 7.40 万至 12.42 万个，呈现波动。判断生态持续性还需连接更新与退出记录，不能只看某个发布高峰。'),
         ('④ 数据供给需要独立进入视野','同期数据集月度新增记录约为 2.55 万至 7.40 万个，亦有明显起伏。模型与数据应分别观察；数据集数量、内容质量和能否用于训练，需要不同证据判断。')],sources(),['I02','I03','I05'])

def top(asset,country,n=6):return sorted([r for r in P if r['countryCode']==country],key=lambda r:(-r[asset]['downloads'],r['name'].casefold()))[:n]
def logo(f,name,x,y,size=21):
    p=R/'assets/logos'/(name+'.png')
    if p.exists():img(f,p,x,y,size,size)
def rank_group(f,x,y,asset,country,maxval,divisor):
    color='china' if country=='CN' else 'blue'
    f.text(x,y,'中国' if country=='CN' else '美国',19,color,True)
    f.text(x+470,y,'累计下载 / '+('亿次' if asset=='models' else '万次'),16,'muted',anchor='end')
    for i,r in enumerate(top(asset,country)):
        yy=y+32+i*28;v=r[asset]['downloads']/divisor
        f.text(x,yy,f'{i+1:02}',15,'muted');logo(f,r['name'],x+25,yy-18,20)
        f.text(x+53,yy,r['name'],17,'ink',i<3)
        f.rect(x+256,yy-12,120,10,'pale');f.rect(x+256,yy-12,120*r[asset]['downloads']/maxval,10,color,.88)
        f.text(x+470,yy,fmt(v,2 if asset=='models' else 1),18,color,i<3,'end')

def publisher_page():
    f=Figure();strip(f,[('826','可定位的组织账号样本'),('73,088','样本模型仓库'),('12,502','同一账号名录下的数据集'),('570','同时发布模型与数据的账号')])
    head(f,0,108,1,'模型获取活动 · 中美样本各前六');f.line(500,126,500,316)
    maximum=max(top('models','CN')[0]['models']['downloads'],top('models','US')[0]['models']['downloads'])
    for x,c in [(0,'CN'),(525,'US')]:rank_group(f,x,141,'models',c,maximum,1e8)
    f.line(0,331,1000,331)
    head(f,0,365,2,'数据获取活动 · 中美样本各前六');f.line(500,382,500,572)
    maximum=max(top('datasets','CN')[0]['datasets']['downloads'],top('datasets','US')[0]['datasets']['downloads'])
    for x,c in [(0,'CN'),(525,'US')]:rank_group(f,x,398,'datasets',c,maximum,1e4)
    f.line(0,589,1000,589);f.line(500,611,500,790)
    head(f,0,625,3,'模型与数据的头部名单不同')
    for x,c in [(0,'CN'),(240,'US')]:
        inter=set(r['name'] for r in top('models',c,3))&set(r['name'] for r in top('datasets',c,3));assert not inter
        f.text(x+8,662,'中国' if c=='CN' else '美国',19,'muted');f.text(x+102,696,'0',39,'teal',True,'middle')
        f.text(x+102,725,'两类前三账号交集',17,'muted',anchor='middle')
    foot(f,0,766,'同一资产的中美条长共用尺度；下载是获取活动，不等于用户数、部署量或模型能力。')
    head(f,525,625,4,'资源组合 · 四个具体账号')
    f.text(525,655,'发布账号',16,'muted');f.text(837,655,'模型 / 个',16,'muted',anchor='end');f.text(985,655,'数据集 / 个',16,'muted',anchor='end')
    for i,name in enumerate(['Qwen','deepseek-ai','InternRobotics','allenai']):
        r=next(r for r in P if r['name']==name);y=686+i*30
        logo(f,name,525,y-18,21);f.text(555,y,name,18)
        f.text(837,y,fmt(r['models']['models']),19,'blue',True,'end');f.text(985,y,fmt(r['datasets']['datasets']),19,'teal',True,'end');f.line(525,y+9,985,y+9)
    f.save('fig-5-1-2')
    return page('5.1','5.1　供给与贡献：发布者比较','同一批组织账号里，模型与数据的头部发布者并不相同。把两类资源放在一起，才能识别不同的供给角色与合作入口。','fig-5-1-2',
        '图 5-1-2　同一组织样本中的模型与数据发布者。来源：OpenGauge 观测快照［2］，2026.10.17 期后获取，统一统计日未声明。下载沿用来源累计口径；地域按账号归属。数据集未与具体模型训练逐一配对。',
        [('① 模型头部反映不同获取入口','中国样本的前三账号为 Qwen、BAAI、deepseek-ai；美国为 sentence-transformers、google-bert、openai。这里比较账号资源的获取活动，不能把累计下载直接解释为性能领先。'),
         ('② 数据供给有自己的关键主体','中国数据集榜前三为 InternRobotics、zai-org、OpenGVLab；美国为 allenai、argilla、huggingface。识别 AI 的数据支撑，需要超出模型榜单寻找发布者和维护入口。'),
         ('③ 支持对象应沿两类资源分别寻找','两国各自的模型榜与数据榜，前三账号均不重合。资助与合作对象不宜仅从模型热度选取，还应核对数据整理、文档更新和持续维护等实际交付。'),
         ('④ 同时发布不等于形成训练配套','826 个组织账号中，570 个同时有模型与数据集，但资源组合差异明显。表中数据只是同一账号发布的资产；是否用于对应模型训练、是否足够复现，仍需逐版本核实。')],sources(),['I02','I03','I05','I10'])

def divisions(asset):return [r for r in S['assets'][asset]['divisions'] if r['parent_id']==':divisions/CN']
def country(asset):return next(r for r in S['assets'][asset]['countries'] if r['code']=='CN')
def china_map(f,x,y,w,h):
    points=[]
    for g in G['china']:
        for cmd,vals in re.findall(r'([MLZ])([^MLZ]*)',g['d']):
            if cmd!='Z':
                v=[float(n) for n in re.findall(r'-?\d+(?:\.\d+)?',vals)];points+=list(zip(v[::2],v[1::2]))
    xmin=min(p[0] for p in points);xmax=max(p[0] for p in points);ymin=min(p[1] for p in points);ymax=max(p[1] for p in points)
    scale=min(w/(xmax-xmin),h/(ymax-ymin));tx=x+(w-(xmax-xmin)*scale)/2-xmin*scale;ty=y+(h-(ymax-ymin)*scale)/2-ymin*scale
    by={r['code']:r for r in divisions('models')};maximum=max(r['models'] for r in by.values())
    f.items.append(f'<g transform="translate({tx},{ty}) scale({scale})">')
    for g in G['china']:
        r=by.get(PM.get(g['id']));v=r['models'] if r and r['organizations']>0 else None
        color=mix('#D9EAF0','blue',math.log(v)/math.log(maximum)) if v else '#F2F5F7'
        f.items.append(f'<path d="{g["d"]}" fill="{color if g.get("kind")!="line" else "none"}" stroke="#9AADB9" stroke-width="{.8/scale}"/>')
    f.items.append('</g>')
    offsets={'110000':(-2,-23),'310000':(67,-15),'330000':(58,19),'440000':(-19,22),'710000':(69,22)}
    for g in G['china']:
        if g['id'] not in offsets:continue
        px=tx+g['center'][0]*scale;py=ty+g['center'][1]*scale;dx,dy=offsets[g['id']];lx=px+dx;ly=py+dy
        name=g['name'].replace('市','').replace('省','');name='台湾省' if g['id']=='710000' else name
        f.line(px,py,lx,ly-5,'muted',.9);ww=tw(name,17)+12;f.rect(lx-ww/2,ly-19,ww,24,'white',.96);f.text(lx,ly,name,17,'ink',True,'middle')

def china_page():
    cm=country('models');cd=country('datasets');mr=divisions('models');dr={r['code']:r for r in divisions('datasets')};four=['CN-BJ','CN-SH','CN-ZJ','CN-GD']
    f=Figure();strip(f,[('147','中国样本 · 组织账号'),('6,093','中国样本 · 模型仓库'),('1,354','同一组织名录 · 数据集'),('88.8%','京沪浙粤模型数 / 全国样本')])
    head(f,0,111,1,'模型资源的省级分布');head(f,550,111,2,'组织、模型与数据并非同序')
    china_map(f,0,137,517,290)
    for i in range(6):f.rect(i*24,439,24,12,mix('#D9EAF0','blue',i/5))
    f.text(157,451,'低 → 高 · 对数色阶',16,'muted');f.rect(350,439,16,12,'#F2F5F7');f.text(376,451,'未覆盖',16,'muted')
    headers=[(550,'地区'),(710,'组织'),(850,'模型'),(985,'数据集')]
    for x,t in headers:f.text(x,147,t,17,'muted',anchor='start' if x==550 else 'end')
    data=sorted([r for r in mr if r['organizations']>0],key=lambda r:-r['models'])
    data.append({'code':'unknown','name_zh':'归属待补',**cm['unassignedDivision']})
    for i,r in enumerate(data):
        y=179+i*28;name=r['name_zh'].replace('特别行政区','').replace('省','').replace('市','');name='台湾省' if r['code']=='CN-TW' else name
        d=dr.get(r['code'],cd['unassignedDivision']);col='muted' if r['code']=='unknown' else 'ink'
        f.text(550,y,name,18,col);f.text(710,y,fmt(r['organizations']),18,col,anchor='end');f.text(850,y,fmt(r['models']),18,'blue',True,'end');f.text(985,y,fmt(d['datasets']),18,'teal',True,'end');f.line(550,y+9,985,y+9)
    f.line(530,128,530,455);f.line(0,470,1000,470);f.line(500,492,500,790)
    head(f,0,510,3,'京沪浙粤集聚三类资源')
    f.text(0,548,'四地合计 / 中国全部样本',17,'muted')
    totals=[('组织账号',sum(r['organizations'] for r in mr if r['code'] in four),cm['organizations'],'violet'),('模型仓库',sum(r['models'] for r in mr if r['code'] in four),cm['models'],'blue'),('数据集',sum(r['datasets'] for r in dr.values() if r['code'] in four),cd['datasets'],'teal')]
    for i,(name,n,den,col) in enumerate(totals):
        y=591+i*59;f.text(0,y,name,20,'ink',True);f.text(470,y,f'{n:,} / {den:,}  ·  {n/den*100:.1f}%',19,col,True,'end');f.rect(0,y+13,470,10,'pale');f.rect(0,y+13,470*n/den,10,col)
    foot(f,0,769,'全国分母保留归属待补记录；灰白地区不解释为零供给。')
    head(f,525,510,4,'获取活动呈现不同地区角色')
    f.rect(525,536,13,10,'blue');f.text(547,547,'模型下载占比',17,'muted');f.rect(764,536,13,10,'teal');f.text(786,547,'数据下载占比',17,'muted')
    for i,code in enumerate(four):
        r=next(r for r in mr if r['code']==code);y=586+i*43
        f.text(525,y+8,r['name_zh'].replace('省','').replace('市',''),18)
        for j,(value,total,col) in enumerate([(r['downloads'],cm['downloads'],'blue'),(dr[code]['downloads'],cd['downloads'],'teal')]):
            v=value/total*100;f.rect(584,y-8+j*16,290*v/60,10,col);f.text(985,y+2+j*16,f'{v:.1f}%',17,col,True,'end')
    foot(f,525,783,'各以中国样本相应资产累计下载为分母。')
    f.save('fig-5-1-3')
    return page('5.1','5.1　供给与贡献：中国结构','组织基础、模型积累与数据供给呈现不同地域组合。将这些维度并列观察，有助于把合作线索落实到具体资源与发布主体。','fig-5-1-3',
        '图 5-1-3　中国模型供给的省级结构与资源组合。来源：OpenGauge 观测快照［2］，2026.10.17 期后获取，统一统计日未声明。按组织账号归属定位；12 个账号、149 个模型、41 个数据集省级归属待补，仍计入全国样本。',
        [('① 地图呈现资源位置，而非完整产业','浙江、北京、上海、广东构成样本中主要供给节点。地图定位的是组织账号发布资源的省级归属，不能直接解释为研发人员、算力或使用者所在地，也不能用浙江数据替代杭州。'),
         ('② 地区优势取决于观察什么资源','北京有 47 个组织账号、480 个关联数据集，浙江有 1,726 个模型仓库。组织基础、模型积累与数据供给对应不同能力线索，适合结合具体任务寻找合作主体。'),
         ('③ 集聚提示协作入口，也提示覆盖缺口','京沪浙粤合计 116 个组织账号、5,408 个模型、1,218 个数据集。资源集聚可提供跨地区合作入口，但样本未覆盖地区不等于没有供给，仍需补齐主体与地域信息。'),
         ('④ 从地方排序转向资源互补','浙江占中国样本模型累计下载的 56.8%；北京和上海合计占数据累计下载的 75.4%。地方支持可据此寻找模型、数据与评测的互补伙伴，再用维护和实际复用记录检验合作。')],sources(),['I02','I03','I10','I12'])

def render():
    pages=[supply_page(),publisher_page(),china_page()]
    save_pages('5.1',pages)
    return pages
