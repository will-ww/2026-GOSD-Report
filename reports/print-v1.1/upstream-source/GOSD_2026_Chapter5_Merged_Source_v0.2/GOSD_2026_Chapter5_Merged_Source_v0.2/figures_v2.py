"""Exact, editable Chapter 5 charts. Public data and frozen report series remain separate."""
from common import *
import gzip,re,xml.etree.ElementTree as ET
import legacy51 as s51
import legacy52 as s52

S=s51.S; P=s51.P; G=s51.G
LIVE=R/'data/live'
Q=json.loads((LIVE/'api_openness_quadrant').read_text())['data']
OV=json.loads((LIVE/'api_overview_summary').read_text())['data']
QCN=[r for r in Q if r['country']=='China']
CNAMES={g['en']:(g['id'],g['name']) for g in G['world']}
CNAMES.update({'China':('CN','中国'),'United States of America':('US','美国'),'South Korea':('KR','韩国'),'United Kingdom':('GB','英国'),'Czech Republic':('CZ','捷克'),'Russia':('RU','俄罗斯'),'Turkey':('TR','土耳其'),'Kyrgyzstan':('KG','吉尔吉斯斯坦')})
CNAMES['United Arab Emirates']=('AE','阿联酋')
TYPES={'company':'企业','non-profit':'非营利／高校','university':'非营利／高校','community':'社区','user':'个人账号'}
TCOLS={'企业':'blue','非营利／高校':'teal','社区':'violet','个人账号':'#8D9EAC'}
TASKN={'Text/NLP':'语言与文本','Multimodal Chat':'多模态对话','Vision/Video/3D':'视觉／视频／3D','Speech/Audio':'语音与音频','Embedding/Retrieval':'嵌入与检索','Other':'其他任务'}
QCOL={'高完整-高开放':'teal','低完整-高开放':'blue','高完整-低开放':'orange','低完整-低开放':'#A5B2BD'}
QN={'高完整-高开放':'双高','低完整-高开放':'仅高开放','高完整-低开放':'仅高完整','低完整-低开放':'双低'}
def head(f,x,y,n,t,fs=20):f.title(x,y,str(n),t,'teal',fs)
def note(f,x,y,t,w=470,fs=16):return f.wrap(x,y,t,w,fs,'muted',leading=23)
def strip(f,items):
 f.rect(0,0,1000,74,'pale')
 for i,(v,t) in enumerate(items):
  x=18+250*i
  if i:f.line(x-18,14,x-18,60)
  f.text(x,38,v,28,'teal',True);f.text(x,61,t,16,'muted')
def countryname(k):return CNAMES.get(k,('',k))[1]
def stats(rows):
 return {'n':len(rows),'open':sum(r['openness_num']>=2 for r in rows),'complete':sum(r['strict_completeness_num']>=3 for r in rows),'both':sum(r['openness_num']>=2 and r['strict_completeness_num']>=3 for r in rows)}
def rect_path_bounds(geos):
 pts=[]
 for g in geos:
  for cmd,ss in re.findall(r'([MLZ])([^MLZ]*)',g['d']):
   if cmd!='Z':
    v=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',ss)];pts+=list(zip(v[::2],v[1::2]))
 return min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)
def world(f,x,y,w,h,values,color='blue',log=True,labels=None,maxv=None):
 geos=[g for g in G['world'] if g['id']!='AQ'];a,b,c,d=rect_path_bounds(geos)
 sc=min(w/(c-a),h/(d-b));tx=x+(w-(c-a)*sc)/2-a*sc;ty=y+(h-(d-b)*sc)/2-b*sc
 maximum=maxv or max(values.values(),default=1)
 f.items.append(f'<g transform="translate({tx},{ty}) scale({sc})">')
 for g in geos:
  k='CN' if g['id'] in ['TW','HK','MO'] else g['id'];v=values.get(k)
  t=(math.log1p(v)/math.log1p(maximum) if log else v/maximum) if v is not None else 0
  col=mix('#DFEDF2',color,min(1,t)) if v is not None else '#F0F3F5'
  f.items.append(f'<path d="{g["d"]}" fill="{col if g.get("kind")!="line" else "none"}" stroke="#A9B6BF" stroke-width="{.55/sc}"/>')
 f.items.append('</g>')
 centers={g['id']:(tx+g['center'][0]*sc,ty+g['center'][1]*sc) for g in geos if g.get('center')}
 for code,label,dx,dy in labels or []:
  if code not in centers:continue
  px,py=centers[code];lx=px+dx;ly=py+dy;ww=tw(label,17,True)
  if dx or dy:f.line(px,py,lx,ly-5,'muted',.8)
  f.rect(lx-ww/2-4,ly-17,ww+8,23,'white',.94);f.text(lx,ly,label,17,'ink',True,'middle')
 return centers
