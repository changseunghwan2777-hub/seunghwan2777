from graphics import *
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union,polylabel
from shapely.affinity import rotate
S=json.loads((J/'design/study.json').read_text());MODELS=S['models'];M=MODELS[3];PLAN=S['plan'];SRC=json.loads((J/'source/rotation-study.json').read_text());u=S['regularisation']['source_coordinate_units_per_u']
C1='#E2E5E3';C2='#E8BD9D';C3='#A9524D';VOID='#44846C';BLUE='#477CA0'
def polygons(gs):return unary_union([Polygon(p['outer'],p.get('holes',[])) for p in gs])
def tmap(x,y,s):return lambda p:(x+p[0]*s,y-p[1]*s)
def geo(d,gs,t,fill=None,stroke=INK,lw=.23):
 for p in gs:d.shape([t(q) for q in p['outer']],[[t(q) for q in h] for h in p.get('holes',[])],fill,stroke,lw)
def wings(d,m,t,fill=C1):
 for k,g in m['regions'].items():geo(d,g,t,fill,INK,.28)
def multi(d,m,t,cut=False,labels=False):
 geo(d,m['envelope'],t,C1,INK,.32)
 for k,gs in m['double'].items():geo(d,gs,t,C2,RUST,.17)
 geo(d,m['triple'],t,'white' if cut else C3,VOID if cut else C3,.28)
 if m['natural']:geo(d,m['natural'],t,'white',VOID,.3)
 if labels:
  for k,gs in m['single'].items():
   p=polygons(gs)
   if not p.is_empty:
    if p.geom_type!='Polygon':p=max(p.geoms,key=lambda q:q.area)
    q=polylabel(p,tolerance=.001);label(d,t((q.x,q.y)),k,8)
def ghosts(d,m,t):
 for k,gs in m['regions'].items():
  for p in gs:d.path([t(q) for q in p['outer']],None,GRAY,.18,[1.2,.7])
def title(d,main,sub,tag):header(d,main,sub,tag)
def note(d,x,y,txt,w=100,size=8.3):return d.wrap(x,y,txt,w,size,4.1)
def badge(d,x,y,txt,col=RUST):d.rect(x,y-4,22,6,'#FFF',col,.3);d.text(x+11,y,txt,8,'EN',col,'middle')
def unitbar(d,x,y,s):
 d.line((x,y),(x+s,y),INK,.55)
 for p in [0,.5,1]:d.line((x+p*s,y-1),(x+p*s,y+1),INK,.18)
 d.text(x,y+4,'0',7,'EN');d.text(x+s,y+4,'1 u',7,'EN',INK,'end')
def metricline(d,x,y,txt,val):d.text(x,y,txt,7.8,color=GRAY);d.text(x+100,y,val,8.3,'EN',INK,'end')
def axes(d,m,t,s):
 if 'radius' in m:
  d.circle(*t((0,0)),m['radius']*s,None,BLUE,.17)
 for k,c in m['centres'].items():
  a=math.radians(m['angles'][k]);q1=[c[0]-.75*math.cos(a),c[1]-.75*math.sin(a)];q2=[c[0]+.75*math.cos(a),c[1]+.75*math.sin(a)]
  d.line(t(q1),t(q2),BLUE,.16,[2,.7,.4,.7]);d.cross(*t(c),.9,BLUE)
 d.cross(*t((0,0)),1,GRAY)
def graph(d,m,x,y):
 pts={'A':(x-12,y+7),'B':(x+12,y+7),'C':(x,y-10)}
 for k,v in m['pair'].items():
  if polygons(v).area>1e-6:d.line(pts[k[0]],pts[k[1]],RUST,.4)
 for k,p in pts.items():label(d,p,k,7)
 if m['metrics']['triple']>1e-6:d.circle(x,y+1,2.4,C3,None)
