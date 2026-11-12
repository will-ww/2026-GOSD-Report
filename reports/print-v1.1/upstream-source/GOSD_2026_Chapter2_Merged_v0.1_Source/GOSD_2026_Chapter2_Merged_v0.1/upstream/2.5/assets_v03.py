"""Four evidence-led, map-based composites. All numeric inputs retained in data/."""
from build import *
import shapefile, pycountry
from datetime import date

C.update(model='#7253A2', data='#007D78', land='#E9EEF2', china='#AD4E22')
J=lambda p:json.loads((D/p).read_text())
REPOS=J('repo-countries.json'); NOW=REPOS['2026Q2']; PREV=REPOS['2025Q2']; TOTAL=sum(NOW.values())
SAMPLE=J('25/raw/publisher_sample_extract.json')['assets']
MODELS={c['id']:c['count'] for c in SAMPLE['models']['countries']}
DATASETS={c['id']:c['count'] for c in SAMPLE['datasets']['countries']}
CNAMES={'US':'美国','IN':'印度','CN':'中国','BR':'巴西','JP':'日本','GB':'英国','ID':'印度尼西亚','DE':'德国','CA':'加拿大','RU':'俄罗斯','FR':'法国','KR':'韩国','SG':'新加坡','VN':'越南','ES':'西班牙','PK':'巴基斯坦','BD':'孟加拉国','NL':'荷兰','MX':'墨西哥','NG':'尼日利亚','FI':'芬兰','IE':'爱尔兰','MY':'马来西亚'}
CENTERS={'US':(-100,39),'CN':(104,35),'FR':(2,47),'DE':(10,51),'GB':(-2,54),'FI':(26,64),'IE':(-8,53),'JP':(139,36),'KR':(128,36),'SG':(104,1),'BR':(-52,-13),'IN':(79,23),'CA':(-105,58),'ES':(-4,40),'RU':(95,61),'MY':(109,5),'ID':(118,-3),'NG':(8,10),'BD':(90,24),'PK':(69,29),'VN':(106,17)}

def project(lon,lat):
    a1,a2,a3,a4=1.340264,-0.081106,0.000893,0.003796
    t=math.asin(math.sqrt(3)/2*math.sin(math.radians(lat)))
    return (2*math.sqrt(3)*math.radians(lon)*math.cos(t)/(3*(9*a4*t**8+7*a3*t**6+3*a2*t*t+a1)),t*(a1+a2*t*t+a3*t**6+a4*t**8))

WORLD=[]
sf=shapefile.Reader(str(D/'naturalearth_lowres.shp'))
for s in sf.iterShapeRecords():
    rec=s.record.as_dict(); a3=rec['iso_a3']; name=rec['name']
    if name=='Antarctica':continue
    overrides={'France':'FR','Norway':'NO','Kosovo':'XK','Somaliland':'SO','N. Cyprus':'CY','Taiwan':'CN'}
    try:iso=overrides.get(name) or pycountry.countries.get(alpha_3=a3).alpha_2
    except:iso='ZZ'
    parts=list(s.shape.parts)+[len(s.shape.points)]
    paths=[[project(*p) for p in s.shape.points[parts[i]:parts[i+1]]] for i in range(len(parts)-1)]
    WORLD.append((iso,paths))

def mix(a,b,t):
    a=cl(a).lstrip('#');b=cl(b).lstrip('#')
    return '#'+''.join(f'{round(int(a[i:i+2],16)*(1-t)+int(b[i:i+2],16)*t):02x}' for i in [0,2,4])

