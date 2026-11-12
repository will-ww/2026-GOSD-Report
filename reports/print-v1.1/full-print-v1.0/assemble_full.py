"""Assemble the approved eight print modules without changing their artwork."""
from pathlib import Path
import hashlib, json, re
import fitz

R = Path(__file__).resolve().parent
INPUT = R/'inputs'
OUT = R/'output/pdf'
QA = R/'review'
OUT.mkdir(parents=True, exist_ok=True)
QA.mkdir(exist_ok=True)
DEST = OUT/'GOSD_2026_Essential_Full_Print_v1.0.pdf'
M = 72/25.4
manifest = json.loads((QA/'module-manifest.json').read_text())
sources = []
for m in manifest:
    path = INPUT/Path(m['file']).name
    assert path.is_file(), path
    doc = fitz.open(path)
    assert len(doc) == m['pages']
    sources.append((m, path, doc))

d = fitz.open()
toc = []
mapping = []
expected_links = []
blank_pages = []
for m, path, doc in sources:
    offset = len(d)
    d.insert_pdf(doc)
    if m['module'] == 1:
        toc.append([1, '封面与前置内容', 1])
    for level, title, page in doc.get_toc():
        title = title.replace(r'\u3000', '　')
        # The source appendix has both a grouped and a separate Chinese thanks entry.
        if m['module'] == 8 and title == '致谢　中英文致谢':
            continue
        toc.append([level + (1 if m['module'] == 1 else 0), title, page+offset])
    for i, p in enumerate(doc):
        mapping.append(dict(module=m['module'], local_page=i+1, physical_page=offset+i+1,
                            folio=p.get_label(), source=path.name))
        for link in p.get_links():
            item = dict(source_page=offset+i, rect=list(link['from']), kind=link['kind'])
            if link['kind'] == fitz.LINK_GOTO:
                item['target_page'] = offset+link['page']
            elif link['kind'] == fitz.LINK_URI:
                item['uri'] = link.get('uri')
            expected_links.append(item)
    blank_pages.extend(offset+i for i in m['blank_pages'])
    m.update(source_file=path.name, source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
             physical_start=offset+1, physical_end=len(d))
assert len(d) == 138 and len(blank_pages) == 16
d.set_toc(toc, collapse=1)
# Use one continuous body numbering range, preceded by the approved Roman front matter.
# ASCII cover labels avoid a source producer's hex-encoded UTF-8 label prefixes.
d.set_page_labels([dict(startpage=0, prefix='Cover', style=''),
                   dict(startpage=1, prefix='Inside cover', style=''),
                   dict(startpage=2, prefix='', style='r', firstpagenum=1),
                   dict(startpage=18, prefix='', style='D', firstpagenum=1)])

added_links = []
def goto(page_index, rect, target, label):
    assert 0 <= target < len(d)
    d[page_index].insert_link(dict(kind=fitz.LINK_GOTO, **{'from':rect}, page=target, to=fitz.Point(0,0)))
    added_links.append(dict(page=page_index+1, target=target+1, label=label, rect=list(rect)))

# The printed table of contents already has the final folios. Add full-document targets.
chapter_folios = [1,13,35,59,75,89]
chapter_titles = ['从开放协作到公共价值','全球开源生态地图','全球开源影响力排行榜',
                  '全球开源技术全景洞察','全球开源大模型发展洞察','关键洞察、前瞻与战略建议']
for title, folio in zip(chapter_titles, chapter_folios):
    hits = d[8].search_for(title)
    assert len(hits) == 1, (title, hits)
    y = hits[0].y0
    goto(8, fitz.Rect(14*M,y-5,133*M,y+35),17+folio,title)
for title, folio in [('附录',97),('致谢',117)]:
    hits = [x for x in d[8].search_for(title) if x.x0 < 200 and x.y0 > 740]
    assert len(hits) == 1
    y=hits[0].y0
    goto(8,fitz.Rect(14*M,y-3,133*M,y+14),17+folio,title)

# Reading-path phrases and six chapter cards use the same final target mapping.
for title, target in [('执行摘要',10),('第一章',18),('第二章',30),('第三章',52),
                      ('第四章',76),('第五章',92),('第六章',106),('附录',114)]:
    for rect in d[8].search_for(title):
        if rect.x0 > 400:
            goto(8, rect+(-2,-2,2,2), target, '阅读路径：'+title)
for i, folio in enumerate(chapter_folios):
    x = 14 if i < 3 else 141
    y = 111 + (i%3)*39
    goto(12, fitz.Rect(x*M,y*M,(x+55)*M,(y+34)*M),17+folio,'结构图：第'+str(i+1)+'章')

