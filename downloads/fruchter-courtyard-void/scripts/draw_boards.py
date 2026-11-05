from graphics import *
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union
S=json.loads((J/'design/study.json').read_text());A=S['alternatives']['A'];B=S['alternatives']['B'];U=S['U'];BASE=S['original']
def geo(d,gs,t,fill=None,stroke=INK,lw=.25):
 for p in gs:d.shape([t(q) for q in p['outer']],[[t(q) for q in h] for h in p['holes']],fill,stroke,lw)
def mapper(x,y,s):return lambda p:(x+p[0]*s,y+p[1]*s)
def orig(d,t):
 for k in 'ABCDE':
  ps=BASE['regions'][k];d.path([t(p) for p in ps],{'D':'#F0D7CF','E':'#FFF'}.get(k,'#E5E6E5'),GRAY,.2,dash=[1,.6] if k=='E' else None)
  p=Polygon(ps).representative_point();label(d,t((p.x,p.y)),k,7)
 d.path([t(p) for p in BASE['hearth']],'#424746',None)
def ghosts(d,t):
 for k in 'ABC':d.path([t(p) for p in BASE['regions'][k]],None,'#ADB3B3',.16,[1.2,.8])
def wings(d,m,t,fill='#DFE2E1',ids=True):
 for k,gs in m['regions'].items():
  geo(d,gs,t,fill,INK,.27)
  if ids:
   p=Polygon(gs[0]['outer']).representative_point();label(d,t((p.x,p.y)),k,7)
def rot(d,m,t,s):
 piv=json.loads((J/'source/rotation-study.json').read_text())['pivots']
 for k in 'ABC':
  q=piv[k];dx,dy=m['translations'][k];c=[q[0]+dx,q[1]+dy];d.arrow([t(q),t(c)],BLUE,.2,1.1)
  d.cross(*t(c),.8,BLUE)
  ang=math.radians(S['angles'][k]);pts=[[c[0]+90*math.cos(a),c[1]+90*math.sin(a)] for a in [(-.65+ang*i/12) for i in range(13)]]
  d.arrow([t(p) for p in pts],RUST,.27,1.2)
  z=t([c[0]+95,c[1]-45]);d.text(*z,f"{k} {S['angles'][k]:+}°",7,'EN',RUST)
def finalmass(d,m,t):
 geo(d,m['floor'],t,'#E2E4E3',INK,.35);geo(d,m['shared'],t,'#F1D8CD',None);geo(d,m['shared'],t,'url(#hatch-orange)',None)
 geo(d,m['void'],t,'#FFF',GREEN,.35)
def bar(d,x,y,s):
 d.line((x,y),(x+U*s,y),INK,.5)
 for p in [0,U/2,U]:d.line((x+p*s,y-1),(x+p*s,y+1),INK,.2)
 d.text(x,y+4,'0',7,'EN');d.text(x+U*s,y+4,'1 U',7,'EN',INK,'end')
def item(d,x,y,n,title,body,w=100):
 d.text(x,y,n,9,'EN',RUST);d.text(x+10,y,title,10.2)
 d.wrap(x,y+7,body,w,8.2,4)
