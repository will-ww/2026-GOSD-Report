"""Compact relation-based redesign; original evidence and approved identities retained."""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;E=R.parents[2]
sys.path.insert(0,str(E/'scripts'))
from infographic_primitives_v1 import *
F=R/'figures';B=json.loads((E.parents[1]/'brand/osdgs/v2.0/source/brand_tokens.json').read_text())

# 1-3 / Development goals and design conditions, followed by implementation gates.
sdgs=['无贫穷','零饥饿','良好健康与福祉','优质教育','性别平等','清洁饮水和卫生设施','经济适用的清洁能源','体面工作和经济增长','产业、创新和基础设施','减少不平等','可持续城市和社区','负责任消费和生产','气候行动','水下生物','陆地生物','和平、正义与强大机构','促进目标实现的伙伴关系']
colors=['E5243B','DDA63A','4C9F38','C5192D','FF3A21','26BDE2','FCC30B','A21942','FD6925','DD1367','FD9D24','BF8B2E','3F7E44','0A97D9','56C02B','00689D','19486A']
s=text(22,101,78,'17 项 SDGs｜共同发展方向',10.6,15,'blue',True)
s+=text(108,101,80,'9 项 DPG 要求｜开放与设计',10.6,15,'teal',True)
s+=rule(22,111,101,'blue!25')+rule(108,111,188,'teal!25')
for i,(name,c) in enumerate(zip(sdgs,colors)):
    col=0 if i<9 else 1;row=i if i<9 else i-9;x=22+col*41;y=115+row*8.8
    s+=rf'\definecolor{{sdg{i+1}}}{{HTML}}{{{c}}}'+'\n'
    s+=rect(x,y+.7,.9,5.7,f'sdg{i+1}')+text(x+2.5,y,7,f'{i+1:02}',7.8,10,'muted',True)+text(x+9,y,30,name,8.3,10.8,'navy')
requirements=[('SDG 相关性','说明发展目标关联'),('开放许可','允许合法复用'),('清晰权属','说明权利归属'),('平台独立性','减少封闭平台依赖'),('文档','支持理解与使用'),('数据提取机制','可提取非身份识别数据'),('隐私与法律','遵守隐私及适用法律'),('标准与最佳实践','遵循相关标准与实践'),('不造成伤害','安全、内容与反骚扰保护')]
for i,(title,desc) in enumerate(requirements):
    y=115+i*8.8
    s+=text(108,y,7,f'{i+1:02}',8.1,11,'teal',True)+text(117,y,32,title,8.6,11,'navy',True)+text(151,y,37,desc,7.8,10.7,'muted')
    if i<8:s+=rule(108,y+7.3,188,'teal!12')
s+=text(22,199,166,'开放资源转化为公共能力，还要跨越四道实施门槛',10.5,15,'navy',True)
centers=[40,83,126,169]
for i,(x,title,desc,c,ic) in enumerate(zip(centers,['可获得','可复用','可维护','有成效'],['版本 · 许可 · 文档','成本 · 语言 · 工具','责任 · 资金 · 安全','覆盖 · 质量 · 公平'],['blue','teal','gold','violet'],['D05','D08','D09','D10'])):
    if i<3:s+=curve((x+7,219),(centers[i+1]-7,219),(x+18,216),(x+23,222),c+'!35',.9,True)
    s+=orb(x,219,5.5,c,ic)+text(x-18,227,36,title,9.8,14,c,True,True)+text(x-20,236,40,desc,8,11,'muted',False,True)
(F/'sdgs-dpg.tex').write_text(s)

# 1-4 / Four pillars surround the approved emblem. Ten dimension identities stay fixed.
s=''
for a,b,p,q,c in [((79,125),(91,142),(88,125),(84,135),'blue'),((131,125),(119,142),(122,125),(127,135),'teal'),((79,184),(91,165),(88,184),(84,172),'gold'),((131,184),(119,165),(122,184),(127,172),'violet')]:
    s+=curve(a,b,p,q,c+'!12',5)+curve(a,b,p,q,c+'!55',.7)
