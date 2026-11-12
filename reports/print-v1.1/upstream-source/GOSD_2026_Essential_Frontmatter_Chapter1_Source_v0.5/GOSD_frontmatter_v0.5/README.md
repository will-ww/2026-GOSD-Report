# GOSD 2026 精要版 · 封面与前置内容 v0.5

本包为 PDF 评审用的可复现源稿，未提交 GitHub。交付范围为封面至第一章，共 23 页。

## 本轮结构

- 第 1 页：在原星座、地球与光带封面上加入精要版标识及三家原始透明 logo。
- 第 3—6 页：奇点智能研究院定位、五大范式、六大研究方向、研究与实践。四幅图保留为可编辑 SVG。
- 其他 18 页：从 v0.4 原样继承；目录页内链接和书签保持可用。

## 构建

使用 Python 3、PyMuPDF、Pillow、fontTools、Inkscape、XeLaTeX、Noto Sans/Serif CJK 字体。执行 `python3 run.py`，生成 `output/GOSD_2026_Essential_Frontmatter_Chapter1_Review_v0.5.pdf`。

`run.py` 定义四幅图与四页文字；`build.py` 提供 SVG 和 LaTeX 工具；`layout.sty` 保留中文排版与动态星座视觉基线。`assets/baseline-v0.4.pdf` 用于合并未改动页面。

图中原始 SVG 文字可编辑，导出为 PDF 时以矢量轮廓保真；正文保留可检索文本并嵌入中文字体。字体与编译缓存由本地环境生成，不打包。

## 证据与评审

机构原稿在 `data/institute-original.txt`，来源与使用边界在 `data/sources.json`；本轮修改、待核查项和评审重点在 `review/editorial-review.md`。宪法、主张地图、材料清单保留读取快照，未将待检验主张当作已证明结论。

四页的新分组与关系属于本轮结构化编辑；尤其五大范式与官网三大范式的表述差异，仍需在正式发布前由机构确认。
