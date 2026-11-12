"""Three dense portrait figures. All quantities are fixed-source observations."""
from common import *
import shapefile,pycountry
G=json.loads((D/'models100.json').read_text());CN=json.loads((D/'china37.json').read_text());S=json.loads((D/'summary.json').read_text())
LOGO={x['publisher']:x for x in json.loads((R/'assets/model-logos/manifest.json').read_text()) if x.get('status')=='ok'}
C.update(violet='#7253A2',blue='#5063A7',china='#A45B34',teal='#497D80',gold='#9F8740',slate='#AAB4C6',land='#EDF0F4')
SOURCES=[
 {'id':'M1','title':'ModelRank：2026 年 6 月 Top 100 原始归档；输入仓库固定提交 c51e344。','url':BASE.replace('data/processed/chapter3/','preview/content/gosr/model-monthly-source/modelrank-2026-06-top100.raw.json')},
 {'id':'M2','title':'发布者身份与所在地：官方组织页、联系地址和法定披露，2026-11-10 核验。','url':'https://huggingface.co/organizations'},
 {'id':'M3','title':'Lambert & Brand，The ATOM Report，2026-04-08，§2.1、§5.1、图 9 与图 12。','url':'https://arxiv.org/html/2604.07190v1'},
 {'id':'M4','title':'Hugging Face，Summer 2026 Observations，§4；固定文本版本 2026-08-17。','url':'https://github.com/huggingface/blog/blob/9e982d5f2ff0c93248a897bf1e0c59c9828c5ab8/state-of-open-models-summer-2026.md'},
 {'id':'M5','title':'DeepSeek-R1 官方模型卡，§3；六个蒸馏版本的基础模型与训练样本说明。','url':'https://huggingface.co/deepseek-ai/DeepSeek-R1'},
 {'id':'M6','title':'DeepSeek-R1-0528-Qwen3-8B 官方模型卡，§2；跨家族后训练关系。','url':'https://huggingface.co/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B'},
 {'id':'M7','title':'Unsloth / Qwen2.5-7B-Instruct 模型卡；base_model 元数据及版本归属。','url':'https://huggingface.co/unsloth/Qwen2.5-7B-Instruct'},
 {'id':'M8','title':'BAAI / bge-m3 官方模型卡；多语言检索与文本表示用途。','url':'https://huggingface.co/BAAI/bge-m3'}]
def logo(f,n,x,y,s=21):
 if n in LOGO:
  p=R/'assets/model-logos'/LOGO[n]['file'];p=p.with_suffix('.png') if p.with_suffix('.png').exists() else p
  img(f,p,x,y,s,s)
def fittext(f,x,y,t,w,fs=16,c='ink',bold=False):f.text(x,y,t,min(fs,fs*w/max(tw(t,fs,bold),w)),c,bold)
def proj(lon,lat):
 a,b,c,d=1.340264,-.081106,.000893,.003796;t=math.asin(math.sqrt(3)/2*math.sin(math.radians(lat)))
 return 2*math.sqrt(3)*math.radians(lon)*math.cos(t)/(3*(9*d*t**8+7*c*t**6+3*b*t*t+a)),t*(a+b*t*t+c*t**6+d*t**8)
def world(f,x,y,w,h):
 vals={'US':50,'CN':37,'FR':2,'DE':1,'GB':1,'KR':1,'IL':1,'AE':1};xmin,xmax,ymin,ymax=-2.72,2.72,-1.08,1.32
 sc=min(w/(xmax-xmin),h/(ymax-ymin));ox=x+(w-sc*(xmax-xmin))/2;oy=y+(h-sc*(ymax-ymin))/2
 def pt(lon,lat):
  a,b=proj(lon,lat);return ox+(a-xmin)*sc,oy+(ymax-b)*sc
 for sh in shapefile.Reader(str(D/'naturalearth_lowres.shp')).iterShapeRecords():
  rr=sh.record.as_dict();n=rr['name']
  if n=='Antarctica':continue
  try:iso={'France':'FR','Norway':'NO','Kosovo':'XK','Somaliland':'SO','N. Cyprus':'CY','Taiwan':'CN'}.get(n) or pycountry.countries.get(alpha_3=rr['iso_a3']).alpha_2
  except:iso='ZZ'
  v=vals.get(iso);color=mix('#EDE6F4','violet',.2+.8*math.sqrt(v/50)) if v else C['land']
  inds=list(sh.shape.parts)+[len(sh.shape.points)]
  for i in range(len(inds)-1):f.path([pt(*p) for p in sh.shape.points[inds[i]:inds[i+1]]],'white',.5,color)
 return pt