def world(f,x,y,w,h,vals,color,labels=(),log=True):
    # Equal Earth projection; Antarctica omitted to devote space to inhabited regions.
    xmin,xmax,ymin,ymax=-2.72,2.72,-1.08,1.32
    scale=min(w/(xmax-xmin),h/(ymax-ymin));ox=x+(w-scale*(xmax-xmin))/2;oy=y+(h-scale*(ymax-ymin))/2
    def pt(lon,lat):
        px,py=project(lon,lat);return ox+(px-xmin)*scale,oy+(ymax-py)*scale
    vmax=max(vals.values());vmin=min(v for v in vals.values() if v>0)
    for iso,paths in WORLD:
        v=vals.get(iso)
        t=(math.log(v)-math.log(vmin))/(math.log(vmax)-math.log(vmin)) if v and log else (v/vmax if v else 0)
        fill=mix('#EAF0F6',color,.10+.90*t) if v else C['land']
        for poly in paths:
            pts=[(ox+(px-xmin)*scale,oy+(ymax-py)*scale) for px,py in poly]
            # Taiwan and mainland share the China value and color.
            f.path(pts,'white',.55,fill)
    for iso in labels:
        px,py=pt(*CENTERS[iso]); name=CNAMES[iso]; ww=tw(name,18,True)+13
        f.rect(px-ww/2,py-14,ww,25,'white',.93);f.text(px,py+4,name,18,'ink',True,'middle')
    return pt

def legend(f,x,y,color,label='数量由少到多 · 对数色阶',missing='未列明'):
    for i in range(6):f.rect(x+i*18,y-13,18,13,mix('#EAF0F6',color,.1+.18*i))
    f.text(x+118,y,label,15,'muted');f.rect(x+371,y-13,14,13,'land');f.text(x+392,y,missing,15,'muted')

def kpi(f,x,w,label,value,note,color):
    f.rect(x,0,w,95,'pale');f.rect(x,0,4,95,color)
    f.text(x+15,24,label,17,'muted');f.text(x+15,62,value,34,color,True);f.text(x+15,85,note,14.5,'muted')

def smallbars(f,rows,x,y,w,rowh=26,color='blue',unit=''):
    maxv=max(v for _,v in rows)
    for i,(n,v) in enumerate(rows):
        yy=y+i*rowh
        f.text(x,yy,f'{i+1:02}',14,'muted');f.text(x+28,yy,n,17,'ink',n=='中国')
        f.rect(x+123,yy-12,max(.8,(w-215)*v/maxv),12,color,.65)
        s=f'{v:,}' if not unit else f'{v/10000:,.0f}'
        f.text(x+w,yy,s,16.8,'ink',n=='中国','end')

def linechart(f,series,x,y,w,h,years,ymax,ticks,unit='',endlabels=True):
    for v in ticks:
        yy=y+h-v/ymax*h;f.line(x,yy,x+w,yy,'line',.8);f.text(x-7,yy+5,f'{v:g}',14,'muted',anchor='end')
    for i,yr in enumerate(years):f.text(x+i*w/(len(years)-1),y+h+24,str(yr),14,'muted',anchor='middle')
    if unit:f.text(x-22,y-13,unit,14,'muted')
    for name,values,color in series:
        pts=[(x+i*w/(len(values)-1),y+h-v/ymax*h) for i,v in enumerate(values)]
        f.path(pts,color,3)
        for px,py in pts:f.circle(px,py,3.2,color)
        if endlabels:f.text(pts[-1][0]+8,pts[-1][1]+5,name,16,color,True)