def board01():
 d=Board('01_Overlap_Model_Families_A2');title(d,'OVERLAP NEEDS A RULE','다섯 배치 규칙을 비교한다. 겹침의 횟수·접점의 형태·연결 구조를 따로 읽는다.','01 / MODEL FAMILIES')
 # Source and the explicit regularisation decision.
 d.text(18,67,'01  원형의 관계',10.5);raw=SRC['original']['regions'];allpts=[p for k in 'ABC' for p in raw[k]];cx=sum(p[0] for p in allpts)/len(allpts);cy=sum(p[1] for p in allpts)/len(allpts)
 st=lambda p:(55+(p[0]-cx)/u*16,97+(p[1]-cy)/u*16)
 for k in 'ABC':d.path([st(p) for p in raw[k]],C1,INK,.2)
 d.path([st(p) for p in raw['D']],'#ECD8CC',None);d.text(93,80,'서로 다른 방향의 세 공간군',10);note(d,93,89,'독립된 세 군과 그 접합 관계를 유지한다. 원래 외곽을 그대로 회전한 복원도는 아니다.',128)
 d.arrow([(229,94),(247,94)],GRAY,.25,1.8)
 d.text(261,67,'02  공통 모듈로 정규화',10.5)
 for i,k in enumerate('ABC'):
  x=265+i*44;d.rect(x,79,31.25,20,C1,INK,.3);d.text(x+15.625,92,k,10,'EN',INK,'middle')
 d.text(261,109,'1.25 u × 0.80 u × 3개',9.3);d.text(261,117,'세 모듈 면적 합 = 원도 추출 A+B+C 면적 합',8,color=GRAY)
 note(d,411,80,'각 군의 면적 변화: A −1.25%, B +2.82%, C −1.46%. 종횡비와 외곽도 조정한 설계 가설이다. 같은 모듈로 배치 규칙의 차이를 비교한다.',164,8.5)
 d.line((18,128),(576,128),LIGHT,.25)
 descriptions=[('동심 중첩','중심을 고정하고 30°씩 회전한다. 중첩의 대부분이 세 겹 영역에 몰린다.','보류: 독립 활동 영역이 크게 줄고 공유 접점이 가늘어진다.'),('교대 연쇄','중심을 0.70 u씩 이동하고 90°씩 교대한다. A–B–C의 두 접점을 만든다.','보류: 접점은 넓지만 B를 거쳐야 A와 C가 연결된다.'),('대칭 방사','세 중심을 120° 간격으로 놓고 장축을 중심에 맞춘다. 반사 대칭도 성립한다.','유지 대안: 공유 접점은 넓지만 장축이 곧바로 공통 중심을 향한다.'),('동일 위상 회전','방사 배치에서 세 군을 똑같이 15° 더 돌린다. 120° 회전 대칭이 유지된다.','우선 발전: 장축이 이웃과의 접점을 먼저 만나고, 삼중 영역을 별도로 비울 수 있다.'),('둘레 순환','세 군을 접선 방향 90°로 놓고 R=0.55 u까지 벌린다. 세 겹 중첩은 사라진다.','유지 대안: 면적 보존에 유리하고 중정이 자연 발생한다. 세 겹을 비우는 실험과는 원리가 다르다.')]
 for i,m in enumerate(MODELS):
  x=18+111*i;c=x+51;t=tmap(c,211,39)
  if i==3:d.rect(x-3,135,108,265,None,RUST,.55)
  d.text(x,144,m['id'],11,'EN',RUST);d.text(x+19,144,descriptions[i][0],11)
  d.text(x,153,m['name'],9,'EN',GRAY);multi(d,m,t);axes(d,m,t,39)
  note(d,x,267,descriptions[i][1],101,8.4)
  graph(d,m,c,303)
  met=m['metrics'];metricline(d,x,326,'세 겹 영역',f"{met['triple']:.3f} u²");metricline(d,x,336,'두 겹 접점 합',f"{met['double_total']:.3f} u²")
  metricline(d,x,346,'세 겹 비운 뒤 실내',f"{met['floor_after_triple_cut']/3*100:.1f}%")
  note(d,x,359,descriptions[i][2],101,8.4)
 d.text(18,398,'회색: 한 겹 / 흙빛: 정확히 두 겹 / 적색: 세 겹 / 녹색 외곽: 자연 발생한 빈 곳. 그래프의 중앙 점은 세 겹 중첩이다.',8,color=GRAY)
 footer(d,'u는 추출된 세 군의 평균 면적의 제곱근. 미터·실측 축척이 아님 / 모든 모델은 동일 모듈·동일 상대 축척.');d.save()
def axis_segment(m,k='A'):
 c=m['centres'][k];a=math.radians(m['angles'][k]);return [[c[0]+v*math.cos(a),c[1]+v*math.sin(a)] for v in [.625,-.625]]
