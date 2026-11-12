from build import *
from section36 import render,SOURCES,G,CN

ensure_fonts();export(R/'assets/osdgs-symbol-compact.svg',B/'assets/osdgs-compact.pdf')
PAGES=render()
tex=r'\documentclass[11pt]{article}\usepackage{layout}\begin{document}'+'\n'
def refs(s):
 for so in SOURCES:
  token='［'+so['id']+'］'
  target=(r'\hyperlink{org-evidence}{'+token+'}') if so['id']=='M2' else (r'\href{'+so['url'].replace('&',r'\&')+'}{'+token+'}')
  s=s.replace(token,target)
 return s
for i,p in enumerate(PAGES):
 tex+=rf'\begin{{canvas}}\Header{{第三章 · 全球开源影响力排行榜}}{{violet}}\Footer{{{i+1:02}}}'+'\n'
 tex+=box(15,27,180,p['title'],20,27,'ink',True)+box(15,40,180,p['intro'],9.7,13.5,'muted',False,True)
 tex+=rf'\Box{{15}}{{53}}{{180}}{{\includegraphics[width=180mm]{{.build/assets/{p["figure"]}.pdf}}}}'+'\n'
 tex+=refs(box(15,199,180,p['caption'],7.6,10.7,'muted',False,True))
 for j,(t,b) in enumerate(p['analyses']):
  x=15+j%2*93;y=214+j//2*34
  tex+=box(x,y,87,t,10.3,14.2,'violet',True)+box(x,y+6,87,b,9.9,15)
 tex+=r'\end{canvas}'+'\n'
tex+=r'\begin{canvas}\Header{第三章 · 附录 1（本节摘录）}{violet}\Footer{04}'+'\n'
tex+=box(15,27,180,'附录 1　指标、证据与本轮评审说明',18.6,25,'ink',True)
tex+=box(15,40,180,'3.6 修订稿 v0.2 · 2026 年 11 月 10 日｜3 页正文、3 幅组合图；未提交 GitHub。',9.1,13,'muted',False,True)
tex+=box(15,50,180,'榜单与地理：保留同一快照，补齐身份核验',10.4,14,'violet',True)
tex+=box(15,56,180,'主期为 2025-07-01 至 2026-06-30；本节采用期末 6 月 ModelRank 月榜，非全年累计。分值沿用来源归一化结果，完整算法复现尚待核验。百强按 22 个发布账户保留；地理汇总将同一机构关联账户映射到组织所在国，94 席可识别。组织资料于 11 月核验，不代表贡献者地理或历史团队全貌。',8.8,13,'ink',False,True)
tex+=box(15,79,180,'外部观察：不同指标解释不同的影响路径',10.4,14,'violet',True)
tex+=box(15,85,180,'ATOM 跟踪约 1,500 个重点开放权重语言模型；图中下载份额按规模组分别计算，OpenRouter 仅覆盖每月前十开放模型。HF 夏季报告分析 1—7 月活动并在 8 月补充发布，本节使用其累计衍生与转换观察。二者均不并入 6 月榜单；下载、token 与派生仓库均不等同独立用户、公共成效或全部 AI 市场份额。',8.8,13,'ink',False,True)
tex+=r'\Box{15}{109}{180}{\hypertarget{org-evidence}{}\sffamily\bfseries\fontsize{10.2}{14}\selectfont\color{violet}［M2］组织国别核验（点击机构名访问证据；数字为模型席位）}'+'\n'
geo=json.loads((D/'publisher-geography.json').read_text());gb={g['publisher']:g for g in geo}
left=[('google','Google · 美国 20'),('facebook','Meta · 美国 13（3 个账户）'),('openai','OpenAI · 美国 7'),('lerobot','Hugging Face · 美国 2（2 个账户）'),('jhu-clsp','JHU CLSP · 美国 2'),('krea','Krea · 美国 2'),('LiquidAI','Liquid AI · 美国 2'),('unsloth','Unsloth · 美国 2')]
right=[('Qwen','阿里巴巴 / Qwen · 中国杭州 36'),('BAAI','智源 BAAI · 中国北京 1'),('black-forest-labs','Black Forest Labs（BFL）· 德国 1'),('stabilityai','Stability AI · 英国 1'),('mistralai','Mistral AI · 法国 2'),('OnomaAIResearch','Onoma AI · 韩国 1'),('Lightricks','Lightricks · 以色列 1'),('tiiuae','TII · 阿联酋 1')]
for col,items in enumerate([left,right]):
 for i,(key,label) in enumerate(items):
  line=box(15+col*93,117+i*5.7,87,label,8.4,11.3,'muted',False,True)
  line=line.replace(esc(label),r'\href{'+gb[key]['location_source']+'}{'+esc(label)+'}')
  tex+=line
