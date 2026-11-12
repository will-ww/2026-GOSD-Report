"""Chinese XeLaTeX publication layout; 10 figure pages plus framing and compact Appendix A."""
from common import *
import re
TITLE='第五章　全球开源大模型发展洞察'
VER='v0.2'
def b(x,y,w,t,fs=10,lead=15,c='ink',bold=False,sans=False):
 q=box(x,y,w,t,fs,lead,c,bold,sans)
 return re.sub(r'［(\d+)］',lambda m:r'\hyperlink{src'+m[1]+'}{'+m[0]+'}',q)
def raw(x,y,w,t):return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{{t}}}'+'\n'
def rect(x,y,w,h,c):return rf'\Rect{{{x}}}{{{y}}}{{{w}}}{{{h}}}{{{c}}}'+'\n'
def rule(y):return rf'\Rule{{15}}{{{y}}}{{195}}{{line}}'+'\n'
def begin(n,title,append=False):
 label='附录 A · 第五章方法与证据' if append else '第五章 · 全球开源大模型发展洞察'
 return rf'\begin{{canvas}}\Header{{{label}}}{{teal}}\Footer{{{n}}}\pdfbookmark[1]{{{esc(title)}}}{{page{n}}}'+'\n'
def end():return r'\end{canvas}'+'\n'
def head(title,subtitle=None):return b(15,27,180,title,20,27,'ink',True)+(b(15,40,180,subtitle,11,16,'teal',True) if subtitle else '')
def opening():
 q=begin('01',TITLE)+head(TITLE,'从开放供给，走向全球接续与公共能力')
 q+=b(15,54,180,'模型生态的价值，既来自新的资源，也来自围绕资源持续展开的适配、再创造与维护。第四章呈现运行模型的技术生态，本章进一步观察模型与数据由谁供给、怎样进入全球接续，以及何种开放条件能够支撑持续使用和独立创新。',10.7,17)
 q+=b(15,88,180,'地图定位发布者，派生网络连接上下游，开放评价检查材料与权利。三组证据互相补充，分别揭示资源位置、协作角色和再创造条件；它们共同帮助判断公共投入应支持哪些环节。',10.7,17)
 units=[('5.1','供给与贡献','从世界地图到中国资源分工','全球地图、发布者与增长、中国区域结构','02—04'),('5.2','网络与影响力','从基座供给到跨国再创造','派生全景、跨国关系、影响位置与时序','05—07'),('5.3','开源开放与分级体系','从使用权限到完整交付','评价体系、地域主体、全球开放、中国画像','08—11')]
 for i,(n,t,sub,desc,pp) in enumerate(units):
  y=121+i*33;q+=rect(15,y,180,29,'paper');q+=b(19,y+4,15,n,15,18,'teal',True)+b(40,y+4,130,t,12,16,'ink',True)+b(173,y+5,20,pp,9,12,'muted',sans=True)
  q+=b(40,y+13,145,sub,10.4,15,'teal',True)+b(40,y+20,145,desc,9.4,14,'muted',sans=True)
 q+=b(15,228,180,'中国贡献放在全球再创造中理解：既观察模型和数据供给，也观察跨境复用、地区分工与材料交付。全球南方可以从语言适配、数据共建、评测与新基座供给等不同环节进入，合作路径应由当地需求与能力条件决定。',10.3,16)
 q+=b(15,260,180,'主统计期：2025.07.01—2026.06.30。历史、期后快照和回溯数据分别标注；开放评价统一采用本次读取的 889 条记录。方法与来源集中于附录 A1—A2。',8.7,12.5,'muted',sans=True)
 return q+end()
def content_page(p):
 q=begin(f'{p["page"]:02}',p['title'])+head(p['title'])
 q+=b(15,40,180,p['intro'],9.7,13.5,'muted',sans=True)
 q+=raw(15,53,180,rf'\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}')
 q+=b(15,199,180,p['caption'],7.6,10.7,'muted',sans=True)
 for i,(h,t) in enumerate(p['analyses']):
  x=15 if i%2==0 else 108;y=214 if i<2 else 247
  q+=b(x,y,87,h,10.1,14.3,'teal',True)+b(x,y+6.2,87,t,9.65,14.6)
 return q+end()