def drawaxis(d,m,t):
 ps=axis_segment(m);d.arrow([t(q) for q in ps],BLUE,.35,1.4,dash=[1.8,.8]);line=LineString(ps)
 for key in ['AB','CA']:
  g=line.intersection(polygons(m['double'][key]))
  for z in getattr(g,'geoms',[g]):
   if z.geom_type=='LineString' and z.length>1e-6:d.path([t(p) for p in z.coords],None,RUST,.95,closed=False)
def board02():
 d=Board('02_Parameter_Selection_A2');title(d,'SELECT THE RELATIONSHIP','중심 반경 R과 공통 회전 위상 φ만 바꿔, 접점의 크기와 진입 관계를 확인한다.','02 / PARAMETER STUDY')
 d.text(18,68,'R = 중심에서 각 모듈 중심까지 거리 / φ = 각 모듈이 방사축에서 돌아간 각도',9,color=GRAY)
 for j,phi in enumerate([0,15,30]):d.text(80+j*112,81,f'φ = {phi}°',12,'EN',RUST if phi==15 else INK,'middle')
 for i,R in enumerate([.4,.45,.5]):
  y=127+i*88;d.text(18,y-27,f'R {R:.2f}',8.5,'EN',GRAY)
  for j,phi in enumerate([0,15,30]):
   m=S['parameter_grid'][i*3+j];x=80+j*112;t=tmap(x,y,25)
   if i==1 and j==1:d.rect(x-47,y-36,94,83,None,RUST,.6)
   multi(d,m,t,cut=True)
   d.text(x,y+35,f"V {m['metrics']['triple']:.3f}  /  J {m['metrics']['joint_areas']['AB']:.3f}",8,'EN',INK,'middle')
   d.text(x,y+42,f"d {m['metrics']['joint_diameters']['AB']:.3f}  /  F {m['metrics']['floor_after_triple_cut']/3*100:.1f}%",7.6,'EN',GRAY,'middle')
 d.text(18,355,'V: 삼중 비움 면적 / J: 한 공유 접점 면적 [u²]',8.2)
 d.text(18,363,'d: 접점 안 최대 내접원 지름 [u] / F: 원래 세 모듈 합 대비 실내 면적',8.2)
 note(d,18,376,'R을 줄이면 공통 영역과 면적 손실이 커진다. R을 늘리면 비움이 작아진다. 30° 회전에서는 공유 접점이 가늘어지는 경향을 확인했다. d는 방의 기하적 여유 지표이며 통로 유효 폭이 아니다.',332,8.3)
 d.line((369,66),(369,398),LIGHT,.25)
 d.text(386,73,'같은 R=0.45 u에서 비교',12)
 for m,x in [(MODELS[2],427),(MODELS[3],532)]:
  t=tmap(x,137,31);multi(d,m,t);drawaxis(d,m,t);d.text(x,189,f"{m['id']} / φ {m['phase']}°",9,'EN',INK,'middle')
 note(d,386,204,'청색 점선은 장축 방향의 분석선이다. 보행 동선이 아니다. 굵은 흙빛 구간은 장축이 두 겹 접점을 통과하는 길이다.',188,8.2)
 rows=[('지표','0°','15°'),('장축의 두 겹 통과','0.000 u','0.081 u'),('공유 접점 내접원','0.266 u','0.252 u'),('삼중 비움 면적','0.159 u²','0.183 u²'),('남는 실내 비율','71.5%','71.8%')]
 for i,row in enumerate(rows):
  yy=237+i*11
  if i==0:d.rect(386,yy-6,189,9,'#F1F3F2',None)
  for xx,txt in zip([388,484,533],row):d.text(xx,yy,txt,8.2)
  d.line((386,yy+3),(575,yy+3),LIGHT,.13)
 d.text(386,301,'선정: M4 / R 0.45 u / φ 15°',11,color=RUST)
 note(d,386,311,'같은 규칙을 반복하면서도 진입 축이 두 공간군의 공유 접점을 먼저 만난다. 삼중 영역은 하늘에 열고, 두 겹 접점은 방으로 남기는 위계가 읽힌다.',188,8.8)
 note(d,386,338,'M3보다 접점은 작다. 방향성의 변화와 교환한 선택이다. M5는 실내 보존율이 92.3%로 높지만 공유 접점과 중정이 더 작다. 면적 보존이 우선이면 M5를 검토한다.',188,8.5)
 note(d,386,370,'선정은 성능 최적화 결과가 아니다. 실제 규모·가구·피난 조건이 정해지면 더 넓은 접점을 가진 M3를 다시 검토할 수 있다.',188,8.1)
 footer(d,'회전·배치의 규칙성을 먼저 확인한 뒤 용도를 부여한다. 수치는 도형 계산이며 사용 성능을 대신하지 않는다.');d.save()
