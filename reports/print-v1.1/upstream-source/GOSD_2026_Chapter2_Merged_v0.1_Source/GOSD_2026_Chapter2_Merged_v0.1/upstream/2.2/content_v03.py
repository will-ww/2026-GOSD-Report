from build import *
from panels_v02 import GS,NS,GR,GT,NAT,NATCN,NPAR

NARRATIVES=[
 [
 ['① 贡献分布于多个地域节点','在 2026 报告年度公开估计中，美国贡献度为 332.10 万，德国、中国和英国分别为 110.77 万、93.68 万和 78.85 万。地图呈现主要贡献节点，欧洲多个国家共同构成重要贡献基础。'],
 ['② 贡献版图补充了人数视角','2026 年度，荷兰、瑞士的贡献位次为第 10 和第 13，活跃位次分别为第 15 和第 25。贡献位置有助于识别不同类型的合作伙伴；具体优势仍需进入组织、项目与技术领域继续观察。'],
 ['③ 位次与平均贡献，解释不同结构','2025 同表快照中，德国、荷兰的平均贡献分别为 1.143、1.131，中国为 0.516。该指标把总量与参与基础结合起来，是地区结构的补充视角；不能据此评价每位开发者的质量或效率。'],
 ['④ 五域综合序列提供另一组观察','2026 年度五域中，欧洲、中国和美国分别为 650.16 万、442.92 万和 423.97 万。它与国家公开估计的覆盖不同，应在各自范围内分析；两种中国读数的差额不全部归因于国内平台。']
 ],
 [
 ['① 中国的相对位置具有上升空间','以五域历史增速延续或逐步放缓推演，2030 年中国综合贡献为 935—1,469 万，欧洲为 787—895 万。两种情景均提示中国相对位置可能继续上升；这取决于持续协作与统计覆盖的稳定。'],
 ['② 全球增长之中，地区节奏不同','2021—2025 自然年，中国贡献读数增长 51.1%，全球、美国分别增长 36.7%、24.4%。按相同情景方法，2030 年中国为 161—203 万。自然年与上方五域覆盖不同，不直接比较两组规模。'],
 ['③ 从参与扩展，走向持续贡献','2026 年度六国公开读数中，巴西贡献度为 43.43 万，约占六国合计的 58.1%；印度尼西亚与越南分别为 10.66 万、8.93 万。全球南方内部的基础与协作位置存在差异。AI 普惠合作应围绕真实项目配置本地化、贡献辅导与维护资源，并在发布后 6—12 个月观察贡献采纳、跨境参与和持续维护；长期情景则随新数据定期修订。']
 ],
 [
 ['① 主要地区构成中国贡献基础','2026 报告年度，京沪粤合计占全国贡献度约 52.9%，与其活跃份额 52.6% 接近。头部地区聚集大量参与和贡献，其他地区也共同支撑生态；省级汇总不能替代城市与产业分工分析。'],
 ['② 完整前 20 展示更多区域层次','北京、上海贡献度分别为 19.93 万和 18.00 万；台湾、浙江为 11.61 万和 11.19 万。四川贡献位次为第 6、活跃位次为第 7。地方支持需要继续连接当地组织、项目和维护团队。'],
 ['③ 同期份额对照，观察区域贡献结构','2026 年度，台湾与浙江合计占全国活跃人数的 18.9%、贡献度的 24.3%，贡献份额高约 5.5 个百分点。其余地区的活跃、贡献份额为 28.6%、22.7%。这提示各地参与基础与贡献结构不同，支持资源应结合本地项目与维护需求配置。'],
 ['④ 平均贡献形成另一种地区次序','2025 同表比较中，浙江、台湾、上海、四川平均贡献分别为 0.655、0.644、0.605、0.540，高于全国比值 0.516。该指标补充规模比较，不代表个人能力；浙江的表现为研究杭州等城市提供线索，机制仍需产业与项目证据。']
 ],
 [
 ['① 中国参与全球接续与共同建设','样本显示双向贡献：中国开发者向美国项目贡献 24,420.69 OpenRank，美国开发者向中国项目贡献 1,980.46。两组项目与分母不同，不能据此推断国家净输出，但可以识别真实的协作连接。'],
 ['② 本土支撑与跨境参与共同存在','中国项目样本的本土贡献为 79.22%，已列境外来源为 14.02%；美国项目相应为 38.28%、39.66%。本土建设提供基础，跨境参与扩大连接；未列部分保留为未知，不全部计为境外贡献。'],
 ['③ 来源集中程度呈现不同参与结构','中国项目前三来源占 87.03%，美国项目为 52.93%；前十分别覆盖 93.24%、77.94%。两组样本的贡献来源集中程度不同，可为拓展合作伙伴提供线索；不能单独用来判断项目开放程度或国家竞争力。'],
 ['④ 从开放发布走向可持续共建','面向模型、工具链与数据项目，基金会和维护团队可通过多语文档、贡献辅导、公开审查与共同维护扩大参与。下一步应跟踪境外贡献采纳和维护职责，检验开放资源能否转为可持续公共能力。']
 ]]

