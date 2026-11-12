"""Three portrait compositions. All rankings retain the fixed source snapshot."""
from common import *
import shapefile, pycountry

GF='table-3-2-1_global_company_openrank_top30.csv'; CF='table-3-2-2_china_company_openrank_top30.csv'
GMF='fig-3-2-2_global_company_monthly_rank.csv'; CMF='fig-3-2-4_china_company_monthly_rank.csv'
GYF='fig-3-2-1_global_company_yearly_rank.csv'; CYF='fig-3-2-3_china_company_yearly_rank.csv'
G=num(rows('32',GF),['rank','openrank','active_repos','active_developers']); CN=num(rows('32',CF),['rank','openrank','active_repos','active_developers'])
GM=rows('32',GMF); CM=rows('32',CMF); GY=rows('32',GYF); CY=rows('32',CYF)
LOGO=json.loads((D/'32/logo-manifest.json').read_text())
C.update(land='#EDF1F4', gold='#A38135', slate='#9DADB9')
COUNTRY_COLORS={'美国':'blue','中国':'china','荷兰':'violet','比利时':'teal'}
SHARE_COLORS=['#554779','#477D7B','#A38135','#9DADB9']
for data in [G,CN]:
    for key in ['openrank','active_repos','active_developers']:
        for i,r in enumerate(sorted(data,key=lambda r:-r[key])):r[key+'_rank']=i+1
def logo(f,r,x,y,size=22):img(f,R/'assets/company-logos'/LOGO[r['company']]['filename'],x,y,size,size)
def lookup(name):return next(r for r in G+CN if r['company_zh']==name)
def ranking(f,data):
    f.text(0,59,'名次 / 企业',14,'muted'); f.text(395,59,'OpenRank',14,'muted',anchor='end')
    f.text(491,59,'仓库 / 个',14,'muted',anchor='end'); f.text(599,59,'关联开发者 / 人',14,'muted',anchor='end')
    for i,r in enumerate(data[:20]):
        y=87+i*26
        if i%2==0:f.rect(0,y-19,602,26,'pale')
        f.text(0,y,f'{int(r["rank"]):02}',15,'muted');logo(f,r,30,y-17,21)
        f.text(60,y,r['company_zh'],16,'ink',i<3)
        f.text(395,y,fmt(r['openrank'],1),16,'ink',i<3,'end')
        f.text(491,y,fmt(r['active_repos']),15,'muted',anchor='end')
        f.text(599,y,fmt(r['active_developers']),15,'ink',anchor='end')
    f.text(0,611,'关联开发者为企业项目的参与者，不等于企业雇员。',15,'muted')

def shares(data):
    vals=[data[0]['openrank'],sum(r['openrank'] for r in data[1:5]),sum(r['openrank'] for r in data[5:10]),sum(r['openrank'] for r in data[10:])]
    return [v/sum(vals) for v in vals]
def stacked(f,x,y,w,h,data,fs=16):
    start=x
    for s,c in zip(shares(data),SHARE_COLORS):
        f.rect(start,y,w*s,h,c);f.text(start+w*s/2,y+h/2+fs*.35,f'{s:.1%}',fs,'white',False,'middle');start+=w*s
def sharelegend(f,x,y,w):
    for i,(label,c) in enumerate(zip(['第 1 名','第 2—5 名','第 6—10 名','第 11—30 名'],SHARE_COLORS)):
        xx=x+w*i/4;f.rect(xx,y-11,11,11,c);f.text(xx+18,y,label,14.5,'muted')
def proj(lon,lat):
    a,b,c,d=1.340264,-.081106,.000893,.003796;t=math.asin(math.sqrt(3)/2*math.sin(math.radians(lat)))
    return 2*math.sqrt(3)*math.radians(lon)*math.cos(t)/(3*(9*d*t**8+7*c*t**6+3*b*t*t+a)),t*(a+b*t*t+c*t**6+d*t**8)
