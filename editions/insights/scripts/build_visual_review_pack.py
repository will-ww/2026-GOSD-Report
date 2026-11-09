"""Assemble the current frontmatter and chapter 1 review; PDFs stay outside Git.

Run after both component build.sh scripts. The output uses continuous page numbers
and clickable chapter navigation. SVG exports are cropped from the same rendered
vectors, so the report and reusable images share one source.
"""
from pathlib import Path
import argparse
import subprocess
import fitz

E = Path(__file__).resolve().parents[1]
F = E/'frontmatter/v0.4'
C = E/'chapters/01/v0.3'
MM = 72/25.4

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True)
    args=p.parse_args()
    inputs=[F/'output/GOSD_2026_Frontmatter_Review_v0.4.pdf',
            C/'output/GOSD_2026_Insights_Chapter1_Review_v0.3.pdf']
    doc=fitz.open()
    for src in inputs:
        with fitz.open(src) as part:
            assert len(part)==10
            doc.insert_pdf(part)
    # Replace only the existing footer numeral, not its rule or running text.
    for i in range(11,20):
        page=doc[i]
        page.add_redact_annot(fitz.Rect(174*MM,280*MM,190*MM,290*MM),fill=(1,1,1))
        page.apply_redactions(images=0,graphics=0,text=0)
        page.insert_textbox(fitz.Rect(174*MM,282*MM,188*MM,291*MM),str(i+1),
                            fontsize=12,fontname='gosdpages',fontfile='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',align=2,color=(.075,.145,.239))
    toc=[[1,'封面',1],[1,'编委会',2],[1,'目录',3],[1,'执行摘要',5],
         [1,'引言：开源共创智能未来',7],[2,'宣言结构图',10],
         [1,'第一章 从开放协作到公共价值',11],
         [2,'1.1 人工智能时代的开源协作：双向重塑',12],
         [2,'1.2 开源发展目标：从开放资源到公共能力',14],
         [3,'SDGs 与数字公共品',14],[3,'OSDGs 四支柱十维框架',15],
         [2,'1.3 观察方法：跨平台的全球开源全景',17],
         [3,'OSDI 指标体系',17]]
    doc.set_toc(toc)
    # Correct the inherited chapter cover's original page label using its exact text bbox.
    page=doc[10]
    spans=[s for b in page.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text']=='01' and s['bbox'][1]>750]
    for s in spans:
        page.add_redact_annot(fitz.Rect(s['bbox']),fill=False)
    if spans:
        page.apply_redactions(images=0,graphics=0,text=0)
        for s in spans:page.insert_text(s['origin'],'11',fontname='gosdpages',fontfile='/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',fontsize=s['size'],color=(.075,.145,.239))
    for rect,target in [((40,85,188,97),10),((40,99,188,107),11),((40,107,188,115),13),((40,115,188,125),16)]:
        doc[2].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(*(v*MM for v in rect)),'page':target})
    for rect,target in [((22,63,56,72),1),((89,63,128,72),4),((136,63,188,72),6)]:
        doc[2].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(*(v*MM for v in rect)),'page':target})
    doc.set_page_labels([{'startpage':0,'prefix':'','style':'D','firstpagenum':1}])
    doc.set_metadata({'title':'GOSD 2026 精要版｜前置内容与第一章视觉强化评审稿 v0.4',
                      'author':'全球开源发展报告编制组',
                      'subject':'前置 v0.4 + 第一章 v0.3；2026-11-09；待作者评审'})
    out=Path(args.output).resolve();out.parent.mkdir(parents=True,exist_ok=True)
    doc.save(out,garbage=4,deflate=True)
    # Reusable vector figures: text is represented by glyph paths, fonts are not packaged.
    specs=[(F,9,(22,79,188,263),'declaration-2026'),
           (C,3,(22,101,188,255),'sdgs-digital-public-goods'),
           (C,4,(22,94,188,258),'osdgs-framework'),
           (C,6,(22,101,188,263),'osdi-framework')]
    for root,page_no,box,name in specs:
        src=inputs[0] if root==F else inputs[1]
        dest=root/'figures/exports';dest.mkdir(exist_ok=True)
        temp=root/'.build'/f'{name}.pdf'
        with fitz.open(src) as source,fitz.open() as cropped:
            clip=fitz.Rect(*(v*MM for v in box))
            p=cropped.new_page(width=clip.width,height=clip.height)
            p.show_pdf_page(p.rect,source,page_no,clip=clip)
            cropped.save(temp)
        subprocess.run(['pdftocairo','-svg',str(temp),str(dest/(name+'.svg'))],check=True)
    print(f'Created {len(doc)}-page review pack and four source-aligned vector figures.')

if __name__=='__main__':main()
