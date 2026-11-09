# 前置内容 v0.5：紧凑宣言信息图

2026-11-09 · 9 页 · **待作者 PDF 评审**。基于 [v0.4](../v0.4/README.md)，保留旧版本。

完整 2026 宣言保持原文；原则标题与短句并行排版，将第六原则移至上一页，为引言末页的总览图腾出空间。总览采用共同愿景连接三组原则，再落到行动共识的横向关系结构，高约 9 厘米，不再独占一页。新图、摘要特色块与页眉导视使用同一轻量光带语言，保留白底正文和原有字体体系。

用户提供的附件仅作为视觉参考，不替换已批准的四支柱十维名称，不改变 OSDGs 品牌母型。封面、编委会和摘要事实沿用已有基线，目录已联动本次 17 页评审包。

## 构建

设置仓库外母稿路径 `GOSD_2026_SOURCE_PDF` 后运行 `bash build.sh`。前置与第一章均构建完成后，在仓库根目录运行 `python editions/insights/scripts/build_compact_review_pack.py --output /absolute/path/review.pdf`。源图使用 TikZ 与专用 SVG 图标，公共图形函数位于 `scripts/infographic_primitives_v1.py`；导出 SVG 与 PDF 使用同一绘制结果。PDF、字体及第三方原件不入库。

源文件指纹见[版本登记](../../releases/frontmatter-v0.5.json)，修改与边界见[评审记录](../../reviews/2026-11-09-compact-infographics.md)。宣言发布主体与机构表述继承 O08 待核查状态，不能以设计评审替代发布核定。
