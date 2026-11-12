from build import *

def begin(title,num):return rf'\begin{{canvas}}\Header{{第二章 · 全球开源生态地图}}{{teal}}\Footer{{{num}}}'+'\n'+box(15,28,180,title,20,26,'ink',True)
def end():return '\\end{canvas}\n'
def head(y,t):return box(15,y,180,t,12,18,'teal',True)
def para(y,t,w=180,x=15,fs=10.3):return box(x,y,w,t,fs,16.5)
def opening():
 t=begin('第二章｜全球开源生态地图','01')
 t+=box(15,44,180,'从参与分布，走向协作能力与行业价值',15,22,'teal',True)
 t+=para(60,'人工智能扩大了开放资源的类型，也改变了生产与协作的节奏。看清这一变化，需要把人、贡献、项目、人才、代码、模型与数据放在相互联系的观察框架中，再追问这些资源能够服务哪些行业和社会需求。')
 t+=para(85,'本章围绕六类相互衔接的主题地图展开这一问题。这里的“地图”既指地域分布，也指生态结构：全球视野揭示不同地区的参与路径，中国观察连接本地建设与跨境协作，行业专题则把视线进一步引向资源的应用条件。')
 t+=head(114,'六节阅读路径')
 rows=[
 ('2.1','活跃地图','谁在参与，增长发生在哪里？','规模、平台覆盖与区域增长','02—04'),
 ('2.2','贡献地图','参与怎样进入共同协作？','贡献结构、平均贡献与跨境连接','05—08'),
 ('2.3','项目影响地图','协作影响汇聚到哪些项目？','网络位置、项目结构与持续积累','09—11'),
 ('2.4','人才地图','哪些地域积累了关键参与者？','高影响力样本与中国城市节点','12—13'),
 ('2.5','资产地图','协作形成了怎样的资源供给？','代码、模型、数据与下载分布','14—17'),
 ('2.6','行业地图','资源可能进入哪些应用领域？','行业构成与 AI 表述差异','18—20')]
 for i,(n,name,q,v,p) in enumerate(rows):
  y=126+i*17
  t+=rf'\Rule{{15}}{{{y+15}}}{{195}}{{line}}'+'\n'
  t+=box(15,y,11,n,11,15,'teal',True)+box(29,y,40,name,11,15,'ink',True)
  t+=box(72,y,105,q,10.3,15)+box(72,y+6,105,v,8.8,12,'muted',False,True)
  t+=box(179,y,16,p,8.5,12,'muted',False,True)
 t+=head(237,'读图时，始终区分三件事')
 t+=para(248,'参与规模、资源供给与实际成效分别计量；报告年度、自然年及期后资料分别标注；观察结果与条件情景、行动建议分别表述。正文保留必要定义，附录 A 统一说明口径、情景计算与来源。',fs=10)
 t+=box(15,273,180,'章末启示与行动方向　21　｜　附录 A：第二章方法与证据　A1—A6',8.7,12,'muted',False,True)
 return t+end()

