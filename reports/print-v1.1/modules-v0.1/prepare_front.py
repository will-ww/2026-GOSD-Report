from pathlib import Path
import re
R=Path(__file__).resolve().parent
p=R/'frontmatter/build_front.py'
s=(R.parent/'front-v0.8/build_front.py').read_text()
# Roman folios count the unprinted verso after the contents page.
for title,old,new in [('执行摘要','viii','ix'),('从证据到行动','ix','x'),('全书结构与阅读路径','x','xi'),('如何读懂一页综合图','xi','xii'),('引言','xii','xiii'),('合作宣言 · 核心原则','xiii','xiv'),('合作宣言 · 共创未来','xiv','xv')]:
 s=re.sub(r"(s=start\('"+re.escape(title)+r"','[^']*',)'"+old+r"'",r"\1'"+new+"'",s)
s=s.replace("('执行摘要','viii—ix')","('执行摘要','ix—x')").replace("('全书结构与阅读路径','x')","('全书结构与阅读路径','xi')").replace("('如何读懂一页综合图','xi')","('如何读懂一页综合图','xii')").replace("('引言与国际合作宣言','xii—xiv')","('引言与国际合作宣言','xiii—xv')")
s=s.replace("'行政区划 · 企业 · 基金会 · 项目 · 模型'","'行政区划 · 企业 · 基金会 · 项目 · 新势力 · 模型'")
s=s.replace("for j,(n,t,b,pg) in enumerate(toc):", "for j,(n,t,b,pg) in enumerate(toc):\n pg=str([1,13,35,59,75,89][j])")
s=s.replace("txt(36,y+2.1,93,t,10.3", "txt(36,y+2.1,81,t,10.3").replace("txt(36,y+8.5,93,b,7.6", "txt(36,y+8.5,92,b,7.25")
s=s.replace("s+=txt(15,267,119,'附录　指标、方法与数据来源  ｜  致谢',8.8,13.5,'navy',True,mh=8)", "s+=txt(120,y+2.2,9,pg,9.5,14,'navy',True,False,r'\\raggedleft ',mh=7)\ns+=txt(15,266.5,104,'附录　指标、方法与数据来源',8.8,13.5,'navy',True,mh=7)+txt(120,266.5,9,'97',9,13.5,'navy',True,False,r'\\raggedleft ',mh=7)\ns+=txt(15,273.3,104,'致谢 / Acknowledgements',8.5,12,'navy',mh=6)+txt(120,273.3,9,'117',9,12,'navy',True,False,r'\\raggedleft ',mh=6)")
# Page number for every chapter row, not just the last iteration.
s=s.replace("\ns+=txt(120,y+2.2", "\n s+=txt(120,y+2.2")
s=s.replace('地图看位置，榜单找主体，结构与份额揭示差异。','规模看积累，周线看变化，地图与份额看地域结构。')
s=s.replace('平台总量、地域样本与累计下载各有口径，分别解释。','主期增量、期后总量与地域样本分别解释，不混为同一总体。')
s=s.replace("('B',166,142", "('B',158,142").replace("('C',222,201", "('C',225,201")
p.write_text(s)
print('Prepared print contents, folios, and current figure 5-1 reading guide')
