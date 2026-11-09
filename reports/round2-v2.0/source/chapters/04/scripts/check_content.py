"""Verify fixed inputs, complete portrait atlases, embedded fonts and final content."""
from pathlib import Path
import hashlib, json, re, unicodedata, subprocess
import fitz

R=Path(__file__).resolve().parents[1]
manifest=json.loads((R/'review/source_preservation.json').read_text())
bad=[]
for item in manifest['entries']:
    path=R/'sources'/item['path']
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:
        bad.append(item['path'])
assert not bad,bad
data=json.loads((R/'content/atlas_data.json').read_text())
geo=json.loads((R/'review/atlas_geometry.json').read_text())
maps=[]
for a in data:
    original=[p['id'] for c in a['categories'] for p in c['records']]
    drawn=[x['id'] for x in geo if x['key']==a['key']]
    assert len(original)==len(set(original))==a['count']
    assert sorted(original)==sorted(drawn)
    maps.append({'key':a['key'],'records':len(original),'logos':sum(bool(p['logo']) for c in a['categories'] for p in c['records']),'all_ids_preserved':True})
P=R/'output/GOSD_2026_第四章_清洁整理_v0.1_评审稿.pdf'
doc=fitz.open(P)
texts=[unicodedata.normalize('NFKC',p.get_text()).replace('‐','-').replace('‑','-') for p in doc]
figs=[int(x) for t in texts for x in re.findall(r'图\s*4\s*-\s*(\d+)\b',t)]
assert sorted(figs)==list(range(1,22)),figs
assert all(p.rect.width<p.rect.height for p in doc)
assert all('完整观察名单' in texts[i-1] for i in [3,4,10,17,18,19,20])
assert all('来源索引' not in t and '方法与证据边界' not in t and '治理补页' not in t for t in texts)
assert '不是基金会正式托管名单' in texts[19]
fonttext=subprocess.check_output(['pdffonts',str(P)],text=True)
fontlines=fonttext.splitlines()[2:]
# pdffonts trailing columns: emb sub uni object ID.
unembedded=[line for line in fontlines if line.split()[-5]!='yes']
assert not unembedded,unembedded
result={'raw_source_files':manifest['files'],'raw_source_hashes_unchanged':True,
        'maps':maps,'total_atlas_appearances':sum(m['records'] for m in maps),
        'total_logo_appearances':sum(m['logos'] for m in maps),
        'figure_sequence':figs,'all_portrait':True,'all_fonts_embedded':True,
        'removed_backmatter_absent':True,'pytorch_scope_explicit':True,
        'pdf_sha256':hashlib.sha256(P.read_bytes()).hexdigest()}
(R/'review/content_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
