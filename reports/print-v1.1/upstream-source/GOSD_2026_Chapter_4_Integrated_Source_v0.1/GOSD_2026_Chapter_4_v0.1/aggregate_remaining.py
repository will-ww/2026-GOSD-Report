from pathlib import Path
import json,collections
R=Path(__file__).resolve().parent;P=R/'data/research';read=lambda n:json.loads((P/n).read_text());sets=read('rankings.json')
members=collections.defaultdict(list)
for r in read('raw/all-members.json')['data']:members[r['id']].append(r)
anchors=collections.defaultdict(set)
for r in read('raw/all-labels.json')['data']:anchors[r['id']].add(r['repo_id'])
orgs=collections.defaultdict(set)
for r in read('raw/all-scope.json')['data']:orgs[r['org_id_value']].add(r['repo_id'])
def agg(ds):
 vals=collections.defaultdict(float);names={}
 for d in ds:
  for r in d['countries']:
   name=r['country'];zh=r['country_zh']
   if name in ['Taiwan','Hong Kong','Macau','Macao']:name='China';zh='中国'
   if name=='Korea':name='South Korea';zh='韩国'
   vals[name]+=float(r['openrank']);names[name]=zh
 total=sum(vals.values())
 return {'label_n':len(ds),'score_known':total,'countries':[{'country':k,'name':names[k],'score':v,'share':v/total*100} for k,v in sorted(vals.items(),key=lambda x:-x[1])]}
out={}
for sec,ps in sets.items():
 by={p['id']:p for p in ps};candidate=[];excluded=[]
 for lid,mem in members.items():
  aa=anchors[lid]&set(by)
  if not aa:continue
  scopes=[{m['entity_id']} if m['entity_type']=='Repo' else orgs[m['entity_id']] for m in mem];scope=set().union(*scopes)
  cats={by[i]['category'] for i in aa}
  if len(scope)!=sum(map(len,scopes)):excluded.append({'id':lid,'reason':'internal_overlap'});continue
  if len(cats)!=1:excluded.append({'id':lid,'reason':'multiple_categories'});continue
  path=P/'public-labels'/(lid[1:].replace('/','__')+'.json')
  d=json.loads(path.read_text())
  if not d.get('contributions'):excluded.append({'id':lid,'reason':'no_country_export'});continue
  candidate.append({'id':lid,'name':d.get('name'),'anchors':sorted(aa),'scope':sorted(scope),'category':next(iter(cats)),'group':by[next(iter(aa))]['group'],'countries':d['contributions']})
 selected=[];used=set()
 for c in sorted(candidate,key=lambda x:(len(x['scope']),x['id'])):
  if used&set(c['scope']):excluded.append({'id':c['id'],'reason':'scope_overlap'});continue
  selected.append(c);used|=set(c['scope'])
 covered=set().union(*(set(d['anchors']) for d in selected)) if selected else set()
 out[sec]={'selected':selected,'excluded':excluded,'coverage':{'labels':len(selected),'anchors':len(covered),'full_n':len(ps),'main_weight_pct':sum(by[i]['score'] for i in covered)/sum(p['score'] for p in ps)*100},'total':agg(selected),'groups':{g:agg([d for d in selected if d['group']==g]) for g in {p['group'] for p in ps}}}
 print(sec,out[sec]['coverage'],'top',[(p['name'],round(p['share'],1)) for p in out[sec]['total']['countries'][:5]])
(P/'public-countries.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
