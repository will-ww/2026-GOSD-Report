"""GOSD 5.2: three evidence compositions, preserving declared relationships."""
from common import *
D=R/'inputs/52/data'
def readcsv(n):return list(csv.DictReader((D/n).open()))
import gzip

SOURCE='https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/c51e3441361407b68f10b339d97eff288319b503/'
def source(i,path):return {'id':str(i),'url':SOURCE+path}
SOURCES=[source(1,'data/processed/chapter5/fig-5-2-1_hf_cumulative_derivation.csv'),
 source(2,'preview/content/gosm/lineage-live-provenance.json'),
 source(3,'data/processed/chapter5/fig-5-2-2_cross_country_derivation_flows.csv'),
 source(4,'data/processed/chapter5/fig-5-2-3_modelrank_country_head_trend.csv')]
def gzrows(name):return list(csv.DictReader(gzip.open(D/name,'rt')))
N=gzrows('lineage-live-full-nodes.csv.gz');E=gzrows('lineage-live-full-edges.csv.gz');NB={n['id']:n for n in N}
A=readcsv('fig-5-2-1_hf_cumulative_derivation.csv');FLOW=readcsv('fig-5-2-2_cross_country_derivation_flows.csv');M=readcsv('fig-5-2-3_modelrank_country_head_trend.csv')
for r in FLOW:r['weight']=int(r['weight'])
for r in M:
 for k in ['k','china','us','other_known','unknown']:r[k]=int(r[k])
COUNTRY={'CN':'中国','US':'美国','DE':'德国','FR':'法国','GB':'英国','JP':'日本','OTH':'其他','IN':'印度','BR':'巴西','ID':'印度尼西亚'}
CC={'CN':'china','US':'blue','DE':'teal','FR':'violet','GB':'orange','JP':'green','OTH':'#9CAAB4'}
TASKS=[('language','语言生成','blue'),('multimodal','多模态','violet'),('vision','图像与视频','green'),('speech','语音','orange'),('other','其他任务','teal'),('unknown','任务未标注','#97A6B2')]
TC={a:c for a,b,c in TASKS}
def task(n):
 t=n['task']
 if not t or t=='unspecified-model':return 'unknown'
 if t=='text-generation':return 'language'
 if t in ('image-text-to-text','any-to-any'):return 'multimodal'
 if any(q in t for q in ['image','video','depth']):return 'vision'
 if any(q in t for q in ['speech','audio']):return 'speech'
 return 'other'
def head(f,x,y,n,t,fs=20):f.title(x,y,str(n),t,'teal',fs)
def strip(f,items):
 f.rect(0,0,1000,74,'pale')
 for i,(v,t) in enumerate(items):
  x=18+250*i
  if i:f.line(x-18,14,x-18,60)
  f.text(x,38,v,29,'teal',True);f.text(x,61,t,17,'muted')
def note(f,x,y,t,w=300,fs=16):f.wrap(x,y,t,w,fs,'muted',leading=23)
def arrow(f,x,y,xx,yy,c='teal'):
 f.line(x,y,xx,yy,c,1.6);ang=math.atan2(yy-y,xx-x)
 f.path([(xx-7*math.cos(ang-.45),yy-7*math.sin(ang-.45)),(xx,yy),(xx-7*math.cos(ang+.45),yy-7*math.sin(ang+.45))],c,1.6)

