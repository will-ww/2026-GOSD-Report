from build import *
import re, datetime as dt

SOURCE=R.parent/'hf_fig51_inputs/source/GOSD_2026_Chapter5_Merged_Source_v0.2'
S=json.loads((SOURCE/'inputs/51/data/supply-observation.json').read_text())
G=json.loads((SOURCE/'inputs/51/data/map-geometry.json').read_text())
V=json.loads((R.parent/'hf_verify_data/figure51_verified_data.json').read_text())
C.update(violet='#7253A2',gold='#9A7042')

def mix(a,b,t):
    a=cl(a).lstrip('#');b=cl(b).lstrip('#')
    return '#'+''.join(f'{round(int(a[i:i+2],16)*(1-t)+int(b[i:i+2],16)*t):02x}' for i in (0,2,4))

def bounds(geos):
    pts=[]
    for g in geos:
        for cmd,ss in re.findall(r'([MLZ])([^MLZ]*)',g['d']):
            if cmd!='Z':
                v=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',ss)];pts+=list(zip(v[::2],v[1::2]))
    return min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)

def world(f,x,y,w,h):
    geos=[g for g in G['world'] if g['id']!='AQ'];a,b,c,d=bounds(geos)
    sc=min(w/(c-a),h/(d-b));tx=x+(w-(c-a)*sc)/2-a*sc;ty=y+(h-(d-b)*sc)/2-b*sc
    values={r['code']:r['models'] for r in S['assets']['models']['countries'] if r['models']>0}
    f.items.append(f'<g transform="translate({tx},{ty}) scale({sc})">')
    for g in geos:
        k='CN' if g['id'] in ['TW','HK','MO'] else g['id'];v=values.get(k)
        t=math.log1p(v)/math.log1p(max(values.values())) if v is not None else 0
        col=mix('#DFEDF2','blue',t) if v is not None else '#F0F3F5'
        f.items.append(f'<path d="{g["d"]}" fill="{col if g.get("kind")!="line" else "none"}" stroke="#A9B6BF" stroke-width="{.48/sc}"/>')
    f.items.append('</g>')
    centers={g['id']:(tx+g['center'][0]*sc,ty+g['center'][1]*sc) for g in geos if g.get('center')}
    for code,label,dx,dy in [('US','美国 46,314',-3,7),('CN','中国 6,093',8,7),('FR','法国 3,186',-29,-4),('IN','印度 657',10,18),('BR','巴西 794',0,1)]:
        px,py=centers[code];lx=px+dx;ly=py+dy;ww=tw(label,15.7,True)
        if dx or dy:f.line(px,py,lx,ly-5,'muted',.65)
        f.rect(lx-ww/2-4,ly-16,ww+8,21,'white',.92);f.text(lx,ly,label,15.7,'ink',True,'middle')

def plot(f,x,key,color,maximum):
    data=V['assets'][key]['weekly'];x0=x+32;x1=x+228;top=278;bottom=385
    start=dt.date(2022,3,6);end=dt.date(2026,7,18)
    xx=lambda d:x0+(d-start).days/(end-start).days*(x1-x0)
    f.rect(xx(dt.date(2025,7,1)),top,xx(dt.date(2026,6,30))-xx(dt.date(2025,7,1)),bottom-top,'pale')
    for v in [0,maximum/2,maximum]:
        yy=bottom-v/maximum*(bottom-top);f.line(x0,yy,x1,yy,'line',.8)
        t=f'{v/10000:g}万' if maximum>2000 and v else str(int(v))
        f.text(x0-5,yy+4,t,13.5,'muted',anchor='end')
    chunks=[];pts=[]
    for r in data:
        if r['count'] is None:
            if pts:chunks.append(pts);pts=[]
        else:pts.append((xx(dt.date.fromisoformat(r['week_start'])),bottom-r['count']/maximum*(bottom-top)))
    if pts:chunks.append(pts)
    for pts in chunks:
        f.path([(pts[0][0],bottom)]+pts+[(pts[-1][0],bottom)],color,0,fill=color,opacity=.055)
        f.path(pts,color,2.35)
    if key=='papers':
        gx=xx(dt.date(2026,3,13));gx1=xx(dt.date(2026,3,31))
        f.rect(gx,top,gx1-gx,bottom-top,'gold',.11)
        f.text(x+130,263,'3 月有 19 天无记录',14.5,'gold',anchor='middle')
    for d,t,an in [(start,'2022.03','start'),(dt.date(2024,1,1),'2024','middle'),(end,'2026.07','end')]:
        f.text(xx(d),406,t,13.7,'muted',anchor=an)

