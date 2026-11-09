"""New explanatory and comparison figures for the integrated chapter.
Uses original reviewed CSV values, not reconstructed observations.
"""
from pathlib import Path
import json,math
import numpy as np
import pandas as pd
from graphics import S,C,ALL_QA
R=Path(__file__).resolve().parents[1]
LAYOUT={'黑龙江':(9,0),'新疆':(0,1),'内蒙古':(5,1),'吉林':(9,1),'甘肃':(2,2),'宁夏':(3,2),'山西':(5,2),'河北':(6,2),'北京':(7,2),'辽宁':(8,2),'西藏':(0,3),'青海':(1,3),'四川':(3,3),'陕西':(4,3),'河南':(5,3),'天津':(7,3),'山东':(8,3),'云南':(2,4),'重庆':(3,4),'贵州':(4,4),'湖北':(5,4),'安徽':(6,4),'江苏':(7,4),'广西':(4,5),'湖南':(5,5),'江西':(6,5),'浙江':(7,5),'上海':(8,5),'广东':(5,6),'福建':(7,6),'台湾':(9,6),'海南':(4,7),'澳门':(5,7),'香港':(6,7)}

def atlas():
 d=pd.read_csv(R/'data/21/china_provinces_with_change.csv').set_index('province')
 s=S(159)
 s.title('头部集聚与多地参与，同时进入观察','A  34个省级地区的活跃人数 / 万人 · 方格保留近似方位')
 palette=['#EFF5F5','#CCE1E3','#87B8BE','#3B939C','#1E6276'];bounds=[1,5,15,30]
 for name,(gx,gy) in LAYOUT.items():
  val=float(d.loc[name,'active_10k']);idx=sum(val>=z for z in bounds);fill=palette[idx];fg='white' if idx>=3 else 'ink'
  x=1+gx*16.9;y=17+gy*8.5
  s.rect(x,y,15.8,7.6,fill,'white',.5,lw=.3)
  s.t(x+7.9,y+3.3,name,8.2,fg,True,'middle');s.t(x+7.9,y+6.4,f'{val:.2f}',7.8,fg,False,'middle')
 for i,(col,l) in enumerate(zip(palette,['<1','1—<5','5—<15','15—<30','≥30'])):
  x=1+34*i;s.rect(x,87,5,2.9,col);s.t(x+7,89.6,l,8.3,'muted')
 s.line(1,94,169,94)
 s.t(1,101,'B  活跃人数前10地区',10.4,'ink',True)
 top=d.reset_index().sort_values('active_10k',ascending=False).head(10)
 for i,row in top.reset_index(drop=True).iterrows():
  col=0 if i<5 else 1;j=i%5;x=1+87*col;y=109+7.3*j
  val=float(row.active_10k);s.t(x,y,f'{i+1:02}',8.4,'muted');s.t(x+8,y,row.province,9.0,'ink',i<3)
  s.rect(x+23,y-2.7,43,3.6,'pale',rx=.4);s.rect(x+23,y-2.7,43*val/60,3.6,'blue' if i<3 else 'teal',rx=.4)
  s.t(x+78,y,f'{val:.2f}',9.0,'ink',True,'end')
 vals=[float(d.loc[['北京','上海','广东'],'active_10k'].sum()),float(top.iloc[3:].active_10k.sum())];total=float(d.active_10k.sum());vals.append(total-sum(vals))
 x=1
 for name,val,col in zip(['京沪粤','第4—10位','其余24地'],vals,['blue','teal','purple']):
  w=168*val/total;s.rect(x,146,w,4.2,col,'white',lw=.25);s.t(169 if name=='其余24地' else x+w/2,156,f'{name} {100*val/total:.1f}%',8.6,'ink',False,'end' if name=='其余24地' else 'middle');x+=w
 s.save(R/'figures/21/china_atlas')