def network(f):
 pts={n['id']:(498+520*float(n['x']),282+160*float(n['y'])) for n in N}
 for e in E:f.path([pts[e['source']],pts[e['target']]],TC[task(NB[e['source']])],.65,opacity=.25)
 for n in sorted(N,key=lambda r:int(r['downstreamCount'])):
  x,y=pts[n['id']];radius=math.sqrt(1.25+int(n['downstreamCount'])*.30)
  f.items.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{cl(TC[task(n)])}" opacity=".88"/>')
 labels=[('Qwen/Qwen-Image-2.1',4,175,'start'),('Qwen/Qwen3-0.6B',5,310,'start'),
  ('openai/whisper-large-v3',120,425,'start'),('Qwen/Qwen3.8-Flash-Next',430,144,'start'),
  ('Qwen/Qwen3.8-27B',735,238,'start'),('zai-org/GLM-5.3-Flash',990,327,'end'),('MiniMaxAI/MiniMax-H3',975,423,'end')]
 for id,x,y,anchor in labels:
  n=NB[id];text=n['name'];w=tw(text,17);left=x if anchor=='start' else x-w
  f.line(*pts[id],x+3 if anchor=='start' else x-3,y-5,TC[task(n)],1)
  f.rect(left-4,y-18,w+8,25,'white',.95);f.text(x,y,text,17,'ink',False,anchor)
 for x,(k,name,col) in zip([7,162,298,477,590,760],TASKS):
  f.circle(x+5,461,4,col);f.text(x+17,467,name,16,'muted')
 note(f,0,495,'点＝模型版本；线＝声明的基座 → 派生；点面积随直接下游数增大。位置仅供导航，密集处省略箭头。',1000)

def annual(f,x,key,maxv,pct=False):
 x0=x+35;x1=x+294;top=605;bottom=744
 for v in [0,maxv/2,maxv]:
  y=bottom-(bottom-top)*v/maxv;f.line(x0,y,x1,y);f.text(x0-7,y+5,f'{v:g}',15,'muted',anchor='end')
 vals=[float(r[key])/(1 if pct else 10000) for r in A];points=[(x0+i*(x1-x0)/4,bottom-(bottom-top)*v/maxv) for i,v in enumerate(vals)]
 col='violet' if pct else 'blue'
 f.path([(x0,bottom)]+points+[(x1,bottom)],col,0,fill=col,opacity=.07);f.path(points,col,2.5)
 for i,((px,py),v) in enumerate(zip(points,vals)):
  f.circle(px,py,3,col);f.text(px,py-9,f'{v:.1f}' if pct else f'{v:.2f}',16,col,True,'middle');f.text(px,770,A[i]['date'][2:4],16,'muted',anchor='middle')
 note(f,x+31,798,'2022—2026 各年 9 月 13 日',290,15)

def page_network():
 f=Figure();strip(f,[('5,777','模型版本 · 网络样本'),('5,111','基座到派生 · 声明关系'),('85.87 万','有基座声明的仓库 · 回溯点'),('+52.3%','派生仓库 · 最近同日一年')])
 head(f,0,110,1,'模型派生网络全景');f.text(1000,110,'全部节点与声明边 · 2026.10.16 期后样本',17,'muted',anchor='end')
 network(f);f.line(0,515,1000,515);f.line(328,537,328,800);f.line(673,537,673,800)
 head(f,0,553,2,'派生规模继续扩大');head(f,349,553,3,'占比与数量并不同步');head(f,697,553,4,'派生还可成为新起点')
 f.text(0,587,'累计派生 / 万个',21,'blue',True);f.text(349,587,'29.14% → 28.04%',21,'violet',True)
 annual(f,0,'derived_models',100);annual(f,349,'derived_pct',35,True)
 # Explicit conceptual relationship, not fabricated records.
 f.rect(703,612,66,34,'pale');f.text(736,635,'基座 A',17,'ink',True,'middle')
 f.rect(809,612,76,34,'pale');f.text(847,635,'派生 B',17,'ink',True,'middle')
 f.rect(925,612,68,34,'pale');f.text(959,635,'后续 C',17,'ink',True,'middle')
 arrow(f,770,629,802,629);arrow(f,886,629,918,629)
 f.text(697,679,'552',30,'teal',True);f.text(775,678,'个版本兼具上下游',17)
 f.text(697,719,'50',30,'violet',True);f.text(775,718,'个版本声明多个上游',17)
 note(f,697,756,'两类重叠 16 个；上方为概念示意，角色计数来自实际边表。',300)
 f.save('fig-5-2-1')
 return page('5.2','5.2　网络与影响力','“基座”是被后续模型声明采用的上游版本，“派生”是其后续版本。沿这些关系，可以观察资源如何被接续，以及谁又成为下一轮开发的起点。','fig-5-2-1',
 '图 5-2-1　派生网络、积累与接续角色。来源：年度回溯表［1］、声明关系样本［2］。均为期后材料：年度按 2026.9.13 可见仓库回溯；网络取 2026.10.16 前 12,000 个连续非随机模型中的双端可见声明边。两组数据不拼接。',
 [('① 关系网络把供给连接到后续创造','全图保留 5,777 个模型版本、5,111 条声明关系。一个版本可以连接不同任务的后续资源；图中名称用于定位，簇群大小不代表全平台份额，声明关系仍需结合模型说明核实。'),
 ('② 再创造形成持续扩大的资源积累','最近两个年度回溯点之间，有基座声明的派生仓库由 56.38 万增至 85.87 万，增长 52.3%。后续版本扩大了可寻找的资源，也使兼容性、文档与更新责任需要沿版本链持续传递。'),
 ('③ 数量增长与占比回落可以同时发生','同期全部可见模型增长 58.3%，快于派生仓库，因此派生占比下降约 1.10 个百分点。占比回落不等于复用转弱；未声明基座的仓库也不能直接归为原创模型。'),
 ('④ 维护支持应看到中间接续者','552 个版本既承接上游又拥有下游，显示适配结果还可成为新基座；50 个版本声明多个上游。可沿这些连接核查评测、文档和问题响应，将真实维护负担落实到具体版本与团队。')],SOURCES[:2],['I03','I04','I05'])

