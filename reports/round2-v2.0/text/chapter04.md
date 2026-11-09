# chapter04 | 第二轮 v2.0 文字层存档

本文件直接提取自已交付的 173 页评审 PDF，保留页序和文字层，不替代排版源码、图形或数据底表。页面中的断行和阅读顺序可能来自 PDF 编码。

## PDF 第 116 页

OSDGs
GOSD / 2026
OSDGs
第四章 / CHAPTER 04
全球开源技术
全景洞察
GLOBAL OPEN SOURCE LANDSCAPE
从功能分⼯出发，理解技术⽣态的组织与演进。
2026 GLOBAL OPEN SOURCE DEVELOPMENT REPORT
04

## PDF 第 117 页

OSDGs
/
GOSD 2026
全球开源发展报告
第四章全球开源技术全景洞察
04 / GLOBAL OPEN SOURCE LANDSCAPE
从功能分工进入技术生态
先看完整全景，再追问资源如何被组织和复用。
技术生态由不同能力共同支撑：任务入口连接工具与模型，模型运行依托数据、计算和工程
系统，开放规范使多种实现能够继续协作。本章以六个观察入口呈现这些分工，在完整名单中定
位具体对象，再选择有证据支持的问题深入分析。
4.1
Agentic AI
任务⼊⼝、构建编排与模型基础
4.2
AI ⼤模型
模型任务、发布账⼾与获取信号
4.3
云基础设施
应⽤交付、服务运⾏与资源⽀撑
4.4
数据库系统
数据模型、查询⽅式与专⽤语义
4.5
RISC-V
软件、⼯具、实现与共同规范
4.6
PyTorch ⽣态
模型与任务、训练执⾏、⼯程协作
4.1、4.2分别从项目协作和模型获取信号进入分析；4.3—4.6保留完整技术全景。全景的分区
与位置用于功能导航，不表示真实依赖、成熟程度或市场规模。每个条目链接到对应仓库或模型
页面。
D03
代码产出
D04
模型开放供给
D06
代码影响力
D07
模型影响力
与本章直接相关的四个发展维度，用于提出问题；不将项目收录数量转换为目标达成评分。
主统计期：2025‑07‑01至2026‑06‑30。4.1采用期后固定名单回看主期；4.2的2026‑10‑02模型快照及HF夏季观察分别标注。其他全
景沿用固定对象与分类，具体时点、待核状态随图说明。项目Logo与账户头像用于辨识对象，不构成托管、许可或认证证明。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
117

## PDF 第 118 页

OSDGs / GOSD 2026
第四章 · 全球开源技术全景洞察
4.1 Agent 应⽤与基础设施
86 个项⽬ · 12 个类别 · 固定观察名单
由任务⼊⼝进⼊编排、⼯具和运⾏条件。相邻位置表达功能分⼯。
任务⼊⼝
构建与编排
运⾏⽀撑
编码代理
16
OpenCode
anomalyco
Codex
openai
Claude Code
anthropics
Qwen Code
QwenLM
Pi
earendil-works
cline
cline
Kilo Code
Kilo-Org
Goose
aaif-goose
kimi-code
MoonshotAI
Gemini CLI
google-gemini
DeepSeek-Reasonix
esengine
OpenHands
OpenHands
Copilot CLI
github
标识
待核
MiniMax Code
MiniMax-AI
DeepSeek Harness
deepseek-ai
标识
待核
ZCode
zai-org
编码⼯作流与⼯具链
7
T3 Code
pingdotgg
cc-switch
farion1231
Oh My OpenAgent
code-yeongyu
Everything Claude Code
affaan-m
herdr
herdrdev
superpowers
obra
spec-kit
github
个⼈助⼿
7
OpenClaw
openclaw
Hermes Agent
NousResearch
QwenPaw
agentscope-ai
LobeHub
lobehub
AstrBot
AstrBotDevs
ZeroClaw
zeroclaw-labs
nanobot
HKUDS
聊天⼯作区
3
Cherry Studio
CherryHQ
Open WebUI
open-webui
LibreChat
danny-avila
多代理编排
5
deer-flow
bytedance
Mastra
mastra-ai
Paperclip
paperclipai
multica
multica-ai
orca
stablyai
⼯作流与代理构建
5
n8n
n8n-io
Dify
langgenius
activepieces
activepieces
Langflow
langflow-ai
Flowise
FlowiseAI
代码优先框架
11
Vercel AI SDK
vercel
agno
agno-agi
CopilotKit
CopilotKit
LangChain
langchain-ai
Microsoft Agent Framework
microsoft
Pydantic AI
pydantic
LiveKit Agents
livekit
Koog
JetBrains
Google ADK
google
Pipecat
pipecat-ai
crewAI
crewAIInc
记忆、知识与上下⽂
9
OpenViking
volcengine
RAGFlow
infiniflow
Milvus
milvus-io
hindsight
vectorize-io
Cognee
topoteretes
mem0
mem0ai
seekdb
oceanbase
headroom
headroomlabs-ai
supermemory
supermemoryai
协议与互操作
8
A2UI
a2ui-project
MCP Context Forge
IBM
AgentGateway
agentgateway
ToolHive
stacklok
A2A
a2aproject
Agent Skills
anthropics
MCP
modelcontextprotocol
AG-UI
ag-ui-protocol
⼯具与计算机使⽤
6
Lark CLI
larksuite
Browser Use
browser-use
Agent Browser
vercel-labs
firecrawl
firecrawl
CUA
trycua
page-agent
alibaba
开发沙箱
5
coder
coder
Warp
warpdotdev
daytona
daytonaio
agent-sandbox
kubernetes-sigs
OpenSandbox
opensandbox-group
可观测与评估
4
Langfuse
langfuse
Opik
comet-ml
Arize Phoenix
Arize-ai
promptfoo
promptfoo
图4-1 Agent 应⽤与基础设施 · 完整观察名单
来源：Agentic AI Landscape 固定版本 e330d75；沿⽤ 145 项主归类中的 Agent Infra。
期后固定名单，不等于主期末名录；统计图另取 2025-07 ⾄ 2026-06。头像⽤于识别账⼾。
区域按功能组织，⾯积不编码规模；点击条⽬可到来源链接。分类与收录不构成依赖、许可或成效认证。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
118

## PDF 第 119 页

