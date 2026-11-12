from common import *
from section41 import fitted,rounded
P=R/'inputs/42';ROWS=list(csv.DictReader((P/'source/fig-4-2-1_model_landscape_recent_downloads.csv').open(encoding='utf-8-sig')))
ORDER=['text','retrieval','image','multimodal','audio','robotics'];ZH=dict(zip(ORDER,['文本生成','嵌入与检索','图像与视频','多模态','语音与音频','机器人']))
COL=dict(zip(ORDER,['teal','blue','violet','teal','blue','violet']))
DESC={'text':'文字、代码与回答','retrieval':'表示资料并比较相关性','image':'视觉识别与图像生成','multimodal':'联合处理文字和图像','audio':'识别、合成与说话人分离','robotics':'把环境观察连接到动作'}
GROUP={k:[r for r in ROWS if r['domain_key']==k] for k in ORDER}
SUM={k:sum(int(r['downloads']) for r in a) for k,a in GROUP.items()};TOTAL=sum(SUM.values())
COUNTRY={'United States':'美国','China':'中国','Germany':'德国','Brazil':'巴西','France':'法国','United Kingdom':'英国','Italy':'意大利','Singapore':'新加坡','Egypt':'埃及','Unknown':'未识别'}
ALIASES={'tiny-Qwen2ForCausalLM-2.5':'tiny-Qwen2 2.5（测试）','Qwen3-Coder-30B-A3B-Instruct-GGUF':'Qwen3-Coder 30B · GGUF','mobilenetv3_small_100.lamb_in1k':'MobileNetV3 small 100','Wan_2.2_ComfyUI_Repackaged':'Wan 2.2 · ComfyUI 重打包','stable-diffusion-xl-base-1.0':'SDXL Base 1.0','CLIP-ViT-B-32-laion2B-s34B-b79K':'CLIP ViT-B/32 · LAION-2B','CLIP-ViT-L-14-laion2B-s32B-b82K':'CLIP ViT-L/14 · LAION-2B','wav2vec2-large-xlsr-53-japanese':'wav2vec2 XLSR-53 · 日语','wav2vec2-large-xlsr-53-portuguese':'wav2vec2 XLSR-53 · 葡语','wav2vec2-large-xlsr-53-russian':'wav2vec2 XLSR-53 · 俄语','speaker-diarization-community-1':'speaker diarization · 社区 1','mms-300m-1130-forced-aligner':'MMS 300M · 强制对齐','paraphrase-multilingual-MiniLM-L12-v2':'multilingual MiniLM-L12-v2','paraphrase-multilingual-mpnet-base-v2':'multilingual MPNet Base v2','granite-embedding-small-english-r2':'Granite Embed small EN r2','libero4in1_wan2.2vae_latent_cosmos_style':'Libero4in1 · Wan2.2 VAE','openvla-7b-oft-finetuned-libero-spatial':'OpenVLA 7B OFT · Libero'}
def label(r):
 if r['model_name']=='smolvla_libero':return 'SmolVLA Libero · '+('HF-VLA' if r['publisher']=='HuggingFaceVLA' else 'LeRobot')
 return ALIASES.get(r['model_name'],r['model_name'])
def logo(f,r,x,y,s=19):img(f,P/'assets/publisher-logos-png'/(r['publisher_logo_sha256']+'.png'),x,y,s,s)
def aggregates(rows,key):
 d={}
 for r in rows:
  a=d.setdefault(r[key],{'name':r[key],'count':0,'value':0});a['value']+=int(r['downloads']);a['count']+=1
 return sorted(d.values(),key=lambda x:-x['value'])
