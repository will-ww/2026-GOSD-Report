from common import *
def render_pdf(pages,name,title,offset=0):
 if not (B/'fonts/NotoSansCJKsc-Regular.otf').exists():ensure_fonts()
 export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
 tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
 for i,p in enumerate(pages):
  tex+=rf'\begin{{canvas}}\Header{{第四章 · 全球开源技术生态}}{{teal}}\Footer{{{i+1+offset:02}}}'+ '\n'
  tex+=rf'\pdfbookmark[1]{{{esc(p["title"])}}}{{p{i}}}'+ '\n'
  tex+=box(15,27,180,p['title'],20,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
  tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+ '\n'
  tex+=box(15,217,180,p['caption'],7.6,10.7,'muted',False,True)
  for j,(head,body) in enumerate(p['analyses']):
   x=15+(j%2)*93;y=233+(j//2)*25
   tex+=box(x,y,87,head,10.3,14.2,'teal',True)+box(x,y+6,87,body,9.4,13.5)
  tex+=r'\end{canvas}'+'\n'
 tex+=r'\end{document}'
 (R/'report.tex').write_text(tex);compile_tex();doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':title,'author':'全球开源发展报告编制组','subject':'技术全景、分层排名与地域/组织观察；主期与期后分列'})
 out=O/name;doc.save(out,garbage=4,deflate=True);doc.close();doc=fitz.open(out)
 for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.65,1.65)).save(R/'review'/f'{name[:-4]}-p{i+1:02}.png')
 print('PDF',name,'PAGES',len(doc))
if __name__=='__main__':
 import sys
 sec=sys.argv[1];a=json.loads((R/'sections'/f'{sec}.json').read_text());render_pdf(a,f'GOSD_2026_Section_{sec[0]}.{sec[1]}_Review_v0.2.pdf',f'GOSD 2026 | {sec[0]}.{sec[1]} 评审稿 v0.2')
