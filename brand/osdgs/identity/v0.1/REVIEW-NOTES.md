# 历史评审包说明

以下为 v0.1 评审时的原始说明，保留其当时状态；现已获批，当前状态以 approval.json 和 README.md 为准。

# OSDGs 动态星座配套标识体系

**设计评审稿 v0.1 · 2026-11-12**

这套配套标识延续已批准的 OSDGs v2.0.0 母版，为《2026 全球开源发展报告》及相关网页、演示与传播材料补充四支柱标识和十维方形图标。核心表达为“让开放资源转化为可持续公共能力”。

## 本次新增与继承

- 继承：OSDGs 主标原版矢量、四支柱和十维的层级、名称、编号、固定配色，以及十维的 Lucide 图形。
- 新增：四支柱辅助图形、十维方形色块、角部弧线与十节点导视、中英版本、浅底版本、单色图形及应用示例。
- 新增传播表述：用“参与、供给、复用、治理与公共价值”联系四支柱与十维。该联系用于叙事和阅读导视，不构成指标等价关系或成效证明。
- 状态：新增部分均待评审；不替换已批准母版。本次没有向 GitHub 提交或发布内容。

十维是观察方向，不是新增十个一级目标，也不是章节编号、权重、综合评分或认证标志。联合国 SDG 仅作为编号、色块与图形组合的呈现参考，本套不使用联合国徽记或 SDG 色轮。

## 内容与结构

| 支柱 | 中文名称 | 维度 |
|---|---|---|
| X1 | 人才规模与多样性 | D01、D02 |
| X2 | 技术产出与开放供给 | D03、D04、D05 |
| X3 | 全球连接与网络效应 | D06、D07、D08 |
| X4 | 开源善治与公共价值 | D09、D10 |

| 编号 | 原体系编码 | 中文名称 | English | 阅读色 |
|---|---|---|---|---|
| D01 | 1.1 | 规模与密度 | Scale & Density | #155FA8 |
| D02 | 1.2 | 生态多样性 | Ecosystem Diversity | #087C99 |
| D03 | 2.1 | 代码产出 | Code Output | #007D78 |
| D04 | 2.2 | 模型开放供给 | Open Model Supply | #267D4E |
| D05 | 2.3 | 数据开放供给 | Open Data Supply | #537D25 |
| D06 | 3.1 | 代码影响力 | Code Influence | #8E6500 |
| D07 | 3.2 | 模型影响力 | Model Influence | #AD4E22 |
| D08 | 3.3 | 数据集影响力 | Dataset Influence | #B53863 |
| D09 | 4.1 | 治理成熟度 | Governance Maturity | #943B9A |
| D10 | 4.2 | 公共福祉 | Public Wellbeing | #6146A5 |

## 文件导航

- `assets/master/`：7 个已批准主标与组合标识，直接复制原件，未改路径或字形。
- `assets/pillars/`：4 个支柱的实底、浅底方形标识。
- `assets/dimensions/`：10 维 × 中英/英文 × 实底/浅底。
- `assets/icons/`：4 支柱与10维的彩色、深蓝、白色透明图形。
- `pages/`：6 页评审稿的编辑版 SVG、文字轮廓版 SVG 与渲染组件。
- `source/build_identity.py`：图形和排版生成代码。
- `source/review.tex`：A4 竖版 XeLaTeX 合稿源。
- `source/assemble_review.py`：保留矢量图形、嵌入字体和目录书签的 PDF 合并脚本。
- `source/approved_brand_tokens.json`：已批准的品牌身份与颜色。
- `source/narrative.json`：本次提出的五段传播表述及导视关联。
- `baseline/`：复用所需的原版输入、品牌规则和 Lucide 许可。
- `evidence/`：本次读取的权威仓库原文快照与来源记录。
- `review/`：文字边界检查、原版主标校验和视觉检查记录。

`*-outlined.svg` 的文字已转换为矢量路径，适合跨设备直接使用；无该后缀的 SVG 保留可编辑文字。方形图标 PNG 为 900 × 900 像素，独立图形 PNG 为 400 × 400 像素，背景透明。

## 使用建议

1. 报告、海报和网页总览使用十维方形图标；结构说明使用四支柱分组版。
2. 母标继续遵循原版规范。不得通过增减节点、改变顺序或重配色表示统计结果。
3. 本稿建议完整方形图标印刷宽度不小于32 mm；更小的导视采用单独图形配文字。该最小尺寸仍需正式印样确认。
4. 图形、编号与名称共同识别；颜色只作辅助。实底使用阅读色，高亮色用于节点及辅助装饰。
5. 所有尺寸和颜色均可由 SVG 精确输出。正式印刷需针对纸张和输出设备进行色彩打样。

## 重建

依赖：Python 3、Pillow、lxml、fontTools、CairoSVG、pypdf；Noto Sans CJK SC、DejaVu Sans、Liberation Serif 系统字体。字体二进制不随包分发。本次交付 PDF 由矢量页面直接合并，保留嵌入的中文字体。

```bash
python3 source/build_identity.py
python3 source/assemble_review.py
```

另附 XeLaTeX 合稿源，可在完整的 XeLaTeX、ctex、pdfpages、hyperref 环境中使用：

```bash
xelatex -interaction=nonstopmode -halt-on-error source/review.tex
xelatex -interaction=nonstopmode -halt-on-error source/review.tex
```

在资源包根目录执行。生成的 `review.pdf` 为6页评审稿。原版母标为文字轮廓资产，复制过程不依赖本机字体；新增组件的中英文字体和字体路径在生成器中声明，可通过 `OSDGS_FONT_*` 环境变量指定。

## 评审与待确认

1. 十维方形图标是否足够醒目，编号、名称和图形的层级是否清楚。
2. 四支柱辅助图形是否能概括各自含义；X4 采用“盾与心”表达规则保护与共同受益。
3. 五段主线的传播用语是否准确，相关观察入口是否适合报告导视。
4. 正式发布前确认小尺寸、印刷色彩和英文措辞。本稿不宣称新增标识已批准，不新增量化事实。

完整依据见 `evidence/SOURCES.md`。十维图形版权和许可见 `baseline/sources/lucide/LICENSE.txt`；项目主标的分发边界沿用 `baseline/RIGHTS.md`。本稿不新增第三方授权或机构背书主张。
