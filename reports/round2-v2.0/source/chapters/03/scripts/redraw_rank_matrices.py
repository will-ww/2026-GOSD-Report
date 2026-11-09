from pathlib import Path
import csv,json,base64,html,hashlib
from PIL import Image
from svgkit import SVG,QA
R=Path(__file__).resolve().parents[1];S=R/'sources/s3.2/ch32_v03';D=S/'data'
man=json.loads((S/'sources/company-logos-manifest.json').read_text())
keys={}
for p in D.glob('table*csv'):
 for r in csv.DictReader(p.open()):keys[r['company_zh']]=r['company']
ACC='#6146A5';colors=['#513786','#7960AA','#C1B1DB','#E4DCF0','#EEF0F3','#F7F8F9'];labels=['第1','第2—3','第4—10','第11—30','第31—100','第101及以后'];limits=[1,3,10,30,100,100000]
records=[]
def cellcolor(v):return colors[next(i for i,t in enumerate(limits) if v<=t)]
def logo(s,name,x,y,w=5,h=5):
 p=S/'logos'/man[keys[name]]['filename'];im=Image.open(p);iw,ih=im.size;k=min(w/iw,h/ih);ww,hh=iw*k,ih*k
 mime='image/png' if p.suffix.lower()=='.png' else 'image/jpeg'
 s.e.append(f'<image x="{x+(w-ww)/2}" y="{y+(h-hh)/2}" width="{ww}" height="{hh}" href="data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"/>')
def panel(s,f,y,monthly=False):
 rows=list(csv.DictReader(f.open()));field='month' if monthly else 'year';names=[k for k in rows[0] if k!=field];dx=8.9 if monthly else 9.72;dy=5.7 if monthly else 8.2;x0=59
 for i,r in enumerate(rows):s.text(x0+i*dx+dx/2,y+2.7,r[field][2:].replace('-','.') if monthly else r[field],7.2 if monthly else 8.3,'muted',False,'middle')
 s.line(0,y+5,166,y+5,'#C7BDD8',.3)
 for j,name in enumerate(names):
  yy=y+7+j*dy;logo(s,name,.8,yy,4.5,4.5);s.text(7,yy+3.7,name,8.3 if monthly else 9.7,'ink',True)
  for i,r in enumerate(rows):
   raw=r[name];xx=x0+i*dx;v=int(float(raw)) if raw else None;s.rect(xx,yy,dx-.55,dy-1.0,'#D6D9DE' if v is None else cellcolor(v),.5)
   s.text(xx+(dx-.55)/2,yy+(dy-1)/2+1.05,'—' if v is None else str(v),7.6 if monthly else 9.3,'#FFFFFF' if v is not None and v<=3 else '#24344B',v is not None and v<=3,'middle')
   records.append({'source':f.name,'entity':name,'period':r[field],'display':v,'raw':raw})
 return y+7+len(names)*dy
s=SVG(166,158)
s.text(0,4,'全球企业 / 所选10家',10.5,ACC,True);panel(s,D/'fig-3-2-2_global_company_monthly_rank.csv',9,True)
s.text(0,81,'中国企业 / 所选10家',10.5,ACC,True);panel(s,D/'fig-3-2-4_china_company_monthly_rank.csv',86,True)
# Legend only uses bins present in both monthly source tables.
for i in range(4):
 x=i*36;s.rect(x,151,4,4,colors[i],.3);s.text(x+6,154.2,labels[i]+'名',7.5,'muted')
s.save('company_monthly_matrix')
for glob,file,title in [(True,'fig-3-2-1_global_company_yearly_rank.csv','全球企业 / 所选10家'),(False,'fig-3-2-3_china_company_yearly_rank.csv','中国企业 / 所选10家')]:
 s=SVG(166,136);s.text(0,5,title,11,ACC,True);s.text(166,5,'原年度标签 · 保留全部有效读数',8,'muted',False,'end');panel(s,D/file,12,False)
 for i in range(6):
  x=(i%3)*54;y=111+(i//3)*8;s.rect(x,y,4,4,colors[i],.3);s.text(x+6,y+3.3,labels[i]+'名',8,'muted')
 s.rect(0,127,4,4,'#D6D9DE',.3);s.text(6,130.4,'缺失 · 不插补',8,'muted');s.text(166,130.4,'逐行读变化，逐列读相对位置；颜色为分档，非线性距离。',8,'muted',False,'end')
 s.save('company_global_history_matrix' if glob else 'company_china_history_matrix')
for name,target in [('company_monthly_matrix','05_monthly'),('company_global_history_matrix','06_global_history'),('company_china_history_matrix','07_china_history')]:
 (R/'figures/32'/f'{target}.pdf').write_bytes((R/'figures/new'/f'{name}.pdf').read_bytes())
assert len(records)==460
assert all(r['display']==int(float(r['raw'])) if r['raw'] else r['display'] is None for r in records)
(R/'review/rank_matrix_cells.json').write_text(json.dumps({'cells':records,'cell_count':len(records),'all_match':True,'layout_checks':QA},ensure_ascii=False,indent=2))
print('Matrices: 460 source cells retained, including missing values')
