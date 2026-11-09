from pathlib import Path
import fitz,json,re,hashlib,unicodedata
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];p=R/'output/GOSD_2026_封面至第一章_视觉整理_v0.8_评审稿.pdf';d=fitz.open(p)
assert len(d)==27
log=(R/'work/pass3.log').read_text();assert not re.search(r'Overfull|undefined references|Missing character',log)
alltext='\n'.join(unicodedata.normalize('NFKC',p.get_text()) for p in d)
assert '参考文献与资料来源' not in alltext
for word in ['2025年7月1日至2026年6月30日','期后观察','2025年10月至2026年9月','2026年1—8月','第一章回望','可复用','可维护','29项候选指标']:assert re.sub(r'\s+','',word) in re.sub(r'\s+','',alltext),word
fonts={f[0]:f for p in d for f in p.get_fonts(full=True)}
missing=[f for x,f in fonts.items() if not d.extract_font(x)[3]];assert not missing
links=[l for p in d for l in p.get_links()];bad=[l for l in links if l['kind']==fitz.LINK_GOTO and (l.get('page',-1)<0 or l.get('page')>=len(d))];assert not bad
uris=[l.get('uri') for l in links if l.get('uri')];ledger=json.loads((R/'provenance/source_ledger.json').read_text());missing_urls=[x['source_url'] for x in ledger if x['source_url'] not in uris];assert not missing_urls,missing_urls
# Render every final page, then create contact sheets for visual review.
for i,page in enumerate(d):
 page.get_pixmap(matrix=fitz.Matrix(1,1)).save(R/'review'/f'final_{i+1:02d}.png')
for start in range(0,len(d),10):
 can=Image.new('RGB',(1500,850),'#E0E5E8');dr=ImageDraw.Draw(can)
 for j,i in enumerate(range(start,min(start+10,len(d)))):
  im=Image.open(R/'review'/f'final_{i+1:02d}.png').convert('RGB');im.thumbnail((284,400));x=j%5*300+8;y=j//5*425+20;can.paste(im,(x,y));dr.text((x,y-15),str(i+1),fill='black')
 can.save(R/'review'/f'final_contact_{start+1:02d}.png')
verification={'version':'0.8','pages':len(d),'main_period':['2025-07-01','2026-06-30'],'rendered_pages':27,'font_objects':len(fonts),'all_fonts_embedded':True,'links':len(links),'source_ledger_entries':len(ledger),'all_source_urls_present':True,'missing_links':bad,'overflow_warnings':0,'removed_reference_section':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(R/'review/final_verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2));print(json.dumps(verification,ensure_ascii=False))
