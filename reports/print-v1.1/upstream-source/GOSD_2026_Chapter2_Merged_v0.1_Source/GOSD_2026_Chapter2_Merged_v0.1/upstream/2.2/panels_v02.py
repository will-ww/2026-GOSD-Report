from build import *

NAT=json.loads((D/'natural-contribution.json').read_text())
NATA=json.loads((D/'natural-developers.json').read_text())
NATCN=json.loads((D/'natural-CN-contribution.json').read_text())
NATCNA=json.loads((D/'natural-CN-developers.json').read_text())
NAR={r['code']:r for r in NATA['leaderboards'][1]['data']}
NPAR={r['code']:r for r in NATCNA['leaderboards'][1]['data']}
GT=readcsv('five_groups_contribution.csv')
GR=[('Europe','欧洲','teal'),('China','中国','china'),('United States','美国','blue'),('Global South representatives','南方六国','south'),('India','印度','india')]
WORLD=json.loads((D/'contribution.json').read_text())
CR={r['code']:r for r in WORLD['leaderboards'][0]['data']}
AR={r['code']:r for r in json.loads((D/'public-developers.json').read_text())['leaderboards'][1]['data']}
SOUTH=[CR[c] for c in ['BR','ID','VN','ZA','PH','EG']]
FLOWS=readcsv('project_sources_top10.csv')

def scenario(values,start):
    end=start+len(values)-1;g=(values[-1]/values[0])**(1/(len(values)-1))-1
    slow=[];value=values[-1]
    for h in range(1,2030-end+1):value*=1+g*.8**h;slow.append(value)
    return {'start':start,'end':end,'history':values,'growth':g,'slowing':slow,'continued':[values[-1]*(1+g)**h for h in range(1,2030-end+1)]}

GS={key:scenario([float(r[key])/1e4 for r in GT],2022) for key,n,c in GR}
NS={key:scenario([v/1e4 for v in NAT['trends'][i]['values']],2021) for i,key in enumerate(['全球','美国','中国'])}

def first_lower(b):
    b.line(0,453,1000,453);b.title(0,485,3,'位次与平均贡献 · 2025 快照',fs=20);b.title(550,485,4,'五域综合贡献 · 2026 年度',fs=20)
    b.text(0,515,'贡献总量前十；同表贡献度 ÷ 活跃人数',15.7,'muted')
    b.circle(8,539,5.5,'blue',False);b.text(21,545,'活跃位次',15.7,'blue');b.circle(145,539,4,'teal');b.text(157,545,'贡献位次',15.7,'teal')
    b.text(500,545,'平均贡献',15.7,'muted',anchor='end')
    x=82;w=224;bx=345;bw=102
    for t in [1,5,10,15]:
        xx=x+(t-1)/14*w;b.line(xx,559,xx,764);b.text(xx,785,t,15.5,'muted',anchor='middle')
    for i,r in enumerate(NAT['leaderboards'][0]['data'][:10]):
        yy=574+i*20.5;a=NAR[r['code']];avg=r['value']/a['value'];xx=x+(a['rank']-1)/14*w;cx=x+(r['rank']-1)/14*w
        strong=r['code'] in ['DE','IN','NL'];b.text(0,yy,r['name_zh'],16.5,'ink',strong);b.line(xx,yy-6,cx,yy-6,'soft',3)
        b.circle(xx,yy-6,5.7,'blue',False);b.circle(cx,yy-6,3.5,'teal')
        b.rect(bx,yy-12,bw*avg/1.2,11,'teal' if strong else 'soft');b.text(500,yy,f'{avg:.3f}',16,'ink',strong,'end')
    b.line(bx,764,bx+bw,764)
    for t in [0,.6,1.2]:b.text(bx+bw*t/1.2,785,f'{t:g}',15.5,'muted',anchor='middle')
    b.line(526,469,526,800)
    b.text(1000,516,'万 OpenRank',16,'muted',anchor='end')
    for j,(key,name,c) in enumerate(GR):
        yy=556+j*39;v=float(GT[-1][key])/1e4
        b.text(550,yy,name,17,'ink',key=='China');b.rect(650,yy-12,236,14,'pale');b.rect(650,yy-12,236*v/660,14,c);b.text(1000,yy,f'{v:,.2f}',17,c,True,'end')
    b.wrap(550,753,'五域为独立综合序列，与国家公开估计覆盖不同，不混排、不相加。平均贡献单位为 OpenRank／人。',450,16,'muted',leading=23)

