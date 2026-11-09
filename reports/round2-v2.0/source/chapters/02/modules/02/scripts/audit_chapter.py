"""Non-destructive delivery audit. Does not certify upstream data production."""
from pathlib import Path
import json,re,hashlib,subprocess,csv
import fitz
R=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest=json.loads((R/'review/input_manifest.json').read_text());figs=json.loads((R/'review/figure_register.json').read_text())
doc=fitz.open(R/'chapter2.pdf');text='\n'.join(p.get_text() for p in doc)
# Compare delivered data copies with the exact input packages when available.
checks=[];changed=[]
for row in manifest:
 s=int(row['section'].replace('.',''));base=Path(row['input_source'])
 olddir=base/'data'
 for f in sorted((R/'data'/str(s)).rglob('*')):
  if not f.is_file():continue
  rel=f.relative_to(R/'data'/str(s));old=olddir/rel
  rec={'section':row['section'],'file':str(f.relative_to(R)),'sha256':sha(f),'bytes':f.stat().st_size}
  if old.exists():rec['matches_review_input']=sha(old)==sha(f)
  else:rec['matches_review_input']=None
  checks.append(rec)
 for ff in figs:
  if ff['section']!=row['section']:continue
  for a in ff['assets']:
   p=R/'figures'/str(s)/f'{a}.svg';old=base/'figures'/f'{a}.svg'
   if old.exists() and sha(p)!=sha(old):changed.append(str(p.relative_to(R)))
fail=[x for x in checks if x['matches_review_input'] is False]
assert not fail,fail
aux=(R/'chapter2.aux').read_text();labels={}
for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',aux):labels[m[1]]={'number':m[2],'page':int(m[3]) if m[3].isdigit() else m[3]}
for f in figs:
 assert f['label'] in labels,f
 assert labels[f['label']]['number']==f['number'],(f,labels.get(f['label']))
 f['page']=labels[f['label']]['page']
 for a in f['assets']:
  for ext in ['svg','pdf']:assert (R/'figures'/f['section'].replace('.','')/(a+'.'+ext)).is_file()
sec_pages={r['section']:labels['sec'+r['section'].replace('.','')]['page'] for r in manifest}
fonts=subprocess.check_output(['pdffonts',str(R/'chapter2.pdf')],text=True)
(R/'qa/embedded_fonts.txt').write_text(fonts)
fontrows=[x for x in fonts.splitlines()[2:] if x.strip()]
assert all('yes' in x.split()[-6:-3] for x in fontrows)
assert all(p.rect.width<p.rect.height for p in doc)
assert all(abs(p.rect.width-595.276)<2 and abs(p.rect.height-841.89)<2 for p in doc)
log=(R/'chapter2.log').read_text(errors='replace')
bad=[x for x in ['Overfull \\hbox','Overfull \\vbox','There were undefined references','Missing character'] if x in log]
assert not bad,bad
assert '2026年7月之后的事件作为期后观察' not in text
# Render review and machine margins serve different functions.
result={'version':'v1.0.0','status':'待作者评审','pages':len(doc),'a4_portrait_pages':len(doc),'numbered_figures':len(figs),'references':len(json.loads((R/'references/references.json').read_text())),'section_start_pages':sec_pages,'data_files':len(checks),'data_file_mismatches':len(fail),'redesigned_figures':sorted(set(changed)),'font_rows':len(fontrows),'all_fonts_embedded':True,'latex_overfull_or_undefined':bad,'pdf_sha256':sha(R/'chapter2.pdf'),'scope':'检查本轮排版、图号、引用、文件与派生计算；不认证上游账号去重、映射、统计窗口和算法执行。'}
(R/'review/data_fingerprints.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
(R/'review/figure_register.json').write_text(json.dumps(figs,ensure_ascii=False,indent=2))
(R/'review/release_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
with (R/'review/图表—来源—正文索引.csv').open('w',newline='',encoding='utf-8-sig') as out:
 w=csv.writer(out);w.writerow(['小节','图号','PDF页码','图题','来源说明','矢量文件'])
 for f in figs:w.writerow([f['section'],f['number'],f['page'],f['caption'],f['source'],';'.join(f'figures/{f["section"].replace(".","")}/{a}.svg' for a in f['assets'])])
print(json.dumps(result,ensure_ascii=False,indent=2))
