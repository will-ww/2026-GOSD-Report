from build import *
from assets_v03 import render

for p in [B/'assets',B/'fonts',B/'texmf-var',O,F,R/'review']:p.mkdir(parents=True,exist_ok=True)
ensure_fonts()
export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
PAGES=render()
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
for i,p in enumerate(PAGES):
    tex+=rf'\begin{{canvas}}\Header{{第二章 · 全球开源生态地图}}{{teal}}\Footer{{{i+1:02}}}'+'\n'
    tex+=box(15,27,180,p['title'],20,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
    tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
    tex+=box(15,199,180,p['caption'],7.6,10.7,'muted',False,True)
    for j,(title,body) in enumerate(p['analyses']):
        x=15+(j%2)*93;y=212+(j//2)*34
        tex+=box(x,y,87,title,10.3,14.2,'teal',True)+box(x,y+6,87,body,9.9,15)
    tex+=r'\end{canvas}'+'\n'

LINKS=[
('S1','GitHub Innovation Graph · repositories.csv / Datasheet','https://github.com/github/innovationgraph/blob/main/data/repositories.csv'),
('S2','GitHub Octoverse 2026 · 提交、推送与公开贡献','https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/'),
('S3','GOSD 归档原表 · 活跃仓库、模型及数据地域样本','https://github.com/will-ww/2026-GOSD-Report/tree/497478a19e92c676c225893a395738e747a71c8b/reports/round2-v2.0/source/chapters/02/modules/02/data/25'),
('S4','Hugging Face · State of Open Models: Summer 2026 Observations','https://huggingface.co/blog/state-of-open-models-summer-2026'),
('S5','Hugging Face · State of Open Source on Hugging Face: Spring 2026','https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026'),
('S6','AI World / F. Ríos · Hugging Face’s Two Million Models and Counting','https://aiworld.eu/story/hugging-faces-two-million-models-and-counting'),
('S7','Longpre et al. · The Economies of Open Intelligence · Figure 1','https://www.dataprovenance.org/economies-of-open-intelligence.pdf')]
tex+=r'\begin{canvas}\Header{附录 1 · 2.5 口径与来源}{teal}\Footer{A1}'+'\n'
tex+=box(15,28,180,'附录 1｜资产口径与证据来源',20,27,'ink',True)
def head(y,t):return box(15,y,180,t,11,16,'teal',True)
tex+=head(45,'1  本节中的“资产”与地域含义')
tex+=box(15,54,180,'本节以可见仓库观察资源供给：代码仓库是保存代码及协作记录的空间，模型仓库存放模型权重和配置，数据集仓库存放训练、评测等材料。公开可访问不自动等于符合开源许可；本节不把数量解释为技术质量、资产估值或开源合规数量。模型／数据归属发布单位，下载不代表使用者所在地。',9.3,14.4)
tex+=head(84,'2  图中数量怎样取得与计算')
tex+=box(15,93,180,'代码地图：GitHub Innovation Graph 季末公开仓库存量，按具备 triage（事务分拣）及以上权限成员的地域众数归属；包括不活跃仓库。排除欧盟汇总行以免重复，中国合并内地、香港、澳门和台湾。4.54 亿为已披露地域合计；历史曲线均取第二季度。活跃仓库沿用报告原表，主期为 2025.07—2026.06；平台间不相加，也不与公开存量计算“活跃率”。',9.3,14.4)
tex+=box(15,129,180,'HF 地域样本：826 家发布单位、63 个国家与地区；原表分别列出 14 个地域，未列明不补零，快照日期与筛选细节待核。平台增长使用 HF 夏季材料的 1 月与 8 月端点，含期后观察；模型日度曲线截至 2025-12-08。下载结构比较“全历史模型”与 2024.08—2025.08 新发布模型，沿用原研究滚动窗口过滤，不能视为同口径年度市场份额变化。',9.3,14.4)
tex+=head(164,'3  可追溯来源 · 2026-11-10 检索；点击条目访问原文')
for i,(tag,t,u) in enumerate(LINKS):
    tex+=r'\Box{15}{'+str(174+i*7)+r'}{180}{\sffamily\fontsize{8.9}{12}\selectfont '+tag+r'\quad\href{'+u+'}{'+esc(t)+'}}\n'
tex+=head(229,'4  v0.3 修订与本轮评审')
tex+=box(15,238,180,'本轮将原三页改为四页地图组合：三类资产总览、代码、模型、数据，共 16 个分析点。新增公开仓库地域底表、历史增长曲线、模型日度增长、下载群体比较；保留正文中的通俗解释。图号暂为 2-13—2-16，合稿时顺延下节。',9.3,14.4)
tex+=box(15,263,180,'待核查：HF 地域样本快照日期及筛选细节、活跃仓库的底层事件规则。评审重点：总览的三资产整合是否清晰；四页的证据与洞察是否足以支撑执行摘要及第六章。',9.3,14.4)
tex+=r'\end{canvas}\end{document}'
(R/'report.tex').write_text(tex)
(D/'content.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2))
(D/'sources.json').write_text(json.dumps(LINKS,ensure_ascii=False,indent=2))
(R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
compile_tex()
doc=fitz.open(O/'report.pdf')
doc.set_metadata({'title':'GOSD 2026 精要版｜2.5 全球开源资产地图｜评审稿 v0.3','author':'全球开源发展报告编制组','subject':'四幅地图组合图；2026-11-10；待作者评审'})
doc.set_toc([[1,p['title'],i+1] for i,p in enumerate(PAGES)]+[[1,'附录 1｜资产口径与证据来源',len(PAGES)+1]])
out=O/'GOSD_2026_Section_2-5_Review_v0.3.pdf';doc.save(out,garbage=4,deflate=True);doc.close();doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.7,1.7)).save(R/'review'/f'page-{i+1}.png')
print('BUILT',out,len(doc));print(json.dumps(QA,ensure_ascii=False))
