from pathlib import Path
import json,re,subprocess,hashlib,unicodedata
import fitz
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]; P=R/'output/GOSD_2026_第六章_清洁整理_v0.1_评审稿.pdf'; V=R/'review';(V/'pages').mkdir(exist_ok=True)
d=fitz.open(P); texts=[];outside=[]; chars=[]
for i,p in enumerate(d):
 texts.append(unicodedata.normalize('NFKC',p.get_text()));p.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(V/'pages'/f'{i+1:02}.png')
 for b in p.get_text('dict')['blocks']:
  for l in b.get('lines',[]):
   for s in l['spans']:
    x0,y0,x1,y1=s['bbox']
    if x0<-.5 or y0<-.5 or x1>p.rect.width+.5 or y1>p.rect.height+.5:outside.append({'page':i+1,'text':s['text'],'bbox':s['bbox']})
    if '\ufffd' in s['text']:chars.append({'page':i+1,'text':s['text']})
for chunk in range((len(d)+4)//5):
 sheet=Image.new('RGB',(1500,470),'#E4E6E8');dr=ImageDraw.Draw(sheet)
 for j in range(5):
  i=chunk*5+j
  if i>=len(d):break
  im=Image.open(V/'pages'/f'{i+1:02}.png');im.thumbnail((280,410));x=j*300+10;sheet.paste(im,(x,10));dr.text((x,432),str(i+1),fill='black')
 sheet.save(V/f'contact-{chunk+1}.png')
log=(R/'work/report.log').read_text();warnings=[l for l in log.splitlines() if any(s in l for s in ['Overfull','Missing character','undefined references'])]
fonts=subprocess.check_output(['pdffonts',str(P)],text=True);(V/'fonts.txt').write_text(fonts)
unembedded=[l for l in fonts.splitlines()[2:] if re.search(r'\sno\s+(?:yes|no)\s+(?:yes|no)\s+\d',l)]
text='\n\f\n'.join(texts);(V/'full_text.txt').write_text(text)
actions=re.findall(r'\\Action\{(\d+)\}',(R/'content/chapter6.tex').read_text());assert actions==[f'{i:02}' for i in range(1,10)]
manifest=json.loads((V/'input_manifest.json').read_text()); badfiles=[]
for a in manifest:
 p=R/'provenance/original_chapter6'/a['path']
 if hashlib.sha256(p.read_bytes()).hexdigest()!=a['sha256']:badfiles.append(a['path'])
result={'pages':len(d),'sizes_pt':sorted(set((round(p.rect.width,1),round(p.rect.height,1)) for p in d)),'page_characters':[len(t) for t in texts], 'actions':actions,'numbered_figures':re.findall(r'图6[‐‑–—-](\d)',text),'outside_text':outside,'replacement_characters':chars,'layout_warnings':warnings,'unembedded_fonts':unembedded,'bookmarks':d.get_toc(),'uri_links':[(i+1,l['uri']) for i,p in enumerate(d) for l in p.get_links() if 'uri' in l],'preserved_original_files':len(manifest),'changed_original_files':badfiles,'sha256':hashlib.sha256(P.read_bytes()).hexdigest()}
(V/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
assert len(d)==10;assert all(p.rect.width<p.rect.height for p in d);assert not outside+chars+warnings+unembedded+badfiles
print(json.dumps({k:v for k,v in result.items() if k not in ['bookmarks','uri_links']},ensure_ascii=False))
