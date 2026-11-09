from pathlib import Path
import fitz,re,json,unicodedata,subprocess
from PIL import Image,ImageOps,ImageDraw
R=Path(__file__).resolve().parents[1];P=R/'output/GOSD_2026_第三章_清洁整理_v0.1_评审稿.pdf';Q=R/'review';(Q/'pages').mkdir(exist_ok=True);(Q/'contacts').mkdir(exist_ok=True)
d=fitz.open(P);inventory=[];alltxt='';issues=[]
for i,p in enumerate(d):
 txt=unicodedata.normalize('NFKC',p.get_text()).replace('‐','-').replace('‑','-');alltxt+=txt
 fp=Q/'pages'/f'{i+1:02}.png';p.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(fp)
 spans=[s for b in p.get_text('dict')['blocks'] if 'lines'in b for l in b['lines'] for s in l['spans']]
 bounds=[s['text'] for s in spans if s['bbox'][0]<-1 or s['bbox'][2]>p.rect.width+1 or s['bbox'][1]<-1 or s['bbox'][3]>p.rect.height+1]
 controls=[hex(ord(c)) for c in txt if ord(c)<32 and c not in '\n\t\r']
 rec={'page':i+1,'size_mm':[round(x/2.83465,2) for x in [p.rect.width,p.rect.height]],'characters':len(txt),'links':len(p.get_links()),'figures':re.findall(r'图3-\d+',txt),'out_of_page_text':bounds,'control_glyphs':controls}
 inventory.append(rec)
 if bounds or controls:issues.append(rec)
for start in range(0,len(d),10):
 thumbw=300;thumbh=425;sheet=Image.new('RGB',(5*thumbw,2*(thumbh+22)),'#DDE4E9');dr=ImageDraw.Draw(sheet)
 for j in range(start,min(start+10,len(d))):
  im=Image.open(Q/'pages'/f'{j+1:02}.png').convert('RGB');im.thumbnail((thumbw-10,thumbh-10));x=(j-start)%5*thumbw;y=(j-start)//5*(thumbh+22);sheet.paste(im,(x+(thumbw-im.width)//2,y+21));dr.text((x+6,y+4),str(j+1),fill='black')
 sheet.save(Q/'contacts'/f'{start+1:02}_{min(start+10,len(d)):02}.png')
log=(R/'work/report.log').read_text();warn=re.findall(r'(?:Overfull[^\n]*|Missing character[^\n]*)',log)
font=subprocess.check_output(['pdffonts',str(P)],text=True);(Q/'fonts.txt').write_text(font)
(Q/'page_inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
(Q/'text.txt').write_text(alltxt)
result={'pages':len(d),'a3_pages':[x['page'] for x in inventory if x['size_mm'][0]>290],'warnings':warn,'glyph_or_bounds_issues':issues,'links':sum(x['links'] for x in inventory),'backmatter_removed':not any(x in alltxt for x in ['方法与证据边界','来源索引 地区','来源索引 项目','见章末来源索引']),'figures_expected':40,'toc_entries':len(d.get_toc())}
(Q/'layout_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
