"""Build a single continuously paginated chapter from seven edited JSON masters.
LaTeX remains the publication master. No page images are used as body text.
"""
from pathlib import Path
import re,json,hashlib
R=Path(__file__).resolve().parents[1]
sections={s:json.loads((R/'sections'/f'{s}.json').read_text()) for s in range(21,28)}
# Global bibliography, de-duplicated by canonical URL. Keep per-section provenance keys.
bib=[];byurl={};keymap={}
for s,o in sections.items():
 for key,desc,url in o['references']:
  norm=url.rstrip('/')
  if norm not in byurl:
   byurl[norm]='ref'+str(len(bib)+1)
   bib.append({'id':byurl[norm],'title':desc,'url':url,'section_keys':[]})
  bid=byurl[norm];keymap[(s,key)]=bid
  next(x for x in bib if x['id']==bid)['section_keys'].append([s,key])
# Titles shortened only for the printed bibliography; full originals retained in references.json.
short={
('21','world'):'GOSD编制组．全球开发者与活跃开发者报告年度归档，2022—2026．OpenDigger／OpenShare来源记录，版本c51e344。',
('21','five'):'GOSD编制组．五域开发者总量与活跃开发者序列，2022—2026报告年度．版本c51e344。',
('21','platform'):'GOSD编制组．本土平台补充量与覆盖比较说明，2026-10-20．版本c51e344。',
('21','province'):'GOSD编制组．中国34个省级地区总量、活跃与同比增量．版本c51e344。',
('21','octoverse'):'GitHub．Octoverse 2026: Commits, pushes, reach new highs in 2026 as developers build with agents．2026-10-28。',
('22','world'):'GOSD编制组．C-Map国家贡献与活跃快照，2025年．236个地域记录，版本c51e344。',
('22','province'):'GOSD编制组．中国34个省级地区贡献与活跃快照，2025年．版本c51e344。',
('23','global'):'GOSD编制组．I-Map地域与企业影响力归档，2025自然年．版本c51e344。',
('24','world'):'GOSD编制组．全球高影响力人才地域表，2026年7月快照．前5%定义沿用源表，筛选方法待核。',
('25','sample'):'GOSD编制组．A-Map发布单位累计样本，observations.json．快照日期未注明，版本c51e344。',
('25','tech25'):'OpenDigger／GOSD 2025．Technology-Domain Bubble Chart Analysis．12类项目数量及影响力，版本5c2ffc4。'}
for b in bib:
 for s,k in b['section_keys']:
  if (str(s),k) in short:b['print_title']=short[(str(s),k)];break
 b.setdefault('print_title',b['title'])
# Namespaced labels prevent same local figure IDs in different sections from colliding.
labels={};figmanifest=[]
for s,o in sections.items():
 n=0
 for i,pg in enumerate(o['pages']):
  for b in pg['blocks']:
   if b['type'] in ['figure','group']:
    n+=1;key=(s,b['label']);labels[key]=f's{s}-{b["label"].replace(":","-")}'
    figmanifest.append({'section':f'2.{s%10}','number':f'2-{s%10}-{n}','label':labels[key],'caption':b['caption'],'page_unit':i+1,'assets':b.get('assets',[b.get('asset')]),'source':b.get('source','')})

used=set()
def esc(s,sec=None):
 s=str(s)
 # escape literal special characters but leave semantic markers for a second pass
 s=s.replace('\\',r'\textbackslash{}').replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#').replace('$',r'\$')
 s=s.replace('<br>',r'\newline ')
 s=re.sub(r'\*\*(.*?)\*\*',lambda m: r'\key{'+m[1]+'}',s)
 def cite(m):
  bid=keymap[(sec,m[1])];used.add(bid);return r'\cite{'+bid+'}'
 s=re.sub(r'\[\[([^\]]+)\]\]',cite,s)
 s=re.sub(r'<<([^>]+)>>',lambda m:r'\ref{'+labels[(sec,m[1])]+'}',s)
 return s

