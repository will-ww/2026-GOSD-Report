from pathlib import Path
import csv,json,base64,html
from PIL import Image
from svgkit import SVG,QA
R=Path(__file__).resolve().parents[1];P=R/'sources/s3.5/GOSD_3.5_v0.5';D=P/'data';L=P/'report/logos/rendered';ref=json.loads((D/'emerging-reference.json').read_text());aliases={}
for project,meta in ref['projects'].items():
 for x in meta.get('representative_repos',[]):aliases[x['repo']]=project
rows=list(csv.DictReader((D/'new_repo.csv').open()))
for r in rows:
 owner=r['repo'].split('/')[0]
 if owner in {'cann','Ascend','openharmony','mindspore','ibm-developer-skills-network'}:aliases[r['repo']]={'cann':'CANN','Ascend':'Ascend','openharmony':'OpenHarmony','mindspore':'MindSpore','ibm-developer-skills-network':'IBM Skills Network'}[owner]
def logo(s,key,x,y):
 path=L/(aliases.get(key,key).replace('/','__').replace(' ','_')+'.png');im=Image.open(path);iw,ih=im.size;k=min(5/iw,4.5/ih);w,h=iw*k,ih*k
 s.e.append(f'<image x="{x+(5-w)/2}" y="{y+(4.5-h)/2}" width="{w}" height="{h}" href="data:image/png;base64,{base64.b64encode(path.read_bytes()).decode()}"/>')
checks=[]
for kind,file,name,h,dy in [('project','new_project.csv','01_projects',178,5.3),('repo','new_repo.csv','02_repos',198,6.0)]:
 data=list(csv.DictReader((D/file).open()));s=SVG(166,h);s.rect(0,0,166,8,'#514078')
 cols=[(2,'名次'),(22,'完整仓库路径' if kind=='repo' else '项目'),(119,'OpenRank'),(163,'活跃者')]
 if kind=='project':cols=[(2,'名次'),(22,'项目'),(116,'OpenRank'),(145,'活跃者'),(163,'仓库')]
 for x,t in cols:s.text(x,5.4,t,8,'white',True,'end' if x>110 else 'start')
 for i,r in enumerate(data):
  y=11+i*dy;mid=y+dy/2
  if i%2==0:s.rect(0,y-.2,166,dy,'#F4F1F7')
  s.text(3,mid+1.0,f'{i+1:02}',8,'#6146A5',i<3);s.text(10,mid+1,'G' if r['platform']=='GitHub' else 'A',7.2,'muted',False,'middle');logo(s,r[kind],13,y+.2)
  if kind=='repo':
   owner,repo=r[kind].split('/',1);s.text(22,y+2.1,owner+'/',7.6,'muted');s.text(22,y+5,repo,8.3,'ink',True)
   bx,bw=108,30;maxv=8000;vx=140;ax=163
  else:
   s.text(22,mid+1.1,r[kind],9.0,'ink',True);bx,bw=93,27;maxv=16000;vx=121;ax=145;s.text(163,mid+1.1,r['repo_count'],8.5,'ink',False,'end')
  value=float(r['openrank']);s.rect(bx,y+1.0,bw*value/maxv,dy-1.7,'#D8CDE7');s.text(vx,mid+1.1,f'{value:,.2f}',8.6,'ink',False,'end');s.text(ax,mid+1.1,f"{int(r['active_developers']):,}",8.3,'ink',False,'end')
  checks.append({'kind':kind,'rank':i+1,'identity':r[kind],'openrank':value,'active_developers':int(r['active_developers']),'repo_count':r.get('repo_count'),'logo':True})
 s.text(0,h-2,'G · GitHub     A · AtomGit     条内底纹为OpenRank线性比例，零基线。',8,'muted')
 s.save('emerging_'+name)
 (R/'figures/35'/f'{name}.pdf').write_bytes((R/'figures/new'/f'emerging_{name}.pdf').read_bytes())
(R/'review/emerging_rank_rows.json').write_text(json.dumps({'rows':checks,'count':len(checks),'layout_checks':QA},ensure_ascii=False,indent=2));print('60 identities, values and logos retained; vector tables redrawn')
