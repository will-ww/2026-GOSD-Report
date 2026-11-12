from build import *
def heading(y,t):return box(15,y,180,t,11.3,16,'teal',True)
def make_appendix():
 t=r'\begin{canvas}\Header{附录 1 · 行业地图口径与来源}{teal}\Footer{A1}'+'\n'
 t+=box(15,28,180,'附录 1｜行业地图口径与证据',20,27,'ink',True)
 t+=heading(46,'1  观察对象、时间与分类含义')
 t+=box(15,55,180,'本节为期后专题，不并入 2025.07—2026.06 主统计期。2026-11-09 从 OpenDigger 所跟踪的公开、非 Fork（非平台复制）仓库中，按创建年份各抽取 4,000 个；候选池合计 269,767 个。以文本前 2,000 字符的 ASCII 比例大于 90% 近似筛选英文，保留 18,086 个。未逐仓核验开源许可。NAICS 原用于企业经营单位，本研究将其迁移为仓库应用领域标签；覆盖 19 类，不含企业管理类（55）。',9.4,14.5)
 t+=heading(90,'2  分类可靠性与图表复核')
 t+=box(15,99,180,'采用 NAICS-GH 的 5,270 个训练及验证样本训练词语与字符特征的线性分类器，独立测试 1,318 个。准确率 76.3%，加权 F1 为 75.8%；F1 同时衡量误分与漏分。专业科技服务 F1 为 0.54，金融为 0.90，公用事业为 0.88，各类可靠性不一，且测试集表现不等于本研究样本准确率。图 2.8-3 的 30 个分年值由附件矢量曲线恢复，并与整数分母及 2025 汇总表核对；原始行业分年明细仍待补归档。',9.4,14.5)
 t+=heading(134,'3  AI 提及的含义与统计边界')
 t+=box(15,143,180,'在简介、标签与 README（项目说明）的合并文本前 1,800 字符中识别 AI／机器学习关键词；窄词表去掉泛化机器学习用语。文本来自同一快照，年份只代表创建群体，不能定位实际采用时间、推断生成式 AI 的因果影响或外推到 2030。行业占比的 Wilson 95% 区间不覆盖分类错误、词表误差及样本偏差。',9.4,14.5)
 t+=heading(173,'4  证据来源')
 t+=box(15,182,180,'[S1] 团队研究稿：Stable Structure, Uneven Diffusion: A Reproducible Industry-Level Study of AI Mentions in Open Source；配套《开源仓库行业版图数据报告》及复现包，2026-11-09 快照。正文数值优先采用复现包汇总表。',8.8,12.5,'muted',False,True)
 t+=r'\Box{15}{203}{180}{\sffamily\fontsize{8.8}{12.5}\selectfont\color{muted}[S2] Xu, K. \& Quispe, A. (2026). \href{https://arxiv.org/abs/2607.06505}{Industry Classification of GitHub Repositories Using the North American Industry Classification System (NAICS). arXiv:2607.06505.}}'+'\n'
 t+=r'\Box{15}{218}{180}{\sffamily\fontsize{8.8}{12.5}\selectfont\color{muted}[S3] \href{https://huggingface.co/datasets/aquiro1994/naics-gh}{NAICS-GH 数据集（6,588 个带标签仓库）}；[S4] \href{https://www.census.gov/naics/}{美国人口普查局：NAICS 官方说明}。外部资料核查于 2026-11-10。}'+'\n'
 t+=heading(236,'5  版本、待核查项与评审重点')
 t+=box(15,245,180,'v0.2 重绘行业位次与规模、AI 总体与行业差异、AI 仓库构成与热力矩阵三幅综合图；压缩方法性配图与说明卡片。待核查：行业分年原始明细、专业科技及小样本分类、多语覆盖和实际复用案例。请重点评审宏观结构与行业差异是否更清楚，图表信息取舍是否恰当；暂不将探索性行业排序提升为全面领先或采用率结论。',9.4,14.5)
 return t+r'\end{canvas}'+'\n'
