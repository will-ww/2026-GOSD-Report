from pathlib import Path
import json, csv, copy, subprocess, xml.etree.ElementTree as ET
from svgkit import SVG, QA
R=Path(__file__).resolve().parents[1]; O=R/'figures/new'
T=json.loads((R/'design/approved_brand_tokens.json').read_text()); D={d['id']:d for d in T['dimensions']}
GOLD='#80682E'; PALE='#F4F0E5'; GREEN='#267D4E'; BLUE='#155FA8'; PURPLE='#943B9A'

# Approved chapter-cover mother: retain the brand geometry verbatim.
root=ET.parse(R/'provenance/chapter1_cover_approved.svg').getroot()
repl={'第1章 章节封面 / 动态星座':'第6章 章节封面 / 动态星座','第一章 / CHAPTER 01':'第六章 / CHAPTER 06','从开放协作':'未来展望','到公共价值':'与行动建议','FOUNDATIONS & PUBLIC VALUE':'OUTLOOK & SHARED ACTION','以共同愿景确定方向，以观察方法理解进展。':'把证据带回支持条件、行动责任与后续观察。','01':'06'}
for e in root:
 if e.get('data-brand')=='OSDGs':continue
 for v in e.iter():
  if v.text in repl:v.text=repl[v.text]
  for a,val in list(v.attrib.items()):
   if val=='#138EAA':v.set(a,GOLD)
   if val=='#e7f4f6':v.set(a,'#F1EDDF')
 if e.tag.endswith('text') and e.text!='OSDGs':e.set('font-family','Liberation Sans, Noto Sans CJK SC')
a=next(e for e in ET.parse(R/'provenance/chapter1_cover_approved.svg').getroot() if e.get('data-brand')=='OSDGs')
b=next(e for e in root if e.get('data-brand')=='OSDGs');assert ET.tostring(a)==ET.tostring(b)
ET.register_namespace('','http://www.w3.org/2000/svg'); ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
ET.ElementTree(root).write(O/'chapter6_cover.svg',encoding='unicode')
subprocess.run(['inkscape',str(O/'chapter6_cover.svg'),'--export-type=pdf','--export-filename='+str(O/'chapter6_cover.pdf')],check=True,capture_output=True)

# Four complementary research views: no causal arrows, ranks or weights.
s=SVG(166,64)
s.text(0,5,'前文的观察',8.5,'muted',True); s.text(70,5,'带回行动的问题',8.5,'muted',True)
rows=[('02','GOSO','参与与资源','谁能持续参与，谁仍未被看见？',BLUE),('03','GOSR','主体与影响','谁在维护，哪些责任需要支持？','#6146A5'),('04','GOSL','技术与分工','实际系统依赖哪些组件与能力？','#955A3C'),('05','GOSM','供给、复用与开放','具体版本能否继续研发与使用？','#476C58')]
for i,(n,code,title,q,c) in enumerate(rows):
 y=13+i*12;s.line(0,y-2,166,y-2,'line',.25);s.rect(0,y+1,1,7,c)
 s.text(5,y+6,n,8.5,c,True);s.text(14,y+6,code,9.2,c,True);s.text(30,y+6,title,7.9,'muted')
 s.text(70,y+6,q,10.5,'ink',True)
s.line(0,61,166,61,'line',.25);s.save('01_evidence')

