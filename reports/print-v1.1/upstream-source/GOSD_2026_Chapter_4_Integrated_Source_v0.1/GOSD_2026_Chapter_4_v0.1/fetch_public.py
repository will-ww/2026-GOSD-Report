from pathlib import Path
import json,urllib.request,concurrent.futures,shutil,hashlib
R=Path(__file__).resolve().parent;D=R/'data/research'
ids=sorted({r['id'] for r in json.loads((D/'raw/all-labels.json').read_text())['data']})
def get(lid):
 f=lid[1:].replace('/','__')+'.json';dest=D/'public-labels'/f;cache=R/'data/43/public-labels'/f
 if cache.exists():shutil.copy2(cache,dest)
 else:
  try:
   req=urllib.request.Request('https://oss.open-digger.cn/'+lid[1:]+'/meta.json',headers={'User-Agent':'GOSD-Report-Research/1.0'})
   with urllib.request.urlopen(req,timeout=25) as r:b=r.read()
   dest.write_bytes(b)
  except Exception as e:return {'id':lid,'error':str(e)}
 d=json.loads(dest.read_text());return {'id':lid,'countries':len(d.get('contributions',[])),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'retrieved':'2026-11-10'}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:a=list(ex.map(get,ids))
(D/'public-manifest.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));print('LABELS',len(a),'ERRORS',[r for r in a if 'error' in r])
