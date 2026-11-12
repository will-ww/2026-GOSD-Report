from build import *

WORLD=json.loads((D/'report-influence.json').read_text())
NAT=json.loads((D/'natural-influence.json').read_text())
ROWS=WORLD['leaderboards'][0]['data']; CR={r['code']:r for r in ROWS}
AR={r['code']:r for r in json.loads((D/'report-developers.json').read_text())['leaderboards'][1]['data']}
CON={r['code']:r for r in json.loads((D/'report-contribution.json').read_text())['leaderboards'][0]['data']}
GI=readcsv('five_groups_influence.csv'); GC=readcsv('five_groups_contribution.csv')
PROJECTS=readcsv('china_projects_display.csv')
GR=[('United States','美国','blue'),('China','中国','china'),('Europe','欧洲','teal'),('Global South representatives','南方六国','south'),('India','印度','india')]

def scenario(values,start):
    end=start+len(values)-1; g=(values[-1]/values[0])**(1/(len(values)-1))-1
    slow=[]; v=values[-1]
    for h in range(1,2030-end+1): v*=1+g*.8**h;slow.append(v)
    return dict(start=start,end=end,history=values,growth=g,slowing=slow,continued=[values[-1]*(1+g)**h for h in range(1,2030-end+1)])

GS={k:scenario([float(r[k])/1e4 for r in GI],2022) for k,n,c in GR}
NS={n:scenario([v/1e4 for v in r['values']],2021) for n,r in zip(['全球','美国','中国'],NAT['trends'])}

def shares():
    out={}
    for name,source in [('活跃人数',AR),('开发者贡献',CON),('项目影响',CR)]:
        total=sum(source[k]['value'] for k in CR)
        vals=[source[k]['value']/total*100 for k in ['US','CN']];vals.append(100-sum(vals))
        out[name]={'total':total,'shares':vals}
    return out

def first():
    b=Figure();b.title(0,22,1,'项目影响汇聚在哪里');b.title(622,22,2,'国家项目影响 · 前 20')
    b.text(0,50,'2026 报告年度 · 国家归属标签覆盖 29 国',16,'muted');b.text(1000,50,'万 OpenRank',16,'muted',anchor='end')
    src=ET.parse(R/'assets/world-base.svg').getroot();tx=-53;ty=30;scale=4.08
    anchors=json.loads((D/'map-anchors.json').read_text())
    b.items.append(f'<g transform="translate({tx},{ty}) scale({scale})">')
    for e in src:
        if e.tag.endswith('path') and e.get('fill')=='#E8F0F1':
            e=copy.deepcopy(e);e.set('fill','#E7EEF2');b.items.append(ET.tostring(e,encoding='unicode'))
    for r in reversed(ROWS[:20]):
        a=anchors[r['code']];rad=math.sqrt(r['value']/1.5e6)*6.2
        c='china' if r['code']=='CN' else 'blue' if r['code']=='US' else 'teal'
        b.items.append(f'<circle cx="{a["cx"]}" cy="{a["cy"]}" r="{rad}" fill="{C[c]}" fill-opacity=".85" stroke="white" stroke-width=".14"/>')
    b.items.append('</g>')
    for code,x,y in [('US',0,129),('CN',438,244),('NL',277,77),('ZA',280,318)]:
        a=anchors[code];r=CR[code];t=f'{r["name_zh"]} {r["value"]/1e4:.2f} 万'
        px=tx+scale*a['cx'];py=ty+scale*a['cy']
        if code=='CN':
            radius=math.sqrt(r['value']/1.5e6)*6.2*scale
            b.path([(px+radius*.8,py+radius*.6),(491,194),(491,y-22)],'#94AAB9',1.2)
        else:b.line(px,py,x+42,y+3,'#94AAB9',1.1)
        b.rect(x-1,y-18,tw(t,17.5,True)+3,23,'white');b.text(x,y,t,17.5,'ink',True)
    for x,v in [(0,1),(167,30),(347,150)]:
        b.circle(x+27,382,math.sqrt(v/150)*6.2*scale,'teal');b.text(x+62,388,f'{v} 万',17,'muted')
    b.text(0,425,'圆面积表示影响力；标签未覆盖不等于没有影响。',16,'muted');b.line(602,0,602,442)
    for i,r in enumerate(ROWS[:20]):
        yy=74+i*18.5;v=r['value']/1e4;c='china' if r['code']=='CN' else 'blue' if r['code']=='US' else 'teal'
        b.text(622,yy,f'{i+1:02}',15.8,'muted');b.text(652,yy,r['name_zh'],16.4,'ink',i<4)
        b.rect(755,yy-11,162,11,'pale');b.rect(755,yy-11,162*v/150,11,c);b.text(1000,yy,f'{v:.2f}',16.5,c,i<2,'end')
    b.line(0,453,1000,453);b.title(0,485,3,'参与、贡献与项目影响',fs=20);b.title(540,485,4,'五域 · 贡献与影响的次序',fs=20)
    b.text(0,515,'同一组 29 国；每类指标分别合计为 100%',15.7,'muted')
    for i,(name,r) in enumerate(shares().items()):
        yy=548+i*63;b.text(0,yy,name,16.5,'ink',True);xx=0
        for v,c in zip(r['shares'],['blue','china','soft']):
            ww=500*v/100;b.rect(xx,yy+9,ww,25,c);b.text(xx+ww/2,yy+28,f'{v:.1f}%',16.4,'white',True,'middle');xx+=ww
    for x,t,c in [(0,'美国','blue'),(122,'中国','china'),(245,'其余 27 国','soft')]:b.rect(x,726,13,13,c);b.text(x+22,739,t,16,'ink')
    b.wrap(0,772,'开发者按所在地、项目按国家标签汇总。份额限于这 29 国，不代表全球总体。',500,15.5,'muted',leading=22)
    b.line(520,469,520,800)
    b.text(540,515,'2026 报告年度 · 两列尺度分别设置',15.7,'muted')
    b.text(758,549,'开发者贡献',16,'muted',anchor='middle');b.text(935,549,'项目影响',16,'muted',anchor='middle')
    order=[GR[2],GR[1],GR[0],GR[3],GR[4]]
    for i,(k,n,c) in enumerate(order):
        yy=580+i*35;v=float(GC[-1][k])/1e4;iv=GS[k]['history'][-1]
        b.text(540,yy,n,16.5,'ink',k=='China')
        b.rect(638,yy-11,105,11,'pale');b.rect(638,yy-11,105*v/700,11,c);b.text(818,yy,f'{v:.1f}',15.8,c,True,'end')
        b.rect(845,yy-11,74,11,'pale');b.rect(845,yy-11,74*iv/180,11,c);b.text(1000,yy,f'{iv:.2f}',15.8,c,True,'end')
    b.line(638,735,743,735);b.text(638,755,'0',14,'muted');b.text(743,755,'700',14,'muted',anchor='end')
    b.line(845,735,919,735);b.text(845,755,'0',14,'muted');b.text(919,755,'180',14,'muted',anchor='end')
    b.text(1000,755,'万',14,'muted',anchor='end')
    b.wrap(540,779,'五域为独立综合序列，与上方国家读数不混排；两列相除不代表“转化率”。',460,15,'muted',leading=21)
    b.save('01-project-influence-map')

