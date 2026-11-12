"""Reader-facing appendix text, refined from the v0.1 review manuscript.

The existing source register, metric parameters and acknowledgement provenance
remain in data/. Reader-facing prose contains no detached reference markers.
"""
import json

INDICATORS = [
 ('活跃开发者规模','有可见活动的账号数量，按统一规则去重。'),
 ('人才聚集密度','一定地域内的人才集中程度，须说明比较基数。'),
 ('新晋开发者增速','首次参与指定协作范围的人数及其变化。'),
 ('全球开源协作占比','跨国协作关系在全部可识别关系中的比例。'),
 ('学术机构贡献占比','高校与科研机构相关贡献在样本中的比例。'),
 ('有效活跃仓库规模','达到活跃条件的仓库数量，区分复制仓库与镜像。'),
 ('代码协作贡献度','依据项目内协作关系衡量贡献，采用 OpenRank 指标。'),
 ('高质量 PR 合入量','符合明确质量条件、并被项目接受的变更请求数量。'),
 ('开源模型发布量','发布的模型数量，分别说明仓库、版本和开放条件。'),
 ('模型供给方多样性','模型发布者的类型、地域及各自所占份额。'),
 ('开源数据集发布量','发布的数据集数量，同时说明许可和重复处理规则。'),
 ('数据供给方多样性','数据发布者的类型、地域及份额分布。'),
 ('代码仓库影响力','仓库在跨项目协作网络中的影响，采用全域 OpenRank。'),
 ('高影响力区域数量','达到指定影响水平的国家、地区或城市数量。'),
 ('高影响力组织数量','达到指定影响水平的企业、基金会等组织数量。'),
 ('高影响力项目数量','达到指定影响水平的项目数量，多个仓库按项目归并。'),
 ('高影响力人才数量','在明确观察范围内，达到指定影响水平的人才数量。'),
 ('模型采用度','以下载等信号观察获取和使用情况。'),
 ('模型社区热度','以点赞、讨论等记录观察社区关注。'),
 ('模型生态衍生力','以模型来源关系及 ModelRank 观察后续再创造。'),
 ('数据集采用度','以下载等信号观察数据的获取和使用情况。'),
 ('数据社区热度','以讨论和互动观察社区关注。'),
 ('数据生态复用率','有明确再次使用记录的数据占比，说明统计范围。'),
 ('基金会托管比例','由基金会正式托管的项目占比。'),
 ('治理主体均衡度','不同参与者在角色、决策与协作中的分布。'),
 ('合规许可覆盖率','按明确规则核验许可及适用条件后的覆盖比例。'),
 ('数字公共品共建度','共同维护、参与使用及服务公共需求的程度。'),
 ('高开放度许可占比','符合指定开放条件的许可占比，按资源版本判断。'),
 ('AI 资产透明度','模型权重、代码、数据说明与评估材料的公开程度。'),
]

