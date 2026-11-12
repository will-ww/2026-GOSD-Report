from common import *
C.update(violet='#6B55A4',lightblue='#93B2D0',lightteal='#A5C8C7',gray='#B9C2CD',paleviolet='#F3F0F8')

def grid(f):
    f.line(500,0,500,620);f.line(0,312,1000,312)
def note(f,x,y,t,w=460):return f.wrap(x,y,t,w,17,'muted',leading=23)
def stack(f,x,y,w,h,parts,labels=True):
    total=sum(p[0] for p in parts);off=0
    for val,col,txt in parts:
        ww=w*val/total;f.rect(x+off,y,ww,h,col)
        if labels and ww>tw(txt,18,True)+4:f.text(x+off+ww/2,y+h*.7,txt,18,'white',True,'middle')
        off+=ww
def legend(f,x,y,items,step=125):
    for i,(label,c) in enumerate(items):f.rect(x+i*step,y-13,12,12,c);f.text(x+18+i*step,y,label,17,'muted')

def globalfig():
    f=Figure(620);grid(f)
    f.title(0,25,'1','参与人数与项目影响力');note(f,0,55,'固定 29 国 · 每项单独合计为 100%')
    legend(f,0,85,[('中国与美国','blue'),('其余 27 国','gray')],step=150)
    for i,(lab,val) in enumerate([('活跃人数',34.1),('开发者贡献',37.1),('项目影响力',89.1)]):
        y=119+i*53;f.text(0,y+18,lab,19);stack(f,118,y,350,29,[(val,'blue',f'{val:.1f}%'),(100-val,'gray',f'{100-val:.1f}%')])
    note(f,0,288,'贡献与项目影响力，分别按协作关系计算。')
    f.title(523,25,'2','智能体与模型各需基础支撑');note(f,523,55,'技术全景 · 已记录的 OpenRank 分值占比')
    f.text(523,92,'智能体工具与设施',19,'blue',True);f.text(990,92,'模型训练与运行设施',19,'teal',True,'end')
    stack(f,523,104,467,36,[(52.3,'blue','52.3%'),(47.7,'teal','47.7%')])
    for i,(label,val,col) in enumerate([('智能编程工具',18.3,'blue'),('模型运行引擎',14.0,'teal'),('训练与并行工具',8.5,'violet')]):
        y=163+i*34;f.text(523,y+18,label,18);f.rect(682,y,220*val/20,22,col);f.text(984,y+18,f'{val:.1f}%',18,col,True,'end')
    note(f,523,288,'智能体可连续执行任务；三类合计占 40.8%。')
    f.title(0,347,'3','数据与应用的新增增速更高')
    note(f,0,377,'Hugging Face 新增仓库 · 较上年同期')
    f.text(210,407,'新增 / 万个',17,'muted','', 'end');f.text(470,407,'同比增幅',17,'muted',anchor='end')
    for i,(label,n,v,col) in enumerate([('模型',112.67,7.8,'blue'),('数据集',52.04,101.0,'teal'),('Spaces',87.13,169.3,'violet')]):
        y=424+i*45;f.text(0,y+20,label,19,'ink',True);f.text(210,y+20,f'{n:.2f}',20,col,True,'end')
        f.rect(240,y,132*v/170,24,col);f.text(470,y+20,f'+{v:.1f}%',20,col,True,'end')
    note(f,0,588,'Spaces：可运行的 AI 应用与演示空间。')
    f.title(523,347,'4','改进后的模型也被继续使用')
    note(f,523,377,'模型改进关系：5,777 个模型 · 5,111 条关系')
    xs=[580,750,925]
    for x,label,col in zip(xs,['已有模型','改进版本','后续版本'],['lightblue','teal','lightblue']):
        f.rect(x-56,412,112,47,'pale');f.text(x,442,label,19,col if col=='teal' else 'blue',True,'middle')
    for x,xx in [(636,694),(806,869)]:
        f.line(x,436,xx,436,'teal',2);f.path([(xx-8,431),(xx,436),(xx-8,441)],'teal',2)
    f.text(523,507,'552',39,'teal',True);f.text(629,493,'个版本改进已有模型，',19);f.text(629,519,'又被他人继续使用',19)
    f.text(523,559,'50',32,'violet',True);f.text(590,557,'个版本结合多个已有模型',19)
    note(f,523,593,'按发布者声明统计；两类共同包含 16 个。')
    f.save('6-1-global')

