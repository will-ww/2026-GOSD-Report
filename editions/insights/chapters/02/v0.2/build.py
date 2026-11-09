"""Three integrated evidence boards, self-contained analysis, and Appendix 1.

All numerical graphics are source-derived SVG. Forecasts are conditional scenario
calculations, NOT fitted statistical models, probabilities or confidence bands.
"""
from pathlib import Path
import csv, json, math, html, copy, hashlib, os, re, subprocess, shutil, zipfile
import xml.etree.ElementTree as ET
from PIL import ImageFont
from fontTools.ttLib import TTCollection
import fitz

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[4]
DATA=REPO/'reports/round2-v2.0/source/chapters/02/modules/02/data/21'
B=ROOT/'.build';O=ROOT/'output';F=ROOT/'figures'
for p in [B/'assets',B/'fonts',O,F,ROOT/'review',ROOT/'data']:p.mkdir(parents=True,exist_ok=True)
C={'ink':'#13253D','muted':'#5C6B7A','line':'#D9E3E9','pale':'#F4F7F9','blue':'#155FA8','teal':'#007D78','china':'#AD4E22','india':'#8E6500','south':'#943B9A','white':'#FFFFFF'}
GROUPS=[('欧洲','teal'),('美国','blue'),('中国','china'),('印度','india'),('全球南方代表国家','south')]
NAMES={'全球南方代表国家':'南方六国代表组'}
PF=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',100,index=2)
BF=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',100,index=2)
QA=[]
def tw(t,fs,bold=False):return (BF if bold else PF).getlength(str(t))/100*fs
def col(c):return C.get(c,c)

class Board:
    def __init__(self,title,subtitle,description,number):
        self.items=[];self.labels=[];self.rect(0,0,1600,900,'white')
        logo=ET.parse(REPO/'brand/osdgs/v2.0/assets/master/osdgs-symbol-compact.svg').getroot()
        logo.set('x','40');logo.set('y','20');logo.set('width','38');logo.set('height','38')
        self.items.append(ET.tostring(logo,encoding='unicode'))
        self.text(91,46,'GOSD 2026  /  全球开源发展报告 · 精要版',18,'muted',True)
        self.text(1560,46,'第二章 · 全球开源生态地图',18,'muted',False,'end')
        self.line(40,65,1560,65)
        for i,c in enumerate(['#155FA8','#087C99','#007D78','#267D4E','#537D25','#8E6500','#AD4E22','#B53863','#943B9A','#6146A5']):self.rect(1192+i*37,63,29,3,c)
        self.text(40,110,title,35,'ink',True)
        self.text(40,146,subtitle,23,'teal',True)
        self.text(1560,110,number,20,'muted',False,'end')
        self.wrap(40,178,description,1520,18,'muted',leading=26)
    def rect(self,x,y,w,h,c,opacity=1):self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col(c)}" opacity="{opacity}"/>')
    def line(self,x,y,xx,yy,c='line',sw=1,dash=None):self.path([(x,y),(xx,yy)],c,sw,dash=dash)
    def path(self,pts,c='blue',sw=2,fill='none',dash=None,opacity=1):
        d=' '.join(('M' if i==0 else 'L')+f'{x:.3f},{y:.3f}' for i,(x,y) in enumerate(pts))
        if fill!='none':d+='Z'
        self.items.append(f'<path d="{d}" fill="{col(fill)}" stroke="{col(c)}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" opacity="{opacity}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def circle(self,x,y,r,c='teal',filled=True):self.items.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col(c) if filled else "white"}" stroke="{col(c)}" stroke-width="1.5"/>')
    def text(self,x,y,t,fs=18,c='ink',bold=False,anchor='start',audit=True):
        t=str(t);w=tw(t,fs,bold);left=x if anchor=='start' else x-w if anchor=='end' else x-w/2
        if audit:self.labels.append(dict(text=t,x=left,y=y-fs*.85,w=w,h=fs*1.06))
        self.items.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK SC" font-size="{fs}" font-weight="{700 if bold else 400}" fill="{col(c)}" text-anchor="{anchor}">{html.escape(t)}</text>')
    def wrap(self,x,y,t,w,fs=18,c='ink',bold=False,leading=27):
        lines=[];line=''
        for ch in t:
            if ch=='\n':lines.append(line);line='';continue
            if tw(line+ch,fs,bold)>w and line:lines.append(line);line=ch
            else:line+=ch
        if line:lines.append(line)
        for i,l in enumerate(lines):self.text(x,y+i*leading,l,fs,c,bold)
        return len(lines)*leading
    def footer(self,t):
        self.line(40,850,1560,850)
        self.wrap(40,873,t,1520,16,'muted',leading=20)
    def save(self,name):
        p=F/f'{name}.svg';p.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">'+''.join(self.items)+'</svg>')
        overflow=[a for a in self.labels if a['x']<0 or a['x']+a['w']>1600 or a['y']<0 or a['y']+a['h']>900]
        overlaps=[]
        for i,a in enumerate(self.labels):
            for b in self.labels[i+1:]:
                dx=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x']);dy=min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])
                if dx>2 and dy>3:overlaps.append([a['text'],b['text'],round(dx,1),round(dy,1)])
        QA.append({'figure':name,'out_of_bounds':overflow,'overlap_candidates':overlaps})
        export(p,B/'assets'/f'{name}.pdf')
        subprocess.run(['inkscape',str(p),'--export-type=png','--export-width=3840',f'--export-filename={O/(name+"-4K.png")}'],check=True,capture_output=True)