def maplegend(f,x,y,label,color='blue',log=True):
 for i in range(6):f.rect(x+i*22,y-12,22,11,mix('#DFEDF2',color,i/5))
 f.text(x+143,y,label,15,'muted');f.rect(x+365,y-12,13,11,'#F0F3F5');f.text(x+386,y,'样本未覆盖',15,'muted')
def small_line(f,x,y,w,h,values,labels,color,maxv,unit='',endlabels=True):
 x0=x+34;x1=x+w-16;top=y+15;bottom=y+h-31
 for v in [0,maxv/2,maxv]:
  yy=bottom-(bottom-top)*v/maxv;f.line(x0,yy,x1,yy);f.text(x0-7,yy+5,f'{v:g}',14,'muted',anchor='end')
 pts=[(x0+i*(x1-x0)/(len(values)-1),bottom-v/maxv*(bottom-top)) for i,v in enumerate(values)]
 f.path([(x0,bottom)]+pts+[(x1,bottom)],color,0,fill=color,opacity=.06);f.path(pts,color,2.8)
 for i,((px,py),v) in enumerate(zip(pts,values)):
  f.circle(px,py,3,color)
  if endlabels:f.text(px,py-10,f'{v:.1f}',15,color,True,'middle')
  f.text(px,bottom+24,labels[i],15,'muted',anchor='middle')

def supply_map():
 f=Figure();strip(f,[('322.61 万','平台模型仓库 · 本次读取'),('112.41 万','平台数据集 · 本次读取'),('73,088','地域样本模型 · 冻结快照'),('826','已关联国家的组织账号')])
 head(f,0,110,1,'模型供给的全球位置');head(f,690,110,2,'模型数量前 15 位')
 rows=sorted(S['assets']['models']['countries'],key=lambda r:-r['models']);vals={r['code']:r['models'] for r in rows if r['models']>0}
 world(f,0,146,663,335,vals,labels=[('US','美国',0,5),('CN','中国',0,5),('FR','法国',-36,-3),('IN','印度',4,12),('BR','巴西',0,0)])
 f.text(0,138,'按发布组织归属定位 · 模型仓库数量',17,'muted')
 maplegend(f,15,502,'低 → 高 · 对数色阶')
 f.text(690,140,'国家',15,'muted');f.text(997,140,'模型 / 个',15,'muted',anchor='end')
 for i,r in enumerate(rows[:15]):
  yy=166+i*23
  if i%2==0:f.rect(685,yy-16,315,22,'pale')
  f.text(690,yy,f'{i+1:02}',14,'muted');f.text(722,yy,'阿联酋' if r['code']=='AE' else r['name_zh'],16,'ink',r['code'] in ['CN','US'])
  f.rect(802,yy-11,88*r['models']/46314,8,'blue',.7);f.text(995,yy,fmt(r['models']),17,'blue',r['code'] in ['CN','US'],'end')
 f.line(675,125,675,505);f.line(0,525,1000,525)
 head(f,0,563,3,'模型与数据供给的地域结构');head(f,525,563,4,'数量与获取活动呈现不同重心')
 cats=[('US','美国','blue'),('CN','中国','china'),('FR','法国','teal'),('OTHER','其余','soft')]
 for i,(_,name,col) in enumerate(cats):f.rect(i*115,582,12,11,col);f.text(i*115+18,594,name,16,'muted')
 for i,asset in enumerate(['models','datasets']):
  rr=S['assets'][asset]['countries'];den=S['assets'][asset]['summary'][asset];v={r['code']:r[asset] for r in rr}
  y=630+i*77;f.text(0,y,'模型仓库' if i==0 else '数据集',18,'ink',True);f.text(474,y,f'{den:,} 个',18,'muted',anchor='end');xx=0
  for code,_,col in cats:
   n=v.get(code,den-sum(v[k] for k in ['US','CN','FR']));ww=474*n/den;f.rect(xx,y+13,ww,26,col)
   if ww>48:f.text(xx+ww/2,y+32,f'{n/den*100:.1f}%',15,'white',True,'middle')
   xx+=ww
 for i,(label,n,den,col) in enumerate([('中美模型数',52407,73088,'blue'),('中美模型下载',sum(r['downloads'] for r in rows if r['code'] in ['US','CN']),S['assets']['models']['summary']['downloads'],'teal')]):
  y=618+i*69;f.text(525,y,label,18);f.text(995,y,f'{n/den*100:.1f}%',25,col,True,'end');f.rect(525,y+17,470,14,'pale');f.rect(525,y+17,470*n/den,14,col)
 note(f,0,789,'地域样本固定于 2026.10.17；数据集沿用同一组织名录。',490,15)
 note(f,525,767,'下载按来源累计口径；反映资源获取活动，不能解释为独立用户、部署量或性能。',470,16)
 f.save('fig-5-1-1')

