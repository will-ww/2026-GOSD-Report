"""Original publication-grade vector figures for chapter 1.
All labels/data are editorial/conceptual, not fabricated empirical observations.
Outputs embedded-font PDF and editable SVG/PNG for review.
"""
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle, PathPatch
from matplotlib.path import Path as MPath
from matplotlib import font_manager as fm
OUT=Path(__file__).parent/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','font.size':10,'font.family':'DejaVu Sans'})
# Font files are never bundled. Set up a system Noto CJK font to redraw.
SC_REG=Path('/tmp/GOSD-NotoSansSC-Regular.otf')
SC_BOLD=Path('/tmp/GOSD-NotoSansSC-Bold.otf')
SYS_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SYS_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT=fm.FontProperties(fname=str(SC_REG if SC_REG.exists() else SYS_REG))
BOLD=fm.FontProperties(fname=str(SC_BOLD if SC_BOLD.exists() else SYS_BOLD))
C={'navy':'#193C4E','teal':'#168A8D','green':'#497D6E','purple':'#76698F','mid':'#55717C','ink':'#183642','rule':'#D8E5E7','paper':'#FFFFFF','pale':'#EFF6F6','soft':'#F8FBFB','aqua':'#D9EEEE','sky':'#ECF3F7','moss':'#EFF6F1','violet':'#F6F4F9','amber':'#BF8E58','sand':'#F9F4EB'}
def page(w,h):
 f=plt.figure(figsize=(w/25.4,h/25.4),facecolor='white');a=f.add_axes([0,0,1,1]);a.set_xlim(0,w);a.set_ylim(0,h);a.set_aspect('equal');a.axis('off');return f,a
def text(a,x,y,s,size=10,color='ink',bold=False,ha='left',va='center',**kw):
 return a.text(x,y,s,fontsize=size,fontproperties=BOLD if bold else FONT,color=C.get(color,color),ha=ha,va=va,**kw)
def box(a,x,y,w,h,r=3,fill='white',edge='rule',lw=.8):
 o=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={r}',lw=lw,edgecolor=C.get(edge,edge) if edge else 'none',facecolor=C.get(fill,fill) if fill else 'none');a.add_patch(o);return o
def path(a,points,color='teal',lw=1.0,style='-'):
 a.plot(*zip(*points),color=C.get(color,color),lw=lw,linestyle=style,solid_capstyle='round')
def arrow(a,a1,a2,color='teal',lw=1.2,style='-|>'):
 a.add_patch(FancyArrowPatch(a1,a2,arrowstyle=style,mutation_scale=10,lw=lw,color=C.get(color,color),shrinkA=0,shrinkB=0))
def make(f,name):
 f.savefig(OUT/f'{name}.pdf',facecolor='white',pad_inches=0)
 f.savefig(OUT/f'{name}.svg',facecolor='white',pad_inches=0)
 f.savefig(OUT/f'{name}.png',facecolor='white',pad_inches=0,dpi=210)
 plt.close(f)
def head(a,w,kicker,title):
 box(a,5,89,w-10,0.6,r=.1,fill='rule',edge=None,lw=0)
 box(a,5,94,25,5.5,r=1.1,fill='navy',edge=None,lw=0);text(a,17.5,96.8,kicker,8,'white',bold=True,ha='center')
 text(a,34,97,title,12.5,'navy',bold=True)

# FIG A: from software to AI / object and responsibility layers
f,a=page(171,104)
box(a,5,97,25,5,r=1.3,fill='navy',edge=None,lw=0);text(a,17.5,99.5,'SHIFT',8,'white',True,ha='center')
text(a,35,99.5,'开放对象在扩展，承担责任的参与者也在增加',13.6,'navy',True)
path(a,[(5,94),(166,94)],'rule',.9)
box(a,5,29,52,59,r=3,fill='soft',edge='rule')
box(a,63,29,103,59,r=3,fill='pale',edge='rule')
box(a,10,76,21,6,r=1.5,fill='sky',edge=None,lw=0);text(a,20.5,79,'软件协作',8.7,'navy',True,ha='center')
text(a,10,66,'代码与持续维护',14.0,'navy',True)
text(a,10,56,'公开、审阅、修改、再分发',8.9,'mid')
path(a,[(15,44),(31,44),(43,44)],'teal',1.4);path(a,[(31,44),(31,35),(44,35)],'teal',1.1)
for xx,yy in [(15,44),(31,44),(43,44),(31,35),(44,35)]:a.add_patch(Circle((xx,yy),2.3,color=C['teal']))
arrow(a,(57,58),(63,58),'teal',1.8)
box(a,69,76,28,6,r=1.5,fill='navy',edge=None,lw=0);text(a,83,79,'智能开放',8.9,'white',True,ha='center')
text(a,69,67,'可组合的开放资源',13.4,'navy',True)
for i,(lab,col) in enumerate([('代码','teal'),('模型','navy'),('数据','green'),('工具','purple')]):
 x=69+i*23.5;box(a,x,53,19.5,9,r=2.1,fill='white',edge='rule')
 box(a,x,53,2,9,r=.3,fill=col,edge=None,lw=0);text(a,x+11.1,57.3,lab,10.5,'navy',True,ha='center')
