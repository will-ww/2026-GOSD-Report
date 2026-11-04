# Original vector figures for the 2026 GOSD report, drawing with matplotlib,
# guided by publication chart practice and explicit semantic layout.
# No third-party diagrams or graphics copied from reference repositories.
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, PathPatch
from matplotlib.path import Path as MPath
from matplotlib import font_manager as fm

OUT=Path(__file__).parent/'figures'
OUT.mkdir(exist_ok=True,parents=True)
matplotlib.rcParams.update({
    'font.family':'DejaVu Sans',
    'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none',
    'font.size':10.2,
})
# Chinese font files are NOT distributed. Prefer local SC font if available,
# otherwise use the system-installed Noto CJK collection.
SC_REG=Path('/tmp/GOSD-NotoSansSC-Regular.otf')
SC_BOLD=Path('/tmp/GOSD-NotoSansSC-Bold.otf')
SYS_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SYS_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SANS=fm.FontProperties(fname=str(SC_REG if SC_REG.exists() else SYS_REG))
BOLD=fm.FontProperties(fname=str(SC_BOLD if SC_BOLD.exists() else SYS_BOLD))
COL={
 'navy':'#193C4E', 'navy2':'#315A6C','teal':'#168A8D','aqua':'#49A1A0',
 'green':'#497D6E','violet':'#76698F','amber':'#B68A57',
 'paper':'#FFFFFF','ink':'#183642','mid':'#55717C','pale':'#EFF6F6',
 'rule':'#D8E5E7','soft':'#F8FBFB','paleblue':'#F1F6F8',
 'palegreen':'#F1F7F4','paleviolet':'#F7F4FA',
}
def fig_setup(w,h):
    f=plt.figure(figsize=(w/25.4,h/25.4),facecolor='white')
    a=f.add_axes([0,0,1,1]);a.set_xlim(0,w);a.set_ylim(0,h);a.set_aspect('equal');a.axis('off')
    return f,a

def txt(a,x,y,t,size=10,color=None,weight='regular',ha='left',va='center',alpha=1,**kw):
    return a.text(x,y,t,fontsize=size,fontproperties=BOLD if weight=='bold' else SANS,
                  color=color or COL['ink'],ha=ha,va=va,alpha=alpha,**kw)

def box(a,x,y,w,h,r=3,edge=None,fill=None,lw=0.7,z=1):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={r}',
            linewidth=lw,edgecolor=edge if edge else 'none',facecolor=fill if fill else 'none',zorder=z)
    a.add_patch(p);return p

def line(a,points,c='rule',lw=.8):
    a.plot([p[0] for p in points],[p[1] for p in points], color=COL.get(c,c),lw=lw,solid_capstyle='round')

def bullet(a,x,y,c):
    a.add_patch(Circle((x,y),1.15,color=c,lw=0))

def save(f,stem):
    f.savefig(OUT/f'{stem}.pdf',bbox_inches=None,pad_inches=0,facecolor='white')
    f.savefig(OUT/f'{stem}.svg',bbox_inches=None,pad_inches=0,facecolor='white')
    f.savefig(OUT/f'{stem}.png',dpi=220,bbox_inches=None,pad_inches=0,facecolor='white')
    plt.close(f)

# 1. FOUR PILLARS -------------------------------------------------------------
f,a=fig_setup(171,121)
# Kicker
box(a,5,111,23,5,1.5,fill=COL['navy']);txt(a,16.5,113.5,'OSDGs',7.9,'white','bold',ha='center')
txt(a,33,114,'OPEN SOURCE DEVELOPMENT GOALS',8.5,COL['mid'])
txt(a,5,103.5,'四种能力，共同决定开放成果能否持续创造价值',15.4,COL['navy'],'bold')
txt(a,166,113.5,'X1—X4 / 10 个观察维度',8.8,COL['mid'],ha='right')
line(a,[(5,97.5),(166,97.5)],'rule',.9)

