GOSD 2026 精要版 · 第二章 2.1 · v0.3 · 待评审
2026-11-09。三页 A4 竖版图文 + 两页附录1。此版本未提交 GitHub。

使用：安装 Python 3、Pillow、fonttools、PyMuPDF；系统需有 Inkscape、XeLaTeX、Noto Sans/Serif CJK 和 Liberation Sans。运行 python build.py，PDF 输出到 output/。运行 python validate.py 进行口径、算术、版式边界与字体检查。
可编辑内容：content.json、content.py；图形生成：build.py；图件：figures/*.svg；数值与来源：data/ 与 review/。
资产：沿用报告批准的 OSDGs v2.0 标志、世界地图与中国地图几何。未修改行政区划要素。
口径：中国五域 2026 年为 454.534 万；GitHub 单国为 250.482488 万；国内平台经去重补充约120万，跨平台约370万。三者不混排、不重复加总。
2030 为两种预设条件情景，无概率、置信区间或AI因果估计。全球南方六国是固定比较组，不代表全球南方全部。
原始国家/省级数据来自 OpenShare GOSD 年度公共接口，2026-11-09 读取，详见 review/validation.json。PDF 与字体未放入此源码包。
待核查与待评审见 PDF 附录和 review/validation.json。