OSDGs / GOSD 2026
第四章 · 全球开源技术全景洞察
4.1 模型基础设施
59 个项⽬ · 13 个类别 · 固定观察名单
由模型服务进⼊训练、数据和计算⽀撑，与前页任务⼊⼝相接。
模型服务
后训练
训练与加速
数据基础
算力与调度
模型 API ⽹关
4
LiteLLM
BerriAI
OmniRoute
diegosouzapw
New API
QuantumNous
higress
higress-group
服务部署
3
NVIDIA Dynamo
ai-dynamo
ollama
ollama
llm-d
llm-d
推理引擎
8
SGLang
sgl-project
vLLM
vllm-project
TensorRT-LLM
NVIDIA
llama.cpp
ggml-org
vLLM Omni
vllm-project
ONNX Runtime
microsoft
OpenVINO
openvinotoolkit
LMCache
LMCache
强化学习与环境
6
NeMo RL
NVIDIA-NeMo
verl
verl-project
RLinf
RLinf
TRL
huggingface
OpenEnv
huggingface
AReaL
areal-project
监督微调
3
Unsloth
unslothai
ms-swift
modelscope
LLaMA Factory
hiyouga
训练框架与并⾏
6
PyTorch
pytorch
JAX
jax-ml
Megatron-LM
NVIDIA
PaddlePaddle
PaddlePaddle
DeepSpeed
deepspeedai
tensorflow
tensorflow
训练评估与观测
2
Weights & Biases
wandb
MLflow
mlflow
机器⼈基础设施
2
LeRobot
huggingface
OpenMind OM1
OpenMind
编译器与加速
8
flashinfer
flashinfer-ai
triton
triton-lang
NVIDIA Model Optimizer
NVIDIA
Transformer Engine
NVIDIA
OpenXLA
openxla
CUTLASS
NVIDIA
FlashAttention
Dao-AILab
DeepEP
deepseek-ai
数据标注
2
CVAT
cvat-ai
Label Studio
HumanSignal
数据集成
4
Apache Airflow
apache
docling
docling-project
airbyte
airbytehq
markitdown
microsoft
数据治理
7
OpenMetadata
open-metadata
DataHub
datahub-project
Apache Iceberg
apache
Delta Lake
delta-io
Apache Hudi
apache
Apache Paimon
apache
Apache Gravitino
apache
计算与调度
4
ray
ray-project
Apache Spark
apache
kserve
kserve
volcano
volcano-sh
图4-2 模型基础设施 · 完整观察名单
来源：Agentic AI Landscape 固定版本 e330d75；沿⽤ 145 项主归类中的 Model Infra。
与前页合为同⼀观察框，项⽬位置不表⽰已验证依赖；账⼾头像不等同项⽬专属 Logo。
区域按功能组织，⾯积不编码规模；点击条⽬可到来源链接。分类与收录不构成依赖、许可或成效认证。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
119

## PDF 第 120 页

OSDGs
/
GOSD 2026
全球开源发展报告
4.1 Agentic AI 全景洞察
任务入口与模型执行同时居前
两张全景共保留145个项目、25个类别。Agent Infra连接任务入口、构建编排与运行支撑；
Model Infra提供模型服务、训练、数据与算力基础。由Codex、OpenClaw等入口继续向下，可
以找到Dify、LangChain、vLLM与PyTorch所处的不同功能位置。
2026年6月，个人助手、编码代理和推理引擎的OpenRank分别为1,373.73、1,328.86和
1,127.31，合占当月已观测样本的42.3%。前两类面向任务组织，后一类提供模型执行能力，重点
区域同时分布在两张全景中。
01
个人助手
1,373.73
7/7项
02
编码代理
1,328.86
14/16项
03
推理引擎
1,127.31
8/8项
04
训练框架与并行
671.48
6/6项
05
服务部署
416.59
3/3项
06
代码优先框架
405.24
11/11项
07
多代理编排
398.36
5/5项
08
记忆、知识与上下文
377.44
9/9项
09
编译器与加速
329.63
8/8项
10
工作流与代理构建
317.42
5/5项
11
数据治理
271.85
7/7项
12
数据集成
250.00
4/4项
13
计算与调度
219.46
4/4项
14
开发沙箱
214.17
5/5项
15
工具与计算机使用
204.73
5/6项
16
编码工作流与工具链
203.42
7/7项
17
模型 API 网关
193.26
4/4项
18
协议与互操作
152.53
8/8项
19
强化学习与环境
148.03
6/6项
20
聊天工作区
131.73
3/3项
21
可观测与评估
122.39
4/4项
22
训练评估与观测
88.11
2/2项
23
监督微调
62.69
3/3项
24
机器人基础设施
30.48
2/2项
25
数据标注
11.47
1/2项
个人助手、编码代理与推理引擎居前
排名 / 类别
OpenRank / 有值项目数
OpenRank / 有值项目数
图4‑3　全部25类的期末影响力与观测覆盖
来源：OpenDigger冻结响应；OpenDigger全域OpenRank方法。2026‑06，141/145项有值，合计9,050.38。紫色为Agent
Infra，蓝色为Model Infra；条长共用尺度，右列为有值数/名单数。类别值为已观测仓库值之和。
类别总量也受收录数量影响：编码代理有16项，推理引擎有8项，个人助手有7项。这里
的排序用于定位继续调查的区域，不能直接解释为单位项目效率、技术需求或支持优先级。
OpenRank反映协作网络影响，不是用户数、模型性能或市场份额。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
120

## PDF 第 121 页

OSDGs
/
GOSD 2026
全球开源发展报告
4.1 Agentic AI 全景洞察
月度位置提示变化，也受到观测覆盖影响
个人助手在Agent Infra中从较后位置进入前列；Model Infra的推理引擎则始终位居本层首
位。沿全景分类排列的月度矩阵，让任务入口的变化与基础工具的稳定位置可以同时被看见。
25.07
25.08
25.09
25.10
25.11
25.12
26.01
26.02
26.03
26.04
26.05
26.06
编码代理
编码工作流与工具链
个人助手
聊天工作区
多代理编排
工作流与代理构建
代码优先框架
记忆、知识与上下文
协议与互操作
工具与计算机使用
开发沙箱
可观测与评估
1
1
1
1
1
1
1
1
1
1
1
2
—
12
12
12
12
11
8
7
7
7
7
9
10
9
8
8
9
9
4
2
2
2
2
1
4
4
4
4
4
4
5
6
8
9
10
11
9
10
10
9
10
10
11
11
6
5
4
4
3
3
3
3
3
3
3
4
4
4
5
6
2
2
2
2
2
2
2
3
3
3
3
3
5
5
5
5
5
5
6
5
5
6
6
5
8
8
9
10
8
7
9
9
9
10
9
10
11
11
11
11
11
12
12
12
12
12
11
8
7
7
7
7
7
8
10
10
11
8
8
7
6
6
6
6
6
6
7
8
10
11
12
12
Agent Infra / 沿全景分类顺序阅读
25.07
25.08
25.09
25.10
25.11
25.12
26.01
26.02
26.03
26.04
26.05
26.06
模型 API 网关
服务部署
推理引擎
强化学习与环境
监督微调
训练框架与并行
训练评估与观测
机器人基础设施
编译器与加速
数据标注
数据集成
数据治理
计算与调度
7
8
8
9
9
9
9
8
7
8
8
8
9
7
9
8
7
8
6
4
3
3
3
3
1
1
1
1
1
1
1
1
1
1
1
1
6
6
6
6
4
4
4
9
9
9
9
9
10
10
10
10
10
10
10
11
11
11
11
11
2
2
2
2
2
2
2
2
2
2
2
2
11
11
11
11
11
11
11
10
10
10
10
10
13
13
13
12
12
12
12
12
12
12
12
12
8
9
7
7
8
7
8
6
5
5
4
4
12
12
12
13
13
13
13
13
13
13
13
13
4
4
4
4
5
6
5
5
6
6
6
6
3
3
3
3
3
3
3
3
4
4
5
5
5
5
5
5
6
5
7
7
8
7
7
7
Model Infra / 沿全景分类顺序阅读
图4‑4　两层全景的月度类别位置
来源：OpenDigger冻结响应。2025‑07至2026‑06。数字为各自层内的类别名次，颜色越深越靠前；并列按同名次处理，无观测留
空。Agent与Model分别计算，名次不直接跨层比较。
位次变化不等于同一批项目的增长。个人助手7项中，只有2项在整个主期连续有值；类别位
置的移动也包含后来进入观测的项目。编码工作流与工具链在2025年7月没有观测，空白不能解释
为相关能力尚不存在。
因此，既要保留当前全景来发现新的可见对象，也要用固定的连续样本观察既有项目。两种
范围回答不同的问题，需要在同一叙事中并读。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
121