# Conditional share: the denominator is the 600 high-openness observations.
q={(r['completeness'],r['openness']):int(r['models']) for r in csv.DictReader((R/'inputs/openness-870.csv').open())}
assert sum(q.values())==870
complete=q['高完整','高开放']; incomplete=q['低完整','高开放']; denom=complete+incomplete
assert (complete,incomplete,denom)==(117,483,600)
s=SVG(166,78);s.text(0,5,'870 个报告样本中的高开放组',10,'ink',True);s.text(166,5,'600 个模型',10,GOLD,True,'end')
w=166*complete/denom
s.rect(0,14,w,13,GREEN);s.rect(w,14,166-w,13,'#E6E9E7')
s.text(w/2,23,'117',12,'white',True,'middle');s.text(w+(166-w)/2,23,'483',12,'ink',True,'middle')
s.text(0,35,'同时高完整',9,GREEN,True);s.text(166,35,'仍属低完整',9,'muted',True,'end')
s.text(0,61,'19.5%',32,GREEN,True);s.text(62,52,'高开放组中，同时高完整的比例',11,'ink',True)
s.text(62,62,'117 / 600；其余 80.5% 仍属低完整。',9.5,'muted')
s.text(0,76,'高完整：L3–L5；高开放：O2–O4。沿用源评估，未重新授级。',8.3,'muted');s.save('02_openness')

# Independent evaluation layers, linked by a checking sequence only.
s=SVG(166,92)
rows=[('01','开放交付','版本、材料、权利与维护入口','交付可查，还需核验能否实际使用。',BLUE),('02','实际采用','运行环境、适配、人员与持续成本','运行发生，还需检验使用者的变化。','#007D78'),('03','公共结果','任务改善、受益差异、负担与风险','按场景评价，保留失败与不利结果。',GOLD)]
for i,(n,title,a,b,c) in enumerate(rows):
 y=2+i*30;s.line(0,y,166,y,'line',.3)
 s.text(0,y+13,n,21,c,True);s.text(19,y+13,title,12.5,c,True)
 s.text(59,y+11,a,10.6,'ink',True);s.text(59,y+21,b,9.4,'muted')
 if i<2:s.line(8,y+21,8,y+27,c,.35);s.path(f'M6 {y+24} L8 {y+27} L10 {y+24}',c,.35)
s.line(0,91,166,91,'line',.3);s.save('03_evaluation')

# Operational comparison follows earlier version evidence, without asserting impact.
s=SVG(166,96)
for x,title,rev,c,lines in [
 (0,'OLMo-2-1124-7B','固定模型卡 7df9a82518af',GREEN,[('已有入口',['权重、中间检查点、分阶段','训练代码与具名数据集。']),('下一步核对',['逐项固定材料版本，核对','训练环境、许可与维护入口。']),('仍缺什么',['完整训练或端到端复现；','具体场景成本与使用结果。'])]),
 (86,'Llama-3.1-8B','固定模型卡 d04e592bb4f6',BLUE,[('已有入口',['权重清单、推理示例与','训练数据范围说明。']),('下一步核对',['分开核对材料可得性、','使用条件和具体运行任务。']),('仍缺什么',['完整预训练运行链；','具体场景成本与使用结果。'])])]:
 s.rect(x,0,80,96,'#F7F8F7',1);s.rect(x,0,80,1,c)
 s.text(x+5,10,title,11,c,True);s.text(x+5,17,rev,8,'muted')
 for i,(a,ls) in enumerate(lines):
  y=27+i*22;s.text(x+5,y,a,9,c,True)
  for j,l in enumerate(ls):s.text(x+5,y+6+j*5.3,l,9.5,'ink')
s.save('04_cases')

# Three longitudinal evidence questions. Steps indicate intended records.
s=SVG(166,86)
rows=[('参与','固定批次','持续贡献','角色接续',BLUE,'看参与者的经历，另记退出、失访与投入。'),('资源','固定版本','实际依赖','维护与采用','#007D78','看具体资源的使用，另记适配、成本与替代。'),('结果','需求与起点','真实运行','收益与负担',GOLD,'看服务对象的变化，另记失败与不利影响。')]
for i,(lab,a,b,c,col,foot) in enumerate(rows):
 y=3+i*28;s.text(0,y+6,lab,10,col,True)
 for x,t in [(25,a),(73,b),(121,c)]:s.text(x,y+6,t,10.6,'ink',True)
 for x in [61,109]:s.line(x,y+4,x+6,y+4,col,.35);s.path(f'M{x+4} {y+2} L{x+6} {y+4} L{x+4} {y+6}',col,.35)
 s.text(25,y+18,foot,9.3,'muted');s.line(0,y+24,166,y+24,'line',.25)