pillars=[
 ('X1','人才规模与多样性','Talent Scale & Diversity','让更多人能够参与并持续成长','规模与密度','生态多样性',COL['teal'],COL['pale'],(5,51)),
 ('X2','技术产出与开放供给','Tech Output & Open Supply','让关键资源可获得、可使用','代码产出','模型供给  ·  数据供给',COL['navy2'],COL['paleblue'],(88,51)),
 ('X3','全球连接与网络效应','Global Connection & Network Effect','让知识跨边界流动、复用和再创造','代码影响力','模型影响力  ·  数据集影响力',COL['violet'],COL['paleviolet'],(5,6)),
 ('X4','开源善治与公共价值','Governance & Public Value','让合作有保障、效果可核验','治理成熟度','公共福祉',COL['green'],COL['palegreen'],(88,6)),
]
for code,title,en,statement,dim1,dim2,accent,tint,(x,y) in pillars:
    w,h=78,40.5
    box(a,x,y,w,h,r=2.5,fill='white',edge=COL['rule'],lw=.8)
    box(a,x,y,1.5,h,r=.5,fill=accent,lw=0)
    box(a,x+4,y+h-13.2,13,9.8,r=2.1,fill=tint,lw=0)
    txt(a,x+10.5,y+h-8.2,code,14.2,accent,'bold',ha='center')
    txt(a,x+20,y+h-7.2,title,12.1,COL['navy'],'bold')
    txt(a,x+20,y+h-13,en,7.4,COL['mid'])
    txt(a,x+5,y+h-20.1,statement,9.0,COL['mid'])
    line(a,[(x+5,y+15.6),(x+w-4,y+15.6)],'rule',.65)
    # Dimension chips, both lines, semantic bullets
    bullet(a,x+6.2,y+10.9,accent);txt(a,x+10.3,y+11,dim1,9.6,COL['ink'],'bold')
    bullet(a,x+6.2,y+5.8,accent);txt(a,x+10.3,y+5.9,dim2,9.3,COL['ink'])
# small footer phrase rather than callout
# bottom edge belongs in cards; no extra caption.
save(f,'fig_osdgs_pillars')

# 2. BOOK ROADMAP -------------------------------------------------------------
f,a=fig_setup(171,110)
box(a,5,99,22,5.1,1.3,fill=COL['navy']);txt(a,16,101.5,'BOOK MAP',7.9,'white','bold',ha='center')
txt(a,32,101.5,'从共同问题到四种证据，再到有条件的行动',10.4,COL['mid'])
# top primary layer
box(a,5,74,161,19,r=3,fill=COL['navy'],lw=0)
box(a,9,79.2,18,8,r=1.8,fill='#286778',lw=0)
txt(a,18,83.2,'CH 01',9.7,'white','bold',ha='center')
txt(a,33,86,'从开放协作到公共价值',14.4,'white','bold')
txt(a,33,79.2,'1.1 共同创新    /    1.2 发展目标 OSDGs    /    1.3 指标与方法 OSDI',9.2,'#D7E7E9')
# connector rail
line(a,[(85.5,74),(85.5,68.8)],'mid',.9);line(a,[(25.5,68.8),(145.5,68.8)],'rule',1.3)
chapters=[
 ('02','全球开源生态','观测地图','GOSO','规模与结构',COL['teal']),
 ('03','全球开源影响力','排行榜','GOSR','主体与影响',COL['violet']),
 ('04','全球开源技术','全景洞察','GOSL','分类与演进',COL['navy2']),
 ('05','全球开源大模型','发展洞察','GOSM','供给·复用·开放',COL['green']),
]
for i,(idx,name1,name2,code,subtitle,accent) in enumerate(chapters):
    x=5+i*41.7
    w=35.9
    line(a,[(x+w/2,68.8),(x+w/2,64.8)],'rule',1.1)
    box(a,x,29,w,35,r=2.5,fill='white',edge=COL['rule'],lw=.8)
    box(a,x,60.8,w,3.2,r=.1,fill=accent,lw=0)
    txt(a,x+4,54.5,idx,14.0,accent,'bold')
    txt(a,x+4,44.9,name1,10.5,COL['navy'],'bold')
    txt(a,x+4,38.9,name2,10.5,COL['navy'],'bold')
    line(a,[(x+4,35.8),(x+w-4,35.8)],'rule',.55)
    txt(a,x+4,32.1,f'{code}   {subtitle}',8.1,COL['mid'])