def aggregate_flows():
 ids=['CN','US','DE','FR','GB','JP','OTH'];agg=Counter();out=Counter();inc=Counter()
 for r in FLOW:
  out[r['source']]+=r['weight'];inc[r['target']]+=r['weight']
  agg[(r['source'] if r['source'] in ids else 'OTH',r['target'] if r['target'] in ids else 'OTH')]+=r['weight']
 return ids,agg,out,inc

def sankey(f,ids,agg):
 out=Counter();inc=Counter()
 for (s,t),v in agg.items():out[s]+=v;inc[t]+=v
 orders=[sorted(ids,key=lambda k:(k=='OTH',-out[k])),sorted(ids,key=lambda k:(k=='OTH',-inc[k]))]
 top=169;bottom=459;gap=15;scale=(bottom-top-gap*6)/10943;positions=[]
 for order,totals in zip(orders,[out,inc]):
  p={};y=top
  for k in order:p[k]=[y,totals[k]*scale];y+=totals[k]*scale+gap
  positions.append(p)
 src,dst=positions;sy={k:v[0] for k,v in src.items()};ty={k:v[0] for k,v in dst.items()};ss={};tt={}
 for s in orders[0]:
  for t in orders[1]:
   if (s,t) in agg:ss[s,t]=sy[s];sy[s]+=agg[s,t]*scale
 for t in orders[1]:
  for s in orders[0]:
   if (s,t) in agg:tt[s,t]=ty[t];ty[t]+=agg[s,t]*scale
 for (s,t),v in sorted(agg.items(),key=lambda q:-q[1]):
  y=ss[s,t];yy=tt[s,t];h=v*scale
  d=f'M 184,{y} C 415,{y} 585,{yy} 816,{yy} L 816,{yy+h} C 585,{yy+h} 415,{y+h} 184,{y+h} Z'
  f.items.append(f'<path d="{d}" fill="{cl(CC[s])}" opacity="{.85 if (s,t)==("CN","US") else .48}"/>')
 for side,(order,pp,totals) in enumerate(zip(orders,positions,[out,inc])):
  ys=[pp[k][0]+pp[k][1]/2 for k in order]
  for j in range(1,len(ys)):ys[j]=max(ys[j],ys[j-1]+23)
  if ys[-1]>463:
   ys[-1]=463
   for j in range(len(ys)-2,-1,-1):ys[j]=min(ys[j],ys[j+1]-23)
  for k,y in zip(order,ys):
   actual,h=pp[k];x=173 if side==0 else 816
   f.rect(x,actual,11,h,CC[k]);f.line(x if side==0 else x+11,actual+h/2,165 if side==0 else 835,y,CC[k])
   f.text(159 if side==0 else 841,y+5,f'{COUNTRY[k]} {totals[k]:,}',18,CC[k],k in ['CN','US'],'end' if side==0 else 'start')
 f.text(173,146,'基座来源国',18,'muted');f.text(827,146,'派生发布国',18,'muted',anchor='end')
 f.text(500,205,'中国 → 美国',24,'white',True,'middle');f.text(500,237,'4,639 对 · 42.4%',22,'white',True,'middle')
 note(f,0,500,'带宽＝关系对数；颜色＝基座来源；“其他”保留全部剩余国家。方向不代表人员、资金或使用者流动。',1000)

