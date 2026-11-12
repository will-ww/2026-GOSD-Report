"""Offline validation from included fixed inputs. No network access or credentials."""
from pathlib import Path
import csv,json,collections,itertools,yaml,hashlib
R=Path(__file__).resolve().parent;D=R/'data';V=R/'review';V.mkdir(exist_ok=True)
g=json.loads((D/'global100.json').read_text())
raw=json.loads((D/'source/project-mainperiod-all.json').read_text())['data']
for i,(r,q) in enumerate(zip(g,raw)):
    assert r['rank']==i+1 and r['project']==q['name']
    assert abs(r['openrank']-q['openrank'])<.001
cn=list(csv.DictReader((D/'34/table-3-4-3_china_project_openrank_top30.csv').open()))
matches=json.loads((V/'china30-reconciliation.json').read_text());byid={r['id']:r for r in raw}
for r,m in zip(cn,matches):
    assert r['project']==m['project'] and len(m['match'])==1
    assert abs(float(r['openrank'])-byid[m['match'][0]['id']]['openrank'])<.001
root=D/'source/accounts';manifest=json.loads((D/'34/accounts_source_manifest.json').read_text())
for x in manifest['inputs']:
    assert hashlib.sha256((root/x['filename']).read_bytes()).hexdigest()==x['sha256']
b=yaml.safe_load((root/'bot_labels.yml').read_text());bots={u['name'].strip().lower() for q in b['data']['platforms'] if q['name']=='GitHub' for u in q['users']}
months=[f'{y}-{m:02}' for y,ms in [(2025,range(7,13)),(2026,range(1,7))] for m in ms]
series={}
for x in manifest['inputs'][:6]:
    d=json.loads((root/x['filename']).read_text());repo=x['url'].split('/github/')[1].split('/activity_details')[0]
    series[repo]={m:{str(r[0]).strip().lower() for r in d[m] if str(r[0]).strip() and '[bot]' not in str(r[0]).lower() and str(r[0]).strip().lower() not in bots} for m in months}
expected=list(csv.DictReader((D/'34/accounts_repository_summary.csv').open()))
for r in expected:
    counts=collections.Counter(a for arr in series[r['repository']].values() for a in arr)
    assert len(counts)==int(r['annual_unique_logins'])
    for lo,hi,key in [(1,2,'months_1_2'),(3,5,'months_3_5'),(6,8,'months_6_8'),(9,12,'months_9_12')]:
        assert sum(lo<=n<=hi for n in counts.values())==int(r[key])
for r in csv.DictReader((D/'34/accounts_pairwise_intersections.csv').open()):
    a,b=series[r['repository_a']],series[r['repository_b']]
    assert len(set.union(*a.values())&set.union(*b.values()))==int(r['annual_intersection'])
    assert len(set.union(*(a[m]&b[m] for m in months)))==int(r['same_month_unique_accounts'])
    assert sum(len(a[m]&b[m]) for m in months)==int(r['same_month_account_months'])
assert len(g)==100 and len(cn)==30 and len(bots)==928
print('PASS: 100 global scores/order, 30 China scores, eight input hashes, six account samples, 15 pairwise intersections.')
