# 2026 全球开源发展报告 · 第二章整章评审源

**v1.0.0 · 2026-11-05 · 待作者评审**

完整书稿为 `chapter2.tex`，可读结构化全文为 `chapter2.md`。七节的编辑主数据为 `sections/21.json` 至 `sections/27.json`；章首、阅读说明、章末与方法由 `scripts/build_chapter.py` 生成，完整Markdown由 `scripts/sync_markdown.py`同步输出。

## 编译

环境：Python 3、XeLaTeX（ctex、xeCJK、fontspec）、Fontconfig、Noto Sans/Serif CJK SC，以及Pandoc。Python依赖见 `requirements.txt`。

```sh
python3 -m pip install -r requirements.txt
make pdf
make qa
```

已有矢量PDF对应本轮审阅SVG，因此默认编译无需重新绘图。修改SVG后运行 `make figures`；修改本轮重绘三图的底表后运行 `make revised-figures`，再运行 `make pdf`。这些命令不会访问或写入GitHub。

`configure_fonts.py` 从本机已安装字体提取简体中文字形到本地临时缓存 `.build_fonts/`。**交付包不含字体文件；不得把该缓存加入仓库或再分发。** PDF嵌入的是文档所需字体子集。

## 内容与复现边界

- `figures/`：49组正式编号图对应的SVG和矢量PDF，另含少量历史未用图件；是否进入正文以图件索引为准。
- `data/`：原始和派生底表；源文件指纹见核查记录。
- `baseline/`：各节最新输入和历史绘图代码，仅作溯源；历史生成脚本保留原目录假设，不是本整章默认构建入口。
- `scripts/draw_chapter_revision.py`：从CSV重绘本轮三组改动图。
- `scripts/export_vector_assets.py`：从全部已使用SVG再导出矢量PDF。
- `review/`：版本依据、整章策略、未解决核查、输入与输出指纹、图表—来源—正文索引。
- `methods/`、`references/`：完整方法说明与49条参考资料。

本包可复编排版，并可从保留SVG复现图形输出；它**不等于**重新执行上游全域账号去重、OpenRank算法及历史归属映射。历史图的原生成程序一并保留，但本轮没有重新运行所有上游研究流水线。

本轮不修改2.1—2.7既有独立包；不把整章稿提前记为获批基线；不将整章PDF上传仓库。私有原件和第三方原始PDF未放入本包。来源许可和地图说明沿用各节 `THIRD_PARTY_NOTICES.md`。