d.set_metadata(dict(title='2026 全球开源发展报告｜精要版｜全文打印版 v1.0',
    author='全球开源发展报告编制组',
    subject='2026年11月11日八模块合稿；A4双面打印；含装订留白和空白页',
    keywords='GOSD 2026,精要版,全球开源发展报告,人工智能,全文打印版',
    creator='XeLaTeX / PyMuPDF', producer='GOSD approved-module print assembly v1.0'))
catalog=d.pdf_catalog()
d.xref_set_key(catalog,'PageLayout','/TwoPageRight')
d.xref_set_key(catalog,'PageMode','/UseOutlines')
d.xref_set_key(catalog,'ViewerPreferences','<< /PrintScaling /None /Duplex /DuplexFlipLongEdge /DisplayDocTitle true >>')
d.save(DEST,garbage=4,deflate=True)
d.close()

merged=fitz.open(DEST)
checks=[]
def check(name, ok, details=None):
    checks.append(dict(check=name, passed=bool(ok), details=details))
    assert ok,(name,details)
check('138 pages',len(merged)==138)
check('Bookmarks retained and redirected',merged.get_toc()==toc)
check('Roman front matter', [merged[i].get_label() for i in range(2,18)] == ['i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii','xiv','xv','xvi'])
check('Continuous 1–120 body folios',[merged[i].get_label() for i in range(18,138)]==list(map(str,range(1,121))))
offset=0
for m,path,doc in sources:
    for i,p in enumerate(doc):
        q=merged[offset+i]
        check(f'P{offset+i+1}: source text retained',q.get_text()==p.get_text())
        check(f'P{offset+i+1}: source artwork retained',
              q.get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False).samples ==
              p.get_pixmap(matrix=fitz.Matrix(.6,.6),alpha=False).samples)
        check(f'P{offset+i+1}: A4 portrait', abs(q.rect.width-210*M)<.1 and abs(q.rect.height-297*M)<.1)
        for link in q.get_links():
            if link['kind']==fitz.LINK_GOTO:
                check(f'P{offset+i+1}: internal link target valid', 0<=link['page']<138)
    print(f'Module {m["module"]}: {len(doc)} pages preserved',flush=True)
    offset+=len(doc)
for physical in blank_pages:
    p=merged[physical-1]
    check(f'P{physical}: intentional blank',not p.get_text().strip() and not p.get_images() and not p.get_drawings())
for m,_,_ in sources[1:]:
    check(f'Module {m["module"]}: recto opening',m['physical_start']%2==1)
font_refs=set()
for page in merged:
    font_refs.update(f[0] for f in page.get_fonts(full=True))
for ref in sorted(font_refs):
    name,extension,kind,data=merged.extract_font(ref)
    check('Embedded font: '+name,bool(data) or kind=='Type3')
for expected in expected_links:
    links=merged[expected['source_page']].get_links()
    found=[x for x in links if x['kind']==expected['kind'] and
           max(abs(a-b) for a,b in zip(x['from'],expected['rect']))<.1]
    if expected['kind']==fitz.LINK_GOTO:
        check('Retained internal destination',any(x['page']==expected['target_page'] for x in found),expected)
    elif expected['kind']==fitz.LINK_URI:
        check('Retained external destination',any(x.get('uri')==expected['uri'] for x in found),expected)
for link in added_links:
    check('Full-book navigation: '+link['label'],any(x['kind']==fitz.LINK_GOTO and x['page']==link['target']-1 and
          max(abs(a-b) for a,b in zip(x['from'],link['rect']))<.1 for x in merged[link['page']-1].get_links()))
check('Repaired folio 80 retained',len(merged[97].get_xobjects())<100 and '5,777' in merged[97].get_text())
check('Clean GOSD back cover',set(x.strip() for x in merged[-1].get_text().splitlines() if x.strip())==
      {'GOSD','共同创造','开放的智能未来','OPEN SOURCE, A SHARED INTELLIGENT FUTURE'})

result=dict(version='1.0',date='2026-11-11',file=str(DEST),size_bytes=DEST.stat().st_size,
    sha256=hashlib.sha256(DEST.read_bytes()).hexdigest(),pages=len(merged),
    intentionally_blank_physical_pages=blank_pages,embedded_font_resources=len(font_refs),
    bookmarks=len(toc),new_full_book_links=len(added_links),checks=checks,
    modules=manifest,page_map=mapping,added_links=added_links,
    evidence='Approved module PDFs, current versions as listed in modules; no statistical recomputation.')
(QA/'full-print-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({k:result[k] for k in ['version','file','size_bytes','pages','intentionally_blank_physical_pages','embedded_font_resources','bookmarks','new_full_book_links']},ensure_ascii=False))
print('Passed checks:',len(checks),flush=True)