def overview():
    f=Figure()
    kpi(f,0,322,'公开代码仓库','4.54 亿','GitHub 已披露地域合计 · 2026 Q2','blue')
    kpi(f,338,322,'公开模型仓库','296 万','Hugging Face 全平台 · 2026 年 8 月','model')
    kpi(f,676,324,'公开数据集仓库','100 万','Hugging Face 全平台 · 2026 年 8 月','data')
    f.title(0,131,'1','三类资产的全球位置')
    pt=world(f,0,157,638,296,NOW,'blue')
    # A restrained set of directly labelled dual-asset anchors avoids dense Europe bubbles.
    for iso,tx,ty in [('US',100,227),('FR',303,191),('CN',508,238),('JP',581,365),('BR',199,417),('IN',411,369)]:
        px,py=pt(*CENTERS[iso]);f.line(px,py,tx,ty-13,'muted',.9);f.circle(px,py,3,'ink')
        rows=[CNAMES[iso],f'模型 {MODELS[iso]:,}']
        if iso in DATASETS:rows.append(f'数据 {DATASETS[iso]:,}')
        else:rows.append('数据未列明')
        bw=128;bh=58;f.rect(tx-bw/2,ty-27,bw,bh,'white',.94)
        f.text(tx,ty-9,rows[0],17,'ink',True,'middle');f.text(tx,ty+10,rows[1],15,'model',anchor='middle');f.text(tx,ty+28,rows[2],15,'data',anchor='middle')
    legend(f,4,481,'blue','底色：公开代码仓库','未披露')
    f.text(4,507,'标注：模型与数据集的发布者样本数量（个）',15,'muted')
    f.title(662,131,'2','三类资产的地域结构')
    for xx,t in [(662,'国家'),(813,'代码'),(900,'模型'),(992,'数据')]:f.text(xx,165,t,16,'muted',anchor='start' if xx==662 else 'end')
    f.text(992,187,'各列为各自口径下的数量份额',13.8,'muted',anchor='end')
    for i,iso in enumerate(['US','CN','IN','BR','DE','FR','JP','GB','CA','SG']):
        yy=217+i*28
        if i%2==0:f.rect(656,yy-19,344,27,'pale')
        f.text(665,yy,CNAMES[iso],17,'ink',iso=='CN')
        for xx,v,total,color in [(813,NOW.get(iso),TOTAL,'blue'),(900,MODELS.get(iso),72280,'model'),(992,DATASETS.get(iso),12291,'data')]:
            f.text(xx,yy,f'{v/total*100:.1f}%' if v else '—',16,color,iso=='CN','end')
    f.line(0,525,1000,525)
    f.title(0,556,'3','扩张仍在继续，三类资产同步增长')
    specs=[(0,'代码仓库','2025 Q2 → 2026 Q2',370919525,453514308,'亿',1e8,'blue'),(340,'模型仓库','2026 年 1 月 → 8 月',2430000,2960000,'万',1e4,'model'),(680,'数据集仓库','2026 年 1 月 → 8 月',711000,1000000,'万',1e4,'data')]
    for x,name,period,a,b,unit,scale,c in specs:
        f.text(x,587,name,17,c,True);f.text(x+304,587,f'+{(b/a-1)*100:.1f}%',24,c,True,'end')
        f.text(x,610,period,14.5,'muted')
        for j,v in enumerate([a,b]):
            yy=634+j*27;f.rect(x,yy-13,191*v/b,15,c,.35 if j==0 else .9)
            f.text(x+305,yy,f'{v/scale:.2f}'.rstrip('0').rstrip('.')+unit,17,'ink',anchor='end')
    f.line(0,681,1000,681)
    f.title(0,712,'4','数量份额与下载份额并不重合')
    f.text(0,747,'两类地域样本分别比较',16,'muted')
    f.text(0,780,'供给广度与使用深度',21,'ink',True)
    f.text(461,741,'模型：数量 → 下载',16,'model',True);f.text(767,741,'数据：数量 → 下载',16,'data',True)
    for yy,n,m,d in [(768,'美国','63.4% → 73.9%','47.8% → 82.6%'),(797,'中国','8.3% → 12.6%','10.9% → 4.7%')]:
        f.text(355,yy,n,17,'ink',True);f.text(461,yy,m,19,'model',True);f.text(767,yy,d,19,'data',True)
    f.save('fig-2-13-asset-world')