def draw01():
 d=Board('01_Expansion_Overlap_Process_A2');header(d,'EXPAND / OVERLAP / CARVE','중앙의 모양을 바꾸기보다, 마주 보는 경계와 비우는 규칙을 바꾼다.','01 / SPATIAL OPERATIONS')
 d.text(18,66,'A  벌림 → 공동 중정',12);d.text(575,66,'OUTWARD TRANSLATION / SAME ROTATION ANGLES',8,'EN',GRAY,'end')
 xs=[18+113*i for i in range(5)];scale=.108
 for i,x in enumerate(xs):
  t=mapper(x-4,77,scale);d.layer('A_Process_'+str(i))
  if i==0:orig(d,t)
  elif i==1:ghosts(d,t);wings(d,A,t);rot(d,A,t,scale)
  elif i==2:
   wings(d,A,t);geo(d,A['shared']+A['void'],t,'#F0D7CF',RUST,.25)
  elif i==3:finalmass(d,A,t)
  else:
   finalmass(d,A,t);p=Polygon(A['void'][0]['outer']);label(d,t((p.centroid.x,p.centroid.y)),'V',8,GREEN)
   for k in 'ABC':
    q=Polygon(A['regions'][k][0]['outer']).representative_point();d.arrow([t((q.x,q.y)),t((p.centroid.x,p.centroid.y))],RUST,.22,1.3)
  if i<4:d.arrow([(x+103,124),(x+110,124)],GRAY,.2,1.5)
 titles=['기존 관계 추출','방향 + 거리 조정','사잇공간의 확대','가장자리 연결','밖을 공유하는 중심']
 desc=['A·B·C의 독립 방향, D의 연결, E의 진입을 기준으로 삼는다.','A −14°, B +18°, C +10°. 바깥으로 이동시켜 마주 보는 거리를 늘린다.','서로 마주 보는 끝점을 연결한다. 잔여 틈을 공동 마당의 범위로 바꾼다.','확대한 틈의 안쪽을 비우고 둘레에 실내 연결 띠를 제안한다.','마당에 면한 세 경계가 새로운 정면이 된다. 큰 마당과 긴 이동이 함께 생긴다.']
 for i,x in enumerate(xs):item(d,x,179,f'0{i+1}',titles[i],desc[i],102)
 d.line((18,207),(576,207),LIGHT,.25)
 d.text(18,219,'B  중첩 → 선택적 비움',12);d.text(575,219,'INWARD TRANSLATION / ACTUAL FOOTPRINT INTERSECTION',8,'EN',GRAY,'end')
 for i,x in enumerate(xs):
  t=mapper(x-4,230,scale);d.layer('B_Process_'+str(i))
  if i==0:orig(d,t)
  elif i==1:ghosts(d,t);wings(d,B,t);rot(d,B,t,scale)
  elif i==2:
   wings(d,B,t,ids=False);geo(d,B['overlap'],t,'#D79A90',RED,.3);geo(d,B['overlap'],t,'url(#hatch-orange)',None)
   geo(d,B['triple_overlap'],t,'#9F514B',None)
  elif i==3:
   geo(d,B['full_subtraction'],t,'#D7DBDA',INK,.3);geo(d,B['overlap'],t,None,RED,.18)
   for j,p in enumerate(B['full_subtraction']):
    q=Polygon(p['outer']).representative_point();label(d,t((q.x,q.y)),str(j+1),7,RED)
   d.text(x+47,312,'3 SEPARATE PARTS',7,'EN',RED,'middle')
  else:finalmass(d,B,t);d.path([t(p) for p in B['loop']],None,RUST,.28,[1,.6],False)
  if i<4:d.arrow([(x+103,277),(x+110,277)],GRAY,.2,1.5)
 titles=['원형과의 관계 유지','안으로 회전·이동','중첩 면적 추출','전부 비우기: 보류','연결 띠를 남겨 비움']
 desc=['가운데에 새 다각형을 먼저 그리지 않는다. 세 공간군의 경계에서 시작한다.','벌림안과 같은 각도, 다른 이동량. 안쪽 경계가 서로 겹치도록 배치한다.','O = (A∩B) ∪ (B∩C) ∪ (C∩A). 진한 면은 세 공간군의 공통 중첩이다.','외곽에서 O 전체를 빼면 실내가 세 조각으로 분리된다. 연결 요구를 충족하지 못한다.','O의 가장자리는 실내 공유 공간으로 남긴다. 안쪽만 비워 연속된 바닥과 중정을 얻는다.']
 for i,x in enumerate(xs):item(d,x,329,f'0{i+1}',titles[i],desc[i],102)
 d.layer('Legend');d.line((18,361),(576,361),LIGHT,.2)
 legend=[('#E2E4E3','기존 공간군의 변형'),('#D79A90','실제 중첩 영역'),('#F1D8CD','실내 공유 공간'),('#FFF','중정: 하늘에 열린 비움')]
 for i,(c,txt) in enumerate(legend):d.rect(18+i*139,369,7,4,c,INK,.15);d.text(28+i*139,373,txt,8.5)
 d.wrap(18,385,'두 줄의 모든 평면은 같은 상대 축척·도면 방향이다. 회전각은 설계 가설이며, A/B는 이동량도 다른 대안 비교다. 점선은 원래 외곽 또는 순환 동선으로 각 단계에서 구분한다.',385,8.2,4)
 bar(d,479,389,scale)
 footer(d,'U = 기존 A 안쪽 변 길이. 실측 축척·방위 미확인 / 원본의 삼각형 요소는 출처 참조이며 새 용도를 확정하지 않음.');d.save()