def export(src,dest):subprocess.run(['inkscape',str(src),'--export-type=pdf',f'--export-filename={dest}'],check=True,capture_output=True)
def data(name):
    p=DATA/name;(ROOT/'data'/name).write_bytes(p.read_bytes());return list(csv.DictReader(p.open()))
def xyseries(x,y,w,h,years,vals,ymax):return [(x+(yr-2022)/8*w,y+h-v/ymax*h) for yr,v in zip(years,vals)]
def scenario(vals):
    g=(vals[-1]/vals[0])**.25-1
    ongoing=[vals[-1]*(1+g)**h for h in range(1,5)]
    slowing=[];v=vals[-1]
    for h in range(1,5):v*=1+g*.8**h;slowing.append(v)
    return {'annual_growth':g,'history':vals,'continued':ongoing,'slowing':slowing}

def first(top,totals):
    b=Board('2.1  全球开源活跃地图','当下｜全球参与基础广泛，跨平台观察补充中国图景',
        '活跃开发者：报告期内有公开活动的账号，包括收藏项目、复制仓库继续开发、提交修改等。累计规模还包含当期未活跃的用户。','图 2-1')
    b.text(40,222,'全球累计规模',18,'muted');b.text(181,224,'1.94 亿',30,'ink',True)
    b.text(420,222,'当期活跃规模',18,'muted');b.text(561,224,'2,890.4 万',30,'teal',True)
    b.text(1045,220,'2025.07—2026.06',18,'muted',False,'end')
    src=ET.parse(REPO/'reports/round2-v2.0/source/chapters/02/modules/02/figures/21/world_map.svg').getroot()
    b.items.append('<g transform="translate(15,130) scale(6.12)">')
    count=0
    for v in list(src):
        tag=v.tag.rsplit('}',1)[-1]
        if (tag=='path' and v.get('fill')=='#E8F0F1') or (tag=='circle' and float(v.get('cy'))<85):
            vv=copy.deepcopy(v)
            if tag=='path':vv.set('fill','#E7EEF2')
            else:count+=1
            b.items.append(ET.tostring(vv,encoding='unicode'))
    b.items.append('</g>');assert count==171
    for cx,cy,lx,ly,t in [(45.703,33.978,80,307,'美国 494.1 万'),(124.179,34.207,853,292,'中国 250.5 万'),(118.55,42.376,839,540,'印度 285.1 万'),(63.499,63.329,165,604,'巴西 193.5 万')]:
        b.line(15+cx*6.12,130+cy*6.12,lx+55,ly+4,'#A4B6C2',1.2)
        b.rect(lx-5,ly-23,tw(t,22,True)+10,31,'white');b.text(lx,ly,t,22,'ink',True)
    for x,n in [(60,10),(310,100),(565,400)]:
        b.circle(x+22,666,math.sqrt(n/400)*4.74*6.12);b.text(x+68,674,f'{n} 万人',18,'muted')
    b.text(1045,674,'圆面积表示规模',17,'muted',False,'end')
    # All twenty entries share one baseline and one linear scale.
    b.line(1080,212,1080,826)
    b.text(1110,221,'主要国家活跃规模｜前 20',21,'ink',True);b.text(1560,247,'万人',17,'muted',False,'end')
    for i,r in enumerate(top):
        y=273+i*25.4;v=float(r['active'])/1e4
        b.text(1110,y,f'{i+1:02}',16.5,'muted');b.text(1152,y,r['name'],19,'ink',i<4)
        b.rect(1306,y-14,168,17,'pale');b.rect(1306,y-14,168*v/500,17,'teal')
        b.text(1560,y,f'{v:.2f}',18,'ink',i<4,'end')
    b.line(1306,773,1474,773)
    for v in [0,250,500]:b.text(1306+168*v/500,796,str(v),16.5,'muted',False,'middle')
    b.text(1110,826,'统一为 GitHub 口径；不混入本土补充量。',16.5,'muted')
    # Coverage is a separate observation, never an artificial combined ranking.
    b.rect(40,705,1005,122,'pale');b.rect(40,705,4,122,'teal')
    b.text(58,734,'中国的平台视野',21,'teal',True)
    b.text(58,769,'GitHub',18);b.rect(230,754,250.48,17,'blue');b.text(505,769,'250.48 万',19,'blue',True)
    b.text(58,805,'本土平台补充',18)
    b.items.append('<defs><pattern id="local-hatch" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="white"/><path d="M-2,2 L2,-2 M0,8 L8,0 M6,10 L10,6" stroke="#007D78" stroke-width="1.5"/></pattern></defs>')
    b.rect(230,790,120,17,'url(#local-hatch)');b.text(374,805,'约 120 万',19,'teal',True)
    b.wrap(654,750,'补充来自 Gitee、AtomGit 等平台统计与问卷。两组覆盖尚未统一，分别展示，不直接相加；五域趋势另用中国约 350 万的修订序列。',365,17,'muted',leading=25)
    b.footer('数据：OpenDigger / OpenShare 的 GitHub 活动与地理统计；本土平台为编制组补充观察。统计期为 2025 年 7 月至 2026 年 6 月。地区未识别或未绘制，不等于零；定义与估算说明见附录 1。')
    b.save('01-global-current')

