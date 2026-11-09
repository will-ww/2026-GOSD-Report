# 2026 全球开源发展报告·精要版

管理基线 v1.0 · 2026-11-09；前置稿 v0.3 · 9 页。正式发布日期尚未确定。

本目录独立管理约 100 页精要版的研究、编辑、证据和评审，以 2025 版与 2026 版为核心材料，形成贯穿全书的人工智能时代叙事。首要读者是政府与国际组织决策者，兼顾产业、基金会、研究机构与社区。

**定位：从中国出发的全球视野，以跨平台、体系化、全域数据观察连接人才、组织、项目、代码、模型与数据，解释全球协作如何形成体系能力和可持续公共能力。** “全域”描述观察范围与研究目标，不意味着全部平台、人口或关系已被完整测量。

## 工作入口

| 内容 | 入口 | 当前状态 |
| --- | --- | --- |
| 精要版宪法补充 | [constitution.md](constitution.md) | 已确认方向的集中登记 |
| 编辑、图表与出版规范 | [editorial-guidelines.md](editorial-guidelines.md) | 继承主宪法，落实本轮修订 |
| 四项大洞察与十二项子洞察 | [claims-map.md](claims-map.md) | 四大方向已确认；子项为研究组织方案，逐项检验 |
| 六章取舍与篇幅 | [chapter-plan.md](chapter-plan.md) | 重点已确认；页数为可调整预算 |
| 十大趋势判断与前瞻 | [outlook-method.md](outlook-method.md) | 时间分层已采纳；具体十条尚未定稿 |
| 十大战略建议 | [recommendations-method.md](recommendations-method.md) | 结构已采纳；具体十条尚未定稿 |
| 材料、证据与缺口 | [材料清单](evidence/README.md) · [证据台账](evidence/ledger.json) · [待核查项](evidence/open-items.md) | 继承原核验状态，不因归档自动升级 |
| 本轮决策与版本 | [评审记录](reviews/2026-11-09-baseline.md) · [版本指针](current.json) | 管理 v1.0 与内容 v0.3 分开编号 |
| 前置内容可编辑源码 | [frontmatter/v0.3](frontmatter/v0.3/README.md) | 原 9 页快照；PDF 在仓库外保存 |
| 第一章精要稿 | [chapters/01/v0.2](chapters/01/v0.2/README.md) | 8 页，新增 DeepSeek 与全球接续；待作者 PDF 评审 |

## 当前边界

已确认约 100 页的精要版定位、前置内容形式、四项特色与四大洞察方向，以及第六章“12 项洞察—10 项前瞻—10 项建议”的总结结构。新结论仍由中间章节证据形成，并反向优化执行摘要。

前置稿 v0.3 获得继续推进的肯定，其第六章目录形成于新总结结构之前；该快照保留原样，下一轮合稿同步更新目录与页码。不能把归档快照视为最新整书目录，也不能将方向认可视为逐项数据认证。

本目录补充而不覆盖[报告宪法](../../docs/report-constitution.md)、[全书主张地图](../../docs/claims-map.md)与[视觉基线](../../brand/osdgs/README.md)。精要版的范围性更新在本目录评审记录登记；完整版、原网站和品牌母型沿用各自的版本管理。

## 下一轮写作

按第一小节打样、评审后推广的路径推进；第一章研究与评审在单独的“第一章撰写与评审”聊天开展。每完成一个图文单元，同时更新其主张、证据、时间口径、反证与附录条目；第六章只汇总已经建立证据的判断。

2026-11-09 本轮用户已明确同意按既定布局制作完整第一章 PDF 评审稿，并确认以 2026 版为准、突出 AI 对开源及开源对 AI 的双向影响。第一章 v0.1 据此完成；这是整章评审范围的授权，不是对新正文、图表或新增判断的批准。修改、证据与核查项见[第一章评审记录](chapters/01/v0.1/review/evidence.md)。

仓库保存 Markdown、JSON、LaTeX、绘图与构建源码。PDF、字体、原始第三方报告、私有附件和本地构建输出不入库。提交前在仓库根目录运行：

~~~bash
python editions/insights/scripts/check_sources.py
python brand/osdgs/v2.0/source/verify_assets.py
git diff --check
~~~

本次归档不等于对外正式发布，不自动更新 Web。

第一章 v0.2 按用户认可方案补充 DeepSeek，保留 [v0.1 历史快照](chapters/01/v0.1/README.md)。新增数据和后续章节安排见 [v0.2 证据记录](chapters/01/v0.2/review/evidence.md)。
