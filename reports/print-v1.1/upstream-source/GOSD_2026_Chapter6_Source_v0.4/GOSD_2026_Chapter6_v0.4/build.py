"""Six-page, portrait Chapter 6 review edition: evidence, outlooks, strategy."""
from common import *
from content import INSIGHTS, OUTLOOKS, RECS
from figures import make_all

OUT = 'GOSD_2026_Chapter6_Review_v0.4.pdf'

def rect(x,y,w,h,c='paper'):
    return rf'\Rect{{{x}}}{{{y}}}{{{w}}}{{{h}}}{{{c}}}'+'\n'

def rule(x,y,xx,c='line'):
    return rf'\Rule{{{x}}}{{{y}}}{{{xx}}}{{{c}}}'+'\n'

def start(num,title,sub,accent='teal',bookmark=None,group_range=None):
    s='\\begin{canvas}\n'+rf'\Header{{第六章・洞察、前瞻与战略建议}}{{{accent}}}\Footer{{{num:02d}}}'+'\n'
    s+=rf'\pdfbookmark[1]{{{esc(bookmark or title)}}}{{p{num}}}'+'\n'
    s+=box(15,29,180,title,20,26,'navy',True)
    s+=box(15,43,151 if group_range else 180,sub,14 if group_range else 12.4,18 if group_range else 17,accent,True)
    if group_range:
        s+=box(168,44,27,group_range,9.3,13,'muted',False,True)
    return s

def end():
    return '\\end{canvas}\n'

def insightpage(p,i):
    title='6.1　十二项关键洞察'
    sub=p['group']+'　'+p['theme']
    group_range='洞察 '+p['items'][0][0]+'—'+p['items'][-1][0]
    s=start(i,title,sub,p['color'],'6.1 '+p['group']+' '+p['theme'],group_range)
    s+=box(15,54,180,p['intro'],10.15,15.5,'muted')
    s+=rf'\node[anchor=north west,inner sep=0pt] at \Pos{{15}}{{71}}{{\includegraphics[width=180mm]{{.build/assets/{p["fig"]}.pdf}}}};'+'\n'
    s+=box(15,185,180,p['caption'],8.1,11.3,'muted',False,True)
    for j,(ident,title,txt) in enumerate(p['items']):
        y=201+j*26
        s+=box(15,y,180,ident+'　'+title,11.1,14.7,p['color'],True)
        s+=box(15,y+6,180,txt,10.15,14.7)
    return s+end()

def compactpage(num,items,is_outlook):
    accent='blue' if is_outlook else 'teal'
    title='6.2　十大前瞻' if is_outlook else '6.3　十大战略建议'
    sub='未来值得关注的十个变化' if is_outlook else '推动全球协作，让开放成果持续惠及更多人'
    s=start(num,title,sub,accent)
    intro=('根据前五章的观察，提出近期、中期和面向 2030 的十项判断。这些前瞻说明可能的发展方向，能否实现仍取决于技术进步与合作条件。'
           if is_outlook else
           '围绕参与、供给、复用、治理与公共价值，提出面向政府、企业、研究机构和社区的十项建议，重点支持开放成果的共同建设、持续使用与长期维护。')
    s+=box(15,54,180,intro,10.5,16,'muted')
    if is_outlook:
        s+=rect(15,67,180,8,'paper')
        s+=box(18,68.5,174,'近期：发布后 6—12 个月　｜　中期：1—3 年　｜　2030：看长期方向与实现条件',9.3,13,'muted',False,True)
    else:
        s+=rule(15,73,195)
    # Read across each row. Each entry has a clear claim and a self-contained explanation.
    for i,p in enumerate(items):
        row,col=divmod(i,2)
        x=15+col*94; y=80+row*39.2
        c=({'近期':'blue','中期':'teal','2030':'violet'}[p['horizon']] if is_outlook else 'teal')
        s+=box(x,y-.5,11,p['id'],18,21,c,True)
        if is_outlook:
            s+=box(x,y+8,11,p['horizon'],7.8,10.5,c,False,True)
        s+=box(x+13,y,73,p['title'],11.9,16.5,'navy',True)
        s+=box(x,y+(14 if is_outlook else 10),86,p['body'],10.5 if is_outlook else 11,15.8 if is_outlook else 17,'ink')
        if row<4:
            s+=rule(x,y+36.8,x+86)
    return s+end()

def main():
    for p in [O,R/'review',D,B/'fonts',B/'assets']:
        p.mkdir(parents=True,exist_ok=True)
    ensure_fonts()
    export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
    make_all()
    tex=('\\documentclass[UTF8]{article}\n\\usepackage{layout}\n'
         '\\hypersetup{pdftitle={2026全球开源发展报告·精要版｜第六章 v0.4},pdfsubject={十二项关键洞察、十大前瞻与十大战略建议}}\n\\begin{document}\n')
    tex+=''.join(insightpage(p,i+1) for i,p in enumerate(INSIGHTS))
    tex+=compactpage(5,OUTLOOKS,True)+compactpage(6,RECS,False)+'\\end{document}\n'
    (R/'report.tex').write_text(tex)
    (D/'content.json').write_text(json.dumps(dict(version='v0.4',insights=INSIGHTS,outlooks=OUTLOOKS,recommendations=RECS),ensure_ascii=False,indent=2))
    compile_tex()
    shutil.copy2(O/'report.pdf',O/OUT)
    doc=fitz.open(O/OUT)
    outtext=''
    for i,page in enumerate(doc):
        page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(R/'review'/f'page-{i+1:02d}.png')
        outtext+=f'\nPAGE {i+1}\n'+page.get_text()
    (R/'review/text-extraction.txt').write_text(outtext)
    from PIL import Image,ImageDraw
    sheet=Image.new('RGB',(356*3,506*2),'#dee5e8')
    for i in range(len(doc)):
        im=Image.open(R/'review'/f'page-{i+1:02d}.png').convert('RGB')
        im.thumbnail((336,476))
        tile=Image.new('RGB',(356,506),'#dee5e8');tile.paste(im,((356-im.width)//2,8))
        ImageDraw.Draw(tile).text((12,486),f'{i+1:02d}',fill='#13253d')
        sheet.paste(tile,((i%3)*356,(i//3)*506))
    sheet.save(R/'review/contact-sheet.png')
    print(json.dumps({'version':'v0.4','pages':len(doc),'pdf':str(O/OUT)},ensure_ascii=False))

if __name__=='__main__':
    main()
