from pathlib import Path
import math,json,copy,xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
import cairosvg

J=Path(__file__).resolve().parents[1];O=J/'output';O.mkdir(exist_ok=True);(J/'review').mkdir(exist_ok=True)
static=J/'assets/NotoSansKR-Study.ttf'
if not static.exists():
 f=TTFont(J/'assets/NotoSansKR.ttf');instantiateVariableFont(f,{'wght':450},inplace=True);f.save(static)
FONTS={'KR':TTFont(static),'EN':TTFont(J/'assets/InstrumentSans-Regular.ttf')}
FM={k:{'cmap':f.getBestCmap(),'glyphs':f.getGlyphSet(),'upem':f['head'].unitsPerEm,'metrics':f['hmtx'].metrics} for k,f in FONTS.items()}
NS='http://www.w3.org/2000/svg';INKS='http://www.inkscape.org/namespaces/inkscape';ET.register_namespace('',NS);ET.register_namespace('inkscape',INKS)
INK='#242E31';GRAY='#647174';LIGHT='#DCE1E1';BLUE='#477CA0';GREEN='#44846C';RUST='#BC6B3F';RED='#BD5253';PALEBLUE='#E5EFF4';PALEGREEN='#E7F0E9';PALEORANGE='#F4E8DA';PT=25.4/72
def width(t,size,font='KR'):
 f=FM[font];return sum(f['metrics'][f['cmap'].get(ord(c),'.notdef')][0] for c in t)*size*PT/f['upem']
