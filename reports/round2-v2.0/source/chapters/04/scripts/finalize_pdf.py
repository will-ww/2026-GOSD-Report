"""Restore item links after SVG/PDF inclusion and add portrait-atlas folios."""
from pathlib import Path
import fitz, json, re

R = Path(__file__).resolve().parents[1]
doc = fitz.open(R / 'work/report.pdf')
geometry = json.loads((R / 'review/atlas_geometry.json').read_text())
layouts = json.loads((R / 'review/atlas_layout.json').read_text())
page_map = {}
for layout in layouts:
    fig = layout['figure']
    matches = [i for i, p in enumerate(doc)
               if p.rect.width > 800 and re.search(rf'图\s*4\s*-\s*{fig}\b', p.get_text())]
    assert len(matches) == 1, (layout, matches)
    page_map[layout['key']] = matches[0]
    p = doc[matches[0]]
    assert p.rect.width < p.rect.height
    p.insert_font(fontname='folio', fontfile='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf')
    p.insert_textbox(fitz.Rect(270*72/25.4, 413*72/25.4, 281*72/25.4, 419*72/25.4),
                    str(matches[0]+1), fontsize=9, fontname='folio', align=2,
                    color=(.08,.17,.29))
for row in geometry:
    p = doc[page_map[row['key']]]
    rect = fitz.Rect([v*72/25.4 for v in row['bbox_mm']])
    assert p.rect.contains(rect), row
    p.insert_link({'kind': fitz.LINK_URI, 'from': rect, 'uri': row['url']})
source_urls = {
    '41a':'https://github.com/antgroup/agentic-ai-landscape/tree/e330d75ea4ca314bc81f6868df63425c8acca5e3',
    '41b':'https://github.com/antgroup/agentic-ai-landscape/tree/e330d75ea4ca314bc81f6868df63425c8acca5e3',
    '42':'https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/tree/c51e3441361407b68f10b339d97eff288319b503/data/processed/chapter4',
    '43':'https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/tree/c51e3441361407b68f10b339d97eff288319b503/data/processed/chapter4',
    '44':'https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/c51e3441361407b68f10b339d97eff288319b503/data/processed/chapter4/fig-4-4-1_database_landscape.csv',
    '45':'https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/d43b14a3850fffa6589b2ebe64bc257a0734ad6a/data/processed/chapter4/fig-4-5-1_riscv_landscape.csv',
    '46':'https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/c51e3441361407b68f10b339d97eff288319b503/data/processed/chapter4/fig-4-6-1_pytorch_landscape.csv',
}
for key, url in source_urls.items():
    doc[page_map[key]].insert_link({'kind':fitz.LINK_URI, 'from':fitz.Rect(16*72/25.4,396*72/25.4,281*72/25.4,401*72/25.4),'uri':url})
metadata = doc.metadata
metadata.update(title='2026全球开源发展报告｜第四章清洁整理评审稿 v0.1', author='GOSD编制组',
                subject='动态星座视觉体系v2.0.0；主统计期2025-07-01至2026-06-30；评审稿，尚未公开发布',
                keywords='GOSD 2026, 第四章, 竖向全景, 评审稿 v0.1')
doc.set_metadata(metadata)
out = R / 'output/GOSD_2026_第四章_清洁整理_v0.1_评审稿.pdf'
doc.save(out, garbage=4, deflate=True)
doc.close()
with fitz.open(out) as saved:
    result={'pages':len(saved),'map_pages':{k:v+1 for k,v in page_map.items()},'item_links':len(geometry),'source_links_added':len(source_urls),'all_portrait':all(p.rect.width<p.rect.height for p in saved),'total_links':sum(len(p.get_links()) for p in saved)}
    assert result['pages']==21 and result['all_portrait']
    for layout in layouts:
        page=saved[page_map[layout['key']]]
        assert len(page.get_links())==layout['records']+1, (layout['key'],len(page.get_links()))
(R/'review/pdf_link_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False))