def publisher_growth():
 f=Figure();head(f,0,26,1,'模型发布者 · 中美累计下载各前六')
 maxv=max(s51.top('models','CN')[0]['models']['downloads'],s51.top('models','US')[0]['models']['downloads'])
 for x,co in [(0,'CN'),(525,'US')]:s51.rank_group(f,x,59,'models',co,maxv,1e8)
 f.line(0,251,1000,251);head(f,0,282,2,'数据发布者 · 中美累计下载各前六')
 maxv=max(s51.top('datasets','CN')[0]['datasets']['downloads'],s51.top('datasets','US')[0]['datasets']['downloads'])
 for x,co in [(0,'CN'),(525,'US')]:s51.rank_group(f,x,315,'datasets',co,maxv,1e4)
 f.line(0,508,1000,508);f.line(500,530,500,795)
 head(f,0,546,3,'仓库与发布账号同步积累');head(f,525,546,4,'模型与数据持续进入生态')
 f.text(0,578,'模型 / 万个  +58.3%',18,'blue',True);f.text(257,578,'账号 / 万个  +48.4%',18,'violet',True)
 a=s51.A;labels=[r['date'][2:4] for r in a]
 small_line(f,0,601,232,157,[int(r['models'])/1e4 for r in a],labels,'blue',350)
 small_line(f,252,601,232,157,[int(r['publishers'])/1e4 for r in a],labels,'violet',70)
 note(f,0,789,'2022—2026 各年 9 月 13 日；据终点可见仓库回溯。',485,15)
 x0=565;x1=982;top=604;bottom=743
 vals={k:[r for r in S['global'][k]['monthlyNew'] if '2024-07'<=r['month']<='2026-06'] for k in ['models','datasets']}
 xx=lambda i:x0+i*(x1-x0)/23
 f.rect((xx(11)+xx(12))/2,top,x1-(xx(11)+xx(12))/2,bottom-top,'pale')
 for yv in [0,5,10,15]:
  yy=bottom-yv/15*(bottom-top);f.line(x0,yy,x1,yy);f.text(x0-8,yy+5,str(yv),14,'muted',anchor='end')
 for k,col in [('models','blue'),('datasets','teal')]:
  pts=[(xx(i),bottom-r['count']/1e4/15*(bottom-top)) for i,r in enumerate(vals[k])];f.path(pts,col,2.6)
  peak=max(range(12,24),key=lambda i:vals[k][i]['count']);px,py=pts[peak];f.circle(px,py,3.5,col);f.text(px,py-9,f"{vals[k][peak]['count']/1e4:.2f}",16,col,True,'middle')
 for i,t in [(0,'24.7'),(6,'25.1'),(12,'25.7'),(18,'26.1'),(23,'6 月')]:f.text(xx(i),767,t,15,'muted',anchor='middle')
 f.text(525,578,'月度新增 / 万个',17,'muted');f.rect(690,566,11,10,'blue');f.text(708,578,'模型',16,'blue');f.rect(768,566,11,10,'teal');f.text(786,578,'数据',16,'teal');f.text(994,578,'浅底为主统计期',15,'muted',anchor='end')
 note(f,525,789,'主期合计：模型 112.67 万；数据 52.04 万。',470,15)
 f.save('fig-5-1-2')

def china_supply():
 # Retain the approved map and provincial comparison, replace redundant aggregation with named resource providers.
 s51.china_page();path=F/'fig-5-1-3.svg';root=ET.parse(path).getroot()
 # Regenerate through an override instead of altering pixels.
 f=Figure();strip(f,[('147','中国样本 · 组织账号'),('6,093','中国样本 · 模型仓库'),('1,354','同一组织名录 · 数据集'),('88.8%','京沪浙粤模型数 / 全国样本')])
 head(f,0,111,1,'模型资源的省级分布');head(f,550,111,2,'组织、模型与数据并非同序');s51.china_map(f,0,137,517,290)
 maplegend(f,3,451,'模型数 · 对数色阶')
 cm=s51.country('models');cd=s51.country('datasets');mr=s51.divisions('models');dr={r['code']:r for r in s51.divisions('datasets')}
 for x,t in [(550,'地区'),(710,'组织'),(850,'模型'),(985,'数据集')]:f.text(x,147,t,17,'muted',anchor='start' if x==550 else 'end')
 data=sorted([r for r in mr if r['organizations']>0],key=lambda r:-r['models'])+[{'code':'unknown','name_zh':'归属待补',**cm['unassignedDivision']}]
 for i,r in enumerate(data):
  y=179+i*28;name=r['name_zh'].replace('特别行政区','').replace('省','').replace('市','');name='台湾省' if r['code']=='CN-TW' else name;ds=dr.get(r['code'],cd['unassignedDivision'])
  f.text(550,y,name,18);f.text(710,y,fmt(r['organizations']),18,'muted',anchor='end');f.text(850,y,fmt(r['models']),18,'blue',True,'end');f.text(985,y,fmt(ds['datasets']),18,'teal',True,'end');f.line(550,y+9,985,y+9)
 f.line(530,128,530,455);f.line(0,470,1000,470);f.line(500,492,500,790)
 head(f,0,510,3,'把资源优势落实到发布者');head(f,525,510,4,'模型与数据形成不同区域重心')
 for x,t in [(0,'地区'),(96,'模型获取首位账号'),(302,'数据获取首位账号')]:f.text(x,550,t,15,'muted')
 for i,code in enumerate(['CN-ZJ','CN-BJ','CN-SH','CN-GD']):
  prs=[p for p in P if code in p['divisionCodes']];m=max(prs,key=lambda p:p['models']['downloads']);d=max(prs,key=lambda p:p['datasets']['downloads']);yy=590+i*43
  f.text(0,yy,{'CN-ZJ':'浙江','CN-BJ':'北京','CN-SH':'上海','CN-GD':'广东'}[code],18,'ink',True);f.text(96,yy,m['name'],17,'blue');f.text(302,yy,d['name'],17,'teal');f.line(0,yy+13,475,yy+13)
 note(f,0,768,'分别按本地两类资产累计下载排序，定位合作入口；同一地区不必由同一主体承担两类供给。',480,16)
 f.rect(525,536,13,10,'blue');f.text(547,547,'模型下载占比',16,'muted');f.rect(764,536,13,10,'teal');f.text(786,547,'数据下载占比',16,'muted')
 for i,code in enumerate(['CN-BJ','CN-SH','CN-ZJ','CN-GD']):
  r=next(r for r in mr if r['code']==code);y=586+i*43;f.text(525,y+8,r['name_zh'].replace('省','').replace('市',''),18)
  for j,(val,total,col) in enumerate([(r['downloads'],cm['downloads'],'blue'),(dr[code]['downloads'],cd['downloads'],'teal')]):
   v=val/total*100;f.rect(584,y-8+j*16,290*v/60,10,col);f.text(985,y+2+j*16,f'{v:.1f}%',17,col,True,'end')
 note(f,525,783,'各以中国样本相应资产累计下载为分母。',470,16);f.save('fig-5-1-3')

