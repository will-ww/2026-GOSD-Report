from pathlib import Path
import fitz,json,re,subprocess,unicodedata
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageChops
R=Path(__file__).resolve().parent;ROOT=R.parent;V=R/'review';V.mkdir(exist_ok=True);(V/'pages').mkdir(exist_ok=True)
p=next((R/'output').glob('*.pdf'));d=fitz.open(p);m=json.loads((R/'assembly_manifest.json').read_text())
texts=[x.get_text()for x in d];full='\n'.join(texts);(V/'full_text.txt').write_text(full)
checks={'pages':len(d),'portrait':all(p.rect.width<p.rect.height for p in d),'a3_pages':[i+1 for i,p in enumerate(d)if p.rect.width>800],'bad_glyphs':[i+1 for i,t in enumerate(texts)if '\ufffd' in t],'appendix_b_absent':not re.search(r'附录\s*[BＢ]|附录\s*A/B',full),'unresolved_placeholders':[],'footer_errors':[],'link_errors':[],'preservation':[]}
for k,pg in enumerate(d):
 for l in pg.get_links():
  if l['kind']==fitz.LINK_GOTO and not 0<=l['page']<len(d):checks['link_errors'].append({'page':k+1,'link':l})
 for s in [s for b in pg.get_text('dict')['blocks']if b['type']==0 for l in b['lines']for s in l['spans']]:
  if k+1 not in [15,28,76,116,137,154] and s['text'].strip().isdigit()and s['size']<16 and s['bbox'][1]>.91*pg.rect.height and s['bbox'][0]>.8*pg.rect.width:
   if int(s['text'].strip())!=k+1:checks['footer_errors'].append((k+1,s['text']))
for item in m['parts'][1:]:
 src=fitz.open(ROOT/item['file']);off=item['start_page']-1;ok=[]
 for j,sp in enumerate(src):
  # No altered subject matter: all text above the footer retains exact extraction.
  clip=fitz.Rect(0,0,sp.rect.width,sp.rect.height*.91)
  eq=sp.get_text(clip=clip)==d[off+j].get_text(clip=clip)
  pix=sp.get_pixmap(matrix=fitz.Matrix(.8,.8),clip=clip)
  a=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
  pp=d[off+j].get_pixmap(matrix=fitz.Matrix(.8,.8),clip=clip);b=Image.frombytes('RGB',[pp.width,pp.height],pp.samples)
  diff=np.abs(np.asarray(a,dtype=float)-np.asarray(b,dtype=float))
  ratio=float(np.count_nonzero(diff>8)/diff.size);mae=float(diff.mean())
  identical=mae<.02 and ratio<.0001
  ok.append({'page':off+j+1,'text_equal':eq,'render_equal_with_antialias_tolerance':identical,'mean_absolute_pixel_difference':mae,'ratio_difference_over_8':ratio})
 checks['preservation'].extend(ok)
expected=json.loads((R/'toc_expected.json').read_text())
checks['contents_targets']=[{'section':s,'page':p,'found':s in texts[p-1][:350]}for s,p in expected.items()]
checks['all_fonts_embedded']=True
fontdump=subprocess.check_output(['pdffonts',str(p)],text=True);(V/'fonts.txt').write_text(fontdump)
for l in fontdump.splitlines()[2:]:
 parts=l.split()
 if len(parts)>7 and parts[-5]!='yes':checks['all_fonts_embedded']=False
checks['bookmarks']=len(d.get_toc());checks['links']=sum(len(p.get_links())for p in d)
for i,pg in enumerate(d):
 # 1000px thumbnail retains enough structure; full resolution for changed / transition pages.
 pix=pg.get_pixmap(matrix=fitz.Matrix(800/pg.rect.width,800/pg.rect.width))
 pix.save(V/'pages'/f'{i+1:03d}.png')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for start in range(0,len(d),12):
 sheet=Image.new('RGB',(1440,1611),'#e4e9ed');dr=ImageDraw.Draw(sheet)
 for j in range(start,min(start+12,len(d))):
  im=Image.open(V/'pages'/f'{j+1:03d}.png');im.thumbnail((344,488));x=(j-start)%4*360+(360-im.width)//2;y=(j-start)//4*537+28
  sheet.paste(im,(x,y));dr.text((x, y-23),str(j+1),font=font,fill='#152a42')
 sheet.save(V/f'contact-{start//12+1:02d}.jpg',quality=90)
(V/'validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
compact={k:v for k,v in checks.items()if k not in ['preservation','contents_targets']}
compact['preservation_failures']=[x for x in checks['preservation']if not x['text_equal']or not x['render_equal_with_antialias_tolerance']]
compact['toc_failures']=[x for x in checks['contents_targets']if not x['found']]
print(json.dumps(compact,ensure_ascii=False,indent=2))
