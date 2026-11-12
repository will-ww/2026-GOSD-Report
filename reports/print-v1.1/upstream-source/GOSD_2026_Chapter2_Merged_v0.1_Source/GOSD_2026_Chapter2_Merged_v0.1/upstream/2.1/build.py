"""GOSD 2.1 v0.3: three A4 portrait evidence compositions; no repository writes."""
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

WORLD=json.loads((D/'public-developers.json').read_text())
CHINA=json.loads((D/'public-CN-developers.json').read_text())
META=json.loads((D/'public-meta.json').read_text())
TOP=WORLD['leaderboards'][1]['data'][:20]
PROVINCES=CHINA['leaderboards'][1]['data']
TOTALS=WORLD['trends']
SOUTH=[r for r in WORLD['leaderboards'][1]['data'] if r['code'] in ['BR','ID','VN','PH','EG','ZA']]
CUR={r['region']:r for r in readcsv('five_groups_current.csv')}
TREND=readcsv('five_groups_active_trend.csv')

def scenario(vals):
    g=(vals[-1]/vals[0])**.25-1;v=vals[-1];slow=[]
    for h in range(1,5):v*=1+g*.8**h;slow.append(v)
    return {'annual_growth':g,'history':vals,'continued':[vals[-1]*(1+g)**h for h in range(1,5)],'slowing':slow}
SC={k:scenario([float(r[k])/1e4 for r in TREND]) for k,c in GROUPS}
GS={k:scenario([v/div for v in t['values']]) for k,t,div in zip(['total','active','china'],TOTALS,[1e8,1e4,1e4])}

