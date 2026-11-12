from section32 import *
import section32 as old

G100=json.loads((D/'32/company-top100-mainperiod.json').read_text())
CC=Counter(r['country_zh'] for r in G100)
GROUPCOL={'美国':'#3D60A1','中国':'#A4502B','德国':'#7253A2','荷兰':'#477D7B','法国':'#A38135','其他':'#AAB5C3'}
LC=['#3F7899','#B57342','#8669B4','#386F63','#A77D29','#637E38','#4B6199','#31908B','#B34E70','#727B88']
GN=list(GM[0])[1:];CNAMES=list(CM[0])[1:]
for name,c in zip(GN,LC):LINE_COLORS[name]=c
for name,c in zip(CNAMES,LC):LINE_COLORS.setdefault(name,c)

def global_v3():
    f=Figure();panel(f,0,27,1,'全球企业影响力前 20 位');ranking(f,G);f.line(615,0,615,805,'line',1)
    headquarters_global(f)
    panel(f,632,382,3,'100 强席位与排名梯次',19)
    groups=['美国','中国','德国','荷兰','法国','其他']
    for i,r in enumerate(G100):
        g=r['country_zh'] if r['country_zh'] in groups else '其他'
        f.rect(632+i%10*16,408+i//10*16,13,13,GROUPCOL[g])
    for i,g in enumerate(groups):
        yy=424+i*27;v=CC[g] if g!='其他' else sum(v for k,v in CC.items() if k not in groups)
        f.rect(814,yy-12,11,11,GROUPCOL[g]);f.text(835,yy,g if g!='其他' else '其他 10 国',15.5);f.text(998,yy,str(v),20,GROUPCOL[g],True,'end')
    f.text(632,589,'每格 1 家；按全球名次从左至右、逐行排列。',13.5,'muted')
    f.text(632,623,'国家 / 排名',14,'muted')
    for xx,txt in [(816,'1—10'),(896,'11—30'),(985,'31—100')]:f.text(xx,623,txt,13.5,'muted',anchor='end')
    for i,g in enumerate(groups):
        yy=651+i*27;f.text(632,yy,g if g!='其他' else '其他 10 国',15,'ink',g=='中国')
        rr=[r for r in G100 if (r['country_zh']==g if g!='其他' else r['country_zh'] not in groups)]
        for x,(lo,hi) in zip([816,896,985],[(1,10),(11,30),(31,100)]):
            v=sum(lo<=r['rank']<=hi for r in rr);f.text(x,yy,str(v),16,GROUPCOL[g],v>0,'end')
    panel(f,0,649,4,'前五名的分值占比 · 以 100 强为分母',19)
    total=sum(r['openrank'] for r in G100);pct=sum(r['openrank'] for r in G100[:5])/total
    f.text(0,692,f'{pct:.1%}',34,'violet',True);f.text(147,690,'前五名 / 100 强 OpenRank 合计',16,'muted')
    colors=['#554779','#477D7B','#A38135','#7D91AB','#C5CFD8'];bounds=[(0,1),(1,5),(5,10),(10,30),(30,100)];xx=0
    for (a,b),c in zip(bounds,colors):
        p=sum(r['openrank'] for r in G100[a:b])/total;f.rect(xx,714,602*p,32,c);f.text(xx+301*p,736,f'{p:.1%}',16,'white' if b<=30 else 'ink',False,'middle');xx+=602*p
    labels=['第 1 名','第 2—5 名','第 6—10 名','第 11—30 名','第 31—100 名']
    for i,(txt,c) in enumerate(zip(labels,colors)):
        xx=i*121;f.rect(xx,770,10,10,c);f.text(xx+16,781,txt,12.5,'muted')
    f.save('fig-3-4-companies-global')

def panel5(f,data,names,x,y,w,h,title,n,lo,hi,annual=False):
    panel(f,x,y,n,title,19)
    for i,name in enumerate(names):
        col=i%3;row=i//3;xx=x+col*w/3;yy=y+20+row*28
        logo(f,lookup(name),xx,yy,19);f.text(xx+25,yy+15,name,13.7,LINE_COLORS[name])
    left=x+27;right=x+w-31;top=y+90;bottom=y+h-31
    rs=[r for r in data if not annual or int(r['year'])>=2022]
    px=lambda i:left+i*(right-left)/(len(rs)-1);py=lambda v:top+(v-lo)/(hi-lo)*(bottom-top)
    if not annual:f.rect((px(5)+px(6))/2,top-8,right-(px(5)+px(6))/2,bottom-top+16,'pale')
    for rank in range(lo,hi+1):
        if hi-lo>8 and rank not in [lo,5,8,10,12,hi]:continue
        f.line(left,py(rank),right,py(rank),'line',.8);f.text(left-10,py(rank)+4,rank,12.5,'muted',anchor='end')
    for i,r in enumerate(rs):f.text(px(i),bottom+24,r['year'] if annual else r['month'][5:],13 if annual else 12,'muted',anchor='middle')
    for name in names:
        pts=[(px(i),py(int(r[name]))) for i,r in enumerate(rs)];c=LINE_COLORS[name];f.path(pts,c,2.5)
        for a,b in pts:f.circle(a,b,3,c)
        v=int(rs[-1][name]);f.text(right+13,py(v)+4,v,13,c)

def global_time():
    f=Figure();panel(f,0,27,1,'全球年度位置 · 九家企业',20)
    f.text(0,58,'2022—2026 年度标签；第 1 名在上',14,'muted')
    data=[r for r in GY if int(r['year'])>=2022];names=[x for x in GN if x!='Anthropic']
    left,right,top,bottom=29,473,87,339;px=lambda i:left+(right-left)*i/4;py=lambda v:top+(v-1)/17*(bottom-top)
    for v in [1,5,10,15,18]:f.line(left,py(v),right,py(v),'line',.8);f.text(17,py(v)+4,v,13,'muted',anchor='end')
    for i,r in enumerate(data):f.text(px(i),bottom+25,r['year'],14,'muted',anchor='middle')
    for i,name in enumerate(names):
        c=LINE_COLORS[name];pts=[(px(j),py(int(r[name]))) for j,r in enumerate(data)];f.path(pts,c,2.7)
        for a,b in pts:f.circle(a,b,3.3,c)
        v=int(data[-1][name]);ly=88+i*27
        f.path([(right,py(v)),(489,py(v)),(510,ly)],c,1.2)
        logo(f,lookup(name),520,ly-13,18);f.text(545,ly+2,name,14.5,c);f.text(682,ly+2,v,14.5,c,True,'end')
    f.line(707,0,707,374,'line',1)
    panel(f,731,27,2,'Anthropic 的前移',18)
    f.text(731,58,'独立位次轴 · 避免压缩头部差异',13,'muted')
    a,b,t,bo=759,984,90,292;py2=lambda v:t+(v-1)/319*(bo-t)
    for v in [1,100,200,300]:f.line(a,py2(v),b,py2(v),'line',.7);f.text(a-9,py2(v)+4,v,12,'muted',anchor='end')
    pts=[(a+(b-a)*i/4,py2(int(r['Anthropic']))) for i,r in enumerate(data)];f.path(pts,LINE_COLORS['Anthropic'],2.8)
    for i,((xx,yy),r) in enumerate(zip(pts,data)):
        f.circle(xx,yy,3.5,LINE_COLORS['Anthropic']);f.text(xx,yy+(-22 if i==0 else -10 if i<3 else 21),r['Anthropic'],13,LINE_COLORS['Anthropic'],True,'middle');f.text(xx,320,str(r['year'])[-2:],13,'muted',anchor='middle')
    f.text(731,358,'309 → 9  位；并非分值增长倍数',14,'ink')
    rule(f,395)
    panel5(f,GM,GN[:5],0,430,473,327,'全球月度 · 本期前五家',3,1,9)
    panel5(f,GM,GN[5:],527,430,473,327,'全球月度 · 第六至十家',4,4,14)
    f.text(0,788,'月度为 2025.07—2026.06，浅底为 2026 年；四面板分别标尺，追踪同一组十家企业。',15,'muted')
    f.save('fig-3-5-companies-time')

def china_time():
    f=Figure()
    panel5(f,CY,CNAMES[:5],0,27,473,350,'中国年度 · 本期前五家',1,1,8,True)
    panel5(f,CY,CNAMES[5:],527,27,473,350,'中国年度 · 第六至十家',2,5,12,True)
    rule(f,399)
    panel5(f,CM,CNAMES[:5],0,434,473,320,'中国月度 · 本期前五家',3,1,6)
    panel5(f,CM,CNAMES[5:],527,434,473,320,'中国月度 · 第六至十家',4,5,11)
    f.text(0,788,'年度：2022—2026 原表标签；月度：2025.07—2026.06，浅底为 2026 年。名次越小越靠前。',15,'muted')
    f.save('fig-3-5b-companies-time-china')

def render():
    old.global_fig=global_v3;old.evolution_fig=global_time
    pages=old.render();china_time()
    p=pages[0]
    p['caption']='图 3-4　企业前 20 位及全球 100 强的国别、席位与分值构成。来源：报告底表［C1］；OpenDigger 主统计期重算［C7］，前 30 家分值逐项一致。分值窗口：2025.07—2026.06；国别为组织标签，总部为官网核对例证。'
    p['analyses'][1]=('② 100 强覆盖 15 国，总部提供组织入口','按单一国别标签统计，100 强分布于 15 个国家。地图着色表示企业数量，总部圆点另列六家例证。二者连接组织布局与具体城市；企业项目可以汇聚跨境参与，因此不应把总部国别视为贡献发生地。')
    p['analyses'][2]=('③ 扩展观察范围，显现更完整的企业梯次','美国占 70 席、中国占 12 席；德国 4 席，荷兰、法国各 2 席，其余十国各 1 席。中国在前 30 名有 4 家，第 31—100 名另有 8 家，涵盖百度、腾讯、PingCAP 等，补充了头部之外的组织观察。')
    p['analyses'][3]=('④ 前五名占 38.5%，后七十家占 25.3%','以 100 强分值合计为分母，前五名占 38.5%，前十名占 50.2%。第 31—100 名仍承载 25.3%，说明观察范围会改变集中度判断。合作资源既可连接大型平台，也应结合具体技术需求识别专业主体。')
    p=pages[1];p['title']='3.2.1 企业影响位置的持续与变化'
    p['intro']='全球十家企业的轨迹呈现两种节奏：头部位置的长期积累，以及部分 AI 相关企业的快速前移。年度与月度分别阅读，既观察趋势，也保留中途波动。'
    p['caption']='图 3-5a　全球十家企业的年度与月度排名。来源：全球年度表［C3］、月度表［C2］。年度保留原标签、覆盖期待核；月度为 2025.07—2026.06。Anthropic 年度位次单列，月度按本期前五与后五分组，坐标分别标明。'
    p['analyses']=[('① 长期梯次稳定，部分主体逐步前移','2022—2026 年度标签中，微软始终第 1，华为由第 5 前移至第 2，英伟达由第 18 前移至第 6。谷歌、Meta、亚马逊保持前五附近。进入前列既可能来自长期积累，也可能表现为连续年度的梯次上移。'),('② Anthropic 提供另一条上升路径','Anthropic 从 2022 年度第 309 位到 2026 年度第 9 位，显著拓宽十家样本的变化幅度。单列尺度可以同时读清其前移与其他头部企业的差别；这一现象提示关注 AI 企业，但仍需项目证据解释原因。'),('③ 月度换位改变近期头部组合','2026 年 3—6 月，华为连续居月榜第 1，微软居第 2。期末英伟达为第 4，Meta 第 5，亚马逊第 9。静态排名之外，连续月份可以显示相对位置何时调整，却不能替代分值或持续维护投入的核查。'),('④ 快速前移也可能伴随明显波动','Anthropic 的月度位次从期初第 13 前移到 3—4 月第 6，期末回到第 13；Elastic 在 5 月到第 6，随后为第 8。年度结果不能抹平月度波动，追踪企业需要观察变化是否持续，而非把单次跃升等同结构性领先。')]
    cp=page('3.2','3.2.1 企业影响位置的持续与变化（续）','中国十家企业的比较同时覆盖头部平台与专业技术企业。五年位置展示梯次形成，十二个月的记录进一步揭示近期换位，以及第二梯队内部的调整。','fig-3-5b-companies-time-china','图 3-5b　中国十家企业的年度与月度排名。来源：中国年度表［C6］、月度表［C5］。年度覆盖窗口待核；月度为 2025.07—2026.06。按本期前五与第六至十家分组，各面板分别标尺；本期选择不能代表历年全部企业。',[
    ('① 稳定的前两位与逐渐形成的新梯次','华为、阿里巴巴在五个年度标签中保持第 1、第 2；字节跳动由第 8 前移至第 3，蚂蚁集团与百度在第 3—5 位之间变化。扩大至十家后，长期稳定和内部重排可以同时呈现。'),
    ('② 专业主体补充头部之外的观察','腾讯、PingCAP、飞致云、乐鑫科技与赜睿信息科技在年度样本中形成第 5—12 位的不同轨迹。赜睿信息科技在 2025 年度第 12、2026 年度第 10；这类变化需要结合项目构成，不能仅凭排名解释业务成败。'),
    ('③ 近期换位需要与全年位置分开判断','2026 年 4—6 月，字节跳动连续居中国月榜第 2，阿里巴巴第 3；百度同期为第 6。月度次序补充了年度表，提供进一步查阅项目活动的时间线索，不把最近三个月直接外推为下一年度格局。'),
    ('④ 第二梯队在期末呈现不同方向','腾讯在 4—6 月保持第 5；飞致云由 5 月第 10 到 6 月第 8，乐鑫科技同期由第 8 到第 11。赜睿信息科技期末为第 9。专业主体的变化并不同步，合作选择应继续落实到具体技术和维护能力。')], [source('C5',CMF),source('C6',CYF)],['I02','I10'])
    pages.insert(2,cp)
    p=pages[3];p['caption']+=' 集中度对照统一限各自前 30 家。'
    p['analyses'][2]=('③ 相同前 30 名口径下，榜首权重有别','为比较相同榜单深度，这里均取各自前 30 家：中国榜前五名占 79.3%，全球榜占 51.6%；榜首分别占 54.1% 和 18.0%。图 3-4 的 38.5% 则以全球 100 强为分母，二者不能混用，更不能推导中国的全球份额。')
    save_pages('32',pages)
    check={'scope':'2025-07-01/2026-06-30','ranked_company_count':374,'top100_count':100,'country_counts':dict(CC),'top30_exact_match':all(a['openrank']==b['openrank'] for a,b in zip(G,G100)),'top5_share_top100':sum(r['openrank'] for r in G100[:5])/sum(r['openrank'] for r in G100),'company_history_global':GN,'company_history_china':CNAMES}
    (R/'review/v03-data-checks.json').write_text(json.dumps(check,ensure_ascii=False,indent=2))
    return pages
