#!/usr/bin/env python3
"""Approved OSDGs dynamic identity exporter, baseline 2.0.0 (2026-11-06).
Packaging extraction of the reviewed render functions; no visual redesign.
The ten-node constellation is a brand illustration, not a statistical network.
No PDFs or font binaries are published to this repository.
"""
from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import argparse, math, json, html, re, os, sys
import numpy as np
from PIL import ImageFont
import cairosvg
from lxml import etree
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
ROOT=Path(__file__).resolve().parents[1]
TOK=json.loads((ROOT/'source/brand_tokens.json').read_text())
DIMS=TOK['dimensions'];PILLARS=TOK['pillars'];COL=[d['color'] for d in DIMS];HERO=[d['hero_color'] for d in DIMS]
P={'navy':'#102950','night':'#082B68','ink':'#203951','muted':'#596F83','line':'#DCE5F0','paper':'#F9FBFF','white':'#FFFFFF','soft':'#EFF3F5','teal':'#176D79','blue':COL[0]}
PT=25.4/72
FONT_CJK=os.environ.get('OSDGS_FONT_CJK','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
FONT_CJK_B=os.environ.get('OSDGS_FONT_CJK_B','/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
FONT_LAT=os.environ.get('OSDGS_FONT_LAT','/usr/share/fonts/opentype/inter/Inter-Regular.otf')
FONT_LAT_B=os.environ.get('OSDGS_FONT_LAT_B','/usr/share/fonts/opentype/inter/Inter-SemiBold.otf')
SERIF=os.environ.get('OSDGS_FONT_SERIF','/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf')
SERIF_B=os.environ.get('OSDGS_FONT_SERIF_B','/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf')
QA=[]
LOCAL_PDF=False
PNG=True
ICON=json.loads((ROOT/'source/icons.json').read_text())
def c(v):return P.get(v,v)

def tint(h,t):
 h=c(h);v=[int(h[i:i+2],16) for i in [1,3,5]]
 return '#'+''.join(f'{round(x*(1-t)+255*t):02x}' for x in v)

def width(text,pt=10,b=False,fam='Noto Sans CJK SC'):return pilfont(fam,b).getlength(str(text))/100*pt*PT

def clean(s):return html.escape(str(s),quote=True)

class S:
 def __init__(self,w,h,bg=None,title=''):
  self.w=w;self.h=h;self.e=[];self.labels=[];self.uid=0;self.title=title
  if bg:self.rect(0,0,w,h,bg)
 def rect(self,x,y,w,h,fill,stroke=None,lw=.25,rx=0,opacity=1):
  self.e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c(fill)}" stroke="{c(stroke) if stroke else "none"}" stroke-width="{lw}" opacity="{opacity}"/>')
 def path(self,d,stroke='navy',lw=.4,fill='none',op=1,dash=None):
  self.e.append(f'<path d="{d}" fill="{c(fill)}" stroke="{c(stroke) if stroke else "none"}" stroke-width="{lw}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def line(self,x,y,x2,y2,col='line',lw=.25,op=1,dash=None):self.path(f'M{x} {y}L{x2} {y2}',col,lw,op=op,dash=dash)
 def circle(self,x,y,r,fill,stroke=None,lw=.3,op=1,extra=''):
  self.e.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c(fill)}" stroke="{c(stroke) if stroke else "none"}" stroke-width="{lw}" opacity="{op}" {extra}/>')
 def t(self,x,y,text,pt=10,col='ink',bold=False,anchor='start',fam='Noto Sans CJK SC',op=1,tracking=0):
  text=str(text);w=width(text,pt,bold,fam)+(len(text)-1)*tracking;xx=x if anchor=='start' else x-w if anchor=='end' else x-w/2
  self.labels.append({'text':text,'x':xx,'y':y-pt*PT*.91,'w':w,'h':pt*PT*1.12,'pt':pt})
  self.e.append(f'<text x="{x}" y="{y}" fill="{c(col)}" font-size="{pt*PT}" font-family="{fam}" font-weight="{600 if bold else 400}" text-anchor="{anchor}" opacity="{op}" letter-spacing="{tracking}">{clean(text)}</text>')
 def wrap(self,x,y,text,w,pt=10,col='ink',bold=False,leading=None,fam='Noto Sans CJK SC'):
  leading=leading or pt*PT*1.55;out=[];buf=''
  for char in text:
   if char=='\n':out.append(buf);buf='';continue
   if width(buf+char,pt,bold,fam)>w and buf:out.append(buf);buf=char
   else:buf+=char
  if buf:out.append(buf)
  for i,l in enumerate(out):self.t(x,y+i*leading,l,pt,col,bold,fam=fam)
  return y+len(out)*leading
 def embed(self,path,x,y,w,h=None):
  rt=etree.fromstring(Path(path).read_bytes());vb=[float(v) for v in rt.get('viewBox').split()]
  h=h or w*vb[3]/vb[2];self.uid+=1
  prefix=f'g{self.uid}_';body=''.join(etree.tostring(n,encoding='unicode') for n in rt if etree.QName(n).localname not in ['title','desc'])
  ids=re.findall(r'\bid="([^"]+)"',body)
  for old in ids:body=body.replace(f'id="{old}"',f'id="{prefix+old}"').replace(f'url(#{old})',f'url(#{prefix+old})')
  self.e.append(f'<g transform="translate({x},{y}) scale({w/vb[2]},{h/vb[3]})">{body}</g>')
 def svg(self):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" height="{self.h}mm" viewBox="0 0 {self.w} {self.h}" role="img"><title>{clean(self.title)}</title>'+''.join(self.e)+'</svg>'
 def save(self,path,px=1500,outline=False,pdf=True):
  path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
  v=self.svg();path.with_suffix('.svg').write_text(v)
  if pdf and LOCAL_PDF:cairosvg.svg2pdf(bytestring=v.encode(),write_to=str(path.with_suffix('.pdf')))
  if px and PNG:cairosvg.svg2png(bytestring=v.encode(),write_to=str(path.with_suffix('.png')),output_width=px)
  if outline:outline_svg(path.with_suffix('.svg'),path.parent/(path.name+'-outlined.svg'))
  bad=[q for q in self.labels if q['x']<-.8 or q['x']+q['w']>self.w+.8 or q['y']<-.8 or q['y']+q['h']>self.h+.8]
  QA.append({'asset':str(path.relative_to(ROOT)),'text_count':len(self.labels),'out_of_bounds':bad})
  if bad:print('OVERFLOW',path.name,bad)

def outline_svg(src,dst):
 rt=etree.parse(str(src));ns='{http://www.w3.org/2000/svg}'
 for t in list(rt.iter(ns+'text')):
  text=''.join(t.itertext());fam=t.get('font-family','Noto Sans CJK SC');b=int(t.get('font-weight','400'))>=600
  f,gs,cmap,upm=outline_font(fam,b);size=float(t.get('font-size'));pt=size/PT;track=float(t.get('letter-spacing','0'))
  tw=width(text,pt,b,fam)+(len(text)-1)*track;x=float(t.get('x'));y=float(t.get('y'));anc=t.get('text-anchor','start')
  if anc=='middle':x-=tw/2
  elif anc=='end':x-=tw
  group=etree.Element(ns+'g',fill=t.get('fill','#142D4C'),opacity=t.get('opacity','1'))
  group.set('aria-label',text)
  for j,ch in enumerate(text):
   gn=cmap.get(ord(ch),'.notdef');pen=SVGPathPen(gs);gs[gn].draw(pen);d=pen.getCommands()
   if d:
    xx=x+width(text[:j],pt,b,fam)+j*track
    p=etree.SubElement(group,ns+'path',d=d);p.set('transform',f'translate({xx},{y}) scale({size/upm},{-size/upm})')
  t.getparent().replace(t,group)
 rt.write(str(dst),encoding='UTF-8',xml_declaration=True)

def icon(s,name,x,y,size,col='navy',stroke=1.65):
 s.e.append(f'<g transform="translate({x},{y}) scale({size/24})" fill="none" stroke="{c(col)}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>')

@lru_cache(None)
def pf(fam,bold):
 if fam=='Inter': fn=FONT_LAT_B if bold else FONT_LAT;idx=0
 elif fam=='Liberation Serif': fn=SERIF_B if bold else SERIF;idx=0
 else: fn=FONT_CJK_B if bold else FONT_CJK;idx=2
 return ImageFont.truetype(fn,100,index=idx)

@lru_cache(None)
def of(fam,bold):
 if fam=='Inter':fn=FONT_LAT_B if bold else FONT_LAT;idx=0
 elif fam=='Liberation Serif':fn=SERIF_B if bold else SERIF;idx=0
 else:fn=FONT_CJK_B if bold else FONT_CJK;idx=2
 f=TTFont(fn,fontNumber=idx)
 return f,f.getGlyphSet(),f.getBestCmap(),f['head'].unitsPerEm
pilfont=pf
outline_font=of
_original_t=S.t
def safe_t(self,x,y,text,pt=10,col='ink',bold=False,anchor='start',fam='Noto Sans CJK SC',op=1,tracking=0):
 if any('\u3400' <= c <= '\u9fff' for c in str(text)) and fam in ['Inter','Liberation Serif']:
  fam='Noto Sans CJK SC'
 return _original_t(self,x,y,text,pt,col,bold,anchor,fam,op,tracking)
S.t=safe_t

def darker(col,t=.2):
 return '#'+''.join(f'{max(0,round(int(col[i:i+2],16)*(1-t))):02x}' for i in [1,3,5])

def defs(s,txt):s.e.append('<defs>'+txt+'</defs>')

def grad(s,ident,a,bb,kind='linear'):
 if kind=='linear':defs(s,f'<linearGradient id="{ident}" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{a}"/><stop offset="1" stop-color="{bb}"/></linearGradient>')
 else:defs(s,f'<radialGradient id="{ident}" cx=".45" cy=".35" r=".7"><stop stop-color="{a}"/><stop offset="1" stop-color="{bb}"/></radialGradient>')
 return 'url(#'+ident+')'

def poly_path(xy,close=False):
 return 'M'+' L'.join(f'{x:.4f} {y:.4f}' for x,y in xy)+(' Z' if close else '')

def ellxy(t,a,rx=38,ry=26.8):
 x=rx*np.cos(t);y=ry*np.sin(t);a=np.deg2rad(a)
 return np.stack([50+x*np.cos(a)-y*np.sin(a),50+x*np.sin(a)+y*np.cos(a)],axis=1)

def ribbon(s,a,uid,co,cb,hero=True,dark=False,mono=None,k=0):
 t=np.linspace(0,2*np.pi,201)
 xy=ellxy(t,a);dxy=np.gradient(xy,axis=0);n=np.stack([-dxy[:,1],dxy[:,0]],axis=1);n/=np.linalg.norm(n,axis=1)[:,None]
 ww=(.38+.94*(.5+.5*np.sin(t+.6+k*.27))**2)[:,None]
 path=poly_path(np.r_[xy+n*ww, (xy-n*ww)[::-1]],True)
 if mono:
  s.path(poly_path(xy),mono,.85,op=.72)
  return
 name=f'{uid}r{k}'
 defs(s,f'<linearGradient id="{name}" x1=".1" y1=".1" x2=".9" y2=".9"><stop stop-color="{co}" stop-opacity=".12"/><stop offset=".28" stop-color="{co}" stop-opacity=".7"/><stop offset=".57" stop-color="{tint(co,.7)}" stop-opacity=".28"/><stop offset=".85" stop-color="{cb}" stop-opacity=".74"/><stop offset="1" stop-color="{cb}" stop-opacity=".15"/></linearGradient>')
 s.path(path,None,0,f'url(#{name})',.85 if hero else .64)
 s.path(poly_path(xy),'#D5EEFF' if dark else '#D8E9F7',.24,op=.48)
 # One travelling half arc: deliberate front/back contrast and taper, no uniform wire mesh.
 tt=np.linspace(.08+(.20*k),np.pi+(.15*k),95);front=ellxy(tt,a)
 s.path(poly_path(front),f'url(#{name})',.53 if hero else .58,op=.96)
 hi=ellxy(np.linspace(.36+.1*k,1.34+.1*k,45),a,38.2,27.0)
 s.path(poly_path(hi),'#FFFFFF',.19,op=.72 if hero else .46)

def emblem(s,x,y,w,variant='master',dark=False,word=False):
 s.uid+=1;uid=f'dyn{s.uid}_'
 s.e.append(f'<g transform="translate({x},{y}) scale({w/100})" data-brand="OSDGs" data-nodes="10" data-master="dynamic-v2" data-mode="{variant}">')
 hero=variant=='display';mini=variant=='compact';mono=variant in ['mono','reverse'];fg='#FFFFFF' if dark or variant=='reverse' else P['navy']
 if not mono and not mini:
  defs(s,f'<radialGradient id="{uid}aura"><stop stop-color="{ "#6AB8FF" if dark else "#FFFFFF"}" stop-opacity=".08"/><stop offset=".55" stop-color="#62B3F5" stop-opacity=".1"/><stop offset=".78" stop-color="#A699F0" stop-opacity=".075"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>')
  s.circle(50,50,49,f'url(#{uid}aura)')
 if mini:
  for k in [0,2,4]:
   xy=ellxy(np.linspace(0,2*np.pi,130),-90+k*36,38,25)
   s.path(poly_path(xy),HERO[k],1.10,op=.70)
 else:
  for k in range(5):ribbon(s,-90+36*k,uid,HERO[k],HERO[k+5],hero,dark,fg if mono else None,k)
 # Central clear field; only decorative mark, no substituted claims or numbers.
 if not mono and not mini:
  defs(s,f'<radialGradient id="{uid}centre"><stop stop-color="{ "#FFFFFF" if (hero or not dark) else "#071F4C"}" stop-opacity=".88"/><stop offset=".72" stop-color="{ "#F4FBFF" if (hero or not dark) else "#163E77"}" stop-opacity=".58"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>')
  s.circle(50,50,28 if hero else 25,f'url(#{uid}centre)')
 # Swoosh aperture shared by all versions.
 aperture=fg if mono else grad(s,uid+'aperture','#1466B7','#46CBF1')
 s.path('M29 42 C43 26 61 27 72 41 C57 31 44 34 29 42 Z',None,0,aperture,.98)
 s.path('M30 61 C45 71 61 70 73 57 C60 76 41 74 30 61 Z',None,0,aperture,.98)
 if not mono:
  s.path('M34 41 C47 33 59 33 68 39','#BDEEFF',.35,op=.83)
  s.path('M35 63 C48 69 59 66 67 61','#9AE7FF',.35,op=.83)
 # Ten fixed identities, clockwise from top; equal radii.
 for i,d in enumerate(DIMS):
  a=math.radians(-90+36*i);px=50+38*math.cos(a);py=50+38*math.sin(a);r=3.65 if mini else 4.05
  co=HERO[i]
  if mono:fill=fg
  elif mini:fill=co
  else:
   defs(s,f'<radialGradient id="{uid}glow{i}"><stop stop-color="{co}" stop-opacity="{.34 if hero else .13}"/><stop offset=".5" stop-color="{co}" stop-opacity=".10"/><stop offset="1" stop-color="{co}" stop-opacity="0"/></radialGradient><radialGradient id="{uid}n{i}" cx=".28" cy=".22" r=".9"><stop stop-color="#FFFFFF"/><stop offset=".16" stop-color="{tint(co,.63)}"/><stop offset=".42" stop-color="{co}"/><stop offset=".75" stop-color="{darker(co,.13)}"/><stop offset="1" stop-color="{darker(co,.43)}"/></radialGradient>')
   s.circle(px,py,r*2.05,f'url(#{uid}glow{i})')
   fill=f'url(#{uid}n{i})'
  s.circle(px,py,r+.38,'#F6FBFF' if not mono else 'none',op=.93)
  s.circle(px,py,r,fill,extra=f'data-dimension="{d["id"]}"')
  if not mono and not mini:
   s.e.append(f'<ellipse cx="{px-1.0}" cy="{py-1.8}" rx="1.12" ry=".6" fill="white" opacity=".42" transform="rotate(-26 {px-1.0} {py-1.8})"/>')
 if word and not mini:
  wordcolor=P['navy'] if (hero and dark) else fg
  s.t(50,56,'OSDGs',40,wordcolor,True,'middle',fam='Liberation Serif')
  q=s.labels[-1];q.update(x=x+q['x']*w/100,y=y+q['y']*w/100,w=q['w']*w/100,h=q['h']*w/100)
 s.e.append('</g>')

def lockup(s,x,y,w,orient='horizontal',mode='light',lang='bilingual'):
 dark=mode in ['dark','reverse'];fg='white' if dark else 'navy';variant='reverse' if mode=='reverse' else 'mono' if mode=='mono' else 'master'
 if orient=='horizontal':
  h=w/3.3;emblem(s,x,y,h,variant,dark,True)
  xx=x+h*1.06
  s.line(x+h*.98,y+h*.16,x+h*.98,y+h*.85,'#9CB6D3' if dark else 'line',.25)
  s.t(xx,y+h*.53,'OSDGs',h*1.26,fg,True,fam='Liberation Serif')
  if lang=='bilingual':
   s.t(xx,y+h*.73,'开源发展目标',h*.32,fg)
   s.t(xx,y+h*.88,'Open Source Development Goals',h*.18,fg,fam='Inter')
  elif lang=='zh':s.t(xx,y+h*.79,'开源发展目标',h*.38,fg)
  else:s.t(xx,y+h*.78,'Open Source Development Goals',h*.20,fg,fam='Inter')
 else:
  emblem(s,x+w*.16,y,w*.68,variant,dark,True)
  s.t(x+w*.5,y+w*.72,'OSDGs',w*.55,fg,True,'middle',fam='Liberation Serif')
  s.t(x+w*.5,y+w*.83,'开源发展目标',w*.19,fg,False,'middle')
  s.t(x+w*.5,y+w*.93,'Open Source Development Goals',w*.10,fg,False,'middle',fam='Inter')

def wave(s,x,y,w,h,co='#409CE0',op=.15,phase=0):
 s.uid+=1;uid=f'wave{s.uid}'
 defs(s,f'<linearGradient id="{uid}" x1="0" y1="1" x2="1" y2="0"><stop stop-color="{co}" stop-opacity="0"/><stop offset=".46" stop-color="{co}" stop-opacity="{op}"/><stop offset="1" stop-color="#94DBEE" stop-opacity="{op*.35}"/></linearGradient>')
 for i in range(3):
  d=f'M{x} {y+h*(.20+i*.15)} C{x+w*.26} {y+h*(1.00-i*.15)} {x+w*.51} {y+h*(-.15+i*.13)} {x+w} {y+h*(.53+i*.18)} L{x+w} {y+h} L{x} {y+h}Z'
  s.path(d,None,0,f'url(#{uid})',1)
  s.path(d,co,.15,fill='none',op=op*.36)

def dimension_card(s,d,x,y,w,h,style='solid'):
 s.uid+=1;uid=f'card{s.uid}';co=d['color'];hi=d['hero_color'];solid=style=='solid';fg='white' if solid else 'navy'
 if solid:
  fill=grad(s,uid,co,darker(hi,.15));s.rect(x,y,w,h,fill,rx=2.0)
  wave(s,x,y+h*.62,w,h*.38,'#FFFFFF',.18)
 else:
  s.rect(x,y,w,h,tint(hi,.94),rx=1.5);s.rect(x,y,w,1,co)
 s.t(x+4,y+7,d['id'][1:],13,fg,True,fam='Inter')
 s.t(x+w-4,y+7,d['pillar']+' · '+d['source_code'],7,fg if solid else 'muted',False,'end',fam='Inter')
 icon(s,d['icon'],x+w-17,y+11.5,11,fg,1.65)
 s.t(x+4,y+18.5,d['name_zh'],11.4,fg,True)
 s.wrap(x+4,y+25.5,d['name_en'],w-23,7.1,fg,leading=3.2,fam='Inter')

def export_core():
 for variant in ['master','display','compact','mono','reverse']:
  s=S(100,100,None,f'OSDGs 开源发展目标：星座网络 {variant}')
  emblem(s,0,0,100,variant,variant=='reverse',False)
  s.save(ROOT/'assets/master'/f'osdgs-symbol-{variant}',px=1800,outline=False)
 for variant in ['master','display','mono','reverse']:
  s=S(100,100,None,'OSDGs 开源发展目标')
  emblem(s,0,0,100,variant,variant=='reverse',True)
  s.save(ROOT/'assets/master'/f'osdgs-emblem-{variant}',px=1800,outline=True)
 for orient in ['horizontal','vertical']:
  for mode in ['light','dark','mono','reverse']:
   w,h=(165,50) if orient=='horizontal' else (100,96)
   s=S(w,h,None,f'OSDGs 开源发展目标 {orient} {mode}')
   lockup(s,0,0,w,orient,mode)
   s.save(ROOT/'assets/lockups'/f'osdgs-{orient}-{mode}',px=2000,outline=True)
 for lang in ['zh','en']:
  s=S(165,50,None);lockup(s,0,0,165,lang=lang)
  s.save(ROOT/'assets/lockups'/f'osdgs-horizontal-{lang}',px=2000,outline=True)
 for d in DIMS:
  for style in ['solid','light']:
   s=S(80,36,None,d['id']+' '+d['name_zh']);dimension_card(s,d,0,0,80,36,style)
   s.save(ROOT/'assets/dimensions'/f'{d["id"]}-{style}',px=1400,outline=True)
  for mode,co in [('color',d['color']),('navy',P['navy']),('white','#FFFFFF')]:
   s=S(24,24,None);icon(s,d['icon'],1,1,22,co)
   s.save(ROOT/'assets/icons'/f'{d["id"]}-{d["icon"]}-{mode}',px=400,outline=False)
 # compact navigation strip / one icon per dimension, never a ten-chapter menu.
 s=S(166,13,None,'十个观察维度 / 视觉编号')
 for i,d in enumerate(DIMS):
  xx=i*16.6;s.rect(xx,0,15,1.4,d['color']);icon(s,d['icon'],xx+1,3,6,d['color']);s.t(xx+9,7.8,d['id'][1:],7.9,d['color'],True,fam='Inter')
 s.save(ROOT/'assets/dimensions/dimension-strip',px=2200)
 # Full dimension board for the executive summary.
 s=S(166,196,None,'四项发展目标下的十个观察维度')
 for i,d in enumerate(DIMS):dimension_card(s,d,(i%2)*85,(i//2)*38,81,34)
 s.t(0,195,'四项发展目标 / 十个观察维度 / 二十九项候选指标',8.3,'muted')
 s.save(ROOT/'assets/dimensions/dimension-board',px=1800)
 # Per-dimension tags, avoiding icon-only navigation.
 for d in DIMS:
  s=S(52,8,None);s.rect(0,0,52,8,tint(d['color'],.94),rx=1);s.rect(0,0,1,8,d['color']);icon(s,d['icon'],3,1.4,5.2,d['color']);s.t(10,5.7,d['id'],7.8,d['color'],True,fam='Inter');s.t(21,5.7,d['name_zh'],8.2,'navy')
  s.save(ROOT/'assets/dimensions'/f'{d["id"]}-tag',px=900)

def extra_assets():
 # Plain wordmarks and transparent explicit mode labels for professional handoff.
 for dark in [False,True]:
  for mode in ['display','master','compact']:
   s=S(100,100,None);emblem(s,0,0,100,mode,dark,mode!='compact');s.save(ROOT/'assets/master'/f'osdgs-{mode}-{"dark" if dark else "light"}',px=2400,outline=True)
 for co,name in [('navy','navy'),('white','white')]:
  s=S(145,38,None);s.t(0,22,'OSDGs',59,co,True,fam='Liberation Serif');s.t(0,33,'Open Source Development Goals · 开源发展目标',9.5,co);s.save(ROOT/'assets/lockups'/f'wordmark-{name}',px=2200,outline=True)
 # Web tokens preserved as data, no animated behavior implied.
 web=ROOT/'assets/web';web.mkdir(parents=True,exist_ok=True)
 (web/'tokens.css').write_text(':root {\n  --osdgs-navy: #102950;\n'+''.join(f'  --{d["id"].lower()}: {d["color"]};\n  --{d["id"].lower()}-hero: {d["hero_color"]};\n' for d in DIMS)+'}\n')

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--svg-only',action='store_true',help='Export SVG and outlined SVG without PNG')
 parser.add_argument('--local-pdf',action='store_true',help='Also render ignored local PDF exports; never commit them')
 args=parser.parse_args()
 global LOCAL_PDF,PNG
 LOCAL_PDF=args.local_pdf;PNG=not args.svg_only
 required=[FONT_CJK,FONT_CJK_B,FONT_LAT,FONT_LAT_B,SERIF,SERIF_B]
 missing=[p for p in required if not Path(p).is_file()]
 if missing: raise SystemExit('Missing system fonts (not distributed): '+', '.join(missing))
 export_core();extra_assets()
 bad=[item for item in QA if item['out_of_bounds']]
 (ROOT/'audit').mkdir(exist_ok=True)
 (ROOT/'audit/render-checks.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
 if bad: raise SystemExit('Text bounds need review: '+str(bad))
 print('Exported',len(QA),'approved SVG assets; PNG:',PNG,'local PDF:',LOCAL_PDF)
if __name__=='__main__':main()
