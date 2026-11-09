from pathlib import Path
import xml.etree.ElementTree as ET,copy,json,subprocess
from svgkit import SVG,QA
R=Path(__file__).resolve().parents[1];O=R/'figures/new';T=json.loads((R/'design/approved_brand_tokens.json').read_text());D={d['id']:d for d in T['dimensions']};ACC='#6146A5'
root=ET.parse(R/'provenance/chapter1_cover_approved.svg').getroot()
repl={'第1章 章节封面 / 动态星座':'第3章 章节封面 / 动态星座','第一章 / CHAPTER 01':'第三章 / CHAPTER 03','从开放协作':'全球开源','到公共价值':'影响力排行榜','FOUNDATIONS & PUBLIC VALUE':'GLOBAL OPEN SOURCE RANKINGS','以共同愿景确定方向，以观察方法理解进展。':'将主体放回协作网络，分别理解规模、位置与变化。','01':'03'}
for e in root:
 if e.get('data-brand')=='OSDGs':continue
 for v in e.iter():
  if v.text in repl:v.text=repl[v.text]
  for a,val in list(v.attrib.items()):
   if val=='#138EAA':v.set(a,ACC)
   if val=='#e7f4f6':v.set(a,'#F1EDF7')
 if e.tag.endswith('text'):e.set('font-family','Liberation Sans, Noto Sans CJK SC')
ET.register_namespace('','http://www.w3.org/2000/svg');ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
ET.ElementTree(root).write(O/'chapter3_cover.svg',encoding='unicode')
subprocess.run(['inkscape',str(O/'chapter3_cover.svg'),'--export-type=pdf','--export-filename='+str(O/'chapter3_cover.pdf')],check=True,capture_output=True)
icons=[copy.deepcopy(e) for e in ET.parse(R/'reference_assets/fig_osdgs_pillars.svg').getroot() if e.tag.endswith('}g')];assert len(icons)==10
nav={31:['D01','D06'],32:['D06'],33:['D06','D09'],34:['D03','D06','D09'],35:['D03','D06'],36:['D04','D07']}
for section,ids in nav.items():
 s=SVG(166,7)
 for j,did in enumerate(ids):
  x=j*48;d=D[did];s.rect(x,0,45,7,'#F4F2F8',.8)
  g=copy.deepcopy(icons[int(did[1:])-1]);g.set('transform',f'translate({x+2},1.5) scale(.18)');s.e.append(ET.tostring(g,encoding='unicode'))
  s.text(x+9,4.8,did,7.3,d['color'],True);s.text(x+17,4.8,d['name_zh'],8.1,d['color'])
 s.save('nav_'+str(section))
s=SVG(166,109)
rows=[('3.1','地区','高位节点与多节点分布'),('3.2','企业','项目组合、参与基础与位置变化'),('3.3','基金会','组织关联与具体仓库的影响结构'),('3.4','项目','资源、协作、交付与持续维护'),('3.5','新势力','项目供给与基础组件的分工'),('3.6','模型','版本位置、任务与发布账户')]
for i,(n,title,q) in enumerate(rows):
 y=2+i*17;s.circ(3,y+6,1.3,ACC)
 if i<5:s.line(3,y+8,3,y+21,'#D8CFE8',.4)
 s.text(10,y+7,n,11,ACC,True);s.text(25,y+7,title,11,'ink',True);s.text(57,y+7,q,10,'ink');s.line(10,y+14,166,y+14,'line',.22)
s.text(0,109,'维度标签用于阅读导航，不表示已测算全部指标或建立统一评分。',8,'muted');s.save('chapter3_navigation')
s=SVG(210,297);s.rect(0,0,210,297,'#211E3C')
s.e.append('<defs><linearGradient id="glow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#67518B"/><stop offset="1" stop-color="#211E3C"/></linearGradient></defs>');s.rect(0,0,210,113,'url(#glow)')
for j in range(5):s.path(f'M-25 {22+j*12} C48 {-10+j*8} 115 {100+j*5} 237 {27+j*12}','#C4B3EE',.3,.18)
s.embed(O/'osdgs-display-dark-outlined.svg',126,21,62,62)
s.text(22,22,'GOSD 2026',9,'#DDD5E9',True);s.text(22,41,'03 / CHAPTER REFLECTION',8.5,'#D1BEF3',True)
s.text(22,59,'从影响位置',25,'white',True);s.text(22,73,'走向持续供给',25,'white',True)
s.text(22,94,'第三章回望',11,'#E3D9F2',True);s.text(22,109,'榜单定位主体，项目证据连接资源与维护。',10.4,'#E6DFF0')
items=[('01','位置与规模，回答不同问题',['席位、分值、参与规模与位次变化分别观察。','具体项目组合，帮助解释相近名次背后的不同结构。']),('02','项目边界，决定所见的供给',['项目与仓库、家族与版本、账户与组织分别识别。','多组件的软件栈与多版本的模型供给，需要逐项联读。']),('03','持续维护，让资源具备复用条件',['从协作记录进入版本、依赖、职责与支持期限。','支持与采用的判断，还需成本、本地化和实际结果。'])]
for i,(n,title,ls) in enumerate(items):
 y=127+i*35;s.text(22,y+5,n,14,'#C8B6EE',True);s.text(37,y+4.5,title,13,'white',True)
 for j,t in enumerate(ls):s.text(37,y+14+j*6.3,t,10,'#E0DBEA')
 s.line(22,y+29.2,188,y+29.2,'#59506E',.25)
s.text(22,246,'下一章 / 全球开源技术全景洞察',10,'#D2BEF3',True)
s.text(22,258,'这些主体如何共同组成技术生态？',13.3,'white',True)
s.text(22,270,'由具体主体进入技术分层、协作结构与可比范围内的演进。',9.6,'#D8D3E5')
for i,d in enumerate(T['dimensions']):s.line(22+i*16.7,284,22+i*16.7+14.2,284,d['hero_color'],.7)
s.text(22,293,'OPEN SOURCE DEVELOPMENT GOALS',6.8,'#C4BBD2');s.text(188,293,'第三章 · 回望与衔接',6.8,'#C4BBD2',False,'end');s.save('chapter3_closing')
(R/'review/brand_geometry_checks.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
(R/'review/section_dimension_map.json').write_text(json.dumps({'purpose':'阅读导航，不表示测算全部指标','mapping':nav},ensure_ascii=False,indent=2))
# Mother mark geometry/content retained without any alteration.
a=next(e for e in ET.parse(R/'provenance/chapter1_cover_approved.svg').getroot() if e.get('data-brand')=='OSDGs');b=next(e for e in root if e.get('data-brand')=='OSDGs');assert ET.tostring(a)==ET.tostring(b)
print('brand complete',len(QA))