def world(f,x,y,w,h):
    vals=dict(Counter(r['country_code'] for r in json.loads((D/'32/company-top100-mainperiod.json').read_text())));xmin,xmax,ymin,ymax=-2.72,2.72,-1.08,1.32
    scale=min(w/(xmax-xmin),h/(ymax-ymin));ox=x+(w-scale*(xmax-xmin))/2;oy=y+(h-scale*(ymax-ymin))/2
    def point(lon,lat):
        a,b=proj(lon,lat);return ox+(a-xmin)*scale,oy+(ymax-b)*scale
    for s in shapefile.Reader(str(D/'naturalearth_lowres.shp')).iterShapeRecords():
        r=s.record.as_dict();n=r['name']
        if n=='Antarctica':continue
        try:iso={'France':'FR','Norway':'NO','Kosovo':'XK','Somaliland':'SO','N. Cyprus':'CY','Taiwan':'CN'}.get(n) or pycountry.countries.get(alpha_3=r['iso_a3']).alpha_2
        except:iso='ZZ'
        v=vals.get(iso);color=mix('#EDE6F4','violet',.2+.8*math.sqrt(v/70)) if v else C['land']
        inds=list(s.shape.parts)+[len(s.shape.points)]
        for i in range(len(inds)-1):f.path([point(*p) for p in s.shape.points[inds[i]:inds[i+1]]],'white',.45,color)
    return point
def headquarters_global(f):
    panel(f,632,27,2,'总部节点与国别布局',19.8)
    f.text(632,58,'底色：100 强企业数量 · 覆盖 15 国',15,'muted')
    point=world(f,628,78,372,204)
    # Explicitly selected headquarters examples; country fills retain original tags.
    entries=[(-122.12,47.67,634,89,'雷德蒙德 · 微软','start'),(-121.96,37.35,634,250,'圣克拉拉 · 英伟达','start'),(4.90,52.37,998,88,'阿姆斯特丹 · JetBrains','end'),(120.16,30.25,998,239,'杭州 · 阿里巴巴 / 蚂蚁','end'),(114.06,22.55,998,271,'深圳 · 华为','end')]
    for lon,lat,tx,ty,label,anchor in entries:
        px,py=point(lon,lat);f.circle(px,py,3.5,'china' if lon>100 else 'blue')
        endx=tx+4 if anchor=='start' else tx-4
        f.line(px,py,endx,ty-6,'soft',.9)
        width=tw(label,14);left=tx if anchor=='start' else tx-width
        f.rect(left-3,ty-15,width+6,20,'white',.95);f.text(tx,ty,label,14,'ink',False,anchor)
    for i,v in enumerate([1,12,70]):
        xx=632+i*63;f.rect(xx,299,19,11,mix('#EDE6F4','violet',.2+.8*math.sqrt(v/70)));f.text(xx+25,310,v,13.5,'muted')
    f.text(998,310,'家 / 国别标签',13.5,'muted',anchor='end')
    f.text(632,339,'圆点：6 家企业总部例证；非贡献来源。',14,'muted')

