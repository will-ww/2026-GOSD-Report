from pathlib import Path
import zipfile,shutil,json,hashlib,fitz
R=Path(__file__).resolve().parents[1];O=Path('/mnt/data')
pdf=O/'GOSD_2026_第二章_v1.0_整章图文优化_评审稿.pdf'
shutil.copy2(R/'chapter2.pdf',pdf)
overview=O/'GOSD_2026_第二章_v1.0_页面总览.png';shutil.copy2(R/'qa/overview.png',overview)
revision=O/'GOSD_2026_第二章_v1.0_整章优化策略与修订说明.md';shutil.copy2(R/'review/整章优化策略与修订说明.md',revision)
checks=O/'GOSD_2026_第二章_v1.0_来源与核查清单.md';shutil.copy2(R/'review/核查清单.md',checks)
# A clearly marked extract, not a replacement for the complete chapter.
focus=O/'GOSD_2026_第二章_v1.0_章首与重点优化页.pdf'
d=fitz.open(R/'chapter2.pdf');subset=fitz.open();pages=[1,2,7,8,20,31,45,50]
for p in pages:subset.insert_pdf(d,from_page=p-1,to_page=p-1)
subset.set_metadata({'title':'第二章v1.0章首与重点优化页（节选）','author':'GOSD编制组'})
subset.save(focus,garbage=4,deflate=True)
# No font files, private source PDFs, or publication PDF inside the source package.
path=O/'GOSD_2026_第二章_v1.0_结构化源码与核查包.zip'
files=[]
for f in R.rglob('*'):
 if not f.is_file():continue
 rel=f.relative_to(R)
 if any(p in ['.build_fonts','__pycache__'] for p in rel.parts):continue
 if f.suffix.lower() in ['.otf','.ttf','.ttc','.woff','.woff2','.pyc','.aux','.out','.log','.toc']:continue
 if rel.parts[0]=='qa' and f.name not in ['overview.png','page_metrics.json','embedded_fonts.txt','compile6.txt']:continue
 if rel.parts[0]=='figures' and f.suffix=='.png':continue
 if rel.name=='chapter2.pdf':continue
 if f.suffix=='.pdf' and rel.parts[0]!='figures':continue
 files.append(f)
with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in sorted(files):z.write(f,'GOSD_Chapter2_v1.0/'+str(f.relative_to(R)))
with zipfile.ZipFile(path) as z:
 assert not any(n.lower().endswith(('.ttf','.otf','.ttc','.woff','.woff2')) for n in z.namelist())
 assert not any(n.endswith('chapter2.pdf') for n in z.namelist())
report=[]
for p in [pdf,focus,overview,path,revision,checks]:
 report.append({'name':p.name,'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(O/'GOSD_2026_第二章_v1.0_交付文件.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2));print('ZIP file count',len(files))
