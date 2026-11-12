from build import *
SRC=D/'source'
def rows(name):return list(csv.DictReader((SRC/name).open()))
CN={'11':'农林渔猎','21':'采矿与油气','22':'公用事业','23':'建筑业','31-33':'制造业','42':'批发贸易','44-45':'零售贸易','48-49':'运输与仓储','51':'信息业','52':'金融与保险','53':'房地产与租赁','54':'专业科技服务','56':'行政支持服务','61':'教育服务','62':'医疗与社会援助','71':'艺术娱乐休闲','72':'住宿与餐饮','81':'其他服务','92':'公共管理'}
COL={'51':'blue','61':'teal','54':'south','52':'china','22':'#537D25','others':'#DCE5EB'}
COUNT={int(r['year']):{k:int(v) for k,v in r.items() if k!='year'} for r in rows('sector_counts_by_year.csv')}
TOTAL={y:sum(r.values()) for y,r in COUNT.items()}
AI={r['code']:{k:float(v) for k,v in r.items() if k not in ['code','name']} for r in rows('sector_ai_mentions_2025.csv')}
OVER={int(r['year']):{k:float(v) for k,v in r.items() if k!='year'} for r in rows('overall_ai_mentions_by_year.csv')}
SENS={int(r['year']):{k:float(v) for k,v in r.items() if k!='year'} for r in rows('ai_keyword_sensitivity.csv')}
TREND={c:[] for c in ['54','52','51','22','31-33','62']}
for r in csv.DictReader((D/'sector_ai_trends_recovered.csv').open()):TREND[r['code']].append(float(r['pct']))
COL.update({'71':'#697795','62':'#AD536D','31-33':'#318E9A','11':'#8A783D','others':'#E4EBF0'})
def circle_tag(f,x,y,n,c='teal'):
 f.circle(x,y,10,c);f.text(x,y+5,n,14,'white',True,'middle',False)
def rank(y,c):return 1+sum(v>COUNT[y][c] for v in COUNT[y].values())

def p1():
 f=Figure();f.title(0,27,1,'行业位次：整体相似，局部交替',fs=21);f.title(536,27,2,'2025 创建组的行业规模',fs=21)
 f.text(0,61,'按仓库份额排序 · 数字越小，位次越高',16,'muted');f.text(536,61,'19 类行业 · 共 3,461 个仓库',16,'muted')
 f.text(536,93,'行业',16,'muted');f.text(920,93,'仓库数',16,'muted',anchor='end');f.text(999,93,'份额',16,'muted',anchor='end')
 xs=[40,150,260,370,480];ys=lambda k:121+(k-1)*31.1
 for i in range(1,20):
  yy=ys(i);f.line(33,yy,489,yy,'line',.8);f.text(18,yy+5,i,15,'muted',anchor='end')
 for x in xs:f.line(x,113,x,690,'line',.7)
 order=sorted(COUNT[2025],key=COUNT[2025].get,reverse=True);hi=['51','61','54','52','22','71']
 for c in [c for c in order if c not in hi]+hi:
  color=COL[c] if c in hi else '#A5B3BE';pts=[(xs[i],ys(rank(y,c))) for i,y in enumerate(range(2021,2026))]
  f.path(pts,color,3.3 if c in hi else 1.8)
  for x,y in pts:f.circle(x,y,4.5 if c in hi else 3.1,color)
 for i,c in enumerate(order):
  yy=ys(i+1);n=COUNT[2025][c];pct=n/TOTAL[2025]*100;col=COL[c] if c in hi else 'soft'
  f.text(536,yy+6,CN[c],18,'ink' if c in hi else 'muted',c in hi)
  f.rect(707,yy-9,n/604*145,17,col);f.text(920,yy+6,n,17,'ink',c in hi,'end');f.text(999,yy+6,f'{pct:.1f}%',17,'ink' if c in hi else 'muted',c in hi,'end')
  if c=='61':circle_tag(f,517,yy,3)
  if c=='52':circle_tag(f,517,yy,4)
 for i,y in enumerate(range(2021,2026)):
  f.text(xs[i],728,y,17,'ink',True,'middle');f.text(xs[i],751,f'n={TOTAL[y]:,}',14,'muted',anchor='middle')
 f.text(0,785,'横轴为仓库创建年份；并列采用相同位次。',16,'muted')
 f.line(536,720,1000,720)
 f.text(536,753,'0.982',32,'teal',True);f.text(658,752,'两端行业位次相关系数',18,'ink',True)
 f.text(536,785,'越接近 1，2021 与 2025 的整体排序越相似。',16,'muted')
 f.save('fig-2-8-1')
 return dict(title='2.8 全球开源行业地图',intro='开源服务于哪些行业？本节借鉴北美行业分类体系（NAICS），按文本估计仓库应用领域。2026 年 11 月 9 日快照覆盖 18,086 个英文文本样本，呈现行业结构的延续与 AI 信号的分化。',figure='fig-2-8-1',caption='图 2.8-1  19 个行业的位次演变与 2025 创建组规模。来源：团队 OpenDigger–NAICS 研究及配套数据。年份为仓库创建年份，文本来自同一期后快照；每个仓库归入一类。',analyses=[
 ('① 宏观格局延续，中部位次交替','2021 与 2025 两端的行业位次相关系数为 0.982，信息业始终居首；中部行业则有交替。这表明，AI 相关表述的增加，可以发生在总体相似的行业结构之中。'),
 ('② 开源供给已跨越单一信息行业','2025 创建组中，信息业占 17.5%，其余 82.5% 分布于教育、专业服务、金融、制造及公共服务等领域。行业标签由此补充了技术分类，让开源的潜在服务对象更清晰。'),
 ('③ 教育与文娱的相对位置上移','教育由第 3 位升至第 2 位，份额由 10.9% 变为 12.3%；艺术娱乐休闲由第 7 位升至第 6 位，份额由 6.5% 变为 7.8%。它们提示开源供给具有广泛的知识与内容应用基础。'),
 ('④ 位次须与份额结合判断','金融与保险由第 5 位升至第 4 位，份额却从约 8.2% 变为 8.1%；公用事业在第 3—7 位之间波动。相对位置变化不能直接解释为行业规模的增减，更不能替代实际使用评价。')])

