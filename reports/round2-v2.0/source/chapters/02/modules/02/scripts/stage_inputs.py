from pathlib import Path
import json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=Path('/mnt/data/gosd_ch2_inputs')
paths={
'21':SRC/'GOSD_2_1_v0.3.3/section21',
'22':SRC/'GOSD_2_2_v0.3.1',
'23':SRC/'GOSD_2_3_v0.1',
'24':SRC/'GOSD_2_4_v0.3',
'25':SRC/'GOSD_2_5_v0.2',
'26':SRC/'GOSD_26_27_v0.4/section26',
'27':SRC/'GOSD_26_27_v0.4/section27'}
manifest=[]
for sec,p in paths.items():
 (ROOT/'figures'/sec).mkdir(exist_ok=True)
 (ROOT/'data'/sec).mkdir(exist_ok=True)
 (ROOT/'baseline'/sec).mkdir(exist_ok=True)
 for f in (p/'figures').glob('*'):
  if f.suffix in ['.svg','.pdf']:
   shutil.copy2(f, ROOT/'figures'/sec/f.name)
 if (p/'data').exists():shutil.copytree(p/'data',ROOT/'data'/sec,dirs_exist_ok=True)
 for name in ['section.json','section.md','THIRD_PARTY_NOTICES.md']:
  if (p/name).exists():shutil.copy2(p/name, ROOT/'baseline'/sec/name)
 for d in ['review','sources']:
  if (p/d).exists():shutil.copytree(p/d,ROOT/'baseline'/sec/d,dirs_exist_ok=True)
 # retain drawing implementations in auditable, isolated folders
 code=ROOT/'baseline'/sec/'generation';code.mkdir(exist_ok=True)
 cdir=p.parent if sec=='21' else p
 for f in cdir.glob('*.py'):shutil.copy2(f,code/f.name)
 obj=json.loads((p/'section.json').read_text());
 manifest.append({'section':'2.'+sec[1],'input_version':obj.get('version'), 'input_source':str(p), 'sha256':hashlib.sha256((p/'section.json').read_bytes()).hexdigest(), 'page_units':len(obj['pages'])})
for f in (SRC/'GOSD_26_27_v0.4').glob('*.py'):shutil.copy2(f,ROOT/'baseline'/(f'26_27_{f.name}'))
shutil.copy2(SRC/'GOSD_2_2_v0.3.1/graphics.py',ROOT/'scripts/graphics.py')
(ROOT/'review/input_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps(manifest,ensure_ascii=False,indent=2))
