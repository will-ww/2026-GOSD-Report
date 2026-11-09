"""Build local assets from the approved external 2026 mother report and repo SVG."""
from pathlib import Path
import hashlib
import os
import subprocess
import fitz
from fontTools.ttLib import TTCollection

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
SOURCE_SHA = '675c3490c45d5fc4b51ca0c9ae2ddd5bb330abc108f148435d7317c221579a66'
source = Path(os.environ['GOSD_2026_SOURCE_PDF']).expanduser().resolve()
assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA, 'Mother report SHA mismatch'
out = ROOT / '.build/assets'
out.mkdir(parents=True, exist_ok=True)
# Select Simplified Chinese explicitly; some XeTeX runtimes ignore TTC indices.
font_dir = ROOT / '.build/fonts'
font_dir.mkdir(parents=True, exist_ok=True)
for family in ['Sans', 'Serif']:
    for weight in ['Regular', 'Bold']:
        target = font_dir / f'Noto{family}CJKsc-{weight}.otf'
        if not target.exists():
            collection = TTCollection(f'/usr/share/fonts/opentype/noto/Noto{family}CJK-{weight}.ttc')
            selected = collection.fonts[2]
            assert selected['name'].getDebugName(6) == f'Noto{family}CJKsc-{weight}'
            selected.save(target)
            collection.close()
font_path = '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
font = fitz.Font(fontfile=font_path)
with fitz.open(source) as mother, fitz.open() as doc:
    doc.insert_pdf(mother, from_page=14, to_page=14)
    page = doc[0]
    spans = [s for b in page.get_text('dict')['blocks'] for l in b.get('lines', [])
             for s in l['spans'] if s['text'] == 'OSDGs']
    assert len(spans) == 2
    for s in spans:
        page.add_redact_annot(fitz.Rect(s['bbox']), fill=False)
    page.apply_redactions(images=0, graphics=0, text=0)
    for s in spans:
        x, y = s['origin']; size = s['size']
        if size > 20:
            x = (s['bbox'][0] + s['bbox'][2] - font.text_length('GOSD', fontsize=size)) / 2
        c = s['color']; rgb = ((c >> 16 & 255)/255, (c >> 8 & 255)/255, (c & 255)/255)
        page.insert_text((x, y), 'GOSD', fontname='gosdcover', fontfile=font_path,
                         fontsize=size, color=rgb)
    doc.save(out/'chapter1-cover.pdf', garbage=4, deflate=True)
for name in ['osdgs-symbol-compact', 'osdgs-emblem-display']:
    svg = REPO / f'brand/osdgs/v2.0/assets/master/{name}.svg'
    target = 'osdgs-compact' if name.endswith('compact') else 'osdgs-display'
    subprocess.run(['inkscape', str(svg), '--export-type=pdf',
                    f'--export-filename={out / (target + ".pdf")}'],
                   check=True, capture_output=True)
print('Local cover and approved brand assets prepared.')