def forecast_axes(b,s,x,y,w,h,maxv,ticks):
    anchor=x+(s['end']-s['start'])/(2030-s['start'])*w;b.rect(anchor,y,x+w-anchor,h,'pale')
    for v in ticks:
        yy=y+h-v/maxv*h;b.line(x,yy,x+w,yy);b.text(x-9,yy+5,f'{v:g}',15,'muted',anchor='end')
    for yr in [s['start'],s['end'],2030]:b.text(x+(yr-s['start'])/(2030-s['start'])*w,y+h+25,yr,15.5,'muted',anchor='middle')
    b.line(anchor,y,anchor,y+h,'#9CAEBB',1,'4 5')

def forecast_lines(b,s,x,y,w,h,maxv,c,band=False):
    point=lambda year,value:(x+(year-s['start'])/(2030-s['start'])*w,y+h-value/maxv*h)
    hist=[point(s['start']+i,v) for i,v in enumerate(s['history'])]
    up=[hist[-1]]+[point(s['end']+i+1,v) for i,v in enumerate(s['continued'])]
    low=[hist[-1]]+[point(s['end']+i+1,v) for i,v in enumerate(s['slowing'])]
    if band:b.path(up+low[::-1],c,0,fill=c,opacity=.1)
    b.path(hist,c,2.7);b.path(up,c,2.1,dash='7 5');b.path(low,c,1.8,dash='2 4')
    for xx,yy in hist:b.circle(xx,yy,2.7,c)

