"""Reading-first evidence and explanatory graphics, v0.5.

Uses the approved palette and icons. Numeric values come from source records;
framework layouts and the local-language example are explanatory, not observations.
"""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;F=R/'figures'
sys.path.insert(0,str(R.parents[2]/'scripts'))
from infographic_primitives_v1 import text,rect,rule,icon,curve,arrow,orb,ribbon
D=json.loads((R/'sources/chart-data.json').read_text())
CAT=json.loads((R/'sources/osdi-catalogue.json').read_text())

def write(name,s):(F/name).write_text(s)
def label(x,y,w,t,c='blue'):return text(x,y,w,t,10.2,14.5,c,True)

# 1-1 / Separate populations, clearly identified snapshots. Not a causal comparison.
s=label(22,101,80,'修改从哪里开始？','blue')+label(108,101,80,'开发者如何使用助手？','teal')
s+=text(22,109,80,'GitHub 中由智能体起草的 PR 占比',9,13,'navy')
s+=text(108,109,80,'Copilot 月活用户中使用智能体功能的比例',9,13,'navy')
for x,c,rows in [(22,'blue',[('2026 年 3 月',.17,'17\\%'),('2026 年 9 月',.40,'超过 40\\%')]),(108,'teal',[('报告所述上年',.35,'35\\%'),('2026 年报告',.55,'55\\%')])]:
 for i,(date,v,num) in enumerate(rows):
  y=121+i*18
  s+=text(x,y,80,date,8.4,12,'muted')
  s+=rect(x,y+7,51,3.5,c+'!8')+rect(x,y+7,51*v,3.5,c)
  s+=text(x+54,y+5,27,num,10,14,c,True)
  if x==22 and i==1:s+=arrow(x+51*v,y+8.7,x+51*v+4,y+8.7,c)
 s+=text(x,159,80,'0—100\\%；“超过”数值以 40\\% 为下界。' if x==22 else '分母是 Copilot 月活用户，不是全部开发者。',7.8,11,'muted')
s+=rule(22,172,188)+label(22,178,166,'从提出任务到长期维护：协作责任怎样衔接','navy')
for i,(x,title,desc,c,ic) in enumerate([(22,'人定义问题','明确需求与约束','blue','D01'),(65,'智能体起草','生成代码与修改','teal','D03'),(108,'人审阅与接纳','核对质量与风险','gold','D09'),(151,'社区持续维护','修复、更新与接续','violet','D10')]):
 s+=icon(x+1,193,6,ic)+text(x+10,193,32,title,9.6,14,c,True)
 s+=text(x,206,38,desc,8.5,12,'muted')
 if i<3:s+=arrow(x+37,198,x+41,198,'muted!40')
s+=text(22,218,166,'流程是解释示意：智能体可参与多个环节，人的审阅与项目治理仍需明确责任。',8.2,12,'muted')
write('agent-workflow.tex',s)

# 1-2a / One observation per row; explain the denominator beside the number.
s=''
rows=[(99,'blue','Qwen｜社区在原有模型上继续开发','151,448','HF 记录的衍生仓库','其他开发者基于 Qwen 继续训练、调整用途或转换运行格式，形成可再次使用的版本。','这些仓库体现再加工，不等于 15.1 万个从零训练的原创模型。'),
(152,'teal','DeepSeek｜模型被下载到使用环境','47\\%','所追踪超大型模型下载份额','ATOM 研究追踪的超大型开放语言模型累计下载中，DeepSeek 占近一半。下载可用于部署、测试或自动化流程。','超大型按总参数≥2500 亿分组；参数是模型训练得到的数值，用于划分规模，不等于性能。'),
(205,'gold','DeepSeek｜通过服务平台在线调用','31.1\\%','所选样本处理文本量份额','在提供多模型调用服务的 OpenRouter 中，DeepSeek 占所选前十开放模型处理文本量的 31.1\\%。','以词元计量；词元是文本处理的基本单位。这是调用量信号，不是用户数或收入份额。')]
for y,c,title,n,measure,desc,limit in rows:
 s+=ribbon(22,y,166,47,c)+label(27,y+3,156,title,c)
 s+=text(27,y+12,57,n,22,27,c,True)+text(27,y+28,57,measure,8.7,12,'navy')
 s+=text(91,y+13,91,desc,9.3,14.5,'ink')
 s+=text(27,y+37,156,limit,8,11.5,'muted')
write('reuse.tex',s)

