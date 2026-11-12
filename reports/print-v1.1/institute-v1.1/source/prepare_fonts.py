"""Extract the SC faces of installed open-source Noto CJK collections."""
from pathlib import Path
import subprocess
from fontTools.ttLib import TTFont,TTCollection
R=Path(__file__).resolve().parent
(R/'fonts').mkdir(exist_ok=True)
for family,prefix in [('Noto Sans CJK SC','NotoSansCJKsc'),('Noto Serif CJK SC','NotoSerifCJKsc')]:
 for style in ['Regular','Bold']:
  out=R/'fonts'/f'{prefix}-{style}.otf'
  if out.exists():continue
  p=Path(subprocess.check_output(['fc-match','-f','%{file}',f'{family}:style={style}'],text=True).strip())
  if p.suffix.lower()=='.ttc':
   coll=TTCollection(p)
   matches=[f for f in coll.fonts if f['name'].getDebugName(6)==f'{prefix}-{style}']
   if not matches:raise RuntimeError(f'Expected {prefix}-{style} in {p}')
   matches[0].save(out)
  else:
   f=TTFont(p)
   if f['name'].getDebugName(6)!=f'{prefix}-{style}':raise RuntimeError(f'Install {family} {style}')
   f.save(out)
print('Noto SC fonts ready.')