def draw02():
 d=Board('02_Spatial_Comparison_A2');header(d,'TWO COURTS / DIFFERENT CONSEQUENCES','넓히는 중정과 겹쳐 비우는 중정은, 같은 빈 공간이지만 다른 관계를 만든다.','02 / COMPARATIVE STUDY')
 d.text(18,70,'A / EXPANDED COURT',16,'EN');d.text(306,70,'B / SELECTIVE SUBTRACTION',16,'EN')
 d.text(18,80,'바깥의 공동 마당 + 둘레의 실내 연결',10);d.text(306,80,'안쪽의 빛마당 + 연결을 유지하는 실내 띠',10)
 scale=.272;ta=mapper(18,75,scale);tb=mapper(277,75,scale)
 finalmass(d,A,ta);finalmass(d,B,tb)
 for m,t in [(A,ta),(B,tb)]:
  for k,gs in m['regions'].items():
   d.path([t(p) for p in gs[0]['outer']],None,'#929B99',.18,[1.2,.7]);q=Polygon(gs[0]['outer']).representative_point();label(d,t((q.x,q.y)),k,9)
  v=Polygon(m['void'][0]['outer']);p=v.representative_point();label(d,t((p.x,p.y)),'V',11,GREEN)
 if True:
  geo(d,B['forecourt'],tb,'#EDF0E6',GREEN,.2);geo(d,B['forecourt'],tb,'url(#hatch-green)',None)
  q=Polygon(B['forecourt'][0]['outer']).representative_point();label(d,tb((q.x,q.y)),'E',10,GREEN)
  d.path([tb(p) for p in B['loop']],None,RUST,.35,[1.2,.65],False)
  d.arrow([tb((650,620)),tb(B['external_ports']['ENTRY']),tb((515,419))],RUST,.4,1.8)
 d.text(306,282,'선정: 도서관·공유작업소의 연결된 실내를 우선',10.8,color=RUST)
 d.wrap(306,291,'독립된 방향은 남기되 경계 일부를 공유한다. 중정은 채광·시선의 중심, 실내 띠는 이동·만남의 중심이다. 외부 E는 큰 모임을 받아 안쪽 중정의 과밀을 줄인다.',260,8.6,4)
 bar(d,18,317,scale);d.text(97,318,'동일한 상대 축척 / 외곽선 기준 비교',8.2,color=GRAY)
 d.line((18,330),(576,330),INK,.25)
 rows=[('비교 항목','A  벌림','B  선택적 비움'),('실내 외곽 면적 / 원래 세 공간군 면적 합','122.4%  /  3.810 U²','63.2%  /  1.969 U²'),('하늘에 열린 안쪽 마당','1.104 U²','0.218 U²'),('실내 공유 띠 / 바닥의 연속성','0.697 U² / 연결됨','0.541 U² / 연결됨'),('얻는 것 / 치르는 비용','큰 공동 마당 / 외곽 확장·긴 이동','가까운 접점·연속 실내 / 사용 면적 감소')]
 for i,row in enumerate(rows):
  y=340+i*10
  if i==0:d.rect(18,y-6,558,9,'#F1F3F2',None)
  for x,t in zip([21,258,418],row):d.text(x,y,t,8.5 if i else 9)
  if i:d.line((18,y+3),(576,y+3),LIGHT,.13)
 d.text(18,398,'면적은 벽 두께를 공제하지 않은 도형 면적. 대지·법규·실측 면적 미확인으로 수용 인원이나 성능 우열을 확정하지 않는다.',8,color=GRAY)
 footer(d,'판단 기준: 내부 연결·조용한 열람·외부 모임의 분리. A를 폐기하지 않고 비교 대안으로 유지한다.');d.save()