def closing():
 t=begin('本章小结｜从生态分布到公共能力','21')
 t+=para(45,'六节观察呈现出一个共同问题：参与增长、资源扩张和协作影响具有不同的地域与行业结构。将开放资源转化为可持续公共能力，需要连接参与者、维护团队、使用场景与长期责任，不能只扩大可见数量。')
 t+=head(71,'本章形成的三项判断')
 jud=[
 ('全球协作具有多种参与位置','人数、贡献和项目影响呈现不同次序。中国既有本地资源建设，也参与跨境协作；任何单一平台份额都不足以概括整体能力。'),
 ('规模积累与成长节点需要并看','印度、南方六国和中国城市样本显示不同成长节奏。增长提供合作机会，但不自动证明人才留存、项目维护或公共成效。'),
 ('资源扩张使应用条件更加关键','代码、模型与数据的数量和下载分布并不重合；行业 AI 表述提供探索线索，实际应用还需具体任务与结果证据。')]
 for i,(h,b) in enumerate(jud):
  y=82+i*22;t+=box(15,y,180,h,10.7,16,'ink',True)+box(15,y+6,180,b,9.8,15)
 t+=head(153,'行动方向｜在未来 6—12 个月形成可检验进展')
 t+=box(15,164,180,'以下由本章证据引出的建议，供第六章综合评议；尚不是已验证的政策效果。',9,13,'muted',False,True)
 rows=[
 ('分层评价地区能力','政府与研究机构','据图 2-1—2-10，同列参与、贡献和项目影响；保留覆盖与时期。以同口径复算及项目抽样，检查增长是否伴随持续协作。'),
 ('支持跨境共同维护','基金会与项目团队','据图 2-7、2-10，选择有明确需求的合作项目，配置多语文档、评审与维护资源。记录贡献采纳、共同维护职责及交接情况。'),
 ('建设本地可用资源','本地伙伴与公共机构','据图 2-2、2-13—2-16，与南方社区共同确定语言和行业任务，配置适配、数据治理与维护预算；跟踪可获得性、成本与持续使用。'),
 ('以城市和行业任务试点','地方部门、高校与企业','据图 2-12、2-17—2-19，连接维护者与真实需求；以成本、本地化、维护责任和实际结果四项记录检验成效，避免仅以数量验收。')]
 for i,(h,who,b) in enumerate(rows):
  y=176+i*22
  t+=rf'\Rule{{15}}{{{y+20}}}{{195}}{{line}}'+'\n'
  t+=box(15,y,43,h,10,14,'teal',True)+box(15,y+7,43,who,8.2,12,'muted',False,True)
  t+=box(62,y,133,b,9.4,14.3)
 t+=box(15,269,180,'下一步：第三章识别关键主体，第四、五章进入技术与模型生态；第六章综合跨章证据，形成预测与行动建议。2030 情景持续校准，不作为政策效果承诺。',9,13.3,'muted')
 return t+end()

def table(x,y,w,headers,rows,widths=None,fs=9.2,leading=13.3):
 n=len(headers)
 spec=('@{}p{44mm}'+r'>{\raggedleft\arraybackslash}X'*(n-1)+'@{}') if widths is None else '@{}'+''.join('p{'+str(v)+'mm}' for v in widths)+'@{}'
 z=rf'\sffamily\fontsize{{{fs}}}{{{leading}}}\selectfont\renewcommand{{\arraystretch}}{{1.1}}\setlength{{\tabcolsep}}{{4pt}}\begin{{tabularx}}{{{w}mm}}{{{spec}}}\toprule '
 z+=' & '.join(esc(a) for a in headers)+r'\\\midrule'+'\n'
 for row in rows:z+=' & '.join(esc(a) for a in row)+r'\\'+'\n'
 z+=r'\bottomrule\end{tabularx}'
 return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{{z}}}'+'\n'

def apbegin(title,i):return rf'\begin{{canvas}}\Header{{附录 A · 第二章方法与证据}}{{teal}}\Footer{{A{i}}}'+'\n'+box(15,28,180,title,20,26,'ink',True)