def code():
    f=Figure()
    kpi(f,0,322,'公开代码仓库','4.54 亿','已披露地域合计 · 2026 Q2','blue')
    kpi(f,338,322,'一年净增公开仓库存量','8,259 万','2025 Q2 至 2026 Q2 · +22.3%','blue')
    kpi(f,676,324,'活跃仓库 · GitHub / Gitee','633 万 / 439 万','报告年度 · 2025.07—2026.06','teal')
    f.title(0,131,'1','代码存量：广泛分布的协作基础')
    world(f,0,157,628,307,NOW,'blue',['US','CN','IN','BR'])
    legend(f,0,488,'blue','数量由少到多 · 对数色阶','未披露')
    f.text(0,514,'仓库按有管理权限的成员地域归属；包括暂不活跃的仓库。',15,'muted')
    f.title(651,131,'2','公开仓库前 20 位')
    f.text(996,155,'万仓库',14.5,'muted',anchor='end')
    rows=sorted(NOW.items(),key=lambda x:-x[1])[:20]
    smallbars(f,[(CNAMES[k],v) for k,v in rows],655,176,342,18.3,'blue','万')
    f.line(0,544,1000,544)
    f.title(0,579,'3','美国与印度接近，积累更加多中心')
    years=list(range(2020,2027));series=[]
    for iso,c in [('US','blue'),('IN','india'),('CN','china'),('BR','teal')]:
        series.append((CNAMES[iso],[REPOS[f'{y}Q2'][iso]/1e4 for y in years],c))
    linechart(f,series,44,616,364,148,years,9000,[0,3000,6000,9000],'万仓库',False)
    for (name,values,c),ly in zip(series,[621,649,715,741]):
        ey=616+148-values[-1]/9000*148
        f.path([(408,ey),(417,ly-5),(423,ly-5)],c,1)
        f.text(429,ly,name,16,c,True)
    f.title(526,579,'4','AI 推动生产节奏跃升')
    f.text(526,609,'GitHub 年度提交次数（含私有仓库）',15,'muted')
    for i,(yr,v) in enumerate([(2024,100),(2025,129),(2026,343)]):
        xx=535+i*93;bh=v/343*113;f.rect(xx,753-bh,58,bh,'blue',.4 if i<2 else 1)
        f.text(xx+29,743-bh,str(v),18,'blue',True,'middle');f.text(xx+29,778,str(yr),14.5,'muted',anchor='middle')
    f.text(811,646,'343 亿',28,'blue',True);f.text(811,671,'年度代码提交',16,'muted')
    f.text(811,721,'25 亿',28,'teal',True);f.text(811,746,'公开贡献次数',16,'muted');f.text(811,777,'同比约 +123%',17,'teal',True)
    f.save('fig-2-14-code-world')

