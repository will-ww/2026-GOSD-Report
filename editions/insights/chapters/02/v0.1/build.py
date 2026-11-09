"""Build the compact 2.1 sample from exact archived data and approved brand assets.

No PDF/font enters Git. Run from any working directory: python3 build.py.
Figures are editable SVG; all content comes from content.json.
"""
from pathlib import Path
import csv, copy, hashlib, html, json, math, os, subprocess
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTCollection
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
ARCHIVE = REPO / 'reports/round2-v2.0/source/chapters/02'
DATA = ARCHIVE / 'modules/02/data/21'
BUILD = ROOT / '.build'
OUTPUT = ROOT / 'output'
FIG = ROOT / 'figures'
for d in [BUILD/'fonts', BUILD/'assets', OUTPUT, FIG, ROOT/'review', ROOT/'data']:
    d.mkdir(parents=True, exist_ok=True)

C = dict(ink='#13253D', muted='#5C6B7A', line='#D9DFE4', pale='#F1F6F8',
         teal='#007D78', blue='#155FA8', land='#E7EEF2', white='#FFFFFF')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BFONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
PF = ImageFont.truetype(FONT,100,index=2)
BF = ImageFont.truetype(BFONT,100,index=2)
QA = []

def width(t, pt, bold=False):
    return (BF if bold else PF).getlength(t)/100*pt*25.4/72

class SVG:
    def __init__(self, w, h):
        self.w,self.h=w,h;self.parts=[];self.labels=[]
        self.rect(0,0,w,h,'white')
    def rect(self,x,y,w,h,c):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{C.get(c,c)}"/>')
    def line(self,x,y,x2,y2,c='line',sw=.2):
        self.parts.append(f'<path d="M{x},{y} L{x2},{y2}" fill="none" stroke="{C.get(c,c)}" stroke-width="{sw}"/>')
    def text(self,x,y,t,pt=9,c='ink',bold=False,anchor='start'):
        w=width(t,pt,bold);left=x if anchor=='start' else x-w if anchor=='end' else x-w/2
        self.labels.append(dict(text=t,x=left,y=y-pt*.3528*.85,w=w,h=pt*.3528*1.08))
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK SC" font-size="{pt*.3527778}" font-weight="{700 if bold else 400}" fill="{C.get(c,c)}" text-anchor="{anchor}">{html.escape(t)}</text>')
    def save(self,name):
        p=FIG/f'{name}.svg'
        p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">'+''.join(self.parts)+'</svg>')
        over=[a for a in self.labels if a['x']<-.2 or a['x']+a['w']>self.w+.2 or a['y']<-.2 or a['y']+a['h']>self.h+.2]
        overlaps=[]
        for i,a in enumerate(self.labels):
            for b in self.labels[i+1:]:
                dx=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])
                dy=min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])
                if dx>.35 and dy>.5:overlaps.append([a['text'],b['text']])
        QA.append(dict(asset=name,overflow=over,overlaps=overlaps))
        export_pdf(p,BUILD/'assets'/f'{name}.pdf')

def export_pdf(src,dest):
    subprocess.run(['inkscape',str(src),'--export-type=pdf',f'--export-filename={dest}'],check=True,capture_output=True)

def readcsv(name):
    src=DATA/name;dest=ROOT/'data'/name
    manifest=ROOT/'review/sources.json'
    if manifest.exists():
        record=next(r for r in json.loads(manifest.read_text())['records'] if r['path']==f'data/{name}')
        assert hashlib.sha256(src.read_bytes()).hexdigest()==record['sha256'],f'Source version changed: {name}'
    dest.write_bytes(src.read_bytes())
    return list(csv.DictReader(src.open()))

def trunc2(x):
    return f'{math.floor(float(x)/10000*100)/100:.2f}'