def second(sc,global_sc):
    b=Board('2.1  参与规模的演进','趋势｜印度与南方六国增长较快，2030 格局取决于增长能否持续',
        '实线为 2022—2026 报告年度；虚线为 2027—2030 条件情景。阴影是两种假设之间的范围，不是置信区间。年均增速按各组历史起点与终点计算。','图 2-2')
    b.text(40,226,'A  五域活跃规模｜万人',22,'ink',True)
    x,y,w,h=95,290,825,365;ymax=1400
    for i,(key,c) in enumerate(GROUPS):
        xx=40+i*203;b.line(xx,255,xx+30,255,c,4);b.text(xx+40,262,NAMES.get(key,key),18,c,True)
    b.rect(x+w*.5,y,w*.5,h,'pale')
    for n in [0,350,700,1050,1400]:
        yy=y+h-n/ymax*h;b.line(x,yy,x+w,yy);b.text(x-15,yy+6,f'{n:,}',17,'muted',False,'end')
    for yr in range(2022,2031):
        xx=x+(yr-2022)/8*w;b.text(xx,y+h+29,str(yr),17,'muted',False,'middle')
    b.line(x+w*.5,y,x+w*.5,y+h,'#899AA6',1.3,'5 5')
    b.text(x+w*.75,y-12,'条件情景',17,'muted',False,'middle')
    for key,c in GROUPS:
        s=sc[key]
        a=xyseries(x,y,w,h,range(2022,2027),s['history'],ymax)
        up=xyseries(x,y,w,h,range(2026,2031),[s['history'][-1]]+s['continued'],ymax)
        low=xyseries(x,y,w,h,range(2026,2031),[s['history'][-1]]+s['slowing'],ymax)
        b.path(up+list(reversed(low)),c,0,fill=c,opacity=.09)
        b.path(a,c,3.4)
        for xx,yy in a:b.circle(xx,yy,4,c)
        b.path(up,c,3,dash='8 5');b.path(low,c,1.3,dash='2 5',opacity=.7)
        b.circle(*up[-1],4.5,c,False)
        label=NAMES.get(key,key).replace('南方六国代表组','南方六国')
        b.text(949,up[-1][1]+6,f'{label} {s["continued"][-1]:,.0f}',17.4,c,True)
    cp=xyseries(x,y,w,h,[2026],[350],ymax)[0]
    b.text(cp[0]-8,cp[1]-16,'中国约 350 万',17,'china',True,'end')
    for xx,txt,dash,sw in [(40,'历史观测',None,3.4),(335,'历史延续','8 5',3),(630,'逐步放缓','2 5',1.3)]:
        b.line(xx,721,xx+58,721,'muted',sw,dash);b.text(xx+72,728,txt,19,'ink',True)
    b.wrap(40,761,'历史延续：未来每年保持 2022—2026 的年均增速。逐步放缓：未来年增速每年按上一年的 80% 递减。两者均未加入 AI 的额外因果效应。',1005,18,'muted',leading=28)
    b.wrap(40,821,'五域为固定比较组：欧洲、美国、中国、印度及巴西／印尼／越南／菲律宾／埃及／南非。它们不是全球完整分区，也不同于图 2-1 的地理汇总。',1005,16.5,'muted',leading=22)
    b.line(1080,215,1080,830)
    b.text(1110,226,'B  累计基础与当期活跃',22,'ink',True)
    b.text(1110,253,'2022 = 100；同样延伸至 2030',17,'muted')
    xx,yy,ww,hh=1150,292,378,203
    b.rect(xx+ww*.5,yy,ww*.5,hh,'pale')
    for v in [0,200,400,600]:
        py=yy+hh-v/600*hh;b.line(xx,py,xx+ww,py);b.text(xx-13,py+5,str(v),15.5,'muted',False,'end')
    for k,c,name in [('total','blue','累计规模'),('active','teal','当期活跃')]:
        ss=global_sc[k];base=ss['history'][0]
        hist=[v/base*100 for v in ss['history']];continued=[v/base*100 for v in ss['continued']];slow=[v/base*100 for v in ss['slowing']]
        a=xyseries(xx,yy,ww,hh,range(2022,2027),hist,600)
        u=xyseries(xx,yy,ww,hh,range(2026,2031),[hist[-1]]+continued,600)
        lo=xyseries(xx,yy,ww,hh,range(2026,2031),[hist[-1]]+slow,600)
        b.path(u+list(reversed(lo)),c,0,fill=c,opacity=.1);b.path(a,c,3);b.path(u,c,2.5,dash='7 4');b.path(lo,c,1,dash='2 4')
        b.text(1537,u[-1][1]+5,f'{continued[-1]:.0f}',16,c,True)
    for yr in [2022,2026,2030]:b.text(xx+(yr-2022)/8*ww,yy+hh+25,str(yr),16,'muted',False,'middle')
    b.line(1120,542,1150,542,'blue',3);b.text(1160,548,'累计规模',17,'blue')
    b.line(1330,542,1360,542,'teal',3);b.text(1370,548,'当期活跃',17,'teal')
    b.text(1110,588,'C  2030 活跃规模的情景区间',21,'ink',True)
    b.text(1300,618,'2026',16.5,'muted',False,'end');b.text(1560,618,'2030 放缓—延续／万人',16.5,'muted',False,'end')
    for i,(k,c) in enumerate(GROUPS):
        sy=650+i*34;s=sc[k];name=NAMES.get(k,k).replace('南方六国代表组','南方六国')
        b.text(1110,sy,name,18,c,True);b.text(1300,sy,f'{s["history"][-1]:,.0f}',18,'ink',False,'end');b.text(1560,sy,f'{s["slowing"][-1]:,.0f}—{s["continued"][-1]:,.0f}',18,c,True,'end')
    b.text(1110,823,'这是条件范围，不给出发生概率。',17,'muted')
    b.footer('数据：编制组五域年度序列；全球累计与活跃来自 OpenDigger / OpenShare。中国 2026 年按约 350 万修订，历史值保留。2030 为编制组情景测算，非确定结果；公式、参数和年度数值见附录 1。')
    b.save('02-trends-2030')