## PDF 第 122 页

OSDGs
/
GOSD 2026
全球开源发展报告
4.1 Agentic AI 全景洞察
观测范围改变，趋势方向也可能改变
期末前三类的曲线并不相同：个人助手在主期后半段抬升较明显，编码代理与推理引擎呈现
另一种走势。分面共用刻度后，差异更容易辨认；进一步固定对象，整体轨迹又出现变化。
25.07
25.12
26.06
0
2,000
4,000
个人助手
25.07
25.12
26.06
编码代理
25.07
25.12
26.06
推理引擎
25.07
25.08
25.09
25.10
25.11
25.12
26.01
26.02
26.03
26.04
26.05
26.06
0
5,000
10,000
15,000
108
111
116
118
122
125
130
135
140
141
142
141
B  同时查看观测范围
名单中当月有值项目
107项全期共同样本
A  期末前三类 / 各小图共用0—4,000刻度
上行数字：各月有值项目数；两组图均为OpenRank，纵轴范围不同。
图4‑5　重点功能区的分值轨迹与观测范围
来源：OpenDigger冻结响应。2025‑07至2026‑06。上图为当月有值项目合计，三类共用0—4,000刻度；下图比较全名单已观测合
计与107项全期共同样本，两线共用纵轴。上行数字为各月有值项目数；缺失不补零。
2026年1月至3月，全名单已观测合计由13,916.42升至15,009.23，107项共同样本却由
12,705.10降至11,486.11。期末26.6%的合计来自非全期连续有值项目，不能把全部变化归给
同一批既有项目。
覆盖扩展与既有项目变化应分别观察。这里描述冻结指标的轨迹；历史算法版本与跨月归一
化参数未完全固定，不能据共同回落推断产业衰退，也不能据覆盖增加推断全球参与增长。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
122

## PDF 第 123 页

OSDGs
/
GOSD 2026
全球开源发展报告
4.1 Agentic AI 全景洞察
份额上升，不一定意味着绝对扩张
在连续有值的107项中，服务部署、编码代理、多代理编排以及编译器与加速的份额上升较
多。这些类别分布于不同层级，相对变化并不集中于单一技术路线。
-3
-2
-1
0
1
2
3
4
2025.07 → 2026.06 / 份额变化（百分点）
服务部署
编码代理
多代理编排
编译器与加速
开发沙箱
推理引擎
个人助手
编码工作流与工具链
协议与互操作
训练评估与观测
可观测与评估
数据治理
数据标注
训练框架与并行
记忆、知识与上下文
计算与调度
机器人基础设施
数据集成
工具与计算机使用
模型 API 网关
代码优先框架
强化学习与环境
监督微调
工作流与代理构建
聊天工作区
+3.44
3
+2.76
9
+2.45
2
+2.06
8
+1.07
3
+1.04
7
+0.05
2
无共同样本
0
≈0.00
6
-0.06
2
-0.08
4
-0.19
7
-0.21
1
-0.21
6
-0.28
5
-0.33
4
-0.35
2
-0.37
4
-0.61
3
-0.70
3
-1.17
11
-1.38
4
-1.47
3
-2.49
5
-2.97
3
共同项数
图4‑6　共同样本在全景各类别中的份额变化
来源：OpenDigger冻结响应。固定107项，比较2025‑07与2026‑06端点；分母为共同样本当月OpenRank合计。紫色为Agent，
蓝色为Model，右列为共同项数；无共同样本不解释为稳定。
服务部署的份额由2.83%升至6.27%，分值由412.26变为416.59；编码代理份额由14.83%升
至17.59%，分值却由2,161.89降至1,169.58。同样是份额上升，一类分值基本稳定，另一类分值
下降。
共同样本减少了覆盖差异，也排除了中途进入和缺少记录的项目。例如个人助手仅2项进入共
同样本，不能据此替代其当前7项全貌。相对位置、绝对轨迹与当前名单需要同时保留。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
123

## PDF 第 124 页

OSDGs
/
GOSD 2026
全球开源发展报告
4.1 Agentic AI 全景洞察
从功能区进入项目，辨认不同的集中结构
推理引擎8项在期末均有值；vLLM、SGLang与TensorRT‑LLM在主期每月都居前三，期末
合占该类的66.7%。头部组合稳定，分值与相互差距仍在变化。
位次 / 项目
期末值
25.07
26.06
1
vLLM
274.25
2
SGLang
263.19
3
TensorRT-LLM
214.20
4
llama.cpp
142.46
5
vLLM Omni
90.15
6
ONNX Runtime
63.96
7
OpenVINO
44.65
8
LMCache
34.45
每行共用0—800刻度；缺失月份断线，不补零。
图4‑7　推理引擎的项目位置与完整月度记录
来源：OpenDigger冻结响应。按2026‑06值排列；轨迹为2025‑07至2026‑06，每行统一0—800刻度。缺失月份断线，不补零；相
关仓库不视为完全独立生态。
个人助手更集中：OpenClaw与Hermes Agent期末分别为592.19和518.86，两项合占该类
的80.9%。同样进入期末前三类的功能区，内部结构并不相同。
0
25%
50%
OpenClaw
Hermes Agent
QwenPaw
ZeroClaw
LobeHub
nanobot
AstrBot
43.1%
37.8%
4.4%
4.3%
3.7%
3.4%
3.3%
个人助手 / 全部7项
0
50%
100%
个人助手
编码代理
推理引擎
85.3%
67.3%
66.7%
三类前3项占比
图4‑8　个人助手完整构成与三类头部集中度
来源：OpenDigger冻结响应。2026‑06，均以各类别有值项目合计为分母。前三项占比分别为85.3%、67.3%、66.7%，不是用户
或技术依赖份额。
完整全景定位能力，类内对照定位对象。集中度有助于选择后续维护调查的入口，不能单凭
指标判断系统脆弱性、市场支配或资助顺序。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
124

