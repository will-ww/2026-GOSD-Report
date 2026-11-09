from pathlib import Path
import fitz,re,json,hashlib
R=Path(__file__).resolve().parent; ROOT=R.parent; OUT=R/'output'; OUT.mkdir(exist_ok=True)
front=R/'front/work/report.pdf'
inputs=[front]+[next((ROOT/'full_inputs').glob(f'*第{x}章*.pdf')) for x in ['二','三','四','五']]+[next((ROOT/'ch6_appendix_v0.2/output').glob('*.pdf'))]
back=ROOT/'ch6_appendix_v0.2/figures/new/full_report_back_cover.pdf'
doc=fitz.open(); toc=[];manifest=[];footer_log=[]
fontfile='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
font=fitz.Font(fontfile=fontfile)
for part,f in enumerate(inputs):
 src=fitz.open(f);off=len(doc)
 if part==0:assert len(src)==27,len(src)
 if part==5:assert len(src)==19,len(src)
 manifest.append({'part':part,'file':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'pages':len(src),'start_page':off+1,'end_page':off+len(src)})
 doc.insert_pdf(src)
 st=src.get_toc()
 if part==4:
  st=[x for x in st if x[0]<3]
  st += [[2,'5.1 供给与贡献',3],[2,'5.2 网络与影响力',7],[2,'5.3 开放条件与分级',12]]
  st.sort(key=lambda x:x[2])
 if part==5:
  if not any(x[1]=='附录 A 指标体系与数据来源'for x in st):st += [[1,'附录 A 指标体系与数据来源',11]]
  st.sort(key=lambda x:(x[2],x[0]))
 for lv,title,p in st:
  if '回望' in title:lv=2
  toc.append([lv,title,p+off])
 # Replace only existing footer number spans. Graphic plates/covers retain their artwork.
 if part:
  for j in range(len(src)):
   if j==0:continue
   p=doc[off+j];spans=[s for b in p.get_text('dict')['blocks']if b['type']==0 for l in b['lines']for s in l['spans']]
   hits=[s for s in spans if s['text'].strip().isdigit() and s['size']<16 and s['bbox'][1]>.91*p.rect.height and s['bbox'][0]>.8*p.rect.width]
   assert len(hits)<=1,(part,j,hits)
   if not hits:continue
   s=hits[0];old=s['text'].strip();assert int(old)==j+1,(part,j,old)
   rect=fitz.Rect(s['bbox']);p.add_redact_annot(rect,fill=(1,1,1))
   p.apply_redactions(images=0,graphics=0)
   n=str(off+j+1);sz=s['size'];right=rect.x1
   p.insert_font(fontname='GlobalPage',fontfile=fontfile)
   p.insert_text((right-font.text_length(n,fontsize=sz),s['origin'][1]),n,fontsize=sz,fontname='GlobalPage',color=(.106,.176,.251))
   footer_log.append({'page':off+j+1,'old':old,'new':n,'bbox':list(rect)})
doc.insert_pdf(fitz.open(back));toc.append([1,'封底',len(doc)])
assert len(doc)==173,len(doc)
# Make all section labels and page numbers in the printed contents clickable.
expected=json.loads((R/'toc_expected.json').read_text());linklog=[]
for pi in [2,3]:
 p=doc[pi]
 lines=[l for b in p.get_text('dict')['blocks'] if b['type']==0 for l in b['lines']]
 for l in lines:
  txt=''.join(s['text']for s in l['spans']).strip()
  if txt in expected:
   y=fitz.Rect(l['bbox']);rec=fitz.Rect(62,y.y0-1,p.rect.width-60,y.y1+2)
   p.insert_link({'kind':fitz.LINK_GOTO,'from':rec,'page':expected[txt]-1,'to':fitz.Point(0,0)})
   linklog.append({'section':txt,'target':expected[txt],'toc_page':pi+1})
 # Appendix and acknowledgements are unnumbered rows.
 for text,page in [('指标体系与数据来源',164),('致谢',171)]:
  for rect in p.search_for(text):
   rec=fitz.Rect(62,rect.y0-1,p.rect.width-60,rect.y1+2)
   p.insert_link({'kind':fitz.LINK_GOTO,'from':rec,'page':page-1,'to':fitz.Point(0,0)})
   linklog.append({'section':text,'target':page,'toc_page':pi+1})
assert {x['section']for x in linklog}>=set(expected),linklog
doc.set_toc(toc)
doc.set_page_labels([{'startpage':0,'prefix':'','style':'D','firstpagenum':1}])
doc.set_metadata({'title':'2026全球开源发展报告｜第二轮整合评审稿 v2.0','author':'《2026全球开源发展报告》编制组','subject':'前置内容、六章、附录A、致谢与封底；主统计期2025-07-01至2026-06-30；评审稿，未公开发布','keywords':'GOSD 2026, OSDGs, OpenRank, ModelRank, 第二轮评审','creator':'XeLaTeX / GOSD 动态星座视觉体系 v2.0.0','producer':'GOSD structured review pipeline'})
path=OUT/'GOSD_2026_全书_第二轮整合_v2.0_评审稿.pdf'
doc.save(path,garbage=4,deflate=True)
(R/'assembly_manifest.json').write_text(json.dumps({'version':'v2.0','total_pages':len(doc),'parts':manifest,'back_cover':str(back.relative_to(ROOT)),'footer_replacements':footer_log,'contents_links':linklog,'toc':toc},ensure_ascii=False,indent=2))
print(json.dumps({'file':str(path),'pages':len(doc),'bytes':path.stat().st_size,'bookmarks':len(toc),'contents_links':len(linklog)},ensure_ascii=False))
