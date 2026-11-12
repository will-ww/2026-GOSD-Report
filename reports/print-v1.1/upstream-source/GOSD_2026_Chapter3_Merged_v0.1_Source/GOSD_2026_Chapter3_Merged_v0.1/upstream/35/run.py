from build import *
from section35 import render,SOURCES,RP,PR,REF

ensure_fonts();export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
PAGES=render()
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
def refs(s):
    for source in SOURCES:s=s.replace('［'+source['id']+'］',r'\href{'+source['url'].replace('&',r'\&')+'}{［'+source['id']+'］}')
    return s.replace('［E6—E7］',r'\href{'+SOURCES[5]['url']+'}{［E6］}'+r'\href{'+SOURCES[6]['url']+'}{［E7］}')
for i,p in enumerate(PAGES):
    tex+=rf'\begin{{canvas}}\Header{{第三章 · 全球开源影响力排行榜}}{{violet}}\Footer{{{i+1:02}}}'+'\n'
    tex+=box(15,27,180,p['title'],20,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
    tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
    tex+=refs(box(15,199,180,p['caption'],7.6,10.7,'muted',False,True))
    for j,(title,body) in enumerate(p['analyses']):
        x=15+(j%2)*93;y=214+(j//2)*34
        tex+=box(x,y,87,title,10.3,14.2,'violet',True)+box(x,y+6,87,body,9.9,15)
    tex+=r'\end{canvas}'+'\n'
tex+=r'\begin{canvas}\Header{第三章 · 附录 1（本节摘录）}{violet}\Footer{04}'+'\n'
tex+=box(15,27,180,'附录 1　指标、证据与本轮评审说明',18.6,25,'ink',True)
tex+=box(15,40,180,'3.5 修订稿 v0.2 · 2026 年 11 月 10 日｜3 页正文、3 幅组合图；未提交 GitHub。',9.1,13,'muted',False,True)
items=[
 ('“新”与榜单范围','两榜各固定 30 个对象，正文列出前 20 位，结构统计覆盖全部 30 位。名录中的仓库创建时间、项目最早仓库时间位于主期内，但迁入、改名和拆分可能改变记录，不能据此断言技术诞生；新增资格及历史映射仍需逐项核验。本轮保留原榜名次，不将后续观察并入主期。'),
 ('分值、参与和分类','OpenRank 衡量协作网络中节点的影响；本节分值为 2025-07-01 至 2026-06-30 月度值之和。两榜“参与账号”沿用 active_developers 字段，其机器人与跨平台去重口径仍待独立核验。技术用途依据逐项官方入口作编辑分类；平台不等于国别，组织标签也不等于贡献者地理。'),
 ('CANN 完整范围与账号口径','按 OpenDigger 当前 CANN 项目标签，汇总 AtomGit 组织 ID 5162848 的主期记录；以仓库 ID 合并三组改名，得到 68 仓和 14,719.47 分，与原榜一致。协作账号来自去机器人归一化贡献表，主期按账号 ID 去重为 5,282 个；此口径有别于原榜 5,460 个参与账号，二者不互换。'),
 ('主期、期后与因果解释','68 仓是主期出现过的仓库并集；6 月 63 仓、10 月 90 仓是各月有 OpenRank 记录的仓库数。图中期后数据为 2026.07—10；官方首页功能与设施为 2026-11-10 观察。跨仓参与不等于跨企业或跨境贡献，按月重复出现也不等于连续留存。当前标签复算不证明所有历史映射始终不变。')]
y=52
for t,b in items:
    tex+=box(15,y,180,t,10.4,14,'violet',True)+box(15,y+6,180,b,8.9,13.1,'ink',False,True);y+=34
tex+=box(15,190,180,'可追溯来源（点击编号访问；明细与 SQL 随可编辑源稿保存）',10.4,14,'violet',True)
y=197
for s in SOURCES:
    tex+=refs(box(15,y,180,'［'+s['id']+'］ '+s['title'],8.1,11.6,'muted',False,True));y+=6.5
tex+=box(15,252,180,'修改内容、待核查项与评审重点',10.4,14,'violet',True)
tex+=box(15,258,180,'本轮将两榜拆为独立组合图，并把 CANN 八仓局部观察扩展为完整 68 仓、功能分层与期后走势。待核：新建资格、其他多仓项目完整映射、榜表参与字段及逐项许可；OpenShare 页面需登录，未取得页面数值，CANN 数值来自 OpenDigger 直接查询。',8.5,12.3,'ink',False,True)
tex+=box(15,275,180,'评审重点：三图分工与密度是否合适；CANN 是否充分连接“体系能力”与“AI 普惠”。',8.5,12.3,'violet',True)
tex+=r'\end{canvas}\end{document}'
(R/'report.tex').write_text(tex);(D/'content.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2));(D/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2));(R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
compile_tex()
doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':'GOSD 2026 精要版｜3.5 新势力仓库与项目｜修订稿 v0.2','author':'全球开源发展报告编制组','subject':'2026-11-10；新仓库、新项目与 CANN 多仓画像；待评审'})
doc.set_toc([[1,p['title'],i+1] for i,p in enumerate(PAGES)]+[[1,'附录 1　指标、证据与本轮评审说明',4]])
for pn,scope,ds,key in [(0,'repos',RP,'repo'),(1,'projects',PR,'project')]:
    for i,row in enumerate(ds[:20]):
        link=REF[scope][row[key]]['official_url'];x,y,w,h=56,87+i*26-19,280,26;sc=180/1000*72/25.4
        rect=fitz.Rect(15*72/25.4+x*sc,53*72/25.4+y*sc,15*72/25.4+(x+w)*sc,53*72/25.4+(y+h)*sc)
        doc[pn].insert_link({'kind':fitz.LINK_URI,'from':rect,'uri':link})
out=O/'GOSD_2026_Section_3-5_Review_v0.2.pdf';doc.save(out,garbage=1,deflate=True);doc.close();doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.85,1.85)).save(R/'review'/f'page-{i+1}.png')
print('BUILT',out,len(doc));print(json.dumps(QA,ensure_ascii=False))
