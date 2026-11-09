from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1];target=R/'output/GOSD_2026_封面至第一章_视觉整理_v0.8_源码与核查.zip'
files=[]
for p in R.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(R)
 if rel.parts[0] in {'output','work','.build_fonts','__pycache__'}:continue
 if p.suffix in {'.png','.aux','.log','.out','.toc','.pyc'}:continue
 files.append(p)
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in sorted(files):z.write(p,'GOSD_front_ch1_v0.8/'+str(p.relative_to(R)))
with zipfile.ZipFile(target) as z:assert z.testzip() is None
print(json.dumps({'path':str(target),'files':len(files),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},ensure_ascii=False))
