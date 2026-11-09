from pathlib import Path
import json,math,base64,html,subprocess,xml.etree.ElementTree as ET
from PIL import Image,ImageFont
R=Path(__file__).resolve().parents[1];O=R/'figures/atlas';O.mkdir(exist_ok=True)
D=json.loads((R/'content/atlas_data.json').read_text());F=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',100,index=2);B=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',100,index=2)
INK='#142C49';MUTED='#536B7D';LINE='#D7E4EA';ACC='#955A3C';QA=[];allgeo=[]
meta={
'41a':('86 个项目 · 12 个类别 · 固定观察名单','由任务入口进入编排、工具和运行条件。相邻位置表达功能分工。',['来源：Agentic AI Landscape 固定版本 e330d75；沿用 145 项主归类中的 Agent Infra。','期后固定名单，不等于主期末名录；统计图另取 2025-07 至 2026-06。头像用于识别账户。'],1),
'41b':('59 个项目 · 13 个类别 · 固定观察名单','由模型服务进入训练、数据和计算支撑，与前页任务入口相接。',['来源：Agentic AI Landscape 固定版本 e330d75；沿用 145 项主归类中的 Model Infra。','与前页合为同一观察框，项目位置不表示已验证依赖；账户头像不等同项目专属 Logo。'],2),
'42':('96 个模型仓库 · 6 类任务 · 各类近期下载 Top 16','2026-10-02 期后快照；序号为类内名次，各类等额截取。',['来源：原报告固定表 c51e344；快照日期沿用原元数据，未重建当日完整采集链。','标识为发布账户头像；3 条原图哈希不匹配，继续标为待核。可下载不等于完整开源。'],9),
'43':('86 个仓库 · 31 个类别 · 4 个功能区','沿交付、运行、资源与观测辨认技术分工；空类别保留。',['来源：原报告固定清单 c51e344 与 OpenDigger 标签 5c2ffc4；原表“2026”起止窗口待核。','项目 Logo 优先，账户头像补充；身份差异条目明确标记。名单不是全球普查或认证目录。'],18),
'44':('93 个仓库 · 17 个类别 · 3 个功能区','沿数据模型和查询任务定位对象；每个仓库仅在主位置出现一次。',['来源：原报告固定清单 c51e344 与 OpenDigger 标签 5c2ffc4；期后整理的固定观察名单。','31 项有附加标签，完整映射随数据保留；空类别不表示技术不存在，头像只识别账户。'],19),
'45':('78 条记录 · 7 个技术类别 · 3 条待核记录单列','由软件任务进入构建验证，再到实现与共同规范。',['来源：原报告固定清单与 RISC-V 分类映射；原表“2026”起止窗口待核。','标识为所属账户头像，不把多个仓库等同多个独立系统；标识缺失及分类待核如实保留。'],20),
'46':('83 个仓库 · 13 个技术类别 · 1 条生态归属待核','围绕 PyTorch 的技术观察样本，不是基金会正式托管名单。',['来源：原报告固定清单与 PyTorch 功能映射；原表“2026”起止窗口待核。','项目 Logo 与账户头像分别保存来源；PytorchForge/client 不等于 meta-pytorch/torchforge。'],21),
}
def mm(pt):return pt*25.4/72
def measure(t,pt,bold=False):return (B if bold else F).getlength(t)/100*mm(pt)
def wrap(t,w,pt,bold=False):
 s=str(t);out=[]
 while s:
  k=0
  while k<len(s) and measure(s[:k+1],pt,bold)<=w:k+=1
  k=max(1,k)
  if k<len(s):
   bp=max(s[:k].rfind('-')+1,s[:k].rfind('_')+1,s[:k].rfind(' ')+1)
   if bp>k*.55:k=bp
  out.append(s[:k].strip());s=s[k:]
 return out or ['']
def tint(c):
 v=[int(c[i:i+2],16) for i in [1,3,5]];return '#'+''.join(f'{round(255*.93+x*.07):02x}' for x in v)