def title(f,x,y,n,t,fs=21,col='teal'):f.title(x,y,str(n),t,col,fs)
def atlas():
 f=Figure(900);f.text(0,25,'Open Model Landscape · 六类任务',27,'teal',True);f.text(1000,25,'96 个模型仓库 · 每类 16 项',18,'muted',anchor='end')
 for i,k in enumerate(ORDER):
  x=(i%3)*342;y=55+(i//3)*415;co=COL[k];rounded(f,x+1,y,314,400,co)
  f.rect(x+2,y+1,312,56,'pale');title(f,x+10,y+26,i+1,ZH[k],21,co);f.text(x+13,y+49,DESC[k],15.8,'muted')
  for j,r in enumerate(GROUP[k]):
   yy=y+79+j*20.2
   f.text(x+9,yy,f'{j+1:02}',12.5,'muted');logo(f,r,x+31,yy-15.5,17)
   fitted(f,x+55,yy,label(r),246,16.2,'ink',False,minfs=13.4)
 f.text(0,895,'按类内近期下载排序；标识为发布账户；同一家族的不同版本分别列示。',17,'muted')
 f.save('4-2-1-atlas')
def ranklist(f,x,y,rs,limit=20,w=485):
 f.text(x,y,'模型 / 发布账户标识',15,'muted');f.text(x+w,y,'下载 / 万次',15,'muted',anchor='end')
 for i,r in enumerate(rs[:limit]):
  yy=y+27+i*22.5
  if i%2==0:f.rect(x,yy-17,w,22.5,'pale')
  f.text(x+1,yy,f'{i+1:02}',13.6,'muted');logo(f,r,x+26,yy-16,18)
  fitted(f,x+51,yy,label(r),w-141,16.5,bold=i<3,minfs=13.8)
  f.text(x+w,yy,fmt(int(r['downloads'])/10000,1),16.1,'teal',i<3,'end')
def rankings():
 f=Figure(900);title(f,0,26,1,'全景样本前 20 位');ranklist(f,0,55,sorted(ROWS,key=lambda r:-int(r['downloads'])),20,483)
 f.line(500,0,500,524)
 title(f,520,26,2,'发布账户前 15 位');f.text(520,55,'账户',15,'muted');f.text(840,55,'仓库',15,'muted',anchor='end');f.text(1000,55,'下载 / 万次',15,'muted',anchor='end')
 pub=aggregates(ROWS,'publisher')
 for i,p in enumerate(pub[:15]):
  yy=82+i*27;rr=next(r for r in ROWS if r['publisher']==p['name'])
  if i%2==0:f.rect(520,yy-18,480,27,'pale')
  f.text(520,yy,f'{i+1:02}',13.6,'muted');logo(f,rr,546,yy-17,19);fitted(f,573,yy,p['name'],224,17,minfs=14.5)
  f.text(840,yy,str(p['count']),16,'muted',anchor='end');f.text(1000,yy,fmt(p['value']/10000,1),17,'blue',i<3,'end')
 f.text(520,508,f"全样本 {len(pub)} 个账户；按发布账户汇总，不追溯原始训练方。",16,'muted')
 f.line(0,536,1000,536);title(f,0,570,3,'六类任务：样本内下载构成');title(f,520,570,4,'各任务前三位：避免被总榜遮蔽')
 f.text(0,597,'任务',15,'muted');f.text(483,597,'占 96 项下载之和',15,'muted',anchor='end')
 for i,k in enumerate(sorted(ORDER,key=lambda k:-SUM[k])):
  yy=630+i*47;v=SUM[k]/TOTAL*100;f.text(0,yy,ZH[k],18)
  f.rect(119,yy-13,240*v/max(SUM.values())*TOTAL/100,13,COL[k]);f.text(483,yy,f'{v:.2f}%',18,COL[k],True,'end')
  f.text(119,yy+18,fmt(SUM[k]/10000,1)+' 万次',14,'muted')
 for i,k in enumerate(ORDER):
  yy=601+i*48;f.text(520,yy,ZH[k],17,COL[k],True)
  rs=GROUP[k][:3]
  names=' / '.join(label(r) for r in rs)
  # Three concise name positions within the category, while the complete names are in the atlas.
  lines=f.wrap(520,yy+21,names,480,14.6,'ink',leading=17)
 f.save('4-2-2-rankings')
def geography():
 f=Figure(900);title(f,0,26,1,'发布方地域：仓库数与下载份额');f.text(0,54,'期后固定样本 · 未识别地域保留在分母中',16,'muted')
 a=aggregates(ROWS,'country');f.text(0,87,'地域',15,'muted');f.text(346,87,'仓库',15,'muted',anchor='end');f.text(482,87,'下载份额',15,'muted',anchor='end')
 for i,p in enumerate(a):
  y=119+i*28;name=COUNTRY[p['name']];co='china' if name=='中国' else 'blue'
  if i%2==0:f.rect(0,y-18,483,28,'pale')
  f.text(0,y,name,18,co,name in ['中国','美国']);f.rect(100,y-12,179*p['value']/a[0]['value'],12,co,.7)
  f.text(346,y,str(p['count']),17,'muted',anchor='end');f.text(482,y,f"{p['value']/TOTAL*100:.2f}%",18,co,False,'end')
 f.line(500,0,500,425)
 title(f,520,26,2,'按任务分层：前三个发布方地域');f.text(520,54,'各任务分母：入选的 16 项近期下载之和',16,'muted')
 for i,k in enumerate(ORDER):
  y=91+i*55;rs=aggregates(GROUP[k],'country')[:3];f.text(520,y,ZH[k],18,COL[k],True)
  text='　'.join(COUNTRY[p['name']]+' '+f"{p['value']/SUM[k]*100:.1f}%" for p in rs)
  f.text(520,y+24,text,17,'ink')
 f.line(0,438,1000,438);title(f,0,474,3,'中美发布账户：优势随任务改变');f.text(0,504,'点位为本任务样本下载份额，不是全球技术份额',15.8,'muted')
 f.circle(15,532,6,'china');f.text(30,538,'中国',17,'china');f.circle(104,532,6,'blue');f.text(119,538,'美国',17,'blue')
 for t in [0,25,50,75,100]:
  xx=128+t*3.2;f.line(xx,565,xx,832,'line',.8);f.text(xx,858,str(t)+'%',14,'muted',anchor='middle')
 for i,k in enumerate(ORDER):
  yy=589+i*43;d={r['name']:r['value']/SUM[k]*100 for r in aggregates(GROUP[k],'country')};c=d.get('China',0);u=d.get('United States',0)
  f.text(0,yy+5,ZH[k],17);f.line(128+c*3.2,yy,128+u*3.2,yy,'soft',3)
  f.circle(128+c*3.2,yy,5,'china');f.circle(128+u*3.2,yy,5,'blue')
 title(f,520,474,4,'同一地域数字，包含不同供给角色')
 examples=[('Qwen','文本与多模态模型供给','Qwen 多模态账户份额 '+f"{sum(int(r['downloads']) for r in GROUP['multimodal'] if r['publisher']=='Qwen')/SUM['multimodal']*100:.1f}%"),('BAAI','检索表示与相关性排序','BGE 系列进入检索任务样本'),('lmstudio-community','格式转换与本地运行版本','4 个 Qwen MLX 版本 · 占多模态 14.9%'),('jonatasgrosman','语言适配与社区接续','日语、葡语、俄语语音仓库 · 巴西标签')]
 for i,(name,role,desc) in enumerate(examples):
  yy=503+i*83;f.rect(520,yy,480,73,'pale');f.text(534,yy+25,name,19,'teal',True);f.text(534,yy+48,role,16.5);f.text(534,yy+67,desc,14.8,'muted')
 f.text(520,870,'账户所在地不能替代原始模型来源、用户地域或国别贡献。',15.8,'china')
 f.save('4-2-3-geography')
def contents():
 pub=aggregates(ROWS,'publisher');ct={p['name']:p for p in aggregates(ROWS,'country')}
 return [
 page('4.2','4.2 开源模型技术全景','从基础设施转向任务能力：六类模型资源分别连接语言、检索、视觉、声音和物理行动。全景按功能组织，帮助识别互补组件与适配环节。','4-2-1-atlas','图 4-5　六类任务的模型资源全景。来源：2026 版模型技术底表；Hugging Face（HF）2026.10.02 近期下载快照，属期后观察。每类固定 16 项，图标为发布账户；样本不等于全部开放模型，也不是性能推荐。',[
 ('① 用任务组织模型选择','生成回答、检索资料和预测动作承担不同任务。六类各 16 项是选样规则，不能据此认为各类供给规模或成熟度相同。'),
 ('② 下载对象也包括运行版本','量化、格式转换、重打包和测试仓库均保留原样本身份。仓库数量描述可获取资源，不能直接等同独立原创模型数量。'),
 ('③ 检索和语音连接日常使用','检索把资料转为可比较的表示；语音包含转写、合成和说话人分离。系统能力往往来自这些专用组件的组合。'),
 ('④ 机器人模型还要通过设备检验','环境观察到动作预测只是技术接口。实际应用仍需核对设备、动作尺度和任务结果，下载热度不能替代现场验证。')],[],['I02','I03','I05']),
 page('4.2','4.2 任务、项目与发布账户的排名','同一全景可从模型仓库、发布账户和任务类别观察。下载反映资源获取行为；分别比较各任务，才能看见被总体规模遮蔽的专业能力。','4-2-2-rankings','图 4-6　全景样本、发布账户与六类任务的近期下载排名。来源同图 4-5；下载单位为万次。任务份额以 96 项下载之和为分母；类内前三位在各自 16 项中排序。下载不等于独立用户或部署量。',[
 ('① 总榜突出常用基础组件',f"嵌入与检索占样本下载的 {SUM['retrieval']/TOTAL*100:.1f}%。面向资料搜索的专用组件十分突出，但总榜不能代表全部 AI 任务的技术重要性。"),
 ('② 账户排名揭示供给的组织方式',f"96 个仓库来自 {len(pub)} 个发布账户。同一账户可以提供多个版本；账户汇总帮助观察维护集中度，但它仍不是按原创机构或模型家族去重后的排名。"),
 ('③ 小规模任务仍有独立观察价值','机器人类的下载量远低于检索类。保持类内排名，才能识别动作模型与设备适配的入口，避免以总体下载量排除新任务。'),
 ('④ 同时看获取与适配','轻量模型、检索组件和运行版本都进入样本前列。采用方应进一步比较目标语言、运行成本和维护条件，而非只按综合名次选型。')],[],['I02','I03','I05']),
 page('4.2','4.2 发布方地域与跨境接续','地域结构随任务和供给角色而改变。这里观察发布账户的地域标签，分别呈现基础模型、语言适配和运行版本；它与代码贡献者所在地是不同视角。','4-2-3-geography','图 4-7　模型任务的发布方地域与资源接续。来源同图 4-5，沿用冻结账户地域映射；中国 25 项、美国 53 项。未知地域进入分母。下载份额表示这些账户发布仓库的获取量，不表示用户所在地或原始训练贡献。',[
 ('① 总体格局需要拆到任务',f"中国账户占样本下载的 {ct['China']['value']/TOTAL*100:.1f}%，美国为 {ct['United States']['value']/TOTAL*100:.1f}%。两者的位置随任务明显不同，不宜由合计份额推断全面技术领先。"),
 ('② 中国资源形成多层任务入口','Qwen 进入文本与多模态，BAAI 进入检索。它们呈现模型供给的不同功能位置，为后文观察派生、工具适配和全球复用提供对象。'),
 ('③ 发布地域与原始来源可以不同','lmstudio-community 发布的 Qwen MLX 版本说明运行适配具有独立维护对象。账户地域统计与原始模型家族统计应分别保留。'),
 ('④ 全球南方可从具体任务参与','带巴西标签的语音发布账户覆盖多种语言。这个个案展示适配与接续的参与入口；是否形成当地公共能力，还需成本、维护和使用结果。')],[],['I03','I05','I07','I08'])]
def render42():
 atlas();rankings();geography();ps=contents();save_pages('42',ps);return ps
if __name__=='__main__':
 render42();(R/'review/42-figures.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2));print(json.dumps([q for q in QA if q['out_of_bounds'] or q['overlaps']],ensure_ascii=False))
