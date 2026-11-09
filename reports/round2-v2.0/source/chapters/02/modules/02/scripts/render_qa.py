from pathlib import Path
import fitz,json,math
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];out=R/'qa/rendered';out.mkdir(exist_ok=True)
doc=fitz.open(R/'chapter2.pdf'); metrics=[]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
for i,p in enumerate(doc):
 p.get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False).save(out/f'page-{i+1:02}.png')
 blocks=[b for b in p.get_text('blocks') if b[1]>48 and b[3]<796]
 outside=[]
 for b in p.get_text('dict')['blocks']:
  if b['type']!=0:continue
  for line in b['lines']:
   for s in line['spans']:
    x0,y0,x1,y1=s['bbox']
    if (x0<46 or x1>551 or y0<15 or y1>823):outside.append({'text':s['text'],'bbox':s['bbox']})
 metrics.append({'page':i+1,'characters':len(p.get_text()),'content_bottom':max(b[3] for b in blocks) if blocks else 0,'outside_margin':outside,'width':p.rect.width,'height':p.rect.height})
# six pages per contact sheet
for offset in range(0,len(doc),6):
 sheet=Image.new('RGB',(3*320,2*470),'#e7eeee');dr=ImageDraw.Draw(sheet)
 for j in range(min(6,len(doc)-offset)):
  im=Image.open(out/f'page-{offset+j+1:02}.png').convert('RGB');im.thumbnail((300,424))
  x=(j%3)*320+10;y=(j//3)*470+10;sheet.paste(im,(x,y));dr.text((x,y+432),f'Page {offset+j+1}',fill='#193c4e',font=font)
 sheet.save(R/'qa'/f'contact-{offset+1:02}-{min(len(doc),offset+6):02}.png')
# entire chapter
w,h=190,270;cols=6;rows=math.ceil(len(doc)/cols)
full=Image.new('RGB',(cols*(w+12),rows*(h+25)),'#e7eeee');dr=ImageDraw.Draw(full)
for i in range(len(doc)):
 im=Image.open(out/f'page-{i+1:02}.png').convert('RGB');im.thumbnail((w,h));x=(i%cols)*(w+12)+6;y=(i//cols)*(h+25)+5;full.paste(im,(x,y));dr.text((x,y+h+3),str(i+1),fill='#193c4e',font=font)
full.save(R/'qa/overview.png')
(R/'qa/page_metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2))
print('Rendered',len(doc),'pages; potential margin entries:',sum(len(p['outside_margin']) for p in metrics))