def global_fig():
    f=Figure();panel(f,0,27,1,'全球企业影响力前 20 位');ranking(f,G)
    f.line(615,0,615,805,'line',1)
    headquarters_global(f)
    panel(f,632,382,3,'席位数量与高位节点联读',19)
    colors=[]
    for name,n in [('美国',24),('中国',4),('荷兰',1),('比利时',1)]:colors.extend([COUNTRY_COLORS[name]]*n)
    for i,c in enumerate(colors):f.rect(632+(i%6)*26,408+(i//6)*26,22,22,c)
    for i,(name,n) in enumerate([('美国',24),('中国',4),('荷兰',1),('比利时',1)]):
        yy=427+i*31;f.rect(814,yy-13,12,12,COUNTRY_COLORS[name]);f.text(836,yy,name,17);f.text(998,yy,n,22,COUNTRY_COLORS[name],True,'end')
    f.text(632,560,'每格 1 家企业；位置分布如下，非分值占比。',14,'muted')
    x0,x1=708,988;px=lambda rank:x0+(rank-1)/29*(x1-x0)
    f.text(632,594,'国别',14,'muted')
    for k in [1,10,20,30]:f.text(px(k),594,k,14,'muted',anchor='middle')
    for i,name in enumerate(['美国','中国','荷兰','比利时']):
        yy=621+i*43;f.text(632,yy+6,name,17,'ink',name=='中国');f.line(x0,yy,x1,yy,'line',.9)
        for r in G:
            if r['country_zh'][2:]==name:f.circle(px(r['rank']),yy,3.7,COUNTRY_COLORS[name])
    f.text(632,788,'圆点 = 1 家企业；横向位置 = 全球榜名次。',14,'muted')
    panel(f,0,649,4,'前五名的榜内分值构成',20)
    f.text(0,692,f'{sum(shares(G)[:2]):.1%}',34,'violet',True)
    f.text(145,690,'前五名 / 本榜 30 家分值合计',16,'muted')
    stacked(f,0,714,602,32,G,17);sharelegend(f,0,781,602)
    f.save('fig-3-4-companies-global')

LINE_COLORS={'微软':'#3F7899','华为':'#B57342','谷歌':'#8669B4','英伟达':'#6B7C43','阿里巴巴':'#2E8A83','字节跳动':'#8669B4','腾讯':'#3F7899'}
def bump(f,data,names,x,y,w,h,title,n,maxrank,annual=False):
    panel(f,x,y,n,title,19.7)
    for i,name in enumerate(names):
        xx=x+i*w/4;logo(f,lookup(name),xx,y+19,22);f.text(xx+29,y+37,name,15.6,LINE_COLORS[name])
    f.text(x,y+69,'位次 · 第 1 名在上',14,'muted')
    left=x+32;right=x+w-27;top=y+94;bottom=y+h-31
    rs=[r for r in data if not annual or int(r['year'])>=2022]
    px=lambda i:left+i*(right-left)/(len(rs)-1);py=lambda v:top+(v-1)/(maxrank-1)*(bottom-top)
    if not annual:
        start=(px(5)+px(6))/2;f.rect(start,top-9,right-start,bottom-top+18,'pale')
    ticks=[1,5,10,15,18] if maxrank==18 else [1,3,5,8] if maxrank==8 else [1,2,3,4,5,6]
    for rank in ticks:
        f.line(left,py(rank),right,py(rank),'line',.9);f.text(left-11,py(rank)+5,rank,14,'muted',anchor='end')
    for i,r in enumerate(rs):
        label=r['year'] if annual else r['month'][5:];f.text(px(i),bottom+24,label,14 if annual else 13,'muted',anchor='middle')
    for name in names:
        pts=[(px(i),py(int(r[name]))) for i,r in enumerate(rs)];c=LINE_COLORS[name]
        f.path(pts,c,2.8)
        for a,b in pts:f.circle(a,b,3.4,c)
        last=int(rs[-1][name]);f.line(right,py(last),right+11,py(last),c,1.3);f.text(right+17,py(last)+5,last,14,c)

def evolution_fig():
    f=Figure()
    bump(f,GY,['微软','华为','谷歌','英伟达'],0,27,466,349,'全球企业 · 年度位置',1,18,True)
    bump(f,CY,['华为','阿里巴巴','字节跳动','腾讯'],534,27,466,349,'中国企业 · 年度位置',2,8,True)
    rule(f,399)
    bump(f,GM,['微软','华为','谷歌','英伟达'],0,434,466,320,'全球企业 · 月度换位',3,6)
    bump(f,CM,['华为','阿里巴巴','字节跳动','腾讯'],534,434,466,320,'中国企业 · 月度换位',4,6)
    f.text(0,788,'年度：2022—2026 原表标签；月度：2025 年 7 月—2026 年 6 月（浅底为 2026 年）。',15,'muted')
    f.save('fig-3-5-companies-time')

def china_outline(f,x,y,w,h):
    # National outline includes Taiwan; no province aggregation is inferred.
    xmin,xmax,ymin,ymax=73,135,18,54;s=min(w/(xmax-xmin),h/(ymax-ymin));ox=x+(w-(xmax-xmin)*s)/2;oy=y+(h-(ymax-ymin)*s)/2
    def p(lon,lat):return ox+(lon-xmin)*s,oy+(ymax-lat)*s
    for sh in shapefile.Reader(str(D/'naturalearth_lowres.shp')).iterShapeRecords():
        if sh.record.as_dict()['name'] not in ['China','Taiwan']:continue
        inds=list(sh.shape.parts)+[len(sh.shape.points)]
        for i in range(len(inds)-1):f.path([p(*q) for q in sh.shape.points[inds[i]:inds[i+1]]],'#C4CDD8',.8,'land')
    return p

def china_fig():
    f=Figure();panel(f,0,27,1,'中国企业影响力前 20 位');ranking(f,CN);f.line(615,0,615,805,'line',1)
    panel(f,632,27,2,'企业总部的城市节点',20)
    f.text(632,58,'已核对的 9 家企业 · 5 个城市',15,'muted')
    point=china_outline(f,633,70,365,252)
    cities=[('北京',116.40,39.90,925,110,'百度 · 小米'),('杭州',120.16,30.25,978,241,'阿里巴巴 · 蚂蚁集团'),('深圳',114.06,22.55,900,309,'华为 · 腾讯'),('上海',121.47,31.23,978,196,'乐鑫科技 · 道客云'),('合肥',117.23,31.82,828,236,'科大讯飞')]
    for i,(name,lon,lat,bx,by,orgs) in enumerate(cities):
        a,b=point(lon,lat);f.circle(a,b,3.1,'violet');f.line(a,b,bx,by,'violet',1)
        f.circle(bx,by,10,'violet');f.text(bx,by+4.8,i+1,14,'white',True,'middle')
    for i,(name,lon,lat,bx,by,orgs) in enumerate(cities):
        yy=348+i*26;f.circle(641,yy-6,8.5,'violet');f.text(641,yy-2,i+1,12,'white',True,'middle');f.text(660,yy,name,16,'ink',True);f.text(714,yy,orgs,15.5,'muted')
    panel(f,0,649,3,'榜内分布 · 两榜均取前 30 家',19)
    for i,(label,data) in enumerate([('全球榜',G),('中国榜',CN)]):
        yy=678+i*53;f.text(0,yy,label,15,'muted');f.text(600,yy,f'前五名 {sum(shares(data)[:2]):.1%}',15,'violet',True,'end');stacked(f,0,yy+10,602,26,data,15.5)
    sharelegend(f,0,790,602)
    panel(f,632,505,4,'模型企业：代码侧位置',19.5)
    for i,name in enumerate(['DeepSeek','Moonshot AI']):
        r=next(r for r in CN if r['company']==name);yy=544+i*94
        logo(f,r,632,yy-21,26);f.text(669,yy,r['company_zh'],18,'ink',True);f.text(998,yy,f'#{int(r["rank"])}',24,'violet',True,'end')
        f.text(632,yy+30,f'{r["openrank"]:,.2f} OpenRank',16,'ink');f.text(998,yy+30,f'{int(r["active_repos"])} 个仓库',16,'muted',anchor='end')
        f.text(632,yy+55,f'{int(r["active_developers"]):,} 名关联开发者',15.5,'muted');f.text(998,yy+55,f'人数位次 #{r["active_developers_rank"]}',15.5,'violet',True,'end')
    f.line(632,716,1000,716)
    f.wrap(632,748,'代码侧参与位置更靠前；模型复用与采用，仍需联读模型榜和第五章。',366,16,'muted',leading=25)
    f.save('fig-3-6-companies-china')

def render():
    global_fig();evolution_fig();china_fig()
    pages=[
    page('3.2','3.2 全球开源企业影响力排行榜','企业把项目供给、开发者协作与持续维护连接起来。OpenRank 衡量协作网络影响；总部节点、国别席位和榜内分值，则补充说明组织布局与影响位置。','fig-3-4-companies-global','图 3-4　全球企业影响力、总部例证、国别席位与分值构成。来源：GOSD 2026 企业榜［C1］；总部据企业官网于 2026-11-10 核对（期后辅助资料，图中企业名可点击）。国别沿用原表，比例限前 30 家；静态榜统计起止待核。',[
    ('① 三项指标呈现不同的组织组合','微软、华为、谷歌居前三，OpenRank 分别为 16.71 万、14.13 万、8.25 万。华为的仓库数量最多，微软的关联开发者最多。组织影响、供给规模与参与广度各有所指，不能据其中一项推断整体效率。'),
    ('② 总部位置连接空间布局与组织观察','例证把微软、英伟达、华为、阿里巴巴、蚂蚁集团和 JetBrains 落到具体城市。总部是识别组织承载与合作入口的一条线索；企业项目可以汇聚全球参与者，因此仍需与第二章的贡献来源联读。'),
    ('③ 数量集中与头部位置可以同时辨识','原榜 30 家主体中，美国标签占 24 席，中国占 4 席，荷兰、比利时各 1 席。中国四家位于第 2、11、13、22，呈现不同梯次。席位衡量入榜数量，横向位置衡量名次，两者均不等于全球贡献份额。'),
    ('④ 前五名承载约一半的榜内影响分值','前五名合计占本榜分值的 51.6%，第 6—30 名仍占 48.4%。这一结构支持同时关注大型协作入口与专业主体；公共合作应落实到具体项目的开放性、维护责任与持续参与能力。')], [source('C1',GF)],['I02','I10','I11']),
    page('3.2','3.2.1 企业影响位置的持续与变化','年度位置呈现积累路径，月度位置标出变化时点。全球榜与中国榜并置，既能辨认 AI 基础支撑企业的前移，也能观察头部企业之间的持续换位。','fig-3-5-companies-time','图 3-5　所选企业的年度与月度排名轨迹。来源：全球及中国年度表［C3］［C6］、月度表［C2］［C5］。各面板单列位次尺度；年度保留原标签、覆盖期待核，月度为 2025.07—2026.06。名次变化不等于分值增长。',[
    ('① 全球年度位置显示 AI 基础支撑前移','在 2022—2026 年度标签下，英伟达由第 18 前移至第 6，华为由第 5 到第 2，微软维持第 1。它们进入前列的路径并不相同；产业观察可进一步追踪算力软件、工具链与项目维护的具体变化。'),
    ('② 中国年度梯次中，新位置逐步形成','华为与阿里巴巴在五个年度标签中保持第 1、第 2；字节跳动由第 8 前移至第 3，腾讯由第 5 变为第 6。头部梯次相对稳定，并不意味着主体之间没有重排，也不能仅凭榜次变化判断绝对投入的增减。'),
    ('③ 全球月度榜标出换位的持续区间','2026 年 3—6 月，华为连续居全球月榜第 1，微软为第 2；英伟达从期初第 6 前移至期末第 4。连续月份补充了静态榜单，适合识别值得跟踪的变化；其幅度与原因仍需同口径分值及项目证据。'),
    ('④ 中国月度榜揭示年度表内的近期移动','字节跳动在 2026 年 4—6 月连续居中国月榜第 2，腾讯同期由第 6 前移至第 5。年度与月度承担不同观察职责：前者看积累，后者看时点。对产业决策而言，持续监测比单次名次更有解释力。')],[source('C2',GMF),source('C3',GYF),source('C5',CMF),source('C6',CYF)],['I02','I10']),
    page('3.2','3.2.2 中国企业：空间节点与结构差异','中国企业榜呈现大型项目组合与专业主体共存的格局。结合总部节点、分值集中度和模型企业的代码侧位置，可以进一步辨认组织承载、参与基础与跨平台影响的差别。','fig-3-6-companies-china','图 3-6　中国企业影响力、总部例证、榜内集中度与模型企业代码侧画像。来源：企业榜［C1］［C4］；总部据官网于 2026-11-10 核对（期后资料，企业名可点击）。总部仅列 9 家例证；人数位次在中国榜 30 家内重排，不是模型影响排名。',[
    ('① 大型组合之外，专业主体构成支撑层','华为、阿里巴巴、字节跳动、蚂蚁集团居前四，PingCAP、飞致云、乐鑫科技等进入前十。不同企业连接不同规模的仓库和参与者。寻找产业合作伙伴，需要把组织榜单进一步落到具体技术、项目和维护团队。'),
    ('② 城市节点提供跨层观察的连接点','已核对总部例证覆盖北京、杭州、深圳、上海与合肥。杭州连接阿里巴巴与蚂蚁集团，深圳连接华为与腾讯；这些组织节点可与地区榜和项目图谱联读，支持地方识别合作资源，而非直接评价城市整体能力。'),
    ('③ 集中度差异主要体现于榜首分值','中国榜前五名占 79.3%，高于全球榜的 51.6%；两榜榜首分别占 54.1% 和 18.0%。差异主要来自榜首权重。两榜分母各异且主体重叠，不能相加或推导中国全球份额，也尚不足以证明产业依赖。'),
    ('④ 模型企业的参与基础与代码影响有别','深度求索的代码影响位次为第 26，关联开发者人数位次为第 10；Moonshot AI 分别为第 27、第 16。人数基础与网络影响并不同步。评价 AI 开源还须连接模型派生、采用及工具链维护，不能停留在企业代码榜。')],[source('C1',GF),source('C4',CF)],['I02','I10','I11','I12'])]
    save_pages('32',pages)
    checks={'global_shares':shares(G),'china_shares':shares(CN),'global_countries':dict(Counter(r['country_zh'][2:] for r in G)),'model_comparison':[{k:r[k] for k in ['company','rank','openrank','active_repos','active_developers','active_developers_rank']} for r in CN if r['company'] in ['DeepSeek','Moonshot AI']],'monthly_window':[GM[0]['month'],GM[-1]['month']]}
    (R/'review/data-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2));return pages