def first():
    b=Figure();b.title(0,22,1,'GitHub 活跃开发者分布');b.title(622,22,2,'主要国家 · 前 20')
    b.text(1000,49,'万人',16,'muted',anchor='end');b.line(602,0,602,441)
    src=ET.parse(R/'assets/world_map.svg').getroot()
    scale=3.45;tx=-15;ty=24
    b.items.append(f'<g transform="translate({tx},{ty}) scale({scale})">')
    nc=0
    for e in list(src):
        tag=e.tag.rsplit('}',1)[-1]
        if (tag=='path' and e.get('fill')=='#E8F0F1') or (tag=='circle' and float(e.get('cy'))<85):
            e=copy.deepcopy(e)
            if tag=='path':e.set('fill','#E7EEF2')
            else:nc+=1
            b.items.append(ET.tostring(e,encoding='unicode'))
    b.items.append('</g>');assert nc==171
    for cx,cy,x,y,t in [(45.703,33.978,9,96,'美国 494.1 万'),(124.179,34.207,396,84,'中国 250.5 万'),(118.55,42.376,408,270,'印度 285.1 万'),(63.499,63.329,35,308,'巴西 193.5 万')]:
        b.line(tx+cx*scale,ty+cy*scale,x+50,y+4,'#9CB0BD',1.2);b.rect(x-3,y-19,tw(t,18,True)+6,25,'white');b.text(x,y,t,18,'ink',True)
    for x,n in [(17,10),(169,100),(337,400)]:
        b.circle(x+17,378,math.sqrt(n/400)*4.74*scale);b.text(x+42,384,f'{n} 万',17,'muted')
    b.text(0,414,'圆面积表示规模；空白或未绘制不表示零。',16.5,'muted')
    for i,r in enumerate(TOP):
        y=66+i*19.15;v=r['value']/1e4
        b.text(622,y,f'{i+1:02}',15.8,'muted');name=r['name_zh']
        b.text(652,y,name,16.3,'ink',i<4)
        b.rect(754,y-11.5,168,12,'pale');b.rect(754,y-11.5,168*v/500,12,'teal')
        b.text(1000,y,f'{v:.2f}',16.3,'ink',i<4,'end')
    b.line(0,446,1000,446)
    b.title(0,478,3,'参与基础与当期活跃');b.title(367,478,4,'五域综合统计与中国平台补充')
    b.text(0,511,'累计 1.94 亿',19,'blue',True);b.text(175,511,'活跃 2,890.4 万',18,'teal',True)
    b.text(0,539,'2022 = 100',16,'muted');x=40;y=564;w=249;h=153
    for v in [100,150,200,250]:
        yy=y+h-(v-100)/150*h;b.line(x,yy,x+w,yy);b.text(x-8,yy+5,str(v),15.5,'muted',anchor='end')
    for z,c,off in [(GS['total'],'blue',-10),(GS['active'],'teal',20)]:
        vals=[v/z['history'][0]*100 for v in z['history']];pts=[(x+i*w/4,y+h-(v-100)/150*h) for i,v in enumerate(vals)]
        b.path(pts,c,3)
        for px,py in pts:b.circle(px,py,3.3,c)
        b.text(pts[-1][0],pts[-1][1]+off,f'{vals[-1]:.1f}',17,c,True,'end')
    for i in [0,2,4]:b.text(x+i*w/4,741,str(2022+i),16,'muted',anchor='middle')
    b.line(0,773,24,773,'blue',3);b.text(33,779,'累计规模',16,'blue');b.line(160,773,184,773,'teal',3);b.text(193,779,'当期活跃',16,'teal')
    b.line(345,468,345,800)
    b.text(685,512,'累计／万人',16,'muted',anchor='end');b.text(1000,512,'活跃／万人',16,'muted',anchor='end')
    for i,(k,c) in enumerate(GROUPS):
        yy=543+i*29;row=CUR[k];total=float(row['total_developers'])/1e4;active=float(row['active_developers'])/1e4
        b.text(367,yy,NAMES.get(k,k),17,'ink',k=='中国')
        b.rect(455,yy-12,140,14,'pale');b.rect(455,yy-12,140*total/3100,14,c);b.text(685,yy,f'{total:,.1f}',17,'ink',anchor='end')
        b.rect(728,yy-12,186,14,'pale');b.rect(728,yy-12,186*active/700,14,c);b.text(1000,yy,f'{active:,.1f}',17,c,True,'end')
    b.line(367,680,1000,680)
    b.text(367,705,'中国跨平台活跃：250.48 万 + 约 120 万 ≈ 370 万',17,'teal',True)
    b.items.append('<defs><pattern id="local-hatch" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#E7F3F1"/><path d="M-2,2 L2,-2 M0,8 L8,0 M6,10 L10,6" stroke="#007D78" stroke-width="1.5"/></pattern></defs>')
    b.rect(367,722,420*250.482488/370.482488,17,'blue');b.rect(367+420*250.482488/370.482488,722,420*120/370.482488,17,'url(#local-hatch)')
    b.text(803,737,'去重后约 370 万',18,'teal',True)
    b.text(367,763,'实色：GitHub；斜线：国内平台去重补充。',16,'muted')
    b.text(367,790,'五域为独立综合统计，不再叠加这约 120 万。',16,'muted')
    b.save('01-global-current')

def axes(b,x,y,w,h,ymax,ticks,small=False):
    b.rect(x+w*.5,y,w*.5,h,'pale')
    for v in ticks:
        yy=y+h-v/ymax*h;b.line(x,yy,x+w,yy);b.text(x-8,yy+5,f'{v:g}',15.2,'muted',anchor='end')
    for yr in [2022,2026,2030]:b.text(x+(yr-2022)/8*w,y+h+25,str(yr),15.5,'muted',anchor='middle')
    b.line(x+w*.5,y,x+w*.5,y+h,'#A8BAC5',1.2,'4 5')
def draw_scenario(b,s,x,y,w,h,ymax,c,band=False):
    points=lambda yrs,vals:[(x+(yr-2022)/8*w,y+h-v/ymax*h) for yr,v in zip(yrs,vals)]
    hp=points(range(2022,2027),s['history']);up=points(range(2026,2031),[s['history'][-1]]+s['continued']);lo=points(range(2026,2031),[s['history'][-1]]+s['slowing'])
    if band:b.path(up+lo[::-1],c,0,fill=c,opacity=.1)
    b.path(hp,c,3);b.path(up,c,2.3,dash='7 5');b.path(lo,c,1.8,dash='2 5')
    for px,py in hp:b.circle(px,py,2.6,c)