def chinafig():
    f=Figure(620);grid(f)
    f.title(0,25,'1','中国模型进入全球影响榜前列');note(f,0,55,'ModelRank 模型网络影响榜 · 2026 年 6 月')
    legend(f,0,85,[('中国','china'),('美国','blue'),('其余已知','teal'),('未知','gray')],step=121)
    for y,label,vals in [(113,'前 20 位',[9,8,3,0]),(195,'前 100 位',[37,50,7,6])]:
        f.text(0,y+13,label,20,'ink',True)
        stack(f,0,y+26,473,31,[(v,col,str(v)) for v,col in zip(vals,['china','blue','teal','gray'])])
    note(f,0,288,'席位反映网络位置，不代表性能或决策权。')
    f.title(523,25,'2','中国模型被海外团队继续使用');note(f,523,55,'可识别跨国关系样本：10,943 对')
    f.text(523,105,'中国模型 → 美国发布的后续版本',21,'china',True)
    f.text(523,161,'4,639',45,'china',True);f.text(686,159,'对',21,'china')
    f.text(986,161,'42.4%',36,'china',True,'end')
    stack(f,523,180,467,28,[(4639,'china',''),(10943-4639,'gray','')],False)
    note(f,523,239,'已有模型的来源地：中国占 53.8%；\n后续版本的发布地：美国占 68.7%。')
    note(f,523,295,'按发布主体地域统计；非全球完整记录。')
    f.title(0,347,'3','CANN 组织多个仓库共同开发');note(f,0,377,'昇腾计算软件 · 参与账号，已剔除机器人')
    f.text(0,427,'68',40,'china',True);f.text(65,423,'个仓库',20)
    f.text(235,427,'5,282',40,'china',True);f.text(374,423,'个账号',20)
    for i,(label,val) in enumerate([('参与多个仓库',1868),('至少 3 个月参与',1869)]):
        y=454+i*57;f.text(0,y+18,label,18);f.rect(179,y,170*val/5282,23,'china');f.text(470,y+19,f'{val:,} / {val/5282:.1%}',18,'china',True,'end')
    note(f,0,588,'两类账号可以重合；参与不等于负责维护。')
    f.title(523,347,'4','中国成果覆盖多个技术环节')
    rows=[('模型','Qwen / DeepSeek','提供模型和使用示例'),('训练工具','verl','支持模型训练与改进'),('计算软件','CANN / torch_npu','帮助模型软件使用计算设备')]
    for i,(lab,ex,desc) in enumerate(rows):
        y=382+i*65;f.text(523,y+18,lab,18,'muted');f.text(628,y+18,ex,20,'china',True);f.text(628,y+43,desc,17,'ink');f.line(523,y+53,990,y+53)
    note(f,523,604,'以上是功能举例，不表示这些项目全部互联。')
    f.save('6-2-china')