def src(s,sec):return '\\src{'+esc(s,sec)+'}\n'
PRE=r'''\documentclass[UTF8,fontset=none,11pt,a4paper]{ctexart}
\usepackage[left=20mm,right=20mm,top=20mm,bottom=19mm,headheight=22pt,headsep=5mm,footskip=8mm]{geometry}
\usepackage{fontspec,xeCJK,graphicx,xcolor,booktabs,tabularx,longtable,array,caption,float,fancyhdr,hyperref,bookmark,titlesec,microtype,needspace,tikz}
\setCJKmainfont[Path=.build_fonts/,BoldFont=NotoSerifSC-Bold.otf]{NotoSerifSC-Regular.otf}
\setCJKsansfont[Path=.build_fonts/,BoldFont=NotoSansSC-Bold.otf]{NotoSansSC-Regular.otf}
\setCJKmonofont[Path=.build_fonts/,BoldFont=NotoSansSC-Bold.otf]{NotoSansSC-Regular.otf}
\setmainfont{Liberation Serif}\setsansfont{Liberation Sans}
\definecolor{navy}{HTML}{193C4E}\definecolor{teal}{HTML}{168A8D}\definecolor{ink}{HTML}{183642}
\definecolor{muted}{HTML}{55717C}\definecolor{rule}{HTML}{D8E5E7}\definecolor{pale}{HTML}{F0F6F6}\definecolor{blue}{HTML}{3E6686}
\color{ink}\raggedbottom\linespread{1.05}
\setlength{\emergencystretch}{2em}
\setlength{\parindent}{2em}\setlength{\parskip}{4.5pt}
\AtBeginDocument{\fontsize{11.2}{18}\selectfont}
\setlength{\textfloatsep}{6pt}\setlength{\intextsep}{6pt}
\hypersetup{colorlinks=true,linkcolor=navy,urlcolor=teal,citecolor=teal,pdftitle={2026全球开源发展报告｜第二章 全球开源生态观测地图｜整章评审稿 v1.0},pdfauthor={GOSD编制组},bookmarksnumbered=false,pdfpagemode=UseOutlines}
\captionsetup{hypcap=false,font={small,sf},labelfont={bf,color=navy},labelsep=quad,skip=4pt,justification=raggedright,singlelinecheck=false}
\titleformat{\section}{\sffamily\bfseries\color{navy}\fontsize{19}{26}\selectfont}{}{0pt}{}
\titleformat{\subsection}{\sffamily\bfseries\color{teal}\fontsize{13.5}{19}\selectfont}{}{0pt}{}
\titlespacing*{\section}{0pt}{0pt}{7pt}\titlespacing*{\subsection}{0pt}{1pt}{7pt}
\newcommand{\key}[1]{{\bfseries\color{navy}#1}}
\newcommand{\src}[1]{\par\vspace{1pt}\noindent{\sffamily\fontsize{8.7}{12.1}\selectfont\color{muted}#1}\par}
\newcommand{\lead}[1]{\par\noindent{\sffamily\fontsize{12.1}{18}\selectfont\color{teal}#1}\par\vspace{4pt}}
\newcommand{\eyebrow}[1]{\noindent{\sffamily\bfseries\fontsize{9}{12}\selectfont\color{teal}#1}\par\vspace{4pt}}
\newcommand{\topic}[1]{\par\vspace{5pt}\noindent{\sffamily\bfseries\color{navy}#1}\par\vspace{1pt}}
\newcommand{\CurrentSection}{第二章\quad 全球开源生态观测地图}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\sffamily\fontsize{8.3}{10}\selectfont\color{muted}GOSD 2026 / 全球开源发展报告}
\fancyhead[R]{\sffamily\fontsize{8.3}{10}\selectfont\color{muted}\CurrentSection}
\fancyfoot[L]{\sffamily\fontsize{8.2}{10}\selectfont\color{muted}第二章\quad 全球开源生态观测地图}
\fancyfoot[R]{\sffamily\fontsize{9}{10}\selectfont\color{navy}\thepage}
\renewcommand{\headrulewidth}{.35pt}\renewcommand{\headrule}{\hbox to\headwidth{\color{rule}\leaders\hrule height .35pt\hfill}}
\renewcommand{\footrulewidth}{.3pt}\renewcommand{\footrule}{\hbox to\headwidth{\color{rule}\leaders\hrule height .3pt\hfill}}
\renewcommand{\arraystretch}{1.4}
\begin{document}
'''
tex=PRE;md=['# 第二章 全球开源生态观测地图（GOSO）\n\n整章评审稿 v1.0.0 · 2026-11-05 · 待作者评审\n']
tex+=r'''\pdfbookmark[0]{第二章 全球开源生态观测地图}{chapter2}
\eyebrow{02 / GLOBAL OPEN SOURCE OBSERVATORY}
\section*{全球开源生态观测地图}
\lead{参与在扩大，生态的不同层面却并不同步}
如果只看开发者人数，世界开源版图会呈现一种格局；换看协作贡献、项目影响或可复用资产，排序和结构可能随之变化。\key{理解开源发展，需要把这些侧面放在一起，而不是寻找一张能够代表一切的总榜。}

第一章说明了从开放协作走向公共价值需要哪些条件。本章转向可以观察的参与与资源：谁进入生态，贡献如何汇聚，项目与人才在哪里积累，代码、模型与数据怎样形成供给，以及多元来源如何获得组织与规则的支持。

七节分别承担一个问题，也构成连续的阅读路径：\key{由参与进入协作，由项目与人才进入资产，再以多样性和治理解释共同建设的条件。}这是一套互补观察，不是一条已经证明的因果链。

\vspace{4pt}
\noindent{\sffamily\bfseries\color{navy}本章阅读路径}\par\vspace{3pt}
\begingroup\fontsize{10.5}{15.5}\selectfont\renewcommand{\arraystretch}{1.38}
\noindent\begin{tabularx}{\linewidth}{@{}>{\raggedright\arraybackslash\sffamily\color{teal}}m{12mm}>{\raggedright\arraybackslash\sffamily\bfseries}m{31mm}>{\raggedright\arraybackslash}X>{\raggedleft\arraybackslash}m{8mm}@{}}
\toprule
2.1 & 活跃地图 & 参与基础有多大，新增活跃在哪里？ & \hyperref[sec21]{\pageref{sec21}}\\
2.2 & 贡献地图 & 人数之外，协作工作怎样汇聚与连接？ & \hyperref[sec22]{\pageref{sec22}}\\
2.3 & 项目影响力地图 & 贡献来源与项目影响为何呈现不同分布？ & \hyperref[sec23]{\pageref{sec23}}\\
2.4 & 人才地图 & 高影响力参与者在哪里积累和增长？ & \hyperref[sec24]{\pageref{sec24}}\\
2.5 & 资产地图 & 代码、模型与数据形成了怎样的供给？ & \hyperref[sec25]{\pageref{sec25}}\\
2.6 & 多样性地图 & 谁进入共同建设，技术选择怎样变化？ & \hyperref[sec26]{\pageref{sec26}}\\
2.7 & 治理地图 & 谁提供组织支持，参与和复用遵循什么规则？ & \hyperref[sec27]{\pageref{sec27}}\\
\bottomrule
\end{tabularx}\endgroup

\topic{三个贯穿全章的观察}
\key{规模与结构分别阅读。}较大规模未必对应较高平均贡献，较快增长也未必提供最多新增量。\key{归属与来源分别记录。}项目可以归属某一组织或地区，同时由多地参与者共同建设。\key{数量与条件分别判断。}资产发布、文件覆盖和许可采用，为持续使用提供入口，但不能替代对维护和实际结果的核查。

\vfill
\src{整章评审稿 v1.0.0 · 2026年11月5日。主统计期：2025年7月1日至2026年6月30日；历史快照、外部观察和条件估算随图标明。}
\clearpage
\pdfbookmark[1]{阅读说明：先分清对象，再比较数字}{reader}
\subsection*{阅读说明：先分清对象，再比较数字}
本章尽量用直观图表呈现差异。以下概念用于区分观察对象，读者无需掌握算法细节，也可以沿着地图、排行和趋势理解主要发现。

\topic{人、项目与资产}
\key{开发者与活跃开发者。}前者描述积累起来的参与基础，后者指在统计期内发生了纳入规则的协作。一个人可能使用多个平台，也可能某年活跃、某年暂停；人数净增不等于首次参与人数。

\key{仓库与项目。}仓库是存放代码、版本及协作记录的空间；一个项目可能包含多个仓库，也可能跨平台托管。代码仓库、模型条目和数据集条目是不同资产，不能直接相加成为独立创新成果数。

\topic{协作、贡献与影响}
\key{修改请求（PR）与问题记录（Issue）。}前者是请求项目接纳的一组修改，后者用于记录问题、需求或讨论。提出、审阅、讨论和维护，都可能构成协作的一部分。

\key{OpenRank。}它依据协作关系观察网络位置，而不是只累加事件次数。开发者贡献度与项目影响力的对象和聚合方式不同；本章保留源表定义，不把两者相除为效率，也不把得分视为质量或社会价值认证。

\topic{读数与图形}
\key{总量、均值与份额。}总量回答“有多少”，均值说明相对于指定分母的差异，份额说明占某一合计的比例。份额从10\%到12\%，增加的是2个百分点、相对增幅为20\%，两种表达不应混用。

\key{地图、条形与流带。}地图帮助定位，条形便于比较大小，趋势图显示时间变化。桑基图的带宽表示连接数值；本章贡献流带表示OpenRank贡献度，不表示人员迁移或资金流动。未知与未列不按零处理。

\topic{本章的比较范围}
五域固定比较欧洲、美国、中国、印度与南方六国代表组，后者由巴西、印度尼西亚、越南、菲律宾、埃及和南非组成。欧洲沿用各表范围；五域不是对世界的完整划分。中国省级观察纳入台湾、香港和澳门。

\src{各图保留具体对象、窗口与关键分母。下载只是使用信号；高影响力人才沿用源表筛选，并非完整能力评价。详细来源与方法见章末，生产端待核事项另存核查包。}
'''
# add method source citations to glossary, not front navigation
tex=tex.replace('不表示人员迁移或资金流动。未知与未列不按零处理。','不表示人员迁移或资金流动。未知与未列不按零处理。')
used.update([keymap[(22,'globalrank')],keymap[(22,'openrank')],keymap[(21,'usage')]])
tex=tex.replace('不把得分视为质量或社会价值认证。','不把得分视为质量或社会价值认证。\\cite{'+keymap[(22,'globalrank')]+','+keymap[(22,'openrank')]+'}')
md+=['## 章首：参与在扩大，生态的不同层面却并不同步\n\n本章依次观察参与、贡献、项目、人才、资产、多样性与治理。规模、结构、来源、使用与条件分别记录，不合成为单一总榜。\n','## 阅读说明\n\n仓库与项目、活跃与累计基础、贡献与影响力、份额与增长率分别理解；具体口径见各图与章末方法。\n']
# By page, source values unchanged; labels remain section-local.
pageplans=[]
for s,o in sections.items():
 sn=s%10
 tex+='\n\\clearpage\n\\renewcommand{\\CurrentSection}{'+f'2.{sn} '+re.sub(r'^2\.\d+\s*','',o['pages'][0]['title']).split('（')[0]+'}\n'
 tex+=f'\\renewcommand{{\\thefigure}}{{2-{sn}-\\arabic{{figure}}}}\\setcounter{{figure}}{{0}}\n'
 tex+=f'\\renewcommand{{\\thetable}}{{2-{sn}-\\arabic{{table}}}}\\setcounter{{table}}{{0}}\n'
 # new section starting outline label
 tex+=f'\\phantomsection\\label{{sec{s}}}\\pdfbookmark[1]{{'+esc(o['pages'][0]['title'].split('（')[0])+'}{section'+str(s)+'}\n'
 for i,pg in enumerate(o['pages']):
  if i:tex+='\n\\clearpage\n'
  tex+=f'\\label{{unit{s}-{i}}}\n'
  t=pg['title'].split('（')[0] if i==0 else pg['title']
  tex+=('\\section*{' if i==0 else '\\subsection*{')+esc(t,s)+'}\n'
  if i and re.match(r'^2\.\d+\.\d+',t): tex+='\\pdfbookmark[2]{'+esc(t,s)+'}{outline'+str(s)+'-'+str(i)+'}\n'
  md+=['\n## '+pg['title']+'\n']
  if pg.get('subtitle'):
   tex+='\\lead{'+esc(pg['subtitle'],s)+'}\n';md +=[pg['subtitle']+'\n']
  for b in pg['blocks']:
   typ=b['type']
   if typ=='p':tex+=esc(b['text'],s)+'\n\n';md +=[b['text']+'\n']
   elif typ=='heading':tex+='\\subsection*{'+esc(b['text'],s)+'}\n';md +=['### '+b['text']+'\n']
   elif typ=='note':tex+=src(b['text'],s);md +=['*'+b['text']+'*\n']
   elif typ=='insight':
    tex+='\\topic{'+esc(b['title'],s)+'}\n'+esc(b['text'],s)+'\n\n';md +=['**'+b['title']+'** '+b['text']+'\n']
   elif typ=='asset':
    tex+='\\par\\vspace{4pt}\\noindent\\includegraphics[width=\\linewidth]{figures/'+str(s)+'/'+b['asset']+'.pdf}\\par\\vspace{5pt}\n';md+=['![](figures/'+str(s)+'/'+b['asset']+'.svg)\n']
   elif typ in ['figure','group']:
    assets=b.get('assets',[b.get('asset')]);tex+='\\par\\vspace{4pt}\\noindent\\begin{minipage}{\\linewidth}\\centering\n'
    for a in assets:
     tex+='\\includegraphics[width=\\linewidth]{figures/'+str(s)+'/'+a+'.pdf}\\par\n';md+=['![](figures/'+str(s)+'/'+a+'.svg)\n']
    tex+='\\captionof{figure}{'+esc(b['caption'],s)+'}\\label{'+labels[(s,b['label'])]+'}\\end{minipage}\\par\\vspace{4pt}\n'
    md +=['**图 '+next(f['number'] for f in figmanifest if f['label']==labels[(s,b['label'])])+' '+b['caption']+'**\n']
    if b.get('source'):tex+=src(b['source'],s);md+=['*'+b['source']+'*\n']
  pageplans.append({'section':f'2.{sn}','unit_label':f'unit{s}-{i}','heading':pg['title']})
