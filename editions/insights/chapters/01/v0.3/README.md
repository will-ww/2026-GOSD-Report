# 第一章 v0.3：视觉强化与自洽阅读

2026-11-09 · 10 页 · **待作者 PDF 评审**。基于 [v0.2](../v0.2/README.md) 增量修订，主统计期与三节结构不变。

本轮新增 SDGs 与数字公共品基础页、OSDI 专页，重绘 OSDGs 正文页；保留 Qwen、DeepSeek 及全球接续证据。必要术语随文解释：智能体、PR、HF、推理、词元、衍生仓库、GGUF、后训练、全球南方、SDGs、DPG、DPGA、OSDGs、OSDI 和 OpenRank。

| 图号 | 内容 | 合并评审包页码 |
| --- | --- | ---: |
| 1-3 | SDGs 17 项目标、DPG 九项要求及实施结果的区别 | 14 |
| 1-4 | 获批动态星座主标识、四个支柱与十个维度 | 15 |
| 1-6 | OSDI 四目标、十方向、29 项候选指标、三种用途 | 17 |

`build_visuals.py` 生成准确的 TikZ 图文；既有数据图仍由 `build_figures.py` 生成。`figures/exports/` 的 SVG 从相同矢量页面导出，供后续网页与整书复用；源与输出一并更新，不另造图中数据。OSDGs 母型、十维顺序、色值和标识不变；OSDI 专页是研究体系的编辑视觉，不登记为新商标。

## 构建

提供环境变量 GOSD_2026_SOURCE_PDF 指向仓库外母稿，再运行 `bash build.sh`。需要 XeLaTeX、TikZ、Noto CJK SC、Liberation、Python 3、PyMuPDF、fontTools、Inkscape；合稿另需 Poppler。母稿 SHA 与本地资产规则继承旧稿。PDF、字体、.build、output、qa 不入 GitHub。

## 证据与评审

新增官方背景来源为联合国 SDGs 与 DPGA 标准；框架和候选指标沿用 2026 获批基线。九项要求不证明本地实施效果；29 项候选指标不代表全部实测。详见[本轮证据](review/visual-evidence.md)、[原有案例证据](review/evidence.md)和[统一评审记录](../../../reviews/2026-11-09-visual-strengthening.md)。

评审重点：读者能否区分国际发展目标、本报告的原创目标框架与指标工具；三张图的信息密度是否适合非技术决策者；两页新增解释是否值得保留。
