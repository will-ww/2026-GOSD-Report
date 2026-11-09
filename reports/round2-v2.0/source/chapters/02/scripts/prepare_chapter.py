from pathlib import Path
import re,json,shutil,hashlib
R=Path(__file__).resolve().parents[1]
s=(R/'provenance/chapter2_original.tex').read_text()
# Retain complete sources and original stable citation numbers.
ledger=[]
for m in re.finditer(r'\\bibitem\[([^]]+)\]\{([^}]+)\} (.+?)\s*\\href\{([^}]+)\}\{来源入口\}。',s):
 ledger.append(dict(label=m[1],key=m[2],description=m[3],url=m[4]))
assert len(ledger)==49
refs={x['key']:x for x in ledger}
(R/'provenance/source_ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
# Only chapter body through final observed practice; the original back matter is archived intact.
body=s[s.index('\\renewcommand{\\CurrentSection}{2.1'):s.index('\\renewcommand{\\CurrentSection}{第二章\\quad 综合观察}')]
removed=[]
for lab in ['22-6','22-7','25-3','25-4']:
 pat=r'\\label\{ch2-unit'+lab+r'\}.*?(?=\\label\{ch2-unit|\\renewcommand\{\\CurrentSection\}|\Z)'
 m=re.search(pat,body,re.S);assert m,lab
 removed.append({'unit':lab,'reason':'来源前十表在2.6展开，完整明细归档' if lab.startswith('22') else '未验证的结构外推转入方法留档，不作为本章观测发现','content':m[0]})
 body=body[:m.start()]+body[m.end():]
# Established pilot corrections, reused as candidate copy edits in this chapter review.
repl=json.loads((R/'provenance/editorial_replacements.json').read_text())
for a,b in repl.items():
 if a in body:body=body.replace(a,b)
body=body.replace('编制组确认的约120万本土平台补充量','编制组登记的约120万本土平台补充量')
body=body.replace('约120万沿用编制组确认记录','约120万沿用编制组登记记录')
body=body.replace('地图说明贡献来自哪里，下一页再比较这些来源在各自样本中占多少。','地图说明贡献来自哪里；各来源的份额与已列跨境构成，集中在2.6节比较。')
body=body.replace('2.2已说明中美项目的本土与跨境结构。本节沿用同一来源前十表，进一步观察已列海外贡献由谁构成：','2.2已呈现中美项目的贡献连接。本节沿用同一来源前十表，比较本土与跨境份额，并观察已列海外贡献由谁构成：')
body=body.replace('资产地图由此先观察代码供给，再看模型与数据。官方研究解释平台变化，本报告样本补充地域与用途结构；技术分类估算则单独标识，用于探索结构，不作为已测得的类别事实。','资产地图由此先观察代码供给，再看模型与数据。平台官方观察与本报告发布单位样本分别呈现活动、供给与使用结构，采用各自的对象清单和时间窗口。')
body=body.replace('主统计期的年度新增量','主统计期的年度新增量')
body=body.replace('文件存在不等于规则有效执行，未检出也可能是材料位于网站或基金会文档。','未检出也可能是材料位于网站或基金会文档。')
body=body.replace('本图保留同一零起点纵轴和每年的读数，避免用不同尺度夸大某类增长。它描述所列样本，不据此计算全球许可覆盖率，也不把历史报告中的不同范围统计拼入本表。','五条序列采用相同纵轴，适合比较本样本的规模与路径；全球许可覆盖仍需更完整的仓库清单与一致的识别规则。')
body=body.replace('较大规模未必对应较高平均贡献','较大规模未必对应较高平均贡献')
# Remove immediate duplicated source sentence, keep actual reference close to figure.
body=body.replace('\\src{五域沿用固定比较组，窗口为2025年7月至2026年6月；与2025自然年地理快照分别阅读。}','')
# Compact dense section intros so navigation does not squeeze the evidence.
body=body.replace('开发者参与可以表现为提出问题、改进代码、审阅修改或维护版本。人数告诉我们有多少人进入生态，贡献地图进一步观察这些工作在哪里汇聚、与哪些项目相连。全球分布、五域变化、中国区域与项目来源，共同构成本节的四个观察层次。','贡献地图观察改进代码、审阅修改与维护等协作工作在哪里汇聚、与哪些项目相连，由全球分布进入五域变化、中国区域和项目来源。')
body=body.replace('本节沿用数据源的“开发者OpenRank贡献度”。它根据协作关系衡量网络中的贡献位置，不是代码行数或提交次数的简单合计，也不是对个人能力的评分。规模、平均值与来源关系分别提供不同线索。','本节沿用源表“开发者OpenRank贡献度”，观察协作网络中的贡献位置。总量、平均值与来源关系分别提供线索，不视为个人能力评分。')
body=body.replace('稳定的开源项目需要人的长期投入。人才地图将视角从项目转向参与者，观察高影响力群体在全球、五域及中国城市的分布，并区分已有规模、净增人数与相对增幅。','人才地图转向高影响力参与者，观察全球、五域及中国城市的分布，分别比较规模、净增与增幅。')
body=body.replace('样本沿用源表“个人全域OpenRank前5\\%”的定义，反映协作网络位置，而非完整的人才能力评价。前5\\%的比较总体、得分窗口和并列处理仍待核验，因此人数变化也不能直接解释为培养成效。','样本沿用“个人全域OpenRank前5\\%”。筛选总体、得分窗口和并列规则仍待核；本节观察网络位置，不作完整能力评价，也不将人数变化解释为培养成效。')
body=body.replace('前五节分别观察参与、贡献、项目、人才与资产。多样性地图进一步询问：这些活动由哪些来源构成，哪些技术社区正在扩张，合作是否连接多个地区。本节聚焦有定义、有来源的维度，不构造笼统的多样性总分。','从参与、贡献、项目、人才与资产出发，本节进一步观察来源构成、技术选择与跨地域连接，分别呈现有明确范围的多样性。')
# Section opens carry the registered dimensions as reading navigation, not claimed measurement coverage.
for i in range(1,8):
 pattern=r'(\\section\*\{2\.'+str(i)+r' [^}]+\})'
 body=re.sub(pattern,r'\\noindent\\includegraphics[width=\\linewidth]{figures/new/nav_2'+str(i)+r'.pdf}\\par\\vspace{3pt}\n\1',body,count=1)
# Restore clear source windows on continuation charts.
extra={
 'ch2-s21-tempo':'2022—2026报告年度；年度累计与当期活跃按原表定义分别比较。',
 'ch2-s21-five':'独立五域汇总，2025-07-01至2026-06-30；覆盖不同于GitHub地理表。',
 'ch2-s21-growth':'2022—2026报告年度；五域固定比较组，相对变化均以自身起点为基准。',
 'ch2-s24-five-trend':'五域报告年度序列，2022—2026；与2026年7月全球快照分开阅读。',
 'ch2-s24-five-change':'同比为2026较2025报告年度；五域筛选规则沿用归档，细节待核。',
 'ch2-s24-city-growth':'中国固定十城，2022—2026报告年度；净增由两期人数相减。'
}
for lab,note in extra.items():
 marker='\\label{'+lab+'}\\end{minipage}\\par\\vspace{4pt}'
 assert marker in body,lab
 body=body.replace(marker,marker+'\n\\src{'+note+'}')
# All production prose is kept separately, source links replace a bulky terminal bibliography.
def citations(t):
 def f(m):
  out=[]
  for key in m[1].split(','):
   q=refs[key];url=q['url'].replace('%','\\%')
   out.append('\\SourceCite{'+url+'}{'+q['label']+'}')
  return ''.join(out)
 return re.sub(r'\\cite\{([^}]+)\}',f,t)
body=citations(body)
body=re.sub(r'(\\clearpage\s*){2,}',r'\\clearpage\n',body)
(R/'content/chapter2_body.tex').write_text(body)
(R/'provenance/relocated_units.json').write_text(json.dumps(removed,ensure_ascii=False,indent=2))
# Ledger of figures used in the new flow. Numbering is regenerated continuously.
figs=[]
for m in re.finditer(r'\\captionof\{figure\}\{(.+?)\}\\label\{([^}]+)\}',body):figs.append({'new_number':f'2-{len(figs)+1}','title_tex':m[1],'stable_label':m[2]})
(R/'review/figure_index.json').write_text(json.dumps(figs,ensure_ascii=False,indent=2))
manifest={str(p.relative_to(R/'modules/02/data')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'modules/02/data').rglob('*') if p.is_file()}
(R/'review/data_fingerprints.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
# Page-level structured copy for future Web synchronization.
units=[]
for block in body.split('\\clearpage'):
 if block.strip():units.append({'tex':block.strip(),'figures':re.findall(r'\\includegraphics\[[^]]+\]\{([^}]+)\}',block)})
(R/'content/chapter2_units.json').write_text(json.dumps(units,ensure_ascii=False,indent=2))
print('sources',len(ledger),'figures',len(figs),'original data files',len(manifest),'relocated',len(removed))