tex+=box(15,165,180,'未识别：intfloat 4、KBlueLeaf 1、cmz1024 1；不按姓名或语言推定。图 3-18 的规模为型号标称总参数量；1—10B 不含 1B，35B-A3B 计 35B。底图仅用于组织分布示意。',8.2,11.7,'muted',False,True)
tex+=box(15,180,180,'数据与关系来源（点击编号访问固定文本或官方模型卡）',10.4,14,'violet',True)
for i,s in enumerate([s for s in SOURCES if s['id']!='M2']):
 tex+=refs(box(15,187+i*5.6,180,'［'+s['id']+'］ '+s['title'],8.1,11.5,'muted',False,True))
tex+=box(15,229,180,'修改内容、证据状态与评审重点',10.4,14,'violet',True)
tex+=box(15,236,180,'本轮重构为全球榜、中国百强子集、Qwen 与 DeepSeek 三幅组合图；新增世界地图、百强排名梯次、发布组织节点、规模矩阵和两类关系箭头。第三图以少量案例解释榜单，模型网络与开放条件的系统展开仍归第五章。',8.8,13,'ink',False,True)
tex+=box(15,253,180,'待核查：ModelRank 完整算法与历史版本链；6 席地理、5 席任务未知；逐版本开放许可及实际部署结果。DeepSeek 未出现在本期百强，外部采用证据作为补充，不人为补排。正式合稿时联动全章图号、页码、附录与主张地图。',8.8,13,'ink',False,True)
tex+=box(15,273,180,'请重点评审：中国页的样本边界是否清楚；第三图是否充分体现互补、全球接续与公共能力。',8.7,12,'violet',True)
tex+=r'\end{canvas}\end{document}'
(R/'report.tex').write_text(tex);(D/'content.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2));(D/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2));(R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
compile_tex()
doc=fitz.open(O/'report.pdf');doc.set_metadata({'title':'GOSD 2026 精要版｜3.6 全球开源模型影响力排行榜｜修订稿 v0.2','author':'全球开源发展报告编制组','subject':'2026-11-10；全球模型榜、中国模型与 Qwen/DeepSeek 生态；待评审'})
doc.set_toc([[1,p['title'],i+1] for i,p in enumerate(PAGES)]+[[1,'附录 1　指标、证据与本轮评审说明',4]])
for pn,ds in [(0,G),(1,CN)]:
 for i,r in enumerate(ds[:20]):
  sc=180/1000*72/25.4;x,y,w,h=57,87+i*26-19,323,26
  rect=fitz.Rect(15*72/25.4+x*sc,53*72/25.4+y*sc,15*72/25.4+(x+w)*sc,53*72/25.4+(y+h)*sc)
  doc[pn].insert_link({'kind':fitz.LINK_URI,'from':rect,'uri':'https://huggingface.co/'+r['name']})
out=O/'GOSD_2026_Section_3-6_Review_v0.2.pdf';doc.save(out,garbage=1,deflate=True);doc.close();doc=fitz.open(out)
for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.85,1.85)).save(R/'review'/f'page-{i+1}.png')
print('BUILT',out,len(doc));print(json.dumps(QA,ensure_ascii=False))
