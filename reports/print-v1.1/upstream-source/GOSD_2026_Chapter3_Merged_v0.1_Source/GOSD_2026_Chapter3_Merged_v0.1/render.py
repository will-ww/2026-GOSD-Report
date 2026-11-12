from build import *
from chapter_pages import intro,closing,APPENDIX
import unicodedata,re
P=json.loads((D/'content.json').read_text())
ensure_fonts()
if not (B/'assets/osdgs-compact.pdf').exists():export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
for p in P:
    if not (B/'assets'/f'{p["figure"]}.pdf').exists():export(F/f'{p["figure"]}.svg',B/'assets'/f'{p["figure"]}.pdf')
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'+intro()
TEXTBOXES=[]
for p in P:
    tex+=rf'\begin{{canvas}}\Header{{第三章 · 全球开源影响力排行榜}}{{violet}}\Footer{{{p["page"]:02d}}}'+'\n'
    tex+=box(15,27,180,p['title'],20,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
    tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
    tex+=box(15,199,180,p['caption'],7.7,10.7,'muted',False,True)
    for j,(h,b) in enumerate(p['analyses']):
        x=15+j%2*93;y=214+j//2*34
        tex+=box(x,y,87,h,10.1,14,'violet',True)+box(x,y+6,87,b,9.8,14.9)
    tex+=r'\end{canvas}'+'\n'
tex+=closing()
for f in APPENDIX:tex+=f()
tex+=r'\end{document}'
(R/'report.tex').write_text(tex)
compile_tex()
d=fitz.open(O/'report.pdf')
# Preserve vector glyphs while normalizing compatibility radicals in searchable text.
changed=0
for x in range(1,d.xref_length()):
    typ,val=d.xref_get_key(x,'ToUnicode')
    if typ!='xref':continue
    target=int(val.split()[0]);raw=d.xref_stream(target)
    if not raw:continue
    st=raw.decode('latin1')
    def sub(m):
        global changed
        cid,u=m.groups();v=int(u,16)
        if 0x2f00<=v<=0x2fdf:
            changed+=1;n=unicodedata.normalize('NFKC',chr(v))
            return f'<{cid}> <{n.encode("utf-16-be").hex()}>'
        return m.group(0)
    ns=re.sub(r'<([0-9a-fA-F]{4})>\s+<([0-9a-fA-F]{4})>',sub,st)
    if ns!=st:d.update_stream(target,ns.encode('latin1'))
toc=[[1,'第三章 全球开源影响力排行榜',1]]
section_titles={'3.1':'行政区划：参与基础与影响节点','3.2':'企业：供给布局与时序变化','3.3':'基金会：共同建设与维护重心','3.4':'项目：技术分层与全球协作','3.5':'新势力：从仓库到体系供给','3.6':'模型：影响位置与家族接续'}
seen=set()
for p in P:
    if p['section'] not in seen:
        toc.append([2,p['section']+' '+section_titles[p['section']],p['page']]);seen.add(p['section'])
    toc.append([3,'图 '+p['number']+' '+p['title'].split(' ',1)[-1],p['page']])
toc.append([2,'本章小结：从影响位置到共同建设',22])
toc.append([1,'附录 A 第三章方法与证据',23])
for i,t in enumerate(['指标与时间口径','对象边界与核验范围','数据与技术证据','案例与外部研究来源']):toc.append([2,f'A{i+1} '+t,23+i])
d.set_toc(toc)
d.set_page_labels([{'startpage':0,'prefix':'','style':'D','firstpagenum':1},{'startpage':22,'prefix':'A','style':'D','firstpagenum':1}])
for i,pg in enumerate([2,5,9,12,16,19]):
    y=98+i*20
    d[0].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(15*72/25.4,y*72/25.4,195*72/25.4,(y+15)*72/25.4),'page':pg-1,'to':fitz.Point(0,0)})
d.set_metadata({'title':'GOSD 2026 精要版｜第三章 全球开源影响力排行榜｜合稿 v0.1','author':'全球开源发展报告编制组','subject':'2026-11-10；六节、20 幅组合图；统一叙事、行动启示及附录 A','keywords':'GOSD; OpenRank; ModelRank; 开源; 人工智能; AI 普惠'})
out=O/'GOSD_2026_Chapter3_Merged_Review_v0.1.pdf'
d.save(out,garbage=4,deflate=True)
d.close();d=fitz.open(out)
assert len(d)==26,len(d)
for i,p in enumerate(d):p.get_pixmap(matrix=fitz.Matrix(1.4,1.4)).save(R/'review'/f'page-{i+1:02}.png')
(R/'review/pdf-text.txt').write_text('\n\f\n'.join(p.get_text() for p in d))
print('BUILT',out,'pages',len(d),'unicode repairs',changed,'bytes',out.stat().st_size)