def world_map():
    """Retain archive's approved geometry and area-scaled circles, replace labels.

    This is a layout/restyle transformation, never a geographic reprojection.
    Natural Earth public-domain geometry is already CHN/TWN-merged upstream.
    """
    original=ARCHIVE/'modules/02/figures/21/world_map.svg'
    root=ET.parse(original).getroot()
    items=list(root); geometry=[];circles=[]
    for e in items:
        tag=e.tag.rsplit('}',1)[-1]
        if tag=='path' and e.get('fill')==C['land']:
            geometry.append(copy.deepcopy(e))
        elif tag=='path' and e.get('fill')=='#E8F0F1':
            v=copy.deepcopy(e);v.set('fill',C['land']);geometry.append(v)
        elif tag=='circle' and float(e.get('cy'))<85:
            v=copy.deepcopy(e);v.set('fill',C['teal']);v.set('opacity','0.82');circles.append(v)
    assert len(geometry)>200 and len(circles)==171
    s=SVG(166,75)
    s.text(0,4,'GitHub 地理记录',8.4,'muted',True)
    s.text(166,4,'2025.07—2026.06',8.4,'muted',False,'end')
    # The uniform transform preserves geography and area relationships.
    s.parts.append('<g transform="translate(0,-10.5) scale(0.9764705882)">')
    s.parts.extend(ET.tostring(v,encoding='unicode') for v in geometry+circles)
    s.parts.append('</g>')
    # Four labeled anchors; all other bubble positions are inherited unchanged.
    anchors=[(45.703,33.978,11,13,'美国 494.14 万'),
             (124.179,34.207,130,14,'中国 250.48 万'),
             (118.550,42.376,130,52,'印度 285.08 万'),
             (63.499,63.329,24,59,'巴西 193.45 万')]
    for x,y,lx,ly,label in anchors:
        px=x*.9764705882;py=y*.9764705882-10.5
        s.line(px,py,lx+9,ly+1,'#97AAB6',.18)
        w=width(label,8.6);s.rect(lx-1,ly-3.1,w+2,4.5,'white');s.text(lx,ly,label,8.6,'ink',True)
    for x,v in [(4,10),(39,100),(78,400)]:
        r=math.sqrt(v*10000/4000000)*4.74*.9764705882
        s.parts.append(f'<circle cx="{x+3}" cy="69" r="{r}" fill="{C["teal"]}" opacity=".82" stroke="white" stroke-width=".15"/>')
        s.text(x+10,70.2,f'{v} 万人',8.4,'muted')
    s.text(166,70.2,'圆面积表示活跃规模',8.3,'muted',False,'end')
    s.save('fig-2-1a-world')
    return dict(source=str(original.relative_to(REPO)),sha256=hashlib.sha256(original.read_bytes()).hexdigest(),geometry_paths=len(geometry),data_circles=len(circles),uniform_scale=.9764705882,geographic_edits=False)

def rank(top):
    s=SVG(166,48)
    s.text(0,4,'活跃规模前 10 国家',9,'ink',True)
    s.text(166,4,'单位：万人；两列使用相同刻度',8.2,'muted',False,'end')
    for i,row in enumerate(top):
        col=i//5;j=i%5;x=col*86;y=12.5+j*6.7
        s.text(x,y,f'{i+1:02d}',8,'muted')
        s.text(x+7,y,row['name_zh'],9,'ink',i<4)
        bx=x+23;bwidth=43;v=float(row['active_developers'])/10000
        s.rect(bx,y-2.8,bwidth,3.8,'pale');s.rect(bx,y-2.8,bwidth*v/500,3.8,'teal')
        s.text(x+80,y,trunc2(row['active_developers']),9,'ink',True,'end')
    for x in [23,109]:
        s.line(x,42,x+43,42)
        for n in [0,250,500]:s.text(x+43*n/500,46,f'{n}',7.6,'muted',False,'middle')
    s.save('fig-2-1b-rank')

