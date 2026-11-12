# GOSD 2026 精要版 · 2.5 全球开源资产地图 · v0.3

日期：2026-11-10。状态：作者评审稿，尚未批准。未提交 GitHub。

交付为 4 页 A4 竖版地图图文及 1 页来源附录。正文有总览、代码、模型、数据四幅组合图，各对应 4 项解读。图号暂定 2-13—2-16，后续合稿顺延。

## 本轮修改

- 总览融合三类资产的规模、全球位置、增长和数量／下载份额。
- 代码地图加入 GitHub 官方公开仓库地域底表及前 20 位；绘制 2020—2026 Q2 四国增长。活跃仓库另列 GitHub 与 Gitee 的原报告年度记录；年度提交、公开贡献来自 Octoverse 2026。
- 模型地图保留发布者样本，加入 HF 日度模型增长、DeepSeek-R1 历史锚点、GGUF 格式仓库增长，以及独立研究的模型群体下载结构。
- 数据地图保留样本数量及下载差异，加入平台总量和机器人数据集增长。
- 已逐页渲染检查；四幅 SVG 文字边界与重叠检查通过；PDF 全部字体嵌入，全部页面为 A4 竖版。

## 数据与出处

完整可点击来源列于 data/sources.json 及 PDF 附录。

1. `data/repositories.csv`：GitHub Innovation Graph 原始公开仓库地域表，获取于 2026-11-10，Git blob SHA 为 `4b6d36c2c4c835a43af29575afd3a041bab24d34`。`data/innovationgraph-methods.md` 保留数据定义。`repo-countries.json` 为逐季地域转换：排除 EU 汇总行；中国合并 CN、HK、MO、TW；空值不补零。地图为公开仓库存量，包括不活跃仓库，并非活跃仓库的地理分布。4.54 亿为已披露地域加总。
2. `data/25/raw/platform_active_repositories.csv`：报告已归档活跃仓库年度序列；2026 报告年度为 2025-07-01—2026-06-30。使用 GitHub 与 Gitee 两列，未使用存在名称映射问题的 GitCode 列。该表和公开仓库存量不能计算活跃率。
3. `data/25/raw/publisher_sample_extract.json`：固定原报告的累计发布单位样本（826 家、63 个国家与地区），分别列出 14 个地域。原稿模型总量 72,280、数据集 12,291；下载原值 60,000,691,937、806,478,232。快照日期及底层筛选细节待核，不替代当期平台普查。
4. `data/hf-daily-models.csv`：AI World / Francisco Ríos 的 HF 模型日度记录，2022-03-02—2025-12-08，末值 2,264,880。原始交互图 `https://franri.dev/pages/CEPS/HF2025/v13/viz_anim.html`；DeepSeek-R1 锚点日期 2025-01-20 来自同图发布事件标记。此标记只表示时间位置，不作增长因果归因。
5. HF Summer 2026：公开模型从 243 万至 296 万，数据集从 71.1 万至 100 万；GGUF 声明格式仓库前七个月增长 464%。平台总量依据 1—8 月端点，增幅复算为约 21.8% 和 40.6%；不将平台和样本数混加。
6. HF Spring 2026：机器人数据集 2024 年 1,145、2025 年 26,991。忠实呈现原文年度数值，不自行断言其为全平台总存量或逐年净新增。
7. Longpre 等《The Economies of Open Intelligence》，图 1：全历史模型下载与 2024.08—2025.08 新发布模型下载两个群体；使用 Rolling Window Filter。个人与跨地域组织分别合计 50.0%、57.6%。这些比例与原报告发布者样本不是同一口径。

地理底图为 Natural Earth 低分辨率底图，采用 Equal Earth 投影。台湾与中国大陆使用同一中国合并数据与色彩，不另列地域。地图不编码用户下载所在地。

## 构建

依赖：Python 3（Pillow、fontTools、PyMuPDF、pyshp、pycountry）、XeLaTeX、Inkscape、Noto CJK 字体。执行 `python run.py`。

`build.py` 从系统 Noto CJK 字体提取简体中文 OTF，并生成 XeLaTeX 格式缓存；`assets_v03.py` 生成精确 SVG/PDF 图件及结构化正文；`run.py` 生成中文 PDF、页面预览、来源记录。排版模板为已采用的 GOSD 精要版视觉体系。

`data/content.json` 是结构化正文；`figures/` 可直接复用到后续 Web 或排版；`report.tex` 为本次生成的书稿；`review/` 包含最终结构检查结果。源包不包含 PDF、字体缓存或数据库凭据。

## 待核查与评审重点

待核查：发布者地域样本的快照日期与筛选细节；活跃仓库底层事件规则。已明确标注，不阻断有证据支持的叙事。

建议本轮评审四页的信息密度、三类资产的整合清晰度，以及中国贡献、全球南方与公共能力主张的支撑力度。
