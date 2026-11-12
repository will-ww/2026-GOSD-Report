"""GOSD 3.5 v0.2: three portrait emerging-ranking compositions; no repository writes."""
from pathlib import Path
import csv, json, math, html, copy, os, subprocess, hashlib, shutil
import xml.etree.ElementTree as ET
from PIL import ImageFont
import fitz

R=Path(__file__).resolve().parent
REPO=R.parent/'gosd-repo'; D=R/'data'; F=R/'figures'; B=R/'.build'; O=R/'output'
C={'ink':'#13253D','muted':'#5C6B7A','line':'#D9E3E9','pale':'#F3F7F9','blue':'#155FA8','teal':'#007D78','china':'#AD4E22','india':'#8E6500','south':'#943B9A','white':'#FFFFFF','soft':'#8BAEBF'}
GROUPS=[('欧洲','teal'),('美国','blue'),('中国','china'),('印度','india'),('全球南方代表国家','south')]
NAMES={'全球南方代表国家':'南方六国'}
PF=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',100,index=2)
BF=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',100,index=2)
QA=[]
for p in [B,B/"fonts",B/"assets",O,F,D,R/"review",R/"sections"]:p.mkdir(parents=True,exist_ok=True)
def tw(t,fs,b=False):return (BF if b else PF).getlength(str(t))*fs/100
def cl(c):return C.get(c,c)
def readcsv(n):return list(csv.DictReader((D/n).open()))
def export(src,dest):subprocess.run(['inkscape',str(src),'--export-type=pdf',f'--export-filename={dest}'],check=True,capture_output=True)

class Figure:
    def __init__(self,height=805):
        self.h=height;self.items=[];self.labels=[];self.rect(0,0,1000,height,'white')
    def rect(self,x,y,w,h,c,opacity=1):self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{cl(c)}" opacity="{opacity}"/>')
    def path(self,pts,c='blue',sw=2,fill='none',dash=None,opacity=1):
        d=' '.join(('M' if i==0 else 'L')+f'{x:.3f},{y:.3f}' for i,(x,y) in enumerate(pts))
        if fill!='none':d+='Z'
        self.items.append(f'<path d="{d}" fill="{cl(fill)}" stroke="{cl(c)}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" opacity="{opacity}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def line(self,x,y,xx,yy,c='line',sw=1,dash=None):self.path([(x,y),(xx,yy)],c,sw,dash=dash)
    def circle(self,x,y,r,c='teal',fill=True):self.items.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{cl(c) if fill else "white"}" stroke="{cl(c)}" stroke-width="1.3"/>')
    def text(self,x,y,t,fs=17,c='ink',bold=False,anchor='start',audit=True):
        t=str(t);w=tw(t,fs,bold);left=x if anchor=='start' else x-w if anchor=='end' else x-w/2
        if audit:self.labels.append(dict(text=t,x=left,y=y-fs*.85,w=w,h=fs*1.05))
        self.items.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK SC" font-size="{fs}" font-weight="{700 if bold else 400}" fill="{cl(c)}" text-anchor="{anchor}">{html.escape(t)}</text>')
    def wrap(self,x,y,t,w,fs=17,c='ink',bold=False,leading=24):
        lines=[];l=''
        for a in t:
            if a=='\n':lines.append(l);l='';continue
            if tw(l+a,fs,bold)>w and l:lines.append(l);l=a
            else:l+=a
        if l:lines.append(l)
        for i,l in enumerate(lines):self.text(x,y+i*leading,l,fs,c,bold)
        return len(lines)*leading
    def title(self,x,y,n,t,c='teal',fs=21):
        self.circle(x+12,y-7,12,c);self.text(x+12,y-1,n,16,'white',True,'middle',False);self.text(x+33,y,t,fs,'ink',True)
    def save(self,name):
        p=F/(name+'.svg');p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{self.h}" viewBox="0 0 1000 {self.h}">'+''.join(self.items)+'</svg>')
        outside=[q for q in self.labels if q['x'] < -0.5 or q['y']<0 or q['x']+q['w']>1000.5 or q['y']+q['h']>self.h]
        overlaps=[]
        for i,a in enumerate(self.labels):
            for b in self.labels[i+1:]:
                dx=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x']);dy=min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])
                if dx>2 and dy>3:overlaps.append([a['text'],b['text'],round(dx,1),round(dy,1)])
        QA.append({'figure':name,'out_of_bounds':outside,'overlaps':overlaps});export(p,B/'assets'/(name+'.pdf'))

def esc(t):return str(t).replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#')
def box(x,y,w,t,fs=10.3,lead=16.8,c='ink',bold=False,sans=False):
    return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{\fontsize{{{fs}}}{{{lead}}}\selectfont\color{{{c}}}'+(r'\sffamily ' if sans or bold else '')+(r'\bfseries ' if bold else '')+esc(t)+'}\n'

def compile_tex():
    env=os.environ.copy();env['TEXMF']='{/usr/share/texmf,/usr/share/texlive/texmf-dist}'
    var=B/'texmf-var';var.mkdir(exist_ok=True);env['TEXMFVAR']=str(var);env['TEXFORMATS']=str(var)
    old=REPO/'editions/insights/chapters/02/v0.3/.build/texmf-var/xelatex.fmt'
    if old.exists() and not (var/'xelatex.fmt').exists():shutil.copy2(old,var/'xelatex.fmt')
    if not (var/'xelatex.fmt').exists():
        with (O/'format-build.txt').open('w') as f:subprocess.run(['xelatex','-ini','-etex','-interaction=nonstopmode','-jobname=xelatex',f'-output-directory={var}',r'\input xelatex.ini'],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    for i in [1,2]:
        with (O/f'build-{i}.txt').open('w') as f:subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory=output','report.tex'],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)



def ensure_fonts():
    from fontTools.ttLib import TTCollection, TTFont
    for family in ['Sans','Serif']:
        for weight in ['Regular','Bold']:
            dest=B/'fonts'/f'Noto{family}CJKsc-{weight}.otf'
            if not dest.exists():
                coll=TTCollection(f'/usr/share/fonts/opentype/noto/Noto{family}CJK-{weight}.ttc')
                coll.fonts[2].save(dest);coll.close()
            font=TTFont(dest)
            cff=font['CFF '].cff
            # Noto TTC shares CFF names across locales; keep metadata consistent with selected SC cmap.
            expected=font['name'].getDebugName(6)
            if cff.fontNames[0]!=expected:
                cff.fontNames=[expected]
                cff.topDictIndex[0].FullName=font['name'].getDebugName(4)
                cff.topDictIndex[0].FamilyName=font['name'].getDebugName(1)
                font.save(dest)
            font.close()