def model():
    f=Figure()
    kpi(f,0,322,'HF 公开模型仓库','296 万','全平台 · 2026 年 8 月','model')
    kpi(f,338,322,'地域观察中的模型','72,280','826 家发布单位 · 快照日期待核','model')
    kpi(f,676,324,'样本模型下载','600 亿次','按发布单位所在地域归属','model')
    f.title(0,131,'1','模型供给：中美与欧洲各有位置','model')
    world(f,0,157,626,298,MODELS,'model',['US','CN','BR','IN'])
    legend(f,0,482,'model','样本数量 · 对数色阶')
    f.text(0,509,'已列明 14 个地域，覆盖样本模型数量的 94.3%。',15,'muted')
    f.title(651,131,'2','模型数量的地域画像','model')
    f.text(996,158,'模型 / 个',14.5,'muted',anchor='end')
    smallbars(f,[(CNAMES[k],v) for k,v in MODELS.items()],655,183,342,24,'model')
    f.line(0,526,1000,526)
    f.title(0,559,'3','供给加速，运行适配增长更快','model')
    rows=readcsv('hf-daily-models.csv');start=date.fromisoformat(rows[0]['date']);end=date.fromisoformat(rows[-1]['date'])
    x,y,w,h=40,604,329,157;maxn=2500000
    for v in [0,1000000,2000000]:
        yy=y+h-v/maxn*h;f.line(x,yy,x+w,yy);f.text(x-8,yy+5,str(v//10000),14,'muted',anchor='end')
    f.text(x-21,y-17,'万',14,'muted')
    points=[(x+(date.fromisoformat(r['date'])-start).days/(end-start).days*w,y+h-int(r['number'])/maxn*h) for r in rows]
    f.path([(x,y+h)]+points+[(x+w,y+h)],'none',0,'model',opacity=.12);f.path(points,'model',3)
    for yr in [2022,2023,2024,2025]:
        xx=x+(date(yr,7,1)-start).days/(end-start).days*w;f.text(xx,y+h+26,str(yr),14,'muted',anchor='middle')
    for d,l,dy in [('2024-10-19','100 万',30)]:
        row=min(rows,key=lambda r:abs((date.fromisoformat(r['date'])-date.fromisoformat(d)).days));xx=x+(date.fromisoformat(row['date'])-start).days/(end-start).days*w;yy=y+h-int(row['number'])/maxn*h
        f.circle(xx,yy,4,'model');f.text(xx-5,yy+dy,l,16,'model',True,'end')
    f.text(370,610,'226.5 万',19,'model',True,'end');f.text(370,634,'2025-12-08',13.5,'muted',anchor='end')
    row=min(rows,key=lambda r:abs((date.fromisoformat(r['date'])-date(2025,1,20)).days))
    xx=x+(date.fromisoformat(row['date'])-start).days/(end-start).days*w;yy=y+h-int(row['number'])/maxn*h
    f.circle(xx,yy,4,'model');f.line(xx,yy,xx-25,yy-31,'model',1)
    f.text(xx-25,yy-38,'DeepSeek-R1',13.7,'model',True,'middle')
    f.line(392,604,392,782,'line',1)
    f.text(411,608,'2026',18,'ink',True);f.text(411,632,'前七个月',14.5,'muted')
    f.text(411,671,'+464%',24,'model',True)
    f.text(411,700,'GGUF',18,'model',True)
    f.text(411,723,'格式仓库',15,'muted')
    f.text(411,752,'支持本地',15,'ink');f.text(411,775,'设备运行',15,'ink')
    f.title(542,559,'4','下载结构：再分发拓宽中国影响','model')
    f.text(542,589,'独立研究样本',15,'muted');f.text(809,589,'全历史',15,'muted',anchor='end');f.text(993,589,'近年新发布模型',15,'muted',anchor='end')
    for i,(n,a,b,c) in enumerate([('中国',6.3,17.1,'china'),('美国',27.5,15.8,'blue'),('个人及跨地域组织',50,57.6,'model'),('其他',16.2,9.5,'muted')]):
        yy=625+i*35;f.text(542,yy,n,16.3,'ink',i==0);f.text(809,yy,f'{a:g}%',19,c,i==0,'end');f.text(993,yy,f'{b:g}%',19,c,i==0,'end');f.line(542,yy+10,996,yy+10)
    f.wrap(542,777,'近年组：2024.08—2025.08 新发布模型；两列为不同模型群体的下载结构。',453,14,'muted',leading=19)
    f.save('fig-2-15-model-world')

def data():
    f=Figure()
    kpi(f,0,322,'HF 公开数据集仓库','100 万','全平台 · 2026 年 8 月','data')
    kpi(f,338,322,'地域观察中的数据集','12,291','同一发布单位样本 · 快照日期待核','data')
    kpi(f,676,324,'样本数据集下载','8.06 亿次','下载衡量使用，不能等同使用人数','data')
    f.title(0,131,'1','数据供给：更多地域拥有参与入口','data')
    world(f,0,157,626,298,DATASETS,'data',['US','CN','BR','RU'])
    legend(f,0,482,'data','样本数量 · 对数色阶')
    f.text(0,509,'已列明 14 个地域，覆盖样本数据集数量的 89.8%。',15,'muted')
    f.title(651,131,'2','数据集数量的地域画像','data')
    f.text(996,158,'数据集 / 个',14.5,'muted',anchor='end')
    smallbars(f,[(CNAMES[k],v) for k,v in DATASETS.items()],655,183,342,24,'data')
    f.line(0,526,1000,526)
    f.title(0,559,'3','规模扩张，机器人数据快速涌现','data')
    f.text(0,590,'HF 数据集总量',16,'ink',True);f.text(0,614,'2026 年 1 月 → 8 月',14.5,'muted')
    for i,(v,l) in enumerate([(71.1,'71.1 万'),(100,'100 万')]):
        xx=12+i*112;bh=v/100*112;f.rect(xx,760-bh,65,bh,'data',.35 if i==0 else .95);f.text(xx+32,750-bh,l,17,'data',True,'middle');f.text(xx+32,784,'1 月' if i==0 else '8 月',14.5,'muted',anchor='middle')
    f.line(251,585,251,789,'line')
    f.text(275,590,'机器人数据集数量',16,'ink',True);f.text(275,615,'2024 → 2025',14.5,'muted')
    for i,(v,l) in enumerate([(1145,'1,145'),(26991,'26,991')]):
        xx=282+i*112;bh=v/26991*112;f.rect(xx,760-bh,65,bh,'data',.35 if i==0 else .95);f.text(xx+32,750-bh,l,17,'data',True,'middle');f.text(xx+32,784,'2024' if i==0 else '2025',14.5,'muted',anchor='middle')
    f.text(282,669,'23.6 倍',19,'teal',True)
    f.title(542,559,'4','从数据数量到使用价值','data')
    f.text(542,590,'同一地域样本：数量份额与下载份额',15,'muted')
    for i,(iso,ct,dl,c) in enumerate([('美国',5871/12291*100,82.6,'blue'),('中国',1338/12291*100,4.7,'china'),('其他地域',100-(5871+1338)/12291*100,12.7,'data')]):
        yy=627+i*53;f.text(542,yy,iso,17,'ink',iso=='中国')
        f.rect(635,yy-13,253*ct/100,13,c,.3);f.rect(635,yy+6,253*dl/100,13,c,.95)
        f.text(997,yy,f'{ct:.1f}%',17,'ink',anchor='end');f.text(997,yy+21,f'{dl:.1f}%',17,c,True,'end')
    f.rect(636,778,16,12,'soft',.5);f.text(663,789,'数量份额',15,'muted');f.rect(806,778,16,12,'teal');f.text(833,789,'下载份额',15,'muted')
    f.save('fig-2-16-data-world')

def render():
    overview();code();model();data()
    return [
    dict(title='2.5 全球开源资产地图',intro='代码、模型与数据共同构成人工智能时代的开放资源基础：既要看全球积累，也要看资源怎样进入实际使用。',figure='fig-2-13-asset-world',caption='图 2-13　三类开源资产的全球分布与增长。代码为 GitHub 公开仓库；模型和数据总量来自 Hugging Face（HF），地域分布来自报告累计样本。来源：GitHub Innovation Graph、HF Summer 2026、报告观察数据；样本日期待核，口径详见附录 1。',analyses=[
    ('① 共同底座，三种不同的资源','代码承载可修改的软件，模型提供可调用、可改造的智能能力，数据支持训练、评测与适配。三类资源相互依赖；地图展示它们的供给位置，不把仓库数量相加为一个“资产总量”。'),
    ('② 同一国家，在不同资产上位置不同','美国在三类观察中均居前列；印度的公开代码仓库接近美国，中国在模型与数据样本中均居第二。代码积累的广度与 AI 资源供给的集中度并存，不能用单一平台替代整体生态判断。'),
    ('③ AI 时代的扩张是多层同步的','代码公开仓库存量一年增长 22.3%；HF 模型、数据集在 2026 年 1—8 月分别增长约 21.8% 和 40.6%。时间跨度各异，但共同说明开放供给正在从软件代码扩展到智能能力与训练材料。'),
    ('④ 开放数量须进一步转化为公共能力','样本中，美国的数据集数量占 47.8%，下载占 82.6%，表明“有资源”与“被使用”并不等同。对中国与全球南方，资源建设还要连接本地需求、维护服务与全球分发，才能形成持续能力。')]),
    dict(title='2.5.1 代码资产：从广泛积累到加速生产',intro='公开仓库存量刻画积累，活跃仓库反映参与运转的基础，代码提交与公开贡献则揭示当期生产和协作的节奏。',figure='fig-2-14-code-world',caption='图 2-14　公开代码仓库地域分布、增长与生产节奏。来源：GitHub Innovation Graph（2026 Q2）；OpenDigger 原报告平台活跃仓库序列；GitHub Octoverse 2026（2025.10—2026.09）。公开贡献与全部提交分列，不能相加。',analyses=[
    ('① 代码积累已形成广泛的地域基础','已披露地域的公开仓库合计 4.54 亿，约为 2020 年同期的 3.45 倍。报告年度 GitHub、Gitee 活跃仓库分别为 633 万、439 万：全球代码资源在积累，也通过不同平台持续运转。'),
    ('② 全球南方拥有可见的供给基础','印度、巴西、印度尼西亚分别有约 7,474 万、2,127 万和 1,138 万公开仓库，孟加拉国、尼日利亚也进入前二十。广泛的代码参与为本地应用与 AI 适配提供入口，其质量和持续维护仍需另行观察。'),
    ('③ 增长路径分化，不能只比较位次','美国与印度仓库存量接近，最近一年分别增长 17.0% 和 35.0%；巴西增长 24.7%。中国合并内地及港澳台后约 3,388 万。地域数量受平台使用与归属方式影响，不足以单独判定技术领先。'),
    ('④ 生产加速，更需识别有效沉淀','2026 年度 GitHub 提交量达 343 亿次，公开贡献达 25 亿次。AI 正改变开发节奏，但一次提交不等于一项新资产；对高产出项目，还应联看问题解决、版本维护、测试与下游采用。')]),
    dict(title='2.5.2 模型资产：供给扩张与全球再分发',intro='模型仓库既包括原创模型，也包括微调、量化与格式转换等再创造；数量增长与下载流向共同揭示开放影响的形成。',figure='fig-2-15-model-world',caption='图 2-15　模型供给地图、增长与下载结构。地域数量：报告发布者样本；增长：HF / AI World 日度序列及 HF Summer 2026；下载：Longpre 等《The Economies of Open Intelligence》（至 2025.08，滚动窗口过滤）。',analyses=[
    ('① 中美之外，欧洲与亚洲也有重要节点','样本中美国发布 45,801 个模型，中国发布 6,017 个；法国、德国、芬兰及日韩、新加坡各有供给。模型并非只由少数大厂生产，专业机构与社区共同连接基础模型、工具和应用。'),
    ('② 中国模型的使用位置高于数量份额','中国占发布者样本模型数量的 8.3%，下载占 12.6%；美国分别为 63.4% 与 73.9%。供给数量与使用集中度并不重合：中国的模型资源正获得超出其仓库数量份额的采用，仍需继续观察具体用途。'),
    ('③ 把模型变得可用，是重要的资产增量','HF 的 GGUF 格式仓库在 2026 年前七个月增长 464%。这种格式便于模型在本地设备运行；微调让模型适配任务，量化通过压缩数值精度降低运行成本。开放的价值由原始权重延伸到这些再创造。'),
    ('④ 中国贡献在全球接续中得到放大','在 2024.08—2025.08 新发布模型的下载中，中国占 17.1%，美国占 15.8%；个人及跨地域组织合计 57.6%。这是特定模型群体的下载结构，提示分发与再创造的重要性，不代表整体市场份额。')]),
    dict(title='2.5.3 数据资产：从积累走向可持续使用',intro='数据集提供训练、评测与本地化的材料。AI 将数据需求从文本扩展到动作、轨迹和环境交互，数据的可用性也因此更加重要。',figure='fig-2-16-data-world',caption='图 2-16　数据集地域分布、增长与使用差异。地域数量和下载来自报告发布者样本；平台增长来自 HF Summer 2026；机器人数据集数量来自 HF Spring 2026。地图中未列明的地域不表示没有数据资产。',analyses=[
    ('① 数据供给的地域结构与模型不同','样本中，美国与中国分别有 5,871 和 1,338 个数据集；德国、法国之后，爱尔兰、马来西亚等也进入前列。较小经济体能够通过专业领域和语言资源形成贡献，不必复制大规模模型训练路线。'),
    ('② 中国有数量基础，还须增强使用连接','中国占样本数据集数量的 10.9%，高于其模型数量份额 8.3%，但数据集下载仅占 4.7%。这一差异提示，应进一步检查语言覆盖、文档、格式、更新与分发条件，不能仅据此推断数据质量。'),
    ('③ 新增需求正在进入物理世界','HF 数据集总量在 2026 年 1—8 月从 71.1 万增至 100 万。机器人数据集从 2024 年的 1,145 个增至 2025 年的 26,991 个，约为前者的 23.6 倍；动作与交互记录正在成为训练智能系统的重要开放资源。'),
    ('④ 数据普惠依赖持续服务与本地参与','样本下载集中于美国，并不意味着需求只在那里。全球南方可围绕本地语言、农业、健康和公共服务建立数据合作；基金会等公共组织可支持明确使用条件、质量评测和维护，使资源持续可用。')])
    ]
