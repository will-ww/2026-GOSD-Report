from build import *
from figures_content import render_all
from content_v03 import make_tex

for p in [B/'assets',B/'fonts',B/'texmf-var',O,F,R/'review']:p.mkdir(parents=True,exist_ok=True)
from fontTools.ttLib import TTCollection
for family in ['Sans','Serif']:
    for weight in ['Regular','Bold']:
        dest=B/'fonts'/f'Noto{family}CJKsc-{weight}.otf'
        if not dest.exists():
            coll=TTCollection(f'/usr/share/fonts/opentype/noto/Noto{family}CJK-{weight}.ttc');coll.fonts[2].save(dest);coll.close()
export(R/'assets/osdgs-symbol-compact.svg', B/'assets/osdgs-compact.pdf')
render_all();make_tex();compile_tex()
doc=fitz.open(O/'report.pdf')
doc.set_metadata({'title':'GOSD 2026 精要版｜2.2 全球开源贡献地图 v0.3','author':'全球开源发展报告编制组','subject':'四页A4竖版综合图文；附录1口径与来源补充；待作者PDF评审'})
doc.set_toc([[1,'2.2 全球开源贡献地图',1],[2,'贡献增长与 2030 情景',2],[2,'中国贡献：规模、结构与平均',3],[2,'全球协作：从参与到共同建设',4],[1,'附录1 指标与情景方法',5],[2,'历史与2030情景、出处及评审记录',6]])
out=O/'GOSD_2026_Section_2-2_Review_v0.3.pdf';doc.save(out,garbage=4,deflate=True)
doc.close();doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(R/'review'/f'page-{i+1}.png')
print('BUILT',out,len(doc))