def finalplan(d,t,scale,labels=True):
 geo(d,B['forecourt'],t,'#F1F3EA',GREEN,.18);geo(d,B['forecourt'],t,'url(#hatch-green)',None)
 for r in B['rooms']:geo(d,r['geometry'],t,r['color'],None)
 geo(d,B['shared'],t,'url(#hatch-orange)',None)
 geo(d,B['void'],t,'#FFF',None)
 # Court planting belongs to the void; no roof or floor fill is added.
 v=Polygon(B['void'][0]['outer']);
 for x,y,r in [(416,288,12),(407,330,9),(333,367,6)]:
  if v.covers(Point(x,y).buffer(r)):
   d.circle(*t((x,y)),r*scale,None,GREEN,.18);d.cross(*t((x,y)),r*scale*.45,GREEN,.13)
 for w in B['walls']:
  if w['kind']=='open':continue
  a,b=t(w['a']),t(w['b'])
  if w['kind']=='glazing':
   dx=b[0]-a[0];dy=b[1]-a[1];ll=math.hypot(dx,dy);ox=-dy/ll*.28;oy=dx/ll*.28
   for sign in [-1,1]:d.line((a[0]+ox*sign,a[1]+oy*sign),(b[0]+ox*sign,b[1]+oy*sign),BLUE,.16)
  else:d.line(a,b,INK,max(.45,w['thickness']*scale*.55))
 for o in B['openings']:
  a,b=t(o['a']),t(o['b']);d.line(a,b,GRAY,.18,[.6,.5]);vec=(b[0]-a[0],b[1]-a[1]);L=math.hypot(*vec)
  if o['id'] in ['ENTRY','SERVICE']:
   d.line(a,(a[0]-vec[1],a[1]+vec[0]),INK,.2)
   ang=math.atan2(vec[1],vec[0]);pts=[(a[0]+L*math.cos(ang+j*math.pi/24),a[1]+L*math.sin(ang+j*math.pi/24)) for j in range(13)];d.path(pts,None,GRAY,.12,[.6,.5],False)
  elif o['id'] in ['T-A','T-C','GARDEN','S-ACCESS']:
   # Sliding leaves stay parallel to the interface; no swing obstructs the gallery.
   nx=-vec[1]/L*.6;ny=vec[0]/L*.6
   d.line((a[0]+nx,a[1]+ny),(a[0]+vec[0]*.52+nx,a[1]+vec[1]*.52+ny),INK,.22)
   d.line((b[0]-nx,b[1]-ny),(b[0]-vec[0]*.52-nx,b[1]-vec[1]*.52-ny),INK,.22)
 for f in B['furniture']:
  geo(d,f['geometry'],t,'#FFF',INK,.22)
  ps=f['geometry'][0]['outer']
  if f['kind'] in ['shelf','storage','counter','display','reading-edge']:
   for frac in [.2,.4,.6,.8]:
    p=[ps[0][i]*(1-frac)+ps[1][i]*frac for i in [0,1]];q=[ps[3][i]*(1-frac)+ps[2][i]*frac for i in [0,1]];d.line(t(p),t(q),GRAY,.12)
  else:
   for i in [0,2]:
    p=ps[i];q=ps[(i+1)%4];mid=[(p[z]+q[z])/2 for z in [0,1]];d.circle(*t(mid),2.3*scale,'#FFF',GRAY,.13)
 d.path([t(p) for p in B['loop']],None,RUST,.35,[1.7,.9],False)
 for key,route in B['routes'].items():d.arrow([t(p) for p in route],GREEN if key=='operations' else RUST,.32,1.5,dash=[1,.6] if key=='operations' else None)
 # Exterior arrival is drawn separately from the indoor loop.
 d.arrow([t(p) for p in [(620,640),(565,515),B['external_ports']['ENTRY']]],RUST,.4,1.8)
 ep=Polygon(B['forecourt'][0]['outer'])
 for cx,cy,r in [(555,595,16),(640,575,18)]:
  if ep.covers(Point(cx,cy).buffer(r)):
   d.circle(*t((cx,cy)),r*scale,None,GREEN,.2);d.cross(*t((cx,cy)),r*scale*.45,GREEN,.15)
 for cx,cy in [(518,535),(568,625)]:
  rect=Polygon([(cx-14,cy-4),(cx+14,cy-4),(cx+14,cy+4),(cx-14,cy+4)])
  if ep.covers(rect):d.path([t(p) for p in rect.exterior.coords],None,GREEN,.3)
 # Short directional markers on the continuous loop.
 for i in [1,4,7]:
  pts=B['loop'];a,b=pts[i],pts[i+1];d.arrow([t(a),t([a[z]+.6*(b[z]-a[z]) for z in [0,1]])],RUST,.3,1.5)
 if labels:
  for k,p in {'A':(287,249),'B':(541,323),'C':(335,474),'S':(280,488),'G':(361,250),'V':(421,315),'E':(580,571)}.items():label(d,t(p),k,11,GREEN if k in 'VE' else INK)
  for k in 'AC':label(d,t(B['ports'][k]),'T'+k,6.5,BLUE)
  d.text(*t((567,447)),'MAIN ENTRY',8,'EN',RUST)
  d.text(*t((444,563)),'SERVICE',7,'EN',GREEN)
