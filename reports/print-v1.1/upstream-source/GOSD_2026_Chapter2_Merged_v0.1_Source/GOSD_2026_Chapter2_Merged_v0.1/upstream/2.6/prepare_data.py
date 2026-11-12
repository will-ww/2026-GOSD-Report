from pathlib import Path
import csv,json,fitz,hashlib,numpy as np
R=Path(__file__).resolve().parent;D=R/'data';S=D/'source'
def load(n):return list(csv.DictReader((S/n).open()))
counts=load('sector_counts_by_year.csv'); overall=load('overall_ai_mentions_by_year.csv'); ai=load('sector_ai_mentions_2025.csv')
print('AI columns',ai[0].keys());print('overall columns',overall[0].keys())
# Recover plotted values from the supplied vector figure, calibrated against its
# five dashed overall values. Verify count integrality and 2025 summary agreement.
p=fitz.open(R/'evidence/figure3_sector_trends.pdf')[0]
paths=[d for d in p.get_drawings() if len(d['items'])==4 and all(x[0]=='l' for x in d['items'])]
assert len(paths)==12
series=[];errors=[]
for i,code in enumerate(['54','52','51','31-33','62','22']):
 ref=paths[2*i];line=paths[2*i+1]
 gety=lambda d:np.array([d['items'][0][1].y]+[a[2].y for a in d['items']])
 yref=gety(ref); vals=np.array([float(a['pct']) for a in overall]); k,b=np.polyfit(yref,vals,1)
 decoded=k*gety(line)+b
 for j,year in enumerate(range(2021,2026)):
  n=int(counts[j][code]); raw=decoded[j]*n/100;num=round(raw);pct=num/n*100
  assert abs(raw-num)<0.0001,(code,year,raw)
  series.append(dict(year=year,code=code,mentions=num,count=n,pct=pct,vector_decoded_pct=float(decoded[j]),count_rounding_error=float(abs(raw-num))))
  errors.append(abs(raw-num))
with (D/'sector_ai_trends_recovered.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=series[0].keys());w.writeheader();w.writerows(series)
for row in series:
 if row['year']==2025:
  a=next(x for x in ai if x['code']==row['code']);assert int(a['sum'])==row['mentions'];assert int(a['count'])==row['count']
meta=json.loads((S/'analysis_metadata.json').read_text())
assert sum(int(r['count']) for r in overall)==18086
assert sum(int(r['sum']) for r in ai)==836
assert sum(int(r['count']) for r in ai)==3461
metrics={'source_figure_sha256':hashlib.sha256((R/'evidence/figure3_sector_trends.pdf').read_bytes()).hexdigest(),'recovery_max_count_error':max(errors),'recovered_series':6,'recovered_points':30,'validation':'All recovered numerators are unique integers within 0.0001; all six 2025 endpoints match the supplied CSV. Curves are creation-cohort comparisons, not historical metadata.'}
(D/'recovery_provenance.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2));print(metrics)