def drawplan(d,t,s,labels=True,flow=True):
 for room in PLAN['rooms']:geo(d,room['geometry'],t,room['color'],None)
 geo(d,PLAN['court'],t,'white',VOID,.3)
 for pair,gs in M['double'].items():geo(d,gs,t,'url(#hatch-orange)',None)
 for w in PLAN['walls']:
  a,b=t(w['a']),t(w['b'])
  if w['kind']=='glazing':
   ll=math.dist(a,b);nx=-(b[1]-a[1])/ll*.25;ny=(b[0]-a[0])/ll*.25
   for sign in [-1,1]:d.line((a[0]+sign*nx,a[1]+sign*ny),(b[0]+sign*nx,b[1]+sign*ny),BLUE,.16)
  else:d.line(a,b,INK,.8 if w['kind']=='wall' else .4)
 for door in PLAN['doors']:
  a,b=t(door['a']),t(door['b']);d.line(a,b,GRAY,.15,[.5,.5])
  if door['kind']=='sliding':
   dx,dy=b[0]-a[0],b[1]-a[1];L=math.hypot(dx,dy);nx=-dy/L*.55;ny=dx/L*.55
   d.line((a[0]+nx,a[1]+ny),(a[0]+dx*.55+nx,a[1]+dy*.55+ny),INK,.24)
   d.line((b[0]-nx,b[1]-ny),(b[0]-dx*.55-nx,b[1]-dy*.55-ny),INK,.24)
  elif door['kind']=='external':
   dx,dy=b[0]-a[0],b[1]-a[1];L=math.hypot(dx,dy);angle=math.atan2(dy,dx);d.line(a,(a[0]-dy,a[1]+dx),INK,.2)
   arc=[(a[0]+L*math.cos(angle+i*math.pi/24),a[1]+L*math.sin(angle+i*math.pi/24)) for i in range(13)];d.path(arc,None,GRAY,.14,[.7,.5],False)
 for f in PLAN['furniture']:
  geo(d,f['geometry'],t,'#FFF',INK,.22);ps=f['geometry'][0]['outer']
  if f['kind']=='table':
   for i in [0,2]:p=[(ps[i][j]+ps[(i+1)%4][j])/2 for j in [0,1]];d.circle(*t(p),s*.017,'#FFF',GRAY,.12)
  else:
   for z in [.25,.5,.75]:p=[ps[0][i]*(1-z)+ps[1][i]*z for i in [0,1]];q=[ps[3][i]*(1-z)+ps[2][i]*z for i in [0,1]];d.line(t(p),t(q),GRAY,.13)
 if flow:
  for name,ps in PLAN['routes'].items():d.path([t(p) for p in ps],None,RUST,.25,[1.5,.8],False)
  ps=PLAN['routes']['entry-B'];c=M['centres']['B'];ang=math.radians(M['angles']['B']);p=PLAN['entries']['B'];outside=[p[0]+.23*math.cos(ang),p[1]+.23*math.sin(ang)];d.arrow([t(outside),t(p),t(ps[1])],INK,.5,2)
 if labels:
  for k,p in PLAN['single_centres'].items():label(d,t([p[0],p[1]+.06]),k,10)
  for pair,p in PLAN['joint_centres'].items():label(d,t([p[0],p[1]+.025]),pair,8,RUST)
  label(d,t((0,0)),'V',11,VOID)
 # Small planting mark entirely inside the actual triple void.
 court=polygons(PLAN['court']);p=polylabel(court,tolerance=.001)
 d.circle(*t((p.x,p.y-.055)),.045*s,None,VOID,.16)
