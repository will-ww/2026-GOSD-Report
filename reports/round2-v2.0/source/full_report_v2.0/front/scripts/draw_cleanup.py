from pathlib import Path
import html, json, subprocess, xml.etree.ElementTree as ET
from PIL import ImageFont
R=Path(__file__).resolve().parents[1];O=R/'figures/new';QA=[]
F=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',100,index=2)
B=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',100,index=2)
C={'ink':'#142C49','muted':'#536B7D','line':'#D7E4EA','teal':'#007D78','blue':'#155FA8','white':'#FFFFFF'}
def col(c):return C.get(c,c)
class SVG:
 def __init__(self,w,h):self.w=w;self.h=h;self.e=[];self.labels=[]
 def rect(self,x,y,w,h,c,rx=0):self.e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{col(c)}"/>')
 def path(self,d,c='line',lw=.3,opacity=1,fill='none'):self.e.append(f'<path d="{d}" fill="{fill}" stroke="{col(c)}" stroke-width="{lw}" opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"/>')
 def line(self,x1,y1,x2,y2,c='line',lw=.3):self.path(f'M{x1} {y1}L{x2} {y2}',c,lw)
 def circ(self,x,y,r,c):self.e.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col(c)}"/>')
 def text(self,x,y,t,pt=10,c='ink',b=False,anchor='start'):
  size=pt*25.4/72;w=(B if b else F).getlength(t)/100*size;left=x if anchor=='start' else x-w/2 if anchor=='middle' else x-w
  self.labels.append({'text':t,'pt':pt,'x':round(left,2),'y':y,'width':round(w,2)})
  family='Liberation Sans' if t.isascii() else 'Noto Sans CJK SC'
  self.e.append(f'<text x="{x}" y="{y}" fill="{col(c)}" font-family="{family}" font-size="{size}" font-weight="{700 if b else 400}" text-anchor="{anchor}">{html.escape(t)}</text>')
 def embed(self,path,x,y,w,h):
  el=ET.parse(path).getroot();el.set('x',str(x));el.set('y',str(y));el.set('width',str(w));el.set('height',str(h));self.e.append(ET.tostring(el,encoding='unicode'))
 def save(self,name):
  p=O/name;p.with_suffix('.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.w}mm" height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">'+''.join(self.e)+'</svg>')
  for ext in ['pdf','png']:
   cmd=['inkscape',str(p.with_suffix('.svg')),'--export-type='+ext,'--export-filename='+str(p.with_suffix('.'+ext))]
   if ext=='png':cmd+=['--export-width=1500']
   subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  bad=[x for x in self.labels if x['x']<-.2 or x['x']+x['width']>self.w+.2 or x['y']>self.h]
  QA.append({'file':name,'labels':len(self.labels),'outside':bad});assert not bad,bad
# Six chapters: a research route, not a causal or measured network.
s=SVG(166,157)
for i,word in enumerate(['参与','供给','复用','治理','公共价值']):
 x=i*33.2;s.text(x+16.6,5,word,10,'teal',True,'middle')
 if i<4:s.circ(x+33.2,3.7,.55,'line')
s.rect(0,12,166,24,'ink',2)
s.text(6,22,'01',17,'white',True);s.text(22,21.8,'从开放协作到公共价值',12,'white',True)
s.text(22,29.7,'共同创新  /  OSDGs发展目标  /  OSDI指标与方法',9,'#C7E5EA')
s.line(9,37,9,126,'#B8CFD9',.6)
s.text(22,44.5,'四个互补视角',9,'muted',True);s.text(165,44.5,'分别观察对象、时期与边界',8,'muted',False,'end')
rows=[('02','GOSO','全球开源生态观测地图','空间分布与参与结构','#155FA8'),('03','GOSR','全球开源影响力排行榜','主体位置与跨期变化','#6146A5'),('04','GOSL','全球开源技术全景洞察','技术分层、协作与演进','#955A3C'),('05','GOSM','全球开源大模型发展洞察','模型供给、派生与开放','#476C58')]
for i,(n,code,title,desc,c) in enumerate(rows):
 y=51+i*19
 s.circ(9,y+6,2,c);s.line(11,y+6,18,y+6,c,.4)
 s.text(22,y+4,n,13,c,True);s.text(33,y+4,code,10,c,True)
 s.text(59,y+4,title,10.9,'ink',True)
 s.text(59,y+11,desc,9.3,'muted')
 s.line(22,y+15.5,166,y+15.5,'line',.2)
