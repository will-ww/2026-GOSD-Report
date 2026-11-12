"""Package only the current reproducible source and evidence; exclude PDF and fonts."""
from pathlib import Path
import json,hashlib,zipfile,subprocess
from datetime import datetime,timezone
import fitz

R=Path(__file__).resolve().parent
pdf=R/'output/GOSD_2026_Chapter5_Merged_Review_v0.2.pdf'
d=fitz.open(pdf)
assert len(d)==14
outside=[];bad=[];rects=[]
for i,p in enumerate(d):
    rects.append([round(p.rect.width,2),round(p.rect.height,2)])
    assert abs(p.rect.width-595.28)<.1 and abs(p.rect.height-841.89)<.1
    for block in p.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for s in line['spans']:
                box=fitz.Rect(s['bbox'])
                if box.x0<0 or box.y0<0 or box.x1>p.rect.width+1 or box.y1>p.rect.height+1:outside.append([i+1,s['text'],list(box)])
                if '\ufffd' in s['text']:bad.append([i+1,s['text']])
assert not outside and not bad
fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True)
font_rows=[x for x in fonts.splitlines()[2:] if x.strip()]
assert all('yes yes yes' in x for x in font_rows)
links=[l for p in d for l in p.get_links()]
assert len(d.get_toc())==14
qa={'version':'v0.2','pages':14,'portrait_A4':True,'figures':10,'page_dimensions_pt':rects,'bookmarks':len(d.get_toc()),'links':len(links),'font_entries':len(font_rows),'all_fonts_embedded_subset_unicode':True,'text_outside_page':outside,'replacement_glyphs':bad,'visual_review':'14 页逐页图像复核；重做跨国流向图标签布局；复核中国案例材料状态；图文四个分析编号对齐。','pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}
(R/'review/pdf-qa-v0.2.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
(R/'review/font-embedding-v0.2.txt').write_text(fonts)

sources={
 'data/live/api_overview_summary':'http://47.100.76.186:9529/api/overview/summary/',
 'data/live/api_openness_quadrant':'http://47.100.76.186:9529/api/openness/quadrant/',
 'data/live/api_openness_overview':'http://47.100.76.186:9529/api/openness/overview/',
 'data/live/grid889.json':'http://47.100.76.186:9529/api/openness/grid/ — page=1…9, page_size=100; original rows concatenated by model_id',
 'provenance/constitution-latest.md':'https://github.com/will-ww/2026-GOSD-Report/blob/main/editions/insights/constitution.md',
 'provenance/claims-map-latest.md':'https://github.com/will-ww/2026-GOSD-Report/blob/main/editions/insights/claims-map.md',
 'provenance/report-constitution-latest.md':'https://github.com/will-ww/2026-GOSD-Report/blob/main/docs/report-constitution.md',
 'provenance/material-inventory-latest.md':'https://github.com/will-ww/2026-GOSD-Report/blob/main/docs/material-inventory.md'
}
sources['inputs/51/data/supply-observation.json']='https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/c51e3441361407b68f10b339d97eff288319b503/preview/content/gosm/supply-observation.json'
rootfiles=['README.md','build.py','common.py','layout.sty','legacy51.py','legacy52.py','figures_v2.py','write_content.py','render_v2.py','validate_v2.py','package_review_v2.py','report.tex']
files=[R/x for x in rootfiles]
for folder in ['figures','assets','data/live']:
    files.extend(p for p in (R/folder).rglob('*') if p.is_file())
for section in ['51','52','53']:
    files.extend(p for p in (R/'inputs'/section/'data').rglob('*') if p.is_file())
files.extend([R/'data/content-v0.2.json',R/'data/references-v0.2.json',R/'data/chapter6-evidence-v0.2.json'])
files.extend(p for p in (R/'provenance').glob('*-latest.md'))
files.extend([R/'provenance/fresh-management-reads.json',R/'provenance/baseline-review.md',R/'provenance/readable-content-review.md',R/'review/data-qa-v0.2.json',R/'review/figure-qa.json',R/'review/pdf-qa-v0.2.json',R/'review/font-embedding-v0.2.txt'])
files=sorted(set(p for p in files if p.is_file() and p.suffix.lower() not in ['.pdf','.otf','.ttf','.ttc']))
manifest={'version':'v0.2','created_utc':datetime.now(timezone.utc).isoformat(),'observed_read_date_beijing':'2026-11-11','authority':'will-ww/2026-GOSD-Report','confirmed_baseline':'fff392e957bab9fb6d89d49dea712af47484efaa','geography':'2026-10-17 frozen 826-organization sample; live geography endpoint timed out','files':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':sources.get(str(p.relative_to(R)),'Derived or frozen input; see references-v0.2.json and input source manifests')} for p in files]}
mf=R/'provenance/source-manifest-v0.2.json';mf.write_text(json.dumps(manifest,ensure_ascii=False,indent=2));files.append(mf)
dest=R/'output/GOSD_2026_Chapter5_Merged_Source_v0.2.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,Path('GOSD_2026_Chapter5_Merged_Source_v0.2')/p.relative_to(R))
print(json.dumps({'pdf_qa':qa,'archive':str(dest),'files':len(files),'bytes':dest.stat().st_size},ensure_ascii=False))