class Page:
 def __init__(self):self.el=[];self.texts=[];self.links=[]
 def rect(self,x,y,w,h,c,stroke='none',rx=0):self.el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}" stroke="{stroke}" stroke-width=".22"/>')
 def line(self,x1,y1,x2,y2,c=LINE,w=.25):self.el.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{c}" stroke-width="{w}"/>')
 def text(self,x,y,t,pt=9,c=INK,bold=False,anchor='start'):
  width=measure(t,pt,bold);left=x-width if anchor=='end' else x-width/2 if anchor=='middle' else x
  self.texts.append({'text':str(t),'pt':pt,'bbox':[left,y-mm(pt),left+width,y+.6]})
  self.el.append(f'<text x="{x}" y="{y}" font-family="Liberation Sans, Noto Sans CJK SC" font-size="{mm(pt)}" fill="{c}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{html.escape(str(t))}</text>')
 def picture(self,path,x,y,w,h):
  p=R/path;im=Image.open(p);iw,ih=im.size;s=min(w/iw,h/ih);ww,hh=iw*s,ih*s
  self.el.append(f'<image x="{x+(w-ww)/2}" y="{y+(h-hh)/2}" width="{ww}" height="{hh}" href="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}"/>')
 def save(self,key):
  p=O/key;p.with_suffix('.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="297mm" height="420mm" viewBox="0 0 297 420">'+''.join(self.el)+'</svg>')
  for ext in ['pdf','png']:
   cmd=['inkscape',str(p.with_suffix('.svg')),'--export-type='+ext,'--export-filename='+str(p.with_suffix('.'+ext))]
   if ext=='png':cmd+=['--export-width=1400']
   subprocess.run(cmd,check=True,capture_output=True)
  bad=[x for x in self.texts if x['bbox'][0]<12 or x['bbox'][2]>285 or x['bbox'][1]<0 or x['bbox'][3]>419];assert not bad,(key,bad)
  return p
# Dynamic programming partitions consecutive category blocks; no identity truncation.
def partition(blocks,n):
 N=len(blocks);prefix=[0]
 for x in blocks:prefix.append(prefix[-1]+x['h']+3)
 dp={(0,0):(0,[])}
 for cols in range(1,n+1):
  for end in range(cols,N+1):
   best=None
   for start in range(cols-1,end):
    prev=dp.get((cols-1,start))
    if prev is None:continue
    height=prefix[end]-prefix[start]-3;score=max(prev[0],height)
    if best is None or score<best[0]:best=(score,prev[1]+[(start,end)])
   dp[(cols,end)]=best
 return dp[(n,N)]
