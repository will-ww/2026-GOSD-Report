"""Replace only the institute opening page; preserve book page objects and navigation."""
from pathlib import Path
import json, hashlib, re, subprocess
import fitz
from PIL import Image
from pypdf import PdfWriter

R=Path(__file__).resolve().parent
O=R/'output'; Q=R/'review'; W=R.parent
MM=72/25.4
target=4
revised=fitz.open(O/'report-page.pdf')
checks=[]
def check(name,ok,details=None):
    checks.append(dict(check=name,passed=bool(ok),details=details))
    assert ok,(name,details)
def canon(s):return re.sub(r'\s+','',s).replace('・','·')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def links(d):
    return [[{k:(list(v) if isinstance(v,(fitz.Rect,fitz.Point)) else v)
              for k,v in item.items() if k not in ('xref','id')}
             for item in p.get_links()] for p in d]

plan=json.loads((Q/'text-box-plan.json').read_text())
log=(O/'report-page.log').read_text()
heights={m[0]:float(m[1])*25.4/72.27 for m in re.findall(r'AUDITBOX\|(siri\d+)\|[^\n]*?\|([\d.]+)pt',log)}
check('No LaTeX overflow or missing glyph warnings',not re.search(r'Overfull|Missing character|LaTeX Error',log))
for b in plan:
    h=heights[b['id']]
    check('Text box fits: '+b['id'],h<=b['max_height'],dict(height_mm=h,max_height_mm=b['max_height']))
    top=b['y']-h/2 if b['center'] else b['y']
    check('Text box inside print area: '+b['id'],b['x']>=18 and b['x']+b['w']<=192.01 and top>12 and top+h<294)

text=canon(revised[0].get_text())
for b in plan:
    check('Searchable content retained: '+b['id'],canon(b['text']) in text)
check('Independent institute identity','GOSD' not in text and 'OSDG' not in text)
image_info=revised[0].get_image_info()
check('One unmodified institution logo image',len(image_info)==1)
im=Image.open(R/'source/assets/siri-color.png'); a,b,c,d=im.getbbox()
x0,y0,x1,y1=image_info[0]['bbox']
ink_x0=x0+(x1-x0)*a/im.width; ink_x1=x0+(x1-x0)*c/im.width
check('Visible logo centered',abs((ink_x0+ink_x1)/2-revised[0].rect.width/2)<.1)
check('Visible logo width 110mm',abs((ink_x1-ink_x0)/MM-110)<.1)
check('Logo effective resolution above 450 dpi',(c-a)/110*25.4>450)

jobs=[
 (W/'full-print-v1.0/output/pdf/GOSD_2026_Essential_Full_Print_v1.0.pdf',O/'GOSD_2026_Essential_Full_Print_v1.1.pdf',138,'v1.0','v1.1'),
 (W/'full-print-v1.0/inputs/GOSD_2026_Print_M01_Frontmatter_v0.1.pdf',O/'GOSD_2026_Print_M01_Frontmatter_v0.2.pdf',18,'v0.1','v0.2')
]
results=[]
for src,dst,count,oldversion,newversion in jobs:
    original=fitz.open(src); doc=fitz.open(src)
    page_xref=doc[target].xref
    temp=doc.new_page(width=doc[target].rect.width,height=doc[target].rect.height)
    temp.show_pdf_page(temp.rect,revised,0)
    for key in ['Resources','Contents']:
        typ,value=doc.xref_get_key(temp.xref,key)
        check('Replacement carries '+key,typ!='null')
        doc.xref_set_key(page_xref,key,value)
    doc.delete_page(len(doc)-1)
    meta=dict(doc.metadata)
    meta['title']=meta.get('title','').replace(oldversion,newversion)
    meta['producer']='GOSD institute-layout revision '+newversion
    doc.set_metadata(meta)
    # Keep independently placed image streams separate; avoid cross-page image-cache changes.
    doc.save(dst,garbage=2,deflate=True)
    doc.close()
    if original.xref_get_key(original.pdf_catalog(),'PageMode')[0]=='null':
        # PyMuPDF auto-selects attachments when saving a signed input. Restore its original implicit mode.
        writer=PdfWriter(clone_from=str(dst))
        writer.root_object.pop('/PageMode',None)
        temp=dst.with_suffix('.mode.pdf')
        writer.write(str(temp)); writer.close(); temp.replace(dst)
    new=fitz.open(dst)
    prefix=dst.stem+': '
    check(prefix+'Page count',len(new)==len(original)==count)
    check(prefix+'All page labels retained',new.get_page_labels()==original.get_page_labels())
    check(prefix+'All bookmarks retained',new.get_toc()==original.get_toc())
    check(prefix+'All link destinations retained',links(new)==links(original))
    for key in ['PageLayout','PageMode','ViewerPreferences']:
        before=original.xref_get_key(original.pdf_catalog(),key)
        after=new.xref_get_key(new.pdf_catalog(),key)
        check(prefix+key+' retained',after==before)
    for i in range(count):
        p=new[i]; old=original[i]
        check(prefix+f'P{i+1} A4',abs(p.rect.width-210*MM)<.1 and abs(p.rect.height-297*MM)<.1)
        if i==target:
            check(prefix+'New page renders unchanged',p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples==revised[0].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples)
            check(prefix+'New page searchable text',canon(p.get_text())==text)
        else:
            check(prefix+f'P{i+1} text unchanged',p.get_text()==old.get_text())
            check(prefix+f'P{i+1} artwork unchanged',p.get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False).samples==old.get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False).samples)
    # Every paragraph previously on this opening page remains, in its original order.
    oldblocks=[b[4] for b in original[target].get_text('blocks') if b[6]==0]
    for i,b in enumerate(oldblocks):
        check(prefix+f'Original text block {i+1} retained',canon(b) in text)
    fonts={f[0] for f in new[target].get_fonts(full=True)}
    for x in fonts:
        name,ext,kind,data=new.extract_font(x)
        check(prefix+'Embedded font: '+name,bool(data) or kind=='Type3')
    if count==138:
        prior=json.loads((W/'full-print-v1.0/review/full-print-verification.json').read_text())
        for n in prior['intentionally_blank_physical_pages']:
            p=new[n-1]
            check(f'Intended blank P{n} retained',not p.get_text().strip() and not p.get_images() and not p.get_drawings())
        check('Repaired folio 80 still present','5,777' in new[97].get_text() and len(new[97].get_xobjects())<100)
        check('GOSD back cover retained',new[-1].get_text()==original[-1].get_text())
        new[target].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(Q/'full-report-page5.png')
    results.append(dict(source=str(src),source_sha256=sha(src),output=str(dst),output_sha256=sha(dst),pages=count,bytes=dst.stat().st_size))
    print(f'{dst.name}: {count} pages verified',flush=True)

subprocess.run(['pdftoppm','-f','1','-singlefile','-scale-to','1800','-png',str(O/'SIRI_Institute_Introduction_v1.1.pdf'),str(Q/'standalone-poppler')],check=True)
result=dict(version='1.1',date='2026-11-11',changed_physical_page=5,folio='iii',
    scope='Only institute introduction layout; no research, statistical, wording or pagination changes.',
    evidence=['Approved v1.0 full print PDF','Approved M01 v0.1 PDF','Supplied transparent color institute logo','Original institute-research-system.svg'],
    outputs=results,checks=checks)
(Q/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(f'Passed {len(checks)} checks',flush=True)