def appendix1():
 t=apbegin('附录 A｜指标与统计覆盖',1)
 t+=box(15,43,180,'本附录统一解释第二章 19 幅图的指标、时期和样本条件。基础数据来自固定归档与注明窗口的公开资料；尚未完成核验的生产与筛选条件分别说明。',9.8,15.5,'muted',False,True)
 t+=head(64,'A1.1  核心指标：每一种计量回答一个问题')
 defs=[
 ('活跃与累计','活跃是报告期内留下公开活动记录的账号，可能包括收藏、讨论或代码活动；累计还含当期未活跃账号。两者均非职业人口、国籍或 AI 研发人数。'),
 ('贡献与项目影响','开发者贡献 OpenRank 按协作网络计算，再按地域汇总；项目影响 OpenRank 观察项目的网络位置。二者对象不同，不相加，也不替代质量、收入或公共成效。'),
 ('平均贡献','同一时期、同一表的贡献总量÷活跃账号数，是地区比值；不是个人分布的中位数，也不是生产效率。同比与净增均为相邻期总量变化。'),
 ('人才与数字资源','人才采用个人全域 OpenRank 前 5% 样本。资产计量仓库、模型和数据记录；不等同于原创作品数、法律权属或货币价值。具体限制见 A4。'),
 ('下载与 AI 提及','下载为资源获取记录，不等于用户数或生产采用。AI 提及为仓库文本出现词表术语，不等于功能实现、采用时间或行业应用率。')]
 for i,(h,b) in enumerate(defs):
  y=77+i*25;t+=box(15,y,30,h,10,15,'teal',True)+box(48,y,147,b,9.6,14.6)
 t+=head(204,'A1.2  三类时间、三套覆盖')
 t+=box(15,215,180,'报告年度：2026 年度为 2025-07-01—2026-06-30，历史年度按同样跨年窗口。自然年：贡献、项目影响部分历史及平均贡献另按 1—12 月。期后与独立窗口：2026 年 7 月人才快照、HF 夏季资料、Octoverse 独立年度，以及 11 月行业快照均单独标明。',9.6,14.8)
 t+=box(15,242,180,'国家及省级 GitHub 估计、编制组五域综合序列、中国跨平台补充分别阅读。中国跨平台约 370 万＝GitHub 250.48 万＋国内平台去重补充约 120 万；不回填历史、不分摊省份、不再加入五域。五域中国为 454.534 万，两种综合数不能互换。',9.6,14.8)
 t+=box(15,269,180,'地理标签表示可观察所在地或发布归属，不表示国籍。台湾、香港、澳门纳入中国；地图为统计示意，正式出版继续复核地图规范。',8.7,13,'muted',False,True)
 return t+end()

def appendix2():
 s=json.loads((R/'upstream/2.1/data/scenarios-v03.json').read_text())
 t=apbegin('附录 A｜历史与情景方法',2)
 t+=head(45,'A2.1  参与历史｜2022—2026 报告年度')
 names={'全球南方代表国家':'南方六国'}
 seq=[(names.get(k,k)+'／万',v) for k,v in s['groups'].items()]
 seq += [(n,s['global_and_china'][k]) for k,n in [('total','全球累计／亿'),('active','全球活跃／万'),('china','中国 GitHub／万')]]
 t+=table(15,57,180,['对象／单位','2022','2023','2024','2025','2026'],[[n]+[f'{v:,.2f}' for v in d['history']] for n,d in seq],fs=9.2)
 t+=head(116,'A2.2  对应的 2030 情景端点')
 t+=table(15,128,180,['对象／单位','历史年均增速','逐步放缓','历史延续'],[[n,f'{d["annual_growth"]*100:.2f}%',f'{d["slowing"][-1]:,.2f}',f'{d["continued"][-1]:,.2f}'] for n,d in seq],fs=9.2)
 t+=head(188,'A2.3  统一算法与使用条件')
 t+=box(15,199,180,'历史年均增速 g＝（末值÷首值）的四次方根−1。以末年为起点，延续情景每年按 g 复利增长；放缓情景第 h 年的增速为 g 乘以 0.8 的 h 次方，逐年复利。报告年度从 2027 年推演，自然年序列从 2026 年推演，均延长到 2030 年。',9.6,15)
 t+=box(15,226,180,'0.8 为预设敏感性参数，并非拟合结果；两条路径不构成概率预测、置信区间或上下限承诺，也未单独估计 AI 与政策的因果效应。计算保留未舍入值，表格仅为展示取整。覆盖或生产规则变化时，须先校准序列再更新情景。',9.6,15)
 t+=box(15,254,180,'五域不是全球完整分区。南方六国为巴西、印度尼西亚、越南、菲律宾、埃及、南非，印度单列；六国综合序列与 GitHub 细分不同。欧洲成员及历史聚合执行记录仍待补齐。',9.3,14.5,'muted')
 return t+end()

