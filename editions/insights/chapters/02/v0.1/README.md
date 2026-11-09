# 第二章 2.1 样节 v0.1

2026-11-09，**待作者 PDF 评审**。正文两页，另附一页摘要与第六章联动建议。不是第二章全章稿，也不是正式发布稿。

按[选择性撰写计划](../plan.md)制作全球参与样节：全球活跃地图与前十国家、五个固定比较组的规模和累计增幅。以 2026 母稿为主体，复用批准视觉体系；不重画近似品牌标识。地图保留归档 Equal Earth 投影几何及面积标度，不独立更改边界。

## 内容入口

- [content.json](content.json)：正文和联动建议的单一文字源。
- [chapter2.tex](chapter2.tex)、[layout.sty](layout.sty)：生成的可编辑 XeLaTeX 稿。
- [build.py](build.py)：精确数据、SVG 图件与 PDF 构建。
- [data](data/)：从归档逐字节继承的 CSV 与重算比较表。
- [figures](figures/)：三张可编辑 SVG，合成两个正文图号。
- [证据、核查与评审](review/evidence.md)、[来源记录](review/sources.json)、[图形检查](review/chart-validation.json)。

## 复建

在装有 XeLaTeX、Inkscape、Noto CJK 字体、Python fontTools／Pillow／PyMuPDF 的环境运行：

```bash
python3 editions/insights/chapters/02/v0.1/build.py
```

脚本从仓库内归档读取 CSV 与世界图几何，从批准品牌目录读取 Compact 标识；字体由系统 TTC 的简体中文实例提取，PDF 嵌入字体。输出和字体仅写入被忽略的本地目录，不进入 GitHub。无需外部母稿 PDF 即可复建本样节。

## 本轮边界

“全球地图”和“五域表”并非同一汇总覆盖，数值不得互换。增长由五域表自身的 2022、2026 原值重算。图 2-1 的万人显示继承来源两位小数截断约定，图 2-2 四舍五入；排序与计算均使用原值。源数据小数精度保留，不声称重新逐人核验。

联动建议仅为 I01 提供部分参与证据，为 I07 补充背景；完整洞察状态仍待后续章节检验。两页正文及一页建议均需作者评审，未覆盖现有前置和第六章快照。