def comparison(current,trend):
    cur={r['region']:float(r['active_developers']) for r in current}
    start=trend[0];end=trend[-1]
    assert int(start['year'])==2022 and int(end['year'])==2026
    ordered=sorted(cur,key=lambda k:cur[k],reverse=True)
    derived=[];s=SVG(166,81)
    s.text(34,5,'2026 年活跃规模',9.2,'blue',True)
    s.text(34,10,'万人',8.1,'muted')
    s.text(110,5,'2022—2026 年累计增幅',9.2,'teal',True)
    s.text(110,10,'相对于各组 2022 年人数',8.1,'muted')
    for i,key in enumerate(ordered):
        y=21+i*11.2;v=cur[key]/10000;growth=(cur[key]/float(start[key])-1)*100
        assert cur[key]==float(end[key])
        label='南方六国' if key=='全球南方代表国家' else key
        s.text(0,y,label,10,'ink',True)
        if key=='全球南方代表国家':s.text(0,y+4.2,'代表组',8.6,'muted')
        s.rect(34,y-3,54,4.4,'pale');s.rect(34,y-3,54*v/700,4.4,'blue')
        s.text(103,y+.2,f'{v:.2f}',9.1,'blue',True,'end')
        s.rect(110,y-3,39,4.4,'pale');s.rect(110,y-3,39*growth/140,4.4,'teal')
        s.text(166,y+.2,f'+{growth:.1f}%',9.1,'teal',True,'end')
        derived.append(dict(group=label+(('代表组') if label=='南方六国' else ''),active_2022=int(float(start[key])),active_2026=int(cur[key]),multiple=cur[key]/float(start[key]),cumulative_growth_pct=growth))
    s.line(34,72,88,72);s.line(110,72,149,72)
    for v in [0,350,700]:s.text(34+54*v/700,77,f'{v}',8,'muted',False,'middle')
    for v in [0,70,140]:s.text(110+39*v/140,77,f'{v}%',8,'muted',False,'middle')
    s.save('fig-2-2-size-growth')
    (ROOT/'data/derived-comparison.json').write_text(json.dumps(derived,ensure_ascii=False,indent=2)+'\n')
    return derived

def texescape(s):
    return s.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
def body(x,y,w,t):return rf'\Body{{{x}}}{{{y}}}{{{w}}}{{{texescape(t)}}}'+'\n'
def label(x,y,w,t,c='ink',size=10.2):
    return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{\sffamily\bfseries\fontsize{{{size}}}{{15}}\selectfont\color{{{c}}}{texescape(t)}}}'+'\n'
def note(x,y,w,t,size=8.2):
    escaped=texescape(t)
    sources={
        '[2-1a]':'https://github.com/will-ww/2026-GOSD-Report/blob/2213819ad32f47ab12e4cccd83ff6691786d8d16/reports/round2-v2.0/source/chapters/02/modules/02/data/21/global_2026_top10.csv',
        '[2-1b]':'https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/c51e3441361407b68f10b339d97eff288319b503/data/processed/chapter2/fig-2-1-3_five_region_active_developers_trend.csv'
    }
    for token,url in sources.items():escaped=escaped.replace(token,rf'\href{{{url}}}{{{token}}}')
    return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{\sffamily\fontsize{{{size}}}{{12.4}}\selectfont\color{{muted}}{escaped}}}'+'\n'
def fig(y,name):return rf'\Box{{22}}{{{y}}}{{166}}{{\includegraphics[width=166mm]{{.build/assets/{name}.pdf}}}}'+'\n'
def rect(x,y,w,h,c):return rf'\Rect{{{x}}}{{{y}}}{{{w}}}{{{h}}}{{{c}}}'+'\n'

