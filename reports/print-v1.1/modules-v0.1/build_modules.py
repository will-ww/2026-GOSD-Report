"""Eight duplex-print review modules, preserving approved vector page bodies."""
from pathlib import Path
import json,re,os,subprocess,hashlib,shutil,math
import fitz
from PIL import Image
from print_config import *

M=72/25.4
MASTER=R/'master'; OUT=R/'output/pdf'; REVIEW=R/'review'
for p in [MASTER,OUT,REVIEW,MASTER/'prepared',MASTER/'output']:p.mkdir(parents=True,exist_ok=True)
FONTDIR=(R.parent/'front-v0.8/fonts').resolve()
FONTFILES={k:FONTDIR/v for k,v in {'sans':'NotoSansCJKsc-Regular.otf','sansb':'NotoSansCJKsc-Bold.otf','serif':'NotoSerifCJKsc-Regular.otf','serifb':'NotoSerifCJKsc-Bold.otf'}.items()}
FONTS={k:fitz.Font(fontfile=str(v)) for k,v in FONTFILES.items()}
PATCHES=[]; TEXT_OVERLAYS={}; BOXES=[]; SEQ=0; TEX_PAGES=[]; SPECS=[]
TOKENS=json.loads((R.parent/'front-v0.8/data/brand_tokens.json').read_text())

def norm(s):return re.sub(r'\s+','',s).replace('⸺','——')
def esc(s):return str(s).replace('\\',r'\textbackslash{}').replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#').replace('\n',r'\\ ')
def txt(x,y,w,t,fs=10.5,ld=16.8,c='ink',bold=False,serif=False,align='',mh=None,center=False):
 global SEQ
 SEQ+=1;bid=f'b{SEQ}'
 BOXES.append(dict(id=bid,page=len(TEX_PAGES)+1,x=x,y=y,w=w,max_height=mh,text=t,center=center))
 f=(r'\rmfamily ' if serif else r'\sffamily ')+(r'\bfseries ' if bold else '')+rf'\fontsize{{{fs}}}{{{ld}}}\selectfont\color{{{c}}}'+align+esc(t)
 return '\\'+('CenterBox' if center else 'Box')+rf'{{{bid}}}{{{x}}}{{{y}}}{{{w}}}{{{f}}}'+'\n'
def image(x,y,w,path,h=None):return rf'\node[anchor=north west,inner sep=0pt] at \Pos{{{x}}}{{{y}}}{{\includegraphics[width={w}mm'+(f',height={h}mm' if h else '')+rf']{{{path}}}}};'+'\n'
def rect(x,y,w,h,c):return rf'\Rect{{{x}}}{{{y}}}{{{w}}}{{{h}}}{{{c}}}'+'\n'
def rule(x,y,xx,c='line'):return rf'\Rule{{{x}}}{{{y}}}{{{xx}}}{{{c}}}'+'\n'
def emblem(x,y,w):return image(x,y,w,'assets/osdgs-symbol-display.pdf')+txt(x,y+w/2,w,'GOSD',w*.42,w*.48,'navy',True,True,r'\centering\wordmark ',center=True)
def logo(x,cy,w,name):
 im=Image.open(MASTER/'assets'/name);a,b,c,d=im.getbbox();iw,ih=im.size;y=cy-w*(d-b)/(c-a)/2
 return rf'\node[anchor=north west,inner sep=0pt] at \Pos{{{x}}}{{{y}}}{{\includegraphics[width={w}mm,trim={a}bp {ih-d}bp {iw-c}bp {b}bp,clip]{{assets/{name}}}}};'+'\n'
def start():return '\\begin{canvas}\n'
def end(s):
 TEX_PAGES.append(s+'\\end{canvas}\n');return len(TEX_PAGES)-1
