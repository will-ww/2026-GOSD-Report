"""Verification of the assembled chapter, scenario arithmetic and PDF integrity."""
from pathlib import Path
import json,math,re,hashlib,xml.etree.ElementTree as ET
import fitz
R=Path(__file__).resolve().parent
P=json.loads((R/'data/content.json').read_text())
issues=[];checks={};mm=72/25.4
pdf=fitz.open(R/'output/GOSD_2026_Chapter2_Merged_Review_v0.1.pdf')
ap=fitz.open(R/'output/GOSD_2026_Chapter2_Appendix_A_Review_v0.1.pdf')
checks['pages']={'full':len(pdf),'body':21,'appendix':len(ap),'figures':len(P)}
assert len(pdf)==27 and len(ap)==6 and len(P)==19
for i,p in enumerate(pdf):
 assert abs(p.rect.width-210*mm)<.05 and abs(p.rect.height-297*mm)<.05
 for b in p.get_text('dict')['blocks']:
  for l in b.get('lines',[]):
   for s in l['spans']:
    x0,y0,x1,y1=s['bbox']
    if x0<12*mm or x1>198*mm or y0<6*mm or y1>293*mm:issues.append(['page_bounds',i+1,s['text']])
 if any(ord(c)<32 and c not in '\n\r\t' for c in p.get_text()):issues.append(['text_encoding',i+1])
for i in range(6):
 assert ap[i].get_text()==pdf[21+i].get_text()
 assert ap[i].get_pixmap(matrix=fitz.Matrix(.7,.7)).samples==pdf[21+i].get_pixmap(matrix=fitz.Matrix(.7,.7)).samples
checks['appendix_matches_full']=True
checks['links']=sum(len(p.get_links()) for p in pdf)
for p in pdf:
 for link in p.get_links():
  if link['kind']==fitz.LINK_GOTO:assert 0<=link['page']<27
checks['bookmarks']=len(pdf.get_toc())
checks['fonts_embedded']=all(bool(pdf.extract_font(x[0])[3]) for p in pdf for x in p.get_fonts())
assert checks['fonts_embedded']
checked=[]
for i,p in enumerate(P,1):
 old=R/'upstream'/p['section']/'figures'/(p['upstream_figure']+'.svg');new=R/'figures'/(p['figure']+'.svg')
 def numeric_texts(path):
  return [re.findall(r'\d+(?:[,.]\d+)*',n.text or '') for n in ET.parse(path).iter() if n.tag.endswith('text')]
 assert numeric_texts(old)==numeric_texts(new),(i,'numeric labels changed')
 assert p['figure_id']==f'2-{i}' and p['page']==i+1
 text=pdf[p['page']-1].get_text().replace(' ','').replace('\n','').replace('‑','-')
 assert f'图2-{i}' in text,(i,'caption missing')
 checked.append(p['figure_id'])
checks['unchanged_figure_numeric_labels']=checked
scenario_inputs=[('2.1','scenarios-v03.json',['groups','global_and_china']),('2.2','scenarios-v02.json',['five_group_report_years','natural_years']),('2.3','derived-v01.json',['five_domain_scenarios','natural_year_scenarios'])]
sc=[]
for sec,name,keys in scenario_inputs:
 d=json.loads((R/'upstream'/sec/'data'/name).read_text())
 for key in keys:
  for region,v in d[key].items():
   start,end=v['history'][0],v['history'][-1];g=(end/start)**.25-1
   slow=end
   for h in range(1,len(v['continued'])+1):
    continued=end*(1+g)**h;slow*=1+g*.8**h
    assert math.isclose(continued,v['continued'][h-1],rel_tol=1e-10),(sec,key,region,h)
    assert math.isclose(slow,v['slowing'][h-1],rel_tol=1e-10),(sec,key,region,h)
   sc.append([sec,key,region,len(v['continued'])])
checks['scenario_series_recomputed']=sc
log=(R/'output/report.log').read_text()
checks['layout_warnings']=re.findall(r'.*(?:Overfull|Missing character|Error).*',log)
assert not checks['layout_warnings']
checks['issues']=issues
checks['status']='pass' if not issues else 'needs_review'
(R/'review/verification.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
print(json.dumps({'status':checks['status'],'pages':checks['pages'],'scenario_series':len(sc),'links':checks['links'],'fonts_embedded':checks['fonts_embedded'],'issues':issues},ensure_ascii=False))
assert not issues