def p2():
 f=Figure();f.title(0,27,1,'不同创建群体的 AI 信号',fs=21);f.title(370,27,2,'行业差异：对照全样本平均水平',fs=21)
 f.text(0,62,'提及比例 / %',16,'muted');f.text(370,62,'2025 创建组 · 比例 / % · n 为样本数',16,'muted')
 # Three compact legend entries; no separate sensitivity diagram.
 f.line(0,93,24,93,'blue',3);f.circle(12,93,3,'blue');f.text(32,99,'宽词表：AI / 机器学习',15,'muted')
 f.line(0,121,24,121,'china',3);f.rect(8,117,8,8,'china');f.text(32,127,'窄词表：去除泛化词',15,'muted')
 f.rect(0,142,24,12,'#E1EAF5');f.text(32,155,'浅色带：宽词表 95% 区间',15,'muted')
 xx=[39+i*65 for i in range(5)];bottom=670;top=205;yy=lambda v:bottom-v/30*(bottom-top)
 for v in [0,5,10,15,20,25,30]:
  y=yy(v);f.line(36,y,306,y,'line',.8);f.text(25,y+5,v,15,'muted',anchor='end')
 lo=[(xx[i],yy(OVER[y]['ci_low'])) for i,y in enumerate(range(2021,2026))];hi=[(xx[i],yy(OVER[y]['ci_high'])) for i,y in enumerate(range(2021,2026))]
 f.path(lo+list(reversed(hi)),'none',0,'#E1EAF5')
 for key,col in [('ai_mention','blue'),('ai_specific','china')]:
  pts=[(xx[i],yy(SENS[y][key])) for i,y in enumerate(range(2021,2026))];f.path(pts,col,3)
  for x,y in pts:
   if key=='ai_mention':f.circle(x,y,4.5,col)
   else:f.rect(x-4,y-4,8,8,col)
 for i,y in enumerate(range(2021,2026)):
  v=OVER[y]['pct'];f.text(xx[i]+(3 if i==0 else 0),yy(v)-16,f'{v:.1f}',17,'blue',True,'start' if i==0 else 'middle');f.text(xx[i],700,y,15,'muted',anchor='middle')
 f.text(291,yy(SENS[2025]['ai_specific'])+24,'22.8',16,'china',True,'end');circle_tag(f,318,yy(SENS[2025]['ai_specific'])+19,3,'china')
 f.text(0,746,'6.1% → 24.2%',28,'blue',True);f.text(0,780,'宽词表：相差 18.1 个百分点',17,'muted')
 f.line(340,0,340,800)
 # Full sector bars, uncertainty whiskers and shared reference line.
 f.text(370,96,'行业',16,'muted');f.text(932,96,'占比',16,'muted',anchor='end');f.text(999,96,'n',16,'muted',anchor='end')
 sx=523;ex=844;tx=lambda v:sx+v/60*(ex-sx)
 for tick in [0,10,20,30,40,50,60]:
  f.line(tx(tick),112,tx(tick),705,'line',.8);f.text(tx(tick),730,tick,15,'muted',anchor='middle')
 f.line(tx(OVER[2025]['pct']),110,tx(OVER[2025]['pct']),705,'china',2,'6,5')
 for i,(c,d) in enumerate(sorted(AI.items(),key=lambda z:z[1]['pct'],reverse=True)):
  y=126+i*31;col='#A79756' if d['count']<100 else 'blue'
  f.text(370,y+6,CN[c]+('＊' if c=='54' else ''),16,'ink',c in ['54','52','31-33','62','22'])
  f.rect(sx,y-10,tx(d['pct'])-sx,20,col,.85)
  xa=tx(d['ci_low']);xb=tx(d['ci_high']);f.line(xa,y,xb,y,'muted',1.4);f.line(xa,y-4,xa,y+4,'muted',1.2);f.line(xb,y-4,xb,y+4,'muted',1.2)
  f.text(932,y+6,f"{d['pct']:.1f}",17,'ink',c in ['54','52','31-33','62','22'],'end');f.text(999,y+6,int(d['count']),16,'muted',anchor='end')
  if c=='31-33':circle_tag(f,355,y,4)
 f.line(370,755,395,755,'china',2,'6,5');f.text(404,761,'全样本 24.2%',16,'muted')
 f.rect(571,746,16,16,'#A79756');f.text(596,761,'n < 100；小样本',16,'muted')
 f.text(370,792,'横线为 95% 区间；＊专业科技分类可靠性较弱。',16,'muted')
 f.save('fig-2-8-2')
 return dict(title='2.8 AI 提及：总体分化与行业落差',intro='行业格局较为稳定，AI 相关表述却在不同创建群体和行业间呈现明显差异。这里的“AI 提及”指简介、标签和说明文本出现相关术语，是技术表述信号，不能直接等同于实际采用率。',figure='fig-2-8-2',caption='图 2.8-2  AI 提及的创建群体差异、词表对照及行业比较。来源：团队配套统计表；区间为 Wilson 95% 区间，仅反映抽样波动。右图按比例排序，行业数量与分类可靠性需一并考虑。',analyses=[
 ('① 较新仓库中的 AI 表述更普遍','宽词表下，2021 创建组为 6.1%，2025 创建组为 24.2%，相差 18.1 个百分点，约为前者的四倍。这是同一快照中的群体差异，反映技术表述变化，尚不能定位实际采用时间。'),
 ('② 行业落差大于总体平均所示','金融与保险为 40.1%，公用事业为 8.1%，相差约 32 个百分点。专业科技服务达到 47.3%，但分类误差较大；建筑、行政支持等小样本行业的高比例也应谨慎解读。'),
 ('③ 收窄词表，主要信号依然存在','窄词表去除泛化机器学习用语后，2025 创建组仍达到 22.8%，与宽词表相差约 1.4 个百分点。较新创建组的高提及比例，不完全由宽泛术语造成，但仍需实际功能与部署证据。'),
 ('④ AI 信号并不局限于信息行业','制造、医疗与社会援助分别为 29.1%、28.9%，均高于全样本 24.2%；信息业为 22.7%。这为后续行业案例提供线索：应结合任务、数据与运行条件，核查技术表述如何转化为应用。')])