def second():
    b=Figure();b.title(0,22,1,'五域项目影响与 2030 条件情景')
    for x,label,dash in [(620,'历史',None),(745,'延续','7 5'),(875,'放缓','2 4')]:b.line(x,15,x+26,15,'ink',2.3,dash);b.text(x+35,21,label,16,'muted')
    b.text(0,54,'万 OpenRank · 报告年度',16,'muted')
    x=50;y=78;w=552;h=188;maxv=250
    forecast_axes(b,GS['Europe'],x,y,w,h,maxv,[0,50,100,150,200,250]);b.text(342,64,'2027—2030：情景',15.5,'muted')
    for k,n,c in GR:forecast_lines(b,GS[k],x,y,w,h,maxv,c)
    b.text(809,54,'2026／万',16,'muted',anchor='end');b.text(1000,54,'2030 放缓—延续',16,'muted',anchor='end')
    for j,(k,n,c) in enumerate(GR):
        s=GS[k];yy=94+j*39;b.text(630,yy,n,17,c,True);b.text(809,yy,f'{s["history"][-1]:.2f}',17,'ink',anchor='end');b.text(1000,yy,f'{s["slowing"][-1]:.2f}—{s["continued"][-1]:.2f}',17,c,True,'end')
    b.text(630,293,'低值组见右侧读数及下方增幅比较。',15.4,'muted')
    b.line(0,310,1000,310);b.title(0,341,2,'全球、美国与中国 · 自然年历史及情景')
    b.text(0,369,'实线：2021—2025 自然年；虚线：2026—2030 推演，2026 点亦为情景值。',16,'muted')
    for j,(k,c,maxv,ticks) in enumerate([('全球','teal',500,[0,250,500]),('美国','blue',300,[0,150,300]),('中国','china',180,[0,90,180])]):
        left=j*345;s=NS[k];x=left+45;y=412;w=245;h=100
        b.text(left,398,f'{k}／万 OpenRank',17,'ink',True);forecast_axes(b,s,x,y,w,h,maxv,ticks);forecast_lines(b,s,x,y,w,h,maxv,c,True)
        b.text(left,558,f'2025：{s["history"][-1]:.1f}',16.2,c,True);b.text(left,581,f'2030：{s["slowing"][-1]:.0f}—{s["continued"][-1]:.0f}',16.2,c,True)
    b.line(0,596,1000,596);b.title(0,627,3,'相对位置上升，绝对差仍大',fs=20);b.title(548,627,4,'不同基数下的增长',fs=20)
    b.text(0,655,'五域序列 · 中国／美国；灰条表示 100%',15.7,'muted');b.text(548,655,'2022—2026 报告年度累计增长',15.7,'muted')
    ratios=[float(r['China'])/float(r['United States'])*100 for r in GI]
    for yy,yr,v in [(694,'2022',ratios[0]),(742,'2026',ratios[-1])]:
        b.text(0,yy,yr,16,'muted');b.rect(61,yy-17,320,21,'pale');b.rect(61,yy-17,320*v/100,21,'china');b.text(485,yy,f'{v:.1f}%',22,'china',True,'end')
    gap0=(float(GI[0]['United States'])-float(GI[0]['China']))/1e4;gap1=(float(GI[-1]['United States'])-float(GI[-1]['China']))/1e4
    b.text(0,784,f'美国减中国：{gap0:.1f} 万 → {gap1:.1f} 万 OpenRank',16,'muted')
    b.line(519,613,519,800)
    for i,(k,n,c) in enumerate([GR[1],GR[4],GR[3],GR[2],GR[0]]):
        yy=683+i*25;v=(GS[k]['history'][-1]/GS[k]['history'][0]-1)*100
        b.text(548,yy,n,16.4,'ink',k=='China');b.rect(651,yy-11,235,11,'pale');b.rect(651,yy-11,235*v/160,11,c);b.text(1000,yy,f'+{v:.1f}%',17,c,True,'end')
    b.save('02-project-influence-evolution')

