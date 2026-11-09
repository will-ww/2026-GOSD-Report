"""Create a complete reader-facing Markdown counterpart from the edited JSON and LaTeX framing."""
from pathlib import Path
import re,json,subprocess
R=Path(__file__).resolve().parents[1]
t=(R/'chapter2.tex').read_text();bib=json.loads((R/'references/references.json').read_text());bn={x['id']:i+1 for i,x in enumerate(bib)}
km=json.loads((R/'review/reference_key_map.json').read_text());fm=json.loads((R/'review/figure_register.json').read_text())
labelnums={x['label']:x['number'] for x in fm}
# Standardize tables and inline macros before asking Pandoc to read the framing fragments.
def transform(fragment):
 def table(m):
  body=m[1];body=re.sub(r'\\addlinespace(?:\[[^\]]*\])?','',body);body=body.replace(r'\midrule','')
  rows=[r.strip() for r in body.split(r'\\') if r.strip()]
  parsed=[]
  for row in rows:
   row=re.sub(r'\\hyperref\[([^\]]+)\]\{\\pageref\{[^}]+\}\}',lambda q:'§'+q[1][-2]+'.'+q[1][-1],row)
   parsed.append([c.strip() for c in row.split('&')])
  # Plain Markdown tables survive Pandoc as verbatim raw TeX via separate marker replacement later.
  idx=len(tables);tables.append(parsed)
  return '\nTABLEPLACEHOLDER'+str(idx)+'END\n'
 tables=[]
 fragment=re.sub(r'\\begin\{tabularx\}.*?\\toprule(.*?)\\bottomrule\s*\\end\{tabularx\}',table,fragment,flags=re.S)
 fragment=re.sub(r'\\cite\{([^}]+)\}',lambda m:''.join('['+str(bn.get(k,'?'))+']' for k in m[1].split(',')),fragment)
 for a,b in [('key','textbf'),('topic','subsubsection*'),('lead','textit'),('src','textit'),('eyebrow','textbf')]:fragment=fragment.replace('\\'+a+'{','\\'+b+'{')
 fragment=re.sub(r'\\pdfbookmark\[\d+\]\{[^}]+\}\{[^}]+\}','',fragment)
 fragment=re.sub(r'\\renewcommand\{\\CurrentSection\}\{[^}]+\}','',fragment)
 fragment=re.sub(r'\\label\{[^}]+\}','',fragment)
 fragment=re.sub(r'\\(?:vspace|fontsize|setlength|renewcommand)(?:\*?)(?:\{[^}]*\}){1,3}','',fragment)
 fragment=re.sub(r'\\(?:noindent|par|selectfont|begingroup|endgroup|clearpage|vfill|sffamily|bfseries)\b','',fragment)
 fragment=re.sub(r'\\color\{[^}]+\}','',fragment)
 out=subprocess.run(['pandoc','--from=latex','--to=gfm','--wrap=none'],input=fragment,text=True,capture_output=True,check=True).stdout
 def plain(s):
  s=s.replace(r'\%', '%').replace(r'\&','&').replace(r'\_','_')
  s=re.sub(r'\\(?:key|textbf)\{([^}]+)\}',r'**\1**',s)
  s=re.sub(r'\\[a-zA-Z]+\s*','',s);return s
 for i,rows in enumerate(tables):
  # First navigation table has no header in the PDF, so supply one in Markdown.
  if len(rows[0])==4 and rows[0][0]=='2.1':rows=[['小节','主题','阅读问题','定位']]+rows
  lines=['| '+' | '.join(plain(c) for c in row)+' |' for row in rows]
  lines.insert(1,'| '+' | '.join('---' for _ in rows[0])+' |')
  out=out.replace('TABLEPLACEHOLDER'+str(i)+'END','\n'.join(lines))
 return out
front=t.split(r'\begin{document}',1)[1].split(r'\renewcommand{\CurrentSection}{2.1',1)[0]
back=t.split(r'\pdfbookmark[1]{本章小结：从观察差异到识别支持需求}{conclusions}',1)[1].split(r'\pdfbookmark[1]{参考资料}',1)[0]
frontmd=transform(front);backmd=transform(back)
(R/'sections/chapter_front.md').write_text(frontmd)
(R/'sections/chapter_back.md').write_text(backmd)
(R/'methods/方法与证据边界.md').write_text(backmd.split('## 资料与方法：',1)[-1])
md=['# 第二章 全球开源生态观测地图（GOSO）\n\n整章评审稿 v1.0.0 · 2026-11-05 · 待作者评审\n',frontmd]
for s in range(21,28):
 o=json.loads((R/'sections'/f'{s}.json').read_text())
 def conv(text):
  text=re.sub(r'\[\[([^\]]+)\]\]',lambda m:'['+str(bn[km[str(s)+':'+m[1]]])+']',text)
  return re.sub(r'<<([^>]+)>>',lambda m:labelnums[f's{s}-'+m[1].replace(':','-')],text)
 for pg in o['pages']:
  md.append('## '+pg['title']+'\n')
  if pg.get('subtitle'):md.append('*'+pg['subtitle']+'*\n')
  for b in pg['blocks']:
   typ=b['type']
   if typ in ['p','heading','note']:
    st=conv(b['text']);md.append(('### ' if typ=='heading' else '')+st+'\n')
   elif typ in ['group','figure']:
    cap=f"图 {labelnums[f's{s}-'+b['label'].replace(':','-')]} {b['caption']}"
    for a in b.get('assets',[b.get('asset')]):md.append(f'![{cap}](figures/{s}/{a}.svg)\n')
    md.append('**'+cap+'**\n')
    if b.get('source'):md.append(conv(b['source'])+'\n')
   elif typ=='asset':md.append(f'![](figures/{s}/{b["asset"]}.svg)\n')
   elif typ=='insight':md.append('**'+b['title']+'** '+conv(b['text'])+'\n')
md.extend([backmd,'## 参考资料\n'])
for b in bib:md.append(f'[{bn[b["id"]]}] {b["print_title"]} [来源入口]({b["url"]})\n')
(R/'chapter2.md').write_text('\n'.join(md))
print('Complete Markdown:',len((R/'chapter2.md').read_text()),'characters')