# Single action synthesis keeps the reader in the chapter rather than seven separate mini-reports.
tex+=r'''
\clearpage
\renewcommand{\CurrentSection}{第二章\quad 综合观察}
\pdfbookmark[1]{本章小结：从观察差异到识别支持需求}{conclusions}
\subsection*{本章小结：从观察差异到识别支持需求}
七幅地图呈现同一生态的不同侧面。参与规模在扩大，但活跃、贡献与项目影响并没有形成相同排序；项目有归属，贡献却可以跨越地域；代码、模型与数据持续积累，供给内容与使用结构也并不一致。将这些差异同时保留，比压成一个总分更能帮助识别实际需求。

\topic{参与与贡献：看见入口，也看见持续工作}
活跃人数提供参与基础，贡献及其来源进一步揭示协作。公共部门和平台既应扩展可进入的机会，也应关注问题响应、代码审阅和维护能否延续。平台覆盖不同造成的可见性差异，尤其不宜被误读为参与力量不存在。

\topic{项目、人才与资产：把支持落实到具体对象}
较高项目影响提示值得关注的协作节点，人才样本提示经验积累的地域差异，资产目录则呈现可复用供给。它们适合用于寻找项目、理解结构和提出问题；具体资源配置仍需核对真实需求、维护缺口和下游使用。

\topic{多样性与治理：把连接转化为可持续合作}
不同地域和技术社区的参与，需要清楚的任务、反馈和规则入口。基金会支持与许可声明提供组织和使用条件，但数量、覆盖与采用并不替代执行。持续观察责任是否明确、问题能否被处理，比单独增加组织或文件更有意义。

\vspace{3pt}
\noindent{\sffamily\bfseries\color{navy}面向不同主体的共同工作}\par\vspace{3pt}
\begingroup\fontsize{10.1}{15}\selectfont
\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.34}
\noindent\begin{tabularx}{\linewidth}{@{}p{27mm}Xp{55mm}@{}}\toprule
行动主体 & 优先支持 & 后续观察\\\midrule
公共部门与国际组织 & 结合参与盲区、真实项目与维护缺口配置支持，连接已有中心与成长社区。 & 是否形成持续任务与当地参与机会，而非只增加注册或发布数量。\\\addlinespace[4pt]
基金会、企业与社区 & 支持评审、文档、安全更新和人员接续，使外部参与能够进入共同建设。 & 反馈是否及时，职责能否交接，许可与版本是否清楚。\\\addlinespace[4pt]
高校、平台与研究机构 & 提供跨地区真实实践，维护可比的对象、来源与统计版本。 & 参与能否延续，资源是否可复用，数据变化能否复查。\\\bottomrule
\end{tabularx}\endgroup

\vspace{4pt}
第二章回答“参与和资源在哪里，结构有何不同”。下一章将把观察落到地区、企业、基金会与项目等主体，进一步考察它们在协作网络中的位置与变化，而不是重复宏观地图。

\clearpage
\renewcommand{\CurrentSection}{第二章\quad 资料与方法}
\pdfbookmark[1]{资料与方法：图表范围、可比性和估算}{methods}
\subsection*{资料与方法：在各自范围内理解比较}
本章采用GOSD归档、平台官方研究与规范文本三类互补资料。主统计期为\key{2025年7月1日至2026年6月30日}；历史快照与独立平台窗口按图说明。不同来源可以相互启发，但不因此成为同一个统计总体。

\begingroup\fontsize{10.2}{15}\selectfont
\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.4}
\noindent\begin{tabularx}{\linewidth}{@{}p{28mm}p{56mm}X@{}}\toprule
资料单元 & 实际范围 & 主要解释边界\\\midrule
参与与活跃 & 2022—2026报告年度；GitHub地域表、五域表与本土平台补充分别使用。 & 不将不同覆盖相加为统一全球人数；净增不是首次参与。\\\addlinespace[3pt]
贡献与项目影响 & 全球及省级图主要为2025自然年快照；五域与项目来源采用报告年度。 & 不跨表反推人均值、转化率或地域净输出。\\\addlinespace[3pt]
高影响力人才 & 全球图为2026年7月快照；五域与固定十城为年度序列。 & 前5\%的总体、窗口和并列规则待核；人数变化不是迁移。\\\addlinespace[3pt]
代码、模型与数据 & 代码为年度活跃仓库；发布单位样本是日期待核的累计快照；任务记录采于2026年10月。 & 各类资产不相加；发布地不同于使用地，下载不等于独立用户。\\\addlinespace[3pt]
外部平台观察 & GitHub 2026年报为截至9月底的年度窗，默认含公私仓；HF资料按各图原窗口。 & 不并入GOSD主期增长或分母；平台自报不改称自行测量。\\\addlinespace[3pt]
治理与许可 & 三组独立归档序列；协作材料覆盖为2025平台观察；条款按明确版本核对。 & 不据有限样本推算全球覆盖，不将文件存在当作治理成效。\\\bottomrule
\end{tabularx}\endgroup

\topic{样本与归属}
地域来自源表所用的位置或组织标签，不等于国籍。项目可能有多仓库、跨平台或基金会托管关系；采用当前公开标签不能自动还原历史归属。本章保留原始对象与数值，并对样本之外、未知与未列分别处理。

\topic{两套贡献关系，分别回答各自问题}
2.2的中美来源前十表含20条记录，并保留完整样本的原始份额；2.6的扩展关系表含60条记录、14个来源和10个目的地。二者覆盖不同，不能用差额判断增长，也不能相互填补未列关系。2.6的内部来源构成对照则明确复用2.2的前十表。

\clearpage
\subsection*{条件估算、核查与复现}
\topic{技术结构估算：明确假设，保留已知总量}
2.5的分类下钻以GOSD 2025技术图表的12类项目数量为基准。设第$i$类记录数为$n_i$，结构比例为$p_i=n_i/\sum_j n_j$，则结构延续估计为：
\[
\widehat{N}_{i,t}=p_i N_t,\qquad
\widehat{\Delta N_i}=p_i(N_{2026}-N_{2025}).
\]
其中$N_t$是已知的GitHub活跃仓库总量。由项目分类比例映射仓库数量，假设样本能够外推、类别互斥且覆盖完整，这些条件尚未验证。因此估计用于观察假设下的结构，不是实测类别统计。

AI敏感性分析将该类增长率分别设为20\%、30\%、40\%，其他类别按共同增幅平衡总量。若AI期初规模为$A_{2025}$、设定增长率为$g$，其余类别的平衡增长率为：
\[
 g_{\mathrm{other}}=
 \frac{N_{2026}-A_{2025}(1+g)}{N_{2025}-A_{2025}}-1.
\]
三个参数是情景假设，不是置信区间、官方预测或实际增速排序。详细未舍入值与计算程序随结构化源保存。

\topic{数值复算与上游核验分别记录}
本次整章工作核对了归档文件、派生计算、图表读数及文字对应关系，未重新运行全平台OpenRank或账号级去重。原材料中尚缺的生产记录，包括部分地域估计方法、项目历史映射、人才筛选、发布单位样本日期、基金会名单与许可识别规则，继续列入核查清单。

这些缺项约束的是依赖它们的具体判断，不改变已展示表中数值的来源，也不允许将图形完善视为数据认证。正文保留必要范围提示，较长的查询、文件指纹、版本差异和逐项待核状态放入配套记录。

\topic{如何使用这些结果}
本章适合用来理解参与结构、寻找协作节点并确定后续调查对象。对政策效果、人才能力、项目质量和实际采用的判断，仍需结合相应对象的具体证据。将不同层面的观察并列，有助于避免由单项规模指标承担超出其定义的结论。
'''
md+=['\n## 本章小结\n\n七幅地图分别观察参与、贡献、项目、人才、资产、多样性与治理。支持重点是持续任务、共同维护、可复用供给和可查的规则，不是笼统的地区总分。\n',
'## 资料与方法\n\n主统计期：2025-07-01—2026-06-30。地理快照、发布单位累计样本、平台官方窗口、条件估算分别记录。技术分类比例外推尚未验证，不作实测分类结论。详见methods目录与review核查清单。\n']
# Bibliography: include only cited entries plus entries that substantiate chapter method notes.
for s,k in [(21,'usage'),(22,'boundary'),(23,'revision'),(23,'code'),(26,'manifest'),(27,'method'),(25,'research'),(25,'ddownload'),(25,'modelcard')]:
 used.add(keymap[(s,k)])