## PDF 第 125 页

OSDGs / GOSD 2026
第四章 · 全球开源技术全景洞察
4.2 AI ⼤模型任务全景
96 个模型仓库 · 6 类任务 · 各类近期下载 Top 16
2026-10-02 期后快照；序号为类内名次，各类等额截取。
语⾔与检索
视觉与融合
声⾳与⾏动
⽂本⽣成
16
Qwen3-0.6B
Qwen
gpt2
openai-community
Qwen3-8B
Qwen
tiny-Qwen2ForCausalLM-2.5
trl-internal-testing
Qwen2.5-7B-Instruct
Qwen
Qwen2.5-0.5B-Instruct
Qwen
Qwen3-Coder-30B-A3B-Instruct-GGUF
unsloth
Llama-3.2-1B-Instruct
meta-llama
Qwen2.5-1.5B-Instruct
Qwen
Qwen3-4B
Qwen
opt-125m
facebook
gpt-oss-20b
openai
Kimi-K3-DSpark
RadixArk
Qwen3.6-35B-A3B-NVFP4
nvidia
Llama-3.1-8B-Instruct
meta-llama
Ornith-1.5-9B-GGUF
ornith-ai
嵌⼊与检索
16
all-MiniLM-L6-v2
sentence-transformers
ms-marco-MiniLM-L6-v2
cross-encoder
bge-small-en-v1.5
BAAI
paraphrase-multilingual-MiniLM-L12-v2
sentence-transformers
bge-m3
BAAI
all-mpnet-base-v2
sentence-transformers
nomic-embed-text-v1.5
nomic-ai
multilingual-e5-small
intfloat
bge-base-en-v1.5
BAAI
paraphrase-multilingual-mpnet-base-v2
sentence-transformers
bge-large-en-v1.5
BAAI
Qwen3-Embedding-0.6B
Qwen
multilingual-e5-large
intfloat
multilingual-e5-base
intfloat
ms-marco-MiniLM-L4-v2
cross-encoder
granite-embedding-small-english-r2
ibm-granite
图像与视频
16
标识
待核
mobilenetv3_small_100.lamb_in1k
timm
clip-vit-base-patch32
openai
vit-base-patch16-224
google
clip-vit-large-patch14
openai
locate-anything.cpp-gguf
mudler
Wan_2.2_ComfyUI_Repackaged
Comfy-Org
stable-diffusion-xl-base-1.0
stabilityai
siglip2-base-patch16-256
google
CLIP-ViT-B-32-laion2B-s34B-b79K
laion
CLIP-ViT-L-14-laion2B-s32B-b82K
laion
Depth-Anything-V2-Small-hf
depth-anything
fashion-clip
patrickjohncyh
clip-vit-large-patch14-336
openai
sam3
facebook
nsfw_image_detection
Falconsai
标识
待核
resnet18.a1_in1k
timm
多模态
16
Qwen3-VL-8B-Instruct
Qwen
gemma-4-26B-A4B-it
google
gemma-4-31B-it
google
Qwen3.5-9B
Qwen
Qwen3.5-4B
Qwen
Qwen3.8-27B
Qwen
Qwen2.5-VL-7B-Instruct
Qwen
Qwen3.6-35B-A3B-FP8
Qwen
GLM-5.3-Flash
zai-org
Qwen3.8-27B-FP8
Qwen
Qwen3.5-2B
Qwen
gemma-4-E4B-it
google
Qwen3.8-27B-MLX-4bit
lmstudio-community
Qwen3.8-27B-MLX-8bit
lmstudio-community
Qwen3.8-27B-MLX-6bit
lmstudio-community
Qwen3.8-27B-MLX-5bit
lmstudio-community
语⾳与⾳频
16
wav2vec2-large-xlsr-53-japanese
jonatasgrosman
Kokoro-82M
hexgrad
whisperkit-coreml
argmaxinc
clap-htsat-fused
laion
speaker-diarization-3.1
pyannote
XTTS-v2
coqui
whisper-large-v3-turbo
openai
audio.cpp-gguf
audio-cpp
wav2vec2-large-xlsr-53-portuguese
jonatasgrosman
speaker-diarization-community-1
pyannote
segmentation-3.0
pyannote
wav2vec2-large-xlsr-53-russian
jonatasgrosman
whisper-large-v3
openai
faster-whisper-small
Systran
whisper-small
openai
mms-300m-1130-forced-aligner
MahmoudAshraf
机器⼈
16
GR00T-N1.7-3B
nvidia
标识
待核
openvla-7b
openvla
libero4in1_wan2.2vae_latent_cosmos_style
MangoGoes
smolvla_base
lerobot
JiRackPrecisionTokenizer
CMSManhattan
smolvla_libero
HuggingFaceVLA
pi0_base
lerobot
Alpamayo-1.5-10B
nvidia
GR00T-N1.6-3B
nvidia
microduck-policies
pollen-robotics
pi05_libero_finetuned_v044
lerobot
MolmoAct2
allenai
pi05_base
lerobot
smolvla_libero
lerobot
openvla-7b-oft-finetuned-libero-spatial
moojink
MolmoAct2-Pretrain
allenai
图4-9 AI ⼤模型任务全景 · 完整观察名单
来源：原报告固定表 c51e344；快照⽇期沿⽤原元数据，未重建当⽇完整采集链。
标识为发布账⼾头像；3 条原图哈希不匹配，继续标为待核。可下载不等于完整开源。
区域按功能组织，⾯积不编码规模；点击条⽬可到来源链接。分类与收录不构成依赖、许可或成效认证。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
125

## PDF 第 126 页

OSDGs
/
GOSD 2026
全球开源发展报告
4.2 AI 大模型全景洞察
模型条目分散，不等于发布主体分散
全景按六类任务各取近期下载Top 16，保留96个模型仓库。嵌入与检索的第一项占本类
41.2%，前三项合占66.6%；多模态区相应为14.3%和35.2%。同样16项，内部集中结构并不相
同。
0
25
50
75
100%
文本生成
嵌入与检索
图像与视频
多模态
语音与音频
机器人
19.3
36.8%
41.2
66.6%
20.6
50.6%
14.3
35.2%
15.3
36.1%
18.9
47.9%
空心：第一项   实心：前三项合计
图4‑10　六类近期下载的样本内集中程度
来源：原报告冻结表，2026‑10‑02期后快照。分母为各类近期下载Top 16的下载合计；空心点为第一项，实心点为前三项。不是
全领域集中度或市场份额。
按发布账户归组，多模态16项来自4个账户；Qwen与google合占80.3%的样本内下载。仓库
层面较分散的结构，可以同时集中于少数发布账户。
嵌入与检索
sentence-transformers
54.9%  / 4项
BAAI
20.2%  / 4项
cross-encoder
15.6%  / 2项
intfloat
4.5%  / 3项
nomic-ai
2.3%  / 1项
Qwen
1.7%  / 1项
ibm-granite
0.9%  / 1项
多模态
Qwen
55.5%  / 8项
google
24.8%  / 3项
lmstudio-community
14.9%  / 4项
zai-org
4.8%  / 1项
图4‑11　两类样本的发布账户构成
来源：原报告冻结表，同一期后快照。按完全一致的publisher字段汇总；右列为下载份额与仓库条数。账户未经机构合并，不等
于最终母公司或全部贡献者。
Hugging Face下载计数基于指定文件请求，不能解释为独立用户或部署数；不同模型库与格式的计数规则也可能不同。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
126

