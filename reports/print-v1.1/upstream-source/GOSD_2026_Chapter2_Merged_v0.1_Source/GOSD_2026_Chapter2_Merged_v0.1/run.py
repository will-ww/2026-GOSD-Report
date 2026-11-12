from build import *
from chapter_pages import opening,closing,APPENDIX,SOURCES
from concurrent.futures import ThreadPoolExecutor
from fix_pdf_text import repair
import re

for p in [B/'assets',B/'fonts',B/'texmf-var',O,F,R/'review']:p.mkdir(parents=True,exist_ok=True)
ensure_fonts()
subprocess.run(['python3',str(R/'assemble_content.py')],check=True)
pages=json.loads((D/'content.json').read_text())
exports=[(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')]+[(F/(p['figure']+'.svg'),B/'assets'/(p['figure']+'.pdf')) for p in pages]
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(lambda v:export(*v),exports))
(R/'review/pdf-text-repairs.json').write_text(json.dumps([repair(v[1]) for v in exports[1:]],ensure_ascii=False,indent=2))
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'+opening()
for p in pages:
 tex+=rf'\begin{{canvas}}\Header{{第二章 · 全球开源生态地图}}{{teal}}\Footer{{{p["page"]:02}}}'+'\n'
 tex+=box(15,27,180,p['title'],21,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
 tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
 tex+=box(15,199,180,p['caption'],7.8,10.8,'muted',False,True)
 for j,(title,body) in enumerate(p['analyses']):
  if len(p['analyses'])==3 and j==2:x=15;y=247;w=180
  else:x=15+(j%2)*93;y=211+(j//2)*34;w=87
  tex+=box(x,y,w,title,10.5,14.2,'teal',True)+box(x,y+6,w,body,10.1,15.6)
 tex+=r'\end{canvas}'+'\n'
tex+=closing()+''.join(f() for f in APPENDIX)+r'\end{document}'
(R/'report.tex').write_text(tex)
(D/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2))
compile_tex()
raw=fitz.open(O/'report.pdf')
assert len(raw)==27,len(raw)
raw.set_metadata({'title':'GOSD 2026 精要版｜第二章合稿与附录 A｜v0.1','author':'全球开源发展报告编制组','subject':'六节合稿；2.5 采用 v0.3；期后行业专题编为 2.6；待作者评审','keywords':'GOSD, OpenDigger, OpenRank, 全球开源生态地图, AI 普惠'})
toc=[[1,'第二章 全球开源生态地图',1]]
seen=set()
for p in pages:
 level=2 if p['section'] not in seen else 3;seen.add(p['section']);toc.append([level,p['title'],p['page']])
toc+=[[2,'本章小结：启示与行动方向',21],[1,'附录 A 第二章方法与证据',22]]
an=['指标与统计覆盖','历史与情景方法','贡献与影响情景读数','样本与资产口径','行业专题方法','来源索引']
toc += [[2,title,22+i] for i,title in enumerate(an)]
raw.set_toc(toc)
raw.set_page_labels([{'startpage':0,'prefix':'','style':'D','firstpagenum':1},{'startpage':21,'prefix':'A','style':'D','firstpagenum':1}])
# Clickable chapter contents: exact destinations in the assembled PDF.
for i,dst in enumerate([1,4,8,11,13,17]):
 raw[0].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(15*72/25.4,(126+i*17)*72/25.4,195*72/25.4,(141+i*17)*72/25.4),'page':dst})
# Caption links keep the full report self-contained while allowing quick methods navigation.
for p in pages:
 match=re.search('附录 A([1-6])',p['caption'])
 if match:
  raw[p['page']-1].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(15*72/25.4,199*72/25.4,195*72/25.4,209*72/25.4),'page':20+int(match.group(1))})
out=O/'GOSD_2026_Chapter2_Merged_Review_v0.1.pdf'
raw.save(out,garbage=4,deflate=True);raw.close()
full=fitz.open(out);ap=fitz.open();ap.insert_pdf(full,from_page=21,to_page=26,links=True)
ap.set_metadata({'title':'GOSD 2026 精要版｜第二章附录 A｜v0.1','author':'全球开源发展报告编制组','subject':'指标、覆盖、情景、样本与来源；待作者评审'})
ap.set_toc([[1,title,i+1] for i,title in enumerate(an)])
ap.set_page_labels([{'startpage':0,'prefix':'A','style':'D','firstpagenum':1}])
ap.save(O/'GOSD_2026_Chapter2_Appendix_A_Review_v0.1.pdf',garbage=4,deflate=True);ap.close()
for i,p in enumerate(full):p.get_pixmap(matrix=fitz.Matrix(1.35,1.35)).save(R/'review'/f'page-{i+1:02}.png')
print('BUILT',out,'pages',len(full),'appendix',6)
