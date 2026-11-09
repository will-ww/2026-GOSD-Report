from pathlib import Path
import re,json
R=Path(__file__).resolve().parents[1];p=R/'atlas/atlas.tex';original=R/'provenance/atlas_original.tex'
if not original.exists():original.write_bytes(p.read_bytes())
s=original.read_text().replace('{1C3441}','{211E3C}').replace('{197D87}','{6146A5}').replace('{657C86}','{5C6B7A}').replace('{EDF3F4}','{F2EFF6}')
s=s.replace('3.4 项目标杆画像：PyTorch与OpenHarmony 全书统稿评审版 v1.0','3.4 完整项目画像：PyTorch与OpenHarmony')
s=s.replace('2026 全球开源发展报告 · 3.4 项目标杆画像 · 全书统稿评审版 v1.0','OSDGs / GOSD 2026 · 完整项目画像')
s=s.replace('来源3.4-S8—3.4-S23及完整口径见章末来源索引。','来源：OpenDigger、GitHub与项目官方材料，逐面板标注。')
s=s.replace('来源3.4-S8、3.4-S9、3.4-S15、3.4-S20、3.4-S21见章末来源索引。','来源：OpenDigger、期末标签与源码清单，逐面板标注。')
s=s.replace('图表为实际数据，无模拟指标；不合成统一健康分。','不合成统一健康分。')
s=s.replace('期后OSV对torch 2.12.1','2026-11-06期后OSV对torch 2.12.1')
s=s.replace('期后对2.12.1的解析','2026-11-06期后对2.12.1的解析')
s=s.replace(r'\usepackage{fontspec,graphicx,xcolor,tabularx,array,booktabs,hyperref,fancyhdr}',r'\usepackage{fontspec,graphicx,xcolor,tabularx,array,booktabs,hyperref,fancyhdr,eso-pic}')
s=s.replace(r'\begin{document}',r'\AddToShipoutPictureBG{\AtPageLowerLeft{\includegraphics[width=\paperwidth]{../figures/new/footer-wave.pdf}}}'+'\n'+r'\begin{document}')
lookup={x['id']:x['urls'][0] for x in json.loads((R/'provenance/source_ledger.json').read_text()) if x['urls']}
def repl(m):
 raw=m[0];sid=re.search(r'3\.4-S\d+',raw)[0]
 return r'\href{'+lookup[sid]+'}{'+raw+'}' if sid in lookup else raw
s=re.sub(r'\[3\.4-S\d+[^]]*\]',repl,s)
p.write_text(s);(R/'atlas/pageoffset.tex').write_text(r'\setcounter{page}{34}'+'\n')
# Match chapter accent; the ten dimension colors remain untouched.
f=R/'design/gosd-book.sty';f.write_text(f.read_text().replace('{C17B3F}','{6146A5}'))
p=R/'build.sh';s=p.read_text();start='for pass in 1 2 3; do xelatex'
if '(cd atlas' not in s:
 s=s.replace(start,'(cd atlas && xelatex -interaction=nonstopmode -halt-on-error atlas.tex > build.log)\n'+start)
p.write_text(s)