s.rect(0,130,166,21,'#EAF4F4',2)
s.text(6,139.5,'06',17,'teal',True);s.text(22,139.5,'未来展望与行动建议',12,'ink',True)
s.text(22,146.5,'明确行动主体、支持条件与后续观察',9.3,'muted')
s.text(0,156,'附录A  指标、数据与研究方法',8,'muted');s.text(166,156,'附录B  模型开放条件与数字公共品研究参照',8,'muted',False,'end')
s.save('report_architecture_full')
# Declaration hierarchy. One neutral palette avoids misidentifying seven principles as ten dimensions.
s=SVG(166,157)
s.rect(0,0,166,29,'#EEF5F8',2)
for x,n,t,d in [(5,'I','时代呼唤','迈向智能协作新纪元'),(88,'II','共同愿景','构建智能共治的数字文明')]:
 s.text(x,10,n,18,'blue',True);s.text(x+12,9,t,11.5,'ink',True);s.text(x+12,20,d,9.3,'muted')
s.line(81,6,81,23,'#CBDDE6',.35)
s.line(0,38,166,38,'teal',.6)
s.text(0,46.5,'III',14,'teal',True);s.text(14,46.5,'核心原则：行动框架',12,'ink',True)
layers=[('第一层','筑牢智能时代基石',[(1,'坚持开放互联','万物智联，普惠共生'),(2,'坚持安全可信','透明算法，信任基石')]),('第二层','夯实伦理治理支柱',[(3,'坚持数据伦理','算法向善，责任共担'),(4,'坚持多元包容','众智共创，价值共享'),(5,'坚持全球协作','跨界协同，智能互联')]),('第三层','共创社会价值未来',[(6,'坚持绿色智能','低碳驱动，创新致远'),(7,'坚持开源普惠','智能为公，成果共享')])]
for i,(ly,title,items) in enumerate(layers):
 y=54+i*28
 s.rect(0,y,166,24,'#F5F8FA',1)
 s.text(4,y+7.5,ly,8.5,'teal',True);s.text(4,y+15,title,8.7,'ink',True)
 left=39;cw=(166-left)/len(items)
 for k,(n,t,q) in enumerate(items):
  x=left+k*cw
  s.line(x,y+4,x,y+20,'#CFDFE5',.25)
  s.text(x+3,y+7,f'{n:02}',8.5,'teal',True);s.text(x+3,y+13.2,t,10,'ink',True);s.text(x+3,y+20,q,8.4,'muted')
s.rect(0,141,166,16,'ink',2)
s.text(5,151.3,'IV',16,'white',True);s.text(20,151.3,'行动共识',11.5,'white',True);s.text(56,151.3,'迈向全球AI治理新格局',9.5,'#D5E9EF')
s.save('declaration_structure_2026')
# Closure: an editorial reflection, not a second cover or a new set of empirical claims.
s=SVG(210,297);s.rect(0,0,210,297,'#0D2543')
s.e.append('<defs><linearGradient id="endglow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#285A85"/><stop offset="1" stop-color="#0D2543"/></linearGradient></defs>')
s.rect(0,0,210,113,'url(#endglow)')
for j in range(5):s.path(f'M-25 {22+j*12} C48 {-10+j*8} 115 {100+j*5} 237 {27+j*12}','#4AA3C5',.3,.2)
s.embed(O/'osdgs-display-dark-outlined.svg',126,21,62,62)
s.text(22,22,'GOSD 2026',9,'#BDD6E4',True);s.text(22,41,'01 / CHAPTER REFLECTION',8.5,'#78DAD2',True)
s.text(22,59,'让开放资源',25,'white',True);s.text(22,73,'成为持续能力',25,'white',True)
s.text(22,94,'第一章回望',11,'#C4E6E8',True)
s.text(22,109,'方向、方法与证据边界，是后续观察的共同起点。',10.4,'#D7E5EE')
items=[('01','以发展目标确定方向',['人才、开放供给、全球连接与善治，共同组织研究问题。','OSDGs表达希望实现的方向，不能替代已经发生的结果。']),('02','用分层指标观察进展',['四个目标、十个观察方向与29项候选指标保持不同层级。','OSDI提供可复核的观察信号，具体可测状态由附录A说明。']),('03','回到真实场景检验价值',['可获得、可复用、可维护、有成效，需要分别取得证据。','参与、影响、下载与派生，都不能独立证明公共成效。'])]
for i,(n,title,lines) in enumerate(items):
 y=127+i*35
 s.text(22,y+5,n,14,'#6BC8D2',True);s.text(37,y+4.5,title,13,'white',True)
 for j,t in enumerate(lines):s.text(37,y+14+j*6.3,t,10,'#D4E0EA')
 s.line(22,y+29.2,188,y+29.2,'#3A506A',.25)