def page_flows():
 ids,agg,out,inc=aggregate_flows();countries=set(out)|set(inc);assert len(countries)==49
 f=Figure();strip(f,[('10,943','可识别的跨国派生关系 / 对'),('49','国家 · 双端归属可识别'),('53.8%','中国基座来源 / 跨国样本'),('68.7%','美国派生发布 / 跨国样本')])
 head(f,0,111,1,'全球接续：从基座来源到派生发布');sankey(f,ids,agg)
 f.line(0,520,1000,520);f.line(328,538,328,800);f.line(673,538,673,800)
 head(f,0,557,2,'同一国家的两种角色');head(f,349,557,3,'中国基座的多个去向');head(f,697,557,4,'全球南方的参与切面')
 f.text(0,589,'国家',16,'muted');f.text(196,589,'基座来源',16,'muted',anchor='end');f.text(311,589,'派生发布',16,'muted',anchor='end')
 for i,c in enumerate(['CN','US','DE','FR']):
  y=628+i*35;f.text(0,y,COUNTRY[c],19,CC[c],True);f.text(196,y,f'{out[c]:,}',20,CC[c],True,'end');f.text(311,y,f'{inc[c]:,}',20,'ink',False,'end');f.line(0,y+10,311,y+10)
 note(f,0,770,'仅列四国；完整样本每端均为 10,943 对。',320,15)
 china=sorted([r for r in FLOW if r['source']=='CN'],key=lambda r:-r['weight'])[:4]
 f.text(349,589,'派生发布地',16,'muted');f.text(657,589,'关系 / 对',16,'muted',anchor='end')
 for i,r in enumerate(china):
  y=628+i*35;f.text(349,y,COUNTRY[r['target']],19);f.rect(416,y-12,145*r['weight']/4639,12,'china');f.text(657,y,f'{r["weight"]:,}',20,'china',True,'end')
 note(f,349,793,'美国占中国来源跨国关系的 78.8%。',310,15)
 f.text(697,589,'国家',16,'muted');f.text(891,589,'来源',16,'muted',anchor='end');f.text(993,589,'发布',16,'muted',anchor='end')
 for i,c in enumerate(['IN','BR','ID']):
  y=627+i*35;f.text(697,y,COUNTRY[c],18);f.text(891,y,str(out[c]),20,'teal',True,'end');f.text(993,y,str(inc[c]),20,'ink',False,'end');f.line(697,y+10,993,y+10)
 note(f,697,747,'印度可见德国基座接续；巴西连接美、法、中；印尼亦有基座输出。',300,16)
 f.save('fig-5-2-2')
 return page('5.2','5.2　网络与影响力：跨国接续','模型的基座来源与后续发布可以位于不同国家。把两端分开观察，能够识别中国资源进入全球再创造的路径，也能看到其他地区的接续位置。','fig-5-2-2',
 '图 5-2-2　可识别跨国派生关系的来源与去向。来源：2026.9.13 期后流向表［3］，186 个有向国家组合、10,943 对关系。地域按发布者归属；原材料国家识别覆盖约 2.59%（含境内），本图为跨国子集，不代表全球复用份额。',
 [('① 中国供给连接到全球后续创造','中国基座到美国派生发布者的 4,639 对关系，是样本中最大的单一方向，占 42.4%。这为理解中国贡献提供了具体的上下游证据；后续仍需沿模型版本核查贡献内容与反馈路径。'),
 ('② 供给节点与接续节点各有侧重','中国作为基座来源对应 5,888 对关系，作为派生发布地为 213 对；美国分别为 1,694 与 7,513 对。两种角色共同构成可见复用网络，单列某一端会遗漏另一端的再创造活动。'),
 ('③ 跨境策略可沿已有关系寻找伙伴','中国来源的跨国关系通向美国、德国、英国、法国等节点，美国占其中 78.8%。已有关系可作为联合评测、兼容维护和文档协作的入口；是否建立合作、是否形成回流，需要实际记录。'),
 ('④ 全球南方参与也具有不同路径','样本中，印度与巴西更多位于派生发布端；印度尼西亚同时有 78 对基座输出、29 对派生发布关系。这些小样本提示参与路径存在差异，尚不足以代表全球南方整体或证明本地应用成效。')],[SOURCES[2]],['I03','I04','I07','I08'])

