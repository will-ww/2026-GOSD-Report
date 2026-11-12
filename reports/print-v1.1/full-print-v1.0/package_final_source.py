"""Preserve the approved module source package plus the final assembly and QA."""
from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parent
original=R/'inputs/GOSD_2026_Print_Modules_Source_v0.3.zip'
dest=R/'output/GOSD_2026_Print_Source_v1.0.zip'
root='GOSD_2026_Print_Source_v1.0'
files=['assemble_full.py','verify_pdfjs.mjs','package_final_source.py','README.md','download-request.json',
       'review/module-manifest.json','review/full-print-verification.json','review/render-verification.json',
       'review/contents-final.png','review/back-cover-final.png','review/folio-80-final-pdfjs.png']
with zipfile.ZipFile(original) as src,zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name in src.namelist():
        if not name.endswith('/'):
            rel=name.split('/',1)[1]
            z.writestr(root+'/'+rel,src.read(name))
    inventory=[]
    for name in files:
        p=R/name
        assert p.is_file(),p
        arc='full-print-v1.0/'+name
        z.write(p,root+'/'+arc)
        inventory.append(dict(path=arc,size_bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    z.writestr(root+'/FULL_ASSEMBLY_INVENTORY.json',json.dumps(inventory,ensure_ascii=False,indent=2))
print(json.dumps(dict(file=str(dest),bytes=dest.stat().st_size),ensure_ascii=False))
