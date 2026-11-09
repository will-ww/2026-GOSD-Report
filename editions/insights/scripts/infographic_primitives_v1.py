"""Compact editorial infographics: precise vectors, readable labels, restrained light."""
def text(x,y,w,t,size=9.5,leading=14,color='ink',bold=False,center=False):
    weight=r'\bfseries' if bold else ''
    align=r'\centering ' if center else ''
    return rf'\Box{{{x}}}{{{y}}}{{{w}}}{{\sffamily{weight}\fontsize{{{size}}}{{{leading}}}\selectfont\color{{{color}}}{align}{t}}}'+'\n'
def rect(x,y,w,h,c):return rf'\Rect{{{x}}}{{{y}}}{{{w}}}{{{h}}}{{{c}}}'+'\n'
def rule(x,y,z,c='line'):return rf'\Rule{{{x}}}{{{y}}}{{{z}}}{{{c}}}'+'\n'
def icon(x,y,w,name):return text(x,y,w,rf'\includegraphics[width={w}mm]{{.build/assets/{name}.pdf}}')
def curve(a,b,p,q,c='teal',width=.65,arrow=False):
    tip=r',-{Stealth[length=1.4mm]}' if arrow else ''
    return rf'\draw[{c},line width={width}pt{tip}] \Pos{{{a[0]}}}{{{a[1]}}} .. controls \Pos{{{p[0]}}}{{{p[1]}}} and \Pos{{{q[0]}}}{{{q[1]}}} .. \Pos{{{b[0]}}}{{{b[1]}}};'+'\n'
def arrow(x,y,a,b,c='muted'):return rf'\LinkLine{{{x}}}{{{y}}}{{{a}}}{{{b}}}{{{c}}}'+'\n'
def orb(x,y,r,c,asset=None):
    s=rf'\fill[{c}!5] \Pos{{{x}}}{{{y}}} circle[radius={r+1.2}mm];'+'\n'
    s+=rf'\shade[top color=white,bottom color={c}!28,shading angle=30,draw={c}!35,line width=.45pt] \Pos{{{x}}}{{{y}}} circle[radius={r}mm];'+'\n'
    s+=rf'\draw[white,line width=.7pt] \Pos{{{x-.58*r}}}{{{y-.58*r}}} arc[start angle=135,end angle=65,radius={.82*r}mm];'+'\n'
    if asset:s+=icon(x-r*.52,y-r*.52,r*1.04,asset)
    return s
def ribbon(x,y,w,h,c):
    # A sloping translucent base carries the light-stream motif without heavy frames.
    s=rf'\shade[left color={c}!10,right color={c}!2,rounded corners=2mm,draw={c}!17,line width=.45pt] \Pos{{{x}}}{{{y}}} rectangle \Pos{{{x+w}}}{{{y+h}}};'+'\n'
    s+=rf'\path[fill={c}!9] \Pos{{{x+w*.36}}}{{{y+h}}} .. controls \Pos{{{x+w*.68}}}{{{y+h-1}}} and \Pos{{{x+w*.76}}}{{{y+h-5}}} .. \Pos{{{x+w-1}}}{{{y+h-4}}} -- \Pos{{{x+w-1}}}{{{y+h-1}}} -- \Pos{{{x+w*.36}}}{{{y+h}}} -- cycle;'+'\n'
    return s
def labelnode(x,y,title,c,asset,w=40):
    s=orb(x,y,5.2,c,asset)
    return s+text(x-w/2,y+7,w,title,10,14,c,True,True)
