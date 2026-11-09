"""2026 declaration visual overview; seven principles in the source's three layers."""
from pathlib import Path
import subprocess
R=Path(__file__).resolve().parent
# Editorial line pictograms, deliberately separate from the OSDGs master mark.
paths=[
 '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6.5h14M5 17.5h14"/>',
 '<path d="M12 2 21 6v7c0 5-9 9-9 9S3 18 3 13V6Z"/><path d="m7 12 3 3 7-7"/>',
 '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v13c0 4 16 4 16 0V5M4 11c0 4 16 4 16 0"/>',
 '<circle cx="12" cy="7" r="3"/><circle cx="4" cy="10" r="2"/><circle cx="20" cy="10" r="2"/><path d="M6 21v-4c0-5 12-5 12 0v4M1 19v-3c0-3 4-3 4-3M23 19v-3c0-3-4-3-4-3"/>',
 '<circle cx="12" cy="12" r="3"/><circle cx="4" cy="4" r="2"/><circle cx="20" cy="4" r="2"/><circle cx="4" cy="20" r="2"/><circle cx="20" cy="20" r="2"/><path d="m6 6 4 4m4 4 4 4m-4-4 4-4M6 18l4-4"/>',
 '<path d="M21 3C7 1-2 12 7 18c9 6 15-2 14-15ZM3 22 17 8M8 17l-1-5M12 13l5 1"/>',
 '<path d="M12 20 3.5 12C-3 5 7-1 12 7c5-8 15-2 8.5 5Z"/>',
]
for i,path in enumerate(paths):
    c=['#155FA8','#155FA8','#007D78','#007D78','#007D78','#943B9A','#943B9A'][i]
    svg=R/f'figures/principle-{i+1}.svg'
    svg.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g fill="none" stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{path}</g></svg>\n')
    subprocess.run(['inkscape',str(svg),'--export-type=pdf',f'--export-filename={R / ".build/assets" / ("principle-"+str(i+1)+".pdf")}'],check=True,capture_output=True)
def text(x,y,w,t,size=9.5,leading=14,color='ink',bold=False):
    weight=r'\bfseries' if bold else ''
    return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{\sffamily{weight}\fontsize{{{size}}}{{{leading}}}\selectfont\color{{{color}}}{t}}}'+'\n'
def rect(x,y,w,h,c):return rf'\Rect{{{x}}}{{{y}}}{{{w}}}{{{h}}}{{{c}}}'+'\n'
def flow(y,z,c='teal'):
    return rf'\draw[{c}!55,line width=.9pt,-{{Stealth[length=2mm]}}] \Pos{{105}}{{{y}}} -- \Pos{{105}}{{{z}}};'+'\n'
s=rect(22,79,166,28,'navy')
s+=text(27,83,156,'时代呼唤 → 共同愿景',9,13,'cyan',True)
s+=text(27,93,156,'从智能鸿沟，走向开放、包容、安全、可持续的全球 AI 开源生态',11,17,'white',True)
s+=flow(107,115)
layers=[(117,'第一层｜筑牢智能时代基石','blue',[(1,'开放互联','万物智联，普惠共生'),(2,'安全可信','透明算法，信任基石')]),(159,'第二层｜夯实伦理治理支柱','teal',[(3,'数据伦理','算法向善，责任共担'),(4,'多元包容','众智共创，价值共享'),(5,'全球协作','跨界协同，智能互联')]),(201,'第三层｜共创社会价值未来','violet',[(6,'绿色智能','低碳驱动，创新致远'),(7,'开源普惠','智能为公，成果共享')])]
for y,title,c,items in layers:
    s+=text(22,y,166,title,10.7,15,c,True)
    w=(166-4*(len(items)-1))/len(items)
    for j,(n,name,motto) in enumerate(items):
        x=22+j*(w+4)
        s+=rect(x,y+11,w,23,c+'!6')+rect(x,y+11,1,23,c)
        s+=text(x+4,y+14,7,rf'\includegraphics[width=6mm]{{.build/assets/principle-{n}.pdf}}')
        s+=text(x+13,y+14,w-17,f'0{n}  {name}',11,16,c,True)
        s+=text(x+4,y+24,w-8,motto,8.7,12,'muted')
    s+=flow(y+35,y+40,c)
s+=rect(22,244,166,19,'teal')
s+=text(27,247,156,'行动共识｜深化 AI 治理、算力共享与人才培育合作',11,16,'white',True)
s+=text(22,268,166,'图引 1　《全球开源与人工智能国际合作宣言》的愿景、三层原则与行动共识。',8.3,12,'muted')
(R/'figures/declaration.tex').write_text(s)