def conclusion():
 q=begin('12','本章综合：将开放资源转为公共能力')+head('本章综合｜将开放资源转为公共能力','支持资源分工，连接全球接续，补齐可持续使用的条件')
 findings=[('供给需要按资源与主体理解','模型与数据的主要供给者并不相同，中国省级样本也呈现资源互补。支持对象应同时覆盖模型、数据、文档与维护，让公开资源能够通过具体接口和共同任务连接起来。见图 5-1—5-3。'),('中国贡献应置于全球再创造中观察','跨国样本中，中国基座至美国派生发布者有 4,639 对关系；另一局部网络中，552 个版本同时连接上下游。这些证据分别揭示跨境方向与接续角色，为联合适配和维护提供入口。见图 5-4—5-6。'),('开放权限还需要完整交付与独立验证','同一组 889 条记录中，高开放 617 条、高完整 175 条，两项重合 117 条。材料与权利的差异指向具体建设任务：训练配方、数据说明、验证环境与维护责任。见图 5-7—5-10。')]
 for i,(h,t) in enumerate(findings):
  y=56+i*30;q+=b(15,y,180,h,11.3,16,'teal',True)+b(15,y+7,180,t,10,15)
 q+=rule(149)+b(15,156,180,'面向行动：明确主体、交付与可观测结果',12,17,'teal',True)
 actions=[('公共资源支持','政府、基金会与资助机构','将数据整理、文档和复现环境列入支持任务；验收材料版本、独立复现结果与维护响应。'),('跨境协作计划','模型发布者与接续社区','沿真实版本关系组织联合评测与适配；观察共同维护、兼容性修复及问题反馈闭环。'),('开放评价治理','标准、评测与研究机构','固定规则、版本和证据，公开改判记录；以材料完整度、验证通过与响应时效持续复核。'),('普惠能力试点','当地伙伴、高校与产业团队','围绕本地语言与场景实施；记录成本、本地化、维护责任和使用结果，再判断是否扩大。')]
 for i,(h,who,t) in enumerate(actions):
  x=15 if i%2==0 else 108;y=167 if i<2 else 216;q+=rect(x,y,87,43,'paper')+b(x+3,y+3,81,h,10.7,14.6,'ink',True)+b(x+3,y+11,81,who,8.8,12,'teal',sans=True)+b(x+3,y+18,81,t,9.4,14)
 q+=b(15,268,180,'这些行动方向由本章证据支持，实施效果仍需验证；第六章进一步明确优先次序、承担主体与后续监测信号。',8.8,12.5,'muted',sans=True)
 return q+end()
def appendix_method():
 q=begin('A1','第五章：数据与阅读口径',True)+head('附录 A｜数据与阅读口径')
 q+=b(15,43,180,'全章区分资源数量、获取活动、声明关系、网络位置与开放条件。图中数字只在标明的对象、样本与时间范围内解释，不合成为一个国家或模型总分。',10,15,'muted')
 rows=[('图 5-1—5-3｜供给与地域','平台总览于北京时间 2026.11.11 读取。地域沿用 2026.10.17 冻结的 826 个组织账号、73,088 个模型与 12,502 个数据集；此次实时地域接口超时，不据平台总量更新地域比例。国家按组织归属，省级归属待补仍留在全国分母。'),('图 5-2｜两类时间序列','年度为 2026.09.13 仍可见仓库按创建日期回看各年同日，非逐年独立快照。月度记录图示 2024.07—2026.06，主期合计与此前 12 个月比较；两套来源不拼接，月度留存与下架规则尚待补充。'),('图 5-4—5-6｜接续与影响','网络来自 2026.10.16 非随机前 12,000 个输入中的双端可见声明关系；网络位置无能力含义。跨国表为 2026.09.13 的 10,943 对关系，与网络样本不同。来源称国家识别覆盖约 2.59%（含境内），完整分母尚未独立重建。'),('图 5-7—5-10｜统一开放评价样本','采用 2026.11.11 读取的 889 个完整模型 ID，与逐项证据逐条对应，保留严格模式等级。以 country 字段重算国别，未知 64 条保留；未使用容易混淆的地区比较标签。旧 870、884 样本留作归档，不将差值视为增长。'),('分级与案例｜规则和证据的边界','L1—L5 为累进完整性，O1—O4 为许可条件；高完整 L3—L5，高开放 O2—O4。材料状态与许可资格字段的语义不同，不能把 missing 直接当成文件不存在。三案例取相同模型 ID；本报告未独立重跑训练或授予等级。'),('待核事项｜后续证据建设','补齐平台样本筛选年度、统一统计截止日与历史留存规则；复核正式标准全文及逐版本许可适用；完善跨国关系地理覆盖和派生类型。面向普惠实施，继续取得成本、本地化、维护与结果证据。')]
 for i,(h,t) in enumerate(rows):
  y=65+i*34;q+=b(15,y,180,h,10.7,15,'teal',True)+b(15,y+7.5,180,t,9.5,14)
 return q+end()