# 1-2b / A documented historical case, with nouns and actions readable without ML jargon.
s=text(22,99,166,'历史案例 · NVIDIA 数据说明，2025 年 5 月',8.6,12,'muted')
for x,c,ic,title,desc in [(22,'blue','D04','DeepSeek-R1','生成回答与推理过程'),(80,'teal','D05','训练材料','NVIDIA 整理并开放'),(138,'gold','D04','Llama-Nemotron','使用相应数据集训练')]:
 s+=ribbon(x,108,50,44,c)+icon(x+4,112,6,ic)+text(x+13,112,34,title,9.6,14,c,True)
 s+=text(x+4,126,42,desc,9,13,'navy')
 if x==80:s+=text(x+4,138,42,'其中 R1 样本约 121.3 万条',9,12,'teal',True)
 if x<138:s+=arrow(x+51,129,x+57,129,'muted!60')
write('reuse-case.tex',s)
s=''
for x,c,title,names,desc in [(22,'blue','计算与推理','FlashMLA · DeepGEMM','优化模型运算与推理执行'),(79,'teal','多芯片协作','DeepEP · DualPipe','支持通信与并行训练调度'),(136,'gold','数据存储','3FS','支撑训练数据的存取')]:
 s+=ribbon(x,196,52,35,c)+label(x+3,199,46,title,c)+text(x+3,210,46,names,9,13,'navy',True)+text(x+3,221,46,desc,8.4,12,'muted')
write('deepseek-infra.tex',s)

# 1-5 / Work an actual branch of the candidate framework rather than showing counts.
s=text(22,101,166,'示例：关注人才发展，为什么不能只看新增账号？',10.2,14.5,'navy',True)
s+=ribbon(22,114,34,50,'blue')+text(26,118,26,'一级 · 目标',8.5,12,'muted')
s+=text(26,128,26,'X1 人才规模与多样性',10.4,16,'blue',True)+text(26,150,26,'培养持续贡献者',8.3,12,'ink')
s+=ribbon(62,114,34,50,'teal')+text(66,118,26,'二级 · 方向',8.5,12,'muted')
s+=text(66,128,26,'D01 规模与密度',10.4,16,'teal',True)+text(66,150,26,'观察规模与分布',8.3,12,'ink')
s+=arrow(56,139,61,139,'blue!50')+arrow(96,139,102,139,'teal!50')
for y,c,typ,title,desc in [(113,'blue','北极星','活跃开发者规模','有多少人在实际参与协作？'),(131,'teal','诊断','人才聚集密度','参与者集中在哪里？'),(149,'gold','驱动','新晋开发者增速','新的参与力量怎样进入？')]:
 s+=ribbon(103,y,85,16,c)+text(106,y+2,60,title,9.4,13,'navy',True)+text(167,y+2,18,typ,8.6,12,c,True)
 s+=text(106,y+9,77,desc,8.6,12,'muted')
write('osdi.tex',s)
# User-supplied four stages, recast as grounded uses with required decision evidence.
s=''
s+=rect(22,199,166,7,'paper')+text(25,200,30,'使用环节',8.8,12,'navy',True)+text(59,200,65,'指标帮助回答什么',8.8,12,'navy',True)+text(127,200,58,'行动前还需核对',8.8,12,'navy',True)
for y,c,title,q,need in [(209,'blue','透视与诊断','哪里供给丰富，哪里连接薄弱？','同窗口、同对象、可比基线'),(222,'teal','引导与激励','如何支持持续贡献与共同维护？','贡献质量、角色与激励后果'),(235,'gold','赋能与决策','公共投入和合作应优先补哪里？','实际成本、本地需求与承接能力'),(248,'violet','连接与共建','哪些伙伴可以共同建设公共能力？','开放条件、责任安排与受益结果')]:
 s+=label(25,y,31,title,c)+text(59,y,64,q,9,13,'ink')+text(127,y,58,need,8.7,12.5,'muted')+rule(22,y+10.5,188,'line')
write('osdi-decisions.tex',s)

# Table 1-1 / Full 29-item candidate catalogue, with exact original types.
B=json.loads((R.parents[4]/'brand/osdgs/v2.0/source/brand_tokens.json').read_text())
s=rect(22,86,166,8,'navy')
for x,w,t in [(25,36,'方向'),(62,75,'候选指标'),(139,16,'用途'),(158,29,'目标关联')]:s+=text(x,87,w,t,8.8,12,'white',True)
y=95;prev=None
for g in CAT['groups']:
 c={'X1':'blue','X2':'teal','X3':'gold','X4':'violet'}[g['pillar']]
 if prev!=g['pillar']:
  title=next(p['name_zh'] for p in B['pillars'] if p['id']==g['pillar'])
  s+=rect(22,y,166,6.5,c+'!9')+text(25,y+1,160,g['pillar']+' '+title,9.2,12.5,c,True);y+=7;prev=g['pillar']
 for j,item in enumerate(g['items']):
  if j==0:s+=text(25,y+.3,34,g['dimension']+' '+g['name'],8.3,11.3,'navy',True)
  s+=text(62,y+.3,73,item['name'],8.7,11.5,'ink')
  typ=item['type'];s+=text(140,y+.3,14,typ,8.6,11.5,c,True)
  s+=text(158,y+.3,27,'、'.join(map(str,item['sdg'])),8.5,11.5,'muted')
  s+=rule(60,y+4.4,188,'line');y+=4.65
