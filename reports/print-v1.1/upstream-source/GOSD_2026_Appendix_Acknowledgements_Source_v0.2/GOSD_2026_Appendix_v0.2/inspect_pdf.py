"""Render every page and check the document's visible text and table geometry."""
from pathlib import Path
import json,hashlib,re,subprocess
import fitz
from PIL import Image,ImageDraw

R=Path(__file__).resolve().parent
PDF=R/'output/GOSD_2026_Appendix_Acknowledgements_Review_v0.2.pdf'
doc=fitz.open(PDF)
assert len(doc)==10
outside=[];overlaps=[];text='';page_info=[]
for i,p in enumerate(doc):
    p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(R/'review'/f'page-{i+1:02d}.png')
    text+=f'\nPAGE {i+1}\n'+p.get_text()
    lines=[line for b in p.get_text('dict')['blocks'] if 'lines' in b for line in b['lines']]
    for a,l in enumerate(lines):
        r=fitz.Rect(l['bbox']);t=''.join(s['text'] for s in l['spans'])
        if r.x0<0 or r.y0<0 or r.x1>p.rect.width or r.y1>p.rect.height:
            outside.append({'page':i+1,'text':t,'box':list(r)})
        if 65<r.y0<800 and r.y1>790:
            outside.append({'page':i+1,'text':t,'note':'body reaches footer zone'})
        for other in lines[a+1:]:
            q=fitz.Rect(other['bbox']);c=r&q
            if not c.is_empty and c.width>3 and c.height>3:
                overlaps.append({'page':i+1,'a':t,'b':''.join(s['text'] for s in other['spans'])})
    page_info.append({'page':i+1,'body_bottom_mm':round(max((l['bbox'][3] for l in lines if 65<l['bbox'][1]<790),default=0)/72*25.4,1)})
assert not outside,outside
assert not overlaps,overlaps
for stale in ['核心来源','[S1','[S2','[S3','[S4','[S5','[S6','[S7','[S8','TF-IDF','LinearSVC','Wilson','2.2235','0.5252']:
    assert stale not in text,stale
compact=lambda s:re.sub(r'\s+','',s)
from content import INDICATORS
assert len(INDICATORS)==29
for name,_ in INDICATORS:
    assert compact(name) in compact(text),name
for code in ['T/CESA1270.3—2023','T/CESA1270.4—2023','T/CESA1270.5—2023']:
    assert code in compact(text),code
assert all(not p.get_links() for p in doc),'Extraneous external links'
fonts=subprocess.check_output(['pdffonts',str(PDF)],text=True)
assert 'NotoSansCJKsc' in fonts and 'NotoSerifCJKsc' in fonts
assert all('yes' in l for l in fonts.splitlines()[2:])
log=(R/'output/report.log').read_text()
assert 'Overfull' not in log and 'Missing character' not in log
fqa=json.loads((R/'review/figure-qa.json').read_text())
assert all(not f['out_of_bounds'] and not f['overlaps'] for f in fqa),fqa
(R/'review/fonts.txt').write_text(fonts)
(R/'review/text-extraction.txt').write_text(text)
report={'version':'v0.2','pages':10,'portrait_a4':True,'embedded_fonts':True,'indicators_preserved':29,'standard_numbers_preserved':3,'external_links':0,'source_list_and_dangling_markers_removed':True,'table_alignment':'horizontal centering with vertically centered m columns, including tabularx X columns','body_outside_page':outside,'body_overlaps':overlaps,'pages_geometry':page_info,'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'figure_geometry':fqa}
(R/'review/quality-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
sheet=Image.new('RGB',(356*5,506*2),'#dfe7e9')
for i,p in enumerate(doc):
    im=Image.open(R/'review'/f'page-{i+1:02d}.png').convert('RGB');im.thumbnail((336,476))
    tile=Image.new('RGB',(356,506),'#dfe7e9');tile.paste(im,((356-im.width)//2,8));ImageDraw.Draw(tile).text((12,486),f'{i+1:02d}',fill='#19314a')
    sheet.paste(tile,((i%5)*356,(i//5)*506))
sheet.save(R/'review/contact-sheet.png')
print(json.dumps({k:report[k] for k in ['version','pages','indicators_preserved','external_links','pdf_sha256']},ensure_ascii=False))
