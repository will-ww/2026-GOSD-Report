from common import *
from section41 import render,DATA
if not all((B/'fonts'/f'Noto{family}CJKsc-{weight}.otf').exists() for family in ['Sans','Serif'] for weight in ['Regular','Bold']):ensure_fonts()
export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
pages=render()
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
for i,p in enumerate(pages):
    atlas=True
    tex+=rf'\begin{{canvas}}\Header{{第四章 · 全球开源技术生态}}{{teal}}\Footer{{{i+1:02}}}'+'\n'
    tex+=rf'\pdfbookmark[1]{{{esc(p["title"])}}}{{page{i+1}}}'+'\n'
    tex+=box(15,27,180,p['title'],20,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
    tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
    tex+=box(15,217 if atlas else 199,180,p['caption'],7.6,10.7,'muted',False,True)
    for j,(title,body) in enumerate(p['analyses']):
        x=15+(j%2)*93;y=(233+(j//2)*25) if atlas else (213+(j//2)*34)
        tex+=box(x,y,87,title,10.3,14.2,'teal',True)+box(x,y+6,87,body,9.4 if atlas else 9.9,13.5 if atlas else 15)
    tex+=r'\end{canvas}'+'\n'
# One concise reader-facing appendix; technical request and review questions live outside the PDF.
tex+=r'\begin{canvas}\Header{附录 A · 4.1 数据与阅读说明}{teal}\Footer{05}\pdfbookmark[1]{附录 A · 数据与来源}{appendixa}'+'\n'
tex+=box(15,27,180,'附录 A　4.1 数据与阅读说明',20,27,'ink',True)
tex+=box(15,42,180,'本节保留完整功能全景，并分别以项目、类别和贡献者地域观察协作影响。主统计期榜单与期后国家样本分开呈现，不能拼接为同一时点的技术实力排名。',10.2,16,'muted',False,True)
tex+=box(15,64,180,'一、全景名单与项目榜单',12,17,'teal',True)
tex+=box(15,74,180,'全景依据蚂蚁 Agentic AI Landscape 的 2026 年 9 月 27 日固定版本，共 145 项、25 类。按主要功能每项只列一处；位置和面积不表示排名。名单用于回看历史，部分项目在主期后出现，入选也不等于通过开源许可认证。',10.1,16)
tex+=box(15,99,180,'图 4-3 使用 2025 年 7 月至 2026 年 6 月的月度 OpenRank 合计，按主要仓库识别项目。数据库于 2026 年 11 月 10 日提取，共 1,529 条项目月记录，与原固定快照核对一致；143 项至少有一个月的记录，107 项连续记录完整。缺值不补零，分值不是平均质量或市场份额。',10.1,16)
tex+=box(15,129,180,'全景 † 表示没有 2026 年 6 月分值：DeepSeek Harness、ZCode 在主期后创建；page-agent、Label Studio 当月缺记录。榜单按未取整分值排序；子类分值为类内仓库合计，不把同一仓库重复计入不同类别。',10.1,16)
tex+=box(15,155,180,'二、国家贡献：期后公开子样本',12,17,'teal',True)
tex+=box(15,165,180,'图 4-4 采用 OpenDigger 公开项目标签的 contributions 数据，与 OpenShare 国家贡献组件同源。导出逻辑汇总当时近一年的归一化社区 OpenRank，再按贡献者所在地分组；2026 年 11 月 10 日读取的文件没有逐一记录这部分数据的精确起止日。',10.1,16)
tex+=box(15,195,180,'为避免重复累计，排除成员范围重叠或与其他入样标签相交的标签，保留 96 项、覆盖 24 类。标签可能含同一项目的多个仓库，不能等同于图 4-3 的主要仓库样本。未识别地域贡献未随公开文件导出，图中份额仅以已识别部分为分母；跨项目开发者人数不相加。',10.1,16)
tex+=box(15,225,180,'国家图尚未覆盖 49 项，包括 PyTorch、OpenClaw、vLLM、SGLang 等重要项目。因此仅用于审视分层观察方式及可核验样本，不支持认定整个全景的国家领先位置。完整年度榜需以同一 145 项、同一主统计期的国家贡献汇总替换。',10.1,16)
tex+=box(15,254,180,'主要来源',10.5,15,'teal',True)
refs=[('蚂蚁 Agentic AI Landscape · 固定分类与标识资源','https://github.com/antgroup/agentic-ai-landscape/tree/e330d75ea4ca314bc81f6868df63425c8acca5e3'),('OpenDigger · 指标定义、数据库与国家贡献导出逻辑','https://github.com/X-lab2017/open-digger/blob/5c2ffc4f5b3dd37ebcb20514c7abfee6853bd830/src/cron/tasks/monthlyExport.ts')]
for i,(lab,url) in enumerate(refs):
    tex+='\\Box{15}{'+str(262+i*6)+'}{180}{\\sffamily\\fontsize{8.6}{12}\\selectfont\\href{'+url+'}{'+esc(lab)+'}}\n'
tex+=r'\end{canvas}\end{document}'
(R/'report.tex').write_text(tex);(D/'content-41.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2));(R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
compile_tex()
doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':'GOSD 2026 精要版｜4.1 Agentic AI 全景洞察｜评审稿 v0.4','author':'全球开源发展报告编制组','subject':'完整全景、四层项目排名与期后国家贡献子样本；年度国家榜待补齐','keywords':'GOSD,Agent Infra,Model Infra,OpenRank,国家贡献,公开子样本'})
final=O/'GOSD_2026_Section_4.1_Review_v0.4.pdf';doc.save(final,garbage=4,deflate=True);doc.close();doc=fitz.open(final)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.8,1.8)).save(R/'review'/f'page-{i+1:02}.png')
print('PAGES',len(doc));print(json.dumps([q for q in QA if q['out_of_bounds'] or q['overlaps']],ensure_ascii=False))
