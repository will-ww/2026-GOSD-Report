from pathlib import Path
import json, math
R=Path(__file__).resolve().parent
F=R/'figures'
D=json.loads((R/'sources/chart-data.json').read_text())
B=json.loads((R.parents[4]/'brand/osdgs/v2.0/source/brand_tokens.json').read_text())
def box(x,y,w,t): return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{{t}}}'+'\n'
def text(x,y,w,t,size=9.5,leading=14,color='ink',bold=False):
 return box(x,y,w,rf'\sffamily{"\\bfseries" if bold else ""}\fontsize{{{size}}}{{{leading}}}\selectfont\color{{{color}}}{t}')
def rect(x,y,w,h,c):return rf'\Rect{{{x}}}{{{y}}}{{{w}}}{{{h}}}{{{c}}}'+'\n'
def circle(x,y,r,c):return rf'\Circle{{{x}}}{{{y}}}{{{r}}}{{{c}}}'+'\n'
def rule(x,y,z,c='line'):return rf'\Rule{{{x}}}{{{y}}}{{{z}}}{{{c}}}'+'\n'
def arrow(x,y,a,b,c='muted'):return rf'\LinkLine{{{x}}}{{{y}}}{{{a}}}{{{b}}}{{{c}}}'+'\n'
# Figure 1-1. Three actual annual points per metric, independent panel scales.
s=''
metrics=[('代码提交',D['github']['commits'],['10.0','12.9','34.3']),
 ('Actions 作业',D['github']['actions_jobs'],['8.0','14.0','45.4']),
 ('合并 PR',D['github']['merged_prs'],['0.402','0.538','1.30'])]
for n,(name,values,labels) in enumerate(metrics):
 x=22+n*57
 s+=text(x,106,52,name,10,15,'blue',True)
 s+=text(x,114,52,'单位：十亿次',7.5,10,'muted')
 base=160
 s+=rule(x,base,x+47)
 for j,(v,lab) in enumerate(zip(values,labels)):
  xx=x+3+j*15;h=30*v/max(values);color=['blue!22','blue!47','blue'][j]
  s+=rect(xx,base-h,10,h,color)
  s+=text(xx-3,base-h-7,16,rf'\centering {lab}',8.7,12,'navy',True)
  s+=text(xx-3,base+2,16,rf'\centering {2024+j}',7.8,10,'muted')
# Stock bars distinguish source endpoints, without invented monthly trajectories.
s+=text(22,183,166,'HF 开放资产：模型、数据与应用空间同步扩张',10.5,15,'teal',True)
hf=[('公共模型仓库',243,296,'243','296'),('数据集',71.1,100,'71.1','100'),('Spaces',100,144,'100','144')]
for n,(name,a,b,al,bl) in enumerate(hf):
 x=22+n*57
 s+=text(x,195,52,name,9.5,14,'navy',True)
 s+=text(x+32,195,19,rf'\raggedleft +{round((b/a-1)*100)}\%',9.5,14,'teal',True)
 for yy,v,lab,col in [(208,a,al,'teal!25'),(218,b,bl,'teal')]:
  w=36*v/b;s+=rect(x,yy,w,4,col)
  s+=text(x+w+2,yy-1.5,14,lab,8.5,11,'navy')
s+=text(22,228,166,'浅色为来源所列期初，深色为期末；单位：万个。增幅按展示数值计算。',7.8,11,'muted')
(F/'growth.tex').write_text(s)
# Figure 1-2. Cyclic co-creation, not a measured dependency network.
s=''
nodes=[(22,'开放供给','模型权重／代码','说明、许可与版本','blue'),
 (80,'社区接续','转换、量化、微调','工具适配与测试','teal'),
 (138,'场景使用','本地部署与集成','应用反馈与维护','gold')]
for x,title,l1,l2,c in nodes:
 s+=rect(x,111,50,37,c+'!6')+rect(x,111,50,1,c)
 s+=text(x+4,116,42,title,11,16,c,True)
 s+=text(x+4,128,42,l1,9.3,14)
 s+=text(x+4,137,42,l2,8.8,13,'muted')
