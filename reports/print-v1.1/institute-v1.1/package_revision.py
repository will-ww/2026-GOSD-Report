"""Preserve the complete prior source package, adding the isolated institute layout revision."""
from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parent
original=R/'refreshed-source/GOSD_2026_Print_Source_v1.0.zip'
if not original.is_file():original=R.parent/'full-print-v1.0/output/GOSD_2026_Print_Source_v1.0.zip'
dest=R/'output/GOSD_2026_Print_Source_v1.1.zip'
root='GOSD_2026_Print_Source_v1.1'
files=['README.md','build_page.py','apply_revision.py','package_revision.py',
       'layout.sty','standalone.tex','report-page.tex',
       'source/layout.sty','source/prepare_fonts.py','source/assets/siri-color.png',
       'source/assets/institute-research-system.svg','source/data/institute-original.txt',
       'review/text-box-plan.json','review/verification.json','review/standalone-poppler.png',
       'review/full-report-page5.png','output/report-page.pdf','output/SIRI_Institute_Introduction_v1.1.pdf']
with zipfile.ZipFile(original) as src,zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name in src.namelist():
        if not name.endswith('/'):
            z.writestr(root+'/'+name.split('/',1)[1],src.read(name))
    inventory=[]
    for name in files:
        p=R/name; assert p.is_file(),p
        arc='institute-v1.1/'+name
        z.write(p,root+'/'+arc)
        inventory.append(dict(path=arc,size_bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    z.writestr(root+'/INSTITUTE_REVISION_INVENTORY.json',json.dumps(inventory,ensure_ascii=False,indent=2))
print(json.dumps(dict(file=str(dest),bytes=dest.stat().st_size),ensure_ascii=False))