def section(d,x,y,w):
 # Diagrammatic section; horizontal intervals are taken from actual selected plan y=300.
 yy=300;v=Polygon(B['void'][0]['outer']);e=Polygon(B['envelope'][0]['outer']);l=LineString([(150,yy),(650,yy)])
 ec=list(e.intersection(l).coords);vc=list(v.intersection(l).coords);x0,x1=sorted([p[0] for p in ec]);v0,v1=sorted([p[0] for p in vc]);s=w/(x1-x0);tx=lambda z:x+(z-x0)*s
 base=y+39;roof=y+11
 d.line((x-3,base),(x+w+3,base),INK,.65)
 for a,b in [(x0,v0),(v1,x1)]:
  d.rect(tx(a),roof,tx(b)-tx(a),1.3,INK,None)
 for a in [x0,x1]:d.line((tx(a),roof),(tx(a),base),INK,.6)
 for a in [v0,v1]:d.line((tx(a),roof+1.3),(tx(a),base),BLUE,.22)
 d.rect(tx(v0),base+1,tx(v1)-tx(v0),3,'#E8EEDD',None)
 for a in [v0+9,(v0+v1)/2,v1-9]:d.arrow([(tx(a),y),(tx(a),base-7)],GREEN,.25,1.5)
 d.text((tx(v0)+tx(v1))/2,base-3,'OPEN SKY',7,'EN',GREEN,'middle')
 d.text(x,base+11,'A / 열람',8);d.text(x+w,base+11,'B / 서가',8,anchor='end')
 d.text(x,y-4,"s1–s2 개념 단면 / 평면 절단선과 대응",9)
 d.text(x,base+19,'수평 경계는 평면에서 추출. 높이·구조·지붕 구성은 미확정.',7.7,color=GRAY)
