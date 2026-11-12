from build import R, O, B, SC, GS, GROUPS, NAMES, PROVINCES, SOUTH, box, esc
import json

def make_tex():
    style=(R/'layout.sty').read_text().replace('v0.2','v0.3')
    if '% PORTRAIT V03' not in style:
        style+=r'''
% PORTRAIT V03
\RequirePackage{booktabs,tabularx,array}
\renewcommand{\Header}[2]{\Box{15}{10}{135}{\sffamily\fontsize{7.7}{10}\selectfont\color{muted}\raisebox{-2.1mm}{\includegraphics[width=7mm]{.build/assets/osdgs-compact.pdf}}\hspace{2mm}\textbf{GOSD 2026}\quad 全球开源发展报告·精要版}\Box{149}{12.7}{46}{\raggedleft\sffamily\fontsize{7.7}{10}\selectfont\color{muted}#1}\Rule{15}{21}{195}{line}\Rect{15}{20.6}{12}{.8}{#2}\Rect{133}{20.7}{5}{.5}{trail0}\Rect{139.2}{20.7}{5}{.5}{trail1}\Rect{145.4}{20.7}{5}{.5}{trail2}\Rect{151.6}{20.7}{5}{.5}{trail3}\Rect{157.8}{20.7}{5}{.5}{trail4}\Rect{164}{20.7}{5}{.5}{trail5}\Rect{170.2}{20.7}{5}{.5}{trail6}\Rect{176.4}{20.7}{5}{.5}{trail7}\Rect{182.6}{20.7}{5}{.5}{trail8}\Rect{188.8}{20.7}{5}{.5}{trail9}}
\renewcommand{\Footer}[1]{\Rule{15}{283}{195}{line}\Small{15}{286}{155}{OPEN SOURCE / A SHARED INTELLIGENT FUTURE}\Box{182}{284.7}{13}{\raggedleft\digits\fontsize{11}{13}\selectfont\color{navy}#1}}
'''
    (R/'layout.sty').write_text(style)
    narratives=[
      [
       ['① 多中心参与，构成全球合作基础','美国、印度、中国和巴西是本图规模较大的节点；欧洲由多个相邻国家共同构成参与网络。地图帮助发现合作基础，参与人数还不能直接代表技术质量、AI 研发实力或公共成效。'],
       ['② 排名之外，也要看见更多参与者','前 20 名把空间位置转为可比较的读数。除既有欧美节点外，印度、巴西、印度尼西亚等已形成可观参与规模；国际合作布局需要同时看见现有中心与成长中的社区。'],
       ['③ 用户基础扩大，持续协作更关键','2022—2026 年，累计规模增长 131.7%，当期活跃增长 87.3%。两者并不同步，生态评价需要继续观察贡献采纳和长期维护；这一差异不能解释为同一批用户的留存下降。'],
       ['④ 跨平台观察，补全中国参与图景','五域中国为 454.5 万，采用独立综合统计。GitHub 250.48 万加国内平台去重补充约 120 万，跨平台约 370 万；补充扩大了可见范围，不再叠加到五域读数。']
      ],
      [
       ['① 增长与积累，形成不同的地域优势','2022—2026 年，南方六国综合组和印度的年均增速分别为 22.2% 和 21.3%，高于欧美比较组。若这些增长条件延续，其相对规模可能提高；欧洲仍保持较大的参与基础。'],
       ['② 把长期预测变成可更新的条件判断','三条小图分别追踪全球累计、全球活跃和中国 GitHub 活跃，避免把注册增长等同于持续参与。2030 范围来自“历史延续”和“逐步放缓”两种假设，每年应以同口径数据重算。'],
       ['③ 全球南方内部，合作需求同样具有差异','在六国 GitHub 细分中，巴西占活跃规模的 61.5%；菲律宾和印度尼西亚的同比增速分别为 12.5% 和 11.5%，快于巴西的 7.4%。AI 普惠合作需要同时支持已有节点与成长社区，由基金会、项目团队和本地伙伴共同提供本地化、导师与维护资源，并以实际采纳和持续贡献检验成效。']
      ],
      [
       ['① 头部集聚与广泛参与并存','全国 GitHub 活跃规模约 250.48 万，同比净增 30.40 万。京沪粤占当期活跃的 52.6%，形成主要参与基础；其余地区共同构成跨区域协作的重要支撑，不能仅以头部排行概括中国。'],
       ['② 现有规模与当期增量联合阅读','北京、上海、广东的净增分别约为 6.45 万、5.07 万和 4.39 万。前 20 表同时列出活跃与净增，帮助地方决策者区分参与基础和年度变化；净增并不等于人才迁入或首次参与。'],
       ['③ 浙江等地区展现更快增长','台湾、浙江的活跃规模同比增长 19.2% 和 16.1%，高于全国的 13.8%；浙江同时拥有 23.29 万的活跃基础。省级差异为后续产业与人才观察提供线索，不能直接替代杭州等城市的证据。'],
       ['④ 增量结构提示区域合作机会','台湾与浙江占当期活跃的 18.9%，占同比净增的 23.3%，相差约 4.4 个百分点。地方支持应进一步连接产业项目、组织与维护团队，判断参与增长能否转化为持续供给和协作能力。']
      ]
    ]
    content={'version':'0.3','status':'待作者评审','pages':narratives,'synthesis':{
      'summary':'全球开源的参与积累与成长速度呈现不同地域格局。跨平台观察补全中国参与图景，全球南方也需要按国家和参与路径区分。人工智能时代的政策重点，应从扩大可见参与进一步转向真实贡献、长期维护和可持续公共能力。',
      'outlook':'2030为条件情景；印度及南方六国的相对参与规模可能提高，成立条件是同口径增长延续并形成持续贡献。各年度以新观察修订，发布后6—12个月先检验贡献采纳与维护条件。',
      'recommendation':'基金会、项目维护团队与本地高校或社区共同选择真实项目，提供本地化、导师和维护资源，以采纳、持续参与及维护责任衡量效果。'},
      'sources':{'OpenShare_GOSD':'https://open-share.com/insight/open-world/gosd','read_date':'2026-11-09','report_period':'2025-07-01/2026-06-30','five_groups':'编制组2026版确认的综合序列','china_local_supplement':'编制组已核实，国内平台去重补充约120万，跨平台约370万'},
      'changes':['全部A4竖版','三页综合图与圈号解读','首图四块完整呈现','恢复中国五域454.534万','确认中国跨平台约370万','补齐全球/中国三条趋势情景','新增南方六国细分与同比','中国前20、同比及存量增量份额']}
    (R/'content.json').write_text(json.dumps(content,ensure_ascii=False,indent=2))
    tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
    titles=['2.1 全球开源活跃地图','增长版图与 2030 情景','中国区域参与结构']
    intros=[
      '活跃开发者指报告期内留下公开活动记录的账号；累计规模还包括当期未活跃账号。地图和排行采用 GitHub 口径，五域另用综合统计。',
      '实线为 2022—2026 报告年度；虚线为 2027—2030 条件情景。五域综合趋势与南方六国 GitHub 细分分别展示，覆盖不同。',
      '将现有参与基础、同比净增与增长速度联合观察。统一采用 GitHub 地理统计，国内平台补充未按省级分摊。'
    ]
    captions=[
      '图 2-1  全球参与全景与平台覆盖。来源：OpenDigger / OpenShare（GOSD 年度统计）；五域及国内平台补充由报告编制组提供。主统计期：2025.07—2026.06。',
      '图 2-2  历史增长、2030 条件情景与南方六国细分。来源：OpenDigger / OpenShare、编制组五域序列及情景测算。情景不赋予概率；方法与完整读数见附录 1。',
      '图 2-3  中国参与基础、同比增长与区域份额。来源：OpenDigger / OpenShare；省级值按平台地理估计阅读。同比为 2026 较 2025 报告年度；各份额独立取整。'
    ]
    names=['01-global-current','02-trends-2030','03-china-regions']
    for i in range(3):
        tex+=rf'\begin{{canvas}}\Header{{第二章 · 全球开源生态地图}}{{teal}}\Footer{{{i+1:02}}}\pdfbookmark[1]{{{titles[i]}}}{{page{i+1}}}'+'\n'
        tex+=box(15,27,180,titles[i],21,27,'ink',True)
        tex+=box(15,40,180,intros[i],9.7,13.5,'muted',False,True)
        tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{names[i]}.pdf}}}}'+'\n'
        tex+=box(15,199,180,captions[i],7.8,10.8,'muted',False,True)
        if i!=1:
            for j,(t,p) in enumerate(narratives[i]):
                x=15+(j%2)*93;y=211+(j//2)*34
                tex+=box(x,y,87,t,10.5,14.2,'teal',True)
                tex+=box(x,y+6,87,p,10.1,15.6)
        else:
            for j,(t,p) in enumerate(narratives[i][:2]):
                x=15+j*93;tex+=box(x,211,87,t,10.5,14.2,'teal',True)+box(x,217,87,p,10.1,15.6)
            t,p=narratives[i][2];tex+=box(15,247,180,t,10.5,14.2,'teal',True)+box(15,253,180,p,10.2,16)
        tex+=r'\end{canvas}'+'\n'
    # Appendix 1: definitions and source provenance without workflow jargon.
    tex+=r'\begin{canvas}\Header{附录 1 · 口径与来源}{teal}\Footer{A1}\pdfbookmark[1]{附录1 指标、口径与来源}{appendix1}'+'\n'
    tex+=box(15,28,180,'附录 1｜指标、口径与来源',20,27,'ink',True)
    tex+=box(15,43,180,'2026 报告年度为 2025 年 7 月 1 日至 2026 年 6 月 30 日；2022—2025 年按同样的跨年窗口阅读。累计规模是期末基础，活跃规模覆盖整个报告年度。',10.3,17)
    tex+=box(15,66,180,'1  人数衡量什么',12,18,'teal',True)
    defs=[
      ('累计规模','平台已有账号基础，包含当期没有公开活动的账号。不是职业开发者人口，也不代表其中每个人都参与 AI 研发。'),
      ('活跃开发者','报告期内出现在公开活动记录中的账号，活动包括收藏项目、复制仓库、提交修改或讨论等；不能与“代码贡献者”直接互换。'),
      ('同比与净增','净增 = 本期活跃 − 上期活跃；同比增速 = 净增 ÷ 上期活跃。它们不直接测量首次参与、人才迁移或同一批人的留存。'),
      ('地理分布','地区值包含按可识别所在地进行的估计，故原始读数可能有小数；表示平台可观察的地域参与，不表示国籍、职业或雇主归属。')
    ]
    for y,(t,p) in zip([79,100,124,145],defs):tex+=box(15,y,29,t,10.2,16,'teal',True)+box(46,y,149,p,10,16)
    tex+=box(15,170,180,'2  三套覆盖分别阅读',12,18,'teal',True)
    coverage=[
      '国家地图、前 20、全球与中国三条趋势及省级图：采用 OpenShare 的 GOSD 年度 GitHub 数据；南方六国细分与之同源。',
      '五域：欧洲、美国、中国、印度、南方六国采用报告编制组的独立综合序列，不是全球完整分区。五域与单国平台表的覆盖不同，不混排、不相加。',
      '中国跨平台：GitHub 250.48 万，加 Gitee、AtomGit 等国内平台经问卷及平台数据去重补充约 120 万，合计约 370 万。该补充已确认；不回填历史、不分摊到省，也不再次叠加到五域。'
    ]
    for y,p in zip([183,202,226],coverage):tex+=box(15,y,180,p,9.7,15.4)
    tex+=box(15,252,180,'来源：OpenDigger / OpenShare、报告编制组。公开数据读取于 2026-11-09；其元数据更新时间为 2026-10-08。地图几何沿用 2026 版，台湾、香港、澳门纳入中国。',8.7,13,'muted')
    tex+=r'\Box{15}{272}{180}{\sffamily\fontsize{8.4}{11}\selectfont\href{https://open-share.com/insight/open-world/gosd}{OpenShare GOSD 入口}\quad\href{https://selfoss.open-digger.cn/openshare/overview_half_year/meta.json}{统计期元数据}\quad\href{https://selfoss.open-digger.cn/openshare/overview_half_year/developers.json}{全球及国家数据}\quad\href{https://selfoss.open-digger.cn/openshare/overview_half_year/CN/developers.json}{中国省级数据}}'+'\n'
    tex+=r'\end{canvas}'+'\n'
    # Appendix 1 continued: sufficient numeric evidence to recreate scenarios.
    tex+=r'\begin{canvas}\Header{附录 1 · 历史与情景}{teal}\Footer{A2}\pdfbookmark[2]{历史序列、情景测算与评审记录}{appendix2}'+'\n'
    tex+=box(15,28,180,'历史序列与 2030 条件情景',20,27,'ink',True)
    tex+=box(15,44,180,'南方六国指巴西、印度尼西亚、越南、菲律宾、埃及、南非，不代表全球南方整体；印度单列。上方五域综合数不等同于六国 GitHub 细分之和。',9.9,16)
    tex+=box(15,65,180,'3  历史读数｜2022—2026 报告年度',11.8,17,'teal',True)
    tab=r'\sffamily\fontsize{9.3}{14}\selectfont\renewcommand{\arraystretch}{1.12}\setlength{\tabcolsep}{5.1pt}\begin{tabularx}{180mm}{@{}Xrrrrr@{}}\toprule 对象／单位 & 2022 & 2023 & 2024 & 2025 & 2026\\\midrule'+'\n'
    for k,c in GROUPS:tab+=esc(NAMES.get(k,k))+'／万&'+'&'.join(f'{v:,.2f}' for v in SC[k]['history'])+r'\\'+'\n'
    for k,t in [('total','全球累计／亿'),('active','全球活跃／万'),('china','中国 GitHub／万')]:tab+=t+'&'+'&'.join(f'{v:,.2f}' for v in GS[k]['history'])+r'\\'+'\n'
    tab+=r'\bottomrule\end{tabularx}';tex+=rf'\Box{{15}}{{77}}{{180}}{{{tab}}}'+'\n'
    tex+=box(15,135,180,'4  2030 情景读数｜不是确定结果或置信区间',11.8,17,'teal',True)
    tab=r'\sffamily\fontsize{9.3}{14}\selectfont\renewcommand{\arraystretch}{1.12}\setlength{\tabcolsep}{7pt}\begin{tabularx}{180mm}{@{}Xrrr@{}}\toprule 对象／单位 & 历史年均增速 & 2030 放缓 & 2030 延续\\\midrule'+'\n'
    for k,c in GROUPS:
        s=SC[k];tab+=esc(NAMES.get(k,k))+f'／万&{s["annual_growth"]*100:.2f}\\%&{s["slowing"][-1]:,.2f}&{s["continued"][-1]:,.2f}'+r'\\'+'\n'
    for k,t in [('total','全球累计／亿'),('active','全球活跃／万'),('china','中国 GitHub／万')]:
        s=GS[k];tab+=t+f'&{s["annual_growth"]*100:.2f}\\%&{s["slowing"][-1]:,.2f}&{s["continued"][-1]:,.2f}'+r'\\'+'\n'
    tab+=r'\bottomrule\end{tabularx}';tex+=rf'\Box{{15}}{{147}}{{180}}{{{tab}}}'+'\n'
    tex+=box(15,205,180,'以 2026 年为起点，历史年均增速 g =（2026 人数 ÷ 2022 人数）的四次方根 − 1。延续情景每年按 g 增长；放缓情景在第 h 年采用 g × 0.8 的 h 次方，逐年复利计算。测算使用未舍入值。',9.6,15.1)
    tex+=box(15,228,180,'0.8 是预设的敏感性参数，未拟合概率，也未单独估计 AI 或政策的因果效应。每年补入新观测后重算；发布后 6—12 个月优先跟踪贡献采纳、持续参与和维护职责。',9.6,15.1)
    tex+=box(15,251,180,'评审记录｜v0.3，2026-11-09：三页正文全部改为 A4 竖版；恢复中国五域 454.534 万，纳入已确认的跨平台约 370 万；补齐三条趋势、南方六国和中国增量分析。',8.5,12.4,'muted')
    tex+=box(15,268,180,'待核查：五域欧洲成员清单及历史覆盖执行记录；地图出版规范。待评审：竖版图文密度与情景假设。上述事项不改变本轮已确认的中国补充数。',8.3,12,'muted')
    tex+=r'\end{canvas}\end{document}'
    (R/'report.tex').write_text(tex)
