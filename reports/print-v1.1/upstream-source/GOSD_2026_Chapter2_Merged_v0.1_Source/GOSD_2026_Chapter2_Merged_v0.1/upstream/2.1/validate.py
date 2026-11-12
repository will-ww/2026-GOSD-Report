from pathlib import Path
import json, math, hashlib, csv, subprocess
import fitz
R=Path(__file__).resolve().parent
D=R/'data';O=R/'output'
world=json.loads((D/'public-developers.json').read_text());cn=json.loads((D/'public-CN-developers.json').read_text());meta=json.loads((D/'public-meta.json').read_text());sc=json.loads((D/'scenarios-v03.json').read_text())
assert meta['period']=={'reportYear':2026,'start':'2025-07-01','endExclusive':'2026-07-01','totalSnapshotQuarter':2}
assert sc['groups']['中国']['history'][-1]==454.534
assert sc['china_cross_platform_current_approx_10k']==370
assert abs(sum(r['value'] for r in cn['leaderboards'][1]['data'])-world['trends'][2]['values'][-1])<.1
assert abs(sum(r['change'] for r in cn['leaderboards'][1]['data'])-(world['trends'][2]['values'][-1]-world['trends'][2]['values'][-2]))<.1
archive=D/'global_report_year_trend.csv'
rows=list(csv.DictReader(archive.open()))
for j,key in enumerate(['developers_total','active_developers','china_active_github']):
 assert all(math.isclose(float(r[key]),v,rel_tol=0,abs_tol=.01) for r,v in zip(rows,world['trends'][j]['values']))
for s in list(sc['groups'].values())+list(sc['global_and_china'].values()):
 g=(s['history'][-1]/s['history'][0])**.25-1
 assert math.isclose(g,s['annual_growth'])
 assert math.isclose(s['history'][-1]*(1+g)**4,s['continued'][-1])
 assert math.isclose(s['history'][-1]*math.prod(1+g*.8**h for h in range(1,5)),s['slowing'][-1])
qa=json.loads((R/'review/figure-qa.json').read_text());assert all(not q['out_of_bounds'] and not q['overlaps'] for q in qa)
pdf=O/'GOSD_2026_Chapter2_Portrait_v0.3.pdf';doc=fitz.open(pdf);assert len(doc)==5
pages=[]
for i,p in enumerate(doc):
 assert p.rect.width < p.rect.height
 assert abs(p.rect.width-595.276)<.2 and abs(p.rect.height-841.89)<.2
 p.get_pixmap(matrix=fitz.Matrix(1.7,1.7),alpha=False).save(O/f'page-{i+1}.png')
 txt=p.get_text();assert '\ufffd' not in txt
 for blk in p.get_text('dict')['blocks']:
  for line in blk.get('lines',[]):
   for span in line['spans']:
    box=fitz.Rect(span['bbox']);assert box.x0>=30 and box.x1<=565 and box.y0>=15 and box.y1<=823,(i,span)
 pages.append({'page':i+1,'size_pt':[p.rect.width,p.rect.height],'text_chars':len(txt)})
text='\n'.join(p.get_text() for p in doc)
assert '350' not in text
assert '370' in text and '454.5' in text and '250.48' in text
log=(O/'report.log').read_text();assert 'Missing character:' not in log and 'Overfull' not in log
fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True);(R/'review/font-check.txt').write_text(fonts)
for line in fonts.splitlines()[2:]:
 parts=line.split();assert parts[-5]=='yes',line
sources=[]
for n,u in [('public-meta.json','https://selfoss.open-digger.cn/openshare/overview_half_year/meta.json'),('public-developers.json','https://selfoss.open-digger.cn/openshare/overview_half_year/developers.json'),('public-CN-developers.json','https://selfoss.open-digger.cn/openshare/overview_half_year/CN/developers.json')]:
 sources.append({'file':'data/'+n,'url':u,'retrieved':'2026-11-09','sha256':hashlib.sha256((D/n).read_bytes()).hexdigest()})
report={'version':'0.3','status':'待作者评审','pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'portrait_pages':pages,'sources':sources,'numeric_checks':'Passed: same-window global/China history, province sums, eight scenarios and rounding','svg_labels':'No out-of-bounds or overlaps detected','fonts':'All fonts embedded; no missing glyph warnings','github_write':False,'pending':['五域欧洲成员清单与历史覆盖执行记录','地图出版规范','情景参数与竖版密度待作者评审']}
(R/'review/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
