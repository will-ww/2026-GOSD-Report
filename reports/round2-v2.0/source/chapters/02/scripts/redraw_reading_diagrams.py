from pathlib import Path
import json,xml.etree.ElementTree as E
import svgkit
from svgkit import SVG
R=Path(__file__).resolve().parents[1];svgkit.O=R/'modules/02/figures/27'
s=SVG(166,74)
s.text(0,6,'组织支持与项目自治：把责任落实到可查记录',12,'ink',True)
s.text(0,12,'Apache官方实践 · 责任分工示意，不作治理评分',8.5,'muted')
rows=[('基金会','法律、资产和共同服务','章程、机构决议、基础设施服务'),('项目管理委员会','项目方向、社区与发布','项目治理文件、讨论与发布投票'),('贡献者与提交者','代码、文档、审阅和维护','Issue、PR、邮件讨论、贡献指南')]
for i,(role,duty,record) in enumerate(rows):
 y=17+i*17;s.rect(0,y,166,15,'#F2F5F9',.8);s.rect(0,y,1,15,'#943B9A')
 s.text(4,y+6,role,9.8,'#943B9A',True);s.text(47,y+5.6,duty,10.1,'ink',True);s.text(47,y+12,record,9.1,'muted')
s.text(0,73,'共同服务不取代项目技术决定；公开讨论与发布记录提供责任核查入口。',8.3,'muted')
s.save('governance_roles')
s=SVG(166,147)
s.text(0,6,'许可条件阅读索引',12,'ink',True);s.text(0,12,'选取与复用直接相关的条款；不是许可证优劣排名',8.5,'muted')
rows=[('MIT','版权与许可声明','软件复制件或实质部分须包含版权及许可声明。'),('BSD-3-Clause','声明与不背书','源码、二进制分发须保留相应声明；未经许可不得使用相关名称背书。'),('Apache-2.0','专利许可与分发条件','明确专利许可；分发时保留许可、修改说明及适用的NOTICE内容。'),('GPL-3.0','分发与对应源码','分发受许可覆盖的作品时，依第5—6条处理许可及对应源码义务。'),('AGPL-3.0','修改后的网络交互','修改版本供用户通过网络交互时，依第13条提供对应源码获取方式。'),('MulanPSL-2.0','专利、声明与双语条款','分发保留许可及相关声明；中英文同等效力，冲突时以中文版为准。')]
for i,(name,title,desc) in enumerate(rows):
 y=21+i*19.4;s.line(0,y-3,166,y-3,'line',.28);s.text(0,y+3,name,10,'ink',True);s.text(43,y+3,title,10.2,'#943B9A',True)
 # Max 122 mm; retain exact text, split only at physical width.
 line='';lines=[]
 for ch in desc:
  if svgkit.F.getlength(line+ch)/100*9.2*25.4/72>122:lines.append(line);line=''
  line+=ch
 if line:lines.append(line)
 assert len(lines)<=2
 for j,l in enumerate(lines):s.text(43,y+9+j*4.9,l,9.2,'muted')
s.text(0,146,'统计表的GPL／AGPL未分only与or-later；具体适用须核对完整条款、版本与材料。',8,'muted')
s.save('license_terms')
(R/'review/redrawn_diagrams_checks.json').write_text(json.dumps(svgkit.QA,ensure_ascii=False,indent=2))
print('Redrawn two reading diagrams; original duties and license descriptions retained')