## PDF 第 127 页

OSDGs
/
GOSD 2026
全球开源发展报告
4.2 AI 大模型全景洞察
保留完整类内对照，区分模型、版本与账户
检索区同时出现向量表示与相关性排序模型；多模态区包含Qwen、Gemma等不同版本。以
下保留两类全部32条，避免由头部几个名称代替完整结构。
嵌入与检索
每条占本类别 Top 16 下载合计的比例
all-MiniLM-L6-v2
01
41.2
ms-marco-MiniLM-L6-v2
02
14.6
bge-small-en-v1.5
03
10.8
paraphrase-multilingual-MiniLM-L12-v2
04
8.6
bge-m3
05
6.0
all-mpnet-base-v2
06
3.4
nomic-embed-text-v1.5
07
2.3
multilingual-e5-small
08
2.0
bge-base-en-v1.5
09
1.7
paraphrase-multilingual-mpnet-base-v2
10
1.7
bge-large-en-v1.5
11
1.7
Qwen3-Embedding-0.6B
12
1.7
multilingual-e5-large
13
1.3
multilingual-e5-base
14
1.2
ms-marco-MiniLM-L4-v2
15
1.0
granite-embedding-small-english-r2
16
0.9
0
45%
多模态
每条占本类别 Top 16 下载合计的比例
Qwen3-VL-8B-Instruct
01
14.3
gemma-4-26B-A4B-it
02
11.9
gemma-4-31B-it
03
9.0
Qwen3.5-9B
04
8.3
Qwen3.5-4B
05
6.9
Qwen3.8-27B
06
6.3
Qwen2.5-VL-7B-Instruct
07
5.4
Qwen3.6-35B-A3B-FP8
08
5.2
GLM-5.3-Flash
09
4.8
Qwen3.8-27B-FP8
10
4.6
Qwen3.5-2B
11
4.4
gemma-4-E4B-it
12
4.0
Qwen3.8-27B-MLX-4bit
13
3.9
Qwen3.8-27B-MLX-8bit
14
3.7
Qwen3.8-27B-MLX-6bit
15
3.7
Qwen3.8-27B-MLX-5bit
16
3.7
0
45%
图4‑12　检索与多模态的完整类内下载结构
来源：原报告冻结表，2026‑10‑02期后快照。每列各16项，以各自下载合计为100%；条长共用0—45%尺度，行序按原表名次。
完整模型标识见全景及随附数据。
多模态区lmstudio‑community的4条记录属于同一命名家族的MLX 4bit、5bit、6bit与8bit
版本。将它们视为四种独立能力会夸大多样性，直接合并又会丢失运行格式的维护对象。本节保
留原仓库，家族与派生关系另行核对。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
127

## PDF 第 128 页

OSDGs
/
GOSD 2026
全球开源发展报告
4.2 AI 大模型全景洞察
改变观察指标，改变的往往是入选对象
近期下载反映近30天的文件获取信号，累计下载保留更长历史的积累，点赞记录关注。三项
指标按六类任务分别取Top 16，共288条榜单记录，对应194个唯一模型仓库，三榜同时出现的仅
22个。
近期 ∩ 累计
近期 ∩ 点赞
累计 ∩ 点赞
文本生成
12/16
3/16
3/16
嵌入与检索
12/16
8/16
7/16
图像与视频
10/16
2/16
1/16
多模态
8/16
3/16
2/16
语音与音频
11/16
7/16
6/16
机器人
11/16
4/16
6/16
64 个共同模型
27 个共同模型
25 个共同模型
六类合计
图4‑13　改变观察指标后保留了多少共同模型
来源：原报告冻结表，同一原表快照（2026‑10‑02，期后）。每个彩色小方块为1个共同模型，灰色为未重合名额；分母为每榜每
类固定的16个名额。各列为两榜交集，不是增长率。
近期与累计下载共有64个模型，近期下载与点赞仅共有27个。图像与视频区的近期下载与点
赞榜只有2个共同条目，累计下载与点赞榜只有1个。
该区近期下载首位为timm 的MobileNetV3 Small，累计下载首位为Falconsai 的ns‑
fw_image_detection，点赞首位则为black‑forest‑labs的FLUX.1‑dev。频繁获取与受到关注，
把读者带向不同任务和对象。
三种视图来自同一快照，不能顺次连接成时间曲线；没有进入某一Top 16也不能补成零值。
持续观察需要先固定要回答的问题，再固定对象、任务边界和时间窗口。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
128

## PDF 第 129 页

OSDGs
/
GOSD 2026
全球开源发展报告
4.2 AI 大模型全景洞察
机器人样本：近期获取、历史积累与关注各有重点
机器人区把三种观察的差异呈现得更清楚。近期下载首位GR00T‑N1.7‑3B占本类18.9%；累
计下载首位OpenVLA占84.1%；点赞首位SmolVLA占12.2%。这些比例分别来自三份独立选样的
榜单。
近期下载 Top 5
占各自 Top 16 合计
nvidia/GR00T-N1.7-3B
18.9%
openvla/openvla-7b
16.2%
MangoGoes/libero4in1_wan2.2vae_latent_cosmos_style
12.7%
lerobot/smolvla_base
11.0%
CMSManhattan/JiRackPrecisionTokenizer
8.3%
累计下载 Top 5
占各自 Top 16 合计
openvla/openvla-7b
84.1%
lerobot/smolvla_base
3.4%
nvidia/GR00T-N1.7-3B
1.8%
nvidia/Alpamayo-R1-10B
1.6%
nvidia/Alpamayo-1.5-10B
1.5%
点赞 Top 5
占各自 Top 16 合计
lerobot/smolvla_base
12.2%
nvidia/Alpamayo-R1-10B
11.7%
microsoft/Magma-8B
11.1%
nvidia/GR00T-N1-2B
9.5%
lerobot/pi0_old
8.3%
图4‑14　机器人模型在三种观察中的头部构成
来源：原报告冻结表，2026‑10‑02期后快照。每榜展示前5项，分母仍为对应榜单全部16项；不是将前5项重新归一化。三榜分别
选样，下载与点赞不等于设备部署、使用者或执行效果。
同一任务区可以同时保留探索热点、历史积累与社区关注。机器人模型能否用于实际任务，
还要确认观测输入、动作表示、控制器与物理设备之间的匹配。下载信号能够提示调查对象，不
能替代运行环境中的验证。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
129