def row(month,k):return next(r for r in M if r['month']==month and r['k']==k)
def trend(f,x,y,k,maxv):
 rows=sorted([r for r in M if r['k']==k],key=lambda r:r['month']);x0=x+42;x1=x+453;top=y+33;bottom=y+210
 xx=lambda i:x0+i*(x1-x0)/25
 f.rect((xx(11)+xx(12))/2,top,xx(23)-(xx(11)+xx(12))/2,bottom-top,'pale')
 f.rect(xx(23),top,x1-xx(23),bottom-top,'#EEF0F2')
 f.text((xx(12)+xx(23))/2,top-11,'主统计期',15,'teal',True,'middle');f.text(x1,top-11,'期后',15,'muted',False,'end')
 for v in [0,maxv/2,maxv]:
  yy=bottom-(bottom-top)*v/maxv;f.line(x0,yy,x1,yy);f.text(x0-9,yy+5,str(int(v)),15,'muted',anchor='end')
 for key,col in [('china','china'),('us','blue')]:
  pts=[(xx(i),bottom-(bottom-top)*r[key]/maxv) for i,r in enumerate(rows)]
  f.path(pts[:24],col,2.6);f.path(pts[23:],col,2.6,dash='5 4')
  for i,(px,py) in enumerate(pts):f.circle(px,py,2.2,col)
 for i,t in [(0,'24.7'),(6,'25.1'),(12,'25.7'),(18,'26.1'),(25,'26.8')]:f.text(xx(i),bottom+26,t,15,'muted',anchor='middle')
 f.text(x+42,bottom+56,f'6 月 中 {row("2026-06",k)["china"]} / 美 {row("2026-06",k)["us"]}',17,'ink',True)
 f.text(x+465,bottom+56,f'8 月 中 {row("2026-08",k)["china"]} / 美 {row("2026-08",k)["us"]}',17,'muted',False,'end')

