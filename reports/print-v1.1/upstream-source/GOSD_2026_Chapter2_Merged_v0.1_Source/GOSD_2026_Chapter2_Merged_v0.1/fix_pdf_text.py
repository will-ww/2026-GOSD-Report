"""Repair Cairo's missing ToUnicode entries without altering rendered glyphs.

The mappings below have been checked against the corresponding editable SVG
labels. CJK radical compatibility characters are normalized to searchable Han
characters. No PDF drawing operators, positions, outlines or values are changed.
"""
from pathlib import Path
import fitz,re,unicodedata,json
FIX={
 'fig-2-10':{'003b':'1'}, # 1Panel
 'fig-2-13':{'001a':'2','0061':'0','0062':'5','0064':'6'}, # 2025 Q2 -> 2026 Q2
 'fig-2-14':{'0014':'2','001b':'0','001c':'5','0020':'3'}, # 2025 Q2, +22.3%
 'fig-2-15':{'003c':'1'}, # DeepSeek-R1
 'fig-2-17':{'0055':'3','0056':'7','0057':'6','0058':'1','0059':'5','005a':'4'}, # cohort n
 'fig-2-18':{'006d':'1','006e':'0'}, # n < 100
}
def repair(path):
 path=Path(path);doc=fitz.open(path);count=0
 for font in doc[0].get_fonts():
  typ,v=doc.xref_get_key(font[0],'ToUnicode')
  if typ!='xref':continue
  xref=int(v.split()[0]);src=doc.xref_stream(xref).decode()
  def sub(m):
   nonlocal count
   cid,u=m.groups();val=int(u,16)
   if val==0xfffd:
    assert cid in FIX.get(path.stem,{}),(path.stem,cid)
    replacement=FIX[path.stem][cid];count+=1
   elif 0x2f00<=val<=0x2fdf:
    replacement=unicodedata.normalize('NFKC',chr(val));count+=1
   else:return m.group(0)
   return f'<{cid}> <{replacement.encode("utf-16-be").hex()}>'
  dst=re.sub(r'<([0-9a-f]{4})> <([0-9a-f]{4})>',sub,src)
  if dst!=src:doc.update_stream(xref,dst.encode())
 tmp=path.with_suffix('.fixed.pdf');doc.save(tmp,garbage=4,deflate=True);doc.close();tmp.replace(path)
 return {'file':path.name,'unicode_entries_repaired':count}