def arrow(f,pts,c='teal',dash=None):
 f.path(pts,c,1.8,dash=dash)
 a,b=pts[-2],pts[-1];ang=math.atan2(b[1]-a[1],b[0]-a[0]);p1=(b[0]-7*math.cos(ang-.45),b[1]-7*math.sin(ang-.45));p2=(b[0]-7*math.cos(ang+.45),b[1]-7*math.sin(ang+.45));f.path([p1,b,p2],c,1.8)
def ranking(f,ds,china=False):
 f.text(0,59,'榜内序 / 模型版本' if china else '名次 / 模型版本',14,'muted')
 f.text(389,59,'全球名次' if china else '发布账户',14,'muted')
 f.text(602,59,'ModelRank',14,'muted',anchor='end')
 short={'black-forest-labs':'BFL','stabilityai':'Stability AI','OnomaAIResearch':'Onoma AI','meta-llama':'Meta Llama','google':'Google','lerobot':'LeRobot','unsloth':'Unsloth'}
 for i,r in enumerate(ds[:20]):
  yy=87+i*26
  if i%2==0:f.rect(0,yy-19,606,26,'pale')
  f.text(0,yy,f'{i+1:02}',15,'muted');logo(f,r['author'],29,yy-17,21)
  name=r['name'].split('/',1)[1];fittext(f,57,yy,name,323,15.5,'ink',i<3)
  if china:f.text(442,yy,r['rank'],16,'china',True,'end')
  else:fittext(f,389,yy,short.get(r['author'],r['author']),110,14.3,'muted')
  f.text(602,yy,fmt(r['score_normalized'],1),16,'ink',i<3,'end')
 f.text(0,613,'分值：2026 年 6 月来源归一化结果；不等于模型能力测试。',14,'muted')