## PDF 第 130 页

OSDGs
/
GOSD 2026
全球开源发展报告
4.2 AI 大模型全景洞察
放宽视野：专用模型与运行工具同样重要
HF夏季报告显示，在2026年7月29日的累计下载分布中，参数少于10亿的模型占全Hub下载
的61.5%；约26%对应缺少参数规模信息的仓库。只在已标注参数的部分归一化，小模型比例才约
为83%。
小于 10 亿参数
10 亿至 100 亿参数
100 亿至 700 亿参数
超过 700 亿参数
无参数规模元数据
61.5%
8.6%
2.8%
1%
26%
图4‑15　模型参数规模与累计下载分布
来源：HF Summer 2026，2026‑07‑29期后快照。按官方图精确标签复绘，未取得逐模型底表；分母含无参数元数据仓库，原图
舍入合计99.9%，未补造尾差。
技术观察也要覆盖可嵌入具体工作流的专用能力。这一结果与全景中的MiniLM、Mo‑
bileNet等对象相呼应，但不能据下载份额判断小模型在所有任务中更有效或更节能。
声明的运行库 / 格式
仓库数：期初 → 期末
仓库数增长
gguf
532 → 2,999
+464%
lerobot
8,060 → 23,705
+194%
mlx
5,605 → 13,881
+148%
sentence-transformers
15,915 → 22,458
+41%
diffusers
98,229 → 118,775
+21%
transformers
774,732 → 900,636
+16%
peft
221,821 → 257,218
+16%
图4‑16　模型仓库声明的运行库与格式增长
来源：HF Summer 2026，2026‑01‑07至2026‑07‑29，跨越主期截止日。按官方印刷标签复绘；统计声明相应library的模型仓库
数，不是下载、安装或用户增长。标签未必互斥，不能相加为Hub总量。
GGUF的高增幅来自较小基数，Transformers的绝对仓库数仍大得多。MLX、LeRobot等变
化则让运行适配和具身工具进入视野：模型能否被采用，还取决于格式、工具与接口。这是更宽
的生态背景，不是对前述96条样本变化的因果解释。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
130

## PDF 第 131 页

OSDGs
/
GOSD 2026
全球开源发展报告
4.2 AI 大模型全景洞察
回到任务，检查能力之间能否接续
全景帮助寻找模型，模型卡进一步说明其输入、输出和使用条件。若要把多个模型用于同一
任务，还需要逐环节核对。下图归纳可按任务组合的能力，并不表示这些项目已被组合部署。
资料问答
检索表示
all-MiniLM-L6-v2
召回覆盖
›
相关性排序
ms-marco-MiniLM-L6-v2
相关性排序
›
文本生成
固定具体生成模型
回答、引用与拒答
语音服务
语音识别
whisper-small
口音与噪声
·
说话人分析
pyannote 系列
分段与说话人
·
语音生成
Kokoro-82M
发音与可懂度
机器人任务
环境与指令
输入、传感与标定
环境覆盖
›
动作策略
openvla-7b 等
动作成功与失误
›
系统执行
控制器与机器人
物理安全边界
图4‑17　从任务链定位模型与检验环节
来源：全景分类及相关模型卡的阅读归纳，非部署实测。资料问答与机器人行示意任务环节；语音行列出可组合能力，无需全部
采用或固定串行。
资料问答：分别检验表示、检索与回答
all‑MiniLM‑L6‑v2将句段转换为向量，cross‑encoder为查询与候选资料计算相关性；检索
能否支撑回答，还需要引用核对与生成环节的检验。
语音服务：区分识别、说话人分析与生成
Whisper‑small识别语音，Kokoro‑82M合成语音，pyannote区分谁在何时说话。三者输出
和评测任务不同，采用前还要检查语言、噪声与说话人条件。
机器人任务：验证动作接口与设备条件
OpenVLA提供视觉语言动作模型与推理说明；实际部署仍须确认动作归一化、机器人接口与
安全约束。功能位置、下载名次都不能替代具体场景中的验证。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
131

## PDF 第 132 页

OSDGs / GOSD 2026
第四章 · 全球开源技术全景洞察
4.3 云基础设施全景
86 个仓库 · 31 个类别 · 4 个功能区
沿交付、运⾏、资源与观测辨认技术分⼯；空类别保留。
应⽤与开发
编排与运⾏
资源与安全
观测与扩展
应⽤定义与镜像构建
3
podman
podman-container-tools
gradle
gradle
compose
docker
持续集成与交付
5
keploy
keploy
bytebase
bytebase
k6
grafana
jenkins
jenkinsci
devtron
devtron-labs
数据库
12
scylladb
scylladb
tidb
pingcap
yugabyte-db
yugabyte
TDengine
taosdata
druid
apache
cassandra
apache
shardingsphere
apache
arangodb
arangodb
redis
redis
hadoop
apache
ignite
apache
foundationdb
apple
流与消息
9
spark
apache
kafka
apache
beam
apache
flink
apache
seatunnel
apache
nifi
apache
pulsar
apache
rabbitmq-server
rabbitmq
emqx
emqx
调度与编排
2
nomad
hashicorp
volcano
volcano-sh
协调与服务发现
1
nacos
alibaba
API ⽹关
5
gravitee-api-management
gravitee-io · ⾝份待核
higress
higress-group
kgateway
kgateway-dev
tyk
TykTechnologies
apisix
apache
服务代理
4
envoy
envoyproxy
traefik
traefik
trafficserver
apache
caddy
caddyserver
服务⽹格
3
meshery
meshery
consul
hashicorp
kuma
kumahq
远程过程调⽤
0
固定名单未收录
容器运⾏时
2
runc
opencontainers
lxd
canonical
云原⽣⽹络
2
calico
projectcalico
antrea
antrea-io
云原⽣存储
2
velero
velero-io
minio
minio
⾃动化与配置
7
pulumi
pulumi
terraform
hashicorp
cloudstack
apache
ansible
ansible
juju
juju
cadence
uber
salt
saltstack
密钥管理
3
teleport
gravitational
keycloak
keycloak
vault
hashicorp
安全与合规
3
tetragon
cilium
external-secrets
external-secrets
openfga
openfga
容器镜像仓库
0
固定名单未收录
K8s 安装器认证
4
gardener
gardener
talos
siderolabs
minikube
kubernetes
kubespray
kubernetes-sigs
K8s 发⾏版认证
3
kubermatic
kubermatic
k3s
k3s-io
vcluster
loft-sh
PaaS 与容器服务
1
portainer
portainer
可观测性
10
grafana
grafana
mimir
grafana
loki
grafana
beats
elastic
centreon
centreon
vector
vectordotdev
netdata
netdata
tempo
grafana
deepflow
deepflowio
influxdb
influxdata
功能开关
0
固定名单未收录
持续优化
0
固定名单未收录
混沌⼯程
0
固定名单未收录
WASM ⼯具链
2
llvm-project
llvm
emscripten
emscripten-core
WASM 运⾏时
1
wasmtime
bytecodealliance
WASM 规范
0
固定名单未收录
Serverless 框架
1
sst
anomalyco
Serverless 托管平台
1
azure-functions-host
Azure
Serverless 可安装平台
0
固定名单未收录
Serverless ⼯具
0
固定名单未收录
图4-18 云基础设施全景 · 完整观察名单
来源：原报告固定清单 c51e344 与 OpenDigger 标签 5c2ffc4；原表“2026”起⽌窗⼝待核。
项⽬ Logo 优先，账⼾头像补充；⾝份差异条⽬明确标记。名单不是全球普查或认证⽬录。
区域按功能组织，⾯积不编码规模；点击条⽬可到来源链接。分类与收录不构成依赖、许可或成效认证。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
132

