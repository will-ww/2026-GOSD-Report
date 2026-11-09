# 前置内容 v0.4：宣言视觉强化评审稿

2026-11-09 · 10 页 · 待作者 PDF 评审。基于 [v0.3](../v0.3/README.md) 增量修改，保留历史快照。

封面与编委会沿用既定方案；目录落实第六章 6.1—6.4，并给出本次评审包的第一章页码。两页摘要补充平台解释，将 Actions、PR、Spaces 图例改为中文通俗名称。引言保留三页 2026 宣言全文，导语改为报告自身的研究立场，去除未经核实的“首份”及外部背书表述；增加一页“三层七原则”结构图和七个专用线性图标。

图引 1 依据 2026 宣言，附件中的 2025 图只提供结构参照，不复用其旧原则文字。新图沿用 2026 色彩与字体，独立于 OSDGs 品牌标识；没有更改十节点母型。

## 构建与图件

提供仓库外 2026 母稿路径至环境变量 GOSD_2026_SOURCE_PDF，然后运行 `bash build.sh`。依赖 XeLaTeX、Noto CJK、fontTools、PyMuPDF、Inkscape。`content/` 保存完整宣言；`build_declaration.py` 与 `figures/` 保存图形和图标源码；`prepare_assets.py` 校验母稿 SHA 并提取封面。源文件指纹见[版本登记](../../releases/frontmatter-v0.4.json)。

与第一章 v0.3 构建完成后，运行 `python ../../scripts/build_visual_review_pack.py --output /absolute/path/review.pdf`，生成连续页码的 20 页评审包和四张可复用 SVG。PDF 与字体均不入库。

## 评审与边界

重点评审宣言图是否清晰连接共同愿景、三层原则和行动；概要与正文的术语是否足够易读。宣言全文中的发布主体、机构名称和制度措辞仍继承 O08 待核查状态。图文通过设计检查不等于正式发布或事实认证。详见[本轮评审记录](../../reviews/2026-11-09-visual-strengthening.md)。
