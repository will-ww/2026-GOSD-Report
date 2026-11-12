from common import *
def refline(y,label,url):
 return '\\Box{15}{'+str(y)+'}{180}{\\sffamily\\fontsize{9.1}{13.5}\\selectfont\\href{'+url+'}{'+esc(label)+'}}\n'
def appendices(start=14):
 s=''
 s+=rf'\begin{{canvas}}\Header{{附录 A · 本章数据说明}}{{teal}}\Footer{{{start:02}}}\pdfbookmark[1]{{附录 A · 样本、指标与时间}}{{app1}}'+'\n'
 s+=box(15,27,180,'附录 A　样本、指标与时间',20,27,'ink',True)
 s+=box(15,42,180,'主统计期为 2025 年 7 月 1 日至 2026 年 6 月 30 日。全景名单是固定观察目录，允许用期后名单回看历史；不把名单规模解释为当期新增或全行业规模。',10,15.5,'muted',False,True)
 s+=box(15,65,180,'一、各节的数据范围',12,17,'teal',True)
 rows=[('4.1 Agentic AI','145 项 / 25 类','143 项有主期记录；107 项满 12 月。'),('4.2 模型任务','96 个模型仓库','六类各 16 项；2026.10.02 近期下载快照。'),('4.3 云基础设施','86 个仓库','86 项有主期记录；82 项满 12 月。'),('4.4 数据库系统','93 个仓库','93 项有主期记录；86 项满 12 月。'),('4.5 RISC-V','78 个仓库','78 项有主期记录；19 项满 12 月；3 项分类待核。'),('4.6 PyTorch','83 个仓库','83 项有主期记录；17 项满 12 月；1 项分类待核。')]
 for i,(sec,n,note) in enumerate(rows):
  y=76+i*14
  if i%2==0:s+=rf'\Rect{{15}}{{{y-1}}}{{180}}{{14}}{{paper}}'+'\n'
  s+=box(17,y,47,sec,9.5,14,'ink',True)+box(65,y,38,n,9.4,14,'teal')+box(105,y,88,note,8.9,12.5)
 s+=box(15,166,180,'二、OpenRank：协作网络中的影响位置',12,17,'teal',True)
 s+=box(15,177,180,'OpenRank 根据开发者与项目的协作联系衡量网络影响。本章榜单累计主统计期内已有月值；不足 12 月的记录不补零、不外推。它不等同提交量、下载量、技术性能或市场份额。类别按主要功能去重，同一仓库不在类间重复计分。',10,15.5)
 s+=box(15,206,180,'主期项目分值于 2026.11.10 从 OpenDigger 查询，按仓库 ID 与月份核对；4.3—4.6 共 325 个不同仓库取得 6,510 条两年度记录，无同月多值冲突。跨小节的共同项目分别服务各自问题，不再相加为全章总量。',10,15.5)
 s+=box(15,235,180,'三、模型下载：资源获取，不是独立用户',12,17,'teal',True)
 s+=box(15,246,180,'HF 通过特定文件请求统计模型下载，不同运行库的计数文件有所不同。4.2 使用固定底表的近期下载字段，不与主期 OpenRank 混合；保留测试、格式转换和重打包仓库，发布账户地域不等于原始训练方或用户地域。各类选样范围及许可状态仍需逐项核验。',10,15.5)
 s+=r'\end{canvas}'+'\n'
 s+=rf'\begin{{canvas}}\Header{{附录 A · 来源与地域说明}}{{teal}}\Footer{{{start+1:02}}}\pdfbookmark[1]{{附录 A · 地域口径与主要来源}}{{app2}}'+'\n'
 s+=box(15,27,180,'附录 A　地域口径与主要来源',20,27,'ink',True)
 s+=box(15,43,180,'一、国家贡献：公开文件所覆盖的子样本',12,17,'teal',True)
 s+=box(15,54,180,'图 4-4、4-8、4-9 的国家份额取自 OpenDigger 公开项目标签的 contributions 字段，与 OpenShare 对应组件同源。该字段按贡献者所在地汇总归一化社区 OpenRank；读取日为 2026.11.10，逐文件未完整记录贡献数据的精确起止日，统一作为期后观察。',10,15.5)
 s+=box(15,85,180,'按可见成员范围剔除内部重叠、跨类或相互交叠标签，4.1 保留 96 个标签（关联 96/145 项、24 类），4.3 保留 37 个标签（37/86 项），4.4 保留 62 个标签（65/93 项）。标签可包含多个仓库，不等于主期排行榜的主要仓库口径。',10,15.5)
 s+=box(15,116,180,'未识别地域贡献未随公开文件导出，份额只以已识别部分为分母；各项目开发者人数不相加。中国相关地域按报告统一规范汇总。4.1 尚未覆盖 PyTorch、OpenClaw、vLLM、SGLang 等重要项目，因此不能据本页样本推断完整全景的国家领先地位。',10,15.5)
 s+=box(15,148,180,'4.5 和 4.6 的可用公开标签不足以形成代表性的国家图，本稿分别采用功能分工与组织型案例。项目发起方、仓库组织、发布账户地域和贡献者所在地是不同关系；任何一种都不能单独证明治理控制权。',10,15.5)
 s+=box(15,177,180,'二、主要来源（点击名称可追溯）',12,17,'teal',True)
 refs=[('2026 版技术生态固定目录与底表 · c51e344', 'https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/tree/c51e3441361407b68f10b339d97eff288319b503/data/processed/chapter4'),('蚂蚁 Agentic AI Landscape · 固定分类 e330d75','https://github.com/antgroup/agentic-ai-landscape/tree/e330d75ea4ca314bc81f6868df63425c8acca5e3'),('OpenDigger · 指标定义与公开数据导出实现','https://github.com/X-lab2017/open-digger/blob/5c2ffc4f5b3dd37ebcb20514c7abfee6853bd830/src/cron/tasks/monthlyExport.ts'),('Hugging Face · 模型下载统计说明','https://huggingface.co/docs/hub/models-download-stats'),('PyTorch 上游全景 · 固定资源 bd7a339','https://github.com/pytorch-fdn/landscape/tree/bd7a33990fd445802d45c10e3679278358c958c3'),('PyTorch · 基金会与治理职责','https://pytorch.org/foundation/'),('PyTorch · 技术治理规则','https://docs.pytorch.org/docs/2.15/community/governance.html'),('PyTorch · 技术咨询委员会（TAC）','https://pytorch.org/tac/'),('PyTorch · 云资源计划','https://pytorch.org/credits/')]
 for i,(name,url) in enumerate(refs):s+=refline(188+i*8.4,name,url)
 s+=box(15,268,180,'公共价值建议基于可见机制提出；本章未以组织身份、下载或协作分值推算降本成效。',8.9,12.7,'muted')
 s+=r'\end{canvas}'+'\n';return s