def draw03():
 d=Board('03_Library_Courtyard_Plan_A2');header(d,'READ / MEET / MAKE','도서관·공유작업소: 바깥의 넓은 마당과 안쪽의 비워진 빛마당을 함께 쓴다.','03 / PROGRAMME RECONSTRUCTION')
 t=lambda p:(20+(p[0]-185)*.47,78+(p[1]-130)*.47)
 d.layer('01_Proposed_Plan');finalplan(d,t,.47)
 # Section line through the actual courtyard.
 d.layer('02_Section_Reference');a=t((230,300));b=t((605,300));d.line(a,b,GRAY,.2,[3,1,.5,1]);d.text(a[0]-3,a[1],'s1',8,'EN');d.text(b[0]+2,b[1],"s2",8,'EN')
 d.layer('03_Notes');d.line((327,66),(327,398),LIGHT,.25)
 d.text(343,70,'경계가 프로그램을 만든다',15)
 entries=[('A','조용한 열람·학습','유리 경계와 문턱 TA로 공유 공간의 소리를 조절한다.','#DBE8EC'),('B','열린 서가·모임','주진입에 가까운 열린 접점. 안내·가벼운 대화가 먼저 온다.','#F2DEB5'),('C','공유작업·자료 보수','별도 운영 출입과 문턱 TC. 소음·분진이 큰 제작은 제외한다.','#DFE6CF'),('G','실내 공유 갤러리','북측은 앉아 읽기, 남측은 작은 전시. 그 옆으로 순환 동선을 잇는다.','#F0D7CF'),('V / E','빛마당 / 진입 마당','V는 채광·식재·짧은 체류, E는 모임·야외 교류를 받는다.','#EFF2E6')]
 for i,(k,title,body,col) in enumerate(entries):
  yy=84+i*25;d.rect(343,yy,15,6,col,GRAY,.15);d.text(350.5,yy+4.5,k,8,'EN',INK,'middle');d.text(362,yy+5,title,10);d.wrap(362,yy+12,body,211,8.3,4)
 d.text(343,218,'S  위생·운영 공간 유보',9);d.wrap(343,225,'필수 설비를 위한 영역만 확보했다. 실측 규모가 정해지기 전에는 위생기구·수용 인원·피난 적합성을 확정하지 않는다.',230,8.1,4)
 d.line((343,239),(575,239),LIGHT,.2)
 section(d,348,256,215)
 d.text(343,332,'왜 도서관·공유작업소인가',11)
 d.wrap(343,340,'조용한 열람, 열린 대화, 가벼운 제작을 분리하면서도 자료와 활동을 공유할 수 있다. 중정은 통행량의 중심이 아니라 서로의 활동을 보게 하는 중심이다.',230,8.6,4.2)
 d.wrap(343,359,'병원은 청결·환자·운영 동선 분리가 더 엄격하고, 학교는 교실 규모와 피난 조건, 시장은 물류·위생 요구가 크다. 현재의 작은 공간군 실험에는 도서관형 조합이 우선 적합하다.',230,8.1,4)
 d.text(18,371,'선과 면의 역할',10)
 samples=[(18,379,INK,.8,'벽체'),(63,379,BLUE,.2,'유리 경계'),(119,379,RUST,.35,'순환·진입'),(182,379,GRAY,.18,'단면·참조')]
 for x,y,c,lw,txt in samples:d.line((x,y),(x+9,y),c,lw,[1,.7] if c==RUST else None);d.text(x+12,y+1,txt,7.5)
 bar(d,18,394,.47);d.text(136,395,'도면 내 1 U = 105.41 mm / 실측 축척 아님',7.5,color=GRAY)
 d.text(343,394,'TA·TC·중정·S: 미닫이 제안 / 띠 기준 폭 0.152 U, 유효 폭 미검증.',7.9,color=GRAY)
 footer(d,'설계 제안 평면. 벽·가구·유리·출입문은 새 가설 / 실내 바닥과 중정의 분리, 동선 중심선·가구 충돌을 기하 검토.');d.save()
if __name__=='__main__':draw01();draw02();draw03()