def publicfig():
    f=Figure(620);grid(f)
    f.title(0,25,'1','提供模型、继续改进，都能参与');note(f,0,55,'跨国关系数量 · 选列三国，非地区总量')
    legend(f,0,85,[('提供已有模型','violet'),('发布后续版本','teal')],step=220)
    for i,(name,a,b) in enumerate([('印度',31,162),('巴西',3,146),('印度尼西亚',78,29)]):
        y=108+i*59;f.text(0,y+25,name,19);f.rect(122,y,265*a/170,17,'violet');f.text(122+265*a/170+9,y+15,str(a),18,'violet',True)
        f.rect(122,y+24,265*b/170,17,'teal');f.text(122+265*b/170+9,y+39,str(b),18,'teal',True)
    note(f,0,299,'仅包括双方地域可识别的关系，覆盖有限。')
    f.title(523,25,'2','使用权限与配套材料需要一起看');note(f,523,55,'889 条模型记录 · 沿用来源分级，非独立认证')
    f.text(755,91,'权限较开放',18,'teal',True,'middle');f.text(916,91,'其他权限等级',17,'muted',anchor='middle')
    f.text(523,137,'材料较完整',18,'ink',True);f.text(523,199,'其他材料',18,'muted');f.text(523,222,'等级',18,'muted')
    for x,y,num,col in [(683,105,117,'teal'),(845,105,58,'lightblue'),(683,180,500,'violet'),(845,180,214,'gray')]:
        f.rect(x,y,149,64,col);f.text(x+74.5,y+43,f'{num}',31,'white',True,'middle')
    note(f,523,272,'较完整：材料支持训练及后续环节；较开放：使用和再次分发的权限较宽。')
    f.title(0,347,'3','补齐材料，才能帮助更多人使用')
    f.text(0,399,'19.0%',43,'violet',True);f.text(178,393,'权限较开放的记录中',20);f.text(178,421,'材料也较完整的比例',20)
    note(f,0,453,'117 / 617；其余 500 条未达到材料较完整等级。')
    for i,(name,desc) in enumerate([('成本','能持续负担'),('本地化','适合语言与场景'),('维护','有人负责与交接'),('结果','人们能够实际受益')]):
        x=(i%2)*245;y=479+(i//2)*59;f.rect(x,y,228,49,'paleviolet');f.text(x+10,y+20,name,20,'violet',True);f.text(x+10,y+42,desc,17)
    f.title(523,347,'4','基金会支持共同使用的设施')
    rows=[('投入','云资源或资金 → 共同测试与设施'),('服务','技术支持人员 → 提供持续帮助'),('责任','项目维护者 → 技术评审与决策')]
    for i,(lab,desc) in enumerate(rows):
        y=379+i*61;f.rect(523,y,57,38,'paleviolet');f.text(551.5,y+26,lab,19,'violet',True,'middle');f.wrap(593,y+22,desc,390,18,'ink',leading=23)
    note(f,523,585,'以 PyTorch 机制为例；各地成本、服务效果和全球南方受益规模仍需另行评估。')
    f.save('6-3-public')

def cityfig():
    f=Figure(620);f.line(500,0,500,326);f.line(0,335,1000,335)
    f.title(0,25,'1','模型与数据由不同团队提供');note(f,0,55,'中国组织样本 · 按各类资源累计下载排序')
    f.text(0,95,'模型前三',21,'blue',True);f.text(252,95,'数据集前三',21,'teal',True)
    for i,(a,b) in enumerate(zip(['Qwen','BAAI','deepseek-ai'],['InternRobotics','zai-org','OpenGVLab'])):
        y=137+i*46;f.text(0,y,str(i+1).zfill(2),18,'muted');f.text(38,y,a,22,'blue',True);f.text(252,y,str(i+1).zfill(2),18,'muted');f.text(290,y,b,20,'teal',True)
    f.text(0,283,'79.3%',35,'blue',True);f.wrap(141,276,'模型前三占中国样本模型下载的比例',330,18,leading=24)
    f.title(523,25,'2','城市人才规模与最近一年增长');note(f,523,55,'固定十城人才样本 · 选列五城 · 人')
    legend(f,523,87,[('2025','gray'),('2026','teal')],step=131)
    f.text(900,87,'2025 → 2026',17,'muted',anchor='middle');f.text(994,87,'净增',17,'muted',anchor='end')
    vals=[('北京',902,971),('上海',795,913),('杭州',414,486),('成都',164,181),('武汉',91,105)]
    for i,(name,a,b) in enumerate(vals):
        y=121+i*39;f.text(523,y+7,name,19,'ink',True)
        # Position represents annual population; exact pair labels remain separate and readable.
        f.rect(591,y-9,205*a/1000,7,'gray');f.rect(591,y+2,205*b/1000,7,'teal')
        f.text(900,y+7,f'{a}→{b}',17,'muted','', 'middle');f.text(994,y+7,f'+{b-a}',18,'teal',True,'end')
    note(f,523,321,'杭州 +17.4% 为十城最高；上海净增最多。')
    f.title(0,374,'3','不同资源的集中地，为跨地区合作提供线索')
    note(f,0,405,'累计下载占比 · 模型、数据集各以中国组织样本对应的下载总量计算',w=1000)
    f.text(0,448,'模型下载',21,'blue',True);f.text(200,448,'浙江',20);f.text(990,448,'其余省域',18,'muted',anchor='end')
    stack(f,200,463,790,34,[(56.8,'blue','56.8%'),(43.2,'gray','43.2%')])
    f.text(0,534,'数据集下载',21,'teal',True);f.text(200,534,'北京与上海',20);f.text(990,534,'其余省域',18,'muted',anchor='end')
    stack(f,200,549,790,34,[(75.4,'teal','75.4%'),(24.6,'gray','24.6%')])
    note(f,0,616,'合作方向：让模型、数据与测试团队共同工作；省级数据不能直接说明某个城市或团队的优势。',w=1000)
    f.save('6-4-cities')

def make_all():
    for p in [F,B/'assets']:p.mkdir(parents=True,exist_ok=True)
    for fn in [globalfig,chinafig,publicfig,cityfig]:fn()
    (R/'review/figure-qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
if __name__=='__main__':make_all()