text(a,69,43.5,'从发布到使用，需要更多角色持续协作',10.1,'mid')
steps=['适配','测试','审阅','维护']
for i,s in enumerate(steps):
 x=69+i*23.5; box(a,x,32,19.5,8,r=2,fill='white',edge='rule');text(a,x+9.8,35.8,s,9.9,'ink',True,ha='center')
 if i<3:arrow(a,(x+19.5,36),(x+23.2,36),'teal',.8)
box(a,5,8,161,16,r=2.5,fill='sky',edge=None,lw=0)
text(a,11,18,'关键辨析',8.9,'navy',True)
text(a,11,12.6,'开放软件、模型权重、数据与接口的权利边界并不相同；开放范围扩大 ≠ 自主能力已经形成。',9.9,'ink')
make(f,'fig_ai_open_landscape')

# FIG B: gating conditions -> public outcome
f,a=page(171,102)
box(a,5,94,26,5.5,r=1.3,fill='navy',edge=None,lw=0);text(a,18,96.7,'CAPACITY',7.8,'white',True,ha='center')
text(a,36,96.7,'开放资源转化为公共能力，需要跨越的四道关口',13.2,'navy',True)
path(a,[(5,90),(166,90)],'rule',.8)
items=[('01','可获得','代码 / 模型 / 数据','有没有真实可取用的资源？','teal','pale'),('02','可复用','权利 / 成本 / 兼容','在当地能否合法、负担得起？','navy','sky'),('03','可维护','人才 / 组织 / 责任','谁负责持续运行与改进？','purple','violet'),('04','有成效','服务 / 公平 / 韧性','产生了什么可核查的改善？','green','moss')]
for i,(n,ttl,sub,question,col,fill) in enumerate(items):
 x=5+i*41.7
 box(a,x,25,35.6,52,r=2.6,fill=fill,edge='rule',lw=.8)
 box(a,x+4,66,10,7.2,r=1.6,fill=col,edge=None,lw=0);text(a,x+9,69.7,n,9.3,'white',True,ha='center')
 text(a,x+4,59,ttl,16,'navy',True)
 text(a,x+4,49.5,sub,9.6,'mid')
 path(a,[(x+4,44.8),(x+31.6,44.8)],'rule',.7)
 text(a,x+4,37.5,question[:9],9.0,'ink')
 text(a,x+4,31.4,question[9:],9.0,'ink')
 if i<3:arrow(a,(x+35.6,49),(x+41.3,49),'teal',1.25)
box(a,5,9,161,10,r=2,fill='white',edge='rule')
text(a,10,14,'重要区别',9.6,'navy',True)
text(a,34,14,'前面三步是需要检查的实施条件；最后一步必须由实际使用与结果证据来回答。',9.6,'ink')
make(f,'fig_capacity_gates')

# FIG C: OSDI Goal -> Dimension -> Measures + supporting classification
f,a=page(171,111)
box(a,5,103,26,5.5,r=1.4,fill='navy',edge=None,lw=0);text(a,18,106,'OSDI',9,'white',True,ha='center')
text(a,36,106,'从发展愿景到可核对的观察信号',13.6,'navy',True)
path(a,[(5,99),(166,99)],'rule',.9)
labels=[('01','发展目标','X1—X4','回答：希望走向哪里？','navy','sky'),('02','观察维度','10 个方向','回答：从哪些方面判断？','teal','pale'),('03','候选指标','29 项','回答：哪些数据能够核实？','purple','violet')]
for i,(idx,ttl,sub,ex,col,tint) in enumerate(labels):
 x=5+i*54
 box(a,x,42,49.5,47,r=2.6,fill=tint,edge='rule')
 box(a,x+4,78,9,7,r=1.5,fill=col,edge=None,lw=0);text(a,x+8.5,81.5,idx,9.1,'white',True,ha='center')
 text(a,x+4,70,ttl,15.4,'navy',True)
 text(a,x+4,59.7,sub,11.5,col,True)
 text(a,x+4,48.8,ex,8.8,'mid')
 if i<2:arrow(a,(x+49.5,65),(x+53.6,65),'teal',.95)
text(a,5,32.6,'同一项指标可承担不同用途，类型不代表证据等级',9.5,'mid')
for i,(word,detail,col,tint) in enumerate([('北极星','长期方向','navy','sky'),('诊断','识别差异','teal','pale'),('驱动','观察动力','green','moss')]):
 x=5+i*54
 box(a,x,11,49.5,17,r=2.4,fill=tint,edge='rule')
 box(a,x+3.7,15,12.8,9,r=1.6,fill=col,edge=None,lw=0);text(a,x+10,19.5,word,8.5,'white',True,ha='center')
 text(a,x+19,20,detail,9.8,'ink',True)
make(f,'fig_osdi_logic')
print('Completed vector images')