def appendix3():
 d=json.loads((R/'upstream/2.2/data/scenarios-v02.json').read_text());p=json.loads((R/'upstream/2.3/data/derived-v01.json').read_text())
 names={'Europe':'欧洲','China':'中国','United States':'美国','Global South representatives':'南方六国','India':'印度','Global':'全球','global':'全球','CN':'中国','US':'美国'}
 t=apbegin('附录 A｜贡献与影响情景读数',3)
 t+=box(15,43,180,'单位均为万 OpenRank。每行的历史首末值与 A2 算法足以复算端点；报告年度（2022→2026）与自然年（2021→2025）分别计算，覆盖不同，不用于相互换算。',9.6,15,'muted',False,True)
 def rows(groups,tag):
  out=[]
  for k,v in groups.items():
   n=names.get(k,k);out.append([n+'·'+tag,f'{v["history"][0]:,.2f}',f'{v["history"][-1]:,.2f}',f'{v["slowing"][-1]:,.2f}',f'{v["continued"][-1]:,.2f}'])
  return out
 t+=head(66,'A3.1  开发者贡献')
 rows1=rows(d['five_group_report_years'],'报告')+rows(d['natural_years'],'自然')
 t+=table(15,78,180,['对象·窗口','历史首值','历史末值','2030 放缓','2030 延续'],rows1,fs=9.1)
 t+=head(139,'A3.2  项目影响')
 rows2=rows(p['five_domain_scenarios'],'报告')+rows(p['natural_year_scenarios'],'自然')
 t+=table(15,151,180,['对象·窗口','历史首值','历史末值','2030 放缓','2030 延续'],rows2,fs=9.1)
 t+=head(214,'A3.3  连接解释，保留证据边界')
 t+=box(15,225,180,'贡献来源与项目归属可以分离：同一地区的参与者可能建设其他地区的项目。图 2-8 的三类份额使用同一组 29 国，但分别以活跃人数 2,181.30 万、贡献度 1,147.66 万、项目影响 222.08 万为分母，不能互作“转化率”。',9.6,15)
 t+=box(15,252,180,'国家公开表含地理估计，相关生产代码有年度调整处理，具体执行映射仍需核对。五域是独立归档；中国五域与国家公开表的差额不能全部解释为国内平台贡献。',9.3,14.5,'muted')
 return t+end()

def appendix4():
 t=apbegin('附录 A｜样本与资产口径',4)
 blocks=[
 (45,'A4.1  跨境协作与中国项目',
 '图 2-7 依据中美项目来源前十表，共 20 条记录、14 个来源国家，主期为 2025.07—2026.06。项目完整名单尚未补齐，结论限于原表样本；未列来源保持未知。图 2-10 的 30 项标签合计 176,313.03 OpenRank，时间窗口、标签重叠和归属规则待核，不作为全国完整项目总量。'),
 (89,'A4.2  人才与固定十城',
 '沿用“个人全域 OpenRank 前 5%”定义；比较总体、得分窗口、并列处理、身份去重和机器人剔除执行记录仍待核。全球地图为 2026 年 7 月快照，五域、十城为报告年度，不能相互拼接。十城合计 3,590 人仅是固定样本；人数变化不等于迁移、留存或政策效果。'),
 (133,'A4.3  代码：存量、活跃与事件分开计量',
 'Innovation Graph 为季末公开仓库存量，按具有事务分拣（triage）及以上权限成员的地域众数归属，包含不活跃仓库。排除欧盟汇总行避免重复，中国合并内地及港澳台；4.54 亿为已披露地域合计，历史均取第二季度。活跃仓库沿用年度归档，GitHub 与 Gitee 未跨平台去重，不能相加或与存量求统一活跃率。'),
 (183,'A4.4  模型与数据：发布归属不等于用户位置',
 '地域归档覆盖 826 个发布单位、63 个国家与地区：模型 72,280 个、下载约 600 亿次；数据集 12,291 个、下载约 8.06 亿次。原表分别列 14 个地域，未列不补零；快照、筛选及累计下载窗口待核。资源公开不自动等于符合完整开源条件，下载也不等于部署。'),
 (227,'A4.5  平台资料与独立研究另用自己的窗口',
 'HF 夏季材料为 2026 年 1—8 月，部分分析截至 7 月；日度模型曲线截至 2025-12-08。Longpre 等比较全历史模型与 2024.08—2025.08 新发布模型，并采用滚动窗口过滤；两组不是可直接相减的年度市场份额。机器人数据集沿用 HF 春季材料的 2024、2025 年计数。')]
 for y,h,b in blocks:t+=head(y,h)+box(15,y+10,180,b,9.4,14.5)
 return t+end()