BASE='https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/c51e3441361407b68f10b339d97eff288319b503/'
REFS=[('1','OpenGauge 平台总览','2026.11.11 读取；公开模型与数据集仓库总量。','http://47.100.76.186:9529/overview'),('2','OpenGauge 供给观测归档','826 个组织账号的地域、主体、资产与月度序列；2026.10.17 冻结。',BASE+'preview/content/gosm/supply-observation.json'),('3','HF 模型与发布账号年度回溯','2022—2026 各年 9 月 13 日；终点可见仓库回溯。',BASE+'data/processed/chapter5/fig-5-1-1_hf_cumulative_models_publishers.csv'),('4','模型基座与派生网络来源记录','2026.10.16 非随机样本；5,777 个节点与 5,111 条声明边。',BASE+'preview/content/gosm/lineage-live-provenance.json'),('5','HF 派生模型年度回溯','有基座声明的仓库；与年度总模型使用同一回溯口径。',BASE+'data/processed/chapter5/fig-5-2-1_hf_cumulative_derivation.csv'),('6','跨国模型派生关系表','2026.09.13；186 个有向国家组合、10,943 对关系。',BASE+'data/processed/chapter5/fig-5-2-2_cross_country_derivation_flows.csv'),('7','ModelRank 国家头部席位月表','2024.07—2026.08；主期末 2026.06，未知归属保留分母。',BASE+'data/processed/chapter5/fig-5-2-3_modelrank_country_head_trend.csv'),('8','模型开放分级规范：项目保留文本与要求表','用于双轴释义；正式标准全文适用仍待逐条核对。',BASE+'preview/content/gosm/openness53-methods.md'),('9','OpenGauge 开放评价模型明细','889 个模型 ID；2026.11.11 读取，保留来源严格模式等级。','http://47.100.76.186:9529/api/openness/quadrant/'),('10','OpenGauge 逐模型材料与许可证据','九页、每页最多 100 条，共 889 条；按模型 ID 关联。','http://47.100.76.186:9529/openness')]
def appendix_sources():
 q=begin('A2','第五章：资料来源与复核入口',True)+head('附录 A｜资料来源与复核入口')
 q+=b(15,42,180,'标题链接通向原始来源。图表以归档数据与本次公开读取结果重绘，正文仅保留必要的来源编号；结构化源稿保留完整数据、口径、计算与版本记录。',9.8,14.5,'muted')
 for i,(n,t,desc,url) in enumerate(REFS):
  y=63+i*17.6;u=url.replace('&',r'\&').replace('%',r'\%').replace('#',r'\#')
  q+=raw(15,y,180,rf'\hypertarget{{src{n}}}{{}}\sffamily\bfseries\fontsize{{10.2}}{{14}}\selectfont\href{{{u}}}{{［{n}］{esc(t)}}}')+b(24,y+6.2,171,desc,9,13,'muted',sans=True)
 q+=rule(244)+b(15,251,180,'地图与名词',10.3,14,'teal',True)
 q+=b(15,259,180,'地图沿用本报告已使用的世界与中国几何，台湾省纳入中国。模型仓库包含基座与后续版本；下载表示获取活动；地域为发布者归属；派生关系来自模型声明。以上指标均不直接证明实际部署或公共成效。',9.3,13.7,'muted')
 return q+end()
def main():
 ensure_fonts();export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
 ps=json.loads((D/'content-v0.2.json').read_text())
 tex=r'\documentclass[11pt]{article}\usepackage{layout}\hypersetup{pdftitle={GOSD 2026 第五章合稿评审版 v0.2},pdfsubject={全球供给地图、模型派生与开放条件}}\begin{document}'+'\n'
 tex+=opening()+''.join(content_page(p) for p in ps)+conclusion()+appendix_method()+appendix_sources()+r'\end{document}'
 (R/'report.tex').write_text(tex);compile_tex()
 doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':'GOSD 2026 第五章｜全球开源大模型发展洞察｜评审版 v0.2','author':'全球开源发展报告编制组','subject':'十幅组合图；12 页正文与 2 页附录 A','keywords':'GOSD,模型生态,全球地图,派生,开放条件,AI普惠'})
 dest=O/'GOSD_2026_Chapter5_Merged_Review_v0.2.pdf';doc.save(dest,garbage=3,deflate=True);doc.close();doc=fitz.open(dest)
 for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.55,1.55)).save(R/'review'/f'page-{i+1:02}.png')
 (D/'references-v0.2.json').write_text(json.dumps(REFS,ensure_ascii=False,indent=2));print(json.dumps({'pdf':str(dest),'pages':len(doc),'figures':len(ps)},ensure_ascii=False))
if __name__=='__main__':main()