s+=arrow(72,130,79,130,'teal')+arrow(130,130,137,130,'teal')
s+=r'\draw[blue,line width=.7pt,-{Stealth[length=2mm]}] \Pos{163}{150} -- \Pos{163}{161} -- \Pos{47}{161} -- \Pos{47}{150};'+'\n'
s+=rect(63,157,84,8,'white')+text(64,157,82,r'\centering 使用反馈、缺陷修复与再创造需求',8.6,12,'blue')
s+=text(22,171,166,'图 1-2　开放供给与社区接续共同支持 AI 演进',8.8,13,'navy',True)
s+=text(22,178,166,'机制示意。连线表示需要观察的接续关系，不代表已核验的训练谱系或贡献比例。',7.8,11,'muted')
(F/'reuse.tex').write_text(s)
# Figure 1-3. Exact approved X/D identities and palette; readable labels not miniature logos.
s=''
questions=[
 '谁能够进入开放创新，并成长为持续贡献者？',
 '哪些代码、模型与数据能被获取、理解并继续创造？',
 '成果如何跨越组织、地域与技术层次形成接续？',
 '谁支撑长期维护，开放成果怎样形成共同受益？']
for i,p in enumerate(B['pillars']):
 y=99+i*35
 c=['blue','teal','gold','violet'][i]
 s+=rule(22,y-3,188)
 s+=text(22,y,15,p['id'],13,18,c,True)
 s+=text(40,y,148,p['name_zh'],12,18,c,True)
 s+=text(40,y+10,148,questions[i],10,15)
 for j,dimid in enumerate(p['dimensions']):
  dim=next(z for z in B['dimensions'] if z['id']==dimid)
  col='d'+dimid
  s+=rf'\definecolor{{{col}}}{{HTML}}{{{dim["color"][1:]}}}'+'\n'
  x=40+j*49
  s+=circle(x+1.3,y+25,1.1,col)
  s+=text(x+5,y+21,44,dim['id']+' '+dim['name_zh'],8.4,12,col)
s+=rule(22,239,188)
(F/'goals.tex').write_text(s)
# Figure 1-4. Staggered gates highlight distinct conditions, not automatic causal achievement.
s=''
gates=[
 ('01','可获得','资源与权利','版本、许可、文档','blue'),
 ('02','可复用','成本与适配','算力、语言、工具','teal'),
 ('03','可维护','人员与治理','责任、资金、安全','gold'),
 ('04','有成效','场景与结果','覆盖、质量、公平','violet')]
for i,(n,title,sub,detail,c) in enumerate(gates):
 x=22+i*43
 s+=rect(x,104,37,58,c+'!6')
 s+=text(x+4,108,29,n,19,23,c,True)
 s+=text(x+4,124,29,title,12,17,c,True)
 s+=text(x+4,138,29,sub,9.3,14)
 s+=text(x+4,148,29,detail,8.1,12,'muted')
 if i<3:s+=arrow(x+38,132,x+42,132,'line')
s+=text(22,170,166,'图 1-4　开放资源形成公共能力，需要逐项建立条件与结果证据',8.8,13,'navy',True)
s+=text(22,177,166,'前三项关注实施条件，最后一项需由实际场景检验；这是一组分析问题，不是自动生效的因果公式。',7.8,11,'muted')
(F/'capacity.tex').write_text(s)
# Figure 1-5. Six entities and five typed relations, with a reuse loop.
s=''
s+=text(22,103,166,'以地域与时序，联读主体、资产及其联系',10.5,15,'teal',True)
nodes=[(22,122,'人才','参与、审阅、维护','blue'),(80,122,'组织','支持、协调、治理','blue'),(138,122,'项目','组织共同工作','blue'),
       (22,177,'代码','开发与工具实现','teal'),(80,177,'模型','发布、派生、适配','gold'),(138,177,'数据','供给、加工、复用','violet')]
for x,y,title,desc,c in nodes:
 s+=rect(x,y,50,28,c+'!6')
 s+=text(x+4,y+3,42,title,11.5,16,c,True)
 s+=text(x+4,y+15,42,desc,8.5,13,'muted')