def header(folio,idx):
 c=COLORS[idx] if idx<6 else 'navy';left=19 if folio%2 else 11;right=left+180
 label=('第'+'一二三四五六'[idx]+'章 · '+SHORT[idx]) if idx<6 else '附录 · 指标、方法与数据来源'
 s=image(left,8,7.2,'assets/osdgs-symbol-compact.pdf')
 s+=txt(left+10,10.2,98,'GOSD 2026  全球开源发展报告 · 精要版',7.5,10.5,'muted',mh=6)
 s+=txt(left+105,10.2,75,label,7.3,10.5,'muted',False,False,r'\raggedleft ',mh=6)
 s+=rule(left,21,right,'line')+rect(left,20.55,12,.9,c)
 for i,d in enumerate(TOKENS['dimensions']):
  name='brand'+str(i);s+=rf'\definecolor{{{name}}}{{HTML}}{{{d["hero_color"][1:]}}}'+rect(right-58+i*5.9,20.75,4.8,.5,name)
 return s
def footer(folio,idx,cover=False):
 left=19 if folio%2 else 11;right=left+180
 s=rule(left,284,right,'line')
 s+=txt(left,287,145,'GOSD 2026  ·  全球开源发展报告',7.4,10.5,'muted',mh=5)
 s+=txt(right-15,286.2,15,str(folio),10.5,13.5,'navy',True,False,r'\raggedleft ',mh=7)
 return s

