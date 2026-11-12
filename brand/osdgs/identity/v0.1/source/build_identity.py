#!/usr/bin/env python3
"""OSDGs companion identity system, review v0.1. Native SVG extension of v2.0.
Approved master geometry, ten IDs, names, colours and dimension glyphs are reused.
"""
from pathlib import Path
import os, json, math, shutil, importlib.util, hashlib, textwrap

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'baseline'
os.environ.setdefault('OSDGS_FONT_LAT','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
os.environ.setdefault('OSDGS_FONT_LAT_B','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
spec=importlib.util.spec_from_file_location('baseline',BASE/'source/render_assets.py')
B=importlib.util.module_from_spec(spec);spec.loader.exec_module(B)
# Keep editable SVG declarations aligned with the actual supplied font files.
_baseline_pilfont=B.pilfont
_baseline_outline_font=B.outline_font
B.pilfont=lambda fam,bold:_baseline_pilfont('Inter' if fam=='DejaVu Sans' else fam,bold)
B.outline_font=lambda fam,bold:_baseline_outline_font('Inter' if fam=='DejaVu Sans' else fam,bold)
import cairosvg
S=B.S
D=B.DIMS;P=B.PILLARS
NAVY='#102950';NIGHT='#0B2047';MUTED='#597088';LINE='#DCE5F0';WHITE='#FFFFFF'
AS=ROOT/'assets';PAGES=ROOT/'pages';QA=[]

def t(s,x,y,txt,pt=10,col=NAVY,b=False,anchor='start',fam='Noto Sans CJK SC'):
    if fam=='Inter':fam='DejaVu Sans'
    s.t(x,y,txt,pt,col,b,anchor,fam=fam)

def save(s,path,png=0,pdf=False):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.with_suffix('.svg').write_text(s.svg(),encoding='utf8')
    outlined=path.parent/(path.name+'-outlined.svg')
    B.outline_svg(path.with_suffix('.svg'),outlined)
    if png:cairosvg.svg2png(url=str(outlined),write_to=str(path.with_suffix('.png')),output_width=png)
    if pdf:
        # The baseline renderer uses the Inter family slot for font metrics.
        # Explicitly declare the supplied DejaVu substitute for the editable PDF.
        pdf_svg=s.svg().replace('font-family="Inter"','font-family="DejaVu Sans"')
        cairosvg.svg2pdf(bytestring=pdf_svg.encode(),write_to=str(path.with_suffix('.pdf')))
    bad=[a for a in s.labels if a['x']<-.3 or a['x']+a['w']>s.w+.3 or a['y']<-.3 or a['y']+a['h']>s.h+.3]
    QA.append({'asset':str(path.relative_to(ROOT)),'text_count':len(s.labels),'out_of_bounds':bad})
    if bad:print('OVERFLOW',path.name,bad)

def node_signature(s,x,y,w,active=None,color=WHITE):
    for i in range(10):
        s.circle(x+i*w/9,y,.6 if i!=active else .9,color,op=1 if i==active or active is None else .25)

def tile(d,style='solid',lang='zh'):
    s=S(60,60,None,d['id']+' '+d['name_zh']+' / '+d['name_en'])
    co=d['color'];fg=WHITE if style=='solid' else co
    s.rect(0,0,60,60,co if style=='solid' else '#F8FAFD',rx=1.2)
    if style=='light':s.rect(0,0,60,1.2,co);s.rect(.3,.3,59.4,59.4,'none',LINE,.3,1.2)
    # Swept corner is a decorative companion motif; it is not a replacement master emblem.
    s.e.append('<defs><clipPath id="tileClip"><rect width="60" height="60" rx="1.2"/></clipPath></defs><g clip-path="url(#tileClip)">')
    s.path('M40 59 C61 47 63 28 55 15',WHITE if style=='solid' else co,.45,op=.12)
    s.path('M48 60 C60 50 66 35 60 25',WHITE if style=='solid' else co,1.7,op=.055)
    s.e.append('</g>')
    t(s,4.6,10.4,d['id'][1:],21,fg,True,fam='Inter')
    t(s,55.2,8.4,d['pillar']+' / '+d['source_code'],6.7,fg,anchor='end',fam='Inter')
    if lang=='zh':
        t(s,4.8,20,d['name_zh'],12.2,fg,True)
        t(s,4.8,25.1,d['name_en'],6.8,fg,fam='Inter')
    else:
        words=d['name_en']; fs=11.2
        s.wrap(4.8,18.8,words,51,fs,fg,True,leading=4.8,fam='Noto Sans CJK SC')
    B.icon(s,d['icon'],19.2,30,21.6,fg,1.75)
    s.line(4.8,54,55.2,54,fg,.22,.25)
    node_signature(s,6.2,57,47.6,int(d['id'][1:])-1,fg)
    return s

PGLYPHS={
 'X1':'<circle cx="7" cy="7" r="3"/><circle cx="17" cy="7" r="3"/><path d="M2 21v-3a5 5 0 0 1 10 0v3M12 21v-3a5 5 0 0 1 10 0v3M9.5 11.5l2.5 2 2.5-2"/>',
 'X2':'<path d="M3 8 12 3 21 8 12 13Z M3 13 12 18 21 13 M3 18 12 23 21 18 M12 13v10"/>',
 'X3':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c-5 5-5 13 0 18M12 3c5 5 5 13 0 18"/><circle cx="4" cy="8" r="2" fill="currentColor" stroke="none"/><circle cx="20" cy="16" r="2" fill="currentColor" stroke="none"/>',
 'X4':'<path d="M12 2 20 5v6c0 5-4 8-8 11-4-3-8-6-8-11V5Z M12 16l-4-4c-3-3 1-6 4-3 3-3 7 0 4 3Z"/>'
}
P_SHORT=[['人才规模','与多样性'],['技术产出','与开放供给'],['全球连接','与网络效应'],['开源善治','与公共价值']]
P_PROMISE=['让更多人参与共建','让开放成果可供接续','让知识跨越边界复用','让协作产生持久公共价值']
P_EN_SHORT=[['Talent Scale','& Diversity'],['Technical Output','& Open Supply'],['Global Connections','& Network Effects'],['Open Source Governance','& Public Value']]

def pillar_icon(s,p,x,y,size,color):
    s.e.append(f'<g transform="translate({x},{y}) scale({size/24})" fill="none" color="{color}" stroke="{color}" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round">{PGLYPHS[p]}</g>')

def pillar_tile(p,i,style='solid'):
    s=S(60,60,None,p['id']+' '+p['name_zh']);co=p['color'];fg=WHITE if style=='solid' else co
    s.rect(0,0,60,60,co if style=='solid' else '#F4F7FB',rx=1.2)
    t(s,4.8,9.5,p['id'],16,fg,True,fam='Inter')
    pillar_icon(s,p['id'],38.2,5.8,15.5,fg)
    for k,line in enumerate(P_SHORT[i]):t(s,4.8,23+k*6.4,line,15.3,fg,True)
    for k,line in enumerate(P_EN_SHORT[i]):t(s,4.8,40+k*4.5,line,8.1,fg,fam='Inter')
    t(s,4.8,54,' · '.join(p['dimensions']),7.4,fg,fam='Inter')
    for j,code in enumerate(p['dimensions']):
        d=next(v for v in D if v['id']==code);s.rect(j*60/len(p['dimensions']),58,60/len(p['dimensions']),2,d['hero_color'])
    return s

def frame(num,title,subtitle=None):
    s=S(210,297,WHITE,title)
    s.embed(AS/'master/osdgs-symbol-compact.svg',14,9.4,10,10)
    t(s,27,16.3,'OSDGs',12,NAVY,True,fam='Liberation Serif')
    t(s,195,15.7,'IDENTITY SYSTEM  /  REVIEW 0.1',7,MUTED,anchor='end',fam='Inter')
    s.line(15,22,195,22,LINE,.28)
    if title:t(s,15,35,title,19,NAVY,True)
    if subtitle:t(s,15,43,subtitle,8.6,MUTED)
    t(s,15,287,'开源发展目标 · 动态星座配套标识',7.1,MUTED)
    t(s,195,287,f'{num:02d}',8,NAVY,True,'end',fam='Inter')
    for i,d in enumerate(D):s.rect(15+i*18,292,16.6,.8,d['hero_color'])
    return s

def embed_tile(s,d,x,y,size=34.6,style='solid',lang='zh'):
    s.embed(AS/f'dimensions/{d["id"]}-{lang}-{style}-outlined.svg',x,y,size,size)

def pill(s,x,y,label,co,w=None):
    w=w or B.width(label,7.3,True)+5
    s.rect(x,y,w,6,B.tint(co,.92),rx=1.1);t(s,x+2.5,y+4.25,label,7.3,co,True)
    return w

def page1():
    s=frame(1,'')
    s.embed(AS/'master/osdgs-display-light-outlined.svg',9,31,80,80)
    t(s,91,54,'开源发展目标',26,NAVY,True)
    t(s,92,65,'OPEN SOURCE',11.6,NAVY,True,fam='Inter')
    t(s,92,72,'DEVELOPMENT GOALS',11.6,NAVY,True,fam='Inter')
    t(s,92,85,'四支柱 · 十个观察方向',10.1,MUTED)
    t(s,15,114,'让开放资源转化为可持续公共能力',17.4,NAVY,True)
    t(s,15,122.2,'From open resources to sustainable public capability',8.9,MUTED,fam='Inter')
    for i,d in enumerate(D):embed_tile(s,d,15+(i%5)*36.6,134+(i//5)*37.6,33.6)
    for i,p in enumerate(P):
        x=15+i*46.1;s.rect(x,218,41.7,1,p['color']);t(s,x,225,p['id'],8.7,p['color'],True,fam='Inter')
        for j,ln in enumerate(P_SHORT[i]):t(s,x,231.5+4.9*j,ln,9.7,NAVY,True)
    t(s,105,259,'参与 · 供给 · 复用 · 治理 · 公共价值',11.6,NAVY,True,'middle')
    t(s,105,270,'目标组织方向，证据检验成效。',9,MUTED,anchor='middle')
    return s

def page2():
    s=frame(2,'四支柱统领十维','沿用既有层级与命名，形成可独立使用、也可组合呈现的标识家族。')
    ys=[54,109,164,219]
    for i,(p,y) in enumerate(zip(P,ys)):
        s.embed(AS/f'pillars/{p["id"]}-solid-outlined.svg',15,y,43,43)
        dims=[d for d in D if d['pillar']==p['id']]
        for j,d in enumerate(dims):embed_tile(s,d,66+j*43,y,40,style='light')
        if len(dims)==2:
            s.line(157,y+7,157,y+34,p['color'],.6)
            lines=['让更多人','参与共建'] if i==0 else ['让协作产生','持久公共价值']
            for k,line in enumerate(lines):t(s,162,y+14+k*6,line,10.1,p['color'],True)
        else:t(s,66,y+47,P_PROMISE[i],8.8,p['color'])
    return s

ICON_NOTES=[
 '参与者构成群体，观察人才的规模与空间分布。',
 '多个节点共同连接，观察不同来源的参与结构。',
 '代码括号代表可继续协作与维护的代码成果。',
 '组合模块代表可获取、适配与接续开发的模型资源。',
 '分层数据容器代表支撑研究与再创造的数据资源。',
 '分叉连接代表代码协作关系中的传播与网络影响。',
 '中心与轨道代表模型的派生、传播与采用关系。',
 '分发节点代表数据集被采用、连接与继续复用。',
 '盾与确认符号代表规则、责任与维护机制。',
 '托举与心形代表共同受益；具体成效仍须验证。']

def page3():
    s=frame(3,'让图形承载清晰含义','十维图形沿用已批准的语义；新增方形构图、节点导视和统一尺度。')
    for i,d in enumerate(D):
        x=15+(i%2)*93;y=53+(i//2)*44
        s.rect(x,y,17,17,B.tint(d['color'],.93),rx=3)
        B.icon(s,d['icon'],x+3,y+3,11,d['color'],1.75)
        t(s,x+22,y+4.8,d['id']+'  '+d['name_zh'],10,d['color'],True)
        t(s,x+22,y+10.7,d['name_en'],6.6,MUTED,fam='Inter')
        s.wrap(x,y+24.2,ICON_NOTES[i],84.5,9.1,NAVY,leading=4.6)
        s.line(x,y+38.5,x+84.5,y+38.5,LINE,.2)
    t(s,15,276,'编号、名称与图形共同识别；颜色只承担辅助导视。',8.5,MUTED)
    return s

def page4():
    s=frame(4,'一套母型，多种使用尺度','主标采用原版矢量；新增组件提供实底、浅底、中英文及单色用法。')
    t(s,15,53,'浅底 / 标准组合',8.6,MUTED)
    s.embed(AS/'master/osdgs-horizontal-light-outlined.svg',22,56,165,50)
    s.rect(15,115,180,61,NIGHT,rx=2)
    t(s,21,123,'DARK / STANDARD LOCKUP',7.4,'#BED3EC',fam='Inter')
    s.embed(AS/'master/osdgs-horizontal-dark-outlined.svg',27,125,153,46.36)
    t(s,15,188,'01  英文方形',8.8,NAVY,True)
    t(s,77,188,'02  单色图形',8.8,NAVY,True)
    t(s,139,188,'03  小尺寸导视',8.8,NAVY,True)
    embed_tile(s,D[3],15,194,45,lang='en')
    for i in range(4):B.icon(s,D[i+6]['icon'],77+(i%2)*24,198+(i//2)*23,16,NAVY,1.7)
    for i in range(4):
        y=195+i*10.2;pill(s,139,y,D[i]['id'],D[i]['color'],15)
        t(s,158,y+4.5,D[i]['name_zh'],7.5,NAVY)
    s.line(15,248,195,248,LINE,.25)
    s.wrap(15,257,'方形图标建议印刷宽度 ≥ 32 mm；再小则使用简化图形配文字。主标按现行规范保留至少 10% 净空。',177,9.2,NAVY,leading=5.3)
    s.wrap(15,271,'实底使用固定阅读色；高亮色只用于节点和辅助装饰。',177,8.4,MUTED,leading=4.6)
    return s

NARR=[
 ('参与','PARTICIPATION','让更多人能够进入并持续参与开放协作。',['D01','D02','D09']),
 ('供给','SUPPLY','让代码、模型与数据成为可以接续的开放资源。',['D03','D04','D05']),
 ('复用','REUSE','让已有成果跨越组织与地区，支持适配和再创造。',['D06','D07','D08','D09']),
 ('治理','GOVERNANCE','让许可、责任与长期维护支撑持续协作。',['D09','D10']),
 ('公共价值','PUBLIC VALUE','检验成本、本地化、维护与实际结果，关注共同受益。',['D09','D10'])]

def page5():
    s=frame(5,'用五段主线讲清价值路径','主线组织叙事，四支柱与十维组织观察；两者相互联系。')
    for i,(cn,en,claim,ids) in enumerate(NARR):
        y=53+i*41;co=[D[0]['color'],D[2]['color'],D[6]['color'],D[8]['color'],D[9]['color']][i]
        s.rect(15,y,180,35,'#F5F8FC',rx=1.5);s.rect(15,y,1.5,35,co)
        t(s,21,y+11,cn,15,co,True)
        t(s,21,y+19,en,6.5,MUTED,True,fam='Inter')
        s.wrap(65,y+10,claim,122,10.1,NAVY,leading=5.7)
        x=65
        for code in ids:
            d=next(d for d in D if d['id']==code)
            x+=pill(s,x,y+23,code,d['color'],18)+3
    s.wrap(15,266,'上列编号表示相关观察入口，不是指标等价关系，也不证明资源已经转化为公共成效。五段用语作为传播与编辑层，不增加一级目标。',177,8.2,MUTED,leading=4.8)
    return s

def page6():
    s=frame(6,'从标识总览走向实际应用','报告、演示与网页共用矢量资产；本次先评审，不替换已批准母版。')
    # Report application specimen.
    s.rect(15,51,85,76,'#F7F9FC',LINE,.25,1.5)
    s.embed(AS/'master/osdgs-symbol-compact.svg',21,57,9,9)
    t(s,33,63,'GOSD 2026',8.9,NAVY,True)
    t(s,21,78,'全球开源生态观测',13,NAVY,True)
    t(s,21,88,'参与结构 · 开放供给 · 跨境连接',7.4,MUTED)
    x=21
    for d in [D[0],D[3],D[6]]:
        B.icon(s,d['icon'],x,98,9,d['color'],1.7);t(s,x,117,d['id'],7.5,d['color'],True);x+=24
    # Event / dark screen application.
    s.rect(106,51,89,76,NIGHT,rx=1.5)
    s.embed(AS/'master/osdgs-display-dark-outlined.svg',155,56,38,38)
    t(s,112,65,'OPEN SOURCE',8.7,WHITE,True,fam='Inter')
    t(s,112,72,'FOR PUBLIC VALUE',8.3,WHITE,True,fam='Inter')
    t(s,112,104,'共同创造 · 持续维护',11,WHITE,True)
    t(s,112,113,'让开放资源服务共同发展',8.7,'#C0D7EF')
    t(s,15,137,'交付内容',12.6,NAVY,True)
    s.wrap(15,145,'四支柱标识、十维方形色块、中英文版本、透明图形、深浅底组合、全套矢量源与预览图。文字轮廓版可跨设备使用，编辑版保留名称与编号。',180,9.2,NAVY,leading=5.2)
    t(s,15,170,'本次评审重点',12.6,NAVY,True)
    for i,tx in enumerate(['方形图标是否比旧版更醒目，且能快速辨认？','四支柱与十维的层级是否清楚，整体气质是否协调？','五段主线的传播表述是否准确体现报告价值？']):
        t(s,17,179+7*i,str(i+1).zfill(2),8.6,D[i*3]['color'],True,fam='Inter');t(s,27,179+7*i,tx,9.1,NAVY)
    s.line(15,201,195,201,LINE,.25)
    t(s,15,211,'版本与依据',11,NAVY,True)
    s.wrap(15,219,'配套标识 v0.1 · 2026-11-12。依据 OSDGs v2.0.0 视觉基线、报告宪法 v0.3、精要版宪法补充 v1.0 与四大洞察主张地图。',180,8.2,NAVY,leading=4.6)
    t(s,15,229,'仓库核对版本：e3aaab8（2026-11-12）。',8.2,NAVY)
    s.wrap(15,237,'参考 SDG 的编号、图形与色块识别方法；本套为 OSDGs 配套设计。十维沿用 Lucide 图形并保留许可；四支柱辅助图形为本次新增。完整来源与可编辑资产见附带资源包。',180,8.2,MUTED,leading=4.6)
    s.wrap(15,255,'待确认：新增四支柱图形、方形构图及五段传播表述。正式发布前复核最小尺寸、印刷色彩与中英文用语。本套不使用联合国徽记或 SDG 色轮。',180,8.2,MUTED,leading=4.6)
    return s

def main():
    AS.mkdir(exist_ok=True);PAGES.mkdir(exist_ok=True)
    (AS/'master').mkdir(exist_ok=True)
    masters=['master/osdgs-display-light-outlined.svg','master/osdgs-display-dark-outlined.svg','master/osdgs-symbol-compact.svg','lockups/osdgs-horizontal-light-outlined.svg','lockups/osdgs-horizontal-dark-outlined.svg','master/osdgs-emblem-mono-outlined.svg','master/osdgs-emblem-reverse-outlined.svg']
    fingerprints=[]
    for p in masters:
        src=BASE/'assets'/p;dst=AS/'master'/src.name;shutil.copy2(src,dst)
        fingerprints.append({'source':p,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'copy_identical':src.read_bytes()==dst.read_bytes()})
    for d in D:
        for sty in ['solid','light']:
            for lang in ['zh','en']:save(tile(d,sty,lang),AS/f'dimensions/{d["id"]}-{lang}-{sty}',png=900)
        for mode,col in [('color',d['color']),('navy',NAVY),('white',WHITE)]:
            s=S(24,24,None,d['name_zh']);B.icon(s,d['icon'],1,1,22,col,1.75)
            save(s,AS/f'icons/{d["id"]}-{mode}',png=400)
    for i,p in enumerate(P):
        for sty in ['solid','light']:save(pillar_tile(p,i,sty),AS/f'pillars/{p["id"]}-{sty}',png=900)
        for mode,col in [('color',p['color']),('navy',NAVY),('white',WHITE)]:
            s=S(24,24,None,p['name_zh']);pillar_icon(s,p['id'],1,1,22,col);save(s,AS/f'icons/{p["id"]}-{mode}',png=400)
    for i,f in enumerate([page1,page2,page3,page4,page5,page6],1):save(f(),PAGES/f'page-{i:02}',png=1800,pdf=True)
    # Shareable single-page poster: full portrait overview, no extra generated artwork.
    shutil.copy2(PAGES/'page-01.png',ROOT/'OSDGs_Companion_Identity_Overview_v0.1.png')
    (ROOT/'review/qa.json').write_text(json.dumps(QA,ensure_ascii=False,indent=2))
    (ROOT/'review/master-fingerprints.json').write_text(json.dumps(fingerprints,indent=2))
    (ROOT/'source/approved_brand_tokens.json').write_text(json.dumps(B.TOK,ensure_ascii=False,indent=2))
    (ROOT/'source/narrative.json').write_text(json.dumps(NARR,ensure_ascii=False,indent=2))
    print(json.dumps({'svg_assets':len(list(AS.rglob('*.svg'))),'png_assets':len(list(AS.rglob('*.png'))),'pages':6,'overflow':sum(bool(x['out_of_bounds']) for x in QA),'master_copies_unchanged':all(x['copy_identical'] for x in fingerprints)}))

if __name__=='__main__':main()