## PDF 第 133 页

OSDGs / GOSD 2026
第四章 · 全球开源技术全景洞察
4.4 数据库系统全景
93 个仓库 · 17 个类别 · 3 个功能区
沿数据模型和查询任务定位对象；每个仓库仅在主位置出现⼀次。
通⽤与结构化
检索与关联
专⽤数据语义
关系型
12/34
ClickHouse
ClickHouse
doris
apache
cockroach
cockroachdb
spark
apache
trino
trinodb
datafusion
apache
mimir
grafana
pinot
apache
velox
facebookincubator
duckdb
duckdb
server
MariaDB
risingwave
risingwavelabs
关系型 · 续
12/34
cubrid
CUBRID
flink
apache
SpacetimeDB
clockworklabs
hive
apache
shardingsphere
apache
vitess
vitessio
matrixone
matrixorigin
comdb2
bloomberg
databend
databendlabs
datafusion-comet
apache
paradedb
paradedb
ArcticDB
man-group
关系型 · 续
10/34
firebird
FirebirdSQL
dolt
dolthub
tigerbeetle
tigerbeetle
datafusion-sqlparser-rs
apache
neon
neondatabase
h2database
h2database
cloudberry
apache
citus
citusdata
phoenix
apache
gel
geldata
键值
11/22
ydb
ydb-platform
scylladb
scylladb
tidb
pingcap
yugabyte-db
yugabyte
presto
prestodb
wiredtiger
wiredtiger
etcd
etcd-io
valkey
valkey-io
ignite-3
apache
ravendb
ravendb
rocksdb
facebook
键值 · 续
11/22
dragonfly
dragonflydb
tarantool
tarantool
cassandra
apache
redis
redis
ignite
apache
foundationdb
apple
garnet
microsoft
infinispan
infinispan
slatedb
slatedb
tikv
tikv
kvrocks
apache
宽列
5
starrocks
StarRocks
hbase
apache
delta
delta-io
druid
apache
accumulo
apache
列存
0
固定名单未收录
⽂档
5
venice
linkedin
crate
crate
lancedb
lancedb
defradb
sourcenetwork
ytsaurus
ytsaurus
搜索引擎
8
elasticsearch
elastic
OpenSearch
opensearch-project
lucene
apache
vespa
vespa-engine
manticoresearch
manticoresoftware
elasticsearch-specification
elastic
meilisearch
meilisearch
typesense
typesense
向量
4
milvus
milvus-io
weaviate
weaviate
qdrant
qdrant
chroma
chroma-core
图
4
arangodb
arangodb
surrealdb
surrealdb
memgraph
memgraph
kuzu
kuzudb
时序
8
prometheus
prometheus
TDengine
taosdata
VictoriaMetrics
VictoriaMetrics
timescaledb
timescale
iotdb
apache
questdb
questdb
greptimedb
GreptimeTeam
influxdb
influxdata
空间
1
sedona
apache
事件
1
KurrentDB
kurrent-io
⾯向对象
1
spicedb
authzed
层次
0
固定名单未收录
RDF
0
固定名单未收录
原⽣ XML
0
固定名单未收录
数组
0
固定名单未收录
内容
0
固定名单未收录
图4-19 数据库系统全景 · 完整观察名单
来源：原报告固定清单 c51e344 与 OpenDigger 标签 5c2ffc4；期后整理的固定观察名单。
31 项有附加标签，完整映射随数据保留；空类别不表⽰技术不存在，头像只识别账⼾。
区域按功能组织，⾯积不编码规模；点击条⽬可到来源链接。分类与收录不构成依赖、许可或成效认证。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
133

## PDF 第 134 页

OSDGs / GOSD 2026
第四章 · 全球开源技术全景洞察
4.5 RISC-V 技术全景
78 条记录 · 7 个技术类别 · 3 条待核记录单列
由软件任务进⼊构建验证，再到实现与共同规范。
软件与应⽤
构建与验证
实现与规范
应⽤
5
riscv-pvm
tezos
risc0
risc0
risc0-ethereum
risc0
x264
zte-riscv
kailua
boundless-xyz
操作系统
7
oerv-team
openeuler-riscv
archriscv-packages
felixonmars
linux
linux-riscv
meta-riscv
riscv
linux-riscv
sophgo
xv6-riscv
mit-pdos
bootloader-riscv
sophgo
库
2
riscv
rust-embedded
librpmi
riscv-software-src
基础设施
8
docs-resources
riscv
dev.eessi.io-riscv
EESSI
opentitan-provisioning
lowRISC
docker-for-riscv64
gounthar
tristan-isolde-unified-access-page
openhwgroup
riscv-ci
plctlab
riscv-vale
riscv-admin
riscv-runner-app
riseproject-dev
设计⼯具与编译验证
14
riscv-arch-test
riscv
riscv-isa-sim
riscv-software-src
chisel
chipsalliance
riscv-gnu-toolchain
riscv-collab
qemu
lowRISC
go
zte-riscv
riscv-perf-model
riscv-software-src
cvw-arch-verif
openhwgroup
core-v-verif
openhwgroup
dvsim
lowRISC
riscv-openocd
riscv-collab
firrtl-spec
chipsalliance
rvv-intrinsic-doc
riscv-non-isa
riscv-semantics
runtimeverification
分类与样本待核
3
标识
待核
riscv-unified-db-kallal
7908837174
CMPUT301F25riscvi
RISCVI-301
riscv-processor-design
marcutudor79
芯⽚实现
11/21
opentitan
lowRISC
caliptra-sw
chipsalliance
caliptra-mcu-sw
chipsalliance
caliptra-ss
chipsalliance
caliptra-rtl
chipsalliance
cva6
openhwgroup
Caliptra
chipsalliance
cvw
openhwgroup
t1
chipsalliance
risc-v
UTOSS
i3c-core
chipsalliance
芯⽚实现 · 续
10/21
VexiiRiscv
SpinalHDL
RISCVBusiness
Purdue-SoCET
adams-bridge
chipsalliance
ibex
lowRISC
caliptra-dpe
chipsalliance
mocha
lowRISC
Cores-VeeR-EL2
chipsalliance
cv-hpdcache
openhwgroup
core-v-mcu
openhwgroup
sonata-system
lowRISC
RISC-V 规范与计划
9/18
riscv-isa-manual
riscv
sail-riscv
riscv
riscv-unified-db
riscv
riscv-cheri
riscv
riscv-iommu
riscv-non-isa
riscv-fast-interrupt
riscv
iopmp-spec
riscv-non-isa
riscv-smmtt
riscv
riscv-trace-spec
riscv-non-isa
RISC-V 规范与计划 · 续
9/18
riscv-memory-tagging
riscv
riscv-isa-manual
RISC-V-Certification-Steering-Committee
riscv-external-debug-security
riscv-non-isa
riscv-hart-trace-interface
riscv-non-isa
riscv-server-platform
riscv-non-isa
riscv-opcodes
riscv
riscv-spmp
riscv
riscv-isa-manual
davidharrishmc
riscv-p-spec
riscv
图4-20 RISC-V 技术全景 · 完整观察名单
来源：原报告固定清单与 RISC-V 分类映射；原表“2026”起⽌窗⼝待核。
标识为所属账⼾头像，不把多个仓库等同多个独⽴系统；标识缺失及分类待核如实保留。
区域按功能组织，⾯积不编码规模；点击条⽬可到来源链接。分类与收录不构成依赖、许可或成效认证。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
134