def cover(idx):
 folio=STARTS[idx];color=COLORS[idx] if idx<6 else 'navy'
 title=TITLES[idx] if idx<6 else '附录与致谢';en=EN[idx] if idx<6 else 'Methods, Evidence & Acknowledgements'
 s=start()+image(0,0,210,'assets/inner-background.png',297)
 s+=txt(18,8.3,25,'GOSD',12.4,15,'navy',True,True)+txt(48,9.7,145,'2026 全球开源发展报告 · 精要版',8,11,'navy')+rule(18,18,196)
 s+=emblem(17,27,30)
 kicker='第'+'一二三四五六'[idx]+'章 / CHAPTER '+str(idx+1).zfill(2) if idx<6 else '附录 / APPENDIX'
 s+=txt(56,27.5,140,kicker,10,14,color,True,mh=8)
 s+=txt(55,38,142,title,24 if idx in [1,2,3,4] else 23,32,'navy',True,True,mh=18)
 s+=txt(56,54,140,en,9.7,13.5,'navy',False,True,mh=8)
 s+=rect(56,64,28,.85,color)
 s+=txt(19,83,177,SUBTITLE[idx],14.2,20.8,color,True,True,mh=12)
 s+=txt(19,99,177,'\n'.join(INTRO[idx]),10.1,16.2,'ink',False,True,mh=35)
 rows=SUBS[idx]
 if len(rows)==6:top=141;h=18.5
 elif idx==0:top=154;h=31
 elif idx==5:top=168;h=28
 elif idx==6:top=140;h=23
 else:top=143;h=32
 if idx==5:
  for j,t in enumerate(['A 全球协作与体系能力','B 中国模型开源与全球协作','C 全球南方与公共能力','D 中国产业、人才与城市结构']):
   x=19+(j%2)*91;y=135+(j//2)*13
   s+=rect(x,y,86,10,color+'!7')+txt(x+3,y+2,80,t,9.3,13,color,True,mh=7)
 else:s+=txt(19,top-12,177,'本章阅读路径' if idx<6 else '查阅路径',11.2,16,color,True,mh=8)
 for j,(n,t,desc,a,b) in enumerate(rows):
  y=top+j*h
  if j%2==0:s+=rect(19,y-1,177,h-1,'white')
  s+=rect(19,y+1,1.05,h-5,color)
  s+=txt(23,y+2,15,n,10.2 if idx<6 else 9.5,14.7,color,True,mh=8)
  s+=txt(41,y+2,130,t,11.2,16,'navy',True,mh=9)
  s+=txt(41,y+9.7,134,desc,9.0,13.2,'muted',mh=9)
  pages=str(a) if a==b else f'{a}—{b}'
  s+=txt(176,y+4.3,16,pages,9.2,13,'navy',True,False,r'\raggedleft ',mh=8)
  s+=rule(23,y+h-2,195,'line')
 note_y=260 if idx in [0,1,2,3,5,6] else 251
 note=NOTES[idx]
 if idx==6:note='先查基础指标，再核对专题样本。方法说明与各幅图的来源、时间和限制共同决定数字可以怎样解释。'
 s+=txt(19,note_y,177,note,9.3,14.2,'ink',False,True,mh=21)
 s+=footer(folio,idx,True)
 return end(s)

def replace(page,old,new,tag):
 matches=page.search_for(old)
 if not matches:return 0
 # XeTeX can split one search hit around Latin glyphs. Treat adjacent pieces
 # on the same baseline as a single replacement, avoiding duplicate overlays.
 merged=[]
 for rr in sorted(matches,key=lambda r:(round(r.y0,1),r.x0)):
  if merged and abs(merged[-1].y0-rr.y0)<.6 and abs(merged[-1].y1-rr.y1)<.6 and -.2<=rr.x0-merged[-1].x1<=max(6,rr.height*.75):
   merged[-1]=merged[-1]|rr
  else:merged.append(fitz.Rect(rr))
 matches=merged
 spans=[s for b in page.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
 pending=[]
 for rr in matches:
  candidates=[s for s in spans if (fitz.Rect(s['bbox'])&rr).get_area()>0]
  if not candidates:continue
  sp=max(candidates,key=lambda s:(fitz.Rect(s['bbox'])&rr).get_area())
  key=('sans' if 'Sans' in sp['font'] else 'serif')+('b' if 'Bold' in sp['font'] else '')
  fs=sp['size'];width=FONTS[key].text_length(new,fontsize=fs) if new else 0
  available=195*M-rr.x0 if 'appendix-title' in tag else rr.width
  if width>available:fs*=available/width
  col=sp.get('color',0);rgb=((col>>16&255)/255,(col>>8&255)/255,(col&255)/255)
  # Tighten the redaction to the matched text only, preserving adjacent glyphs.
  cut=fitz.Rect(rr.x0+.03,rr.y0+.08,rr.x1-.03,rr.y1-.08)
  page.add_redact_annot(cut,fill=(1,1,1),cross_out=False)
  pending.append((rr.x0,sp['origin'][1],key,fs,rgb,new))
 page.apply_redactions(images=0,graphics=0,text=0)
 for x,y,key,fs,rgb,t in pending:
  if t:
   # Keep all new Chinese text in the XeLaTeX layer; do not resubset source CFF fonts.
   sourcekey=tag.split('-')[0]
   TEXT_OVERLAYS.setdefault((sourcekey,page.number),[]).append(dict(x=x,y=y,key=key,fs=fs,rgb=rgb,text=t))
 PATCHES.append(dict(tag=tag,page=page.number+1,old=old,new=new,count=len(pending)))
 return len(pending)

def prepare_sources():
 paths={}
 for name in ['chapter1','chapter2','chapter3','chapter4','chapter5','chapter6','appendix','figure5-1']:
  doc=fitz.open(R/'inputs'/f'{name}.pdf')
  if name=='chapter1':
   for p in list(doc)[14:23]:replace(p,'附录A','附录',name)
  if name=='chapter2':
   for p in list(doc)[:21]:
    for a,b in [('附录A2—A3','附录10—11'),('附录A1','附录9'),('附录A2','附录10'),('附录A3','附录11'),('附录A4','附录12'),('附录A5','附录13'),('附录A','附录')]:replace(p,a,b,name)
   titles=['9　生态地图：指标与统计覆盖','10　生态地图：历史与情景方法','11　生态地图：贡献与影响情景','12　生态地图：样本与资产口径','13　生态地图：行业专题方法']
   oldtitles=['附录A｜指标与统计覆盖','附录A｜历史与情景方法','附录A｜贡献与影响情景读数','附录A｜样本与资产口径','附录A｜行业专题方法']
   for idx,t,ot in zip(range(21,26),titles,oldtitles):
    p=doc[idx]
    replace(p,ot,t,name+'-appendix-title')
    for j in range(1,7):replace(p,f'A{idx-20}.{j}',f'{idx-12}.{j}',name+'-appendix-label')
   replace(doc[21],'具体限制见A4','具体限制见12',name+'-appendix-reference')
   replace(doc[23],'每行的历史首末值与A2 算法足以复算端点','由各行历史首末值与第10节方法复算端点',name+'-appendix-reference')
  if name in ['chapter3','chapter4']:
   for p in list(doc)[:22 if name=='chapter3' else 13]:replace(p,'附录A','附录',name)
  if name=='chapter3':
   replace(doc[23],'附录A　对象边界与核验范围','14　排行榜：对象边界与核验范围',name+'-appendix-title')
   for j in range(1,9):replace(doc[23],f'A2.{j}',f'14.{j}',name+'-appendix-label')
  if name=='chapter4':
   replace(doc[13],'附录A　样本、指标与时间','15　技术全景：样本、指标与时间',name+'-appendix-title')
   replace(doc[14],'附录A　地域口径与主要来源','16　技术全景：地域口径与来源',name+'-appendix-title')
  if name=='chapter5':
   for p in doc:
    for n in range(1,11):replace(p,'［'+str(n)+'］','',name+'-source-mark')
    replace(p,'附录A1—A2','附录17',name)
  # Remove production hand-offs from the clean reading edition.
  cleanup={'chapter2':(20,['以下由本章证据引出的建议','下一步：第三章识别关键主体']),
           'chapter3':(21,['上述为证据引出的行动建议']),
           'chapter5':(11,['这些行动方向由本章证据支持'])}
  if name in cleanup:
   pi,prefixes=cleanup[name];p=doc[pi]
   for b in p.get_text('blocks'):
    if any(b[4].startswith(prefix) for prefix in prefixes):
     p.add_redact_annot(fitz.Rect(b[:4]),fill=(1,1,1),cross_out=False)
     PATCHES.append(dict(tag=name+'-clean-handoff',page=pi+1,old=b[4],new='',count=1))
   p.apply_redactions(images=0,graphics=0,text=0)
  out=MASTER/'prepared'/f'{name}.pdf';doc.save(out,garbage=4,deflate=True);paths[name]=out
 return paths

def model_method(folio=115):
 s=start()+header(folio,6)+footer(folio,6)
 s+=txt(19,28,177,'17　模型生态：数据与阅读口径',18.5,26,'navy',True,mh=13)
 s+=txt(19,44,177,'分别理解资源数量、获取活动、声明关系、网络位置与开放条件。不同对象、时间和样本不合成为一个国家或模型总分。',10.1,16.5,'ink',False,True,mh=17)
 rows=[
 (65,'图 5-1｜资产总量与周度新增','平台总览于 2026.11.11 读取；仓库总量更新日为 2026.11.09，论文与社区为本次读取值。模型、数据集和 Spaces 的主期新增与上年同窗逐日合计比较；周线统一截至 2026.07.18。论文日期含义尚未明确，不计算同比，也不解释为当周新收录。'),
 (100,'图 5-1—5-3｜地域、主体与获取活动','地域沿用 2026.10.17 冻结的 826 个组织账号、73,088 个模型与 12,502 个数据集，不以平台总量更新地域比例。国家按发布组织归属，省级归属待补仍留在全国分母。下载与点赞不代表独立用户、部署量或质量。'),
 (133,'图 5-2｜两类时间序列','年度回看采用 2026.09.13 仍可见仓库的创建日期，不是逐年独立快照。月度记录覆盖 2024.07—2026.06，主期合计与此前 12 个月比较；两套来源不拼接，留存与下架规则仍待补充。'),
 (164,'图 5-4—5-6｜派生与影响','网络来自 2026.10.16 非随机前 12,000 个输入中双端可见的声明关系，网络位置不代表模型能力。跨国表为 2026.09.13 的 10,943 对关系，与网络样本不同。来源称国家识别覆盖约 2.59%（含境内），完整分母尚未独立重建。'),
 (198,'图 5-7—5-10｜统一开放评价样本','采用 2026.11.11 读取的 889 个完整模型 ID，与逐项证据对应，保留严格模式等级。按 country 字段重算国别，未知 64 条保留；旧 870、884 样本仅作归档，不将差值视为增长。三案例均使用精确模型 ID。'),
 (232,'分级与证据｜材料、权限及实际结果','L1—L5 为累进材料完整性，O1—O4 为权利条件；材料较完整为 L3—L5，权限较开放为 O2—O4。missing 只表示来源未找到充分证据，不直接证明文件不存在。本报告未独立重跑训练或授予等级。正式标准、逐版本许可、统一截止日与地理覆盖继续核查；公共能力仍需成本、本地化、维护与结果证据。')]
 for y,t,b in rows:
  s+=txt(19,y,177,t,10.8,15.7,'teal',True,mh=8)
  s+=txt(19,y+8,177,b,9.8,15.3,'ink',False,True,mh=33 if y==232 else 26)
 return end(s)

def back_cover():
 s=start()+image(0,0,210,'assets/cover-background.png',297)
 s+=emblem(75,24,60)
 s+=txt(18,102,174,'共同创造',35,46,'navy',True,True,r'\centering ',mh=20)
 s+=txt(12,124,186,'开放的智能未来',35,46,'navy',True,True,r'\centering ',mh=20)
 s+=txt(18,151,174,'OPEN SOURCE, A SHARED INTELLIGENT FUTURE',11.5,17,'navy',False,False,r'\centering ',mh=12)
 return end(s)

def compile_master():
 (MASTER/'master.tex').write_text(r'\documentclass[11pt,a4paper]{article}\usepackage{layout}\begin{document}'+'\n'+''.join(TEX_PAGES)+r'\end{document}')
 (REVIEW/'master-boxes.json').write_text(json.dumps(BOXES,ensure_ascii=False,indent=2))
 env=os.environ.copy();env['TEXMF']='{/usr/share/texmf,/usr/share/texlive/texmf-dist}';env['TEXMFVAR']=str((R.parent/'front-v0.8/.texmf-var').resolve());env['TEXFORMATS']=env['TEXMFVAR']
 passes=1 if '--incremental' in __import__('sys').argv and (MASTER/'output/master.aux').exists() else 2
 for i in range(passes):
  with (MASTER/'output'/f'build-{i+1}.txt').open('w') as f:
   subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory=output','master.tex'],cwd=MASTER,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 print('Master compiled:',len(TEX_PAGES),'pages',flush=True)

def add_spec(module,kind,folio,idx,**kw):
 s=dict(module=module,kind=kind,folio=folio,idx=idx,**kw)
 if kind=='body':
  layer=start()+header(folio,idx)+footer(folio,idx)
  dx=4 if folio%2 else -4
  for t in TEXT_OVERLAYS.get((kw['sourcekey'],kw['sourcepage']),[]):
   if not 24*M<t['y']<281.5*M:continue
   c='patch'+str(len(TEX_PAGES))+'x'+str(round(t['x']))+'y'+str(round(t['y']))
   layer+=rf'\definecolor{{{c}}}{{rgb}}{{'+','.join(str(x) for x in t['rgb'])+'}\n'
   font=(r'\sffamily ' if t['key'].startswith('sans') else r'\rmfamily ')+(r'\bfseries ' if t['key'].endswith('b') else '')
   layer+=rf'\node[anchor=base west,inner sep=0pt,text={c}] at \Pos{{{t["x"]/M+dx}}}{{{t["y"]/M}}}{{'+font+rf'\fontsize{{{t["fs"]}}}{{{t["fs"]*1.4}}}\selectfont '+esc(t['text'])+'};\n'
  s['overlay']=end(layer)
 SPECS.append(s);return s

def setup_specs(paths):
 for idx,name in enumerate(['chapter1','chapter2','chapter3','chapter4','chapter5','chapter6']):
  module=idx+2;folio=STARTS[idx]
  add_spec(module,'cover',folio,idx,overlay=cover(idx));add_spec(module,'blank',folio+1,idx)
  indexes=[*range(14,23)] if idx==0 else [*range(1,21)] if idx==1 else [*range(1,22)] if idx==2 else [*range(13)] if idx==3 else [*range(1,12)] if idx==4 else [*range(6)]
  for j,sp in enumerate(indexes):
   source=paths['figure5-1'] if idx==4 and sp==1 else paths[name];sourcepage=0 if idx==4 and sp==1 else sp
   add_spec(module,'body',folio+2+j,idx,source=str(source),sourcepage=sourcepage,sourcekey='figure5-1' if idx==4 and sp==1 else name)
  while len([s for s in SPECS if s['module']==module])<COUNTS[idx]:add_spec(module,'blank',folio+len([s for s in SPECS if s['module']==module]),idx)
 # Appendix: common reference, unique chapter methods, bilingual thanks, back cover.
 add_spec(8,'cover',97,6,overlay=cover(6));add_spec(8,'blank',98,6)
 app=[('appendix',i) for i in range(8)]+[('chapter2',i) for i in range(21,26)]+[('chapter3',23),('chapter4',13),('chapter4',14)]
 for j,(name,sp) in enumerate(app):add_spec(8,'body',99+j,6,source=str(paths[name]),sourcepage=sp,sourcekey=name)
 add_spec(8,'custom',115,6,overlay=model_method());add_spec(8,'blank',116,6)
 for j in range(2):add_spec(8,'body',117+j,6,source=str(paths['appendix']),sourcepage=8+j,sourcekey='appendix')
 add_spec(8,'blank',119,6);add_spec(8,'back',120,6,overlay=back_cover())

def copy_links(dst,src,dx,clip,index_map):
 for l in src.get_links():
  if not clip.contains(l['from']):continue
  ll={k:v for k,v in l.items() if k not in ['xref','id']};rr=fitz.Rect(ll['from']);rr.x0+=dx;rr.x1+=dx;ll['from']=rr
  if l['kind']==fitz.LINK_GOTO:
   if l['page'] not in index_map:continue
   ll['page']=index_map[l['page']]
   if 'to' in ll:ll['to']=fitz.Point(ll['to'].x+dx,ll['to'].y)
  try:dst.insert_link(ll)
  except (ValueError,RuntimeError):pass

def assemble():
 overlay=fitz.open(MASTER/'output/master.pdf');docs={};manifest=[];allbody=[]
 fnames=['M01_Frontmatter','M02_Chapter1','M03_Chapter2','M04_Chapter3','M05_Chapter4','M06_Chapter5','M07_Chapter6','M08_Appendix_Acknowledgements']
 # Roman preliminaries: blank inside front cover, after contents, before Chapter 1.
 front=fitz.open(R/'frontmatter/output/report.pdf');d=fitz.open();mapping={}
 for i in range(15):
  mapping[i]=len(d);d.insert_pdf(front,from_page=i,to_page=i)
  if i in [0,7,14]:d.new_page(width=210*M,height=297*M)
 assert len(d)==18
 names=['封面','扉页与报告说明','编委会','奇点智能研究院','五大范式转换','六大研究方向','从研究问题走向可检验的实践','目录','执行摘要','从证据到行动','全书结构与阅读路径','如何读懂一页综合图','引言与国际合作宣言','合作宣言：核心原则','合作宣言：共创未来']
 d.set_toc([[2 if i in [4,5,6,9,13,14] else 1,n,mapping[i]+1] for i,n in enumerate(names)])
 # Explicit front-matter navigation; chapter folios are coordinated across modules.
 for j,target in enumerate([2,3,8,10,11,12]):
  y=94+j*8.2;d[mapping[7]].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(14*M,y*M,133*M,(y+7.5)*M),'page':mapping[target]})
 d.set_page_labels([dict(startpage=0,prefix='封面',style=''),dict(startpage=1,prefix='封二',style=''),dict(startpage=2,prefix='',style='r',firstpagenum=1)])
 d.set_metadata(dict(title='2026 全球开源发展报告·精要版｜模块 1：封面和前置内容｜打印评审 v0.1',author='全球开源发展报告编制组',subject='A4双面打印；空白页无标识；中文字体嵌入',creator='XeLaTeX / PyMuPDF'))
 out=OUT/f'GOSD_2026_Print_{fnames[0]}_v0.1.pdf';d.save(out,garbage=4,deflate=True)
 manifest.append(dict(module=1,name='封面和前置内容',file=str(out),pages=18,blank_pages=[2,10,18],folios='i—xvi，封面与封二不计罗马页码',source_pages=mapping))
 for module in range(2,9):
  ss=[s for s in SPECS if s['module']==module];d=fitz.open();idx=module-2
  maps={}
  for i,s in enumerate(ss):
   if s['kind']=='body':maps.setdefault(s['source'],{})[s['sourcepage']]=i
  for s in ss:
   p=d.new_page(width=210*M,height=297*M)
   if s['kind']=='blank':continue
   if s['kind']=='body':
    src=docs.setdefault(s['source'],fitz.open(s['source']));sp=src[s['sourcepage']]
    # No scaling: a 4 mm horizontal translation creates a binding gutter.
    dx=(4 if s['folio']%2 else -4)*M
    clip=fitz.Rect(10*M,24*M,200*M,281.5*M);dst=fitz.Rect(clip.x0+dx,clip.y0,clip.x1+dx,clip.y1)
    p.show_pdf_page(dst,src,s['sourcepage'],clip=clip)
    allbody.append(dict(module=module,local_page=p.number+1,source=s['source'],sourcepage=s['sourcepage'],dx=dx,clip=list(clip),expected_text=sp.get_text(clip=clip)))
   p.show_pdf_page(p.rect,overlay,s['overlay'])
  for i,s in enumerate(ss):
   if s['kind']=='body':
    sp=docs[s['source']][s['sourcepage']];dx=(4 if s['folio']%2 else -4)*M
    copy_links(d[i],sp,dx,fitz.Rect(10*M,24*M,200*M,281.5*M),maps[s['source']])
  # Module bookmarks and the opener's local navigation.
  title=TITLES[idx] if idx<6 else '附录与致谢'
  toc=[[1,('第'+'一二三四五六'[idx]+'章　' if idx<6 else '')+title,1]]
  for n,t,desc,a,b in SUBS[idx]:
   target=a-STARTS[idx];toc.append([2,n+'　'+t,target+1])
  if idx in [1,2,4]:toc.append([2,'本章综合与行动方向',{1:34,2:57,4:87}[idx]-STARTS[idx]+1])
  if idx==6:
   toc += [[2,'致谢',21],[2,'Acknowledgements',22],[1,'封底',24]]
   # Actual Chinese and English thanks are pages 21 and 22 in this module.
  d.set_toc(toc)
  # Safe local links from chapter navigation rows.
  rows=SUBS[idx]
  top=141 if len(rows)==6 else 154 if idx==0 else 168 if idx==5 else 140 if idx==6 else 143
  h=18.5 if len(rows)==6 else 31 if idx==0 else 28 if idx==5 else 23 if idx==6 else 32
  for j,(_,_,_,a,b) in enumerate(rows):
   d[0].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(19*M,(top+j*h-1)*M,196*M,(top+(j+1)*h-2)*M),'page':a-STARTS[idx]})
  d.set_page_labels([dict(startpage=0,prefix='',style='D',firstpagenum=STARTS[idx])])
  version='0.3' if module==8 else '0.2' if module==6 else '0.1'
  d.set_metadata(dict(title=f'2026 全球开源发展报告·精要版｜模块 {module}：{title}｜打印评审 v{version}',author='全球开源发展报告编制组',subject='A4双面打印；章首页右页；内侧装订留白；中文字体嵌入',creator='XeLaTeX / PyMuPDF'))
  out=OUT/f'GOSD_2026_Print_{fnames[module-1]}_v{version}.pdf';d.save(out,garbage=4,deflate=True)
  manifest.append(dict(module=module,name=title,file=str(out),pages=len(d),blank_pages=[i+1 for i,s in enumerate(ss) if s['kind']=='blank'],folios=[STARTS[idx],STARTS[idx]+len(d)-1]))
  print('Module',module,'saved:',len(d),'pages',flush=True)
 (REVIEW/'module-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 (REVIEW/'body-retention.json').write_text(json.dumps(allbody,ensure_ascii=False,indent=2))
 (REVIEW/'pdf-text-patches.json').write_text(json.dumps(PATCHES,ensure_ascii=False,indent=2))
 (REVIEW/'page-specs.json').write_text(json.dumps(SPECS,ensure_ascii=False,indent=2))
 print('TOTAL',sum(m['pages'] for m in manifest),'pages,',sum(len(m['blank_pages']) for m in manifest),'intentional blank pages',flush=True)

if __name__=='__main__':
 paths=prepare_sources();print('Prepared text corrections and appendix remapping',flush=True)
 setup_specs(paths);compile_master();assemble()
