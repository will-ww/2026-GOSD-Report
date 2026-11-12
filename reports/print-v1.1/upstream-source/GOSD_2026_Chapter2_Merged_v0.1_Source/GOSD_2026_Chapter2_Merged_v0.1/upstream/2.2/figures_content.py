from build import *

WORLD=json.loads((D/'contribution.json').read_text())
CN=json.loads((D/'CN-contribution.json').read_text())
ACTIVE=json.loads((D/'public-developers.json').read_text())
CN_ACTIVE=json.loads((D/'public-CN-developers.json').read_text())
ROWS=WORLD['leaderboards'][0]['data']; PROV=CN['leaderboards'][0]['data']
AR={r['code']:r for r in ACTIVE['leaderboards'][1]['data']}
PR={r['code']:r for r in CN_ACTIVE['leaderboards'][1]['data']}
CR={r['code']:r for r in ROWS}
GT=readcsv('five_groups_contribution.csv')
GR=[('Europe','欧洲','teal'),('China','中国','china'),('United States','美国','blue'),('Global South representatives','南方六国','south'),('India','印度','india')]
SOUTH=[CR[k] for k in ['BR','ID','VN','ZA','PH','EG']]

def short(n):
    for t in ['壮族自治区','维吾尔自治区','回族自治区','特别行政区','自治区','省','市']:n=n.replace(t,'')
    return n

def first():
    b=Figure();b.title(0,22,1,'主要贡献节点 · 前 20');b.title(622,22,2,'国家贡献读数 · 前 20')
    b.text(0,50,'2026 报告年度；公开估计口径',16,'muted');b.text(1000,50,'万 OpenRank',16,'muted',anchor='end')
    src=ET.parse(R/'assets/world-base.svg').getroot();tx=-53;ty=30;scale=4.08
    b.items.append(f'<g transform="translate({tx},{ty}) scale({scale})">')
    for e in src:
        if e.tag.endswith('path') and e.get('fill')=='#E8F0F1':
            e=copy.deepcopy(e);e.set('fill','#E7EEF2');b.items.append(ET.tostring(e,encoding='unicode'))
    anchors=json.loads((D/'map-anchors.json').read_text())
    for r in ROWS[:20]:
        a=anchors[r['code']];rad=math.sqrt(r['value']/4e6)*5.28
        b.items.append(f'<circle cx="{a["cx"]}" cy="{a["cy"]}" r="{rad}" fill="{C["china"] if r["code"]=="CN" else C["teal"]}" fill-opacity=".85" stroke="white" stroke-width=".12"/>')
    b.items.append('</g>')
    for code,x,y in [('US',3,129),('CN',420,125),('IN',410,268),('BR',50,319)]:
        a=anchors[code];r=CR[code];t=f'{r["name_zh"]} {r["value"]/1e4:.1f} 万'
        b.line(tx+scale*a['cx'],ty+scale*a['cy'],x+50,y+3,'#94AAB9',1.1);b.rect(x-3,y-19,tw(t,18,True)+6,24,'white');b.text(x,y,t,18,'ink',True)
    for x,v in [(0,10),(171,100),(354,300)]:
        b.circle(x+22,382,math.sqrt(v/400)*5.28*scale);b.text(x+49,388,f'{v} 万',17,'muted')
    b.text(0,425,'圆面积表示贡献度；未画出不表示没有贡献。',16,'muted');b.line(602,0,602,442)
    for i,r in enumerate(ROWS[:20]):
        yy=74+i*18.5;v=r['value']/1e4;c='china' if r['code']=='CN' else 'teal'
        b.text(622,yy,f'{i+1:02}',15.8,'muted');b.text(652,yy,r['name_zh'],16.4,'ink',i<4)
        b.rect(754,yy-11,163,11,'pale');b.rect(754,yy-11,163*v/340,11,c);b.text(1000,yy,f'{v:.2f}',16.5,c,r['code']=='CN','end')
    from panels_v02 import first_lower
    first_lower(b)
    b.save('01-contribution-map')

def third():
    b=Figure();b.title(0,22,1,'中国贡献结构 · 34 个省级地区');b.title(612,22,2,'省级贡献读数 · 前 20')
    b.text(0,55,'全国 93.68 万 OpenRank',21,'china',True);b.text(1000,52,'万 OpenRank',16,'muted',anchor='end')
    pmap={short(r['name_zh']):r for r in PROV};geom=json.loads((D/'china-drawing-geometry.json').read_text());pal=['#E5EFF4','#BDDAE5','#88B7CE','#4F91B5','#155F8B'];bounds=[.5,2,10,15]
    scale=.91;tx=-166;ty=47
    for f in geom['features']:
        n=f['name'];fill='none' if n=='十段线' else 'white' if n=='南海诸岛' else pal[sum(pmap[n]['value']/1e4>=q for q in bounds)]
        b.items.append(f'<path d="{f["path"]}" transform="translate({tx},{ty}) scale({scale})" fill="{fill}" fill-rule="evenodd" stroke="#8DA7B4" stroke-width="0.8"/>')
    centers={f['name']:f['center'] for f in geom['features']}
    for n,lx,ly in [('北京',476,178),('上海',500,235),('浙江',502,274),('台湾',502,322),('广东',433,390),('四川',168,304)]:
        lon,lat=centers[n];px=tx+scale*(185.5365860534777+(lon-73.502355)*.75*11.018439414576823);py=ty+scale*(18+(53.563624-lat)*11.018439414576823)
        if n!='四川':b.path([(px,py),(lx-12,ly-6),(lx-4,ly-6)],'#7F9AA9',1.2);b.circle(px,py,2.1,'blue')
        b.rect(lx-3,ly-17,tw(n,17.5,True)+6,23,'white');b.text(lx,ly,n,17.5,'ink',True)
    b.text(0,441,'万',15.8,'muted')
    for i,(c,t) in enumerate(zip(pal,['<0.5','0.5—<2','2—<10','10—<15','≥15'])):
        xx=37+i*108;b.rect(xx,428,20,13,c);b.text(xx+26,441,t,15,'muted')
    b.line(591,0,591,447)
    for i,r in enumerate(PROV[:20]):
        yy=76+i*18.6;v=r['value']/1e4
        b.text(612,yy,f'{i+1:02}',15.8,'muted');b.text(647,yy,short(r['name_zh']),16.5,'ink',i<5);b.rect(735,yy-11,162,11,'pale');b.rect(735,yy-11,162*v/20,11,'blue');b.text(1000,yy,f'{v:.2f}',17,'ink',i<5,'end')
    from panels_v02 import third_lower
    third_lower(b)
    b.save('03-china-collaboration')

def render_all():
    from panels_v02 import second as second_new, fourth, save_derived
    first();second_new();third();fourth();save_derived()
    (R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
    print(json.dumps([{'figure':q['figure'],'outside':len(q['out_of_bounds']),'overlaps':q['overlaps']} for q in QA],ensure_ascii=False))
