from pathlib import Path
import xml.etree.ElementTree as ET,copy,json,subprocess,hashlib
from svgkit import SVG,QA
R=Path(__file__).resolve().parents[1];O=R/'figures/new';T=json.loads((R/'design/approved_brand_tokens.json').read_text());D={d['id']:d for d in T['dimensions']}
# Reconstruct the approved Chapter 2 application from its shared Chapter 1 mother-page.
p=R/'provenance/chapter1_cover_approved.svg';root=ET.parse(p).getroot()
repl={'第1章 章节封面 / 动态星座':'第2章 章节封面 / 动态星座','第一章 / CHAPTER 01':'第二章 / CHAPTER 02','从开放协作':'全球开源生态','到公共价值':'观测地图','FOUNDATIONS & PUBLIC VALUE':'GLOBAL OPEN SOURCE OBSERVATORY','以共同愿景确定方向，以观察方法理解进展。':'从七个主题，观察参与、资源与共同建设的条件。','01':'02'}
for e in root:
 if e.get('data-brand')=='OSDGs':continue
 for v in e.iter():
  if v.text in repl:v.text=repl[v.text]
  for a,val in list(v.attrib.items()):
   if val=='#138EAA':v.set(a,'#7161BF')
   if val=='#e7f4f6':v.set(a,'#F0EDF9')
 if e.tag.endswith('text'):e.set('font-family','Liberation Sans, Noto Sans CJK SC')
ET.register_namespace('','http://www.w3.org/2000/svg');ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
ET.ElementTree(root).write(O/'chapter2_cover.svg',encoding='unicode')
subprocess.run(['inkscape',str(O/'chapter2_cover.svg'),'--export-type=pdf','--export-filename='+str(O/'chapter2_cover.pdf')],check=True,capture_output=True)
icons=[copy.deepcopy(e) for e in ET.parse(R/'reference_assets/fig_osdgs_pillars.svg').getroot() if e.tag.endswith('}g')]
assert len(icons)==10
nav={21:['D01','D02'],22:['D06','D02'],23:['D06'],24:['D01','D06'],25:['D03','D04','D05'],26:['D02','D06'],27:['D09','D10']}
for section,ids in nav.items():
 s=SVG(166,7)
 for j,did in enumerate(ids):
  x=j*48;d=D[did];s.rect(x,0,45,7,'#F3F6F8',.8)
  g=copy.deepcopy(icons[int(did[1:])-1]);g.set('transform',f'translate({x+2},1.5) scale(.18)');s.e.append(ET.tostring(g,encoding='unicode'))
  s.text(x+9.0,4.8,did,7.3,d['color'],True);s.text(x+17,4.8,d['name_zh'],8.1,d['color'])
 s.save('nav_'+str(section))
# Seven questions, with a clear editorial path and the same hierarchy used in chapter 1.
s=SVG(166,124)
rows=[('2.1','活跃','参与基础有多大，新增活跃在哪里？','参与'),('2.2','贡献','人数之外，协作工作怎样汇聚与连接？','协作'),('2.3','项目影响','贡献来源与项目影响为何呈现不同分布？','项目'),('2.4','人才','高影响力参与者在哪里积累和增长？','人才'),('2.5','资产','代码、模型与数据形成怎样的供给？','供给'),('2.6','多样性','谁进入共同建设，技术选择怎样变化？','连接'),('2.7','治理','谁提供组织支持，复用遵循什么规则？','条件')]
for i,(n,title,q,label) in enumerate(rows):
 y=3+i*17;s.circ(3,y+5.6,1.3,'#7161BF');s.line(3,y+7.7,3,y+20.4,'#D4CFEA',.4) if i<6 else None
 s.text(10,y+7,n,11,'#7161BF',True);s.text(25,y+7,title,11,'ink',True);s.text(57,y+7,q,9.7,'ink')
 s.line(10,y+14,166,y+14,'line',.22)