s.text(22,246,'下一章 / 全球开源生态观测地图',10,'#7FDCD6',True)
s.text(22,258,'参与与资源分布在哪里，差异又意味着什么？',13.3,'white',True)
s.text(22,270,'从共同语言进入全球观察，以明确的对象和时期读懂地图。',9.6,'#CBDDEB')
# Fixed approved dimension order as a quiet brand register; no weights or chapter assignment.
t=json.loads((R/'design/approved_brand_tokens.json').read_text())
for i,d in enumerate(t['dimensions']):s.line(22+i*16.7,284,22+i*16.7+14.2,284,d['hero_color'],.7)
s.text(22,293,'OPEN SOURCE DEVELOPMENT GOALS',6.8,'#9CB8CE');s.text(188,293,'第一章 · 回望与衔接',6.8,'#9CB8CE',False,'end')
s.save('chapter1_closing')
(R/'review/diagram_geometry_checks.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
print(json.dumps(QA,ensure_ascii=False))
# Compact first-chapter explanatory figures. All wording and relationships are inherited.
import copy
oldO=O;O=R/'figures/ch1'
# Reuse the ten original Lucide paths; identity and order stay fixed.
icons=[copy.deepcopy(e) for e in ET.parse(R/'provenance/figures/fig_osdgs_pillars.svg').getroot() if e.tag.endswith('}g')]
tok=json.loads((R/'design/approved_brand_tokens.json').read_text());dims={d['id']:d for d in tok['dimensions']}
s=SVG(166,90);k=0
for i,p in enumerate(tok['pillars']):
 y=i*22
 s.line(0,y+1,166,y+1,p['color'],.55);s.text(0,y+8.4,p['id'],14,p['color'],True);s.text(16,y+8,p['name_zh'],11,'ink',True)
 for j,did in enumerate(p['dimensions']):
  d=dims[did];x=16+j*49.5;g=copy.deepcopy(icons[k]);k+=1;g.set('transform',f'translate({x},{y+13}) scale(0.25)');s.e.append(ET.tostring(g,encoding='unicode'))
  s.text(x+8,y+17.8,did,8.1,d['color'],True);s.text(x+17,y+17.8,d['name_zh'],9.1,'ink')
s.save('fig_osdgs_pillars')
s=SVG(166,70);s.text(0,6,'从资源开放到实际结果',11,'ink',True);s.text(166,6,'条件关系，不是自动发生的因果链',8,'muted',False,'end')
cols=[('01','可获得','资源能否真正取得？','代码、模型与数据'),('02','可复用','使用是否可行？','权利、成本与兼容'),('03','可维护','运行由谁持续承担？','人才、组织与责任'),('04','有成效','产生了什么改善？','服务、公平与韧性')]
for i,(n,t,q,desc) in enumerate(cols):
 x=i*42;s.rect(x,14,40,44,'#F1F7F8' if i<3 else '#E7F1F3',1)
 s.text(x+3,22,n,10,'teal',True);s.text(x+3,32,t,13,'ink',True);s.text(x+3,41,q,9,'muted');s.text(x+3,51,desc,8.3,'muted')
s.text(0,67,'实施条件：逐项检查',8.7,'teal',True);s.text(126,67,'结果证据：另行验证',8.7,'teal',True)
s.save('fig_capacity_gates')
s=SVG(166,72);s.text(0,6,'协作对象与工作角色，都在扩展',11,'ink',True)
s.rect(0,13,51,37,'#EDF4F8',1);s.text(4,23,'软件协作',9,'muted');s.text(4,33,'代码与持续维护',11.5,'ink',True);s.text(4,43,'公开、审阅、修改、再分发',8,'muted')
s.path('M55 32 H61 M59 30L61 32L59 34','#9DB7C6',.45)
for x,y,t,desc,c in [(67,17,'代码','可修改的实现','#007D78'),(118,17,'模型','可使用的参数','#267D4E'),(67,38,'数据','可理解的材料','#537D25'),(118,38,'工具','可运行的环境','#155FA8')]:
 s.line(x,y-3,x+48,y-3,c,.5);s.text(x,y+3,t,10.7,'ink',True);s.text(x,y+10,desc,8.5,'muted')
s.line(0,55,166,55,'line',.3);s.text(0,62,'从发布到使用',9,'ink',True)
for i,t in enumerate(['适配','测试','审阅','维护']):s.circ(64+i*26,60.8,.65,'teal');s.text(67+i*26,62,t,9,'muted')
s.text(0,71,'代码、权重、数据和接口的开放条件不同；资源增多不等于自主能力已经形成。',8,'muted')
s.save('fig_ai_open_landscape')
s=SVG(166,70);s.text(0,6,'把目标转化为可核对的观察信号',11,'ink',True)
for i,(n,t,q,c) in enumerate([('4','发展目标','希望走向哪里？','#007D78'),('10','观察方向','从哪些方面判断？','#155FA8'),('29','候选指标','哪些数据能够核实？','#6146A5')]):
 x=i*56;s.text(x,29,n,25,c,True);s.text(x+20,23,t,10,'ink',True);s.text(x,39,q,9,'muted');s.line(x,44,x+50,44,'line',.3)
for i,(t,q) in enumerate([('北极星','提示长期方向'),('诊断','识别结构差异'),('驱动','观察变化动力')]):
 x=i*56;s.text(x,53,t,10,'ink',True);s.text(x,60,q,8.7,'muted')
s.text(0,69,'指标用途不是证据等级；29项为候选目录，不表示均已完成本期测量。',8,'muted')
s.save('fig_osdi_logic')
# Preserve the exact matrix dot relationships from the original chart.
original=ET.parse(R/'provenance/figures/fig_pillars_theme_matrix.svg').getroot();circles=[e for e in original.iter() if e.tag.endswith('}circle')]
print('Original matrix dots:',[(e.get('cx'),e.get('cy')) for e in circles])
s=SVG(166,112);s.text(0,6,'从四项发展目标，进入七个主题',11,'ink',True);s.text(0,13,'主要阅读关系；不代表计算权重',8,'muted')
for i,(p,short) in enumerate(zip(tok['pillars'],['人才','供给','连接','治理'])):
 x=104+i*19;s.text(x,21,p['id'],9,p['color'],True,'middle');s.text(x,27,short,8,'muted',False,'middle')
rows=[('V-Map · 活跃','参与规模、地域分布与变化趋势'),('C-Map · 贡献','贡献来源、强度与协作关系'),('I-Map · 项目影响','影响分布、项目结构与时间变化'),('T-Map · 人才','人才聚集、参与积累与全球连接'),('A-Map · 资产','代码、模型与数据供给'),('D-Map · 多样性','参与结构、跨域协作与开放连接'),('G-Map · 治理与社会公益','治理实践、开放条件与公共价值')]
for i,(title,desc) in enumerate(rows):
 y=36+i*10;s.text(0,y,'2.'+str(i+1),8.5,'muted',True);s.text(12,y,title,9.2,'ink',True);s.text(12,y+4.8,desc,7.8,'muted');s.line(0,y+7,166,y+7,'line',.2)
for e in circles:
 x=float(e.get('cx'));y=float(e.get('cy'));i=round((y-49)/11.3);j=round((x-102)/20)
 assert 0<=i<7 and 0<=j<4,(x,y,i,j)
 s.circ(104+j*19,36+i*10,1.35 if float(e.get('r'))>1 else .35,tok['pillars'][j]['color'] if float(e.get('r'))>1 else 'line')
s.text(0,111,'其他关联在后续证据中展开，不作一一映射。',8,'muted')
s.save('fig_pillars_theme_matrix')
O=oldO
(R/'review/diagram_geometry_checks.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