LINKS=[
 ('OpenShare 宏观洞察（自然年）','https://open-share.com/insight/open-world'),
 ('OpenShare GOSD（报告年度）','https://open-share.com/insight/open-world/gosd'),
 ('自然年贡献 JSON','https://selfoss.open-digger.cn/openshare/overview/contribution.json'),
 ('报告年度贡献 JSON','https://selfoss.open-digger.cn/openshare/overview_half_year/contribution.json'),
 ('自然年活跃 JSON','https://selfoss.open-digger.cn/openshare/overview/developers.json'),
 ('中国自然年贡献 JSON','https://selfoss.open-digger.cn/openshare/overview/CN/contribution.json'),
 ('中国自然年活跃 JSON','https://selfoss.open-digger.cn/openshare/overview/CN/developers.json'),
 ('中国报告年度贡献 JSON','https://selfoss.open-digger.cn/openshare/overview_half_year/CN/contribution.json'),
 ('五域及项目来源归档','https://github.com/will-ww/2026-GOSD-Report/tree/497478a19e92c676c225893a395738e747a71c8b/reports/round2-v2.0/source/chapters/02/modules/02/data/22'),
 ('中美来源样本与分母说明','https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/c51e3441361407b68f10b339d97eff288319b503/preview/content/cmap/flow-method.md'),
 ('OpenDigger 社区 OpenRank','https://open-digger.cn/docs/user-docs/metrics/community-openrank'),
 ('公开数据生产代码','https://github.com/X-lab2017/open-digger/blob/5c2ffc4f5b3dd37ebcb20514c7abfee6853bd830/src/dataProduction/openshareOverview.ts')
]

def heading(y,title):return box(15,y,180,title,11.6,17,'teal',True)

