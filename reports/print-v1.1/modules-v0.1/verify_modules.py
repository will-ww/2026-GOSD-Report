"""Print preflight and complete page rendering, without altering source figures."""
from pathlib import Path
import json,re,collections,hashlib
import fitz
from PIL import Image,ImageOps,ImageDraw,ImageFont

R=Path(__file__).resolve().parent
M=72/25.4
review=R/'review';render=review/'rendered';contacts=review/'contacts'
render.mkdir(exist_ok=True);contacts.mkdir(exist_ok=True)
manifest=json.loads((review/'module-manifest.json').read_text())
body=json.loads((review/'body-retention.json').read_text())
docs={m['module']:fitz.open(m['file']) for m in manifest}
checks=[];problems=[];texts={};fontrecords={};pageinfo=[]
def check(name,result,details=None):
 checks.append(dict(check=name,passed=bool(result),details=details))
 if not result:problems.append(checks[-1])
def clean(s):return re.sub(r'\s+','',s)
check('8 modules',len(docs)==8)
check('module page counts',[len(d) for d in docs.values()]==[18,12,22,24,16,14,8,24])
for m in manifest:
 d=docs[m['module']];mid=m['module'];texts[mid]=[]
 thumbs=[];fontrecords[mid]=[]
 for i,p in enumerate(d):
  check(f'M{mid:02d} page {i+1}: A4 portrait',abs(p.rect.width-210*M)<.1 and abs(p.rect.height-297*M)<.1)
  t=p.get_text();texts[mid].append(t)
  if i+1 in m['blank_pages']:
   check(f'M{mid:02d} page {i+1}: intentional blank',not t.strip() and not p.get_images() and not p.get_drawings())
  check(f'M{mid:02d} page {i+1}: valid local links',all(l.get('kind')!=fitz.LINK_GOTO or 0<=l.get('page',-1)<len(d) for l in p.get_links()))
  pix=p.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False)
  filename=render/f'M{mid:02d}_{i+1:02d}.png';pix.save(filename)
  im=Image.open(filename).convert('RGB');im.thumbnail((315,446))
  tile=Image.new('RGB',(337,477),'#e1e6ed');tile.paste(im,((337-im.width)//2,8))
  label=f'M{mid:02d} / {i+1:02d}' + ('  BLANK' if i+1 in m['blank_pages'] else '')
  ImageDraw.Draw(tile).text((12,457),label,fill='#14284a')
  thumbs.append(tile)
  rects=[s['bbox'] for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
  pageinfo.append(dict(module=mid,page=i+1,label=p.get_label(),texts=len(t),images=len(p.get_images()),drawings=len(p.get_drawings()),min_text_x=min([r[0]/M for r in rects],default=None),max_text_x=max([r[2]/M for r in rects],default=None)))
 for start in range(0,len(thumbs),12):
  cells=thumbs[start:start+12];sheet=Image.new('RGB',(337*3,477*((len(cells)+2)//3)),'#ccd5e0')
  for j,im in enumerate(cells):sheet.paste(im,((j%3)*337,(j//3)*477))
  sheet.save(contacts/f'M{mid:02d}_{start//12+1}.jpg',quality=90)
 seen=set()
 for p in d:
  for f in p.get_fonts(full=True):
   if f[0] in seen:continue
   seen.add(f[0]);base,ext,typ,data=d.extract_font(f[0])
   fontrecords[mid].append(dict(name=base,type=typ,extension=ext,embedded_bytes=len(data)))
   check(f'M{mid:02d} font {base}: embedded',bool(data) or typ=='Type3')
 check(f'M{mid:02d}: no old appendix label',not re.search(r'附录\s*A', ''.join(texts[mid])))
 check(f'M{mid:02d}: even pages',len(d)%2==0)
 check(f'M{mid:02d}: no replacement glyph','\ufffd' not in ''.join(texts[mid]))
 print(f'M{mid:02d}: {len(d)} pages rendered',flush=True)

retention=[]
for b in body:
 p=docs[b['module']][b['local_page']-1];c=fitz.Rect(b['clip']);c.x0+=b['dx'];c.x1+=b['dx']
 expected=collections.Counter(clean(b['expected_text']));actual=collections.Counter(clean(p.get_text(clip=c)))
 missing=expected-actual
 retention.append(dict(module=b['module'],page=b['local_page'],missing=dict(missing)))
 check(f'M{b["module"]:02d} page {b["local_page"]}: all source body characters retained',not missing,dict(missing))

log=(R/'master/output/master.log').read_text(errors='replace')
measure={m.group(1):float(m.group(2))*25.4/72.27 for m in re.finditer(r'AUDITBOX\|([^|]+)\|[^|]+\|[^|]+\|[^|]+\|([\d.]+)pt',log)}
boxes=json.loads((review/'master-boxes.json').read_text());heights=[]
for b in boxes:
 h=measure.get(b['id']);heights.append({**b,'height':h})
 if b['max_height'] and h is not None:check('native box '+b['id']+' height',h<=b['max_height']+.3,dict(page=b['page'],height=h,limit=b['max_height'],text=b['text']))
check('XeLaTeX no missing characters','Missing character:' not in log)
check('16 planned blank pages',sum(len(m['blank_pages']) for m in manifest)==16)
check('138 total physical pages',sum(len(d) for d in docs.values())==138)
check('Chinese thanks starts on recto',docs[8][20].get_label()=='117')
check('current 5-1 date retained in chapter 5','2026.11.09' in ''.join(texts[6]) or '2026.11.9' in ''.join(texts[6]))
check('appendix internal references remapped',not re.search(r'(?<![A-Za-z0-9])A[1-6](?![A-Za-z0-9])',''.join(texts[8])))
check('production hand-offs removed',not any(s in ''.join(''.join(v) for v in texts.values()) for s in ['供第六章综合评议','下一步：第三章识别关键主体','上述为证据引出的行动建议','这些行动方向由本章证据支持']))
check('method introduction has no duplicated second line',clean(texts[8][12]).count('不用于相互换算。')==1)
if (review/'method-intro.json').exists():
 ml=(R/'master/output/method-intro.log').read_text(errors='replace')
 hit=re.search(r'AUDITBOX\|methodintro\|[^|]+\|[^|]+\|[^|]+\|([\d.]+)pt',ml)
 height=float(hit.group(1))*25.4/72.27 if hit else 999
 check('reflowed method introduction fits reserved area',height<12,{'height_mm':height})
patches=json.loads((review/'pdf-text-patches.json').read_text())
for patch in patches:
 if 'appendix-title' in patch['tag']:
  check('one replacement per appendix title: '+patch['new'],patch['count']==1)
  check('one visible copy of appendix title: '+patch['new'],clean(''.join(texts[8])).count(clean(patch['new']))==1)
(review/'preflight.json').write_text(json.dumps(dict(checks=checks,problems=problems,fonts=fontrecords,pages=pageinfo,retention=retention,boxes=heights),ensure_ascii=False,indent=2))
(review/'module-text.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2))
print(json.dumps(dict(checks=len(checks),problems=problems),ensure_ascii=False,indent=2))