def buildfig():
    f=Figure(852)
    f.title(0,24,'1','HF 的资产与协作规模','teal',21)
    f.text(1000,24,'OpenGauge 观测 · 2026.11.11 读取',15,'muted',anchor='end')
    cards=[('模型  Models','322.61 万','权重与配套文件','累计下载 787.3 亿次','blue'),('数据集  Datasets','112.41 万','训练与评测数据','累计下载 41.8 亿次','teal'),('应用空间  Spaces','152.35 万','可运行的 AI 应用与演示','累计点赞 115.8 万次','violet'),('论文  Papers','97,161','研究文献与资源关联','累计赞同 47.7 万次','gold')]
    for i,(label,total,desc,eng,col) in enumerate(cards):
        x=i*253
        f.rect(x,42,241,112,'pale');f.rect(x,42,241,3,col)
        f.text(x+12,66,label,18,col,True);f.text(x+12,101,total,31,'ink',True)
        f.text(x+12,124,desc,15.2,'muted');f.text(x+12,145,eng,16.5,col,True)
    f.text(0,178,'协作主体',16,'muted',True);f.text(88,178,'106.76 万账号',19,'ink',True)
    f.text(249,178,'含 753 个组织账号',15.5,'muted')
    f.text(518,178,'社区帖子',16,'muted',True);f.text(607,178,'1,751',19,'ink',True)
    f.text(687,178,'条  ·  评论 2,963 条',15.5,'muted')
    f.line(0,193,1000,193)
    f.title(0,221,'2','仓库新增与论文记录的周度变化','teal',21)
    f.text(1000,221,'单位：个 · 浅底为主期 · 论文另用纵轴',15,'muted',anchor='end')
    for i,(key,title,col) in enumerate([('models','模型','blue'),('datasets','数据集','teal'),('spaces','Spaces','violet'),('papers','论文','gold')]):
        x=i*253;f.text(x,247,title,18.5,col,True)
        if key!='papers':
            y=V['assets'][key]['yoy_pct'];f.text(x+235,247,f'同比 +{y:.1f}%',18,col,True,'end')
            f.text(x,265,f"主期新增 {V['assets'][key]['main']['sum']/1e4:.2f} 万",14.5,'muted')
        else:f.text(x+235,247,'同比不计算',15.5,'muted',anchor='end')
        plot(f,x,key,col,1200 if key=='papers' else 40000)
    f.text(0,426,'同比按 2025.07—2026.06 与前一年同窗逐日合计；周线按周日至周六聚合，统一截至 2026.07.18。',14.3,'muted')
    f.text(0,446,'前三类为新增仓库数；论文为来源日期记录数，日期含义未明，不等同于 HF 当周新收录。',14.3,'muted')
    f.line(0,460,1000,460)
    f.title(0,480,'3','全球模型供给地图','teal',21)
    f.text(0,503,'826 个组织账号 · 73,088 个模型 · 2026.10.17 冻结样本',15,'muted')
    world(f,0,515,578,261)
    for i in range(6):f.rect(4+i*18,779,18,9,mix('#DFEDF2','blue',i/5))
    f.text(122,788,'模型数 · 对数色阶',14,'muted');f.rect(306,779,11,9,'#F0F3F5');f.text(326,788,'样本未覆盖',14,'muted')
    f.line(594,463,594,790)
    f.title(615,480,'4','供给与获取的地域结构','teal',20)
    cats=[('US','美国','blue'),('CN','中国','china'),('FR','法国','teal'),('OTHER','其余','soft')]
    for i,(_,n,c) in enumerate(cats):
        x=615+i*95;f.rect(x,500,10,10,c);f.text(x+15,511,n,15.5,'muted')
    for i,key in enumerate(['models','datasets']):
        rows=S['assets'][key]['countries'];den=S['assets'][key]['summary'][key];v={r['code']:r[key] for r in rows};yy=539+i*75
        f.text(615,yy,'模型仓库' if i==0 else '数据集',17,'ink',True);f.text(998,yy,f'{den:,} 个',16,'muted',anchor='end')
        left=615
        for code,n,c in cats:
            num=v.get(code,den-sum(v[k] for k in ['US','CN','FR']));ww=383*num/den
            f.rect(left,yy+12,ww,24,c)
            if ww>65:f.text(left+ww/2,yy+29,f'{num/den*100:.1f}%',15,'white',True,'middle')
            left+=ww
        f.text(615,yy+57,f"美国 {v['US']/den*100:.1f}%  ·  中国 {v['CN']/den*100:.1f}%",14.7,'muted')
    rows=S['assets']['models']['countries'];dl=sum(r['downloads'] for r in rows if r['code'] in ['US','CN'])/S['assets']['models']['summary']['downloads']*100
    f.line(615,686,1000,686)
    f.text(615,710,'中美合计占比',16,'muted',True)
    for i,(label,pct,c) in enumerate([('模型数',52407/73088*100,'blue'),('模型下载',dl,'teal')]):
        y=737+i*36;f.text(615,y,label,15.5,'muted');f.rect(705,y-11,205,10,'pale');f.rect(705,y-11,205*pct/100,10,c);f.text(1000,y,f'{pct:.1f}%',19,c,True,'end')
    f.line(0,805,1000,805)
    f.wrap(0,825,'图 5-1 HF 资产规模、增长与全球供给。来源：OpenGauge 接口与归档；仓库总量更新日为 2026.11.09，论文与社区为本次读取值。',1000,14.3,'muted',leading=20)
    f.wrap(0,846,'地域按发布组织归属，采用 2026.10.17 冻结组织样本，非全平台分布；下载与点赞采用来源汇总口径，不代表独立用户、部署量或质量。',1000,14.3,'muted',leading=20)
    f.save('fig-5-1-hf-assets')
    (R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))