def growth_mix():
 d=pd.read_csv(R/'data/21/china_provinces_with_change.csv').set_index('province')
 groups=[('京沪粤',['北京','上海','广东']),('台湾与浙江',['台湾','浙江']),('江苏、四川与湖北',['江苏','四川','湖北'])];used=sum([a for _,a in groups],[]);groups.append(('其他26地',[x for x in d.index if x not in used]))
 s=S(151);s.title('总量份额相近，增量结构仍有差异','A  规模份额与净增份额对照 · 各自以全国合计为100%')
 s.rect(1,18,5,2.8,'blue');s.t(8,20.5,'当前活跃份额',8.8,'muted');s.rect(49,18,5,2.8,'teal');s.t(56,20.5,'净增量份额',8.8,'muted');s.t(156,20.5,'差额 / 百分点',8.5,'muted',False,'middle')
 for i,(name,members) in enumerate(groups):
  y=32+i*14;stock=d.loc[members,'active_10k'].sum()/d.active_10k.sum()*100;inc=d.loc[members,'increase_10k'].sum()/d.increase_10k.sum()*100
  s.t(1,y+1,name,9.0,'ink',i==1)
  for val,off,col in [(stock,-4,'blue'),(inc,1,'teal')]:
   s.rect(40,y+off,78,3.2,'pale',rx=.4);s.rect(40,y+off,78*val/60,3.2,col,rx=.4);s.t(132,y+off+2.8,f'{val:.1f}%',9.1,col,True,'end')
  s.t(157,y+1.8,f'{inc-stock:+.1f}',11.2,'teal' if inc>stock else 'muted',True,'middle')
 s.line(40,84,118,84)
 for v in [0,20,40,60]:s.t(40+v/60*78,89,f'{v}%',8,'muted',False,'middle')
 s.line(1,94,169,94);s.t(1,101,'B  活跃人数净增前10地区',10.2,'ink',True);s.t(169,101,'2026较2025 / 万人',8.6,'muted',False,'end')
 top=d.reset_index().sort_values('increase_10k',ascending=False).head(10).reset_index(drop=True)
 for i,row in top.iterrows():
  col=0 if i<5 else 1;j=i%5;x=1+87*col;y=109+7.3*j;val=row.increase_10k
  s.t(x,y,f'{i+1:02}',8.4,'muted');s.t(x+8,y,row.province,9,'ink',i<3)
  s.rect(x+23,y-2.8,43,3.6,'pale',rx=.4);s.rect(x+23,y-2.8,43*val/7,3.6,'teal',rx=.4);s.t(x+78,y,f'{val:.2f}',9,'ink',True,'end')
 s.t(1,149,'净增是两期人数之差，不是新增注册或首次参与人数。',8.6,'muted')
 s.save(R/'figures/21/china_growth_mix')

def project_evolution():
 d=pd.read_csv(R/'data/23/raw/five_groups_influence.csv');print(d.columns.tolist())
 years=d.iloc[:,0].tolist();groups=list(d.columns[1:]);zh={'United States':'美国','China':'中国','Europe':'欧洲','Global South representatives':'南方六国代表组','India':'印度'}
 colors={'United States':'blue','China':'mint','Europe':'teal','India':'gold','Global South representatives':'purple'}
 s=S(145);s.title('当前规模与相对扩张，采用不同但互补的尺度','上栏保留2026读数；下栏统一2022＝100，比较各组增长路径')
 # Five equal columns, large explicit numbers ensure the indexing does not hide scale.
 for i,g in enumerate(groups):
  x=1+34*i;v=float(d[g].iloc[-1]);s.rect(x,18,32,24,'pale',rx=1)
  s.t(x+16,25,zh[g],8.7,colors[g],True,'middle');s.t(x+16,33,f'{v/10000:,.2f}',13,colors[g],True,'middle');s.t(x+16,39,'万OpenRank',7.8,'muted',False,'middle')
 # Common-scale line chart with direct endpoint label rail
 x0=14;x1=124;y0=121;ytop=51;vmin=100;vmax=280
 for v in [100,150,200,250]:
  yy=y0-(v-vmin)/(vmax-vmin)*(y0-ytop);s.line(x0,yy,x1,yy,'line',.2);s.t(x0-3,yy+1,f'{v}',8.3,'muted',False,'end')
 ends=[]
 for g in groups:
  a=np.array(d[g],float);vv=a/a[0]*100;pts=[]
  for j,v in enumerate(vv):
   x=x0+(x1-x0)*j/(len(years)-1);y=y0-(v-vmin)/(vmax-vmin)*(y0-ytop);pts.append((x,y))
  s.path('M'+' L'.join(f'{x:.3f},{y:.3f}' for x,y in pts),'none',colors[g],.65)
  for x,y in pts:s.circle(x,y,.8,colors[g],colors[g],.15)
  ends.append([g,pts[-1][1],vv[-1]])
 # Direct labels spaced to prevent endpoint collisions.
 ends.sort(key=lambda r:r[1]);ys=[]
 for g,y,v in ends:
  yy=max(y,ys[-1]+8.4) if ys else y;ys.append(yy)
 for (g,y,v),yy in zip(ends,ys):
  s.path(f'M124,{y:.2f} L129,{y:.2f} L132,{yy:.2f}','none',colors[g],.3)
  s.t(135,yy+1.0,zh[g],8.9,colors[g],True);s.t(169,yy+1.0,f'{v:.0f}',8.8,colors[g],True,'end')
 for j,year in enumerate(years):s.t(x0+(x1-x0)*j/(len(years)-1),128,str(year),8.5,'muted',False,'middle')
 s.t(1,138,'100表示2022年规模；200表示规模翻倍。指数相近，不表示得分总量接近。',8.5,'muted')
 s.save(R/'figures/23/five_evolution')

if __name__=='__main__':
 atlas();growth_mix();project_evolution()
 (R/'review/new_figure_geometry.json').write_text(json.dumps(ALL_QA,ensure_ascii=False,indent=2))
