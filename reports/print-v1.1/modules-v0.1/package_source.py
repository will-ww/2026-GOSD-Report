"""Save the exact print assembly and upstream sources, excluding runtime caches."""
from pathlib import Path
import json,zipfile,hashlib
R=Path(__file__).resolve().parent;W=R.parent
qa=json.loads((R/'review/preflight.json').read_text())
assert not qa['problems'],qa['problems']
files={}
def add(p,arc):
 if p.is_file():files[str(arc)]=p
def tree(p,arc):
 for f in p.rglob('*'):
  if f.is_file():add(f,Path(arc)/f.relative_to(p))
for name in ['README.md','rebuild.py','build_modules.py','prepare_front.py','print_config.py','verify_modules.py','package_source.py','refine_method_intro.py','update_backcover_v02.py','update_backcover_v03.py','repair_page80.py','verify_pdfjs.mjs']:
 add(R/name,Path('modules-v0.1')/name)
for folder in ['inputs','source-provenance']:
 tree(R/folder,Path('modules-v0.1')/folder)
for folder in ['frontmatter','master']:
 for name in ['layout.sty','build_front.py','prepare_fonts.py']:
  add(R/folder/name,Path('modules-v0.1')/folder/name)
 for sub in ['assets','data']:
  tree(R/folder/sub,Path('modules-v0.1')/folder/sub)
for name in ['build_front.py','layout.sty','prepare_fonts.py']:
 add(W/'front-v0.8'/name,Path('front-v0.8')/name)
for sub in ['assets','data']:tree(W/'front-v0.8'/sub,Path('front-v0.8')/sub)
for name in ['module-manifest.json','page-specs.json','pdf-text-patches.json','body-retention.json','master-boxes.json','preflight.json','print-qa.md','method-intro.json']:
 add(R/'review'/name,Path('modules-v0.1/review')/name)
tree(R/'review/contacts','modules-v0.1/review/contacts')
add(R/'review/backcover-v02/verification.json','modules-v0.1/review/backcover-v02/verification.json')
add(R/'review/backcover-v02/poppler-after.png','modules-v0.1/review/backcover-v02/poppler-after.png')
for sub in ['page80-check','backcover-v03']:
 for name in ['verification.json','engine-checks.json','poppler-after.png','pdfjs-after.png']:
  add(R/'review'/sub/name,Path('modules-v0.1/review')/sub/name)
upstream=list((W/'assembly-audit/inputs').rglob('*Source*.zip'))
upstream+=[W/'inputs/GOSD_2026_Essential_Frontmatter_Chapter1_Source_v0.5.zip']
for p in upstream:add(p,Path('upstream-source')/p.name)
add(W/'front-v0.8/output/GOSD_2026_Essential_Frontmatter_Clean_Review_v0.8.pdf','upstream-source/GOSD_2026_Frontmatter_Approved_v0.8.pdf')
inventory=[dict(path=arc,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for arc,p in sorted(files.items())]
root='GOSD_2026_Print_Modules_Source_v0.3'
out=R/'output'/f'{root}.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for arc,p in files.items():z.write(p,root+'/'+arc)
 z.writestr(root+'/FILE_INVENTORY.json',json.dumps(inventory,ensure_ascii=False,indent=2))
print(json.dumps(dict(file=str(out),files=len(files),bytes=out.stat().st_size),ensure_ascii=False))
