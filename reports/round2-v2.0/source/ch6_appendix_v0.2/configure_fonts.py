"""Extract SC font faces from locally installed TTCs for XeLaTeX.
The cache is generated locally, ignored by git, and MUST NOT be distributed.
"""
from pathlib import Path
import subprocess
from fontTools.ttLib import TTFont
ROOT=Path(__file__).resolve().parent
out=ROOT/'.build_fonts';out.mkdir(exist_ok=True)
for family,prefix in [('Noto Sans CJK SC','NotoSansSC'),('Noto Serif CJK SC','NotoSerifSC')]:
 for weight in ['Regular','Bold']:
  pattern=family+(':style=Bold' if weight=='Bold' else ':style=Regular')
  raw=subprocess.check_output(['fc-match','-f','%{file}|%{index}',pattern],text=True).strip()
  src,idx=raw.split('|'); target=out/f'{prefix}-{weight}.otf'
  if not target.exists():
   font=TTFont(src,fontNumber=int(idx));font.save(target)
  print('Prepared local font face:',family,weight)
