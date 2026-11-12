# GOSD 2026 精要版 · 2.2 全球开源贡献地图 v0.3

状态：2026-11-09 作者 PDF 评审稿，未获定稿批准。四页 A4 竖版正文、两页附录。未提交 GitHub。

## 本轮修改

v0.3 仅更新第三页及相关来源说明：恢复“参与与贡献 · 区域份额”，与地图、前 20、平均贡献组成四单元，新增对应的第四个分析点。其他正文页沿用 v0.2。以下保留整个小节的组成说明。

1. 全球贡献图保留地图及前 20 国家，新增 2025 同表活跃位次、贡献位次和平均贡献对照。
2. 五域历史延长至 2030 条件情景；补充全球、美国和中国自然年历史及情景，以及全球南方六国细分。
3. 中国图保留地图及省级前 20，恢复京沪粤、台湾＋浙江、其他地区的活跃与贡献份额对照，同时保留贡献总量前十地区的平均贡献与活跃人数。
4. 第四幅综合图新增来源网络、本土与跨境结构、来源累计集中度、中美各前十来源完整明细。

## 统计范围

- 主统计期：2025-07-01 至 2026-06-30。国家、省级当期图及南方六国采用 OpenShare 报告年度输出。
- 平均贡献采用 2025 自然年贡献和活跃人数同表配对；单位为 OpenRank／人，不是个人质量、效率或中位数。
- 五域历史为编制组 2022—2026 报告年度独立综合序列，不与国家公开估计拼接、混排或相加。欧洲成员和覆盖说明待核查。
- 全球、美、中历史为 OpenShare 自然年 2021—2025。其 2026—2030 均为条件情景；2026 点不是当期报告年度读数。
- 南方六国：巴西、印度尼西亚、越南、南非、菲律宾、埃及；不代表全球南方总体，印度在五域中单列。
- 中美协作图仅含各前十来源，共 20 条记录、14 个来源国家、2 个项目归属地。各样本的分母不同；未列份额保留未知。不可推出全国净输出、所有项目开放程度或 AI 因果关系。
- 底图继承 2026 版，中国包含台湾、香港、澳门。出版审图仍待完成。

区域份额使用同报告年度 34 地合计作分母。台湾与浙江合计活跃份额 18.858694%、贡献份额 24.333296%，差 5.474601 个百分点；独立舍入后为 18.9%、24.3% 和约 5.5 个百分点。详见 data/regional-shares-v03.json。

## 情景方法

各序列 g = (历史末年／首年)^(1/4) − 1。延续情景每年按 g 复利；放缓情景第 h 年按 g × 0.8^h 复利。五域推演四年，自然年推演五年。0.8 是敏感性参数；两条路径不是概率区间或置信区间。公式及完整年度推演见 data/scenarios-v02.json。

历史数据沿用已发布序列，未单独估计 AI 的因果效应，未剔除生产规则的数值调整。当前公开生产代码说明地域估计、国内平台补充及年度调整；代码与已发布 JSON 的版本对应仍待核验。

## 数据与出处

- 自然年 API：https://selfoss.open-digger.cn/openshare/overview/（contribution.json、developers.json、CN/ 同名文件、meta.json），本地 natural-*。
- 报告年度 API：https://selfoss.open-digger.cn/openshare/overview_half_year/，本地 half-*；绘图使用 contribution.json、CN-contribution.json、public-developers.json、public-CN-developers.json，验证与本轮 half-* 对应文件一致。
- 展示入口：https://open-share.com/insight/open-world ，报告年度入口 /gosd。
- 五域与项目来源：权威仓库 will-ww/2026-GOSD-Report 固定提交 497478a19e92c676c225893a395738e747a71c8b，reports/round2-v2.0/source/chapters/02/modules/02/data/22。
- 研究基线：fff392e957bab9fb6d89d49dea712af47484efaa；精要版排版延续已评审 2.1 v0.3。
- 数据生产代码：X-lab2017/open-digger 固定提交 5c2ffc4f5b3dd37ebcb20514c7abfee6853bd830，src/dataProduction/openshareOverview.ts。
- 来源样本说明：X-lab2017/2026-Global-Open-Source-Development-Report 固定提交 c51e3441361407b68f10b339d97eff288319b503，preview/content/cmap/flow-method.md。
- 来源读取日 2026-11-09，两个 API 元数据更新日均为 2026-10-08。输入文件 SHA-256 见 review/input-manifest.json。

## 复现

安装 Python 3、PyMuPDF、Pillow、fontTools，XeLaTeX、Inkscape、Noto CJK Sans/Serif 字体。在本目录运行 `python run.py`。图表由精确数值生成 SVG，转换为矢量 PDF，中文 XeLaTeX 排版并嵌入字体。核心文件：panels_v02.py、figures_content.py、content_v03.py、layout.sty。

源包包含结构化内容 content.json、原始数据、四幅 SVG、排版源和验证记录；不含 PDF、字体缓存和任何数据库凭据。本地输出目录可重新生成 PDF。

## 评审问题

- 平均贡献和总贡献的区别是否清楚？
- 五域及自然年的时间、覆盖和情景假设是否足够清楚？
- 第四幅图的来源结构能否支撑“全球接续与共同建设”，并自然导向采纳、维护及可持续公共能力？

本轮数值核验与页面检查见 review/validation.json、review/figure-qa.json。待核查项保留在 PDF 附录，不以草稿替代正式确认。
