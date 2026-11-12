"""Read-only bounded OpenDigger query runner. Credentials are supplied via process environment."""
from pathlib import Path
import os,sys,json,base64,urllib.request,urllib.parse,time,hashlib
R=Path(__file__).resolve().parent
def query(sql,stem):
    assert sql.lstrip().split()[0].upper() in {'SELECT','WITH','SHOW','DESCRIBE','EXPLAIN'}
    (R/'data/research/sql'/f'{stem}.sql').write_text(sql)
    host=os.environ.get('GOSD_CH_ENDPOINT','http://clickhouse.open-digger.cn:8123/')
    params={'database':'opensource','max_execution_time':'45','max_threads':'2','readonly':'1'}
    auth=base64.b64encode((os.environ.get('GOSD_CH_USER','OpenShare')+':'+os.environ['GOSD_CH_PASSWORD']).encode()).decode()
    req=urllib.request.Request(host+'?'+urllib.parse.urlencode(params),data=sql.encode(),headers={'Authorization':'Basic '+auth,'Content-Type':'text/plain'})
    start=time.time()
    try:
        with urllib.request.urlopen(req,timeout=58) as resp:raw=resp.read()
    except urllib.error.HTTPError as e:
        body=e.read().decode();print('Query failed',stem,e.code,body[:1300]);return None
    out=R/'data/research/raw'/f'{stem}.json';out.write_bytes(raw)
    d=json.loads(raw)
    meta={'query':stem,'elapsed_client_seconds':round(time.time()-start,3),'rows':d.get('rows'),'statistics':d.get('statistics'),'sha256':hashlib.sha256(raw).hexdigest()}
    (R/'data/research/raw'/f'{stem}.meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    print(json.dumps(meta));return d
if __name__=='__main__':
    sql=Path(sys.argv[1]).read_text();result=query(sql,sys.argv[2]);
    if result is not None:print(json.dumps(result.get('data',[])[:12],ensure_ascii=False))