s+=icon(86,135,38,'osdgs-display')
s+=text(79,177,52,'共同发展 · 全球接续',9.1,13,'teal',True,True)
locations=[(22,99,58,'blue'),(130,99,58,'teal'),(22,160,58,'gold'),(130,160,58,'violet')]
questions=['扩大参与与持续成长','形成可复用的开放资源','让成果跨境接续生长','让协作持续、成果共享']
for i,(p,(x,y,w,c)) in enumerate(zip(B['pillars'],locations)):
    s+=ribbon(x,y,w,53,c)
    s+=text(x+3,y+3,52,p['id']+' '+p['name_zh'],9.6,14,c,True)
    s+=text(x+3,y+12,52,questions[i],8.4,12,'muted')
    for j,did in enumerate(p['dimensions']):
        d=next(d for d in B['dimensions'] if d['id']==did)
        s+=icon(x+3,y+24+j*8.7,4.2,did)+text(x+10,y+24+j*8.7,45,f"{did} {d['name_zh']}",8.6,12,'ink')
s+=text(22,218,166,'OSDGs / Open Source Development Goals',8.2,12,'muted',False,True)
(F/'goals.tex').write_text(s)

# 1-5 / OSDI: a compact conversion of goals to observation, not a composite score.
s=ribbon(22,99,166,59,'blue')
s+=text(27,102,35,'OSDI',18,23,'navy',True)+text(63,104,120,'开源发展指标体系｜把目标转化为观察信号',11,15,'blue',True)
for i,(x,n,label,c) in enumerate([(50,'4','发展目标','blue'),(105,'10','观察方向','teal'),(160,'29','候选指标','violet')]):
    s+=text(x-17,113,34,n,27,31,c,True,True)+text(x-20,133,40,label,10,14,'navy',True,True)
    if i<2:s+=arrow(x+23,126,x+32,126,c+'!30')
s+=text(27,147,156,'X1 人才：5 项　　X2 供给：7 项　　X3 连接：11 项　　X4 治理与公共价值：6 项',8.4,12,'muted')
for x,title,desc,c in [(22,'北极星','把握长期方向','blue'),(80,'诊断','识别差异与瓶颈','teal'),(138,'驱动','跟踪过程与变化','gold')]:
    s+=text(x,163,50,title,10,14,c,True)+text(x+18,163,33,desc,8.5,12,'muted')
(F/'osdi.tex').write_text(s)

# 1-6 / People, organisations, projects and three kinds of asset form typed relationships.
s=text(22,188,166,'把指标放回协作关系：六类对象联读',10.5,15,'navy',True)
for a,b,p,q,c in [((49,204),(97,204),(65,201),(81,207),'blue'),((108,204),(156,204),(124,201),(140,207),'blue'),((161,210),(48,235),(161,229),(48,219),'teal'),((161,210),(103,235),(161,222),(103,222),'gold'),((161,210),(161,235),(161,220),(161,226),'violet')]:
    s+=curve(a,b,p,q,c+'!45',.7,True)
for x,y,title,c,ic in [(42,204,'人才','blue','D01'),(103,204,'组织','blue','D02'),(162,204,'项目','blue','D03'),(42,239,'代码','teal','D03'),(103,239,'模型','gold','D04'),(162,239,'数据','violet','D05')]:s+=labelnode(x,y,title,c,ic,40)
s+=text(64,197,18,'参与',7.5,10,'muted',False,True)+text(125,197,18,'共建',7.5,10,'muted',False,True)
s+=text(78,225,61,'项目形成与维护开放资产',8.1,11,'muted',False,True)
(F/'entities.tex').write_text(s)

# 1-8 / Four evidence perspectives orbit a shared question; six chapter roles remain.
s=''
for x,y,c in [(60,123,'blue'),(151,123,'gold'),(60,170,'teal'),(151,170,'violet')]:
    s+=curve((x, y),(105,147),(x,147),(87 if x<100 else 123,147),c+'!20',3)