def el(p,tag,**attrs):return ET.SubElement(p,'{'+NS+'}'+tag,{k.replace('_','-'):str(v) for k,v in attrs.items() if v is not None})
class Board:
 def __init__(self,name):
  self.name=name;self.text_checks=[];self.root=ET.Element('{'+NS+'}svg',{'width':'594mm','height':'420mm','viewBox':'0 0 594 420','version':'1.1'})
  el(self.root,'title').text='Fruchter House — Expansion / Overlap / Subtraction'
  el(self.root,'desc').text='A2 landscape vector architectural study. Real dimensions unknown; all new rotation, programme and wall changes are design proposals.'
  self.g=self.root;self.rect(0,0,594,420,'#FFF',None)
  defs=el(self.root,'defs')
  for name,color,mode in [('blue',BLUE,'diag'),('green',GREEN,'dots'),('orange',RUST,'cross'),('gray',GRAY,'diag')]:
   p=el(defs,'pattern',id='hatch-'+name,patternUnits='userSpaceOnUse',width=2.4,height=2.4)
   if mode=='dots':el(p,'circle',cx=.7,cy=.7,r=.17,fill=color)
   else:
    el(p,'path',d='M -1,1 L 1,-1 M 0,2.4 L 2.4,0 M 1.4,3.4 L 3.4,1.4',fill='none',stroke=color,stroke_width=.1)
    if mode=='cross':el(p,'path',d='M 0,0 L 2.4,2.4',fill='none',stroke=color,stroke_width=.1)
 def layer(self,name):
  self.g=el(self.root,'g',id=name);self.g.set('{'+INKS+'}groupmode','layer');self.g.set('{'+INKS+'}label',name)
 def path(self,pts,fill=None,stroke=INK,lw=.2,dash=None,closed=True):
  return el(self.g,'path',d='M '+' L '.join(f'{x:.5f},{y:.5f}' for x,y in pts)+(' Z' if closed else ''),fill=fill or 'none',stroke=stroke or 'none',stroke_width=lw,stroke_linejoin='miter',stroke_dasharray=' '.join(map(str,dash)) if dash else None)
 def shape(self,outer,holes=None,fill=None,stroke=INK,lw=.2):
  a=''
  for ps in [outer]+(holes or []):a+='M '+' L '.join(f'{x:.5f},{y:.5f}' for x,y in ps)+' Z '
  return el(self.g,'path',d=a,fill=fill or 'none',stroke=stroke or 'none',stroke_width=lw,fill_rule='evenodd')
 def line(self,a,b,color=INK,lw=.2,dash=None):return self.path([a,b],None,color,lw,dash,False)
 def rect(self,x,y,w,h,fill=None,stroke=INK,lw=.2):return self.path([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],fill,stroke,lw)
 def circle(self,x,y,r,fill=None,stroke=INK,lw=.2):return el(self.g,'circle',cx=x,cy=y,r=r,fill=fill or 'none',stroke=stroke or 'none',stroke_width=lw)
 def text(self,x,y,t,size=8,font='KR',color=INK,anchor='start'):
  p=el(self.g,'text',x=x,y=y,fill=color,font_size=size*PT,font_family='Noto Sans KR' if font=='KR' else 'Instrument Sans',font_weight='450' if font=='KR' else '400',text_anchor=anchor,data_font=font);p.text=t
  tw=width(t,size,font);left=x-tw*(1 if anchor=='end' else .5 if anchor=='middle' else 0);self.text_checks.append({'text':t,'left':left,'right':left+tw,'baseline':y,'size':size})
 def wrap(self,x,y,text,maxw,size=8,leading=4,color=GRAY,font='KR'):
  line='';rows=[]
  for c in text:
   if c=='\n':rows.append(line);line='';continue
   if line and width(line+c,size,font)>maxw:
    pos=line.rfind(' ')
    if pos>len(line)*.35:rows.append(line[:pos]);line=line[pos+1:]+c
    else:rows.append(line);line=c
   else:line+=c
  if line:rows.append(line)
  for i,r in enumerate(rows):self.text(x,y+i*leading,r,size,font,color)
  return y+leading*len(rows)
 def arrow(self,pts,color=RUST,lw=.3,head=1.4,dash=None):
  self.path(pts,None,color,lw,dash,False);a,b=pts[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]);self.path([b,(b[0]-head*math.cos(ang-.42),b[1]-head*math.sin(ang-.42)),(b[0]-head*math.cos(ang+.42),b[1]-head*math.sin(ang+.42))],color,None)
 def cross(self,x,y,r=1.2,color=GRAY,lw=.18):self.line((x-r,y),(x+r,y),color,lw);self.line((x,y-r),(x,y+r),color,lw)
 def save(self):
  ET.ElementTree(self.root).write(O/(self.name+'.svg'),encoding='utf-8',xml_declaration=True)
  outline=copy.deepcopy(self.root)
  for parent in list(outline.iter()):
   for node in list(parent):
    if node.tag!='{'+NS+'}text':continue
    txt=node.text or '';fm=FM[node.get('data-font','KR')];size=float(node.get('font-size'));x=float(node.get('x'));y=float(node.get('y'));a=node.get('text-anchor');adv=sum(fm['metrics'][fm['cmap'].get(ord(c),'.notdef')][0] for c in txt);sc=size/fm['upem'];x-=adv*sc*(1 if a=='end' else .5 if a=='middle' else 0)
    g=ET.Element('{'+NS+'}g',{'aria-label':txt,'data-original-text':txt,'fill':node.get('fill',INK)});offset=0
    for c in txt:
     gn=fm['cmap'].get(ord(c),'.notdef');pen=SVGPathPen(fm['glyphs']);fm['glyphs'][gn].draw(pen)
     if pen.getCommands():el(g,'path',d=pen.getCommands(),transform=f'translate({x+offset*sc:.6f} {y:.6f}) scale({sc:.8f} {-sc:.8f})')
     offset+=fm['metrics'][gn][0]
    i=list(parent).index(node);parent.remove(node);parent.insert(i,g)
  p=O/(self.name+'_outlined.svg');ET.ElementTree(outline).write(p,encoding='utf-8',xml_declaration=True)
  cairosvg.svg2pdf(url=str(p),write_to=str(O/(self.name+'.pdf')))
  cairosvg.svg2png(url=str(p),write_to=str(O/(self.name+'.png')),output_width=2800,output_height=1980)
  bad=[a for a in self.text_checks if a['left']<0 or a['right']>594 or a['baseline']>420];assert not bad,bad
  (J/'review'/(self.name+'-text-bounds.json')).write_text(json.dumps(self.text_checks,ensure_ascii=False,indent=2));print(self.name,'exported')
def Tmap(x,y,s):return lambda p:(x+(p[0]+80)*s,y+(p[1]+60)*s)
def label(d,p,t,size=7,color=INK):
 d.circle(*p,max(1.7,width(t,size,'EN')*.57),'#FFF',color,.14);d.text(p[0],p[1]+.75,t,size,'EN',color,'middle')
def header(d,title,subtitle,tag):
 d.layer('00_Header');d.text(18,17,'FRUCHTER HOUSE 1951 / LOUIS I. KAHN / SPATIAL RECONSTRUCTION',8.5,'EN',GRAY)
 d.text(18,32,title,29,'EN');d.text(18,45,subtitle,12.2)
 d.text(576,21,tag,9.5,'EN',RUST,'end');d.text(576,34,'A2 LANDSCAPE / 594 × 420 mm',8,'EN',GRAY,'end');d.line((18,54),(576,54),INK,.3)
def footer(d,t):
 d.layer('99_Footer');d.line((18,408),(576,408),LIGHT,.18);d.text(18,415,t,7.1,'KR',GRAY);d.text(576,415,'NTS / DESIGN PROPOSAL',7.1,'EN',GRAY,'end')
