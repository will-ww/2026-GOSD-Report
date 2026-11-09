from pathlib import Path
import json, shutil
from svgkit import SVG, QA
R=Path(__file__).resolve().parents[1]; O=R/'figures/new'
T=json.loads((R/'design/approved_brand_tokens.json').read_text())
BLUE='#155FA8';TEAL='#007D78';LIGHT='#F3F7F9';GRAY='#536B7D'
s=SVG(166,145)
# Two independent categorical axes. No quantitative scales.
s.rect(0,15,78,54,'#F2F6FB',1.5);s.rect(88,15,78,54,'#EFF7F5',1.5)
s.rect(0,82,78,54,'#F6F7F8',1.5);s.rect(88,82,78,54,'#EFF7F5',1.5)
s.line(83,9,83,138,GRAY,.45);s.path('M81 12 L83 9 L85 12',GRAY,.45)
s.line(0,75,166,75,GRAY,.45);s.path('M163 73 L166 75 L163 77',GRAY,.45)
s.text(83,5,'开发者',10.5,GRAY,True,'middle');s.text(83,144,'项目',10.5,GRAY,True,'middle')
s.text(2,72,'微观视角 · 社区贡献度',8,BLUE,True);s.text(164,72,'宏观视角 · 全域影响力',8,TEAL,True,'end')
def box(x,y,w,h,lines,solid=False,c=TEAL):
 s.rect(x,y,w,h,c if solid else '#FFFFFF',1.4)
 if not solid:s.path(f'M{x+1.4} {y} H{x+w-1.4} Q{x+w} {y} {x+w} {y+1.4} V{y+h-1.4} Q{x+w} {y+h} {x+w-1.4} {y+h} H{x+1.4} Q{x} {y+h} {x} {y+h-1.4} V{y+1.4} Q{x} {y} {x+1.4} {y}',c,.25)
 for j,t in enumerate(lines):s.text(x+w/2,y+h/2+(j-(len(lines)-1)/2)*4.8+1.3,t,9 if solid else 7.7,'white' if solid else c,True,'middle')
def arr(x1,y1,x2,y2,c):
 s.line(x1,y1,x2,y2,c,.32);s.path(f'M{x2-1.2} {y2-1.7} L{x2} {y2} L{x2+1.2} {y2-1.7}',c,.32)
box(13,21,52,15,['开发者','社区贡献度'],True,BLUE)
s.line(39,36,39,42,BLUE,.3);s.line(13,42,65,42,BLUE,.3)
for x,ls in [(1,['个体或群体','开源贡献度']),(27,['企业或组织','开源贡献度']),(53,['国家或地区','开源贡献度'])]:
 arr(x+12,42,x+12,48,BLUE);box(x,49,24,14,ls,False,BLUE)
box(101,21,52,15,['开发者','全域影响力'],True);arr(127,36,127,48,TEAL)
box(101,49,52,14,['个人或群体开源影响力'])
s.text(39,103,'本图未设置相应指标',10,GRAY,True,'middle')
s.text(39,114,'不表示项目没有贡献',8.5,GRAY,False,'middle')
box(101,87,52,15,['仓库 / 项目','全域影响力'],True)
s.line(127,102,127,108,TEAL,.3);s.line(101,108,153,108,TEAL,.3)
for x,ls in [(89,['企业或组织','开源影响力']),(115,['国家或地区','开源影响力']),(141,['技术生态','开源影响力'])]:
 arr(x+12,108,x+12,115,TEAL);box(x,116,24,14,ls)
s.save('openrank_quadrants')
shutil.copyfile(R.parent/'full_report_v2.0/front/figures/new/dimension_strip.pdf',O/'appendix_dimensions.pdf')
# Back cover: same fixed ten-node brand mark, no new institution marks.
s=SVG(210,297);s.rect(0,0,210,297,'#13253D')
s.e.append('<defs><linearGradient id="backflow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#007D78"/><stop offset="1" stop-color="#13253D"/></linearGradient></defs>')
s.rect(0,0,210,297,'url(#backflow)')
for j in range(9):s.path(f'M-35 {17+j*13} C42 {5+j*9} 119 {129+j*9} 245 {47+j*14}','#98D8DB',.25,.17)
s.text(22,24,'GOSD / 2026',9,'#DFE9EE',True)
s.embed(O/'osdgs-display-dark-outlined.svg',65,48,80,80)
s.text(105,164,'共同创造',26,'white',True,'middle')
s.text(105,181,'开放的智能未来',26,'white',True,'middle')
s.text(105,199,'OPEN SOURCE, A SHARED INTELLIGENT FUTURE',8.8,'#C5D9DF',False,'middle')
s.line(77,213,133,213,'#7CABB9',.4)
s.text(105,232,'参与 · 供给 · 复用 · 治理 · 公共价值',10.4,'#D4E3E7',False,'middle')
s.text(105,251,'2026 全球开源发展报告',11,'white',True,'middle')
s.text(105,261,'第二轮整合评审稿 v2.0 · 2026年11月7日',8.2,'#B9CDD5',False,'middle')
s.text(105,269,'主统计期 2025-07-01 至 2026-06-30',8.2,'#B9CDD5',False,'middle')
for i,d in enumerate(T['dimensions']):s.line(22+i*16.7,284,22+i*16.7+14.2,284,d['hero_color'],.8)
s.text(105,292,'OPEN SOURCE DEVELOPMENT GOALS',6.7,'#C0D2DB',False,'middle');s.save('full_report_back_cover')
(R/'review/appendix_figure_geometry.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
print('OpenRank diagram and back cover exported.')