def forecast_axes(b,s,x,y,w,h,maxv,ticks):
    anchor=x+(s['end']-s['start'])/(2030-s['start'])*w
    b.rect(anchor,y,x+w-anchor,h,'pale')
    for v in ticks:
        yy=y+h-v/maxv*h;b.line(x,yy,x+w,yy);b.text(x-9,yy+5,f'{v:g}',15,'muted',anchor='end')
    for yr in [s['start'],s['end'],2030]:b.text(x+(yr-s['start'])/(2030-s['start'])*w,y+h+25,yr,15.5,'muted',anchor='middle')
    b.line(anchor,y,anchor,y+h,'#9CAEBB',1,'4 5')

def forecast_lines(b,s,x,y,w,h,maxv,c,band=False):
    point=lambda year,value:(x+(year-s['start'])/(2030-s['start'])*w,y+h-value/maxv*h)
    hist=[point(s['start']+i,v) for i,v in enumerate(s['history'])]
    up=[hist[-1]]+[point(s['end']+i+1,v) for i,v in enumerate(s['continued'])]
    low=[hist[-1]]+[point(s['end']+i+1,v) for i,v in enumerate(s['slowing'])]
    if band:b.path(up+low[::-1],c,0,fill=c,opacity=.09)
    b.path(hist,c,2.7);b.path(up,c,2.1,dash='7 5');b.path(low,c,1.8,dash='2 4')
    for xx,yy in hist:b.circle(xx,yy,2.7,c)

def second():
    b=Figure();b.title(0,22,1,'五域贡献趋势与 2030 情景')
    for x,label,dash in [(620,'历史',None),(745,'延续','7 5'),(875,'放缓','2 4')]:b.line(x,15,x+26,15,'ink',2.3,dash);b.text(x+35,21,label,16,'muted')
    b.text(0,54,'万 OpenRank · 报告年度',16,'muted')
    x=58;y=78;w=550;h=210;maxv=1600
    forecast_axes(b,GS['Europe'],x,y,w,h,maxv,[0,400,800,1200,1600])
    b.text(350,64,'2027—2030：情景',15.5,'muted')
    for key,name,c in GR:forecast_lines(b,GS[key],x,y,w,h,maxv,c)
    b.text(807,54,'2026／万',16,'muted',anchor='end');b.text(1000,54,'2030 放缓—延续',16,'muted',anchor='end')
    for j,(key,name,c) in enumerate(GR):
        s=GS[key];yy=95+j*42;b.text(635,yy,name,17,c,True);b.text(807,yy,f'{s["history"][-1]:,.1f}',17,'ink',anchor='end');b.text(1000,yy,f'{s["slowing"][-1]:,.0f}—{s["continued"][-1]:,.0f}',17,c,True,'end')
    b.text(635,314,'区间来自两种假设，不是置信区间。',15.5,'muted')
    b.line(0,331,1000,331);b.title(0,364,2,'全球、美国与中国 · 自然年历史及 2030 情景')
    b.text(0,393,'实线：2021—2025 自然年；虚线：2026—2030 推演，2026 点亦为情景值。',16,'muted')
    for j,(key,c,maxv,ticks) in enumerate([('全球','teal',3000,[0,1500,3000]),('美国','blue',600,[0,300,600]),('中国','china',220,[0,100,200])]):
        left=j*345;s=NS[key];x=left+45;y=436;w=245;h=105
        b.text(left,422,f'{key}／万 OpenRank',17,'ink',True);forecast_axes(b,s,x,y,w,h,maxv,ticks);forecast_lines(b,s,x,y,w,h,maxv,c,True)
        b.text(left,588,f'2025：{s["history"][-1]:,.1f}',16.2,c,True)
        b.text(left,611,f'2030：{s["slowing"][-1]:,.0f}—{s["continued"][-1]:,.0f}',16.2,c,True)
    b.line(0,626,1000,626);b.title(0,658,3,'全球南方六国 · 2026 年度贡献与参与位置')
    b.text(714,686,'贡献／万',16,'muted',anchor='end');b.text(853,686,'贡献名次',16,'muted',anchor='end');b.text(1000,686,'活跃名次',16,'muted',anchor='end')
    for i,r in enumerate(SOUTH):
        yy=709+i*18;v=r['value']/1e4;b.text(0,yy,r['name_zh'],16.5,'ink',i==0);b.rect(150,yy-11,440,10,'pale');b.rect(150,yy-11,440*v/45,10,'south');b.text(714,yy,f'{v:.2f}',16,'south',True,'end');b.text(853,yy,r['rank'],16,'ink',anchor='end');b.text(1000,yy,AR[r['code']]['rank'],16,'blue',anchor='end')
    b.save('02-contribution-evolution')