active=[b for b in bib if b['id'] in used]
# numbers by first registered occurrence, not section-local numbers
bibnum={b['id']:i+1 for i,b in enumerate(active)}
tex+='\n\\clearpage\\pdfbookmark[1]{参考资料}{references}\\renewcommand{\\CurrentSection}{第二章\\quad 参考资料}\n\\subsection*{参考资料}\n'
tex+=r'\begingroup\fontsize{9.8}{14.0}\selectfont\renewcommand{\section}[2]{}\begin{thebibliography}{99}\setlength{\itemsep}{5pt}\setlength{\parskip}{0pt}'+'\n'
for b in active:
 tex+='\\bibitem{'+b['id']+'} '+esc(b['print_title'])+' \\href{'+b['url']+'}{来源入口}。\n'
tex+='\\end{thebibliography}\\endgroup\n\\end{document}\n'
# Final Markdown replacements with section context, generated cleanly for the complete artifact.
md2=['# 第二章 全球开源生态观测地图\n\n整章评审稿 v1.0.0 · 2026-11-05\n',
'## 章首\n\n参与在扩大，生态的不同层面却并不同步。七节由参与进入协作，由项目与人才进入资产，再以多样性和治理解释共同建设的条件。规模、来源、结构与结果分别观察，不构造一个能够替代所有问题的总榜。\n']
for s,o in sections.items():
 for pg in o['pages']:
  md2+=['## '+pg['title']+'\n']
  if pg.get('subtitle'):md2+=[pg['subtitle']+'\n']
  def m(s0):
   t=re.sub(r'\[\[([^\]]+)\]\]',lambda x:'['+str(bibnum.get(keymap[(s,x[1])],'?'))+']',s0)
   return re.sub(r'<<([^>]+)>>',lambda x:next(f['number'] for f in figmanifest if f['label']==labels[(s,x[1])]),t)
  for b in pg['blocks']:
   if b['type'] in ['p','heading','note']:
    txt=m(b['text']);md2 +=[(('### ' if b['type']=='heading' else '')+txt)+'\n']
   elif b['type'] in ['group','figure']:
    for a in b.get('assets',[b.get('asset')]):md2+=['![](figures/'+str(s)+'/'+a+'.svg)\n']
    md2+=['图 '+next(f['number'] for f in figmanifest if f['label']==labels[(s,b['label'])])+' '+b['caption']+'\n']
    if b.get('source'):md2+=[m(b['source'])+'\n']
md2+=['## 本章小结与行动建议\n\n'+ '\n\n'.join(o['pages'][-1]['section_implication']['text'] for o in sections.values())+'\n',
'## 资料与方法\n\n详见chapter2.tex中的资料与方法正文、methods/方法与证据边界.md，以及review/核查清单.md。\n', '## 参考资料\n']
for b in active:md2 +=[f'[{bibnum[b["id"]]}] {b["print_title"]} <{b["url"]}>\n']
(R/'chapter2.tex').write_text(tex)
(R/'chapter2.md').write_text('\n'.join(md2))
(R/'references/references.json').write_text(json.dumps(active,ensure_ascii=False,indent=2))
(R/'review/figure_register.json').write_text(json.dumps(figmanifest,ensure_ascii=False,indent=2))
(R/'review/page_plan.json').write_text(json.dumps(pageplans,ensure_ascii=False,indent=2))
(R/'review/reference_key_map.json').write_text(json.dumps({str(s)+':'+k:v for (s,k),v in keymap.items()},ensure_ascii=False,indent=2))
print('LaTeX written. Body units:',len(pageplans),'figures:',len(figmanifest),'references:',len(active))