def board03():
 d=Board('04_Overlap_Development_A2');title(d,'ONE / TWO / THREE','한 겹은 독립 활동, 두 겹은 공유 접점, 세 겹은 하늘에 열린 비움으로 발전시킨다.','04 / DEVELOPMENT LOGIC')
 titles=['120° 배치','동일한 15° 회전','겹침 횟수 분리','세 겹만 비움','두 겹을 방으로','경계·문턱 구체화']
 desc=['세 중심은 반경 0.45 u 위에 둔다. 각 군을 따로 임의 이동하지 않는다.','각 중심을 축으로 같은 각도를 더한다. 세 군의 회전 대칭이 유지된다.','한 겹·두 겹·세 겹을 배타적으로 나눠 면적과 관계를 읽는다.','V=A∩B∩C. 새 중앙 다각형을 그리거나 등폭으로 깎지 않는다.','AB·BC·CA를 실내로 남긴다. 겹침은 통로를 넘어 함께 쓰는 방이다.','공유 접점마다 두 문턱을 둔다. 조용한 A는 미닫이 경계로 조절한다.']
 for i in range(6):
  x=18+i*94;c=x+42;t=tmap(c,125,29)
  d.text(x,69,f'0{i+1}',10,'EN',RUST);d.text(x,79,titles[i],10.2)
  if i==0:
   d.circle(*t((0,0)),.45*29,None,BLUE,.3)
   for k,p in M['centres'].items():d.line(t((0,0)),t(p),BLUE,.2);label(d,t(p),k,8)
   d.text(c,157,'120° / 120° / 120°',8,'EN',BLUE,'middle')
  elif i==1:
   wings(d,M,t);ghosts(d,MODELS[2],t)
   for k,p in M['centres'].items():
    a=math.radians(M['angles'][k]);pts=[[p[0]+.42*math.cos(a+math.radians(v)),p[1]+.42*math.sin(a+math.radians(v))] for v in range(-15,1,2)];d.arrow([t(q) for q in pts],RUST,.4,1.3)
  elif i==2:multi(d,M,t)
  elif i==3:multi(d,M,t,cut=True);label(d,t((0,0)),'V',9,VOID)
  elif i==4:
   multi(d,M,t,cut=True)
   for k,p in PLAN['joint_centres'].items():label(d,t(p),k,6.5,RUST)
  else:drawplan(d,t,29,False,False)
  note(d,x,180,desc[i],86,8.2)
  if i<5:d.arrow([(x+86,128),(x+92,128)],GRAY,.2,1.3)
 d.line((18,215),(576,215),LIGHT,.25)
 d.text(18,229,'기하는 반복되고, 사용하는 관계가 달라진다',13)
 d.text(576,229,'THREE CONGRUENT JOINTS / THREE SOCIAL RELATIONS',8,'EN',GRAY,'end')
 names={'AB':('자료 함께 읽기','열람과 열린 서가 사이. 자료를 비교하고 대화를 시작하는 접점.'),'BC':('작업·전시 공유','서가와 작업 공간 사이. 만든 결과와 관련 자료가 함께 놓이는 접점.'),'CA':('작은 토론·피드백','작업과 조용한 학습 사이. 검토·질문 후 각 활동으로 돌아가는 접점.')}
 for i,pair in enumerate(['AB','BC','CA']):
  x=18+i*188;centre=PLAN['joint_centres'][pair];t=lambda p,xx=x,cc=centre:(xx+82+(p[0]-cc[0])*150,288-(p[1]-cc[1])*150)
  d.layer('Joint_'+pair);clipid='clip-'+pair;cl=el(d.root,'clipPath',id=clipid);el(cl,'rect',x=x,y=240,width=173,height=94);g=el(d.g,'g',clip_path=f'url(#{clipid})');saved=d.g;d.g=g
  drawplan(d,t,150,False,True);d.g=saved
  d.text(x,346,pair+' / '+names[pair][0],11);note(d,x,355,names[pair][1],173,8.7)
  d.text(x,376,'같은 0.099 u² / 내접원 지름 약 0.252 u',8.2,color=GRAY)
 note(d,18,392,'세 접점은 120° 회전으로 서로 일치한다. 형태가 다른 방 세 개라는 주장이 아니라, 동일한 기하를 서로 다른 인접 활동에 연결한 것이다.',552,8.3)
 footer(d,'원형의 세 독립 공간군과 연결 원리를 계승한다. 공통 모듈 정규화·회전·용도·새 경계는 모두 설계 가설.');d.save()
