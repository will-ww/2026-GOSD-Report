from pathlib import Path
import subprocess,sys,json,hashlib,concurrent.futures
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;ROOT=R.parent;V=R/'review';TMP=V/'isolated';TMP.mkdir(exist_ok=True)
m=json.loads((R/'assembly_manifest.json').read_text());target=next((R/'output').glob('*.pdf'))
CODE='''import fitz,sys,pathlib
d=fitz.open(sys.argv[1]);out=pathlib.Path(sys.argv[2]);out.mkdir(exist_ok=True)
for i,p in enumerate(d):
 clip=fitz.Rect(0,0,p.rect.width,p.rect.height*.91)
 p.get_pixmap(matrix=fitz.Matrix(.8,.8),clip=clip).save(out/f'{i+1:03d}.png')
'''
jobs=[('target',target)]+[(str(x['part']),ROOT/x['file'])for x in m['parts'][1:]]
def run(job):
 name,p=job;subprocess.run([sys.executable,'-c',CODE,str(p),str(TMP/name)],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as ex:list(ex.map(run,jobs))
results=[]
for part in m['parts'][1:]:
 for i in range(part['pages']):
  n=part['start_page']+i
  a=np.asarray(Image.open(TMP/str(part['part'])/f'{i+1:03d}.png'),dtype=float);b=np.asarray(Image.open(TMP/'target'/f'{n:03d}.png'),dtype=float)
  diff=np.abs(a-b);mae=float(diff.mean());ratio=float(np.count_nonzero(diff>8)/diff.size)
  results.append({'page':n,'mean_absolute_pixel_difference':mae,'ratio_difference_over_8':ratio,'pass':mae<.02 and ratio<.0001})
q=json.loads((V/'validation.json').read_text());q['isolated_render_preservation']=results
q['cross_document_render_cache_note']='Same-process cross-document MuPDF comparisons can reuse conflicting embedded font caches. Independent processes compare preserved page bodies without that interference.'
q['all_content_preserved']=all(x['text_equal']for x in q['preservation'])and all(x['pass']for x in results)
(V/'validation.json').write_text(json.dumps(q,ensure_ascii=False,indent=2))
print(json.dumps({'pages_checked':len(results),'all_content_preserved':q['all_content_preserved'],'failures':[x for x in results if not x['pass']]},ensure_ascii=False))