def second():
    b=Figure();b.title(0,22,1,'五域历史与 2030 条件情景')
    b.line(651,15,678,15,'ink',2.7);b.text(687,21,'历史',16,'muted')
    b.line(759,15,786,15,'ink',2.3,'7 5');b.text(795,21,'延续',16,'muted')
    b.line(866,15,894,15,'ink',2,'2 5');b.text(903,21,'放缓',16,'muted')
    b.text(0,51,'活跃／万人',16,'muted');x=48;y=73;w=589;h=195
    axes(b,x,y,w,h,1300,[0,400,800,1200])
    for k,c in GROUPS:draw_scenario(b,SC[k],x,y,w,h,1300,c)
    b.text(362,64,'2027—2030：情景',15.5,'muted')
    b.text(778,55,'2026',16,'muted',anchor='end');b.text(1000,55,'2030 放缓—延续',16,'muted',anchor='end')
    for i,(k,c) in enumerate(GROUPS):
        yy=94+i*42;s=SC[k];b.text(660,yy,NAMES.get(k,k),17,c,True);b.text(788,yy,f'{s["history"][-1]:.1f}',17,'ink',anchor='end');b.text(1000,yy,f'{s["slowing"][-1]:,.0f}—{s["continued"][-1]:,.0f}',18,c,True,'end')
    b.text(660,293,'范围表示两种假设，不是置信区间。',15.8,'muted')
    b.line(0,310,1000,310)
    b.title(0,342,2,'全球与中国：规模增长与活跃增长分开观察')
    sets=[('total','全球累计／亿人','blue',5,[0,2,4]),('active','全球活跃／万人','teal',6000,[0,3000,6000]),('china','中国 GitHub 活跃／万人','china',550,[0,250,500])]
    for j,(k,title,c,ymax,ticks) in enumerate(sets):
        left=j*345;b.text(left,375,title,18,'ink',True);s=GS[k]
        x=left+44;y=401;w=246;h=115;axes(b,x,y,w,h,ymax,ticks,True);draw_scenario(b,s,x,y,w,h,ymax,c,True)
        if k=='total':current=f'{s["history"][-1]:.2f}';out=f'{s["slowing"][-1]:.2f}—{s["continued"][-1]:.2f}'
        else:current=f'{s["history"][-1]:,.1f}';out=f'{s["slowing"][-1]:,.0f}—{s["continued"][-1]:,.0f}'
        b.text(left,568,f'2026：{current}  →  2030：{out}',16,c,True)
    b.line(0,585,1000,585)
    b.title(0,616,3,'全球南方细分：增长速度与现有规模并不相同')
    b.circle(688,610,4,'soft',False);b.text(702,616,'2025',16,'muted');b.rect(789,604,25,10,'south');b.text(824,616,'2026',16,'muted')
    b.text(0,646,'GitHub 口径',16,'muted');b.text(773,646,'活跃／万人',16,'muted',anchor='end');b.text(900,646,'同比增长',16,'muted',anchor='end');b.text(1000,646,'净增／万',16,'muted',anchor='end')
    for i,r in enumerate(SOUTH):
        yy=670+i*24;v=r['value']/1e4;prev=(r['value']-r['change'])/1e4;growth=(v/prev-1)*100
        b.text(0,yy,r['name_zh'],17,'ink',True);b.rect(142,yy-11,515,11,'pale');b.rect(142,yy-11,515*v/200,11,'south');b.circle(142+515*prev/200,yy-5.5,4.6,'soft',False)
        b.text(773,yy,f'{v:.2f}',17,'south',True,'end');b.text(900,yy,f'+{growth:.1f}%',17,'ink',anchor='end');b.text(1000,yy,f'+{r["change"]/1e4:.2f}',17,'ink',anchor='end')
    b.save('02-trends-2030')

def short(n):
    for a in ['壮族自治区','维吾尔自治区','回族自治区','特别行政区','自治区','省','市']:n=n.replace(a,'')
    return n