def axon(d,m,x,y,s,h=.55):
 # Diagrammatic equal-height extrusion; roof and court follow actual boolean geometry.
 proj=lambda p,z:(x+(p[0]-p[1])*.866*s,y+(p[0]+p[1])*.5*s-z*s)
 polygons_data=m['floor']
 quads=[]
 for g in polygons_data:
  for ring in [g['outer']]+g.get('holes',[]):
   for a,b in zip(ring,ring[1:]+ring[:1]):quads.append(((a[0]+a[1]+b[0]+b[1])/2,[proj(a,0),proj(b,0),proj(b,h),proj(a,h)]))
 for _,pts in sorted(quads,key=lambda z:z[0]):d.path(pts,'#E3E7E4',GRAY,.18)
 for g in polygons_data:d.shape([proj(p,h) for p in g['outer']],[[proj(p,h) for p in ring] for ring in g.get('holes',[])],'#F2F3F0',INK,.27)
 for k,gs in m['regions'].items():
  for g in gs:d.path([proj(p,h+.002) for p in g['outer']],None,GRAY,.15,[1,.65])
 for k,gs in m['double'].items():
  for g in gs:d.path([proj(p,h+.003) for p in g['outer']],C2,RUST,.15)
 for g in m['triple']:d.path([proj(p,h+.004) for p in g['outer']],None,VOID,.35)
def board04():
 d=Board('05_Selected_Model_Plan_A2');title(d,'THREE JOINTS / ONE OPEN SKY','M4 우선 발전안 — 공공 학습·자료·작업 공간을 연결하는 세 공유 접점과 하나의 중정','05 / SELECTED DEVELOPMENT')
 t=tmap(177,214,110);d.layer('Plan');drawplan(d,t,110)
 d.text(18,70,'평면 / 벽·개구부·가구 배치 가설',11)
 d.line(t((-1.17,0)),t((1.12,0)),GRAY,.2,[3,1,.5,1]);d.text(*t((-1.23,0)),'s1',8,'EN');d.text(*t((1.15,0)),'s2',8,'EN')
 # Source footprint interpretation is tested, not silently equated with the prototype.
 d.text(18,357,'A 조용한 열람   B 열린 서가·대화   C 자료 작업·배움',9.2)
 d.text(18,367,'AB 함께 읽기   BC 작업·전시   CA 토론·피드백   V 비움',9.2)
 d.text(18,379,'실선 화살표: 주진입 / 흙빛 점선: 연결 가능한 경로 / A 문턱: 미닫이 제안',7.9,color=GRAY)
 unitbar(d,18,393,55);d.text(88,394,'주평면 1 u = 110 mm / 축척은 상대 단위',8,color=GRAY)
 d.line((340,66),(340,398),LIGHT,.25)
 d.text(357,72,'동일 높이로 본 중첩·비움 모델',12)
 axon(d,M,466,159,57)
 d.text(357,219,'지붕 위 점선: 원래 모듈 경계 / 흙빛: 두 겹 접점',8,color=GRAY)
 d.text(357,227,'높이 h=0.55 u는 입체 관계를 보기 위한 가설이다.',8,color=GRAY)
 # Exact horizontal section across the selected union and triple void.
 env=polygons(M['envelope']);court=polygons(M['triple']);line=LineString([(-2,0),(2,0)]);e=env.intersection(line);v=court.intersection(line);a,b=sorted([p[0] for p in e.coords]);c,f=sorted([p[0] for p in v.coords]);xx=lambda z:357+(z-a)/(b-a)*211;roof=251;base=283
 for p,q in [(a,c),(f,b)]:d.rect(xx(p),roof,xx(q)-xx(p),1.2,INK,None)
 d.line((357,base),(568,base),INK,.6)
 for q in [a,b]:d.line((xx(q),roof),(xx(q),base),INK,.55)
 for q in [c,f]:d.line((xx(q),roof),(xx(q),base),BLUE,.2)
 for frac in [.25,.5,.75]:z=c+(f-c)*frac;d.arrow([(xx(z),241),(xx(z),277)],VOID,.24,1.3)
 d.text(357,295,'s1–s2 / 평면의 실제 교차 경계로 구성한 개념 단면',8.7)
 d.text(357,303,'비움에는 지붕을 두지 않는다. 구조·배수·관리 출입은 후속 검토.',7.7,color=GRAY)
 d.text(357,320,'선택과 남은 과제',11)
 note(d,357,329,'실내는 2.154 u², 세 모듈 합의 71.8%가 남는다. 중정은 0.183 u², 공유 접점은 각 0.099 u²다. 겹침으로 생긴 중복 면적과 비움을 모두 반영했다.',217,8.7)
 note(d,357,352,'원래 외곽을 같은 규칙에 다시 놓아도 세 접점과 공통 영역은 생긴다. 다만 정확한 120° 대칭은 사라진다. 현재안의 정규화는 의도적인 설계 선택이다.',217,8.5)
 note(d,357,376,'동선 중심선·벽·가구 충돌은 확인했다. 유효 폭·피난·위생·실측 규모가 정해지기 전의 평면 연구이며 완성된 시설 설계가 아니다.',217,8.1)
 footer(d,'기하적 규칙성은 배치·중첩에서 검증. 활동과 경계는 그 규칙 위에 제안. 대지 방위·절대 치수·구조 성능 미확인.');d.save()