# Explicit arrows kept out of node text.
s+=arrow(72,135,79,135,'blue')+arrow(130,135,137,135,'blue')
s+=text(69,119,17,r'\centering 参与',7.1,10,'muted')+text(127,119,17,r'\centering 支持',7.1,10,'muted')
s+=r'\draw[teal,line width=.65pt] \Pos{163}{151} -- \Pos{163}{163} -- \Pos{47}{163};'+'\n'
for x in [47,105,163]:s+=arrow(x,163,x,175,'teal')
s+=text(76,155,58,r'\centering 形成与维护开放资产',8,11,'teal')
s+=r'\draw[gold,line width=.65pt,-{Stealth[length=2mm]}] \Pos{47}{207} -- \Pos{47}{218} -- \Pos{177}{218} -- \Pos{177}{151};'+'\n'
s+=rect(72,214,89,8,'white')+text(74,214,85,r'\centering 在其他项目中被复用与再创造',8,12,'gold')
s+=text(22,229,166,'图 1-5　六类对象的关联观察框架',8.8,13,'navy',True)
s+=text(22,236,166,'框架示意：同一实体可对应多个账号、仓库或资源；具体关系须有来源，并登记映射与覆盖状态。',7.8,11,'muted')
(F/'entities.tex').write_text(s)
# Figure 1-6. Same illustrative collaboration; no fake metric values.
s=''
s+=rect(22,105,57,92,'paper')
s+=text(26,108,49,'项目 P：修复兼容问题',9.2,14,'navy',True)
for i,(who,action) in enumerate([('甲','发现并报告问题'),('乙','提交兼容性修复'),('丙','审阅与验证改动'),('丁','在项目 Q 中复用')]):
 y=122+i*17
 s+=circle(29,y+3,3,'blue!13')+text(26,y+.4,6,r'\centering '+who,8,10,'blue',True)
 s+=text(36,y,39,action,8.4,12,'navy')
 if i<3:s+=arrow(29,y+7,29,y+13,'blue!40')
s+=text(26,189,49,'协作示意，不代表实测结果。',7.2,10,'muted')
# Explanatory rows for the three reading dimensions.
rows=[
 ('参与','哪些人持续进入协作？','人数、留存与角色分布','blue'),
 ('贡献','完成了哪些共同工作？','开发、讨论、审阅与修复','teal'),
 ('影响力','这些工作怎样被连接和接续？','协作联系、接续路径与结构位置','gold')]
for i,(title,q,signal,c) in enumerate(rows):
 y=105+i*32
 s+=text(88,y,100,title,11,16,c,True)
 s+=text(88,y+9,100,q,9.4,14)
 s+=text(88,y+19,100,signal,8.2,12,'muted')
s+=text(22,204,166,'图 1-6　同一协作过程，可以从参与、贡献与影响力三个视角观察',8.8,13,'navy',True)
s+=text(22,211,166,'OpenRank 依据定义的协作关系计算网络影响；单次计数、下载或关注均不能直接替代这一观察。',7.8,11,'muted')
(F/'measures.tex').write_text(s)
# Figure 1-7. Four substantive chapters, contextual foundation and synthesis.
s=''
rows=[
 ('02','GOSO','生态地图','参与与资源分布在哪里？','blue'),
 ('03','GOSR','影响力排行','哪些主体形成关键影响？','gold'),
 ('04','GOSL','技术全景','技术如何分层、连接与演进？','teal'),
 ('05','GOSM','模型生态','模型如何供给、复用与开放？','violet')]
for i,(n,abbr,title,q,c) in enumerate(rows):
 y=100+i*22
 s+=rect(22,y,166,19,c+'!5')
 s+=text(26,y+3,13,n,14,18,c,True)
 s+=text(44,y+2,36,title,10.5,15,c,True)
 s+=text(44,y+11,36,abbr,7.5,10,'muted')
 s+=text(85,y+5,99,q,9.5,15)
s+=text(22,194,166,'图 1-7　第一章提出问题与方法，第二至第五章提供四类互补证据',8.8,13,'navy',True)
(F/'roadmap.tex').write_text(s)
print('Generated 7 editable figure groups from structured data and approved identity registry.')
