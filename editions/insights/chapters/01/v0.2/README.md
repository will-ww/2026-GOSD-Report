# 精要版第一章 v0.2：从开放协作到公共价值

2026-11-09 · 8 页 · **待作者 PDF 评审**。

本稿在 [v0.1](../v0.1/README.md) 基础上，仅重构第 3 页及相关证据记录。用户认可增加 DeepSeek 并要求更新一版；其余七页保持原稿，既有获批研究框架和主统计期不变。该授权不等于新稿自动通过评审。

## 本轮修改

- Qwen：保留 151,448 个社区衍生仓库及 GGUF 转换的社区贡献。
- DeepSeek：新增 ATOM 论文所列 250B+ 模型累计下载份额 47%、OpenRouter 前十开放模型样本词元份额 31.1%，分别标注范围。
- 全球接续：用 NVIDIA 已披露的 1,212,994 条 R1 生成样本说明模型输出、开放数据和后续模型之间的联系。
- 基础设施：简述计算内核、通信、并行训练和存储的开放，详细材料归入第四章研究；五节点事件线为第五章保留在研究记录中，不额外增加第一章页数。

来源和核查项见 [证据记录](review/evidence.md)，后续章节可复用的 [事件线](review/deepseek-timeline.md) 已注明历史/主期属性。完整统计数据在 sources/chart-data.json；版式核验在 review/validation.json。

## 构建

~~~bash
export GOSD_2026_SOURCE_PDF='/absolute/path/to/external-2026-mother-report.pdf'
bash build.sh
~~~

中文友好 XeLaTeX、TikZ、Noto CJK SC、Liberation、Python 3、PyMuPDF、fontTools、Inkscape。母稿 SHA-256 及本地资产生成规则继承 v0.1；字体、PDF、.build、output、qa 均不入 GitHub。

## 评审重点

第 3 页的 Qwen/DeepSeek 互补观察是否平衡；数据接续图是否让全球协作具体可见；新增信息与来源注释的密度是否合适。
