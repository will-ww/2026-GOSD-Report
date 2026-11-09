"""Precise editorial diagrams; brand assets and dimension identities stay unchanged."""
from pathlib import Path
import json

R = Path(__file__).resolve().parent
F = R / 'figures'
B = json.loads((R.parents[4] / 'brand/osdgs/v2.0/source/brand_tokens.json').read_text())

def text(x,y,w,t,size=9.5,leading=14,color='ink',bold=False):
    weight = r'\bfseries' if bold else ''
    return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{\sffamily{weight}\fontsize{{{size}}}{{{leading}}}\selectfont\color{{{color}}}{t}}}'+'\n'
def rect(x,y,w,h,c): return rf'\Rect{{{x}}}{{{y}}}{{{w}}}{{{h}}}{{{c}}}'+'\n'
def rule(x,y,z,c='line'): return rf'\Rule{{{x}}}{{{y}}}{{{z}}}{{{c}}}'+'\n'
def arrow(x,y,a,b,c='muted'):return rf'\LinkLine{{{x}}}{{{y}}}{{{a}}}{{{b}}}{{{c}}}'+'\n'
def icon(x,y,w,name):return text(x,y,w,rf'\includegraphics[width={w}mm]{{.build/assets/{name}.pdf}}')

# 1-3: all 17 SDGs and nine DPG requirements, without implying a 1:1 mapping.
sdgs=['无贫穷','零饥饿','良好健康与福祉','优质教育','性别平等','清洁饮水和卫生设施','经济适用的清洁能源','体面工作和经济增长','产业、创新和基础设施','减少不平等','可持续城市和社区','负责任消费和生产','气候行动','水下生物','陆地生物','和平、正义与强大机构','促进目标实现的伙伴关系']
colors=['E5243B','DDA63A','4C9F38','C5192D','FF3A21','26BDE2','FCC30B','A21942','FD6925','DD1367','FD9D24','BF8B2E','3F7E44','0A97D9','56C02B','00689D','19486A']
s=text(22,102,76,'SDGs｜希望改善什么？',11,16,'blue',True)
s+=text(106,102,82,'DPG 标准｜方案具备什么条件？',10.7,16,'teal',True)
s+=text(22,112,76,'17 项共同发展目标',8.8,13,'muted')
s+=text(106,112,82,'9 项基础要求；由 DPGA 维护',8.8,13,'muted')
for i,(name,c) in enumerate(zip(sdgs,colors)):
    col=0 if i<9 else 1; row=i if i<9 else i-9
    x=22+col*41;y=125+row*11.6
    s+=rf'\definecolor{{sdg{i+1}}}{{HTML}}{{{c}}}'+'\n'
    s+=rect(x,y+.8,1.1,7,f'sdg{i+1}')
    s+=text(x+3,y,6,f'{i+1:02}',8.5,12,'muted',True)
    s+=text(x+10,y,29,name,8.6,12,'navy')