def third(provinces,totals):
    b=Board('2.1  中国区域参与结构','中国｜头部集聚与多地增长并存，积累与增量需要联合观察',
        '本图统一采用 GitHub 地理口径。累计规模是已有账号基础；当期活跃是在报告期内有公开活动的账号；净增是两期规模之差，不是首次参与或人才迁入。','图 2-3')
    pmap={r['province']:r for r in provinces}
    b.text(40,225,'A  34 个省级地区的活跃分布',22,'ink',True)
    b.text(745,225,'2025.07—2026.06',17,'muted',False,'end')
    geom=json.loads((ROOT/'data/china-drawing-geometry.json').read_text())
    palette=['#E5EFF4','#BDDAE5','#88B7CE','#4F91B5','#155F8B'];bounds=[1,5,15,30]
    # Preserve all 36 geographic features including maritime lines and inset.
    for f in geom['features']:
        name=f['name'];fill='none' if name=='十段线' else '#FFFFFF' if name=='南海诸岛' else palette[sum(float(pmap[name]['active_10k'])>=q for q in bounds)]
        b.items.append(f'<path d="{f["path"]}" transform="translate(-138,205) scale(1.03)" fill="{fill}" fill-rule="evenodd" stroke="#8DA7B4" stroke-width="0.8"/>')
    # Convert the inherited geographic centres through the original projection;
    # leader lines explicitly connect offset labels to their geographic feature.
    centres={f['name']:f['center'] for f in geom['features']}
    for name,lx,ly in [('北京',610,380),('上海',640,457),('浙江',640,501),('台湾',640,551),('广东',600,601),('四川',287,489)]:
        lon,lat=centres[name]
        px=-138+1.03*(185.5365860534777+(lon-73.502355)*.75*11.018439414576823)
        py=205+1.03*(18+(53.563624-lat)*11.018439414576823)
        if name!='四川':
            b.path([(px,py),(lx-20,ly-7),(lx-6,ly-7)],'#7F9AA9',1.2)
            b.circle(px,py,2.6,'blue')
        b.rect(lx-3,ly-20,tw(name,20,True)+6,26,'white');b.text(lx,ly,name,20,'ink',True)
    b.text(40,660,'活跃规模／万人',17,'muted')
    for i,(c,t) in enumerate(zip(palette,['<1','1—<5','5—<15','15—<30','≥30'])):
        xx=225+i*99;b.rect(xx,644,25,16,c);b.text(xx+33,659,t,16,'muted')
    # National series: exact historical GitHub values, separate from five-group data.
    b.text(40,707,'B  全国活跃规模｜万人',20,'ink',True)
    x,y,w,h=84,732,280,83
    for v in [0,150,300]:
        sy=y+h-v/300*h;b.line(x,sy,x+w,sy);b.text(x-10,sy+5,str(v),15.5,'muted',False,'end')
    vals=[float(r['china_active_github'])/1e4 for r in totals]
    pts=[(x+i/4*w,y+h-v/300*h) for i,v in enumerate(vals)]
    b.path(pts,'blue',3)
    for i,(xx,yy) in enumerate(pts):b.circle(xx,yy,3.5,'blue');b.text(xx,837,str(2022+i),15,'muted',False,'middle')
    b.text(pts[0][0],pts[0][1]-12,f'{vals[0]:.2f}',16,'blue',True)
    b.text(pts[-1][0],pts[-1][1]-12,f'{vals[-1]:.2f}',16,'blue',True,'end')
    total=sum(float(r['active_10k']) for r in provinces)
    ordered=sorted(provinces,key=lambda r:float(r['active_10k']),reverse=True)
    shares=[sum(float(r['active_10k']) for r in ordered[:3])/total,sum(float(r['active_10k']) for r in ordered[3:10])/total,sum(float(r['active_10k']) for r in ordered[10:])/total]
    b.text(420,707,'C  活跃规模的区域构成',20,'ink',True)
    xx=420
    for share,c in zip(shares,['blue','teal','south']):b.rect(xx,728,330*share,22,c);xx+=330*share
    for i,(name,v,c) in enumerate(zip(['京沪粤','第 4—10 位','其余 24 地'],shares,['blue','teal','south'])):
        sy=778+i*27;b.rect(420,sy-13,13,13,c);b.text(445,sy,name,17,'ink');b.text(750,sy,f'{v*100:.1f}%',18,c,True,'end')
    b.line(785,212,785,837)
    b.text(815,225,'D  省级地区前 20｜按当期活跃排序',22,'ink',True)
    for xx,t in [(1195,'累计规模'),(1400,'当期活跃'),(1560,'净增量')]:b.text(xx,259,t,17,'muted',False,'end')
    b.text(815,259,'单位：万人',16.5,'muted')
    for i,r in enumerate(ordered[:20]):
        sy=291+i*25.4;b.text(815,sy,f'{i+1:02}',16,'muted');b.text(854,sy,r['province'],19,'ink',i<3)
        for bx,bw,val,maxv,cl,tx in [(973,140,float(r['total_10k']),420,'#92B4C9',1195),(1216,108,float(r['active_10k']),56,'blue',1400),(1420,61,float(r['increase_10k']),7,'teal',1560)]:
            b.rect(bx,sy-14,bw,17,'pale');b.rect(bx,sy-14,bw*val/maxv,17,cl);b.text(tx,sy,f'{val:.2f}',18,'ink',False,'end')
    b.text(815,822,'净增窗口：2026 报告年度较 2025 报告年度。',17,'muted')
    b.footer('数据：OpenDigger / OpenShare，2025.07—2026.06；省级累计与活跃按平台估计阅读，本土平台补充未分摊。底图沿用 OpenShare / GeoJSON.CN；台湾、香港、澳门纳入中国。各份额独立取整。')
    b.save('03-china-regions')

