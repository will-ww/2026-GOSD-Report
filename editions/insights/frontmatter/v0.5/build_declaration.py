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

import sys
sys.path.insert(0,str(R.parents[1]/'scripts'))
from infographic_primitives_v1 import *
s=text(22,181,166,'宣言总览｜以共同愿景贯通三层原则',10.3,15,'navy',True)
for yy,c in [(199.5,'blue'),(223.5,'teal'),(247.5,'violet')]:
    s+=curve((64,224),(79,yy),(72,224),(72,yy),c+'!10',4)
    s+=curve((64,224),(79,yy),(72,224),(72,yy),c+'!55',.65)
s+=orb(46,224,17,'blue')
s+=text(27,199,38,'共同愿景',8.5,12,'teal',True,True)
s+=text(28,216,36,'开源共创',12.2,17,'navy',True,True)
s+=text(28,227,36,'智能未来',12.2,17,'navy',True,True)
for y,title,c,items in [
 (190,'智能时代基石','blue',[(1,'开放互联'),(2,'安全可信')]),
 (214,'伦理治理支柱','teal',[(3,'数据伦理'),(4,'多元包容'),(5,'全球协作')]),
 (238,'社会价值未来','violet',[(6,'绿色智能'),(7,'开源普惠')])]:
    s+=ribbon(80,y,108,19,c)
    s+=text(84,y+2,100,title,8.7,12,c,True)
    step=100/len(items)
    for j,(n,name) in enumerate(items):
        x=84+j*step
        s+=icon(x,y+10,4.1,'principle-'+str(n))
        s+=text(x+6,y+10,step-7,name,9.2,12,'navy',True)
s+=ribbon(22,261,166,9,'teal')
s+=text(27,262.5,28,'行动共识',9.5,13,'teal',True)
s+=text(60,262.5,123,'深化 AI 治理、算力共享与人才培育合作',9.4,13,'navy',True)
s+=text(22,273,166,'图引 1　2026 宣言的共同愿景、三层七项原则与行动共识（依据前述全文绘制）。',7.8,11,'muted')
(R/'figures/declaration.tex').write_text(s)

# The summary cards adopt the same light-stream treatment.
p=R/'figures/features.tex'
f=p.read_text()
for x in [22,108]:
    for y in [215,246]:f=f.replace(rect(x,y,80,27,'paper'),ribbon(x,y,80,27,'teal'))
p.write_text(f)