s.save('05_observation')

# Use the ten existing icons as navigation, not a new hierarchy or scores.
icons=[copy.deepcopy(e) for e in ET.parse(R/'assets/fig_osdgs_pillars.svg').getroot() if e.tag.endswith('}g')];assert len(icons)==10
s=SVG(166,17)
for j,did in enumerate(['D01','D04','D09','D10']):
 x=j*42;d=D[did];s.rect(x,0,40,16,PALE,.6);g=copy.deepcopy(icons[int(did[1:])-1]);g.set('transform',f'translate({x+2},3) scale(.21)');s.e.append(ET.tostring(g,encoding='unicode'));s.text(x+10,5.4,did,7.8,d['color'],True);s.text(x+10,11.3,d['name_zh'],8.7,d['color'],True)
s.save('chapter6_dimensions')

# Final chapter: a whole-report reflection; no promise of a next chapter.
s=SVG(210,297);s.rect(0,0,210,297,'#192C3A')
s.e.append('<defs><linearGradient id="closingglow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#726039"/><stop offset="1" stop-color="#192C3A"/></linearGradient></defs>');s.rect(0,0,210,116,'url(#closingglow)')
for j in range(5):s.path(f'M-25 {22+j*12} C48 {-10+j*8} 115 {100+j*5} 237 {27+j*12}','#D5C48F',.3,.18)
s.embed(O/'osdgs-display-dark-outlined.svg',126,21,62,62)
s.text(22,22,'GOSD 2026',9,'#EAE5D7',True);s.text(22,41,'06 / SHARED ACTION',8.5,'#D6C48E',True)
s.text(22,59,'让开放资源',25,'white',True);s.text(22,74,'成为持续的公共能力',21,'white',True)
s.text(22,96,'第六章回望 · 全书收束',11,'#E4D4A7',True)
s.text(22,110,'共同创造，需要明确的责任、资源与可检验的结果。',10,'#EAE6DE')
items=[('01','支持参与，也支持留下来',['让进入、反馈和角色成长形成连续路径，','让培养与维护获得相应资源。']),('02','发布资源，也承担接续责任',['把材料、权利、适配和支持落实到具体版本，','让上下游共同承担持续使用的工作。']),('03','面向公共价值，也接受结果检验',['从真实需求出发，记录成本、收益与负担，','依据证据决定继续、调整或退出。'])]
for i,(n,title,ls) in enumerate(items):
 y=128+i*35;s.text(22,y+5,n,14,'#D7C28A',True);s.text(37,y+4.5,title,12.6,'white',True)
 for j,t in enumerate(ls):s.text(37,y+14+j*6.3,t,10,'#E2E5E5')
 s.line(22,y+29.2,188,y+29.2,'#4F5D63',.25)
s.text(22,249,'从参与出发，经由供给与复用，',12,'#F0E5C6',True)
s.text(22,260,'在治理中检验公共价值。',12,'#F0E5C6',True)
s.text(22,274,'让每一次投入，都留下可以继续共同创造的能力。',9.7,'#DDE1E1')
for i,d in enumerate(T['dimensions']):s.line(22+i*16.7,284,22+i*16.7+14.2,284,d['hero_color'],.7)
s.text(22,293,'OPEN SOURCE DEVELOPMENT GOALS',6.8,'#C9D0D2');s.text(188,293,'第六章 · 共同行动',6.8,'#C9D0D2',False,'end');s.save('chapter6_closing')
(R/'review/figure_geometry.json').write_text(json.dumps({'brand_mother_unchanged':True,'charts':QA,'arithmetic':{'n':sum(q.values()),'high_open':denom,'both_high':complete,'conditional_percent':complete/denom*100}},ensure_ascii=False,indent=2))
print('5 figures, chapter cover and closing prepared; 117 / 600 = 19.5%')