s.text(0,124,'七个主题互补观察；维度标签用于阅读导航，不表示已测算全部指标。',8,'muted')
s.save('chapter2_navigation')
# Concept reading key: three distinct objects, three different comparisons.
s=SVG(166,111)
rows=[('01','人 / 活动',['开发者是参与者；活跃人数记录当期参与。','PR与Issue是修改、讨论和维护的协作记录。','一个人可以贡献多次，活动量与人数分别观察。']),('02','仓库 / 项目',['仓库存放代码与协作记录；一个项目可含多个仓库。','模型与数据集按各自条目计量；平台覆盖分别保留。','跨平台或多仓库统计需要固定清单与去重记录。']),('03','贡献 / 影响',['OpenRank通过协作网络观察位置与关系。','开发者贡献度和项目影响力采用不同对象与聚合。','总量、均值、份额与增幅，均按各自分母理解。'])]
for i,(n,title,ls) in enumerate(rows):
 y=i*37;s.line(0,y+1,166,y+1,'#7161BF',.6);s.text(0,y+10,n,15,'#7161BF',True);s.text(15,y+10,title,12,'ink',True)
 for j,l in enumerate(ls):s.text(15,y+18+j*6,l,9.7,'muted')
s.save('reading_objects')
# Reflect, then hand off to the next research view. No fresh empirical claims added.
s=SVG(210,297);s.rect(0,0,210,297,'#182444')
s.e.append('<defs><linearGradient id="endglow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#544D86"/><stop offset="1" stop-color="#182444"/></linearGradient></defs>')
s.rect(0,0,210,113,'url(#endglow)')
for j in range(5):s.path(f'M-25 {22+j*12} C48 {-10+j*8} 115 {100+j*5} 237 {27+j*12}','#B7A9EB',.3,.18)
s.embed(O/'osdgs-display-dark-outlined.svg',126,21,62,62)
s.text(22,22,'GOSD 2026',9,'#C7D0E5',True);s.text(22,41,'02 / CHAPTER REFLECTION',8.5,'#BEA9F2',True)
s.text(22,59,'看见生态差异',25,'white',True);s.text(22,73,'找到支持对象',25,'white',True)
s.text(22,94,'第二章回望',11,'#DBD2F0',True);s.text(22,109,'从参与和资源的分布，走向具体的共同建设。',10.4,'#E0DEEE')
items=[('01','规模扩大，结构仍需分别观察',['累计基础、当期活跃、贡献与项目影响呈现不同次序。','比较对象与覆盖范围，是理解地区差异的第一步。']),('02','项目有归属，协作连接多个来源',['项目归属地与贡献者所在地，说明不同侧面的参与。','本土支持与跨境贡献可以并存，完整关系仍需逐项核对。']),('03','发布之外，支持持续维护与复用',['代码、模型和数据供给积累，使用信号与数量并不同步。','责任、说明与许可提供条件，实际公共成效还需场景证据。'])]
for i,(n,title,ls) in enumerate(items):
 y=127+i*35;s.text(22,y+5,n,14,'#B5A5E9',True);s.text(37,y+4.5,title,13,'white',True)
 for j,t in enumerate(ls):s.text(37,y+14+j*6.3,t,10,'#DADDEA')
 s.line(22,y+29.2,188,y+29.2,'#49506E',.25)
s.text(22,246,'下一章 / 全球开源影响力排行榜',10,'#C7B3F4',True)
s.text(22,258,'哪些主体连接生态，位置又如何变化？',13.3,'white',True)
s.text(22,270,'由宏观格局进入具体主体，在同一指标和对象边界内比较。',9.6,'#CDD5E8')
for i,d in enumerate(T['dimensions']):s.line(22+i*16.7,284,22+i*16.7+14.2,284,d['hero_color'],.7)
s.text(22,293,'OPEN SOURCE DEVELOPMENT GOALS',6.8,'#B2BBD2');s.text(188,293,'第二章 · 回望与衔接',6.8,'#B2BBD2',False,'end')
s.save('chapter2_closing')
(R/'review/brand_geometry_checks.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
(R/'review/section_dimension_map.json').write_text(json.dumps({'purpose':'阅读导航，不表示已经测算所有候选指标','mapping':nav},ensure_ascii=False,indent=2))
print('brand / navigation / closing:',len(QA),'assets')