def treemap(items,x,y,w,h):
 if len(items)==1:return [(items[0][0],x,y,w,h)]
 total=sum(v for c,v in items);k=min(range(1,len(items)),key=lambda i:abs(sum(v for c,v in items[:i])-total/2));a=items[:k];b=items[k:];ratio=sum(v for c,v in a)/total
 if w>=h:return treemap(a,x,y,w*ratio,h)+treemap(b,x+w*ratio,y,w*(1-ratio),h)
 return treemap(a,x,y,w,h*ratio)+treemap(b,x,y+h*ratio,w,h*(1-ratio))
def heatcol(v):
 a=(243,247,249);b=(21,95,168);t=max(0,min(v/50,1));return '#'+''.join(f'{round(a[i]+(b[i]-a[i])*t):02x}' for i in range(3))

def p3():
 f=Figure();f.title(0,27,1,'AI 相关仓库集中在哪里',fs=21);f.title(624,27,2,'两种行业份额的差距',fs=21)
 f.text(0,61,'2025 创建组 · 836 个 AI 提及仓库 · 面积表示数量',16,'muted')
 f.text(624,60,'AI 提及仓库中的份额，',16,'muted');f.text(624,84,'减去全部仓库中的份额 / 百分点',16,'muted')
 top=['54','51','52','61','62','31-33','71','11'];items=[(c,int(AI[c]['sum'])) for c in top];items.append(('others',836-sum(n for c,n in items)));items.sort(key=lambda a:a[1],reverse=True)
 short={'54':'专业科技服务＊','51':'信息业','52':'金融与保险','61':'教育服务','62':'医疗援助','31-33':'制造业','71':'文娱休闲','11':'农林渔猎','others':'其余 11 行业'}
 left=[(c,int(AI[c]['sum'])) for c in ['54','51','52']]; lw=580*435/836; rects=[];cy=93
 for c,n in left:
  hh=347*n/435;rects.append((c,0,cy,lw,hh));cy+=hh
 rects+=treemap([(c,n) for c,n in items if c not in ['54','51','52']],lw,93,580-lw,347);audit=[]
 for c,x,y,w,h in rects:
  n=dict(items)[c];f.rect(x,y,w,h,COL[c]);f.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="white" stroke-width="3"/>')
  color='ink' if c=='others' else 'white';fs=18 if w>150 else 15
  name=short[c]
  while tw(name,fs,True)>w-22 and fs>13:fs-=1
  f.text(x+11,y+26,name,fs,color,True)
  if h<85:
   num=f'{n} · {n/836*100:.1f}%'; nfs=17
   while tw(num,nfs,True)>w-20:nfs-=.5
   f.text(x+11,y+53,num,nfs,color,True)
  else:
   f.text(x+11,y+58,str(n),27,color,True);f.text(x+11,y+82,f'{n/836*100:.1f}%',17,color)
  audit.append({'code':c,'count':n,'x':x,'y':y,'w':w,'h':h,'area_share':w*h/(580*347)})
 (D/'treemap-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
 zx=832;scale=10
 for i,c in enumerate(['54','52','62','51','61','71','22']):
  y=126+i*45;d=100*AI[c]['sum']/836-100*AI[c]['count']/3461;f.text(624,y+5,CN[c],16,'ink',c in ['54','52','22']);f.rect(zx+min(d,0)*scale,y-10,abs(d)*scale,19,'teal' if d>0 else 'soft');f.text(999,y+5,f'{d:+.1f}',18,'ink',True,'end')
 f.line(zx,107,zx,417,'muted',1)
 for v in [-6,0,12]:f.text(zx+v*scale,440,f'{v:+d}' if v else '0',15,'muted',anchor='middle')
 f.line(0,462,1000,462)
 f.title(0,498,3,'六个行业：不同创建群体中的 AI 提及比例',fs=21);f.title(798,498,4,'两端差值',fs=21)
 f.text(798,527,'2025 减 2021 / 百分点',15,'muted')
 hx=170;hw=112;rh=39;ystart=556;order=['54','52','51','31-33','62','22']
 for i,y in enumerate(range(2021,2026)):f.text(hx+(i+.5)*hw,540,y,17,'ink',True,'middle')
 for i,c in enumerate(order):
  yy=ystart+i*rh;f.text(0,yy+25,CN[c]+('＊' if c=='54' else ''),17,'ink',True)
  for j,v in enumerate(TREND[c]):
   x=hx+j*hw;f.rect(x+1,yy+1,hw-2,rh-2,heatcol(v));f.text(x+hw/2,yy+26,f'{v:.1f}%',18,'white' if v>=30 else 'ink',True,'middle')
  d=TREND[c][-1]-TREND[c][0];f.rect(800,yy+10,d/40*128,19,'teal');f.text(999,yy+26,f'+{d:.1f}',18,'teal',True,'end')
 f.text(0,530,'颜色越深，提及率越高',15,'muted')
 f.save('fig-2-8-3')
 return dict(title='2.8 行业结构与 AI 集中度的错位',intro='行业规模、AI 提及比例与 AI 相关仓库数量，是三个不同的问题。将它们放在一起，才能看见哪些领域集中了更多技术表述，以及哪些行业需要进一步核查应用与复用条件。',figure='fig-2-8-3',caption='图 2.8-3  AI 相关仓库的行业构成、份额差及创建群体差异。来源：团队汇总表与论文图 3，重绘方法见附录 1。面积与份额以 836 个 AI 提及仓库为分母；＊专业科技分类待复核。',analyses=[
 ('① 三个行业集中了过半 AI 仓库','专业科技、信息、金融合计 435 个 AI 提及仓库，占 52.0%；三者占全部仓库的份额为 36.9%。AI 表述具有比仓库分布更强的行业集中性，值得进一步追踪其共享工具与知识资源。'),
 ('② 规模优势与 AI 集中度并不一致','信息业仓库最多，但 AI 提及数量为 137 个，低于专业科技服务的 186 个。专业科技、金融的 AI 仓库份额分别比自身仓库份额高 10.9、5.3 个百分点；观察需求应结合规模和结构。'),
 ('③ 行业群体差异并非单向递增','制造、医疗在 2023 创建组的比例约为 23.7%、23.5%，高于 2024 组的 15.4%、14.7%，2025 组又较高。群体构成和文本更新均可能产生这种差异，不能直接视为应用曾经退潮。'),
 ('④ 把差异转化为能力建设的问题','两端提及率差距从公用事业的 3.4 个百分点，到专业科技的 38.5 个百分点不等。公共投入宜据行业任务，核查数据、成本、本地化与维护条件；以可复用能力和实际结果检验普惠价值。')])

def render():return [p1(),p2(),p3()]