def appendix5():
 t=apbegin('附录 A｜行业专题方法',5)
 blocks=[
 (45,'A5.1  期后快照与样本构成',
 '2026-11-09 在 OpenDigger 跟踪的公开、非 Fork（非平台复制）仓库中，按 2021—2025 创建年份各抽取 4,000 个，候选池共 269,767 个。以前 2,000 字符中 ASCII 比例大于 90% 近似筛选英文，保留 18,086 个；各年依次为 3,761、3,713、3,635、3,516、3,461。未逐仓核验许可，不能外推到全部 GitHub 或中国、全球南方整体。'),
 (94,'A5.2  从行业标准到仓库应用标签',
 'NAICS 原用于企业经营单位，本研究迁移为仓库应用领域标签，覆盖 19 类，不含企业管理类（55）。采用 NAICS-GH 的 5,270 个训练及验证样本训练词语、字符特征线性分类器，另以 1,318 个测试。准确率 76.3%，加权 F1 为 75.8%；F1 同时衡量误分与漏分。专业科技服务 F1 为 0.54，金融为 0.90，公用事业为 0.88；测试表现不等于本章样本准确率。'),
 (149,'A5.3  AI 表述、群体差异与统计区间',
 '在简介、标签和 README（项目说明）合并文本前 1,800 字符识别 AI／机器学习词语；窄词表去掉泛化机器学习用语。所有文本来自同一快照，年份只表示仓库创建群体，不能还原历年采用率或识别生成式 AI 的因果影响。Wilson 95% 区间只反映抽样波动，不覆盖分类错误、词表误差或样本选择偏差；图中另标 n＜100 的行业。'),
 (204,'A5.4  图表复核与待补证据',
 '图 2-17 的 Spearman 位次相关系数按原研究结果报告，图上并列名次按最小名次表示。图 2-19 的 30 个行业分年值由提供的矢量图恢复，结合整数分母校准，并与 2025 汇总表核对；原始分年明细仍待补归档。专业科技与小样本分类应抽查，多语覆盖、实际复用与行业结果需要进一步证据。')]
 for y,h,b in blocks:t+=head(y,h)+box(15,y+10,180,b,9.5,14.8)
 t+=box(15,266,180,'本专题只提供结构线索：不把 AI 关键词视为应用成效，不将创建群体差异延长为 2030 数值预测。',9.2,13.5,'muted',False,True)
 return t+end()