def manuscript(d):
    p=d['page1'];q=d['page2'];r=d['review']
    s=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
    s+=r'\begin{canvas}\Header{第二章 · 全球开源生态地图}{teal}\Footer{01}'+'\n'
    s+=rf'\SectionTitle{{teal}}{{{d["section_title"]}}}{{{d["section_subtitle"]}}}{{section21}}'+'\n'
    s+=body(22,68,166,p['lead'])
    s+=label(22,98,166,p['figure_title'],size=10.4)
    s+=fig(108,'fig-2-1a-world')+fig(185,'fig-2-1b-rank')
    s+=label(22,239,80,p['finding1_title'],'teal',10.2)+label(108,239,80,p['finding2_title'],'teal',10.2)
    s+=rf'\Box{{22}}{{247}}{{80}}{{\fontsize{{9.8}}{{15.5}}\selectfont {texescape(p["finding1"])}}}'+'\n'
    s+=rf'\Box{{108}}{{247}}{{80}}{{\fontsize{{9.8}}{{15.5}}\selectfont {texescape(p["finding2"])}}}'+'\n'
    s+=note(22,265,166,p['source'],7.6)
    s+=r'\end{canvas}'+'\n'
    s+=r'\begin{canvas}\Header{2.1 全球开源活跃地图}{teal}\Footer{02}'+'\n'
    s+=rf'\ContinueTitle{{teal}}{{2.1 续 · 规模与增长}}{{{q["title"]}}}'+'\n'
    s+=body(22,65,166,q['lead'])
    s+=label(22,96,166,q['figure_title'],size=10.4)
    s+=note(22,104,166,q['scope'],8.7)
    s+=fig(114,'fig-2-2-size-growth')
    s+=note(22,198,166,q['definitions'],8.4)
    s+=note(22,210,166,q['group_note'],8.4)
    s+=label(22,228,80,q['finding1_title'],'blue',10.2)+label(108,228,80,q['finding2_title'],'teal',10.2)
    s+=rf'\Box{{22}}{{236}}{{80}}{{\fontsize{{9.8}}{{15.5}}\selectfont {texescape(q["finding1"])}}}'+'\n'
    s+=rf'\Box{{108}}{{236}}{{80}}{{\fontsize{{9.8}}{{15.5}}\selectfont {texescape(q["finding2"])}}}'+'\n'
    s+=rect(22,255,166,12,'paper')+rect(22,255,.8,12,'teal')
    s+=rf'\Box{{26}}{{258}}{{158}}{{\sffamily\fontsize{{9.5}}{{14}}\selectfont {texescape(q["action"])}}}'+'\n'
    s+=note(22,270,166,q['source'],7.6)
    s+=r'\end{canvas}'+'\n'
    s+=r'\begin{canvas}\Header{联动建议 · 待评审}{violet}\Footer{R1}'+'\n'
    s+=rf'\pdfbookmark[1]{{摘要与第六章联动建议}}{{feedback}}\ContinueTitle{{violet}}{{执行摘要 × 第六章}}{{{r["title"]}}}'+'\n'
    s+=body(22,65,166,r['intro'])
    s+=label(22,91,166,r['summary_title'],'violet',11)
    s+=rect(22,102,.8,65,'teal')
    s+=body(27,102,161,r['summary_global'])+body(27,143,161,r['summary_south'])
    s+=r'\Rule{22}{172}{188}{line}'+'\n'
    s+=label(22,178,80,r['i01_title'],'blue',10.2)+label(108,178,80,r['i07_title'],'teal',10.2)
    s+=rf'\Box{{22}}{{187}}{{80}}{{\fontsize{{9.8}}{{15.8}}\selectfont {texescape(r["i01"])}}}'+'\n'
    s+=rf'\Box{{108}}{{187}}{{80}}{{\fontsize{{9.8}}{{15.8}}\selectfont {texescape(r["i07"])}}}'+'\n'
    s+=label(22,218,166,r['recommendation_title'],'violet',10.7)
    for i,(key,val) in enumerate(r['recommendation']):
        y=229+i*10.4
        s+=label(22,y,22,key,'ink',9.2)
        s+=rf'\Box{{47}}{{{y}}}{{141}}{{\sffamily\fontsize{{9.1}}{{13.5}}\selectfont {texescape(val)}}}'+'\n'
    s+=note(22,265,166,r['outlook'],8.2)
    s+=r'\end{canvas}\end{document}'+'\n'
    (ROOT/'chapter2.tex').write_text(s)

