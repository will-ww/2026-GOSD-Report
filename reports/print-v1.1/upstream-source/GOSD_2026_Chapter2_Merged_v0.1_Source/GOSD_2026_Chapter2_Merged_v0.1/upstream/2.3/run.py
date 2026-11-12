from build import *
from figures_content import render_all
from content import make_tex

for p in [B/'assets',B/'fonts',B/'texmf-var',O,F,R/'review']:p.mkdir(parents=True,exist_ok=True)
ensure_fonts()
export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
render_all();make_tex();compile_tex()
doc=fitz.open(O/'report.pdf')
doc.set_metadata({'title':'GOSD 2026 精要版｜2.3 全球开源项目影响地图 v0.3','author':'全球开源发展报告编制组','subject':'三页 A4 竖版综合图文；附录1口径与来源补充；待作者 PDF 评审'})
doc.set_toc([[1,'2.3 全球开源项目影响地图',1],[2,'项目影响的增长与长期情景',2],[2,'中国项目：结构与增长',3],[1,'附录1 指标、时期与情景方法',4],[2,'数据出处与评审记录',5]])
out=O/'GOSD_2026_Section_2-3_Review_v0.3.pdf';doc.save(out,garbage=4,deflate=True)
doc.close();doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.7,1.7)).save(R/'review'/f'page-{i+1}.png')
print('BUILT',out,len(doc))