def derivation_network():
 f=Figure();strip(f,[('5,777','实际网络 · 模型版本'),('5,111','基座 → 派生 · 声明边'),('552','同时承接上游并拥有下游'),('50','声明多个上游的版本')])
 head(f,0,107,1,'读懂派生：一次接续，也可成为新的起点')
 # Two upstreams merge into one derivation, then another; diagram is explicitly conceptual.
 for x,y,w,t in [(0,124,150,'基座 A'),(0,169,150,'基座 B'),(302,145,180,'派生版本'),(671,145,180,'后续派生')]:
  f.rect(x,y,w,33,'pale');f.text(x+w/2,y+23,t,18,'ink',True,'middle')
 s52.arrow(f,155,141,295,158);s52.arrow(f,155,185,295,168);s52.arrow(f,487,162,663,162)
 f.text(191,194,'允许多个上游',15,'muted');f.text(524,194,'派生可再作基座',15,'muted');f.text(1000,130,'关系示意',15,'muted',anchor='end')
 f.line(0,217,1000,217);head(f,0,249,2,'模型网络全景');f.text(1000,249,'颜色＝任务；节点面积随直接下游数增大',16,'muted',anchor='end')
 pts={n['id']:(498+520*float(n['x']),435+170*float(n['y'])) for n in s52.N}
 for e in s52.E:f.path([pts[e['source']],pts[e['target']]],s52.TC[s52.task(s52.NB[e['source']])],.65,opacity=.25)
 for n in sorted(s52.N,key=lambda n:int(n['downstreamCount'])):
  x,y=pts[n['id']];rad=math.sqrt(1.25+int(n['downstreamCount'])*.30);f.items.append(f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{cl(s52.TC[s52.task(n)])}" opacity=".88"/>')
 labels=[('Qwen/Qwen-Image-2.1',0,320,'start'),('Qwen/Qwen3-0.6B',0,455,'start'),('openai/whisper-large-v3',60,588,'start'),('Qwen/Qwen3.8-Flash-Next',460,285,'start'),('Qwen/Qwen3.8-27B',775,390,'start'),('zai-org/GLM-5.3-Flash',995,466,'end'),('MiniMaxAI/MiniMax-H3',995,588,'end')]
 for id,x,y,anchor in labels:
  n=s52.NB[id];t=n['name'];w=tw(t,17);left=x if anchor=='start' else x-w
  f.line(*pts[id],x,y-6,s52.TC[s52.task(n)],.9);f.rect(left-3,y-18,w+6,24,'white',.94);f.text(x,y,t,17,'ink',False,anchor)
 for x,(_,name,col) in zip([0,160,300,490,620,800],s52.TASKS):f.circle(x+5,617,4,col);f.text(x+17,623,name,16,'muted')
 f.line(0,640,1000,640);head(f,0,671,3,'有基座声明的仓库持续增长');head(f,534,671,4,'复用链把适配者变成新供给者')
 a=s52.A
 for i,r in enumerate(a):
  x=i*99;v=int(r['derived_models'])/1e4;h=73*v/90;f.rect(x+18,762-h,45,h,'blue');f.text(x+40,755-h,f'{v:.2f}',16,'blue',True,'middle');f.text(x+40,786,r['date'][:4],15,'muted',anchor='middle')
 f.text(501,698,'万个',15,'muted',anchor='end')
 f.text(534,710,'552',30,'blue',True);f.text(620,707,'个版本既承接上游，也连接下游',17)
 f.text(534,751,'50',30,'teal',True);f.text(620,748,'个版本连接多个上游来源',17)
 note(f,534,786,'两类重合 16 个；角色计数不可直接相加。',465,16)
 f.save('fig-5-2-1')

def crossborder():
 f=Figure();strip(f,[('10,943','可识别跨国派生关系 / 对'),('49','国家 · 来源与去向可识别'),('53.8%','中国基座来源 / 跨国样本'),('68.7%','美国派生发布 / 跨国样本')])
 head(f,0,110,1,'从基座供给，到全球再创造')
 ids,agg,out,inc=s52.aggregate_flows()
 # Full Sankey retains every directed relationship; map adds a geographic navigation view.
 total=sum(agg.values());gap=12;scale=(310-gap*(len(ids)-1))/total
 left={};right={};yl=170;yr=170
 for co in ids:
  a=sum(v for (s,t),v in agg.items() if s==co);b=sum(v for (s,t),v in agg.items() if t==co)
  left[co]=[yl,a*scale];right[co]=[yr,b*scale];yl+=a*scale+gap;yr+=b*scale+gap
 ly={co:yy for co,(yy,h) in left.items()};ry={co:yy for co,(yy,h) in right.items()}
 for s in ids:
  for t in ids:
   v=agg.get((s,t),0)
   if not v:continue
   a=ly[s];b=ry[t];h=v*scale
   f.items.append(f'<path d="M125,{a} C250,{a} 360,{b} 490,{b} L490,{b+h} C360,{b+h} 250,{a+h} 125,{a+h} Z" fill="{cl(s52.CC[s])}" opacity=".58"/>')
   if s=='CN' and t=='US':
    f.text(308,(a+b+h)/2-5,'中国 → 美国',22,'white',True,'middle');f.text(308,(a+b+h)/2+23,'4,639 对',25,'white',True,'middle')
   ly[s]+=h;ry[t]+=h
 for co in ids:
  a,h=left[co];b,hh=right[co];f.rect(117,a,8,h,s52.CC[co]);f.rect(490,b,8,hh,s52.CC[co])
  f.text(108,a+h/2+5,f'{s52.COUNTRY[co]} {sum(v for (s,t),v in agg.items() if s==co):,}',16,'ink',co=='CN','end')
  f.text(507,b+hh/2+5,f'{s52.COUNTRY[co]} {sum(v for (s,t),v in agg.items() if t==co):,}',16,'ink',co=='US')
 f.text(117,149,'基座来源',17,'muted');f.text(490,149,'派生发布',17,'muted')
 f.text(0,506,'带宽＝关系对数；颜色＝基座来源；其余国家合并保留。',15,'muted')
 head(f,625,110,2,'主要跨境路径的地理位置',18)
 centers=world(f,620,145,380,220,{k:out[k]+inc[k] for k in set(out)|set(inc)},color='teal')
 for s,t in [('CN','US'),('DE','US'),('FR','US'),('US','CN')]:
  v=next(r['weight'] for r in s52.FLOW if r['source']==s and r['target']==t);x,y=centers[s];xx,yy=centers[t];cy=min(y,yy)-35-(10 if s=='US' else 0)
  f.items.append(f'<path d="M{x},{y} Q{(x+xx)/2},{cy} {xx},{yy}" fill="none" stroke="{cl(s52.CC[s])}" stroke-width="{1+4*v/4639}" opacity=".72"/>');s52.arrow(f,xx-4 if xx>x else xx+4,yy-2,xx,yy,s52.CC[s])
 for co,dx,dy in [('CN',25,14),('US',-15,28),('DE',20,-19),('FR',-24,20)]:
  x,y=centers[co];f.circle(x,y,3.5,s52.CC[co]);f.text(x+dx,y+dy,s52.COUNTRY[co],16,'ink',True,'middle')
 f.text(625,397,'中国 → 美国',20,'china',True);f.text(995,397,'4,639 对',22,'china',True,'end')
 note(f,625,433,'占全部跨国样本 42.4%。地图仅突出四条路径；左图保留全部计数。',370,17)
 f.line(0,516,1000,516);f.line(500,540,500,800)
 head(f,0,552,3,'同一国家的两种协作角色');head(f,525,552,4,'南方参与：接续与供给并存')
 for x,t in [(0,'国家'),(300,'基座来源'),(471,'派生发布'),(525,'国家'),(820,'基座来源'),(995,'派生发布')]:f.text(x,590,t,16,'muted',anchor='start' if x in [0,525] else 'end')
 for i,co in enumerate(['CN','US','DE','FR','GB']):
  y=624+i*32;f.text(0,y,s52.COUNTRY[co],18,s52.CC[co],True);f.text(300,y,fmt(out[co]),20,s52.CC[co],True,'end');f.text(471,y,fmt(inc[co]),20,'ink',False,'end');f.line(0,y+10,475,y+10)
 for i,co in enumerate(['IN','BR','ID']):
  y=627+i*39;f.text(525,y,s52.COUNTRY[co],18);f.text(820,y,fmt(out[co]),21,'teal',True,'end');f.text(995,y,fmt(inc[co]),21,'ink',False,'end');f.line(525,y+12,995,y+12)
 note(f,525,757,'印度、巴西更多出现在派生端；印尼亦是可见上游。合作应按具体角色寻找伙伴。',470,17)
 f.save('fig-5-2-2')

def framework():
 f=Figure();f.rect(0,0,1000,69,'pale');f.text(18,30,'先确认一个具体模型版本，再分别问两个问题',25,'teal',True);f.text(18,55,'材料是否足够？使用权利是否明确？两条轴独立记录，不合成为一个总分。',18,'muted')
 head(f,0,104,1,'完整性 L：再创造能走到哪一步');head(f,650,104,2,'开放性 O：允许怎样使用')
 f.line(625,87,625,550)
 levs=[('L1','能部署','权重、配置、分词器','推理脚本与运行环境'),('L2','能理解','模型原理、训练过程','测试结果与已知局限'),('L3','能再训练','训练代码、环境、数据','或完整来源与处理规则'),('L4','能验证','测试代码、数据与环境','训练／测试无重叠说明'),('L5','能全链复现','清洗与处理脚本、数据配方','从数据准备到部署的复现指引')]
 for i,(lv,name,a,b) in enumerate(levs):
  yy=134+i*76;x=14+i*12;col=mix('blue','teal',i/4);f.rect(x,yy,590-x,67,'pale');f.rect(x,yy,50,67,col);f.text(x+25,yy+39,lv,22,'white',True,'middle');f.text(x+64,yy+28,name,20,col,True);f.text(258,yy+25,a,17);f.text(258,yy+50,b,17,'muted')
 note(f,15,545,'逐级累积：高等级包含此前各级要求；仍须运行验证。',591,16)
 op=[('O1','有限制开放','核对用途、商业化与再分发限制。'),('O2','互惠开放','衍生再分发须延续相同或兼容许可。'),('O3','宽松开放','广泛授权，保留署名与许可等义务。'),('O4','零义务开放','无额外合同义务；法定义务仍适用。')]
 for i,(lv,name,desc) in enumerate(op):
  y=151+i*88;f.circle(673,y-7,21,mix('blue','teal',i/3));f.text(673,y,lv,18,'white',True,'middle');f.text(710,y,name,20,'ink',True);note(f,651,y+31,desc,346,17)
 f.rect(646,491,354,54,'pale');note(f,657,514,'核心许可不能核实，应标待核；不能自动降为 O1。',332,16)
 f.line(0,569,1000,569);head(f,0,606,3,'怎样读出一个版本的开放条件');head(f,525,606,4,'怎样将公开材料变成可用能力')
 f.text(0,654,'L2 + O3',38,'blue',True);f.text(232,652,'示意组合',17,'muted')
 note(f,0,694,'能够部署并理解，许可较宽松；仍不能据此认定训练与全链复现材料已经齐备。',470,18)
 f.text(0,774,'比较分组：高完整 L3—L5；高开放 O2—O4',16,'muted')
 steps=[('查材料','逐条记录版本与出处'),('跑验证','按公开环境完成规定验证'),('查许可','对相应材料逐项比对权利')]
 for i,(a,b) in enumerate(steps):
  yy=649+i*48;f.circle(540,yy-5,12,'teal');f.text(540,yy+1,i+1,15,'white',True,'middle');f.text(563,yy,a,18,'teal',True);f.text(650,yy,b,17)
 f.save('fig-5-3-1')

def geography_actors():
 f=Figure();strip(f,[('889','开放评价 · 模型记录'),('25','有记录的国家和地区'),('244','平台发布主体标签'),('64','地域归属未知 · 保留分母')])
 head(f,0,109,1,'全球模型评价样本的地理分布');head(f,682,109,2,'有记录国家前 15 位')
 by=defaultdict(list)
 for r in Q:by[r['country']].append(r)
 vals={CNAMES[k][0]:len(v) for k,v in by.items() if k in CNAMES}
 world(f,0,145,652,312,vals,labels=[('CN','中国 415',10,8),('US','美国 263',-8,5),('FR','法国 36',-38,8),('IN','印度 6',0,21),('KR','韩国 28',45,-24)])
 maplegend(f,0,487,'模型数 · 对数色阶')
 countries=sorted([(k,len(v)) for k,v in by.items() if k!='Unknown'],key=lambda q:(-q[1],q[0]))
 for i,(co,n) in enumerate(countries[:15]):
  y=143+i*24;f.text(682,y,f'{i+1:02}',14,'muted');f.text(714,y,countryname(co),16);f.rect(831,y-10,94*n/415,9,'blue');f.text(995,y,str(n),18,'blue',True,'end')
 f.line(667,125,667,496);f.line(0,515,1000,515);f.line(479,536,479,798)
 head(f,0,551,3,'企业与公共研究的交付结构');head(f,502,551,4,'不同地域的主体组合')
 f.text(0,583,'发布主体',16,'muted');f.text(295,583,'记录',16,'muted',anchor='end');f.text(458,583,'其中双高',16,'muted',anchor='end')
 for i,typ in enumerate(['企业','非营利／高校','社区','个人账号']):
  rr=[r for r in Q if TYPES[r['org_type']]==typ];st=stats(rr);yy=623+i*44
  f.text(0,yy,typ,17);f.rect(129,yy-12,98*len(rr)/728,12,TCOLS[typ]);f.text(295,yy,str(st['n']),21,TCOLS[typ],True,'end');f.text(458,yy,f"{st['both']} / {st['both']/st['n']*100:.1f}%",18,'teal',True,'end')
 note(f,0,792,'“双高”＝高完整且高开放；比例以本类记录为分母。',470,15)
 types=['企业','非营利／高校','社区','个人账号'];xs=[681,788,890,982]
 for x,t in zip(xs,['企业','非营利/高校','社区','个人']):f.text(x,583,t,14,'muted',anchor='end')
 for i,(co,n) in enumerate(countries[:7]):
  yy=614+i*26;rr=by[co];f.text(502,yy,countryname(co),16)
  for x,t in zip(xs,types):
   v=sum(TYPES[r['org_type']]==t for r in rr);f.rect(x-77,yy-16,85,23,mix('white',TCOLS[t],.08+.48*v/n));f.text(x,yy,str(v),16,'ink',True,'end')
 f.save('fig-5-3-2')

def openness_world():
 st=stats(Q);f=Figure();strip(f,[('69.4%','高开放 · 617 / 889'),('19.7%','高完整 · 175 / 889'),('13.2%','两项均高 · 117 / 889'),('49.3%','最大单元 L2—O3 · 438 条')])
 head(f,0,109,1,'完整材料的地域分布');head(f,600,109,2,'使用权限与完整交付并不同步')
 by=defaultdict(list)
 for r in Q:by[r['country']].append(r)
 vals={CNAMES[k][0]:stats(v)['complete']/len(v)*100 for k,v in by.items() if k in CNAMES}
 world(f,0,144,565,285,vals,color='teal',log=False,maxv=100,labels=[('CN','中国 16.4%',10,16),('US','美国 27.0%',0,0),('FR','法国 13.9%',-32,-5),('KR','韩国 7.1%',29,-26)])
 maplegend(f,0,458,'高完整比例 · 0—100%','teal',False)
 f.text(0,493,'比例按各国样本计算；小样本地区需结合数量解读。',15,'muted')
 f.rect(600,130,12,10,'blue');f.text(620,142,'高开放',15,'blue');f.rect(736,130,12,10,'teal');f.text(756,142,'其中双高',15,'teal');f.text(997,142,'样本数',15,'muted',anchor='end')
 for i,co in enumerate(['China','United States of America','France','South Korea','Germany','United Kingdom']):
  a=stats(by[co]);y=181+i*51;f.text(600,y,countryname(co),17);f.text(997,y,str(a['n']),16,'muted',anchor='end')
  for j,(key,col) in enumerate([('open','blue'),('both','teal')]):
   v=a[key]/a['n']*100;f.rect(686,y-13+j*17,210*v/100,10,col);f.text(954,y-2+j*17,f'{v:.1f}%',16,col,True,'end')
 f.line(0,516,1000,516);f.line(548,540,548,797)
 head(f,0,553,3,'全球完整性 × 开放性矩阵');head(f,572,553,4,'从“可用权利”走向“可复现材料”')
 xs=[162,267,372,477]
 for x,op in zip(xs,['O1','O2','O3','O4']):f.text(x,593,op,17,'muted',True,'middle')
 mat=Counter((r['strict_completeness_num'],r['openness_num']) for r in Q)
 for i,lv in enumerate([5,4,3,2,1]):
  y=617+i*32;f.text(0,y+21,f'L{lv} '+{1:'部署',2:'理解',3:'训练',4:'验证',5:'全链'}[lv],17,'ink',True)
  for x,op in zip(xs,range(1,5)):
   v=mat[lv,op];col=mix('white','teal' if lv>=3 else 'blue',.06+.84*math.log1p(v)/math.log1p(438));f.rect(x-48,y,96,28,col);f.text(x,y+21,str(v),18,'white' if v>90 else 'ink',True,'middle')
 f.text(572,598,'617 条高开放记录',24,'blue',True);f.rect(572,618,424,29,mix('white','blue',.22));f.rect(572,618,424*117/617,29,'teal');f.text(572,678,'117 条同时达到高完整',22,'teal',True);f.text(995,712,'19.0%',39,'teal',True,'end')
 note(f,572,745,'另外 500 条停留于 L1—L2。共同维护训练配方、数据说明和复现环境，是开放之后的重要增量工作。',424,17)
 f.save('fig-5-3-3')

def openness_china():
 f=Figure();strip(f,[('415','中国模型记录 · 46.7% 样本'),('354','高开放 · 中国样本 85.3%'),('68','高完整 · 中国样本 16.4%'),('56','双高 · 中国样本 13.5%')])
 head(f,0,110,1,'主要发布主体与材料完整性');head(f,560,110,2,'中国样本：开放权限与交付层级')
 org=defaultdict(list)
 for r in QCN:org[r['story_org']].append(r)
 orgs=sorted(org.items(),key=lambda p:(-len(p[1]),p[0]))[:12]
 lcols=['#D5E2EA','blue','teal','violet','#9D6E2B']
 for i,col in enumerate(lcols):f.rect(i*93,132,12,10,col);f.text(i*93+19,144,f'L{i+1}',15,'muted')
 for i,(name,rows) in enumerate(orgs):
  y=177+i*26;f.text(0,y,name,16,'ink',i<4);xx=167
  for lv in range(1,6):
   n=sum(r['strict_completeness_num']==lv for r in rows);w=277*n/113;f.rect(xx,y-12,w,14,lcols[lv-1]);xx+=w
  f.text(510,y,str(len(rows)),18,'ink',True,'end')
 f.line(535,125,535,478)
 mat=Counter((r['strict_completeness_num'],r['openness_num']) for r in QCN);xs=[686,799,912]
 for x,t in zip(xs,['O1','O2','O3']):f.text(x,151,t,17,'muted',True,'middle')
 for i,lv in enumerate([5,4,3,2,1]):
  yy=174+i*42;f.text(560,yy+25,f'L{lv}',18,'ink',True)
  for x,op in zip(xs,[1,2,3]):
   v=mat[lv,op];f.rect(x-48,yy,96,34,mix('white','teal' if lv>=3 else 'blue',.05+.85*math.log1p(v)/math.log1p(287)));f.text(x,yy+25,str(v),20,'white' if v>50 else 'ink',True,'middle')
 f.text(560,425,'中国高开放记录中，15.8% 达到双高',20,'teal',True);note(f,560,457,'O4 本次无记录；保留平台主体标签，按模型版本逐项计数。',439,16)
 f.line(0,499,1000,499);f.line(500,520,500,800)
 head(f,0,537,3,'供给已经覆盖多类模型任务');head(f,525,537,4,'把评价落到具体版本与材料')
 ts=Counter(r['task_category'] for r in QCN)
 for i,(task,n) in enumerate(ts.most_common()):
  yy=581+i*32;f.text(0,yy,TASKN[task],17);f.rect(157,yy-12,230*n/162,13,'blue');f.text(474,yy,str(n),19,'blue',True,'end')
 note(f,0,797,'任务标签来自来源；一条模型记录归入一个任务组。',480,15)
 ev=json.loads((LIVE/'grid889.json').read_text()) if (LIVE/'grid889.json').exists() else json.loads((LIVE/'api_openness_grid').read_text())['data']['rows']
 byid={r['model_id']:r for r in ev}
 cases=[('Qwen/Qwen3-0.6B','Qwen3-0.6B'),('deepseek-ai/DeepSeek-R1','DeepSeek-R1'),('BAAI/bge-m3','bge-m3')]
 keys=['L1_weights','L3_train_code','L3_train_data','L4_eval_code'];xx=[734,807,880,953]
 for x,t in zip(xx,['权重','训练代码','训练数据','评测代码']):f.text(x,579,t,13,'muted',anchor='middle')
 for i,(id,label) in enumerate(cases):
  yy=620+i*50;r=byid[id];f.text(525,yy,label,17,'ink',True)
  for x,key in zip(xx,keys):
   value=r['indicators'][key] if r else 'missing';col={'complete':'teal','partial':'orange','missing':'#C0CBD2'}.get(value,'#C0CBD2');f.circle(x,yy-6,8,col)
  if r:f.text(525,yy+20,r['strict_final_grade']+' · 来源评估',14,'muted')
 for x,label,col in [(525,'完整','teal'),(642,'部分','orange'),(760,'未找到充分证据','#C0CBD2')]:f.circle(x+5,773,5,col);f.text(x+17,779,label,15,'muted')
 f.save('fig-5-3-4')

def main():
 supply_map();publisher_growth();china_supply();derivation_network();crossborder();s52.page_influence();framework();geography_actors();openness_world();openness_china()
 # Only retain the final pass per figure in the QA ledger.
 q={r['figure']:r for r in QA};(R/'review/figure-qa.json').write_text(json.dumps(list(q.values()),ensure_ascii=False,indent=2));print(json.dumps({k:{'outside':len(v['out_of_bounds']),'overlaps':len(v['overlaps'])} for k,v in q.items()},ensure_ascii=False))
if __name__=='__main__':main()