assert y<260,y
write('osdi-catalogue.tex',s)

# 1-6 / An ecosystem: roles, coordination, reusable assets, cross-project circulation.
s=''
for x,c,ic,title,desc in [(22,'blue','D01','人才','开发者、研究者、维护者与使用者'),(108,'violet','D02','组织','企业、高校、基金会与公共机构')]:
 s+=ribbon(x,100,80,24,c)+icon(x+4,104,7,ic)+text(x+15,104,59,title,11,15,c,True)+text(x+4,115,72,desc,8.6,12,'ink')
s+=arrow(62,125,79,135,'blue!60')+text(23,128,46,'贡献、审阅、反馈',8,11,'blue')
s+=arrow(148,125,131,135,'violet!60')+text(143,128,45,'投入、治理、支持',8,11,'violet')
s+=ribbon(61,137,88,22,'teal')+icon(65,141,7,'D03')+text(77,140,65,'项目：围绕共同目标持续协作',10,14,'teal',True)+text(65,150,80,'如软件系统、研究工具或公共服务方案',8.5,12,'ink')
for x,c,ic,title,desc in [(22,'blue','D03','代码','实现功能的程序与工具'),(79,'teal','D04','模型','训练后用于预测或生成的模型文件'),(136,'gold','D05','数据','训练、评测或服务所需资料')]:
 s+=curve((105,160),(x+26,171),(105,166),(x+26,165),'muted!35',.6)
 s+=ribbon(x,172,52,24,c)+icon(x+3,176,6,ic)+text(x+12,175,37,title,10.5,15,c,True)+text(x+3,186,46,desc,8.1,11,'ink')
s+=text(22,200,166,'项目组织研发、采用与维护；代码调用模型，数据支持训练或评测，三类资产还可被其他项目复用。',8.3,12,'muted')
write('entities.tex',s)

# 1-8 / Rich reading matrix, deliberately not four empty cards.
s=''
for i,(x,t) in enumerate([(22,'参与'),(56,'供给'),(90,'复用'),(124,'治理'),(158,'公共价值')]):
 c=['blue','teal','gold','violet','teal'][i];s+=text(x,101,30,t,10,14,c,True,True)
 if i<4:s+=arrow(x+30,104,x+33,104,'muted!40')
s+=text(22,110,166,'五段主线贯穿全书；四个视角各有职责，关系核验后才联合解释。',8.3,12,'muted')
s+=rect(22,120,166,8,'navy')
for x,w,t in [(25,31,'章节与视角'),(61,64,'主要对象与证据'),(129,56,'可以支持的判断')]:s+=text(x,121,w,t,8.8,12,'white',True)
rows=[(130,'blue','02 生态地图','GOSO','地区、人才与资产','空间分布、增长、贡献强度、未知覆盖','哪里在增长，增长是否形成持续贡献；识别地区和人才结构。'),(157,'gold','03 影响力排行','GOSR','地区、企业、基金会与项目','协作网络、影响位置、排名与时序','谁承担关键连接与长期维护；识别合作伙伴与结构变化。'),(184,'teal','04 技术全景','GOSL','技术类别、项目与工具链','技术分层、项目联系、维护与演进','模型之外还需要哪些基础工具；识别技术支撑与协作缺口。'),(211,'violet','05 模型生态','GOSM','发布者、模型、数据与复用者','开放供给、衍生网络、许可和使用条件','中国模型怎样进入全球再创造；何种条件支持本地化与普惠。')]
for y,c,title,abbr,objects,ev,meaning in rows:
 s+=rect(22,y,3,25,c)+text(28,y+2,31,title,9.2,13,c,True)+text(28,y+11,31,abbr,8,11,'muted')
 s+=text(61,y+2,64,objects,9.3,13,'navy',True)+text(61,y+12,64,ev,8.4,12,'muted')
 s+=text(129,y+2,56,meaning,8.9,13.2,'ink')+rule(22,y+25,188)
write('roadmap.tex',s)
print('Built readable workflow, model reuse, 29-item catalogue, ecosystem roles and decision pathway.')
