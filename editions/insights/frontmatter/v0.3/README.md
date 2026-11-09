# 前置内容 v0.3 可编辑快照

2026-11-09 · 9 页。特色与洞察方向得到用户肯定，继续随全文证据迭代；具体事实、机构措辞和许可仍按[待核查项](../../evidence/open-items.md)逐项管理。

顺序：封面 1 页、编委会 1 页、目录 2 页、执行摘要 2 页、引言 3 页。编委会沿用 2025 版；引言是 2025 版体例与 2026 版全文。封面恢复 173 页 2026 母稿原样，仅更正两处报告字标为 GOSD。

本快照保留原正文和旧 6.1—6.5 目录。之后获认可的新第六章结构见[章节计划](../../chapter-plan.md)，下一版本落实，不能误将此快照作为最新整书目录。

## 文件

- frontmatter.tex：封面、编委会、目录；revised-content.tex：两页摘要和引言页面。
- content/：2026 宣言正文；sources/declaration-2026-verbatim.txt：核对文本。
- build_figures.py 与 figures/：摘要图形和文字；sources/chart-data.json：官方数据、口径；sources/summary-content.json：四项特色与洞察结构化文本。
- prepare_assets.py：从外部母稿提取封面并局部更正，从根目录批准 SVG 生成页眉 PDF。
- build.sh：本地资产准备与双遍 XeLaTeX 编译。

原稿和前置 PDF 指纹见[版本登记](../../releases/frontmatter-v0.3.json)。文件级校验固定来源身份，不意味着母稿所有统计已获认证。正式来源清单集中在[evidence/](../../evidence/README.md)，不再复制历史宪法文件。

## 本地构建

需要 Python 3、PyMuPDF（支持 Page.apply_redactions 的 graphics 参数）、Inkscape、XeLaTeX、TikZ、fontspec，以及 Noto CJK 与 Liberation 系统字体。归档环境为 Linux；字体路径在 layout.sty 中显式指定，可按本机安装位置调整，但应重新检查字形与版式。字体不得随仓库提交。

提供仓库外的 173 页母稿，SHA-256 必须是 675c3490c45d5fc4b51ca0c9ae2ddd5bb330abc108f148435d7317c221579a66。脚本仅接受登记版本，防止错误母稿被静默替换。

在本目录运行：

~~~bash
export GOSD_2026_SOURCE_PDF='/absolute/path/to/external-mother-report.pdf'
bash build.sh
~~~

封面替换字体默认使用系统 Liberation Serif Bold，可通过 GOSD_COVER_FONT 指定路径。页眉直接引用根目录 brand/osdgs/v2.0/assets/master/osdgs-symbol-compact.svg；与原快照 SVG 核对后仅有末尾换行差异，无品牌改动。

本地生成的两份资产 PDF 在 .build/assets/；评审稿在 output/。这些目录和所有 PDF、字体均被忽略并由提交检查再次拦截。没有外部母稿时构建会明确停止，仓库不嵌入原 PDF、字体或编码后的替代物。

本次源码归档只调整资产路径和准备步骤；保留历史文字与图表。PDF 元数据可能随构建变化，不承诺逐字节一致；复建需检查九页文字、渲染、链接与字体。核验记录见[归档构建检查](../../reviews/2026-11-09-source-validation.json)。
