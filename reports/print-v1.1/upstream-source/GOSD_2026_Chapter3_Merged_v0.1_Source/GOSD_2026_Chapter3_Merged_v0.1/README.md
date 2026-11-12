# GOSD 2026 精要版 · 第三章合稿 v0.1

2026-11-10。本包为第三章六个小节的合稿源文件，供评审、复用与后续修订。新增章节串联与行动启示尚待评审，不替代已批准宪法。

交付结构为 22 页正文、4 页统一附录，共 20 幅组合图。保留最新六节图件，统一连续图号、页码、章节书签、图题与叙事；正文清除零散外链及过程性文字，必要方法与证据汇入附录 A。PDF 独立交付，不进入 GitHub。

## 重新生成

在本目录执行 `python3 render.py`。依赖 Python 3、PyMuPDF、Pillow、fontTools、NumPy、XeLaTeX、Inkscape、Poppler，以及系统 Noto CJK Sans / Serif Regular / Bold 字体。字体默认路径见 `build.py`；其他平台请按实际安装位置调整。首次构建会从 SVG 生成矢量图 PDF，并将中文字体嵌入最终 PDF。

正文结构与四页附录见 `chapter_pages.py`，20 个图文单元见 `data/content.json`。`figures/` 是获批小节最新图件的矢量快照，不依赖外部图片链接；数据、图表原始脚本与核验材料保存在 `upstream/`。部分上游脚本仅作为溯源资料，并非本次合稿的构建入口。合稿图件重用现有结果，不重新计算或替换排行榜数字。

`data/figure-index.json` 记录原稿页码、原文件哈希和图件哈希；`data/sources-full.json` 保存完整来源。`provenance/` 保留本次对齐使用的宪法、主张地图、规范与第六章对应关系。`review/release-checks.json` 保存本次导出核验。

## 核验

`verify.py` 将最终 PDF 与 `../merge3-reference/` 中六份最新小节 PDF 逐图比较，因此只有恢复对应原稿后才可运行完整图件一致性核验。原稿文件名与 SHA-256 见 `data/figure-index.json`。正文共 20 幅图的文本及像素一致性已验证，所有字体嵌入，全部页面竖版；26 页均已逐页检查。

## 统计与引用

主统计期为 2025-07-01 至 2026-06-30。历史序列沿用原标签并注明窗口核查状态，ModelRank 为 2026 年 6 月快照，期后机构与模型观察单独标注。不同对象、来源、窗口与分母不合并为同一指标。详细待核项见 `review/merge-review.md` 与最终 PDF 附录 A。

权威仓库为 https://github.com/will-ww/2026-GOSD-Report ，用户确认基线为 fff392e957bab9fb6d89d49dea712af47484efaa；本次同时读取了现行精要版规范及评审记录。本包不包含账号、数据库密码或认证配置。