BASE='https://github.com/will-ww/2026-GOSD-Report/tree/497478a19e92c676c225893a395738e747a71c8b/reports/round2-v2.0/source/chapters/02/modules/02/data/'
SOURCES=[
 ('S01','OpenShare · GOSD 年度统计与主统计期','https://open-share.com/insight/open-world/gosd','图 2-1—2-10；公开数据读取 2026-11-09，元数据更新 2026-10-08。'),
 ('S02','OpenShare · 全球宏观洞察（自然年）','https://open-share.com/insight/open-world','图 2-4—2-6、2-9 的自然年序列；须与报告年度分开。'),
 ('S03','GOSD 2026 编制组 · 第二章归档与补充资料',BASE,'图 2-1—2-16；公开归档 497478a，另含编制组确认的综合序列及平台补充。'),
 ('S04','OpenDigger · 宏观统计生产代码（固定版本）','https://github.com/X-lab2017/open-digger/blob/5c2ffc4f5b3dd37ebcb20514c7abfee6853bd830/src/dataProduction/openshareOverview.ts','地理估计与年度处理规则参考；与已发布 JSON 的执行映射待核。'),
 ('S05','GitHub Innovation Graph · Repositories / Datasheet','https://github.com/github/innovationgraph/blob/main/data/repositories.csv','图 2-13—2-14；读取 2026-11-10，数据版本 4b6d36c2。'),
 ('S06','GitHub · Octoverse 2026：Commits and pushes','https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/','图 2-14；独立观察窗口 2025.10—2026.09。'),
 ('S07','Hugging Face · State of Open Models: Summer 2026','https://huggingface.co/blog/state-of-open-models-summer-2026','图 2-13、2-15—2-16；1—8 月观察，部分分析截至 7 月。'),
 ('S08','Hugging Face · State of Open Source: Spring 2026','https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026','图 2-16 的机器人数据集计数：2024、2025 年。'),
 ('S09','F. Ríos / AI World · Two Million Models and Counting','https://aiworld.eu/story/hugging-faces-two-million-models-and-counting','图 2-15 的日度模型序列：2022-03-02—2025-12-08。'),
 ('S10','Longpre et al. · The Economies of Open Intelligence','https://www.dataprovenance.org/economies-of-open-intelligence.pdf','图 2-15 下载结构，采用原研究图 1 的群体和过滤条件。'),
 ('S11','团队研究 · Stable Structure, Uneven Diffusion','', '图 2-17—2-19；配套《开源仓库行业版图数据报告》、复现包及汇总表。'),
 ('S12','Xu & Quispe (2026) · GitHub Repositories / NAICS','https://arxiv.org/abs/2607.06505','行业分类参考论文，arXiv:2607.06505；非本章复现结果的替代。'),
 ('S13','NAICS-GH 数据集；美国人口普查局 NAICS','https://huggingface.co/datasets/aquiro1994/naics-gh','分类训练数据 6,588 个标注仓库；官方分类体系见 census.gov/naics。')]
def appendix6():
 t=apbegin('附录 A｜来源索引',6)
 t+=box(15,43,180,'图题已给出直接来源与关键窗口。以下索引提供可点击出处；图件、原表、派生数据和文件指纹保留在配套结构化源稿中。来源列示不消除各页注明的样本限制。',9.5,14.5,'muted',False,True)
 for i,(tag,name,url,note) in enumerate(SOURCES):
  y=64+i*15.8
  label=esc(name)
  if url:label=r'\href{'+url+'}{'+label+'}'
  t+=rf'\Box{{15}}{{{y}}}{{180}}{{\sffamily\fontsize{{9.3}}{{13.5}}\selectfont\textcolor{{teal}}{{{tag}}}\hspace{{2mm}}{label}}}'+'\n'
  t+=box(27,y+6,168,note,8.5,12,'muted',False,True)
 t+=r'\Box{15}{274}{180}{\sffamily\fontsize{8.6}{12}\selectfont\href{https://www.census.gov/naics/}{NAICS 官方说明}　｜　主统计期：2025-07-01—2026-06-30；期后及独立窗口已分别标注。}'+'\n'
 return t+end()

APPENDIX=[appendix1,appendix2,appendix3,appendix4,appendix5,appendix6]
