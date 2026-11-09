from pathlib import Path
import xml.etree.ElementTree as ET,copy,json,subprocess
from svgkit import SVG,QA
R=Path(__file__).resolve().parents[1];O=R/'figures/new';T=json.loads((R/'design/approved_brand_tokens.json').read_text());D={d['id']:d for d in T['dimensions']};ACC='#955A3C'
root=ET.parse(R/'provenance/chapter1_cover_approved.svg').getroot()
repl={'第1章 章节封面 / 动态星座':'第4章 章节封面 / 动态星座','第一章 / CHAPTER 01':'第四章 / CHAPTER 04','从开放协作':'全球开源技术','到公共价值':'全景洞察','FOUNDATIONS & PUBLIC VALUE':'GLOBAL OPEN SOURCE LANDSCAPE','以共同愿景确定方向，以观察方法理解进展。':'从功能分工出发，理解技术生态的组织与演进。','01':'04'}
for e in root:
 if e.get('data-brand')=='OSDGs':continue
 for v in e.iter():
  if v.text in repl:v.text=repl[v.text]
  for a,val in list(v.attrib.items()):
   if val=='#138EAA':v.set(a,ACC)
   if val=='#e7f4f6':v.set(a,'#F5EEE8')
 if e.tag.endswith('text'):e.set('font-family','Liberation Sans, Noto Sans CJK SC')
ET.register_namespace('','http://www.w3.org/2000/svg');ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
ET.ElementTree(root).write(O/'chapter4_cover.svg',encoding='unicode');subprocess.run(['inkscape',str(O/'chapter4_cover.svg'),'--export-type=pdf','--export-filename='+str(O/'chapter4_cover.pdf')],check=True,capture_output=True)
a=next(e for e in ET.parse(R/'provenance/chapter1_cover_approved.svg').getroot() if e.get('data-brand')=='OSDGs');b=next(e for e in root if e.get('data-brand')=='OSDGs');assert ET.tostring(a)==ET.tostring(b)
# Six research entries; the ten dimensions are not forced into six chapter bins.
s=SVG(166,114)
rows=[('4.1','Agentic AI','任务入口、构建编排与模型基础'),('4.2','AI 大模型','模型任务、发布账户与获取信号'),('4.3','云基础设施','应用交付、服务运行与资源支撑'),('4.4','数据库系统','数据模型、查询方式与专用语义'),('4.5','RISC-V','软件、工具、实现与共同规范'),('4.6','PyTorch 生态','模型与任务、训练执行、工程协作')]
for i,(n,title,detail) in enumerate(rows):
 y=2+i*18;s.circ(3,y+6,1.3,ACC)
 if i<5:s.line(3,y+8,3,y+22,'#DDC8BB',.4)
 s.text(10,y+7,n,11,ACC,True);s.text(25,y+7,title,11,'ink',True);s.text(62,y+7,detail,9.3,'muted');s.line(10,y+15.8,166,y+15.8,'line',.22)
s.save('chapter4_navigation')
icons=[copy.deepcopy(e) for e in ET.parse(R/'assets/fig_osdgs_pillars.svg').getroot() if e.tag.endswith('}g')];assert len(icons)==10
s=SVG(166,17)
for j,did in enumerate(['D03','D04','D06','D07']):
 x=j*42;d=D[did];s.rect(x,0,40,16,'#F7F4F1',.6)
 g=copy.deepcopy(icons[int(did[1:])-1]);g.set('transform',f'translate({x+2},3) scale(.21)');s.e.append(ET.tostring(g,encoding='unicode'))
 s.text(x+10,5.4,did,7.8,d['color'],True);s.text(x+10,11.3,d['name_zh'],8.7,d['color'],True)
s.save('chapter4_dimensions')
s=SVG(210,297);s.rect(0,0,210,297,'#212536');s.e.append('<defs><linearGradient id="glow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#855B45"/><stop offset="1" stop-color="#212536"/></linearGradient></defs>');s.rect(0,0,210,113,'url(#glow)')
for j in range(5):s.path(f'M-25 {22+j*12} C48 {-10+j*8} 115 {100+j*5} 237 {27+j*12}','#DCB89F',.3,.18)
s.embed(O/'osdgs-display-dark-outlined.svg',126,21,62,62)
s.text(22,22,'GOSD 2026',9,'#ECE2DC',True);s.text(22,41,'04 / CHAPTER REFLECTION',8.5,'#E4C1AA',True)
s.text(22,59,'从完整全景',25,'white',True);s.text(22,73,'走向可复用的能力',23,'white',True)
s.text(22,94,'第四章回望',11,'#F0DCCB',True);s.text(22,109,'辨认功能分工，再进入具体项目、版本与运行条件。',10,'#EFE5DE')
items=[('01','先看完整分工，再找具体对象',['全景保留任务、工具、基础设施与工程支撑。','按功能找到项目，才有进一步比较和调查的起点。']),('02','同一图景，需要不同观察尺度',['项目与仓库、模型版本与发布账户分别辨认。','位次、份额与绝对值联读，历史与期后窗口分开。']),('03','资源能否复用，仍需运行证据',['技术位置不能替代兼容性、维护和场景验证。','下一步把视线落到模型的派生、复用与开放条件。'])]
for i,(n,title,ls) in enumerate(items):
 y=127+i*35;s.text(22,y+5,n,14,'#E3C0A7',True);s.text(37,y+4.5,title,12.8,'white',True)
 for j,t in enumerate(ls):s.text(37,y+14+j*6.3,t,10,'#E1DFE3')
 s.line(22,y+29.2,188,y+29.2,'#5B5761',.25)
s.text(22,246,'下一章 / 全球开源大模型发展洞察',10,'#E3C0A7',True);s.text(22,258,'模型资源怎样被接续开发与使用？',13,'white',True);s.text(22,270,'从功能全景进入模型供给、衍生网络与具体开放条件。',9.6,'#DFD9D6')
for i,d in enumerate(T['dimensions']):s.line(22+i*16.7,284,22+i*16.7+14.2,284,d['hero_color'],.7)
s.text(22,293,'OPEN SOURCE DEVELOPMENT GOALS',6.8,'#D2C7C1');s.text(188,293,'第四章 · 回望与衔接',6.8,'#D2C7C1',False,'end');s.save('chapter4_closing')
(R/'review/brand_geometry_checks.json').write_text(json.dumps({'mother_mark_unchanged':True,'geometry':QA},ensure_ascii=False,indent=2));print('Chapter 4 brand complete')
