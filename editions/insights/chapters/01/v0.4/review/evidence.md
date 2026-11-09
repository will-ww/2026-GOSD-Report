# 第一章 v0.2：DeepSeek 补充与证据记录

日期：2026-11-09。状态：补充方案获认可，新稿待作者 PDF 评审。来源读取日：2026-11-09。

用户要求在“中国模型与全球社区”中补充 DeepSeek，并认可 Qwen 与 DeepSeek 并列、NVIDIA 跨境复用及基础设施延伸的方案。母版为 c6df912d5345fe56eaa05fb5131e87c3a8adfc26 中的第一章 v0.1；本次只重构第 3 页，保留 8 页篇幅。其余章节口径继承 [v0.1 证据记录](../../v0.1/review/evidence.md)。

## 图 1-2 的新增证据

| 编号 | 事实与定位 | 判断性质及边界 |
| --- | --- | --- |
| C1-E02a | HF Summer 2026：Qwen 151,448 个衍生仓库；28,531 个 GGUF 转换中官方 54 个 | 沿用 v0.1；约 99.8% 为计算值，不等于原创模型数或生产采用 |
| C1-E02b | ATOM v1 §5.1、图 12：DeepSeek 在追踪的总参数 250B+ 模型累计下载中占 47% | 研究方报告值；特定开放权重生成语言模型样本，不是全部 AI 或全球市场份额 |
| C1-E02c | ATOM v1 §2.1、§5.1、图 9：论文标注“2026 年 1 月”观察点中，DeepSeek 的 OpenRouter token 份额 31.1% | 每月仅前十开放模型，非 OpenRouter 全平台；沿用原文月份标签，不擅自改为截至 1 月 31 日 |
| C1-E02d | NVIDIA 2025-05-14，表 2：1,212,994 条 DeepSeek-R1 生成样本；正文列出用于训练 Llama-Nemotron 系列 | 复用方一手披露；图示约 121.3 万条。不是独立问题数、权重继承或性能提升归因；属历史背景 |
| C1-E02e | DeepSeek open-infra-index 的 202502 Open-Source Week：FlashMLA、DeepEP、DeepGEMM、DualPipe、3FS 等 | 支持开放涉及内核、通信、并行和存储；不宣称整个训练系统已开放，也不把公告五天当成实际仓库总数 |

## 原始来源

- [HF Summer 2026](https://huggingface.co/blog/state-of-open-models-summer-2026)，2026-08-14；既有转录。
- [The ATOM Report v1](https://arxiv.org/html/2604.07190v1)，Nathan Lambert、Florian Brand，2026-04-08；本轮阅读全文相关章节，采用图 9、12 和方法，未复算底层数据。
- [NVIDIA：Build Custom Reasoning Models with Advanced, Open Post-Training Datasets](https://developer.nvidia.com/blog/build-custom-reasoning-models-with-advanced-open-post-training-datasets/)，2025-05-14，表 2 及正文训练模型说明。
- [DeepSeek Open Infra](https://github.com/deepseek-ai/open-infra-index)，2025 年 2 月开源周历史记录。

ATOM 倡议的美国开放模型竞争力立场与其测量论文分开处理。其 HF 数据与其他 HF 转述不计为独立复测；OpenRouter 提供不同观测面。未使用 ATOM 待解释的总体下载数字，也未采用历史峰值 75.6% 作醒目数字。

## 主张与章节回链

- I03：NVIDIA 案例支持开放成果可通过模型输出与数据继续流动；维护和持续能力仍需其他证据。
- I04：Qwen 与 DeepSeek 展示不同维度的生态位置；不作同指标排名，也不推出全领域领先。
- I05：开放基础设施的存在支持分层观察的必要性；使用成效、成本和成熟度尚待第四章检验。
- 执行摘要前置稿 v0.3 为不可覆盖历史快照。本次在证据台账中登记补充，下一轮摘要合稿时联动，不提前更改其已归档文件。
- 第四章承接基础设施，第五章承接模型与事件线；第六章仍只提炼证据充分的发现，不新增既定结论。

## 待核查项

1. ATOM 模型列表、底层月度数据与 47% 分母快照尚未逐行复算；31.1% 保留报告的月份标签及前十样本边界，不扩展为主期全年份额。
2. NVIDIA 样本归因来自发布者表 2，未重新运行生成流程；不推断性能贡献率、产业收益或全球南方效果。
3. HF 存量快照日及全部跨平台映射、实际公共成效，继承 v0.1 核查项。
4. 具体模型和基础设施的许可、开放层级需逐版本处理；本页不作完整开源定义认证。

## 评审问题

第 3 页是否有效补充 DeepSeek，且保留 Qwen 的社区贡献；“输出—数据—后续模型”的具体接续是否有解释力；一页中的数字、正文与注释是否平衡。