def third():
    b=Figure();b.title(0,22,1,'中国项目 · 样本前 20');b.title(548,22,2,'影响集中于哪些项目',fs=20)
    b.text(0,51,'30 项归档样本；原表统计窗口待核',15.7,'muted');b.text(490,51,'OpenRank',16,'muted',anchor='end')
    for i,r in enumerate(PROJECTS[:20]):
        yy=79+i*18.4;v=float(r['openrank']);c='china' if i<2 else 'teal'
        b.text(0,yy,f'{i+1:02}',15.4,'muted');b.text(31,yy,r['project'],16,'ink',i<2)
        b.rect(185,yy-11,190,10,'pale');b.rect(185,yy-11,190*v/80000,10,c);b.text(490,yy,f'{v:,.2f}',16,c,i<2,'end')
    b.line(520,0,520,445)
    b.text(548,52,'以原表 30 个标签的读数之和为分母',15.6,'muted')
    vals=[float(PROJECTS[0]['share_pct']),float(PROJECTS[1]['share_pct']),sum(float(r['share_pct']) for r in PROJECTS[2:10]),sum(float(r['share_pct']) for r in PROJECTS[10:])]
    # Two stacked rows, kept proportional by area, with readable labels.
    xx=548;ww=452;hh=192;yy=75;top=vals[0]+vals[1];toph=hh*top/100
    segments=[(xx,yy,ww*vals[0]/top,toph,0),(xx+ww*vals[0]/top,yy,ww*vals[1]/top,toph,1),(xx,yy+toph,ww*vals[2]/(100-top),hh-toph,2),(xx+ww*vals[2]/(100-top),yy+toph,ww*vals[3]/(100-top),hh-toph,3)]
    for sx,sy,sw,sh,i in segments:
        c=['china','#C27645','teal','soft'][i];b.rect(sx,sy,sw-2,sh-2,c)
        label=['OpenHarmony','openEuler','第 3—10 项','第 11—30 项'][i]
        b.text(sx+sw/2,sy+sh/2-5,label,17 if i!=1 else 15.5,'white',True,'middle');b.text(sx+sw/2,sy+sh/2+25,f'{vals[i]:.1f}%',25,'white',True,'middle')
    b.text(548,300,'前两项',18,'muted');b.text(730,302,f'{sum(vals[:2]):.1f}%',30,'china',True,'end');b.text(804,300,'前十项',18,'muted');b.text(1000,302,f'{sum(vals[:3]):.1f}%',30,'teal',True,'end')
    b.wrap(548,343,'头部项目承载较多网络影响；其余项目提供技术与组织多样性。',452,19,'ink',True,leading=28)
    b.wrap(548,408,'这是标签读数结构，不是全国份额；项目标签可能重叠，不解释为去重后的资产总量。',452,15.5,'muted',leading=22)
    b.line(0,458,1000,458);b.title(0,490,3,'中国项目影响 · 五年增长',fs=20);b.title(548,490,4,'参与规模与影响位置',fs=20)
    b.text(0,519,'五域年度序列 · 万 OpenRank',15.7,'muted');b.text(548,519,'影响前十项目；两类位次均在 30 项样本内',15.2,'muted')
    vals=GS['China']['history'];xx0=45;yy0=551;ww=443;hh=165
    for v in [0,20,40,60,80]:
        y=yy0+hh-v/80*hh;b.line(xx0,y,xx0+ww,y);b.text(xx0-10,y+5,str(v),14.6,'muted',anchor='end')
    pts=[(xx0+i*ww/4,yy0+hh-v/80*hh) for i,v in enumerate(vals)];b.path(pts,'blue',2.8)
    for i,(x,y) in enumerate(pts):
        b.circle(x,y,3.4,'blue');b.text(x,740,2022+i,14.8,'muted',anchor='middle');b.text(x+8 if i==0 else x,y-12,f'{vals[i]:.2f}',14.8,'blue',True,'start' if i==0 else 'middle')
    b.text(0,773,'五年增长 159.9% · 2026 相当于美国的 41.2%',16.4,'blue',True)
    b.text(0,799,'综合年度序列；不与上方 30 项标签样本合计。',15.2,'muted')
    b.line(520,475,520,800)
    b.circle(554,542,5.5,'blue',False);b.text(567,548,'活跃位次',15,'blue');b.circle(692,542,3.8,'teal');b.text(704,548,'影响位次',15,'teal');b.text(1000,548,'左侧位次高',15,'muted',anchor='end')
    x=730;w=259
    for t in [1,5,10,15,20]:
        xx=x+(t-1)/19*w;b.line(xx,558,xx,774);b.text(xx,799,t,14.8,'muted',anchor='middle')
    for i,r in enumerate(PROJECTS[:10]):
        yy=575+i*21.3;a=int(r['participant_rank_in_sample']);rank=int(r['rank']);c='china' if r['project'] in ['openGauss','PaddlePaddle'] else 'teal'
        b.text(548,yy,r['project'],16.3,'ink',c=='china');xx=x+(a-1)/19*w;cx=x+(rank-1)/19*w
        b.line(xx,yy-6,cx,yy-6,'soft',2.5);b.circle(xx,yy-6,5.5,'blue',False);b.circle(cx,yy-6,3.6,c)
    b.save('03-china-project-structure')

def render_all():
    first();second();third()
    derived={'fixed_country_codes':list(CR),'fixed_country_shares':shares(),'five_domain_scenarios':GS,'natural_year_scenarios':NS,'china_sample_sum':sum(float(r['openrank']) for r in PROJECTS),'china_top2_share':sum(float(r['share_pct']) for r in PROJECTS[:2]),'china_top10_share':sum(float(r['share_pct']) for r in PROJECTS[:10])}
    (D/'derived-v01.json').write_text(json.dumps(derived,ensure_ascii=False,indent=2))
    (R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
    print(json.dumps([{'figure':q['figure'],'outside':len(q['out_of_bounds']),'overlaps':q['overlaps']} for q in QA],ensure_ascii=False))