def countrygroup(c):return c if c in ['美国','中国','法国','未识别'] else '英国、德国' if c in ['英国','德国'] else '其他 3 国'
CC={'美国':'blue','中国':'china','法国':'teal','英国、德国':'violet','其他 3 国':'gold','未识别':'slate'}
def fig_global():
 f=Figure();panel(f,0,27,1,'全球模型影响力前 20 位');ranking(f,G);f.line(620,0,620,805)
 panel(f,638,27,2,'发布组织的世界分布',19)
 f.text(638,58,'94 席归属可识别 · 8 个国家',15,'muted')
 point=world(f,632,77,368,210)
 for lon,lat,tx,ty,label,anchor in [(-100,38,642,99,'美国 50','start'),(104,35,998,266,'中国 37','end'),(4,49,995,100,'欧洲 4：法 2、英德各 1','end')]:
  px,py=point(lon,lat);f.circle(px,py,3,'violet');f.line(px,py,tx+2 if anchor=='start' else tx-2,ty-5,'soft',.8);ww=tw(label,14.2);f.rect(tx-3 if anchor=='start' else tx-ww-3,ty-17,ww+6,22,'white',.96);f.text(tx,ty,label,14.2,'ink',False,anchor)
 for i,v in enumerate([1,2,37,50]):
  xx=638+i*60;f.rect(xx,294,19,10,mix('#EDE6F4','violet',.2+.8*math.sqrt(v/50)));f.text(xx+23,305,v,13,'muted')
 f.text(998,305,'席 / 国家',13,'muted',anchor='end')
 f.wrap(638,331,'韩国、以色列、阿联酋各 1 席。\n按组织归属；灰色为未列明。',360,14.5,'muted',leading=21)
 panel(f,638,389,3,'百强席位与排名梯次',19)
 for i,r in enumerate(G):f.rect(638+i%10*16,411+i//10*16,13,13,CC[countrygroup(r['country'])])
 groups=list(CC)
 for i,n in enumerate(groups):
  yy=427+i*27;f.rect(812,yy-12,11,11,CC[n]);f.text(833,yy,n,14.5);f.text(998,yy,sum(countrygroup(r['country'])==n for r in G),19,CC[n],True,'end')
 f.text(638,595,'每格 1 个版本，按全球名次逐行排列。',13.6,'muted')
 for x,t in [(638,'组织国别'),(815,'1—10'),(906,'11—30'),(998,'31—100')]:f.text(x,631,t,13.5,'muted',anchor='start' if x==638 else 'end')
 for i,n in enumerate(groups):
  yy=659+i*26;f.text(638,yy,n,14.6)
  for x,a,b in [(815,1,10),(906,11,30),(998,31,100)]:f.text(x,yy,sum(countrygroup(r['country'])==n and a<=r['rank']<=b for r in G),16,CC[n],True,'end')
 panel(f,0,652,4,'百强任务结构 · 语言之外的复用节点',19.5)
 items=[('文本生成',38),('图文输入转文本',20),('文本生成图像',6),('跨模态转换',6),('语音识别',6),('零样本图像分类',6),('填词预测',4),('句子相似度',4),('特征提取',3),('机器人',1),('图像生成视频',1),('未标注任务',5)]
 for i,(n,v) in enumerate(items):
  col=i//4;row=i%4;x=col*208;y=692+row*31
  f.rect(x,y-12,3,15,'slate' if n=='未标注任务' else 'teal');f.text(x+11,y,n,14.5,'muted');f.text(x+192,y,v,19,'slate' if n=='未标注任务' else 'teal',True,'end')
 f.save('fig-3-17-model-global')
def china_outline(f,x,y,w,h):
 shapes=[s.shape for s in shapefile.Reader(str(D/'naturalearth_lowres.shp')).iterShapeRecords() if s.record.as_dict()['name'] in ['China','Taiwan']]
 xmin,xmax,ymin,ymax=73,135,18,54;sc=min(w/(xmax-xmin),h/(ymax-ymin));ox=x+(w-62*sc)/2;oy=y+(h-36*sc)/2
 def pt(lon,lat):return ox+(lon-xmin)*sc,oy+(ymax-lat)*sc
 for sh in shapes:
  inds=list(sh.parts)+[len(sh.points)]
  for i in range(len(inds)-1):f.path([pt(*p) for p in sh.points[inds[i]:inds[i+1]]],'#BBC7D4',.6,'#EDF0F4')
 return pt
def fig_china():
 f=Figure();panel(f,0,27,1,'中国发布模型 · 百强内前 20 位',20);ranking(f,CN,True);f.line(620,0,620,805)
 panel(f,638,27,2,'两类发布主体的供给',19.5)
 f.text(638,58,'Qwen 36 席 · 智源 BAAI 1 席',15,'muted')
 point=china_outline(f,645,78,343,198)
 for lon,lat,tx,ty,t in [(116.4,39.9,638,95,'北京 · 智源 BAAI'),(120.2,30.3,798,264,'杭州 · 阿里巴巴')]:
  px,py=point(lon,lat);f.circle(px,py,4,'violet');f.line(px,py,tx+8,ty-6,'soft',1);ww=tw(t,14.5);f.rect(tx-2,ty-18,ww+4,23,'white',.97);f.text(tx,ty,t,14.5)
 f.text(638,302,'Qwen：企业发布的通用模型系列',14.6,'ink')
 f.text(638,329,'BAAI：非营利研究机构的检索底座',14.6,'ink')
 f.text(638,355,'地点为组织节点，不代表模型研发全址。',13.4,'muted')
 panel(f,638,396,3,'任务布局与专长',19.5)
 vals=[('文本生成',22,'violet'),('图文输入转文本',13,'teal'),('特征提取',1,'gold'),('句子相似度',1,'gold')]
 for i,(n,v,c) in enumerate(vals):
  yy=443+i*57;f.text(638,yy,n,15.2);f.text(998,yy,f'{v} 席',19,c,True,'end');f.rect(638,yy+9,360,10,'pale');f.rect(638,yy+9,360*v/37,10,c)
 f.rect(638,677,360,96,'pale');logo(f,'BAAI',650,689,27);f.text(687,711,'bge-m3',20,'ink',True);f.text(982,711,'全球第 51',18,'gold',True,'end')
 f.wrap(650,740,'把文字转为可比较的表示，支撑检索；\n与通用生成模型形成任务互补。',337,14.1,'muted',leading=21)
 panel(f,0,652,4,'Qwen 的 36 席：多代并存，小规模居多',19.5)
 f.text(0,684,'系列 / 型号规模',13.4,'muted')
 for x,t in [(245,'≤1B'),(354,'1—10B'),(457,'>10B'),(594,'合计')]:f.text(x,684,t,13.4,'muted',anchor='end')
 for i,fam in enumerate(['Qwen2.5','Qwen3','Qwen3.5','Qwen3.6']):
  yy=710+i*24;f.text(0,yy,fam,14.6)
  for j,band in enumerate(['≤1B','1—10B','>10B']):
   n=S['qwen_family_size'][fam][band];xx=166+j*105;f.rect(xx,yy-16,92,21,mix('white','violet',.13+.7*n/10) if n else 'pale');f.text(xx+46,yy,n,15,'white' if n>=6 else 'ink',True,'middle')
  f.text(594,yy,S['qwen_family'][fam],16,'violet',True,'end')
 f.save('fig-3-18-model-china')
def fig_families():
 f=Figure();f.line(500,0,500,364);f.line(0,382,1000,382);f.line(620,402,620,805)
 panel(f,0,27,1,'两种采用路径：模型规模不同',20)
 f.text(0,58,'ATOM · 2023.11—2026.03 · 开放语言模型',14.2,'muted')
 for yy,n,share,c in [(108,'小于 10B 组：Qwen',44,'violet'),(212,'250B 以上组：DeepSeek',47,'teal')]:
  f.text(0,yy,n,18,'ink',True);f.text(478,yy,f'{share}%',29,c,True,'end')
  f.rect(0,yy+16,478,29,'pale');f.rect(0,yy+16,478*share/100,29,c);f.text(0,yy+67,'占该规模组累计下载；每条的分母各自独立。',13.6,'muted')
 f.text(0,323,'31.1%',28,'teal',True);f.text(115,319,'DeepSeek 的调用份额',17,'ink',True)
 f.wrap(115,342,'2026.01 · OpenRouter 每月前十开放模型\n样本的 token（文本处理单位）份额。',366,13.4,'muted',leading=19)
 panel(f,520,27,2,'Qwen 底座的社区接续',20)
 f.text(520,58,'HF 夏季报告 · 期后发布的独立观察',14.2,'muted')
 f.text(520,115,'151,448',43,'violet',True);f.text(520,145,'个社区衍生仓库',18,'ink',True)
 f.text(520,172,'是下游改造与再发布，并非 Qwen 自行发布。',14,'muted')
 f.line(520,193,1000,193)
 f.text(520,224,'GGUF 转换仓库',18,'ink',True);f.text(998,224,'28,531',27,'teal',True,'end')
 f.rect(520,244,478,23,'teal');f.rect(520,244,max(1,478*54/28531),23,'violet')
 f.text(520,292,'Qwen 官方 54',15,'violet',True);f.text(998,292,'其他账户 28,477',16,'teal',True,'end')
 f.text(520,325,'99.8% 由非 Qwen 账户发布',21,'teal',True)
 f.text(520,353,'GGUF：常用于本地运行的模型文件格式。',14,'muted')
 panel(f,0,424,3,'蒸馏：推理样本与基础权重相结合',19.7)
 f.rect(167,447,278,62,'pale');img(f,R/'assets/model-logos/deepseek-ai.png',181,455,26,26);f.text(323,473,'DeepSeek-R1',22,'teal',True,'middle');f.text(306,496,'生成训练用的推理样本',15,'muted',False,'middle')
 # Solid arrows are base-weight inheritance; dashed arrows are sample transfer.
 f.rect(0,552,204,67,'pale');logo(f,'Qwen',12,564,28);f.text(50,580,'Qwen2.5 系列',17,'violet',True);f.text(12,605,'4 个基础模型版本',14.5,'muted')
 f.rect(0,651,204,67,'pale');logo(f,'meta-llama',12,663,28);f.text(50,679,'Llama 3 系列',17,'blue',True);f.text(12,704,'2 个基础模型版本',14.5,'muted')
 f.rect(304,552,300,67,mix('white','violet',.09));f.text(317,580,'R1-Distill-Qwen',19,'violet',True);f.text(317,605,'1.5B / 7B / 14B / 32B',16)
 f.rect(304,651,300,67,mix('white','blue',.09));f.text(317,679,'R1-Distill-Llama',19,'blue',True);f.text(317,704,'8B / 70B',16)
 arrow(f,[(204,590),(298,590)],'violet');f.text(213,577,'权重',14,'violet')
 arrow(f,[(204,689),(298,689)],'blue');f.text(213,676,'权重',14,'blue')
 arrow(f,[(445,478),(580,478),(580,546)],'teal','5 4');f.text(474,502,'样本',14,'teal')
 arrow(f,[(167,478),(145,478),(145,527),(285,527),(285,638),(580,638),(580,645)],'teal','5 4')
 f.text(0,754,'后续接续：R1-0528 推理样本 + Qwen3-8B-Base',14.5,'ink',True)
 f.text(0,783,'→ DeepSeek-R1-0528-Qwen3-8B（2025.05）',15,'teal')
 panel(f,638,424,4,'跨账户复用，跨境接续',19)
 f.text(638,454,'同一 Qwen 底座，在两种发布位置出现',14.5,'muted')
 logo(f,'Qwen',650,480,30);f.text(692,502,'Qwen · 中国',19,'violet',True)
 f.text(650,532,'Qwen2.5-7B-Instruct',17);f.text(650,561,'全球第 6 · ModelRank 12,230.3',14.8,'muted')
 arrow(f,[(814,578),(814,618)],'violet');f.text(831,603,'声明的底座关系',14,'violet')
 logo(f,'unsloth',650,635,30);f.text(692,657,'Unsloth · 美国',19,'blue',True)
 f.text(650,687,'Qwen2.5-7B-Instruct',17);f.text(650,716,'全球第 10 · ModelRank 7,912.5',14.8,'muted')
 f.wrap(638,755,'训练适配与分发也形成网络位置。\n不能把再发布归属改写为底座来源。',360,14.5,'muted',leading=22)
 f.save('fig-3-19-qwen-deepseek')
def render():
 fig_global();fig_china();fig_families()
 pages=[page('3.6','3.6 全球开源模型影响力排行榜','ModelRank 从模型派生与复用关系观察影响位置。本节以 2026 年 6 月百强快照为入口，连接发布组织、任务类型与模型家族；入榜不等于能力领先或开放程度认证。','fig-3-17-model-global',
 '图 3-17　全球模型前 20 位、发布组织分布与百强结构。来源：ModelRank 6 月原始归档［M1］；组织归属核验［M2］。94 席可定位，6 席未识别；地图不表示贡献者、训练数据或使用者的所在地。',[
 ('① 头部影响位置跨越语言、视觉与机器人','FLUX.1-dev 和 Stable Diffusion XL 基础版居前两位；前十有 5 个文本生成版本、4 个图像生成版本和 1 个机器人模型。榜单呈现的是多种复用节点，公共资源建设应兼顾这些任务差异。'),
 ('② 地图呈现组织布局，贡献仍跨越国界','按发布组织归属，美国占 50 席、中国占 37 席，其余 7 席分布于 6 国，另有 6 席未知。组织所在国提供空间入口；底座继承、社区适配和跨国维护关系，仍须沿具体模型继续追踪。'),
 ('③ 席位数量与头部位置并不同序','中国的 37 席中有 16 席进入前三十；美国的 50 席中有 10 席进入前三十。英德虽各仅一席，却占据前两位。数量、排名梯次与技术专长共同构成格局，任何单项都不足以概括国家能力。'),
 ('④ 全景观察让支撑性任务显现','文本生成占 38 席，其余版本覆盖图文理解、语音、检索与特征表示等任务，5 席尚无任务标注。面向产业与公共服务，选型应回到用途、运行成本和维护条件，不能由通用名次直接替代。')],SOURCES[:2],['I01','I03','I04']),
 page('3.6','3.6 中国模型：榜内位置与供给结构','本页聚焦全球百强中可识别的 37 个中国发布模型，展示其中前 20 位；这是百强子集，不是完整中国模型总榜。B 表示十亿参数，型号规模用于描述供给层次。','fig-3-18-model-china',
 '图 3-18　中国发布模型的全球位次、组织节点与任务分布。来源：6 月快照［M1］、组织核验［M2］、bge-m3 模型卡［M8］。规模按型号标称值分组，Qwen 的 36 席中有 31 席不超过 10B；不据此估算实际运行成本。',[
 ('① 多代模型共同构成持续可复用的底座','Qwen 占 36 席，9 席进入全球前二十；榜内前二十的中国版本均来自 Qwen。Qwen2.5、Qwen3、Qwen3.5 与 Qwen3.6 同时出现，说明既有版本仍占据复用位置，不能只追踪最新发布。'),
 ('② 企业系列与科研专长形成互补','样本连接杭州的阿里巴巴与北京智源两类主体：前者提供通用模型系列，后者以 bge-m3 进入第 51 位。组织节点揭示供给的不同载体，尚不足以推出城市整体实力、人才聚集或政策成效。'),
 ('③ 生成之外，检索能力也进入头部网络','37 席包括文本生成 22 席、图文输入转文本 13 席，以及特征提取、句子相似度各 1 席。检索与表示模型有助于把知识资源接入应用；单看对话模型会遗漏这类支撑环节。'),
 ('④ 小规模覆盖提供可及性线索','Qwen 的 36 席中，31 席的型号参数量不超过 10B，包含 7 席不超过 1B。这种供给层次为不同部署条件提供选择；能否转化为 AI 普惠，还需验证硬件成本、本地语言效果和长期维护。')],SOURCES[:2]+[SOURCES[-1]],['I04','I08','I10','I12']),
 page('3.6','3.6 Qwen 与 DeepSeek：互补与接续','从单个版本转向模型家族，可以同时看见广泛的社区复用、大模型服务需求，以及推理经验跨底座传递。以下保留各来源窗口，解释连接关系，不合成为一个“综合领先”分数。','fig-3-19-qwen-deepseek',
 '图 3-19　Qwen 与 DeepSeek 的采用结构、社区转换与跨家族接续。来源：ATOM［M3］、HF 夏季报告［M4］、DeepSeek 模型卡［M5］［M6］、6 月榜单及 Unsloth 模型卡［M1］［M7］。不同平台与窗口分别标注。',[
 ('① 两种优势对应不同的使用条件','ATOM 样本中，Qwen 占小于 10B 组累计下载的 44%，DeepSeek 占 250B 以上组的 47%；调用数据补充了后者的服务使用。部署与复用路径不同，不能由六月榜内未见 DeepSeek 就推断其缺乏影响。'),
 ('② 社区承担把模型变得可用的工作','HF 观察到大量 Qwen 衍生与格式转换；GGUF 仓库中，非 Qwen 账户承担 99.8% 的发布。模型团队之外的适配、分发与维护值得持续观测；转换数量本身尚不证明质量、实际部署或受益人数。'),
 ('③ 中国贡献体现为底座与推理经验','通过蒸馏，DeepSeek-R1 将生成的推理示例用于训练较小模型，形成 Qwen 与 Llama 底座上的六个版本，后续又接续到 Qwen3。基础权重与训练样本分别贡献能力，体现跨家族、跨主体再创造。'),
 ('④ 全球协作需要保留来源与维护责任','Qwen 与 Unsloth 的同名版本分别进入榜单第 6 与第 10 位，说明底座供给与适配分发均可能获得网络位置。公共平台应保留来源、版本及转换说明，把互操作、质量复核和维护纳入支持范围。')],SOURCES,['I03','I04','I05','I08'])]
 save_pages('36',pages);return pages
