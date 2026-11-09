from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
M={x['figure_number']:x for x in json.loads((R/'review/editorial_map.json').read_text())}
p=R/'content/chapter3_body.tex';s=p.read_text()
def esc(t):return t.replace('%',r'\%').replace('_',r'\_').replace('&',r'\&')
def plate(n):
 m=re.search(r'\\plate\{figures/'+re.escape(M[n]['figure'].split('figures/')[1])+r'\}[^\n]+',s);assert m,n;return m[0]
start=s.index(r'\clearpage'+'\n'+r'\pdfbookmark[2]{3.4.2')
end=s.index(r'\clearpage'+'\n'+r'\pdfbookmark[2]{跨项目共同出现',start)
new=r'''\clearpage
\pdfbookmark[2]{3.4.2 资源与交付：从清单到版本}{resources-delivery}
\subsection*{3.4.2 资源与交付：从清单到版本}
OpenHarmony期末默认源码清单含512项，其中第三方依赖183项、系统框架117项、基础能力109项，提供分解维护责任的起点。

'''+plate(24)+r'''

PyTorch核心仓库主期新增23,777条PR、7,329条Issue，发布7个非预发布版本；后半期PR较前半期增加31.4\%，应进一步核对评审与兼容维护容量。

'''+plate(25)+r'''

\clearpage
\pdfbookmark[2]{3.4.3 贡献接续：平台转换与持续参与}{people-continuity}
\subsection*{3.4.3 贡献接续：平台转换与持续参与}
OpenHarmony主期贡献榜并集有513个平台账号标识；11月起前100条目均来自AtomGit。平台构成转换不等于人员迁移完成。

'''+plate(26)+r'''

PyTorch项目标签榜形成244个账号标识，61个出现9—12个月（25.0\%），105个只出现1—2个月（43.0\%）。持续与阶段性参与并存。

'''+plate(27)+r'''

将贡献榜与固定维护者名册联读，才能进一步检查模块责任、共同维护及替补安排；账号进入榜单本身不证明拥有维护权限。

'''
s=s[:start]+new+s[end:]
start=s.index(r'\clearpage'+'\n'+r'\pdfbookmark[2]{3.4.4')
end=s.index(r'\clearpage\phantomsection\label{ch3-portraits}',start)
new=r'''\clearpage
\pdfbookmark[2]{3.4.4 复用与维护：依赖约束与责任接续}{reuse-maintenance}
\subsection*{3.4.4 复用与维护：依赖约束与责任接续}
期末vLLM与SGLang均声明PyTorch及Transformers依赖，具体版本与启用方式不同。使用方需要核对兼容条件和支持期限。

'''+plate(30)+r'''

'''+plate(31)+r'''



'''
s=s[:start]+new+s[end:]
p.write_text(s)
(R/'atlas/pageoffset.tex').write_text(r'\setcounter{page}{31}'+'\n')
(R/'review/compact_page_groups.json').write_text(json.dumps({'paired_figures':[[24,25],[26,27],[30,31]],'preserved':'All 40 numbered figures, complete rankings, and both A3 portraits','narrative_detail':'Detailed original commentary archived; overlapping technical evidence retained in the A3 portraits'},ensure_ascii=False,indent=2))
