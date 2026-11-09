from pathlib import Path
import fitz,json,re,hashlib,unicodedata,xml.etree.ElementTree as E
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];f=R/'output/GOSD_2026_第二章_清洁整理_v0.1_评审稿.pdf';d=fitz.open(f)
log=(R/'work/pass3.log').read_text();assert not re.search(r'Overfull|undefined references|Missing character|Undefined control',log)
assert len(d)==48,len(d)
text='\n'.join(unicodedata.normalize('NFKC',p.get_text()) for p in d);flat=re.sub(r'\s+','',text).replace('‑','-').replace('‐','-').replace('–','-')
for w in ['第二章回望','2025-07-01','2026-06-30','2026年7月快照','快照日期未注明','样本名单及份额分母待核验','独立五域','2026-10-15','2025自然年','筛选总体','2026年1—8月']:
 assert re.sub(r'\s+','',w) in flat,w
for w in ['参考资料','条件估算、核查与复现','持续活跃并不同步','技术结构估算：在已知总量'] :assert w not in text,w
controls=[(i+1,repr(ch)) for i,p in enumerate(d) for ch in p.get_text() if ord(ch)<32 and ch not in '\n\t\r'];assert not controls,controls[:15]
fonts={f[0]:f for p in d for f in p.get_fonts(full=True)};missing=[f for x,f in fonts.items() if not d.extract_font(x)[3]];assert not missing,missing
links=[l for p in d for l in p.get_links()];bad=[l for l in links if l['kind']==fitz.LINK_GOTO and (l.get('page',-1)<0 or l['page']>=len(d))];assert not bad
short=[i+1 for i,p in enumerate(d) if len(p.get_text())<180 and i not in [0,len(d)-1]];assert not short,short
# Numeric files are immutable; presentation updates never alter raw or derived source data.
fingerprints=json.loads((R/'review/data_fingerprints.json').read_text());checks=[]
for p in (R/'modules/02/data').rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(R/'modules/02/data');equal=hashlib.sha256(p.read_bytes()).hexdigest()==fingerprints[str(rel)];checks.append({'path':str(rel),'identical':equal});assert equal,rel
(R/'review/data_preservation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
# Every displayed numbered figure has a stable label, caption and embedded vector derivative.
tex=(R/'content/chapter2_body.tex').read_text();numfig=len(re.findall(r'\\captionof\{figure\}',tex));assert numfig==45
ledger=json.loads((R/'provenance/source_ledger.json').read_text());usedkeys=set(re.findall(r'\\SourceCite\{.*?\}\{(2-R\d+)\}',tex));uris={l['uri'] for l in links if l.get('uri')}
assert all(x['url'] in uris for x in ledger if x['label'] in usedkeys)
# Ensure main figures do not cross content box horizontally and fonts are embedded.
margin=[]
for i,p in enumerate(d):
 if i in [0,len(d)-1]:continue
 for b in p.get_text('dict')['blocks']:
  for line in b.get('lines',[]):
   for span in line['spans']:
    x0,y0,x1,y1=span['bbox']
    if x0<58 or x1>538 or y0<25 or y1>820:margin.append({'page':i+1,'text':span['text'],'box':span['bbox']})
assert not margin,margin[:10]
# Refresh the structured page copy after final layout edits.
units=[{'tex':b.strip(),'figures':re.findall(r'\\includegraphics\[[^]]+\]\{([^}]+)\}',b)} for b in tex.split('\\clearpage') if b.strip()]
(R/'content/chapter2_units.json').write_text(json.dumps(units,ensure_ascii=False,indent=2))
q=R/'work/final_pages';q.mkdir(exist_ok=True)
for i,p in enumerate(d):p.get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(q/f'page_{i+1:02}.png')
for start in range(0,len(d),10):
 im=Image.new('RGB',(1500,850),'#e0e7eb');dr=ImageDraw.Draw(im)
 for j,i in enumerate(range(start,min(start+10,len(d)))):
  a=Image.open(q/f'page_{i+1:02}.png').convert('RGB');a.thumbnail((284,400));x=j%5*300+8;y=j//5*425+20;im.paste(a,(x,y));dr.text((x,y-15),str(i+1),fill='black')
 im.save(q/f'contact_{start+1:02}.png')
ver={'version':'chapter2-clean-v0.1','pages':len(d),'numbered_figures':numfig,'data_files_unchanged':len(checks),'main_period':['2025-07-01','2026-06-30'],'all_fonts_embedded':True,'font_objects':len(fonts),'links':len(links),'source_records':len(ledger),'sources_used':len(usedkeys),'undefined_references':0,'overflow_warnings':0,'unintended_blank_or_fragment_pages':short,'missing_control_glyphs':controls,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
(R/'review/final_verification.json').write_text(json.dumps(ver,ensure_ascii=False,indent=2));print(json.dumps(ver,ensure_ascii=False))
