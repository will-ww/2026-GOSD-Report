from pathlib import Path
import fitz,json,re,unicodedata,subprocess,hashlib
import numpy as np
R=Path(__file__).resolve().parent
pdf=R/'output/GOSD_2026_Chapter3_Merged_Review_v0.1.pdf'
d=fitz.open(pdf);idx=json.loads((R/'data/figure-index.json').read_text());content=json.loads((R/'data/content.json').read_text())
mm=72/25.4;clip=fitz.Rect(15*mm,53*mm,195*mm,197.9*mm)
def norm(t):return re.sub(r'\s+','',unicodedata.normalize('NFKC',t))
figs=[]
for i,row in enumerate(idx):
    src=fitz.open(R.parent/'merge3-reference'/row['source_file']);p=src[row['source_page']-1];q=d[i+1]
    a=p.get_pixmap(matrix=fitz.Matrix(1,1),clip=clip);b=q.get_pixmap(matrix=fitz.Matrix(1,1),clip=clip)
    aa=np.frombuffer(a.samples,dtype=np.uint8).astype(float);bb=np.frombuffer(b.samples,dtype=np.uint8).astype(float)
    equal=norm(p.get_text(clip=clip))==norm(q.get_text(clip=clip));mad=float(np.mean(np.abs(aa-bb)))
    figs.append({'figure':row['number'],'source_page':row['source_page'],'chapter_page':i+2,'text_equal':equal,'mean_pixel_difference_0_255':round(mad,4)})
    assert equal,('figure text changed',row['number'])
    assert mad<1.0,('figure changed visually',row['number'],mad)
text='\n'.join(p.get_text() for p in d)
for phrase in ['附录 1','本轮评审','评审重点','未提交 GitHub','点击编号','图 3-5a','图 3-5b']:
    assert phrase not in text,phrase
assert '\ufffd' not in text
assert all(595<p.rect.width<596 and 841<p.rect.height<843 for p in d)
assert len(d)==26 and len(idx)==20
assert all(re.search(r'图\s*3[-\u2011]'+str(i+1)+r'(?!\d)',d[i+1].get_text()) for i in range(20))
assert sum(len(p.get_links()) for p in list(d)[1:22])==0
fonttext=subprocess.check_output(['pdffonts',str(pdf)],text=True)
(R/'review/fonts.txt').write_text(fonttext)
fonts=fonttext.splitlines()[2:];assert fonts and all(re.search(r'\byes\s+yes\s+yes\b',f) for f in fonts)
collisions=[]
for pn in range(1,21):
    lines=[l for b in d[pn].get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] if l['bbox'][1]>600 and l['bbox'][1]<795]
    for j,a in enumerate(lines):
        for b in lines[j+1:]:
            ix=min(a['bbox'][2],b['bbox'][2])-max(a['bbox'][0],b['bbox'][0]);iy=min(a['bbox'][3],b['bbox'][3])-max(a['bbox'][1],b['bbox'][1])
            if ix>1 and iy>1:collisions.append([pn+1,ix,iy])
assert not collisions,collisions
out={'version':'v0.1','date':'2026-11-10','pages':26,'body_pages':22,'appendix_pages':4,'figures':20,'all_a4_portrait':True,'all_fonts_embedded':True,'font_count':len(fonts),'figure_checks':figs,'analysis_text_overlaps':collisions,'body_external_links':0,'contents_links':6,'appendix_links':sum(len(p.get_links()) for p in list(d)[22:]),'bookmarks':len(d.get_toc()),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'visual_review':'26 pages rendered and inspected; final changed appendix pages reinspected'}
(R/'review/release-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='figure_checks'},ensure_ascii=False,indent=2))
print('Maximum figure pixel difference:',max(f['mean_pixel_difference_0_255'] for f in figs))