def esc(s):return s.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
def box(x,y,w,t,fs=10.8,lead=17,color='ink',bold=False):
    return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{\fontsize{{{fs}}}{{{lead}}}\selectfont\color{{{color}}}'+(r'\sffamily\bfseries ' if bold else '')+esc(t)+'}\n'
def pdf_sources(d,sc,gs,totals):
    style=(REPO/'editions/insights/chapters/02/v0.1/layout.sty').read_text().replace('v0.1','v0.2')
    (ROOT/'layout.sty').write_text(style)
    # A3 graphic pages retain ordinary text analysis beneath the integrated board.
    tex=r'\documentclass[11pt]{article}\usepackage{layout}\geometry{paperwidth=420mm,paperheight=297mm,margin=0mm}\begin{document}'+'\n'
    for i,name in enumerate(['01-global-current','02-trends-2030','03-china-regions']):
        tex+=r'\begin{canvas}'+'\n'+rf'\pdfbookmark[1]{{图 2-{i+1}}}{{fig{i+1}}}\Box{{17}}{{10}}{{386}}{{\includegraphics[width=386mm]{{.build/assets/{name}.pdf}}}}'+'\n'
        for j,(title,body) in enumerate(d[f'figure{i+1}_analysis']):
            xx=17+j*201
            tex+=box(xx,237,185,title,12.5,18,'teal',True)+box(xx,248,185,body,11.1,18.5)
        tex+=rf'\Rule{{17}}{{285}}{{403}}{{line}}\Small{{17}}{{289}}{{350}}{{GOSD 2026 / 全球开源发展报告 · 精要版}}\Box{{385}}{{288}}{{18}}{{\raggedleft\digits\fontsize{{11}}{{13}}\selectfont {i+1:02}}}'+'\n'+r'\end{canvas}'+'\n'
    tex+=r'\end{document}';(ROOT/'boards.tex').write_text(tex)
    t=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
    t+=r'\begin{canvas}\Header{附录 1 · 指标与数据}{teal}\Footer{A1}\Kicker{teal}{附录 1}\Title{怎样读懂这些人数与变化}'+'\n'
    rows=[('累计规模','截至统计期末的用户基础，包含当期未活跃账号；地区值含平台估计，不等同于职业人口。'),('活跃开发者','报告期内在公开事件记录中出现过的账号；包括收藏项目、复制仓库继续开发、提交修改、讨论等公开活动。不是代码贡献者人数。'),('参与者与贡献者','参与者统计问题讨论（Issue）及代码修改请求（PR）中的互动账号；贡献者统计修改请求被项目采纳的作者。二者都不同于活跃人数。'),('地区与净增','按公开所在地归属，不表示国籍或雇主所在地。净增 = 本期活跃 − 上期活跃，不能推断首次参与、迁入或留存。')]
    for y,(name,desc) in zip([65,95,125,155],rows):t+=box(22,y,35,name,10.4,16,'teal',True)+box(61,y,127,desc,10.1,16)
    t+=box(22,189,166,'2022—2026 报告年度的规模序列／万人',11.5,16,'blue',True)
    tab=r'\sffamily\fontsize{9.5}{16}\selectfont\begin{tabular}{lrrrrr}\textbf{比较组}&\textbf{2022}&\textbf{2023}&\textbf{2024}&\textbf{2025}&\textbf{2026}\\\hline'+'\n'
    for key,c in GROUPS:tab+=esc(NAMES.get(key,key))+'&'+'&'.join(f'{v:.2f}' for v in sc[key]['history'])+r'\\'+'\n'
    for key,name in [('total','全球累计规模'),('active','全球当期活跃')]:tab+=name+'&'+'&'.join(f'{v:.2f}' for v in gs[key]['history'])+r'\\'+'\n'
    tab+=r'\end{tabular}';t+=rf'\Box{{22}}{{200}}{{166}}{{{tab}}}'+'\n'
    t+=box(22,249,166,'报告年度统一指上年 7 月 1 日至当年 6 月 30 日。五域是编制组独立比较序列，欧洲成员与平台覆盖的详细执行记录仍待补齐；不作为全球完整分区。南方六国指巴西、印尼、越南、菲律宾、埃及、南非。',9.4,14.5)
    t+=r'\end{canvas}'+'\n'
    t+=r'\begin{canvas}\Header{附录 1 · 情景方法}{teal}\Footer{A2}\Kicker{teal}{附录 1 · 续}\Title{2030 情景如何形成，如何更新}'+'\n'
    t+=box(22,65,166,'以 2026 报告年度末为算术起点。历史年均增速 g =（2026 人数 ÷ 2022 人数）的四次方根 − 1。历史延续情景每年按 g 增长；逐步放缓情景第 h 年增速为 g × 0.8 的 h 次方。每年逐次相乘，得到 2027—2030 年人数。',10.5,17)
    t+=box(22,100,166,'0.8 是用于检验敏感性的预设参数，不是拟合所得。只有五个年度点，不估计置信区间或情景概率；外推不识别 AI、政策、人口等因素的因果作用。所有情景都可能因结构变化而失效。',10.1,16)
    tab=r'\sffamily\fontsize{9.6}{16}\selectfont\begin{tabular}{lrrr}\textbf{对象}&\textbf{历史年均增速}&\textbf{2030 放缓}&\textbf{2030 延续}\\\hline'+'\n'
    for key,c in GROUPS:
        z=sc[key];tab+=esc(NAMES.get(key,key))+f'&{z["annual_growth"]*100:.1f}\\%&{z["slowing"][-1]:,.0f}万&{z["continued"][-1]:,.0f}万'+r'\\'+'\n'
    for key,name in [('total','全球累计规模'),('active','全球当期活跃')]:
        z=gs[key];tab+=name+f'&{z["annual_growth"]*100:.1f}\\%&{z["slowing"][-1]:,.0f}万&{z["continued"][-1]:,.0f}万'+r'\\'+'\n'
    tab+=r'\end{tabular}';t+=rf'\Box{{22}}{{134}}{{166}}{{{tab}}}'+'\n'
    t+=box(22,184,166,'修订与口径：五域中国 2026 年按编制组本轮更正取约 350 万，2022—2025 年保持原序列；旧值 454.53 万不再用于本版。GitHub 地图的中国约 250.48 万与旧本土补充约 120 万各自保留，不能由二者推出五域数值或另行混排。',9.7,15)
    t+=box(22,220,166,'数据与复核：图 2-1、2-3 使用 OpenDigger／OpenShare 报告年度归档；累计规模及地区活跃含估计。图 2-2 使用编制组五域序列。定义已核对 OpenDigger 公开指标文档；上游去重、历史地理执行与本土补充覆盖仍待逐项核定。',9.4,14.5)
    t+=box(22,252,166,'复核频率：每年补入同口径观测，重算情景；发布后 6—12 个月先监测持续贡献和维护条件。方法参照：Hyndman 与 Athanasopoulos，Forecasting: Principles and Practice，第 3 版，第 6.5 节“情景预测”。',8.8,13.4)
    t+=r'\end{canvas}\end{document}';(ROOT/'text.tex').write_text(t)

