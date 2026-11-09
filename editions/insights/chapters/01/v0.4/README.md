# 第一章 v0.4：紧凑信息图与关联观察

2026-11-09 · 8 页 · **待作者 PDF 评审**。基于 [v0.3](../v0.3/README.md)，保留主统计期、三节结构及既有数值。

- SDGs、数字公共品条件与公共能力实施门槛合为一页。17 项目标与 9 项要求分别列示，不制造逐项映射。
- OSDGs 用获批标识连接四个支柱，十维编号、名称与图标完整保留。
- OSDI 的 4 目标、10 方向、29 项候选指标，与六类对象的关联观察合页；三类用途另行列示。
- 中国模型复用、参与／贡献／影响力、四视角阅读路径统一为清晰的矢量关系信息图。

## 构建与复用

设置仓库外母稿路径 `GOSD_2026_SOURCE_PDF`，运行 `bash build.sh`。`build_figures.py` 提供基础图与数据，`build_infographics.py` 生成本轮改绘图件；公共函数见 `editions/insights/scripts/infographic_primitives_v1.py`。与前置 v0.5 合稿使用 `build_compact_review_pack.py`，同步生成八张 SVG。PDF、字体、第三方原始材料不入库。

数据与来源保留于 `sources/`、`review/`，本轮新增记录见[紧凑信息图评审](../../../reviews/2026-11-09-compact-infographics.md)。29 项仍是候选指标，不表示已完整测量；统计窗口、样本范围及原有待核查项不变。