def make_tex():
    titles=['2.2 全球开源贡献地图','2.2 贡献增长与 2030 情景','2.2 中国贡献：规模、结构与平均','2.2 全球协作：从参与到共同建设']
    intros=[
    'OpenRank 贡献度以项目协作网络衡量开发者贡献，再按所在地汇总。地图与排行为 2026 报告年度；平均贡献采用 2025 自然年同表快照。',
    '历史曲线回答增长发生在哪里，2030 情景展示不同假设下的可能路径。实线为历史，虚线为推演；五域按报告年度，全球与中美按自然年。',
    '地图与排行观察贡献的地域分布，区域份额比较同一时期的参与和贡献；平均贡献补充历史结构。四个视角联合阅读，分别标明统计时期。',
    '贡献在参与、审查与维护中进入共同项目。本图将来源网络、参与结构、来源集中程度与明细联读，观察中国如何连接全球社区。'
    ]
    captions=[
    '图 2-4  全球贡献全景、位次与平均贡献。来源：OpenDigger / OpenShare；五域来自编制组。①②④为 2026 报告年度，③为 2025 自然年；平均值不是个体质量评分。',
    '图 2-5  贡献历史与 2030 条件情景。来源：OpenShare 自然年及 GOSD 年度输出、编制组五域序列；情景由本报告测算。区间为两种假设的结果，不赋予发生概率。',
    '图 2-6  中国贡献分布、区域份额与平均贡献。来源：OpenDigger / OpenShare。①②③为 2025.07—2026.06；④为 2025 自然年。份额各以全国合计为分母，平均贡献采用同期同表数据。',
    '图 2-7  全球协作网络、来源结构与集中程度。来源：编制组中美项目来源前十表，统计期 2025.07—2026.06。箭头表示贡献方向；各项目样本份额分别计算。'
    ]
    names=['01-contribution-map','02-contribution-evolution','03-china-collaboration','04-global-collaboration']
    tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
    for i in range(4):
        tex+=rf'\begin{{canvas}}\Header{{第二章 · 全球开源生态地图}}{{teal}}\Footer{{{i+1:02}}}\pdfbookmark[1]{{{titles[i]}}}{{page{i+1}}}'+'\n'
        tex+=box(15,27,180,titles[i],21,27,'ink',True)+box(15,40,180,intros[i],9.7,13.5,'muted',False,True)
        tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{names[i]}.pdf}}}}'+'\n'
        tex+=box(15,199,180,captions[i],7.8,10.8,'muted',False,True)
        if len(NARRATIVES[i])==4:
            for j,(title,body) in enumerate(NARRATIVES[i]):
                x=15+(j%2)*93;y=211+(j//2)*34
                tex+=box(x,y,87,title,10.5,14.2,'teal',True)+box(x,y+6,87,body,10.1,15.6)
        else:
            for j,(title,body) in enumerate(NARRATIVES[i][:2]):tex+=box(15+j*93,211,87,title,10.5,14.2,'teal',True)+box(15+j*93,217,87,body,10.1,15.6)
            title,body=NARRATIVES[i][2];tex+=box(15,247,180,title,10.5,14.2,'teal',True)+box(15,253,180,body,10.2,16)
        tex+=r'\end{canvas}'+'\n'
    tex+=r'\begin{canvas}\Header{附录 1 · 2.2 指标与情景方法}{teal}\Footer{A1}\pdfbookmark[1]{附录1 指标、时期与情景方法}{app1}'+'\n'
    tex+=box(15,28,180,'附录 1｜指标、时期与情景方法',20,27,'ink',True)
    tex+=heading(47,'1  贡献度与平均贡献')
    tex+=box(15,57,180,'OpenRank 以协作网络刻画贡献关系。本节汇总开发者贡献，项目影响力另在 2.3 讨论。平均贡献 = 地区贡献度 ÷ 同表、同期活跃开发者数，单位为 OpenRank／人；它是地区汇总比值，不是个人贡献的中位数，也不直接测量质量、效率或社会成效。',10,16)
    tex+=heading(87,'2  时间与覆盖明确分开')
    tex+=box(15,97,180,'当期图：国家与省级贡献图、南方六国细分采用 2026 报告年度，即 2025-07-01 至 2026-06-30。五域历史为 2022—2026 报告年度，其 2030 情景段始于 2027；该综合序列与国家公开估计覆盖不同，不混排、不相加。',9.8,15.5)
    tex+=box(15,125,180,'历史比较：平均贡献采用 2025 自然年同表数据；全球、美国、中国趋势采用 OpenShare 自然年入口的 2021—2025 数据。对应情景从 2026 开始，2026 点也是推演值；不将 2026 报告年度读数拼入自然年曲线。',9.8,15.5)
    tex+=box(15,153,180,'地域读数包含估计。当前生产代码说明按可识别地域占比估算、中国另补国内平台，并含年度数值调整；代码与已发布 JSON 的版本对应仍待核验。南方六国指巴西、印度尼西亚、越南、南非、菲律宾、埃及，不代表全球南方总体。',9.6,15.3)
    tex+=heading(183,'3  2030 情景如何计算')
    tex+=box(15,193,180,'各序列独立计算历史年均增速 g =（末年读数 ÷ 首年读数）的四次方根 − 1。延续情景：从历史终点起，每年按 g 复利增长。放缓情景：第 h 个推演年的增速为 g × 0.8 的 h 次方，逐年复利。五域推演四年，自然年序列推演五年。',9.8,15.5)
    tex+=box(15,221,180,'0.8 为预设敏感性参数，两条路径不是概率分布或置信区间。测算沿用已发布序列，未单独估计 AI 的因果效应，也未剔除统计调整。解释成立需覆盖、地区映射及指标版本保持可比；每年加入新数据重算。',9.6,15.2)
    tex+=heading(249,'4  协作网络与来源集中程度')
    tex+=box(15,259,180,'中美各前十来源共 20 条记录、14 个来源国家。前 N 来源份额为原表前 N 项相加，各项目样本分母不同；未列份额不补入任何国家。样本未附完整项目清单，结果不代表中美所有项目，也不推断人员迁移或国家净输出。',8.8,12.8)
    tex+=r'\end{canvas}'+'\n'
    tex+=r'\begin{canvas}\Header{附录 1 · 读数、出处与评审}{teal}\Footer{A2}\pdfbookmark[2]{情景读数、出处及评审记录}{app2}'+'\n'
    tex+=box(15,28,180,'情景读数、出处与评审记录',20,27,'ink',True)
    tex+=heading(45,'5  五域历史与 2030 情景｜万 OpenRank')
    table=r'\sffamily\fontsize{8.8}{12}\selectfont\renewcommand{\arraystretch}{1.13}\setlength{\tabcolsep}{3.8pt}\begin{tabularx}{180mm}{@{}Xrrrrrr@{}}\toprule 报告年度 & 2022 & 2023 & 2024 & 2025 & 2026 & 2030 放缓—延续\\\midrule'+'\n'
    for key,name,c in GR:
        s=GS[key];table+=name+'&'+'&'.join(f'{v:,.2f}' for v in s['history'])+f'&{s["slowing"][-1]:,.2f}—{s["continued"][-1]:,.2f}'+r'\\'+'\n'
    table+=r'\bottomrule\end{tabularx}';tex+=rf'\Box{{15}}{{56}}{{180}}{{{table}}}'+'\n'
    tex+=heading(98,'6  自然年历史与 2030 情景｜万 OpenRank')
    table=r'\sffamily\fontsize{8.8}{12}\selectfont\renewcommand{\arraystretch}{1.13}\setlength{\tabcolsep}{3.8pt}\begin{tabularx}{180mm}{@{}Xrrrrrr@{}}\toprule 自然年度 & 2021 & 2022 & 2023 & 2024 & 2025 & 2030 放缓—延续\\\midrule'+'\n'
    for key,s in NS.items():table+=key+'&'+'&'.join(f'{v:,.2f}' for v in s['history'])+f'&{s["slowing"][-1]:,.2f}—{s["continued"][-1]:,.2f}'+r'\\'+'\n'
    table+=r'\bottomrule\end{tabularx}';tex+=rf'\Box{{15}}{{109}}{{180}}{{{table}}}'+'\n'
    tex+=box(15,140,180,'历史与情景分开，按未舍入读数计算。来源读取日：2026-11-09；OpenShare 元数据更新日：2026-10-08。',8.5,12.5,'muted')
    tex+=heading(157,'7  资料出处｜点击可查看原始资料')
    for i,(label,url) in enumerate(LINKS):
        x=15+(i%2)*93;y=168+(i//2)*7
        tex+='\\Box{'+str(x)+'}{'+str(y)+'}{87}{\\sffamily\\fontsize{8.7}{11.5}\\selectfont\\href{'+url+'}{['+str(i+1)+'] '+label+'}}\n'
    tex+=heading(217,'8  v0.3 评审记录 · 2026-11-09')
    tex+=box(15,227,180,'本轮修改：第三幅恢复“参与与贡献 · 区域份额”，与地图、前 20、平均贡献组成四个图表单元；配套扩充为四个分析点。份额按 34 地同表数据重算，百分点差采用未舍入值。全文仍为四页正文、两页附录，PDF 未提交 GitHub。',9.4,14.7)
    tex+=box(15,250,180,'待核查：五域欧洲成员与历史覆盖；公开数据生产版本；项目来源完整清单；地图出版审图。底图沿用 2026 版，中国包括台湾、香港、澳门。当前图表是上述统计范围内的展示，不替代发布前核验。',9.2,14)
    tex+=box(15,272,180,'评审重点：第三幅四单元是否清晰、密度适当；区域份额与平均贡献的时期、含义是否区分充分。',8.1,11.5,'muted')
    tex+=r'\end{canvas}\end{document}'
    (R/'report.tex').write_text(tex)
    (R/'content.json').write_text(json.dumps({'version':'0.3','status':'待作者PDF评审','body_pages':4,'appendix_pages':2,'titles':titles,'intros':intros,'captions':captions,'narratives':NARRATIVES,'sources':LINKS,'integration_candidates':{'I01':'参与规模、贡献总量和平均贡献呈现不同地域结构。','I06':'项目样本中，中国参与双向跨境贡献；本土基础与国际连接需要共同建设。','I07':'全球南方合作需要按参与路径和本地能力差异配置资源。','I10':'中国地区的贡献规模与平均贡献具有差异，城市机制另需研究。','chapter6':'发布后6—12个月追踪采纳与维护；长期情景以统一覆盖的新增观察年度滚动更新。'},'new_fourth_figure':'地图+来源结构+累计集中度+中美各前十明细；不将机制示意冒充实际事件'},ensure_ascii=False,indent=2))