for d in D:
 key=d['key'];subtitle,desc,notes,num=meta[key];n=d['columns'];gap=4;cw=(265-gap*(n-1))/n;groups={g['id']:g for g in d['groups']};blocks=[]
 for cat in d['categories']:
  ps=cat['records'];chunk_count=math.ceil(len(ps)/16) if ps else 1
  step=math.ceil(len(ps)/chunk_count) if ps else 0
  for part in range(chunk_count):
   pp=ps[part*step:(part+1)*step] if ps else [];rows=[]
   for p in pp:
    label=p['name'];pt=8.8 if n==3 else 8.2;available=cw-16
    lines=wrap(label,available,pt,True)
    owner=p['owner']+(' · 身份待核' if p.get('identity_conflict') else '')
    ownerlines=wrap(owner,available,6.8)
    h=max(8.2,len(lines)*3.05+len(ownerlines)*2.5+1.9)
    rows.append({'p':p,'name_lines':lines,'owner_lines':ownerlines,'h':h,'pt':pt})
   title=cat['name']+(' · 续' if part else '')
   titlelines=wrap(title,cw-18,9.2,True);headerh=5.5+len(titlelines)*3.15
   h=headerh+sum(x['h'] for x in rows)+1.5 if rows else headerh+6.2
   blocks.append({'cat':cat,'rows':rows,'h':h,'title_lines':titlelines,'head_h':headerh,'part':part,'parts':chunk_count,'total':len(ps)})
 maxh,segments=partition(blocks,n);print(key,'max body',round(maxh,1),'columns',n,'rows',d['count'])
 assert maxh<321.5,(key,maxh)
 pg=Page();pg.rect(0,0,297,420,'white')
 # Approved compact brand mark converted without altering its geometry.
 compact=R/'figures/new/osdgs_symbol_compact.png'
 if not compact.exists():subprocess.run(['inkscape',str(R/'figures/new/osdgs_symbol_compact.pdf'),'--export-type=png','--export-width=140','--export-filename='+str(compact)],check=True,capture_output=True)
 pg.picture(str(compact.relative_to(R)),16,9,6.8,6.8);pg.text(25,13.7,'OSDGs  /  GOSD 2026',8.4,MUTED,True);pg.text(281,13.7,'第四章 · 全球开源技术全景洞察',8.4,MUTED,anchor='end');pg.line(16,19,281,19);pg.line(16,19,30,19,ACC,.7)
 pg.text(16,31,f"{d['section']}  {d['title']}",21,INK,True)
 pg.text(16,39.5,subtitle,10.2,ACC,True);pg.text(16,46,desc,9.4,MUTED)
 gw=(265-4*(len(d['groups'])-1))/len(d['groups'])
 for i,g in enumerate(d['groups']):
  x=16+i*(gw+4);pg.rect(x,51,gw,8.5,tint(g['color']),rx=.8);pg.rect(x,51,1.2,8.5,g['color']);pg.text(x+4,56.7,g['name'],9.3,g['color'],True)
 seen=[];geo=[]
 for col,(a,b) in enumerate(segments):
  x=16+col*(cw+gap);y=65
  for block in blocks[a:b]:
   cat=block['cat'];g=groups[cat['group']];color=g['color'];h=block['h'];head=block['head_h']
   pg.rect(x,y,cw,h,'white',LINE,.7);pg.rect(x+.2,y+.2,cw-.4,head,tint(color));pg.rect(x+.2,y+.2,1.1,head,color)
   for k,t in enumerate(block['title_lines']):pg.text(x+3.4,y+4+k*3.15,t,9.2,color,True)
   count=str(block['total']) if block['parts']==1 else f"{len(block['rows'])}/{block['total']}"
   pg.text(x+cw-3,y+4,count,7.8,MUTED,anchor='end')
   if not block['rows']:
    pg.text(x+3.4,y+head+3.8,'固定名单未收录',7.5,MUTED)
   yy=y+head
   for ri,row in enumerate(block['rows']):
    p=row['p'];rh=row['h'];xx=x+12
    if ri:pg.line(x+3,yy,x+cw-3,yy,'#E8EDF0',.15)
    if p['logo']:pg.picture(p['logo'],x+3.2,yy+(rh-6.5)/2,6.5,6.5)
    else:
     pg.text(x+6.4,yy+rh/2-.2,'标识',5.5,MUTED,anchor='middle');pg.text(x+6.4,yy+rh/2+2.2,'待核',5.5,MUTED,anchor='middle')
    for k,t in enumerate(row['name_lines']):pg.text(xx,yy+3.0+k*3.05,t,row['pt'],INK,True)
    oy=yy+3.0+len(row['name_lines'])*3.05
    for k,t in enumerate(row['owner_lines']):pg.text(xx,oy+k*2.5,t,6.8,ACC if p.get('identity_conflict') or p.get('pending') else MUTED)
    geo.append({'key':key,'section':d['section'],'repo':p['repo'],'id':p['id'],'category':cat['id'],'logo':bool(p['logo']),'logo_kind':p['logo_kind'],'url':p['url'],'bbox_mm':[x+2,yy,x+cw-2,yy+rh],'name_lines':row['name_lines'],'owner_lines':row['owner_lines'],'font':row['pt']});seen.append(p['id']);yy+=rh
   y+=h+3
 assert len(seen)==len(set(seen))==d['count']
 pg.line(16,387,281,387)
 pg.text(16,394,f'图4-{num}  '+d['title']+' · 完整观察名单',10.6,INK,True)
 pg.text(16,400,notes[0],8.1,MUTED);pg.text(16,405,notes[1],8.1,MUTED)
 pg.text(16,410,'区域按功能组织，面积不编码规模；点击条目可到来源链接。分类与收录不构成依赖、许可或成效认证。',7.8,MUTED)
 pg.text(16,417,'OPEN SOURCE / A SHARED INTELLIGENT FUTURE',6.5,MUTED)
 pg.save(key);QA.append({'key':key,'records':len(seen),'categories':len(d['categories']),'columns':n,'max_body_height_mm':maxh,'bounds_ok':True,'figure':num});allgeo.extend(geo)
(R/'review/atlas_geometry.json').write_text(json.dumps(allgeo,ensure_ascii=False,indent=2));(R/'review/atlas_layout.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
print('Complete: 7 portrait maps; fixed records preserved',sum(x['records'] for x in QA))
