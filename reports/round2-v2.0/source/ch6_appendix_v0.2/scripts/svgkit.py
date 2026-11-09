from pathlib import Path
import html, json, subprocess, xml.etree.ElementTree as ET
from PIL import ImageFont
R=Path(__file__).resolve().parents[1];O=R/'figures/new';QA=[]
F=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',100,index=2)
B=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',100,index=2)
C={'ink':'#142C49','muted':'#536B7D','line':'#D7E4EA','teal':'#007D78','blue':'#155FA8','white':'#FFFFFF'}
def col(c):return C.get(c,c)
class SVG:
 def __init__(self,w,h):self.w=w;self.h=h;self.e=[];self.labels=[]
 def rect(self,x,y,w,h,c,rx=0):self.e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{col(c)}"/>')
 def path(self,d,c='line',lw=.3,opacity=1,fill='none'):self.e.append(f'<path d="{d}" fill="{fill}" stroke="{col(c)}" stroke-width="{lw}" opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"/>')
 def line(self,x1,y1,x2,y2,c='line',lw=.3):self.path(f'M{x1} {y1}L{x2} {y2}',c,lw)
 def circ(self,x,y,r,c):self.e.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col(c)}"/>')
 def text(self,x,y,t,pt=10,c='ink',b=False,anchor='start'):
  size=pt*25.4/72;w=(B if b else F).getlength(t)/100*size;left=x if anchor=='start' else x-w/2 if anchor=='middle' else x-w
  self.labels.append({'text':t,'pt':pt,'x':round(left,2),'y':y,'width':round(w,2)})
  family='Liberation Sans, Noto Sans CJK SC'
  self.e.append(f'<text x="{x}" y="{y}" fill="{col(c)}" font-family="{family}" font-size="{size}" font-weight="{700 if b else 400}" text-anchor="{anchor}">{html.escape(t)}</text>')
 def embed(self,path,x,y,w,h):
  el=ET.parse(path).getroot();el.set('x',str(x));el.set('y',str(y));el.set('width',str(w));el.set('height',str(h));self.e.append(ET.tostring(el,encoding='unicode'))
 def save(self,name):
  p=O/name;p.with_suffix('.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.w}mm" height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">'+''.join(self.e)+'</svg>')
  for ext in ['pdf','png']:
   cmd=['inkscape',str(p.with_suffix('.svg')),'--export-type='+ext,'--export-filename='+str(p.with_suffix('.'+ext))]
   if ext=='png':cmd+=['--export-width=1500']
   subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  bad=[x for x in self.labels if x['x']<-.2 or x['x']+x['width']>self.w+.2 or x['y']>self.h]
  QA.append({'file':name,'labels':len(self.labels),'outside':bad});assert not bad,bad
