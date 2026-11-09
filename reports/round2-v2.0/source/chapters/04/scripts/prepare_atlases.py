from pathlib import Path
import json,csv,shutil,hashlib,urllib.request,concurrent.futures,io,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'sources';O=R/'assets/logos';O.mkdir(parents=True,exist_ok=True)
records=[];assets=[]
def j(p):return json.loads(p.read_text())
def raster(path,stem):
 dest=O/(stem+'.png')
 if path.suffix=='.svg':
  if not dest.exists():subprocess.run(['inkscape',str(path),'--export-type=png','--export-width=160','--export-filename='+str(dest)],check=True,capture_output=True)
 else:
  im=Image.open(path).convert('RGBA');im.thumbnail((256,256));im.save(dest)
 return str(dest.relative_to(R))
def add_asset(key,path,kind,source,section):
 target=raster(path,hashlib.sha256((section+key).encode()).hexdigest()[:20])
 assets.append({'section':section,'key':key,'path':target,'kind':kind,'source':source,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'render_sha256':hashlib.sha256((R/target).read_bytes()).hexdigest()});return target
# All existing source identity markings are preserved, with their role explicit.
d=j(S/'41/work/sources/classification.json');a={x['repo_name']:x for x in j(S/'41/assets/project_asset_mapping.json')}
cols=[('application','任务入口','#6146A5'),('framework','构建与编排','#007D78'),('runtime','运行支撑','#155FA8')]
modelcols=[('serving','模型服务','#6146A5'),('posttrain','后训练','#AD4E22'),('pretrain','训练与加速','#155FA8'),('data','数据基础','#007D78'),('compute','算力与调度','#8E6500')]
print('41 stages',sorted(set(x['stage'] for x in d['PROJECTS'])))
for layer,key,title,groups in [('Agent Infra','41a','Agent 应用与基础设施',cols),('Model Infra','41b','模型基础设施',modelcols)]:
 ps=[p for p in d['PROJECTS'] if p['layer']==layer];cats=[]
 stagefix={'serving':'serving','post-train':'posttrain','pre-train':'pretrain','compute':'compute','data':'data','post_train':'posttrain','pre_train':'pretrain'}
 for section,meta in d['SECMAP'].items():
  rr=[]
  for p in ps:
   if p['section']!=section:continue
   x=a[p['repo']];logo=add_asset(p['repo'],S/'41/assets'/x['asset_relative_path'],'owner_avatar',x.get('source_blob_url',''),'41') if x.get('asset_relative_path') else None
   rr.append({'id':p['id'],'repo':p['repo'],'name':p['name'],'owner':p['repo'].split('/')[0],'url':'https://github.com/'+p['repo'],'logo':logo,'logo_kind':'owner_avatar' if logo else 'missing'})
  group=stagefix.get(meta['stage'],meta['stage'])
  if layer=='Model Infra':
   group='serving' if section.startswith(('Model API','Serving')) else 'posttrain' if section.startswith('Post-Train') else 'pretrain' if section.startswith('Pre-Train') else 'data' if section.startswith('Data') else 'compute'
  if rr:cats.append({'id':section,'name':meta['name'],'group':group,'records':rr})
 records.append({'key':key,'section':'4.1','title':title,'groups':[{'id':a,'name':b,'color':c} for a,b,c in groups],'categories':cats,'columns':3,'count':len(ps)})