def maketex():
    ensure_fonts();export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
    tex=r'''\documentclass{article}
\usepackage{layout}
\hypersetup{pdftitle={GOSD 2026 图5-1 HF资产全景 单页评审版 v0.3},pdfsubject={HF资产规模、周新增趋势与全球供给地域结构}}
\begin{document}
\begin{canvas}
\Header{第五章 · 全球开源大模型发展洞察}{teal}
'''
    tex+=box(15,27,180,'5.1　供给与贡献：HF 资产全景',19,24,'ink',True,True)
    tex+=box(15,40,180,'Hugging Face（HF）连接模型、数据、应用与研究文献。规模揭示资源积累，新增反映供给节奏，地图则定位发布者；三者共同呈现可被持续接续的 AI 资产生态。',9.8,14.2,'muted',False,True)
    tex+=r'\node[anchor=north west,inner sep=0pt] at \Pos{15}{54}{\includegraphics[width=180mm]{.build/assets/fig-5-1-hf-assets.pdf}};'+'\n'
    # Keep the report\'s four numbered interpretations and clear reading order.
    notes=[
      (15,214.5,'① 资产供给已超出模型仓库','模型与数据提供开发材料，Spaces 承载应用与演示，论文和社区连接知识与讨论。不同资产需要分别统计，不能把仓库数、账号数与互动量相加。'),
      (108,214.5,'② 数据与应用的供给增速更快','主期新增模型 112.67 万、数据集 52.04 万、Spaces 87.13 万；同比增幅依次为 7.8%、101.0% 和 169.3%。增长体现发布活动，不直接证明使用成效。'),
      (15,247,'③ 供给节点集中，也存在多元入口','冻结组织样本中，美国模型份额为 63.4%，中国为 8.3%；法国、印度、巴西等亦有可见供给。地图描述发布组织归属，不代表全部研发或使用所在地。'),
      (108,247,'④ 资产类型与获取活动呈现不同重心','美国的数据集份额低于其模型份额，中国则相反；中美占模型数 71.7%，占模型下载 86.6%。数量、获取活动与开放条件应联读，后续章节再看接续与完整交付。')
    ]
    for x,y,title,body in notes:
        tex+=box(x,y,87,title,10.3,14.5,'teal',True,True)
        tex+=box(x,y+6.5,87,body,9.25,14.7,'ink',False,False)
    tex+=r'''\Footer{02}
\end{canvas}
\end{document}'''
    (R/'report.tex').write_text(tex)
    compile_tex()
    # Add compact verified source links directly to the caption, without a second appendix page.
    doc=fitz.open(O/'report.pdf');p=doc[0]
    p.insert_link({'kind':fitz.LINK_URI,'from':fitz.Rect(42.5,567,552.7,579),'uri':'http://47.100.76.186:9529/overview'})
    p.insert_link({'kind':fitz.LINK_URI,'from':fitz.Rect(42.5,580,552.7,592),'uri':'https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/c51e3441361407b68f10b339d97eff288319b503/preview/content/gosm/supply-observation.json'})
    doc.save(O/'GOSD_2026_Figure_5-1_HF_Assets_Review_v0.3.pdf')

if __name__=='__main__':
    buildfig();maketex()
