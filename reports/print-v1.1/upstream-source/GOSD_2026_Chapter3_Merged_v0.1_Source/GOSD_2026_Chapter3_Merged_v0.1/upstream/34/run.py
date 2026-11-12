from build import *
from section34 import render, SOURCES, G, CN, PURPOSE

ensure_fonts();export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
PAGES=render()
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
def refs(s):
    for source in SOURCES:
        # P7 is a methodology inventory, not a claim that a repository landing page proves every category.
        if source['id']!='P7':s=s.replace('［'+source['id']+'］',r'\href{'+source['url']+'}{［'+source['id']+'］}')
    return s
for i,p in enumerate(PAGES):
    tex+=rf'\begin{{canvas}}\Header{{第三章 · 全球开源影响力排行榜}}{{violet}}\Footer{{{i+1:02}}}'+'\n'
    tex+=box(15,27,180,p['title'],20,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
    tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
    tex+=refs(box(15,199,180,p['caption'],7.6,10.7,'muted',False,True))
    for j,(title,body) in enumerate(p['analyses']):
        x=15+(j%2)*93;y=214+(j//2)*34
        tex+=box(x,y,87,title,10.3,14.2,'violet',True)+box(x,y+6,87,body,9.9,15)
    tex+=r'\end{canvas}'+'\n'

# Self-contained local appendix; consolidates methods, traceable sources, and review status.
tex+=r'\begin{canvas}\Header{第三章 · 附录 1（本节摘录）}{violet}\Footer{05}'+'\n'
tex+=box(15,27,180,'附录 1　指标、证据与本轮评审说明',18.6,25,'ink',True)
tex+=box(15,40,180,'3.4 修订稿 v0.2 · 2026 年 11 月 10 日｜4 页正文、4 幅组合图；未提交 GitHub。',9.1,13,'muted',False,True)
items=[
 ('统计对象与时间','OpenRank 是协作网络影响指标，考虑协作连接及相连节点的重要性。本节按 OpenDigger 项目标签所覆盖的仓库汇总 2025-07-01 至 2026-06-30 的月度分值；当前映射复算与全球前 100 名、中国前 30 名的分值逐项一致。此次复算验证分值，不同时证明历史组织归属、许可或跨标签去重。'),
 ('参与规模与组织国别','参与账号沿用榜表 active_developers 字段，仅作参与规模对照；该字段的统计覆盖期、机器人处理及跨平台身份去重仍待独立复核。组织字段混合发起方和托管方，地图沿用其国别，不作为贡献者地理分布。全球百强有 9 项国别、10 项组织未识别，分别单列。'),
 ('技术与对象分类','依据项目官方入口，按主要用途单列一类；AI 辅助编程工具仍可归入开发工具，因此“AI 与机器学习”不是全部 AI 相关对象。软件项目指相对明确的软件入口，项目生态包含多个关联组件，项目集合为原榜聚合标签。组织类型按榜表名称归类，“企业及其他机构”不含基金会、高校及未知项。'),
 ('账号样本与接口案例','图 3-13 使用六仓库 12 个月的 activity_details.json；每仓每月至多 100 个账号，剔除空值、[bot] 及固定机器人标签表中的账号，按小写 login 去重。重叠指至少同月出现一次的去重账号；持续出现以年度并集为分母，不等于全量留存。接口案例仅证明官方文档列明的支持与配套，不表示所有组合兼容或已经规模采用。')]
y=52
for title,body in items:
    tex+=box(15,y,180,title,10.4,14,'violet',True)+box(15,y+6,180,body,8.9,13.1,'ink',False,True);y+=34
tex+=box(15,190,180,'可追溯来源（点击编号进入固定版本或数据入口）',10.4,14,'violet',True)
source_lines=[
 ('P1','报告全球项目百强 HTML，固定提交 c51e344；含名次、分值、参与账号、组织与国别。'),
 ('P2','报告中国项目前 30 名 CSV，同一固定提交；本轮复算明细及 SQL 随可编辑源稿保存。'),
 ('P3','OpenDigger 指标实现，固定提交 5c2ffc4；复算读取日期 2026-11-10。'),
 ('P4','六仓库账号数据：PyTorch、vLLM、SGLang、LangChain、Dify、Kubernetes；2026-11-10 重新取回复算，与 11-06 固定样本一致，原始数据和方法随源稿保留。'),
 ('P5','verl README，固定提交 38b5793（2026-05-29）；列举训练、生成、模型与硬件支持。'),
 ('P6','Ascend/pytorch README，固定提交 554f7cd（2026-06-16）；扩展定义及版本匹配表。'),
 ('P7','分类清单逐项记录官方 URL；前两幅图的项目名可点击进入对应官方文档，完整清单随源稿保留。')]
y=197
for id,body in source_lines:
    tex+=refs(box(15,y,180,'［'+id+'］ '+body,8,11.5,'muted',False,True));y+=7 if id!='P4' else 10
tex+=box(15,251,180,'变更与待核查项',10.4,14,'violet',True)
tex+=box(15,257,180,'本轮重构全球、中国、多维特征与跨项目连接四幅图，并收紧配套叙事。待核：历史项目—仓库映射及标签重叠、参与字段、组织身份和逐项许可；公开仓库不代表完整产品开源（如 Claude Code），n8n 等许可亦需单独判定。',8.5,12.3,'ink',False,True)
tex+=box(15,274,180,'评审重点：四图分工、信息密度与可读性，以及中国贡献的接口与维护叙事是否充分。',8.5,12.3,'violet',True)
tex+=r'\end{canvas}\end{document}'
(R/'report.tex').write_text(tex);(D/'content.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2));(D/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2))
(R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
compile_tex()
doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':'GOSD 2026 精要版｜3.4 全球开源项目影响力排行榜｜修订稿 v0.2','author':'全球开源发展报告编制组','subject':'2026-11-10；四幅A4竖版组合图；全球百强、中国项目、多维特征、跨项目连接；待评审'})
doc.set_toc([[1,p['title'],i+1] for i,p in enumerate(PAGES)]+[[1,'附录 1　指标、证据与本轮评审说明',5]])
# Directly link every displayed ranking name to the official classification evidence.
for pn,scope,data in [(0,'global',G),(1,'china',CN)]:
    evidence={r['project']:r['evidence'] for r in PURPOSE if r['scope']==scope}
    for i,row in enumerate(data[:20]):
        x,y,w,h=60,87+i*26-19,230,26;sc=180/1000*72/25.4
        rect=fitz.Rect(15*72/25.4+x*sc,53*72/25.4+y*sc,15*72/25.4+(x+w)*sc,53*72/25.4+(y+h)*sc)
        doc[pn].insert_link({'kind':fitz.LINK_URI,'from':rect,'uri':evidence[row['project']]})
out=O/'GOSD_2026_Section_3-4_Review_v0.2.pdf';doc.save(out,garbage=1,deflate=True);doc.close();doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.85,1.85)).save(R/'review'/f'page-{i+1}.png')
print('BUILT',out,len(doc));print(json.dumps(QA,ensure_ascii=False))