def regional_shares():
    cr=json.loads((D/'CN-contribution.json').read_text())['leaderboards'][0]['data']
    ar=json.loads((D/'public-CN-developers.json').read_text())['leaderboards'][1]['data']
    result={}
    for kind,rows in [('活跃',ar),('贡献',cr)]:
        total=sum(r['value'] for r in rows);shares=[]
        for names in [('北京','上海','广东'),('台湾','浙江')]:
            shares.append(sum(r['value'] for r in rows if any(n in r['name_zh'] for n in names))/total*100)
        shares.append(100-sum(shares));result[kind]=shares
    result['difference_pp']=result['贡献'][1]-result['活跃'][1]
    return result

def third_lower(b):
    b.line(0,461,1000,461);b.title(0,494,3,'参与与贡献 · 区域份额',fs=20);b.title(530,494,4,'平均贡献 · 补充规模视角',fs=20)
    b.text(0,523,'2026 报告年度 · 同一组地区的国内份额',16,'muted')
    shares=regional_shares()
    for kind,label,yy in [('活跃','活跃份额',561),('贡献','贡献份额',641)]:
        b.text(0,yy,label,17.5,'ink',True);xx=0
        for v,color in zip(shares[kind],['blue','china','soft']):
            width=475*v/100;b.rect(xx,yy+14,width,31,color);b.text(xx+width/2,yy+37,f'{v:.1f}%',20,'white',True,'middle');xx+=width
    for xx,label,color in [(0,'京沪粤','blue'),(145,'台湾＋浙江','china'),(330,'其他地区','soft')]:
        b.rect(xx,706,14,14,color);b.text(xx+23,720,label,16.5,'ink')
    b.wrap(0,753,f'台湾与浙江：贡献份额高出活跃份额约 {shares["difference_pp"]:.1f} 个百分点（按未舍入值计算）。',475,16,'muted',leading=23)
    b.text(0,801,'份额独立舍入，合计可能不等于 100%。',14.5,'muted')
    b.line(505,477,505,802)
    b.text(530,523,'2025 自然年 · 贡献总量前十地区',16,'muted')
    b.text(605,551,'平均贡献（OpenRank／人）',15.7,'muted');b.text(1000,551,'活跃／万',15.7,'muted',anchor='end')
    raw=NATCN['leaderboards'][0]['data'];ref=sum(r['value'] for r in raw)/sum(r['value'] for r in NPAR.values())
    top=sorted(raw[:10],key=lambda r:r['value']/NPAR[r['code']]['value'],reverse=True)
    x=605;w=220;xx=x+ref/.75*w
    for i,r in enumerate(top):
        yy=577+i*19.5;avg=r['value']/NPAR[r['code']]['value'];c='teal' if avg>=ref else 'blue';name=r['name_zh'].replace('省','').replace('市','')
        b.text(530,yy,name,16.5,'ink',i<3);b.rect(x,yy-12,w*avg/.75,12,c);b.text(898,yy,f'{avg:.3f}',16.3,c,True,'end');b.text(1000,yy,f'{NPAR[r["code"]]["value"]/1e4:.2f}',16.3,'ink',anchor='end')
    b.line(xx,558,xx,763,'#A1B2BE',1.7,'5 5');b.line(x,764,x+w,764)
    for v in [0,.25,.5,.75]:b.text(x+w*v/.75,784,f'{v:g}',15,'muted',anchor='middle')
    b.text(1000,801,f'虚线：全国合计比值 {ref:.3f}',15.5,'muted',anchor='end')

