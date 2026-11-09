from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1];out=R/'output/GOSD_2026_第二章_清洁整理_v0.1_源码与核查.zip'
files=[]
for p in R.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(R)
 if any(x in {'work','output','.build_fonts','__pycache__'} for x in rel.parts):continue
 if p.suffix.lower() in {'.png','.otf','.ttf','.ttc','.pyc','.aux','.log','.out','.toc'}:continue
 files.append(p)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(files):z.write(p,'GOSD_2026_Chapter2_Clean_v0.1/'+str(p.relative_to(R)))
print(json.dumps({'path':str(out.resolve()),'files':len(files),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},ensure_ascii=False))
