from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
FIG=ROOT/'figures'; FIG.mkdir(exist_ok=True)
def box(x,y,w,text):
    return rf'\Box{{{x:.2f}}}{{{y:.2f}}}{{{w:.2f}}}{{{text}}}'+'\n'
groups=[
 (22,'blue','GitHub 开发活动','浅色：2025 · 深色：2026（十亿次）',[
 ('代码提交',12.9,34.3,'12.9','34.3'),('自动化作业',14,45.4,'14.0','45.4'),('合入修改提案',.538,1.3,'0.538','1.30')]),
 (110,'teal','HF 开放资产','浅色：期初 · 深色：期末（万个）',[
 ('公共模型仓库',243,296,'243','296'),('数据集',71.1,100,'71.1','100'),('应用空间',100,144,'100','144')])
]
tex=''
for x,c,title,legend,rows in groups:
 tex+=box(x,93,78,rf'\sffamily\bfseries\fontsize{{11.5}}{{16}}\selectfont\color{{{c}}}{title}')
 tex+=box(x,102,78,rf'\sffamily\fontsize{{7.7}}{{11}}\selectfont\color{{muted}}{legend}')
 for i,(label,v0,v1,t0,t1) in enumerate(rows):
  y=113+i*22
  rate=round((v1/v0-1)*100)
  tex+=box(x,y,53,rf'\sffamily\bfseries\fontsize{{9.4}}{{13}}\selectfont {label}')
  tex+=box(x+53,y,25,rf'\raggedleft\sffamily\bfseries\fontsize{{9.6}}{{13}}\selectfont\color{{{c}}}约 +{rate}\%')
  for yy,v,s,fill in [(y+7,v0,t0,c+'!25'),(y+14,v1,t1,c)]:
   w=49*v/v1
   tex+=rf'\Rect{{{x}}}{{{yy}}}{{{w:.3f}}}{{3.4}}{{{fill}}}'+'\n'
   tex+=box(x+w+2,yy-1,24,rf'\digits\fontsize{{8.8}}{{12}}\selectfont {s}')
(FIG/'growth.tex').write_text(tex)
features=[
 ('AI 全景 · 体系化观察','以地图、排行、技术全景与模型网络，贯通参与、供给、复用与治理。'),
 ('跨平台 · 全域数据视野','联读 GitHub、HF、Gitee 等平台，从资源数量深入协作与复用关系。'),
 ('中国出发 · 全球视野','把中国产业与社区实践置于全球分工，兼顾欧美积累与全球南方潜力。'),
 ('深度洞察 · AI 普惠','从地域差异与时序演化识别战略机会，服务产业布局、地方决策与公共能力建设。')]
tex=''
for i,(title,desc) in enumerate(features):
 x=22+(i%2)*86;y=215+(i//2)*31
 tex+=rf'\Rect{{{x}}}{{{y}}}{{80}}{{27}}{{paper}}'+'\n'
 tex+=box(x+4,y+2.5,72,rf'\sffamily\bfseries\fontsize{{10.4}}{{15}}\selectfont\color{{teal}}{title}')
 tex+=box(x+4,y+10.5,72,rf'\fontsize{{9.3}}{{14.1}}\selectfont {desc}')
(FIG/'features.tex').write_text(tex)
insights=[
 ('01','全球协作的深度，塑造开放生态的体系能力','欧洲的人才积累、中国的模型供给、印度与巴西的参与基础，体现全球开源的地域差异；增长速度与既有规模也不总是同向。将人才、组织、项目、代码、模型与数据统一观测，才能解释不同地区在创造、复用与维护中的分工及其时序变化。本报告主张把跨境接续、跨层支撑与长期维护纳入发展评价，以协作关系判断体系能力，为国际合作和公共投入提供依据。','1'),
 ('02','中国模型开源的领先，需要拓展为体系与协作优势','HF 期后观察中，Qwen 的衍生仓库达到 15.1 万个，显示以其为代表的中国模型处于全球开放复用生态的领先行列。围绕模型，训练推理、AI 工具链与异构算力适配正在分层展开；国家政策纳入开源贡献激励，xLLM 等项目进入基金会治理。下一步应以开放接口、共同评测与跨境维护连接国内产业和全球社区，使模型优势沉淀为长期体系能力。','2'),
 ('03','全球南方的潜力，在于成为共创者与治理参与者','本地语言、文化知识与真实场景，是全球南方参与 AI 开源的独特资源。Masakhane 的非洲语言协作展示了以数据共建、模型适配和社区研究进入全球创新网络的路径。基金会应发挥连接长期资金、中立治理、人才培养与跨境合作的关键作用。AI 普惠应支持当地伙伴共同定义问题、掌握维护能力并参与规则制定，把资源可及推进为可持续公共能力。','3'),
 ('04','杭州等成长节点提示：中国 AI 开源需要因地施策','中国 AI 开源呈现企业牵引、科研供给与社区接续并存的结构，模型、工具链与基础软件承担不同产业角色。人才规模、增长速度与模型供给指向不同的优势节点；杭州的开源人才增长与浙江的模型供给值得联读。地方决策应区分研究、工程适配、长期维护与应用人才需求，围绕自身产业补齐协作环节，通过跨城、跨境项目合作形成特色。','4')]
tex=''
for i,(n,title,body,source_id) in enumerate(insights):
 y=79+i*46
 tex+=box(22,y,14,rf'\digits\bfseries\fontsize{{20}}{{25}}\selectfont\color{{blue}}{n}')
 tex+=box(40,y,148,rf'\sffamily\bfseries\fontsize{{11.2}}{{16}}\selectfont {title}')
 tex+=box(40,y+10,148,rf'\fontsize{{10.4}}{{16.4}}\selectfont {body}\textsuperscript{{\color{{teal}}[{source_id}]}}')
(FIG/'insights.tex').write_text(tex)
(ROOT/'sources/summary-content.json').write_text(json.dumps({'version':'v0.4','features':features,'insights':insights},ensure_ascii=False,indent=2)+'\n')
print('Generated v0.4 executive-summary figures.')
