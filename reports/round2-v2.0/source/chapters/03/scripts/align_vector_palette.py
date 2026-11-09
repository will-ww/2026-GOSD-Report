from pathlib import Path
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ContentStream,FloatObject,NameObject
import hashlib,json,io,fitz
R=Path(__file__).resolve().parents[1]
# Specific semantic colors only. Raster logos and all numerical/path/text operators stay unchanged.
M={'#1F5D73':'#514078','#233F4B':'#1B2D40','#233D48':'#1B2D40','#21343C':'#1B2D40','#1C3441':'#1B2D40','#226276':'#514078','#438B92':'#007D78','#358F91':'#007D78','#197D87':'#007D78','#C38C36':'#AD7A22','#C47C48':'#AD4E22','#D65C3E':'#B65A3B','#746AA6':'#6146A5','#786BA2':'#6146A5','#627C87':'#5C6B7A','#657C86':'#5C6B7A','#607780':'#5C6B7A','#EDF3F5':'#F2EFF6','#EDF2F4':'#F2EFF6','#F6F8F8':'#F6F5F8','#F0F5F5':'#F6F5F8','#F0F5F6':'#F6F5F8'}
logs=[]
paths=sorted((R/'figures').glob('*/*.pdf'))+sorted((R/'atlas/figures').glob('*.pdf'))
for p in paths:
 if p.parent.name=='new':continue
 if p.name in ['05_monthly.pdf','06_global_history.pdf','07_china_history.pdf'] and p.parent.name=='32':continue
 original=R/'provenance/original_vectors'/p.relative_to(R);original.parent.mkdir(parents=True,exist_ok=True)
 if not original.exists():original.write_bytes(p.read_bytes())
 data=original.read_bytes();r=PdfReader(io.BytesIO(data));w=PdfWriter();w.clone_document_from_reader(r);count=0
 for page in w.pages:
  c=ContentStream(page.get_contents(),w)
  for args,op in c.operations:
   if op in [b'rg',b'RG'] and len(args)==3:
    col='#'+''.join(f'{round(float(v)*255):02X}' for v in args)
    if col in M:
     new=M[col];args[:]=[FloatObject(int(new[k:k+2],16)/255) for k in [1,3,5]];count+=1
  page[NameObject('/Contents')]=w._add_object(c)
 if count:w.write(p)
 before=fitz.open(stream=data,filetype='pdf');after=fitz.open(p)
 assert all(a.get_text()==b.get_text() and a.rect==b.rect for a,b in zip(before,after)),p
 logs.append({'file':str(p.relative_to(R)),'recolored_commands':count,'text_and_size_preserved':True,'original_sha256':hashlib.sha256(data).hexdigest(),'new_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(R/'review/vector_palette_alignment.json').write_text(json.dumps(logs,indent=2))
print('Vector palette checked',len(logs),'files; no text or geometry changes')