def setup():
    for family in ['Sans','Serif']:
        for weight in ['Regular','Bold']:
            dest=BUILD/'fonts'/f'Noto{family}CJKsc-{weight}.otf'
            if not dest.exists():
                coll=TTCollection(f'/usr/share/fonts/opentype/noto/Noto{family}CJK-{weight}.ttc')
                assert coll.fonts[2]['name'].getDebugName(6)==f'Noto{family}CJKsc-{weight}'
                coll.fonts[2].save(dest);coll.close()
    export_pdf(REPO/'brand/osdgs/v2.0/assets/master/osdgs-symbol-compact.svg',BUILD/'assets/osdgs-compact.pdf')
    style=(REPO/'editions/insights/chapters/01/v0.5/layout.sty').read_text()
    style=style.replace('GOSD insights chapter 1','GOSD insights chapter 2 sample')
    style=style.replace('第一章评审稿 v0.5','第二章 2.1 样节评审稿 v0.1')
    style=style.replace('从开放协作到公共价值：人工智能时代的开源发展目标与观察方法','全球参与规模与成长群体；正文样节及摘要、第六章联动建议')
    (ROOT/'layout.sty').write_text(style)

def compile_pdf():
    env=os.environ.copy()
    if subprocess.run(['kpsewhich','article.cls'],stdout=subprocess.DEVNULL).returncode:
        env['TEXMF']='{/usr/share/texmf,/usr/share/texlive/texmf-dist}'
    if subprocess.run(['kpsewhich','xelatex.fmt'],env=env,stdout=subprocess.DEVNULL).returncode:
        var=BUILD/'texmf-var';var.mkdir(exist_ok=True)
        env['TEXMFVAR']=str(var);env['TEXFORMATS']=str(var)
        if not (var/'xelatex.fmt').exists():
            with (OUTPUT/'format-build.txt').open('w') as f:
                subprocess.run(['xelatex','-ini','-etex','-interaction=nonstopmode','-jobname=xelatex',f'-output-directory={var}',r'\input xelatex.ini'],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    for i in [1,2]:
        with (OUTPUT/f'build-pass-{i}.txt').open('w') as f:
            subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory=output','-jobname=GOSD_2026_Insights_Chapter2_Sample_v0.1','chapter2.tex'],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)

def main():
    setup()
    top=readcsv('global_2026_top10.csv')
    current=readcsv('five_groups_current.csv');trend=readcsv('five_groups_active_trend.csv')
    readcsv('global_active_excerpt.csv')
    geo=world_map();rank(top);derived=comparison(current,trend)
    manuscript(json.loads((ROOT/'content.json').read_text()))
    (ROOT/'review/chart-validation.json').write_text(json.dumps(dict(geography=geo,labels=QA,derived=derived),ensure_ascii=False,indent=2)+'\n')
    assert all(not q['overflow'] and not q['overlaps'] for q in QA),QA
    compile_pdf()
    import fitz
    file=OUTPUT/'GOSD_2026_Insights_Chapter2_Sample_v0.1.pdf'
    with fitz.open(file) as doc:
        doc.set_page_labels([{'startpage':0,'prefix':'','style':'D','firstpagenum':1},{'startpage':2,'prefix':'R','style':'D','firstpagenum':1}])
        doc.set_toc([[1,'第二章 2.1 全球开源活跃地图',1],[2,'规模与增幅不同序',2],[1,'摘要与第六章联动建议（待评审）',3]])
        temp=file.with_name('finalized.pdf');doc.save(temp,garbage=4,deflate=True)
    temp.replace(file)
    print('Built 2正文 + 1联动评审页; no source data changed.')

if __name__=='__main__':main()