def fonts():
    for family in ['Sans','Serif']:
        for weight in ['Regular','Bold']:
            out=B/'fonts'/f'Noto{family}CJKsc-{weight}.otf'
            if not out.exists():
                coll=TTCollection(f'/usr/share/fonts/opentype/noto/Noto{family}CJK-{weight}.ttc');coll.fonts[2].save(out);coll.close()
    export(REPO/'brand/osdgs/v2.0/assets/master/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')

def compile_tex(name):
    env=os.environ.copy()
    if subprocess.run(['kpsewhich','article.cls'],stdout=subprocess.DEVNULL).returncode:env['TEXMF']='{/usr/share/texmf,/usr/share/texlive/texmf-dist}'
    if subprocess.run(['kpsewhich','xelatex.fmt'],env=env,stdout=subprocess.DEVNULL).returncode:
        var=B/'texmf-var';var.mkdir(exist_ok=True)
        env['TEXMFVAR']=str(var);env['TEXFORMATS']=str(var)
        if not (var/'xelatex.fmt').exists():
            with (O/'format-build.txt').open('w') as f:
                subprocess.run(['xelatex','-ini','-etex','-interaction=nonstopmode','-jobname=xelatex',f'-output-directory={var}',r'\input xelatex.ini'],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    for n in [1,2]:
        with (O/f'{name}-build-{n}.txt').open('w') as f:subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory=output',name+'.tex'],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)

def main():
    fonts();top20=data('top20_display.csv');top10=data('global_2026_top10.csv');full={r['code']:float(r['active_developers']) for r in top10}
    top=[{'code':r['code'],'name':r['name_zh'],'active':full.get(r['code'],float(r['active_rounded']))} for r in top20]
    totals=data('global_report_year_trend.csv');trend=data('five_groups_active_trend.csv');provinces=data('china_provinces_with_change.csv')
    sc={}
    for k,c in GROUPS:
        vals=[float(r[k])/1e4 for r in trend]
        if k=='中国':vals[-1]=350.0
        sc[k]=scenario(vals)
    gs={k:scenario([float(r[field])/1e4 for r in totals]) for k,field in [('total','developers_total'),('active','active_developers')]}
    (ROOT/'data/scenarios.json').write_text(json.dumps({'units':'万人','anchor':'2026 report year','forecast_years':[2027,2028,2029,2030],'damping':.8,'china_correction':{'old':454.534,'new':350,'source':'作者2026-11-09更正','approximate':True,'history_unchanged':True},'groups':sc,'global':gs,'not_probability_or_confidence_interval':True},ensure_ascii=False,indent=2)+'\n')
    first(top,totals);second(sc,gs);third(provinces,totals)
    (ROOT/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2)+'\n')
    d=json.loads((ROOT/'content.json').read_text());pdf_sources(d,sc,gs,totals)
    compile_tex('boards');compile_tex('text')
    final=fitz.open()
    for src in [O/'boards.pdf',O/'text.pdf']:
        with fitz.open(src) as doc:final.insert_pdf(doc)
    final.set_toc([[1,'2.1 全球开源活跃地图',1],[2,'趋势与2030情景',2],[2,'中国区域参与结构',3],[1,'附录1 指标与数据',4],[2,'情景方法与复核',5]])
    final.set_metadata({'title':'GOSD 2026 精要版｜第二章2.1三幅组合主图与2030情景 v0.2','author':'全球开源发展报告编制组','subject':'待作者评审；3页A3横向图文＋附录1两页；2030为条件情景'})
    final.save(O/'GOSD_2026_Chapter2_Integrated_v0.2.pdf',garbage=4,deflate=True)
    with zipfile.ZipFile(O/'GOSD_2026_Chapter2_Figures_v0.2.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path in sorted(F.glob('*.svg')):z.write(path,'SVG/'+path.name)
        for path in sorted(O.glob('*-4K.png')):z.write(path,'PNG-4K/'+path.name)
        for path in sorted((ROOT/'data').glob('*.csv')):z.write(path,'data/'+path.name)
        z.write(ROOT/'data/scenarios.json','data/scenarios.json')
        z.writestr('README.txt','GOSD 2026 精要版 · 第二章2.1 v0.2，待评审。\n三幅16:9组合图，SVG可编辑，PNG为3840×2160。\n2027—2030为条件情景，不是确定预测或置信区间。五域中国2026年按作者更正取约350万；原始CSV保留旧值，修订值见scenarios.json。\n中国地图沿用 OpenShare / GeoJSON.CN 底图，几何不变；正式出版需完成边界与许可复核。\n正文分析、定义及完整方法见配套PDF。\n')
    print('Built',len(final),'pages; 3 vector boards and 4K exports.')
    print(json.dumps([{'figure':q['figure'],'overflow':len(q['out_of_bounds']),'overlaps':len(q['overlap_candidates'])} for q in QA],ensure_ascii=False))

if __name__=='__main__':main()