def fourth():
    b=Figure();b.title(0,22,1,'贡献来源网络 · 连接中国与全球社区')
    b.text(1000,50,'20 条记录 · 14 个来源国家 · 2 个项目归属地',16,'muted',anchor='end')
    src=ET.parse(R/'assets/flows-base.svg').getroot();scale=3.85;tx=172.5;ty=-38
    b.items.append(f'<g transform="translate({tx},{ty}) scale({scale})">')
    edges=0;nodes=0
    for e in src:
        tag=e.tag.rsplit('}',1)[-1];include=False
        if tag=='path':
            fill=e.get('fill');stroke=e.get('stroke');d=e.get('d','')
            if fill=='#EBF0F2':include=True
            elif (stroke in ['#155F91','#329A9B'] or fill in ['#155F91','#329A9B']) and ('Q' in d or 'C' in d or (fill in ['#155F91','#329A9B'] and float(d.split(',')[1].split()[0])>25)):
                include=True
                if 'Q' in d or 'C' in d:edges+=1
        elif tag=='circle' and 25<float(e.get('cy'))<100:include=True;nodes+=1
        if include:
            e=copy.deepcopy(e)
            for attr in ['fill','stroke']:
                val=e.get(attr)
                if val=='#329A9B':e.set(attr,C['china'])
                elif val=='#155F91':e.set(attr,C['blue'])
            b.items.append(ET.tostring(e,encoding='unicode'))
    b.items.append('</g>');assert edges==20 and nodes==14,(edges,nodes)
    positions={'美国':(42.921,44.773),'中国':(126.952,45.019),'加拿大':(44.669,34.857),'印度':(120.925,53.766),'新加坡':(133.762,66.559)}
    for name,x,y,dx,dy in [('美国',42.921,44.773,-45,26),('中国',126.952,45.019,5,26),('加拿大',44.669,34.857,-77,-12),('印度',120.925,53.766,-45,26),('新加坡',133.762,66.559,24,6)]:
        px=tx+x*scale;py=ty+y*scale;lx=px+dx;ly=py+dy
        b.line(px,py,lx+12,ly-6,'soft',1);b.rect(lx-3,ly-17,tw(name,17,True)+6,23,'white');b.text(lx,ly,name,17,'ink',True)
    for left,label,c in [(0,'流向中国项目','china'),(0,'流向美国项目','blue')]:
        yy=81 if c=='china' else 109;b.line(left,yy-5,left+29,yy-5,c,2);b.text(left+38,yy,label,16,c)
    b.wrap(0,151,'开发者所在地\n→ 项目归属地\n\n线宽 ∝ √贡献度\n回环 = 本土贡献',163,15.6,'muted',leading=23)
    b.line(0,349,1000,349)
    b.title(0,380,2,'本土建设与跨境参与',fs=20);b.title(540,380,3,'来源集中程度',fs=20)
    for j,(label,vals,c) in enumerate([('中国项目',[79.22,14.02,6.76],'china'),('美国项目',[38.28,39.66,22.06],'blue')]):
        yy=410+j*79;b.text(0,yy,label,17,c,True);xx=0
        for share,color in zip(vals,[c,'soft','#E2E8ED']):b.rect(xx,yy+10,480*share/100,20,color);xx+=480*share/100
        b.text(0,yy+52,f'本土 {vals[0]:.2f}% · 已列境外 {vals[1]:.2f}% · 未列 {vals[2]:.2f}%',15,'muted')
    x=590;y=409;w=376;h=95
    for v in [0,50,100]:
        yy=y+h-v/100*h;b.line(x,yy,x+w,yy);b.text(x-10,yy+5,f'{v}%',15,'muted',anchor='end')
    for j,(target,c) in enumerate([('China','china'),('United States','blue')]):
        vals=[];total=0
        for row in [r for r in FLOWS if r['project_country']==target]:total+=float(row['share_pct']);vals.append(total)
        pts=[(x+i/9*w,y+h-v/100*h) for i,v in enumerate(vals)];b.path(pts,c,2.6)
        for i in [0,2,4,9]:b.circle(*pts[i],3,c)
    for r in [1,3,5,10]:b.text(x+(r-1)/9*w,528,f'前{r}',15.5,'muted',anchor='middle')
    b.text(540,551,'前三来源：中国 87.03% · 美国 52.93%',16,'muted')
    b.line(515,366,515,554);b.line(0,567,1000,567)
    b.title(0,596,4,'中美项目贡献来源 · 前十明细',fs=20)
    zhn={'China':'中国','United States':'美国','Canada':'加拿大','Germany':'德国','Singapore':'新加坡','India':'印度','Czechia':'捷克','Sweden':'瑞典','Bulgaria':'保加利亚','United Kingdom':'英国','France':'法国','Netherlands':'荷兰','Switzerland':'瑞士','Poland':'波兰'}
    for j,(target,vals,c) in enumerate([('China',[79.22,14.02,6.76],'china'),('United States',[38.28,39.66,22.06],'blue')]):
        left=j*520;ww=480
        b.text(left,624,f'{zhn[target]}项目／来源地',16,c,True);b.text(left+351,624,'OpenRank',16,'muted',anchor='end');b.text(left+480,624,'原表份额',16,'muted',anchor='end')
        rows=[r for r in FLOWS if r['project_country']==target]
        for i,r in enumerate(rows):
            yy=647+i*16.8;bold=i<2;b.text(left,yy,zhn[r['developer_country']],15.8,'ink',bold);b.text(left+351,yy,f'{float(r["openrank"]):,.2f}',15.8,c,bold,'end');b.text(left+480,yy,f'{float(r["share_pct"]):.2f}%',15.8,'ink',bold,'end')
    b.line(500,616,500,802);b.save('04-global-collaboration')