def page_influence():
 f=Figure();strip(f,[('9 / 8','主期末 Top20 · 中 / 美席位'),('37 / 50','主期末 Top100 · 中 / 美席位'),('196 / 417','主期末 Top1000 · 中 / 美席位'),('28.0%','主期末 Top1000 · 归属未知')])
 f.line(500,95,500,789);f.line(0,449,1000,449)
 head(f,0,111,1,'期末三档榜单的地域构成');head(f,525,111,2,'Top20：最头部也有反复')
 cats=[('china','中国','china'),('us','美国','blue'),('other_known','其他已知','teal'),('unknown','未知','#A7B2BB')]
 for x,(key,name,col) in zip([0,100,202,360],cats):f.rect(x,137,13,10,col);f.text(x+20,148,name,16,'muted')
 for i,k in enumerate([20,100,1000]):
  r=row('2026-06',k);y=194+i*76
  f.text(0,y,f'Top{k}',18,'ink',True);f.text(475,y,' / '.join(str(r[key]) for key,_,_ in cats)+' 席',17,'muted',anchor='end')
  xx=0
  for key,name,col in cats:
   w=475*r[key]/k
   if w:f.rect(xx,y+14,w,24,col)
   xx+=w
 note(f,0,424,'2026.6 · 条长均为 100%；三档榜单相互包含。',480,16)
 trend(f,525,151,20,20)
 head(f,0,488,3,'Top100：长窗与年度分别判断');head(f,525,488,4,'期后信号单独保留')
 f.rect(4,509,13,10,'china');f.text(24,521,'中国',16,'muted');f.rect(110,509,13,10,'blue');f.text(130,521,'美国',16,'muted')
 trend(f,0,520,100,80)
 f.text(525,531,'月份',16,'muted');f.text(727,531,'Top20',16,'muted',anchor='end');f.text(863,531,'Top100',16,'muted',anchor='end');f.text(990,531,'未知*',16,'muted',anchor='end')
 for i,month in enumerate(['2025-07','2026-06','2026-08']):
  a=row(month,20);b=row(month,100);c=row(month,1000);y=576+i*47
  if i==2:f.rect(519,y-26,481,43,'pale')
  f.text(525,y,month.replace('-','.'),18,'ink',i==1);f.text(727,y,f'{a["china"]} / {a["us"]}',19,'ink',True,'end');f.text(863,y,f'{b["china"]} / {b["us"]}',19,'ink',True,'end');f.text(990,y,str(c['unknown']),19,'muted',False,'end');f.line(525,y+14,990,y+14)
 note(f,525,712,'中 / 美席位；* 未知为 Top1000 归属未知版本。',470,16)
 f.text(525,754,'主统计期 Top100 席位差：12 → 13',20,'teal',True)
 note(f,525,789,'较长窗口 2024.7—2026.8：59 → 3（美减中）。',470,16)
 f.save('fig-5-2-3')
 return page('5.2','5.2　网络与影响力：层次与时序','ModelRank 从模型派生与复用网络观察影响位置。“席位”指入榜模型版本数；比较不同榜单范围与月份，才能区分最头部变化和更广的生态结构。','fig-5-2-3',
 '图 5-2-3　ModelRank 国家席位的层次与月度变化。来源：2024.7—2026.8 月表［4］，26 个月、三档榜单。主期末为 2026.6；曲线浅青区为主统计期，灰区及虚线为期后。未知归属保留在分母，席位不等于影响力分值份额。',
 [('① 最头部接近，广度结构仍有差异','主期末 Top20 中，中国与美国为 9 席和 8 席；扩大到 Top100，为 37 席和 50 席。不同榜单范围揭示不同层次，同一家族可有多个版本入榜，三档席位不能相加。'),
 ('② 一个报告年度内也有多次反复','主统计期 Top20 中国席位在 6—14 席之间，美国为 5—12 席；两国席位较多的一方发生四次月间反转。单月变化适合作为继续追踪的信号，持续影响仍需连接具体版本的复用记录。'),
 ('③ 长期接近不等于年度单向增长','Top100 中美席位差在较长窗口由 59 席缩至 3 席；但本报告期首末月为 12 席与 13 席。把历史、年度和期后分别呈现，能够保留结构变化，也避免用长窗口替代年度判断。'),
 ('④ 期后变化需要连同未知归属观察','8 月 Top20 中美变为 16 席与 4 席，同时 Top1000 未知归属由 6 月的 280 席变为 330 席。应继续核查入榜版本、家族边界和归属修订；复用位置也不能替代 5.3 的开放条件核验。')],[SOURCES[3]],['I03','I04','I05'])

def render():
 pages=[page_network(),page_flows(),page_influence()];save_pages('5.2',pages);return pages