dpg=[('SDG 相关性','说明所支持的\n发展目标'),('开放许可','允许他人\n合法复用'),('清晰权属','说明成果的\n权利归属'),('平台独立性','减少对封闭\n平台的依赖'),('文档','提供理解与\n使用资料'),('数据提取机制','可提取非个人\n身份识别数据'),('隐私与法律','遵守隐私及\n适用法律'),('标准与实践','遵循相关标准\n和最佳实践'),('不造成伤害','数据安全、内容\n及反骚扰保护')]
for i,(title,desc) in enumerate(dpg):
    x=106+(i%3)*28;y=124+(i//3)*35
    s+=rect(x,y,26,32,'teal!4')+rect(x,y,.7,32,'teal!50')
    s+=text(x+2,y+2,22,f'{i+1:02}',8,11,'teal',True)
    s+=text(x+2,y+9,22,title,8.7,12,'navy',True)
    s+=text(x+2,y+20,22,desc.replace('\n',r'\\'),8,11,'muted')
s+=rule(22,232,188)
for x,w,title,desc,c in [(22,51,'发展方向','SDGs：希望改变什么','blue'),(80,51,'设计与开放条件','DPG 标准：能否作为公共资源','teal'),(138,50,'本地实施结果','成本、质量、公平与持续性','gold')]:
    s+=text(x,238,w,title,10,14,c,True)+text(x,247,w,desc,8.3,12,'muted')
s+=arrow(73,242,78,242,'line')+arrow(131,242,136,242,'line')
(F/'sdgs-dpg.tex').write_text(s)

# 1-4: the approved signature emblem plus the complete four-by-ten framework.
s=icon(24,95,47,'osdgs-display')
s+=text(84,97,104,'开源发展目标',17,22,'navy',True)
s+=text(84,109,104,'Open Source Development Goals',9.4,14,'muted')
s+=text(84,121,104,'4 项发展目标 · 10 个观察维度',12,17,'teal',True)
s+=text(84,132,104,'让开放创新的规模、结构与公共价值进入同一视野。',9.5,14)
qs=['谁能参与，并持续成长？','什么资源能够被继续使用？','成果如何跨越边界继续生长？','谁来维护，如何形成共同受益？']
cs=['blue','teal','gold','violet']
for i,p in enumerate(B['pillars']):
    y=148+i*27.8;c=cs[i]
    s+=rule(22,y,188)
    s+=text(22,y+3,10,p['id'],10.5,15,c,True)
    s+=text(36,y+3,82,p['name_zh'],10.7,15,c,True)
    s+=text(118,y+3,70,qs[i],9.2,14,'ink')
    for j,did in enumerate(p['dimensions']):
        d=next(d for d in B['dimensions'] if d['id']==did);x=36+j*51
        s+=icon(x,y+14,4.8,did)
        s+=text(x+7,y+14,44,f"{did} {d['name_zh']}",8.8,13,c)
(F/'goals.tex').write_text(s)

# 1-6: OSDI visual signature is editorial typography, not a replacement brand mark.
s=rect(22,101,166,41,'navy')
s+=text(27,105,42,'OSDI',28,32,'white',True)
s+=text(77,106,105,'开源发展指标体系',14,19,'white',True)
s+=text(77,117,105,'Open Source Development Indicators',8.8,13,'white')
s+=text(27,130,154,'科学性：对应问题　　可操作性：定义可核　　前瞻性：覆盖新型资产与复用',8.6,12,'white')
for x,n,title,c in [(22,'4','发展目标','blue'),(81,'10','观察方向','teal'),(140,'29','候选指标','violet')]:
    s+=text(x,149,21,n,26,30,c,True)+text(x+23,156,28,title,10.2,15,'navy',True)
s+=arrow(72,160,78,160,'line')+arrow(130,160,137,160,'line')
s+=text(22,173,166,'由目标逐层细化；29 项是候选目录，逐项注明数据可得性与核验状态。',8.8,13,'muted')
rows=[('X1 参与机会','规模／多样性','3 + 2 = 5 项','blue'),('X2 开放供给','代码／模型／数据','3 + 2 + 2 = 7 项','teal'),('X3 全球连接','代码／模型／数据影响','5 + 3 + 3 = 11 项','gold'),('X4 公共价值','治理／公共福祉','3 + 3 = 6 项','violet')]
for i,(name,dims,count,c) in enumerate(rows):
    y=186+i*11
    s+=rect(22,y,166,10,c+'!5')+text(26,y+1,43,name,9,13,c,True)+text(70,y+1,69,dims,8.8,13)+text(141,y+1,44,count,8.8,13,c)
s+=text(22,235,166,'同一指标，可以服务三种决策用途',10.5,15,'navy',True)
for x,title,desc,c in [(22,'北极星｜把握方向','长期是否朝目标前进','blue'),(80,'诊断｜识别差异','瓶颈与薄弱环节在哪里','teal'),(138,'驱动｜跟踪变化','哪些过程值得继续观察','gold')]:
    s+=text(x,246,50,title,9.3,14,c,True)+text(x,255,50,desc,8.5,12,'muted')
(F/'osdi.tex').write_text(s)
print('Generated SDGs–DPG, OSDGs and OSDI editorial diagrams.')
