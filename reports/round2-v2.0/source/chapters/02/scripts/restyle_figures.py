from pathlib import Path
import re,json,xml.etree.ElementTree as E,subprocess,concurrent.futures
R=Path(__file__).resolve().parents[1];SOURCE=R/'provenance/baseline'
body=(R/'content/chapter2_body.tex').read_text();files=sorted(set(re.findall(r'\\includegraphics\[[^]]+\]\{(modules/[^}]+)\}',body)))
# These are chart semantic colors, not an assignment of countries to dimensions.
palette={'#193C4E':'#142C49','#168A8D':'#007D78','#49A1A0':'#329A9B','#3E6686':'#155F91','#AF824E':'#9C6A2D','#76698F':'#776195','#57717D':'#506778','#D8E4E7':'#D8E3E9','#F0F6F6':'#F1F6F8'}
records=[]
def convert(path):
 subprocess.run(['inkscape',str(path),'--export-type=pdf','--export-filename='+str(path.with_suffix('.pdf'))],check=True,capture_output=True)
for rel in files:
 src=(SOURCE/rel).with_suffix('.svg');dst=(R/rel).with_suffix('.svg');root=E.parse(src).getroot();original_labels=[]
 for el in root.iter():
  if el.tag.endswith('text'):
   original_labels.append(''.join(el.itertext()))
   el.set('font-family','Liberation Sans, Noto Sans CJK SC')
  for k,v in list(el.attrib.items()):
   if v in palette:el.set(k,palette[v])
 E.register_namespace('','http://www.w3.org/2000/svg');E.ElementTree(root).write(dst,encoding='unicode')
 after=[''.join(e.itertext()) for e in E.parse(dst).getroot().iter() if e.tag.endswith('text')]
 assert original_labels==after
 records.append({'path':rel,'labels_unchanged':True,'label_count':len(after),'minimum_font_pt':round(min([float(e.get('font-size','4'))*72/25.4 for e in root.iter() if e.tag.endswith('text')]),2)})
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(convert,[(R/f).with_suffix('.svg') for f in files]))
(R/'review/chart_restyling_checks.json').write_text(json.dumps({'palette':palette,'figures':records},ensure_ascii=False,indent=2))
print('Vector restyle complete:',len(records),'assets, all labels retained')