def save_derived():
    (D/'regional-shares-v03.json').write_text(json.dumps({'period':'2025-07-01/2026-06-30','groups':['京沪粤','台湾＋浙江','其他地区'],'unit':'%','rounding':'各份额独立舍入；百分点差按未舍入值计算',**regional_shares()},ensure_ascii=False,indent=2))
    (D/'scenarios-v02.json').write_text(json.dumps({'unit':'万 OpenRank','model':'历史复合增速延续/逐步放缓','slowing_multiplier':.8,'five_group_report_years':GS,'natural_years':NS,'forecast_is_probability':False,'natural_2026_point_is_scenario':True,'main_window':'2025-07-01/2026-06-30'},ensure_ascii=False,indent=2))
    avg={'national':[{**r,'active':NAR[r['code']]['value'],'active_rank':NAR[r['code']]['rank'],'average':r['value']/NAR[r['code']]['value']} for r in NAT['leaderboards'][0]['data'][:10]],'province':[{**r,'active':NPAR[r['code']]['value'],'average':r['value']/NPAR[r['code']]['value']} for r in NATCN['leaderboards'][0]['data'][:10]],'period':'2025-01-01/2025-12-31'}
    (D/'averages-v02.json').write_text(json.dumps(avg,ensure_ascii=False,indent=2))