def third():
    b=Figure();b.title(0,22,1,'中国活跃开发者 · 34 个省级地区');b.title(612,22,2,'规模与净增 · 前 20')
    b.text(0,55,'全国 250.48 万',21,'blue',True);b.text(274,55,'同比净增 30.40 万',19,'teal',True)
    pmap={short(r['name_zh']):r for r in PROVINCES}
    geom=json.loads((D/'china-drawing-geometry.json').read_text());pal=['#E5EFF4','#BDDAE5','#88B7CE','#4F91B5','#155F8B'];bounds=[1,5,15,30]
    scale=.91;tx=-166;ty=47
    for f in geom['features']:
        name=f['name'];fill='none' if name=='十段线' else 'white' if name=='南海诸岛' else pal[sum(pmap[name]['value']/1e4>=q for q in bounds)]
        b.items.append(f'<path d="{f["path"]}" transform="translate({tx},{ty}) scale({scale})" fill="{fill}" fill-rule="evenodd" stroke="#8DA7B4" stroke-width="0.8"/>')
    centers={f['name']:f['center'] for f in geom['features']}
    for name,lx,ly in [('北京',476,178),('上海',500,235),('浙江',502,274),('台湾',502,322),('广东',433,390),('四川',168,304)]:
        lon,lat=centers[name];px=tx+scale*(185.5365860534777+(lon-73.502355)*.75*11.018439414576823);py=ty+scale*(18+(53.563624-lat)*11.018439414576823)
        if name!='四川':b.path([(px,py),(lx-12,ly-6),(lx-4,ly-6)],'#7F9AA9',1.2);b.circle(px,py,2.1,'blue')
        b.rect(lx-3,ly-17,tw(name,17.5,True)+6,23,'white');b.text(lx,ly,name,17.5,'ink',True)
    b.text(0,439,'万人',15.8,'muted')
    for i,(c,t) in enumerate(zip(pal,['<1','1—<5','5—<15','15—<30','≥30'])):
        xx=57+i*101;b.rect(xx,426,22,13,c);b.text(xx+28,439,t,15.5,'muted')
    b.line(591,0,591,447)
    b.text(869,49,'活跃／万',16,'muted',anchor='end');b.text(1000,49,'净增／万',16,'muted',anchor='end')
    for i,r in enumerate(PROVINCES[:20]):
        yy=72+i*19.15;v=r['value']/1e4;inc=r['change']/1e4
        b.text(612,yy,f'{i+1:02}',15.5,'muted');b.text(644,yy,short(r['name_zh']),16.8,'ink',i<5)
        b.rect(712,yy-11.5,90,12,'pale');b.rect(712,yy-11.5,90*v/55,12,'blue');b.text(869,yy,f'{v:.2f}',16.5,'ink',i<5,'end')
        b.rect(890,yy-11.5,39*inc/7,12,'teal');b.text(1000,yy,f'+{inc:.2f}',16.5,'teal',False,'end')
    b.line(0,464,1000,464);b.title(0,497,3,'同比增速：看增长，也看基数');b.title(535,497,4,'份额对照：存量与增量')
    total=sum(r['value'] for r in PROVINCES);net=sum(r['change'] for r in PROVINCES);rate=net/(total-net)*100
    b.text(0,528,'全国 +13.8%；下列七地为活跃规模前七位。',16.2,'muted')
    x=70;w=353;y0=560
    for i,r in enumerate(PROVINCES[:7]):
        yy=y0+i*30;g=r['change']/(r['value']-r['change'])*100;c='china' if r['code'] in ['CN-TW','CN-ZJ'] else 'blue'
        b.text(0,yy,short(r['name_zh']),17,'ink',r['code']=='CN-ZJ');b.rect(x,yy-12,w*g/22,14,c);b.text(493,yy,f'{g:.1f}%',17,c,True,'end')
    b.line(x+w*rate/22,542,x+w*rate/22,752,'#547487',1.4,'3 4')
    b.text(0,786,'虚线：全国增速；净增不是首次参与人数。',16,'muted')
    b.line(514,487,514,797)
    segments=[PROVINCES[:3],PROVINCES[3:5],PROVINCES[5:]];labels=['京沪粤','台湾＋浙江','其余 29 地'];colors=['blue','china','soft']
    b.text(535,530,'同一组地区，比较活跃份额与净增份额',16.2,'muted')
    for j,(field,den,title) in enumerate([('value',total,'当期活跃'),('change',net,'同比净增')]):
        yy=573+j*91;b.text(535,yy-10,title,17,'ink',True);xx=535
        for seg,c in zip(segments,colors):
            share=sum(r[field] for r in seg)/den;b.rect(xx,yy+3,465*share,29,c);b.text(xx+465*share/2,yy+24,f'{share*100:.1f}%',17,'white',True,'middle');xx+=465*share
    for i,(t,c) in enumerate(zip(labels,colors)):
        xx=535+i*157;b.rect(xx,711,12,12,c);b.text(xx+19,723,t,16.4,'ink')
    b.rect(535,745,465,55,'pale');b.text(547,768,'台湾＋浙江：净增份额高于活跃份额',16.3,'ink');b.text(547,793,'约 4.4 个百分点',22,'china',True)
    b.save('03-china-regions')

