from pathlib import Path
import fitz,json,hashlib,re,unicodedata
R=Path(__file__).resolve().parent
ROOT=R.parent
PAGES=[]; INDEX=[]; SOURCES=[]
mm=72/25.4
clip=fitz.Rect(15*mm,53*mm,195*mm,197.9*mm)
for s,count in [(31,3),(32,4),(33,3),(34,4),(35,3),(36,3)]:
    base=R/'upstream'/str(s)
    p=base/'sections'/f'{s}.json'
    if not p.exists():p=base/'data/content.json'
    content=json.loads(p.read_text())
    assert len(content)==count
    src=ROOT/'merge3-reference'/f'GOSD_2026_Section_3-{s-30}_Review_v0.2.pdf'
    d=fitz.open(src)
    for i,item in enumerate(content):
        n=len(PAGES)+1; name=f'fig-3-{n:02d}'
        out=fitz.open();pg=out.new_page(width=clip.width,height=clip.height)
        pg.show_pdf_page(pg.rect,d,i,clip=clip)
        # Crop preserves the final approved map annotation adjustment in 3.4.
        fp=R/'.build/assets'/f'{name}.pdf';out.save(fp,garbage=4,deflate=True)
        (R/'figures'/f'{name}.svg').write_text(pg.get_svg_image())
        INDEX.append(dict(number=f'3-{n}',section=f'3.{s-30}',old_figure=item['figure'],source_file=src.name,source_page=i+1,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),figure_sha256=hashlib.sha256(fp.read_bytes()).hexdigest(),text=pg.get_text()))
        item['source_figure']=item['figure'];item['figure']=name;item['section']=f'3.{s-30}';item['number']=f'3-{n}';item['page']=n+1
        PAGES.append(item)
    so=base/'data/sources.json'
    if so.exists():SOURCES.extend(json.loads(so.read_text()))
(R/'data/original-content.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2))
(R/'data/figure-index.json').write_text(json.dumps(INDEX,ensure_ascii=False,indent=2))
(R/'data/sources-full.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2))
print('Prepared',len(PAGES),'approved vector figures')