def board_policy():
 d=Board('03_Void_Policy_And_Lineage_A2');title(d,'WHAT SHOULD BE EMPTIED?','같은 중첩 모델에서도 삭제 규칙에 따라 중심·접점·연결이 달라진다.','03 / VOID POLICY')
 texts=[('전부 유지','세 겹 T가 실내 중심이 된다. 공유 접점은 있지만 중앙 홀의 위계가 강해진다.'),('모든 중첩 삭제','한 겹 영역만 남는다. 세 군의 실내 연결이 끊어지므로 보류한다.'),('두 겹만 삭제','공유 접점을 없애면 중앙 T와 세 군이 분리된다. 점 접촉은 통로가 아니다.'),('세 겹만 삭제','세 군과 세 공유 접점이 연결된다. 중앙은 비우고 관계를 가장자리로 옮긴다.')]
 for i,pol in enumerate(S['void_policies']):
  x=18+i*140;t=tmap(x+63,128,43)
  if i==3:d.rect(x-3,64,137,170,None,RUST,.5)
  d.text(x,76,f"P{i} / "+texts[i][0],11)
  geo(d,pol['floor'],t,C1,INK,.3);geo(d,pol['void'],t,'white',VOID,.25)
  if i in [0,3]:
   for k,g in M['double'].items():geo(d,g,t,C2,RUST,.2)
  if i in [0,2]:geo(d,M['triple'],t,C3,None)
  d.text(x,191,f"연속 실내 영역 {pol['components']}개 / {pol['floor_area']:.3f} u²",9)
  note(d,x,202,texts[i][1],129,8.6)
 d.line((18,243),(576,243),LIGHT,.25)
 d.text(18,257,'원래 외곽에도 같은 규칙이 작동하는가?',13)
 for m,x,name in [(M,85,'공통 모듈 / 선정안'),(S['original_outline_check'],253,'원래 외곽 재적용')]:
  t=tmap(x,318,39);multi(d,m,t,cut=True);d.text(x,376,name,10,anchor='middle');d.text(x,386,f"V {m['metrics']['triple']:.3f} u² / 실내 {m['metrics']['floor_after_triple_cut']/3*100:.1f}%",8.3,anchor='middle')
 d.text(355,273,'유지되는 것과 달라지는 것',11)
 note(d,355,284,'동일한 중심·배치 반경·공통 회전 위상을 적용하면 원래 외곽에서도 세 공유 접점과 삼중 영역이 생긴다. 세 군의 관계 구조는 이어진다.',216,8.8)
 note(d,355,311,'그러나 삼중 영역은 0.183에서 0.033 u²로 약 82% 작아진다. 접점도 서로 같은 모양이 아니며 정확한 회전 대칭은 성립하지 않는다.',216,8.8)
 note(d,355,340,'따라서 정규화는 단순한 표현 정리가 아니라 공간을 바꾸는 설계 조작이다. 이번안은 세 군의 총면적과 관계 원리를 유지하면서 외곽·종횡비를 재구성한 모델이다.',216,8.8)
 note(d,355,374,'원래 외곽 보존이 우선되는 다음 단계에서는 이 재적용안을 출발점으로 반경과 비움의 규모를 다시 조정해야 한다.',216,8.2)
 footer(d,'점·선만 닿는 연결을 실제 통로로 세지 않는다. 삭제 규칙 비교는 동일한 M4에서 수행 / 원래 외곽 비교는 별도 민감도 검토.');d.save()
if __name__=='__main__':board01();board02();board_policy();board03();board04()

