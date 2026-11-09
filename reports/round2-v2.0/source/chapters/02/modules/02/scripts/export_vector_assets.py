"""Regenerate all currently used vector PDFs from the reviewed editable SVGs."""
from pathlib import Path
import json
import cairosvg
R=Path(__file__).resolve().parents[1]
count=0
for section in range(21,28):
 o=json.loads((R/'sections'/f'{section}.json').read_text())
 assets=set()
 for p in o['pages']:
  for b in p['blocks']:
   if b['type'] in ['figure','group']:assets.update(b.get('assets',[b.get('asset')]))
   elif b['type']=='asset':assets.add(b['asset'])
 for name in sorted(assets):
  src=R/'figures'/str(section)/f'{name}.svg'
  if not src.is_file():raise FileNotFoundError(src)
  cairosvg.svg2pdf(url=str(src),write_to=str(src.with_suffix('.pdf')));count+=1
print('Exported SVG to vector PDF:',count,'assets')
