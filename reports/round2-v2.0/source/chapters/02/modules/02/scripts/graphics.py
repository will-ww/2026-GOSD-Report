"""Exact-data editorial graphics. SVG is the editable master, PDF embeds fonts.
All physical sizes are millimetres; font sizes are in points. No font files shipped.
"""
from pathlib import Path
import json, math, html
import pandas as pd
import numpy as np
import cairosvg
from PIL import ImageFont
import geopandas as gpd
from pyproj import Transformer
from shapely.ops import unary_union
import pycountry
from fontTools.ttLib import TTFont

ROOT=Path(__file__).resolve().parent
C={'ink':'#193C4E','teal':'#168A8D','mint':'#49A1A0','blue':'#3E6686','gold':'#AF824E','purple':'#76698F','gray':'#AABCC3','line':'#D8E4E7','pale':'#F0F6F6','land':'#E8F0F1','muted':'#57717D','white':'#FFFFFF'}
GROUP={'Europe':C['teal'],'United States':C['blue'],'China':C['mint'],'India':C['gold'],'Global South representatives':C['purple']}
ZH={'Europe':'欧洲','United States':'美国','China':'中国','India':'印度','Global South representatives':'南方六国代表组'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
PF=ImageFont.truetype(FONT,100,index=2); BF=ImageFont.truetype(BOLD,100,index=2)
SUPPORTED=set(TTFont(FONT,fontNumber=2).getBestCmap())
ALL_QA=[]

def width(s,pt,bold=False):return (BF if bold else PF).getlength(str(s))/100*pt*25.4/72

class S:
 def __init__(self,h,w=170):
  self.w=w;self.h=h;self.items=[];self.labels=[]
  self.items.append(f'<rect width="{w}" height="{h}" fill="white"/>')
  self.items.append('<defs><pattern id="hatch" patternUnits="userSpaceOnUse" width="2.4" height="2.4"><rect width="2.4" height="2.4" fill="#F7FBFB"/><path d="M-1,1 L1,-1 M0,2.4 L2.4,0 M1.4,3.4 L3.4,1.4" stroke="#49A1A0" stroke-width="0.3"/></pattern></defs>')
 def rect(self,x,y,w,h,fill='pale',stroke=None,rx=0,lw=.18):
  self.items.append(f'<rect x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}" rx="{rx}" fill="{C.get(fill,fill)}" stroke="{C.get(stroke,stroke) if stroke else "none"}" stroke-width="{lw}"/>')
 def line(self,x1,y1,x2,y2,c='line',lw=.22,dash=None):
  self.items.append(f'<path d="M{x1:.3f},{y1:.3f} L{x2:.3f},{y2:.3f}" fill="none" stroke="{C.get(c,c)}" stroke-width="{lw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def path(self,d,fill='none',stroke=None,lw=.25,opacity=1):
  self.items.append(f'<path d="{d}" fill="{C.get(fill,fill)}" stroke="{C.get(stroke,stroke) if stroke else "none"}" stroke-width="{lw}" opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"/>')
 def circle(self,x,y,r,fill='teal',stroke='white',lw=.22,opacity=1):
  self.items.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{C.get(fill,fill)}" stroke="{C.get(stroke,stroke)}" stroke-width="{lw}" opacity="{opacity}"/>')
 def t(self,x,y,text,pt=9.2,c='ink',bold=False,anchor='start'):
  text=str(text); ww=width(text,pt,bold); xx=x if anchor=='start' else x-ww if anchor=='end' else x-ww/2
  self.labels.append(dict(text=text,x=xx,y=y-pt*.3528*.84,w=ww,h=pt*.3528*1.08,pt=pt))
  self.items.append(f'<text x="{x:.4f}" y="{y:.4f}" font-family="Noto Sans CJK SC" font-size="{pt*25.4/72:.5f}" font-weight="{700 if bold else 400}" fill="{C.get(c,c)}" text-anchor="{anchor}">{html.escape(text)}</text>')
 def wrap(self,x,y,text,maxw,pt=9.2,c='muted',bold=False,leading=None):
  line='';lines=[]
  for ch in text:
   if ch=='\n':lines.append(line);line='';continue
   if width(line+ch,pt,bold)>maxw and line:lines.append(line);line=ch
   else:line+=ch
  if line:lines.append(line)
  leading=leading or pt*.3528*1.5
  for i,l in enumerate(lines):self.t(x,y+i*leading,l,pt,c,bold)
  return len(lines)*leading
 def title(self,title,sub=None):
  self.t(1,6,title,12,'ink',True)
  if sub:self.t(1,12,sub,8.5,'muted')
 def save(self,base):
  base=Path(base);base.parent.mkdir(parents=True,exist_ok=True)
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">'+'\n'.join(self.items)+'</svg>'
  base.with_suffix('.svg').write_text(svg,encoding='utf8')
  cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(base.with_suffix('.pdf')))
  cairosvg.svg2png(bytestring=svg.encode(),write_to=str(base.with_suffix('.png')),output_width=2040)
  bad=[q for q in self.labels if q['x'] < -.25 or q['x']+q['w']>self.w+.25 or q['y']<-.3 or q['y']+q['h']>self.h+.3]
  # Only check text-to-text overlap. Borders/lines that encode values are checked visually.
  overlaps=[]
  for i,a in enumerate(self.labels):
   for b in self.labels[i+1:]:
    ox=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x']);oy=min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])
    if ox>.45 and oy>.65:overlaps.append([a['text'],b['text'],round(ox,2),round(oy,2)])
  missing=sorted({ch for q in self.labels for ch in q['text'] if not ch.isspace() and ord(ch) not in SUPPORTED})
  assert not missing,(base.name,'Unsupported glyphs',missing)
  ALL_QA.append({'missing_glyphs':missing,'asset':base.name,'width_mm':self.w,'height_mm':self.h,'out_of_bounds':bad,'text_overlap_candidates':overlaps})
  print(base.name,'overflow',len(bad),'overlap candidates',len(overlaps))

# Geographic figures retain the projection from the accepted v0.2.
def geo_records(data,worldfile):
 g=gpd.read_file(worldfile);tr=Transformer.from_crs('EPSG:4326','EPSG:8857',always_xy=True)
 china=unary_union(list(g[g.iso_a3.isin(['CHN','TWN'])].geometry)); paths=[];pts={}
 for _,row in g.iterrows():
  if row['name']=='Antarctica' or row.iso_a3=='TWN':continue
  geom=china if row.iso_a3=='CHN' else row.geometry
  code=row.iso_a3
  if code=='-99':code={'France':'FRA','Norway':'NOR','Kosovo':'XKX','Somaliland':'SOM','N. Cyprus':'CYP'}.get(row['name'],code)
  parts=[geom] if geom.geom_type=='Polygon' else list(geom.geoms)
  for p in parts:
   arr=np.array(p.exterior.coords);x,y=tr.transform(arr[:,0],arr[:,1]);paths.append(np.array([x,y]).T)
  if row['name'] in ['Somaliland','N. Cyprus']:continue
  country=pycountry.countries.get(alpha_3=code);a2=country.alpha_2 if country else {'XKX':'XK'}.get(code)
  if a2 in data:
   p=max(parts,key=lambda p:p.area).representative_point();pts[a2]=tr.transform(p.x,p.y)
 return paths,pts