# HF: keep verified original publisher avatars; 3 changed hashes remain explicitly unresolved.
hf=j(S/'42/research_assets/publisher_logo_manifest_96.json')['rows'];hfm={x['model_id']:x for x in hf}
domains=[('text','文本生成','language'),('retrieval','嵌入与检索','language'),('image','图像与视频','visual'),('multimodal','多模态','visual'),('audio','语音与音频','action'),('robotics','机器人','action')]
rows=list(csv.DictReader((S/'42/work/sources/fig-4-2-1_model_landscape_recent_downloads.csv').open()));cats=[]
for key,name,group in domains:
 rr=[]
 for p in sorted([x for x in rows if x['domain_key']==key],key=lambda x:int(x['rank'])):
  x=hfm[p['model_id']];logo=None
  if x.get('status')=='verified_original_hash':
   path=S/'42'/x['render_png_path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==x['render_png_sha256'];logo=add_asset(p['model_id'],path,'publisher_avatar',x['sourceURL'],'42')
  rr.append({'id':p['model_id'],'repo':p['model_id'],'name':p['model_name'],'owner':p['publisher'],'url':p['model_url'],'logo':logo,'logo_kind':'publisher_avatar' if logo else 'missing','rank':int(p['rank'])})
 cats.append({'id':key,'name':name,'group':group,'records':rr})
records.append({'key':'42','section':'4.2','title':'AI 大模型任务全景','groups':[{'id':a,'name':b,'color':c} for a,b,c in [('language','语言与检索','#6146A5'),('visual','视觉与融合','#155FA8'),('action','声音与行动','#007D78')]],'categories':cats,'columns':3,'count':96})
# Existing fixed functions and record lists are the only membership source.
cloud_assets={x['repo']:x for x in j(S/'43/work/assets/manifest.json')}
pt_assets={x['repo']:x for x in j(S/'46/work/assets/mapping.json')}
for sec,path,title in [('43','43/work/sources/cloud_landscape.json','云基础设施全景'),('44','44/work/sources/landscape.json','数据库系统全景'),('45','45/work/sources/riscv_latest_dataset.json','RISC-V 技术全景'),('46','46/work/sources/pytorch_landscape.json','PyTorch 生态全景')]:
 d=j(S/path);d=d.get('dataset',d);cats=[];groups=[];cm={x['id']:x for x in d['categories']}
 for i,g in enumerate(d['groups']):
  groups.append({'id':g['id'],'name':g['name'],'color':['#007D78','#155FA8','#955A3C','#6146A5'][i]})
  for cid in g['categories']:
   rr=[]
   for p in [x for x in d['projects'] if x['category']==cid]:
    logo=None;kind='missing'
    if sec=='43':
     x=cloud_assets[p['repo']]
     if x.get('status')=='ok':logo=add_asset(p['repo'],S/'43/work'/x['display_path'],x['kind'],x['url'],sec);kind=x['kind']
    if sec=='44':
     raw=S/'44/assets'/f"{p['owner']}.png"
     if not raw.exists():raw=raw.with_suffix('.img')
     logo=add_asset(p['repo'],raw,'owner_avatar','https://github.com/'+p['owner']+'.png',sec);kind='owner_avatar'
    if sec=='46' and p['repo'] in pt_assets:
     x=pt_assets[p['repo']];raw=S/'46/work'/x['logo'];assert hashlib.sha256(raw.read_bytes()).hexdigest()==x['sha256'];logo=add_asset(p['repo'],raw,'project_logo',x['source'],sec);kind='project_logo'
    rr.append({'id':p['id'],'repo':p['repo'],'name':p['name'],'owner':p['owner'],'url':p['url'],'logo':logo,'logo_kind':kind,'tags':p['tags'],'classification':p['classification'],'pending':cid=='pending'})
   name=cm.get(cid,{}).get('name','生态归属待核')
   if sec=='43':name={'runtime':'WASM 运行时','specifications':'WASM 规范','framework':'Serverless 框架','tools':'Serverless 工具','hosted_platform':'Serverless 托管平台','installable_platform':'Serverless 可安装平台'}.get(cid,name)
   cats.append({'id':cid,'name':name,'group':g['id'],'records':rr})
 records.append({'key':sec,'section':'4.'+sec[-1],'title':title,'groups':groups,'categories':cats,'columns':4 if sec in ['43','44'] else 3,'count':len(d['projects'])})
# Fill 4.5 / 4.6 with actual account avatars, never synthetic project logos.
need={p['owner'] for d in records if d['key'] in ['45','46'] for c in d['categories'] for p in c['records'] if not p['logo']}
cache=R/'assets/account-originals';cache.mkdir(exist_ok=True)
def fetch(owner):
 url='https://github.com/'+owner+'.png?size=160';dst=cache/(owner+'.img')
 result={'owner':owner,'url':url,'retrieved_date':'2026-11-07','role':'current_account_avatar_not_historical_project_ownership'}
 try:
  if not dst.exists():
   req=urllib.request.Request(url,headers={'User-Agent':'GOSD-Report-Review/1.0'})
   with urllib.request.urlopen(req,timeout=25) as response:raw=response.read();result['final_url']=response.url
   Image.open(io.BytesIO(raw)).verify();dst.write_bytes(raw)
  result['sha256']=hashlib.sha256(dst.read_bytes()).hexdigest();result['status']='ok'
 except Exception as exc:result['status']='unavailable';result['error']=str(exc)[:200]
 return result
fetched=list(concurrent.futures.ThreadPoolExecutor(max_workers=10).map(fetch,sorted(need)));fm={x['owner']:x for x in fetched}
for d in records:
 if d['key'] not in ['45','46']:continue
 for c in d['categories']:
  for p in c['records']:
   if not p['logo'] and fm[p['owner']]['status']=='ok':
    p['logo']=add_asset(p['repo'],cache/(p['owner']+'.img'),'owner_avatar',fm[p['owner']]['url'],d['key']);p['logo_kind']='owner_avatar'
# Frozen public identity mismatch is shown explicitly, never silently renamed.
audit=list(csv.DictReader((R/'provenance/public_audit/identity_audit.csv').open(encoding='utf-8-sig')))
conflicts={x['repo'] for x in audit if x['identity_status']=='id_mismatch'}
for d in records:
 for c in d['categories']:
  for p in c['records']:
   if p['repo'] in conflicts:p['identity_conflict']=True
 assert sum(len(c['records']) for c in d['categories'])==d['count']
 assert len({p['id'] for c in d['categories'] for p in c['records']})==d['count']
(R/'content/atlas_data.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
(R/'review/logo_manifest.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2))
(R/'review/new_account_assets.json').write_text(json.dumps(fetched,ensure_ascii=False,indent=2))
print(json.dumps([{'key':d['key'],'records':d['count'],'categories':len(d['categories']),'logos':sum(bool(p['logo']) for c in d['categories'] for p in c['records'])} for d in records],ensure_ascii=False))
print('Missing accounts',[(x['owner'],x.get('error')) for x in fetched if x['status']!='ok'])