s+=orb(105,147,13,'blue')+text(93,138,24,'全球开放',10,14,'navy',True,True)+text(93,149,24,'协作',12,16,'teal',True,True)
views=[(22,103,'02','生态地图','GOSO','参与与资源分布','blue','D01'),(132,103,'03','影响力排行','GOSR','关键主体与位置','gold','D06'),(22,155,'04','技术全景','GOSL','技术分层与连接','teal','D03'),(132,155,'05','模型生态','GOSM','供给、复用与开放','violet','D04')]
for x,y,n,t,a,q,c,ic in views:
    s+=ribbon(x,y,56,36,c)+orb(x+9,y+10,4.5,c,ic)
    s+=text(x+17,y+4,37,n+' '+t,10,14,c,True)+text(x+17,y+14,37,a,8,11,'muted')+text(x+4,y+26,48,q,8.5,12,'ink',False,True)
s+=text(22,196,166,'图 1-8　第一章提出方法 · 第二至第五章提供证据 · 第六章归纳洞察与行动',8.4,12,'muted',False,True)
(F/'roadmap.tex').write_text(s)

# The reuse case keeps the numbers and scopes, while making the connection visual.
s=(F/'reuse.tex').read_text()
for x,c in [(22,'blue'),(108,'teal')]:
    s=s.replace(rect(x,99,80,64,c+'!5')+rect(x,99,80,1,c),ribbon(x,99,80,64,c))
start=s.index(r'\Rect{22}{181}');end=s.index(r'\Box{22}{220}')
chain=curve((53,196),(72,196),(61,193),(64,199),'teal!50',1,True)
chain+=curve((137,196),(157,196),(145,193),(149,199),'gold!50',1,True)
chain+=orb(41,196,10,'blue','D04')+text(22,209,39,'DeepSeek-R1',9.8,13,'blue',True,True)
chain+=ribbon(75,181,62,36,'teal')+text(79,184,54,'NVIDIA 开放后训练数据',9.1,13,'teal',True)
chain+=text(79,194,54,'121.3 万条',19,23,'teal',True)+text(79,207,54,'明确列为 R1 生成的样本',7.7,11,'muted')
chain+=orb(169,196,10,'gold','D04')+text(148,209,42,'Llama-Nemotron',8.7,12,'gold',True,True)
s=s[:start]+chain+s[end:]
(F/'reuse.tex').write_text(s)

# One collaboration, three lenses. A process replaces the previous tall card stack.
s=text(22,102,166,'同一案例：项目 P 的兼容性修复，在项目 Q 中继续使用',10.4,15,'navy',True)
for i,(x,role,desc,c,ic) in enumerate([(40,'甲｜发现问题','报告不兼容现象','blue','D01'),(83,'乙｜提交修复','贡献代码改动','teal','D03'),(126,'丙｜审阅验证','测试并完善修改','gold','D09'),(169,'丁｜接续使用','在项目 Q 中复用','violet','D08')]):
    if i<3:s+=curve((x+8,130),(x+35,130),(x+16,126),(x+25,134),c+'!35',1,True)
    s+=orb(x,130,6.5,c,ic)+text(x-19,140,38,role,9.2,13,c,True,True)+text(x-20,149,40,desc,8,11,'muted',False,True)
for x,title,q,signal,c,ic in [(22,'参与','谁持续进入协作？','人数、留存与角色','blue','D01'),(79,'贡献','完成了哪些共同工作？','开发、讨论与审阅','teal','D03'),(136,'影响力','工作怎样被连接与接续？','协作关系与结构位置','gold','D06')]:
    s+=ribbon(x,172,52,43,c)+orb(x+8,181,4,c,ic)
    s+=text(x+16,176,32,title,11,15,c,True)+text(x+4,190,44,q,8.8,12,'navy')+text(x+4,202,44,signal,8.3,12,'muted')
s+=text(22,219,166,'图 1-7　协作示意，非实测样本。OpenRank 综合协作关系，观察贡献在网络中的结构性影响。',8.1,12,'muted')
(F/'measures.tex').write_text(s)
print('Generated compact SDG/DPG, OSDGs, OSDI, entity and reading-path infographics.')