def populate(g):
    title,para,heading,table,note,img,page=g.title,g.para,g.heading,g.table,g.note,g.img,g.page
    s=title('附录｜指标体系与数据来源','读懂全书的观察对象、指标与比较方法')
    s+=para('本附录帮助读者理解：报告观察了谁，数字说明什么，以及哪些结果可以比较。开源发展目标（OSDGs）明确发展方向，开源发展指标（OSDI）提供观察线索，共同服务于参与、供给、复用、治理与公共价值的研究。')
    s+=heading('1　理论基础与标准参照')
    s+=para('报告参照《信息技术 开源治理》系列团体标准，并结合 OpenDigger 的开放指标，分别观察社区治理、项目发展和开发者贡献。')
    s+=table(['标准编号','名称','在本报告中的作用'],[
        ['T/CESA 1270.3—2023','第 3 部分：社区治理框架','理解社区协作与治理'],
        ['T/CESA 1270.4—2023','第 4 部分：项目评估模型','参照项目评估的维度与方法'],
        ['T/CESA 1270.5—2023','第 5 部分：开源贡献者评估模型','参照开发者贡献的评价方法']],[45,64,None],10,16)
    s+=heading('2　五类核心协作行为')
    s+=para('议题（Issue）用于提出问题和开展讨论；变更请求（PR）用于提交修改方案，供项目评审和接受。')+img('five-actions')
    s+=table(['缩写','协作行为','通俗解释'],[
        ['OI','创建议题','提出问题、需求或讨论主题。'],
        ['ID','参与讨论','围绕议题或变更请求发表评论。'],
        ['OPR','发起变更请求','提交修改方案，一次请求可包含多次代码提交。'],
        ['PRR','提出评审评论','对修改方案的具体内容给出评审意见。'],
        ['MPR','变更请求合入','修改方案被项目接受，纳入项目内容。']],[16,46,None],10.2,16.3)
    s+=note('图附-1、表附-1　五类核心协作行为。依据 OpenDigger 指标说明整理；行为记录反映协作过程，不能单独证明质量或工作量。')
    page('附录｜概念与行为',s,10.8,18.2)

    s=title('3　参与规模、贡献量与活跃度','人数、次数与协作强度，回答不同问题')
    s+=para('活跃账号、协作参与者和已被接受的修改方案作者，覆盖范围有所不同。阅读人数时，先看纳入了哪些行为；比较不同地区或年份时，再确认统计规则是否一致。')
    s+=img('participant-sets')+note('图附-2　同一平台、对象与时间内的参与范围示意。不同平台的账号，须确认身份后才能合并为同一人。')
    s+=heading('四类基础指标')
    s+=table(['指标','主要回答','读数要点'],[
        ['活跃开发者／参与者','有多少账号参与？','同一账号只计一次，全年人数不能由每月人数直接相加。'],
        ['活跃仓库／项目','有多少资源单元持续活动？','仓库是资源存放与协作单元，一个项目可能包含多个仓库。'],
        ['贡献量','发生了多少次协作行为？','按明确的行为类型计数，分别理解讨论、评审和合入。'],
        ['Activity 活跃度','可见协作有多活跃？','综合不同协作行为计算分值，区别于人数和行为次数。']],[39,53,None],10.3,17)
    s+=heading('如何理解 Activity')
    s+=para('Activity 综合前述五类协作行为，体现账号与仓库的协作强度。不同类型的行为采用不同权重，并压缩单一账号大量重复行为的数值影响，再汇总为仓库的活跃度。')
    s+=para('因此，两个项目即使行为总数相近，也可能得到不同的活跃度。它有助于观察协作节奏，但仍需结合评审、维护和实际使用来理解项目的发展。')
    s+=r'\vspace{6pt}\Shaded{\textbf{阅读要点：}人数看参与基础，次数看行为规模，活跃度看综合强度。三者互为补充，不直接等同于代码质量、投入工时或公共收益。}'
    s+=note('依据 OpenDigger 数据使用说明与 Activity 指标文档整理。')
    page('附录｜基础指标',s,11,18.6)

    s=title('4　OpenRank：贡献度与影响力','既看项目内部协作，也看跨项目连接')
    s+=para('OpenRank 依据协作关系衡量贡献和影响。社区 OpenRank 观察开发者在一个项目中的相对贡献；全域 OpenRank 观察开发者、仓库或项目在更大协作网络中的位置，并考虑历史积累。')
    s+=img('openrank-matrix')+note('图附-3　两种观察范围。依据 OpenDigger 的社区与全域 OpenRank 文档整理，图中网络为示意。')
    s+=heading('不同对象，需要不同的归属规则')
    s+=table(['观察对象','主要看什么','合计时注意'],[
        ['开发者／群体','参与规模、协作行为、贡献与影响','区分个人与群体，避免重复计算。'],
        ['仓库／项目','供给、参与者与项目影响','多个仓库属于同一项目时，按名录归并。'],
        ['企业／基金会','关联项目、开发者与生态影响','员工贡献与关联项目影响分别理解。'],
        ['国家／地区','人才分布、资源与贡献份额','区分人员所在地、组织总部和项目归属。'],
        ['技术／模型生态','技术类别、模型供给与复用关系','代码与模型采用不同网络指标。']],[33,68,None],9.7,15.2)
    s+=r'\vspace{5pt}\Shaded{\textbf{阅读要点：}网络影响不等于技术性能或经济价值。“平均贡献”须以同一时期、同一样本的贡献总量除以人数，不能代替每个人的实际贡献。}'
    page('附录｜网络评价',s,10.8,18.2)

    s=title('5　候选指标目录','四个目标、十个方向、29 项候选指标')
    s+=para('目录承接第一章的发展框架，说明希望观察的问题。部分指标仍需完善数据与方法，以下名称不表示已经对所有样本完成测量或资格认定。')
    s+=heading('X1　人才规模与多样性　｜　参与从何而来')
    s+=table(['候选指标','读法与要点'],INDICATORS[:5],[54,None],11,19)
    s+=heading('X2　技术产出与开放供给　｜　形成哪些资源')
    s+=table(['候选指标','读法与要点'],INDICATORS[5:12],[54,None],11,19)
    s+=r'\vspace{9pt}\Shaded{\textbf{共同要求：}每项指标都应说明观察对象、单位、统计时期和来源。比较比例时须明确分母；“高质量”等判断须先给出清楚的条件。}'
    s+=note('表附-2（上）　人才与资源供给指标。候选指标用于明确观察方向，具体测量范围以正文图表为准。')
    page('附录｜指标目录',s,10.8,18.2)

    s=title('候选指标目录（续）','连接与治理，让开放成果形成长期价值')
    s+=heading('X3　全球连接与网络效应　｜　资源如何连接与复用')
    s+=table(['候选指标','读法与要点'],INDICATORS[12:23],[54,None],10.5,17)
    s+=heading('X4　开源善治与公共价值　｜　开放如何长期持续')
    s+=table(['候选指标','读法与要点'],INDICATORS[23:],[54,None],10.5,17)
    s+=note('表附-2（下）　连接、治理与公共价值指标。下载不等于实际部署，公开材料不等于已经独立验证；公共价值还需结合成本、本地适用性、维护和使用结果判断。')
    page('附录｜指标目录',s,10.8,18.2)

    s=title('6　数据来源、统计周期与归属','看清时间、对象和范围，才能正确比较')
    s+=img('time-windows')+note('图附-4　报告的时间安排。主统计期为 2025 年 7 月 1 日至 2026 年 6 月 30 日；历史材料与期后观察分别标明。')
    s+=heading('数据从哪里来')
    s+=table(['来源','主要内容','如何理解'],[
        ['OpenDigger','开源协作事件、指标与标签','以 GitHub 为主要观察平台，各指标覆盖范围分别说明。'],
        ['OpenShare','榜单、指标应用与生态观察','部分底层数据来自 OpenDigger，不重复算作独立证据。'],
        ['Gitee、AtomGit 等','中国平台记录与专项材料','按实际取得的材料补充观察。'],
        ['Hugging Face','模型、数据集、下载与开放材料','记录采集日期，区分资源可见、开放条件与实际使用。'],
        ['项目与机构公开材料','归属、治理、许可与维护信息','支持具体案例，按材料日期理解其适用范围。']],[33,62,None],10,16.5)
    s+=heading('合计之前，区分三类归属')
    s+=para(r'\textbf{账号与身份。}跨平台合计需确认身份；机器人和未知身份分别处理。不同图表按各自来源说明清理范围。')
    s+=para(r'\textbf{地域与总部。}开发者所在地、组织总部与项目归属是不同视角。中国地域统计包含台湾地区；无法识别的地域保留为未知。')
    s+=para(r'\textbf{项目与组织。}一个项目可能有多个仓库，组织之间也可能存在包含或交叉关系，合计前应避免重复。')
    s+=r'\Shaded{\textbf{比较要点：}先确认对象、时期、统计规则和分母一致；未覆盖、归属未知与真实为零，分别呈现。}'
    page('附录｜数据来源',s,10.8,18.2)

    s=title('7　模型、行业与趋势的读法','扩展观察视野，同时说明数字能解释什么')
    s+=heading('模型与数据：数量、复用和实际应用分开理解')+img('model-units')
    s+=para('模型仓库是发布载体，模型版本是具体成果，模型家族包含相关版本。派生关系表示在已有模型上继续改进；缺少来源标注，并不能证明没有使用他人成果。')
    s+=para('下载反映获取活动，点赞反映关注，派生关系与 ModelRank 反映再创造及其网络位置。开放条件则要结合许可、代码、数据说明等材料判断。')
    s+=note('图附-5　模型资产的观察层次。依据 Hugging Face 公开说明与报告模型样本整理。')
    s+=heading('行业地图：从仓库内容识别行业线索')
    s+=table(['环节','本报告的处理与读法'],[
        ['选取样本','按 2021—2025 年创建的仓库分别抽样，经文本筛选保留 18,086 个。'],
        ['识别行业','根据仓库描述等文本推断 19 个行业门类，分类存在误差。'],
        ['观察 AI 关联','统计描述中是否提及 AI 或机器学习，反映文本关联程度。']],[32,None],10.2,17)
    s+=note('表附-3　行业样本方法摘要。依据团队行业数据报告整理。年份指仓库创建年份；文本提及不等于实际采用率，样本不能代表全部平台或行业产值。')
    s+=heading('趋势与 2030 展望：把事实与假设区分开')
    s+=para('历史数据说明已经观测到的变化；预测线说明在给定假设下可能出现的路径。报告用不同线型、时期和情景区分二者，不把历史增长率直接视为未来必然结果。')
    s+=para('低、中、高情景用于比较不同条件下的可能结果，并非发生概率。技术与环境变化后，判断也需要更新；面向 2030 的讨论主要用于辨认长期方向与实现条件。')
    page('附录｜专项读法',s,11,18.8)

    s=title('8　常用术语速查','用简明解释连接全书的关键概念')
    s+=para('同一词语可能有不同统计含义。下表给出本报告的常用读法，具体对象和时间以正文图表说明为准。')
    s+=table(['术语','通俗读法'],[
        ['活跃开发者','在指定平台和时期内有可见活动的账号，纳入哪些行为由来源说明。'],
        ['协作参与者','参与议题或变更请求讨论、评审等协作的账号。'],
        ['贡献者','一般指参与贡献的人；采用特定数据字段时，可能仅指已合入变更请求的作者。'],
        ['贡献量／活跃度','贡献量统计行为次数；活跃度综合不同协作行为形成强度分值。'],
        ['贡献度／影响力','分别观察项目内部的相对贡献，以及跨项目协作网络中的位置。'],
        ['ModelRank','依据模型之间的来源和派生关系，观察模型在再创造网络中的影响。'],
        ['快照／创建年份分组','快照记录某一采集时点的状态；按创建年份分组，用于比较不同年份形成的对象。'],
        ['模型家族／派生关系','家族是一组相关模型版本；派生关系说明新版本与已有模型之间的联系。'],
        ['情景推演','在明确假设下讨论未来可能路径，不代表已经发生或必然实现。'],
        ['数字公共品','服务公共需求的开放数字资源，须符合相应标准；认可状态另行说明。']],[43,None],11,19.5)
    page('附录｜术语速查',s,11,18.8)

    cn=[
        '《2026 全球开源发展报告》由中国科学技术协会指导，依托其联合国经济及社会理事会（ECOSOC）咨商地位，由中国科协联合国咨商开源创新专委会提供政策框架支持并牵头编写。中国通信学会作为专委会秘书处承担单位，负责组织协调与实施保障；奇点智能研究院担任出品方。',
        '联合国教科文组织（UNESCO）、国际电信联盟（ITU）、联合国国际电子计算中心（UNICC）以及联合国数字和新兴技术办公室（ODET）的专家，围绕核心议题、分析框架及全球发展倡议提出建议，支持研究与《2030 年可持续发展议程》相衔接。',
        '清华大学、北京大学、上海交通大学、复旦大学、华东师范大学、中国科学院大学、南京大学、北京航空航天大学、北京邮电大学、国防科技大学、香港大学、对外经济贸易大学、北京理工大学、东北大学，以及中国科学院科技战略咨询研究院、中国科学院文献情报中心、上海人工智能实验室、阿里研究院等高校与科研机构的专家学者，参与了理论构建、数据分析和章节撰写。',
        '新加坡国立大学、牛津大学、加州大学伯克利分校、凯斯西储大学、爱尔兰软件研究中心等国际高校与研究机构的学者，为开源治理、创新生态和技术社会影响研究提供了跨国比较视角。',
        '中国电子技术标准化研究院和中国信息通信研究院，在标准引用、开源评估、政策合规与数据方法方面提供了专业支持。',
        '华为、阿里巴巴、蚂蚁集团、字节跳动、百度等企业开源办公室（OSPO）的工程师与治理专家，分享了技术实践与生态建设经验。LF AI & Data、OpenInfra Foundation、PyTorch Foundation 等国际开源基金会代表，协助完善了开放治理的国际比较分析。',
        '中国开源软件推进联盟（COPU）、开源社、X-lab 开放实验室、ALC-Beijing，以及 GitHub、Gitee、GitCode、Hugging Face、魔搭等社区成员，以志愿协作方式参与研讨和案例收集。CSDN 支持了技术趋势调研与理念传播。',
        '国际基准测试委员会（Benchmark Council）为技术评估体系提供了方法与数据标准支持。',
        '谨向所有参与研究、编写、评审与内容贡献的机构和个人致以诚挚谢意。我们期待继续汇聚各方力量，以开放协作促进 AI 普惠与可持续发展。'
    ]
    s=title('致谢','共同研究、开放协作与持续贡献')
    s+='\n\n'.join(g.esc(p) for p in cn)
    s+=r'\par\vspace{10pt}{\raggedleft\sffamily\color{teal}《2026 全球开源发展报告》编制组\par}'
    page('致谢',s,11,19.2)

    en=[
        'The 2026 Global Open Source Development Report was guided by the China Association for Science and Technology (CAST), drawing on its consultative status with the United Nations Economic and Social Council (ECOSOC). The CAST Advisory Committee on Open Source Innovation (CCOSI) provided policy support and led the compilation. The Chinese Institute of Communications (CIC), as the committee’s secretariat, coordinated the work. The Singularity Intelligence Research Institute served as the publishing entity.',
        'Experts from UNESCO, the International Telecommunication Union (ITU), the United Nations International Computing Centre (UNICC), and the United Nations Office for Digital and Emerging Technologies (ODET) advised on the report’s core themes, analytical framework and links to global development initiatives, supporting its alignment with the 2030 Agenda for Sustainable Development.',
        'Scholars from Tsinghua University, Peking University, Shanghai Jiao Tong University, Fudan University, East China Normal University, University of Chinese Academy of Sciences, Nanjing University, Beihang University, Beijing University of Posts and Telecommunications, National University of Defense Technology, The University of Hong Kong, University of International Business and Economics, Beijing Institute of Technology, and Northeastern University contributed to the framework, data analysis and chapters. They were joined by researchers from the Institutes of Science and Development and the National Science Library of the Chinese Academy of Sciences, Shanghai Artificial Intelligence Laboratory, and Alibaba Research.',
        'Scholars from the National University of Singapore, the University of Oxford, the University of California, Berkeley, Case Western Reserve University, and the Irish Software Research Centre contributed comparative perspectives on open source governance, innovation ecosystems and the social impact of technology.',
        'The China Electronics Standardization Institute (CESI) and the China Academy of Information and Communications Technology (CAICT) provided expertise in standards, open source assessment, policy compliance and data methods.',
        'Engineers and governance experts from the open source program offices (OSPOs) of Huawei, Alibaba, Ant Group, ByteDance, Baidu and other enterprises shared technical and ecosystem experience. Representatives of LF AI & Data, OpenInfra Foundation and PyTorch Foundation supported the international comparison of open governance.',
        'Members of the China Open Source Promotion Union (COPU), KAIYUAN.SHE, X-lab Open Laboratory, ALC-Beijing, and the GitHub, Gitee, GitCode, Hugging Face and ModelScope communities volunteered in discussions and case collection. CSDN supported technology trend research and outreach.',
        'The Benchmark Council provided guidance on methods and data standards for the report’s technical assessment framework.',
        'We sincerely thank every institution and individual who contributed to the research, writing, review and supporting materials. We look forward to continued collaboration to advance AI for All and sustainable development.'
    ]
    s=title('Acknowledgements','Shared research, open collaboration and lasting contributions')
    s+=r'{\latin\fontsize{10.7}{15.6}\selectfont\raggedright\setlength{\columnsep}{7mm}\setlength{\multicolsep}{0pt}\begin{multicols}{2}\setlength{\parskip}{6pt}'
    s+='\n\n'.join(g.esc(p) for p in en)
    s+=r'\par\vspace{8pt}{\raggedleft\color{teal}The 2026 GOSD Report Team\par}\end{multicols}}'
    page('Acknowledgements',s,10.7,15.6)
    (g.R/'data/acknowledgements-2026.json').write_text(json.dumps({'cn':cn,'en':en},ensure_ascii=False,indent=2))
    (g.R/'data/indicators.json').write_text(json.dumps([{'name':name,'explanation':body} for name,body in INDICATORS],ensure_ascii=False,indent=2))
