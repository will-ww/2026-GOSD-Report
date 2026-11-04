"""Original vector reconstruction of SDGs x DPGA standard overview for GOSD ch1.
SDG names and ring colors follow UN's 17 SDGs; DPG criteria follow DPGA's nine indicators.
Conceptual two-column juxtaposition, not a one-to-one mapping or certification.
No image assets or third-party graphics copied; text-based summary plus vector arcs/cards.
"""
from pathlib import Path
from matplotlib.patches import Wedge, Circle, FancyBboxPatch, Rectangle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

OUT=Path(__file__).parent/'figures'; OUT.mkdir(exist_ok=True)
FONT = fm.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
BOLD = fm.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
W,H=171,142
fig=plt.figure(figsize=(W/25.4,H/25.4),facecolor='white'); ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,W);ax.set_ylim(0,H);ax.axis('off');ax.set_aspect('equal')
INK='#203945'; NAVY='#193E51'; TEAL='#167C8B'; RULE='#D7E3E6'; PALE='#F3F8F8'; MUTED='#617B87'; LIGHT='#ECF4F7'

def txt(x,y,s,size=9.5,color=INK,bold=False,ha='left',va='center'):
    return ax.text(x,y,s,fontproperties=BOLD if bold else FONT,fontsize=size,color=color,ha=ha,va=va)
def line(a,b,color=RULE,lw=.8):ax.plot([a[0],b[0]],[a[1],b[1]],color=color,linewidth=lw)
def rect(x,y,w,h,fc='white',ec=RULE,r=2.4):
    o=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={r}',linewidth=.72,edgecolor=ec,facecolor=fc);ax.add_patch(o);return o

rect(4,134,24,5.5,fc=NAVY,ec='none',r=1.2)
txt(16,136.8,'GLOBAL GOALS',7.3,color='white',bold=True,ha='center')
txt(34,136.8,'共同的发展目标 · 可核查的开放条件',12.2,NAVY,True)
line((4,131.7),(167,131.7))
rect(5,123.5,4,2.8,fc=TEAL,ec='none',r=0.3)
txt(12,125,'联合国 SDGs  ·  17项目标',10.6,NAVY,True)
rect(85,123.5,4,2.8,fc=TEAL,ec='none',r=0.3)
txt(92,125,'数字公共品联盟  ·  9项标准条件',10.6,NAVY,True)

colors=['#E5243B','#DDA63A','#4C9F38','#C5192D','#FF3A21','#26BDE2','#FCC30B','#A21942','#FD6925','#DD1367','#FD9D24','#BF8B2E','#3F7E44','#0A97D9','#56C02B','#00689D','#19486A']
labels=['无贫穷','零饥饿','良好健康与福祉','优质教育','性别平等','清洁饮水和卫生设施','经济适用的清洁能源','体面工作和经济增长','产业、创新和基础设施','减少不平等','可持续城市和社区','负责任消费和生产','气候行动','水下生物','陆地生物','和平、正义与强大机构','促进目标实现的伙伴关系']
center=(42,92.5);rad=28.3;ring=9.2
for i,c in enumerate(colors):
    th1=90-(i+1)*360/17+0.7; th2=90-i*360/17-0.7
    ax.add_patch(Wedge(center,rad,theta1=th1,theta2=th2,width=ring,facecolor=c,edgecolor='white',linewidth=.35))
    import math
    alpha=math.radians((th1+th2)/2); rr=rad-ring/2
    x=center[0]+rr*math.cos(alpha); y=center[1]+rr*math.sin(alpha)
    textcolor='#193E51' if i in [1,2,5,6,10,11,14] else 'white'
    txt(x,y,str(i+1),8.4,textcolor,True,ha='center')
txt(center[0],94.8,'UN SDGs',13,NAVY,True,ha='center')
txt(center[0],88.7,'共同的发展目标',8.3,MUTED,False,ha='center')
for i,(c,label) in enumerate(zip(colors,labels)):
    col=0 if i<9 else 1; row=i if i<9 else i-9
    x=4.5 if col==0 else 44.5
    y=61.4 - row*5.1
    ax.add_patch(Rectangle((x,y-1.8),1.6,3.6,facecolor=c,edgecolor='none'))
    txt(x+3.2,y,f'{i+1:02d}',7.8,MUTED)
    txt(x+11,y,label,7.7,INK)
criteria=[
    ('01','SDG相关性',['说明与可持续','发展目标的联系']),
    ('02','开放许可',['提供允许合法','使用和复用的许可']),
    ('03','权属清晰',['明确数字成果','权属与责任主体']),
    ('04','平台独立性',['说明依赖关系','与开放替代选择']),
    ('05','文档',['提供使用、维护','与再开发资料']),
    ('06','非个人数据提取',['支持非个人数据','以开放格式导出']),
    ('07','隐私与适用法律',['核对隐私保护','及适用法律']),
    ('08','标准与最佳实践',['遵循适用标准','与专业最佳实践']),
    ('09','设计上避免伤害',['考虑隐私、安全、','内容与用户保护']),
]
for i,(num,title,desc) in enumerate(criteria):
    col=i%3;row=i//3; x=86.0+col*27.2;y=91.0-row*31.5
    rect(x,y,25.0,28.5,fc=PALE if row%2==0 else LIGHT,ec='#C5D6DC',r=2.0)
    txt(x+3.2,y+23.2,num,8.8,TEAL,True)
    line((x+3.2,y+19.7),(x+21.8,y+19.7),'#D4E1E5',.6)
    titleSize=8.7 if len(title)<8 else 7.8
    txt(x+12.5,y+15.7,title,titleSize,NAVY,True,ha='center')
    txt(x+12.5,y+9.2,desc[0],7.3,MUTED,ha='center')
    txt(x+12.5,y+5.1,desc[1],7.3,MUTED,ha='center')
line((4,8.1),(167,8.1))
txt(5,14,'读图',8.4,TEAL,True)
txt(17,14,'左侧回答“希望改善什么”，右侧回答“方案应具备哪些条件”；两者不作逐项对应。',8.5,INK)
txt(5,4.2,'DPGA Standard 第九项含隐私安全、内容与反骚扰等子要求；具体适用性依官方标准逐项核对。',7.8,MUTED)
for suffix in ('pdf','svg','png'):
    fp=OUT/f'fig_sdgs_dpga.{suffix}'
    fig.savefig(fp,dpi=220 if suffix=='png' else None,pad_inches=0,facecolor='white')
print('Wrote', [str(OUT/f'fig_sdgs_dpga.{s}') for s in ['pdf','svg','png']])
