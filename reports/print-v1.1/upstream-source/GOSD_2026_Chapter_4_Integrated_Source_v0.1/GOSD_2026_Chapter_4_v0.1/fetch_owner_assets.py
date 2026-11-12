from pathlib import Path
import json,urllib.request,hashlib,concurrent.futures
R=Path(__file__).resolve().parent;P=R/'assets/owners';P.mkdir(exist_ok=True);owners=sorted({p['owner'] for p in json.loads((R/'data/research/rankings.json').read_text())['46']})
def get(n):
 url='https://github.com/'+n+'.png?size=96';p=P/(n+'.png')
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'GOSD-Report-Research/1.0'}),timeout=22) as r:b=r.read()
  p.write_bytes(b);return {'owner':n,'url':url,'path':'assets/owners/'+p.name,'sha256':hashlib.sha256(b).hexdigest(),'kind':'repository owner avatar','retrieved':'2026-11-10'}
 except Exception as e:return {'owner':n,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:a=list(ex.map(get,owners))
(P/'manifest.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));print(a)
