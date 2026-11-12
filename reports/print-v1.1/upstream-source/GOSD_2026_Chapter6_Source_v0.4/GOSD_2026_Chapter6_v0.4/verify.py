"""Independent numerical and document checks against the frozen inputs."""
from pathlib import Path
import json,csv,re,collections,hashlib,subprocess
import fitz

R=Path(__file__).resolve().parent
D=R/'data'
def load(n):return json.loads((D/n).read_text())

def main():
    matrix=collections.Counter()
    rows=load('openness-records-889.json')
    assert len(rows)==len({r['model_id'] for r in rows})==889
    for r in rows:
        m=re.fullmatch(r'L(\d)O(\d)',r['strict_final_grade']);assert m
        matrix[(int(m[1])>=3,int(m[2])>=2)]+=1
    assert matrix=={(True,True):117,(True,False):58,(False,True):500,(False,False):214}
    high_open=matrix[(True,True)]+matrix[(False,True)]
    assert round(100*117/high_open,1)==19.0
    flow=list(csv.DictReader((D/'country-derivation-flows.csv').open()))
    assert sum(int(r['weight']) for r in flow)==10943
    assert next(int(r['weight']) for r in flow if r['source']=='CN' and r['target']=='US')==4639
    assert round(100*4639/10943,1)==42.4
    for code,out,inc in [('IN',31,162),('BR',3,146),('ID',78,29)]:
        assert sum(int(r['weight']) for r in flow if r['source']==code)==out
        assert sum(int(r['weight']) for r in flow if r['target']==code)==inc
    ranks=list(csv.DictReader((D/'modelrank-country-monthly.csv').open()))
    for k,expected in [('20',[9,8,3,0]),('100',[37,50,7,6])]:
        row=next(r for r in ranks if r['month']=='2026-06' and r['k']==k)
        assert [int(row[x]) for x in ['china','us','other_known','unknown']]==expected
    cities=load('fixed-ten-cities.json')
    assert sum(c['2026'] for c in cities)==3590
    assert round(100*(971+913)/3590,1)==52.5
    assert max(cities,key=lambda x:x['growth_pct'])['city']=='杭州'
    assert max(cities,key=lambda x:x['increase'])['city']=='上海'
    assert round(100*(486/414-1),1)==17.4
    assert 117+58==175 and 117+500==617
    fqa=json.loads((R/'review/figure-qa.json').read_text())
    assert all(not x['out_of_bounds'] and not x['overlaps'] for x in fqa)
    p=R/'output/GOSD_2026_Chapter6_Review_v0.4.pdf'
    doc=fitz.open(p);assert len(doc)==6
    assert all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in doc)
    outside=[];body_collisions=[]
    for i,page in enumerate(doc):
        for b in page.get_text('dict')['blocks']:
            if 'lines' not in b:continue
            for ln in b['lines']:
                r=fitz.Rect(ln['bbox'])
                if r.x0<0 or r.y0<0 or r.x1>page.rect.width or r.y1>page.rect.height:outside.append([i+1,r])
        # Compare real body text lines, excluding outlined figures and within-line spans.
        lines=[ln for b in page.get_text('dict')['blocks'] if 'lines' in b for ln in b['lines']]
        for a,ln in enumerate(lines):
            ra=fitz.Rect(ln['bbox'])
            for other in lines[a+1:]:
                rb=fitz.Rect(other['bbox']);rc=ra&rb
                if not rc.is_empty and rc.width>3 and rc.height>3:
                    body_collisions.append({'page':i+1,'a':''.join(s['text'] for s in ln['spans']),'b':''.join(s['text'] for s in other['spans'])})
    assert not outside,outside
    assert not body_collisions,body_collisions
    txt='\n'.join(p.get_text() for p in doc)
    for stale in ['870 个','870 条','600 条','4-16','4‑16','（更新图）','6.4','附录 A','重点观察什么','何时需要修订','交付与验收','承接','接续','联读']:assert stale not in txt,stale
    for title in ['6.1','十二项关键洞察','十大前瞻','十大战略建议']:assert title in txt,title
    from content import INSIGHTS,OUTLOOKS,RECS
    assert sum(len(p['items']) for p in INSIGHTS)==12
    assert len(OUTLOOKS)==len(RECS)==10
    assert collections.Counter(p['horizon'] for p in OUTLOOKS)=={'近期':6,'中期':3,'2030':1}
    page5=doc[4].get_text();page6=doc[5].get_text()
    compact=lambda t:re.sub(r'\s+','',t)
    title_positions=[];subtitle_positions=[]
    for page,panel in zip(doc,INSIGHTS):
        text=compact(page.get_text())
        assert '6.1十二项关键洞察' in text
        assert compact(panel['group']+panel['theme']) in text
        assert '洞察'+panel['items'][0][0]+'—'+panel['items'][-1][0] in text
        for _,title,body in panel['items']:
            assert compact(title) in text,title
            assert compact(body) in text,title
        title_positions.append(tuple(round(v,2) for v in page.search_for('6.1')[0]))
        subtitle_positions.append(tuple(round(v,2) for v in page.search_for(panel['theme'])[0]))
    assert len(set(title_positions))==1,title_positions
    assert max(p[1] for p in subtitle_positions)-min(p[1] for p in subtitle_positions)<0.1,subtitle_positions
    assert max(p[3] for p in subtitle_positions)-min(p[3] for p in subtitle_positions)<0.1,subtitle_positions
    for item in OUTLOOKS:assert compact(item['title']) in compact(page5),item['title']
    for item in RECS:assert compact(item['title']) in compact(page6),item['title']
    fonts=subprocess.check_output(['pdffonts',str(p)],text=True)
    assert 'NotoSansCJKsc' in fonts and 'NotoSerifCJKsc' in fonts
    assert all('yes' in l for l in fonts.splitlines()[2:])
    log=(R/'output/report.log').read_text()
    assert 'Overfull' not in log and 'Missing character' not in log
    report={'version':'0.4','pages':6,'portrait_a4':True,'embedded_chinese_fonts':True,'pdf_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'numerical_rechecks':['889 unique model IDs and strict-grade 2x2 matrix','country relation totals and three selected country endpoints','June ModelRank seats','fixed ten-city totals and growth maxima'],'structure':{'insight_pages':4,'outlook_pages':1,'strategy_pages':1,'insights':12,'outlooks':10,'recommendations':10,'section_6_4_removed':True,'appendix_removed':True,'consistent_section_title_positions':title_positions,'consistent_theme_vertical_positions':subtitle_positions,'insight_ranges':['01—03','04—06','07—09','10—12']},'figure_text_bounds_and_collisions':fqa,'body_overlaps':body_collisions,'body_outside_page':outside,'visual_review':'Pending final manual inspection of all rendered pages.','note':'Numeric checks establish consistency with frozen inputs, not representativeness or independently validated model openness.'}
    (R/'review/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    (R/'review/fonts.txt').write_text(fonts)
    print(json.dumps({k:report[k] for k in ['version','pages','portrait_a4','embedded_chinese_fonts','pdf_sha256']},ensure_ascii=False))
if __name__=='__main__':main()