def esc(t):return str(t).replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
def box(x,y,w,t,fs=10.3,lead=16.8,c='ink',bold=False,sans=False):
    return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{\fontsize{{{fs}}}{{{lead}}}\selectfont\color{{{c}}}'+(r'\sffamily ' if sans or bold else '')+(r'\bfseries ' if bold else '')+esc(t)+'}\n'

def compile_tex():
    env=os.environ.copy();env['TEXMF']='{/usr/share/texmf,/usr/share/texlive/texmf-dist}'
    var=B/'texmf-var';var.mkdir(exist_ok=True);env['TEXMFVAR']=str(var);env['TEXFORMATS']=str(var)
    old=REPO/'editions/insights/chapters/02/v0.2/.build/texmf-var/xelatex.fmt'
    if old.exists() and not (var/'xelatex.fmt').exists():shutil.copy2(old,var/'xelatex.fmt')
    if not (var/'xelatex.fmt').exists():
        with (O/'format-build.txt').open('w') as f:subprocess.run(['xelatex','-ini','-etex','-interaction=nonstopmode','-jobname=xelatex',f'-output-directory={var}',r'\input xelatex.ini'],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    for i in [1,2]:
        with (O/f'build-{i}.txt').open('w') as f:subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory=output','report.tex'],cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)

def main():
    for p in [B/'assets',B/'fonts',O,F,R/'review']:p.mkdir(parents=True,exist_ok=True)
    from fontTools.ttLib import TTCollection
    for family in ['Sans','Serif']:
        for weight in ['Regular','Bold']:
            dest=B/'fonts'/f'Noto{family}CJKsc-{weight}.otf'
            if not dest.exists():
                coll=TTCollection(f'/usr/share/fonts/opentype/noto/Noto{family}CJK-{weight}.ttc');coll.fonts[2].save(dest);coll.close()
    export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
    first();second();third()
    (R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
    (D/'scenarios-v03.json').write_text(json.dumps({'units':{'five_groups':'万人','total':'亿人','active':'万人','china':'万人'},'groups':SC,'global_and_china':GS,'damping':.8,'anchor':'2026报告年度','forecast_years':[2027,2028,2029,2030],'china_five_group_2026':454.534,'china_cross_platform_current_approx_10k':370,'historical_cross_platform_backfill':False},ensure_ascii=False,indent=2))
    make_tex();compile_tex()
    doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':'GOSD 2026 精要版｜第二章 2.1 竖版图文评审稿 v0.3','author':'全球开源发展报告编制组','subject':'三页综合图文与附录1；主统计期2025-07至2026-06；2030条件情景'})
    doc.set_toc([[1,'2.1 全球开源活跃地图',1],[2,'趋势与2030条件情景',2],[2,'中国区域参与结构',3],[1,'附录1 指标、口径与来源',4],[2,'历史序列、情景测算与评审记录',5]])
    out=O/'GOSD_2026_Chapter2_Portrait_v0.3.pdf';doc.save(out,garbage=4,deflate=True)
    print('BUILT',out,'pages',len(doc));print(json.dumps([{'figure':q['figure'],'outside':len(q['out_of_bounds']),'overlaps':len(q['overlaps'])} for q in QA],ensure_ascii=False))

if __name__=='__main__':
    from content import make_tex
    main()