# action layer and appendix strip
line(a,[(85.5,29),(85.5,24.4)],'rule',1.2)
box(a,5,8,161,16,r=2.6,fill=COL['pale'],edge=COL['rule'],lw=.7)
box(a,9,12.6,18,7,r=1.4,fill=COL['teal'],lw=0);txt(a,18,16.2,'CH 06',9.4,'white','bold',ha='center')
txt(a,33,18.6,'未来展望与行动建议',12.5,COL['navy'],'bold')
txt(a,33,12.8,'由经验证的发现出发，明确行动主体、约束与后续观察',9.1,COL['mid'])
txt(a,5,4,'附录A  指标、数据与方法       /       附录B  开放条件与数字公共品',8.3,COL['mid'])
save(f,'fig_book_structure')

# 3. 4 PILLARS -> 7 THEME MAPS: an information matrix ---------------------------
f,a=fig_setup(171,137)
box(a,5,125,23,5.1,1.5,fill=COL['navy']);txt(a,16.5,127.5,'RESEARCH MAP',7.5,'white','bold',ha='center')
txt(a,5,118.5,'四大支柱如何连接第二章的七类观测',14.7,COL['navy'],'bold')
txt(a,166,126,'主阅读关系 / 不代表计算权重',8.4,COL['mid'],ha='right')
# column headers and top line
colx=[98,115,132,149]
cols=[('X1','人才',COL['teal']),('X2','供给',COL['navy2']),('X3','连接',COL['violet']),('X4','治理',COL['green'])]
for xc,(code,t,c) in zip(colx,cols):
    box(a,xc-7.5,101,15,11,r=2.3,fill='#F4F8F9',lw=0)
    txt(a,xc,108,code,10.7,c,'bold',ha='center')
    txt(a,xc,103.5,t,7.9,COL['mid'],ha='center')
line(a,[(5,98),(166,98)],'rule',1.1)
rows=[
 ('2.1','V-Map  活跃','参与规模 · 地域分布 · 变化趋势',0),
 ('2.2','C-Map  贡献','贡献来源 · 贡献强度 · 协作关系',1),
 ('2.3','I-Map  项目影响力','影响分布 · 项目结构 · 时间变化',2),
 ('2.4','T-Map  人才','人才聚集 · 成长轨迹 · 全球连接',0),
 ('2.5','A-Map  资产','代码 · 模型 · 数据',1),
 ('2.6','D-Map  多样性','参与结构 · 跨域协作 · 开放连接',2),
 ('2.7','G-Map  治理与社会公益','治理实践 · 开放条件 · 公共价值',3)
]
for i,(n,label,detail,which) in enumerate(rows):
    top=95.5-i*12.0; y=top-10.8
    # subtle alternating stripes for tabular reading
    if i%2==0: box(a,5,y,161,11,r=.5,fill=COL['soft'],lw=0)
    color=cols[which][2]
    box(a,7,y+2,1.6,7,r=.5,fill=color,lw=0)
    txt(a,12,top-4, f'{n}  {label}',10.6,COL['navy'],'bold')
    txt(a,12,top-8.5,detail,7.8,COL['mid'])
    for xc in colx:
        line(a,[(xc-7,top-11),(xc+7,top-11)],'rule',.32)
    a.add_patch(Circle((colx[which],top-5.2),2.5,color=color,lw=0))
    a.add_patch(Circle((colx[which],top-5.2),1.03,color='white',lw=0))
# legend footer
line(a,[(5,9.5),(166,9.5)],'rule',.8)
txt(a,5,5.1,'●  主要阅读与研究联系',8.4,COL['mid'])
txt(a,166,5.1,'其他关联由后文证据具体说明，不作机械一一映射',8.2,COL['mid'],ha='right')
save(f,'fig_pillars_theme_matrix')

print('DONE:',*[str(x) for x in sorted(OUT.glob('*.pdf'))],sep='\n')