## PDF 第 135 页

OSDGs / GOSD 2026
第四章 · 全球开源技术全景洞察
4.6 PyTorch ⽣态全景
83 个仓库 · 13 个技术类别 · 1 条⽣态归属待核
围绕 PyTorch 的技术观察样本，不是基⾦会正式托管名单。
模型与任务
训练与执⾏
⼯程与协作
计算机视觉
1
vision
pytorch
⾳频
1
audio
pytorch
强化学习
3
rl
pytorch
OpenEnv
meta-pytorch
torchforge
meta-pytorch
领域应⽤
7
torchrec
meta-pytorch
pytc-client
PytorchConnectomics
pytorch_connectomics
PytorchConnectomics
pytorch_tabular
pytorch-tabular
VesiclePy
PytorchConnectomics
SynAnno
PytorchConnectomics
pytorch-lifestream
pytorch-lifestream
数据
3
torchcodec
meta-pytorch
data
meta-pytorch
tokenizers
meta-pytorch
隐私
1
opacus
meta-pytorch
训练
5
pytorch
pytorch
torchtune
meta-pytorch
ignite
pytorch
tnt
meta-pytorch
torcheval
pytorch
分布式训练
8
torchtitan
pytorch
monarch
meta-pytorch
torchcomms
meta-pytorch
autoparallel
meta-pytorch
torchft
meta-pytorch
torchstore
meta-pytorch
gloo
pytorch
kraken
pytorch-labs
编译器与运⾏时
7
executorch
pytorch
helion
pytorch
TensorRT
pytorch
xla
pytorch
tritonparse
meta-pytorch
tlparse
meta-pytorch
compile-graph-break-site
meta-pytorch
优化
13
ao
pytorch
FBGEMM
pytorch
tritonbench
meta-pytorch
botorch
meta-pytorch
tensordict
pytorch
kineto
pytorch
MSLK
meta-pytorch
BackendBench
meta-pytorch
KernelAgent
meta-pytorch
attention-gym
meta-pytorch
benchmark
pytorch
chakra_replay
meta-pytorch
AccelKernels
meta-pytorch
MLOps
3
torchx
meta-pytorch
captum
meta-pytorch
monarch-kubernetes
meta-pytorch
核心基础设施
11
test-infra
pytorch
ci-infra
pytorch
pytorch-integration-testing
pytorch
cpuinfo
pytorch
FACTO
meta-pytorch
expecttest
pytorch
alerting-infra
pytorch
accelerator-integration-wg
pytorch-fdn
monitoring-observability
pytorch-fdn
extension-cpp
pytorch
multicloud-ci-infra
pytorch-fdn
⽂档与社区
10/19
tutorials
pytorch
torch-release-notes
meta-pytorch
标识
待核
tutorials-kr
PyTorchKorea
ambassador-program
pytorch-fdn
executorch-examples
meta-pytorch
landscape
pytorch-fdn
docs
pytorch
examples
pytorch
ecosystem
pytorch-fdn
pytorch_sphinx_theme
pytorch
⽂档与社区 · 续
9/19
pytorch.github.io
pytorch
tac
pytorch-fdn
rfcs
pytorch
标识
待核
pytorch.kr
PyTorchKorea
标识
待核
oss-landscape
PyTorchKorea
标识
待核
Awesome-Physical-AI
PyTorchKorea
meta-pytorch.github.io
meta-pytorch
foundation-hosted
pytorch-fdn
wg-ospo-and-academic-outreach
pytorch-fdn
分类与样本待核
1
client
PytorchForge
图4-21 PyTorch ⽣态全景 · 完整观察名单
来源：原报告固定清单与 PyTorch 功能映射；原表“2026”起⽌窗⼝待核。
项⽬ Logo 与账⼾头像分别保存来源；PytorchForge/client 不等于 meta-pytorch/torchforge。
区域按功能组织，⾯积不编码规模；点击条⽬可到来源链接。分类与收录不构成依赖、许可或成效认证。
OPEN SOURCE / A SHARED INTELLIGENT FUTURE
135

## PDF 第 136 页

GOSD 2026
04 / CHAPTER REFLECTION
从完整全景
⾛向可复⽤的能力
第四章回望
辨认功能分⼯，再进⼊具体项⽬、版本与运⾏条件。
01
先看完整分⼯，再找具体对象
全景保留任务、⼯具、基础设施与⼯程⽀撑。
按功能找到项⽬，才有进⼀步⽐较和调查的起点。
02
同⼀图景，需要不同观察尺度
项⽬与仓库、模型版本与发布账⼾分别辨认。
位次、份额与绝对值联读，历史与期后窗⼝分开。
03
资源能否复⽤，仍需运⾏证据
技术位置不能替代兼容性、维护和场景验证。
下⼀步把视线落到模型的派⽣、复⽤与开放条件。
下⼀章 / 全球开源⼤模型发展洞察
模型资源怎样被接续开发与使⽤？
从功能全景进⼊模型供给、衍⽣⽹络与具体开放条件。
OPEN SOURCE DEVELOPMENT GOALS
第四章 · 回望与衔接

