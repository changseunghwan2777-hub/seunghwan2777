from draw import *
from selected import C
from hatching import hatch
H=hatch(C)
BASELINE=build_field('BASE',0)

def rule_board():
 b=Board('02_Independent_Pivots');header(b,'TWENTY PIVOTS, ONE CONTINUOUS RULE','20개의 독립 회전 중심 + 두 기준점이 만드는 위치·각도 변화','02 / RULE')
 frame=unary_union([C['floor'],BASELINE['floor']]).envelope
 for n in range(3):
  x=18+n*188;T=fit(frame,x,85,176,135)
  b.text(x,69,['01 / STARTING LATTICE','02 / MOVE THE LOCAL CENTRES','03 / ROTATE EACH WHOLE MOTIF'][n],10,'EN')
  if n==0:
   drawgeom(b,BASELINE['floor'],T,'#D9D9D6')
   for u in BASELINE['units']:b.circle(*T(u['pivot']),.7,BLACK,None)
  elif n==1:
   for u in C['units']:
    b.cross(*T(u['q']),.9,'#AAA',.15);b.arrow([T(u['q']),T(u['pivot'])],RED,.25,1.1);b.circle(*T(u['pivot']),.7,RED,None)
   for fx,lab in [(-2.4,'F1'),(2.4,'F2')]:
    p=T((fx,0));b.circle(*p,7,None,'#CCC',.2);b.cross(*p,2,BLACK);b.text(p[0]+3,p[1]-3,lab,11,'EN')
   for j in range(4):b.path([T(u['pivot']) for u in C['units'] if u['j']==j],None,'#AAA',.18,closed=False)
  else:
   for u in C['units']:
    drawgeom(b,u['floor'],T,None,'#777',.16);p=T(u['pivot']);b.circle(*p,.7,RED,None)
    a=math.radians(u['angle']);r=.28;arc=[T((u['x']+r*math.cos(t),u['y']+r*math.sin(t))) for t in np.linspace(0,a,14)];b.arrow(arc,RED,.2,.8)
    b.text(p[0],p[1]+3.3,u['id'],6.5,'EN',BLACK,'middle')
  captions=['비교 기준을 20개로 맞춘 동일 방향 배열.\n각 모듈 내부의 세 날개 형태와 중정은 유지한다.','F1·F2는 방향을 정하는 제어점이다.\n실제 회전축은 이동한 20개 개별 중심 P이다.','각 모듈 전체를 자신의 P에서 θ만큼 회전한다.\n확대·축소·전단 없이 같은 모듈의 방향을 바꾼다.']
  b.wrap(x,231,captions[n],174,10,5.2)
 b.line((18,253),(576,253),'#CCC',.2)
 b.text(18,270,'LOCAL ANGLES / 모듈별 회전각',13,'EN')
 for u in C['units']:
  x=18+u['i']*56;y=289+(3-u['j'])*22
  b.text(x,y,u['id'],10,'EN',RED);b.text(x+15,y,f"{u['angle']:+.1f}°",12,'EN',BLACK)
 b.text(318,270,'A SMOOTH FIELD, NOT RANDOM ROTATION',12,'EN')
 b.wrap(318,285,'두 제어점에서 멀어질수록 회전 영향은 약해진다. 왼쪽과 오른쪽의 영향은 반대 부호를 갖고, 행 위치에 따른 각도 변화가 더해진다.',250,10,5.5)
 b.text(318,315,'θ(q) = 44° (w₁ − w₂) + 6° qᵧ',12,'EN')
 b.text(318,327,'wₖ = exp[−|q − Fₖ|² / (2 × 2.5²)]',11,'EN')
 b.wrap(318,343,'위치는 두 제어점에 대한 가중 회전 변위의 62%를 합산해 이동한다. 계산식과 모든 P·θ 좌표는 JSON과 설계 설명에 저장했다.',250,9.5,5.4)
 b.text(18,391,'선정 범위 −39.6° ~ +39.6° / 20개 독립 중심 / 동일한 원형 모듈 / 연속적인 위치·각도 규칙',10)
 footer(b,'F1·F2는 2개의 실제 건물 회전축이 아니다. 각 모듈은 자신의 중심 P를 축으로 회전한다. u는 상대 단위이며 모든 조작은 설계 가설.');b.save()

def hero(hatching=False,clean=False):
 name=('Clean_Organic_Hatch' if hatching else 'Clean_Organic_Figure_Ground') if clean else ('04_Organic_Hatch' if hatching else '03_Organic_Figure_Ground')
 b=Board(name);T=fit(C['floor'],35,30 if clean else 68,524,360 if clean else 296)
 if not clean:header(b,'DIRECTIONS INTERWEAVE' if hatching else 'AN IRREGULAR FIELD FROM A REGULAR MOTIF','같은 모듈이 다른 각도로 만나면서 생기는 선의 방향·밀도·겹침의 차이' if hatching else '20개 중정과 변형된 외부 틈, 다양한 접합을 가진 하나의 실내 바닥','04 / HATCH' if hatching else '03 / FIGURE–GROUND')
 if hatching:
  for k in ['A','B','C']:
   b.layer('Wing_'+k+'_hatch')
   for h in H:
    if h['kind']==k:b.path([T(p) for p in h['pts']],None,'#242424',.2*h['weight'],closed=False)
  b.layer('Intermodule_overlap_edges');drawgeom(b,C['overlap'],T,None,'#454545',.09)
 else:
  b.layer('Built_floor');drawgeom(b,C['floor'],T,'#111')
 if not clean:
  b.layer('Legend');b.line((18,375),(576,375),'#CCC',.2)
  if hatching:
   b.text(18,387,'60 DIRECTIONAL LAYERS',11,'EN');b.text(222,387,f'{len(H)} CLIPPED VECTOR STROKES',11,'EN');b.text(440,387,'20 LOCAL ROTATIONS',11,'EN')
   b.text(18,398,'세 날개의 기준 방향에 각 모듈의 θ를 더한다. 가는 윤곽선은 실제 모듈 간 중첩 경계만 강조한다.',9)
  else:
   b.text(18,387,'20 MODULE COURTS',11,'EN');b.text(220,387,'32 PRIMARY CONTACTS',11,'EN');b.text(430,387,'1 CONNECTED FLOOR',11,'EN')
   b.text(18,398,'검정: 공유 공간을 포함한 실내 바닥 / 흰색: 중정과 외부. 39개 전체 접합 중 가는 7개는 주요 연결망에서 제외한다.',9)
  footer(b,'동일 배열·방향·축척의 한 쌍. 0.18u 내접원 기준은 접합 비교용 가정이며 실제 통로 폭이나 법규 검토를 뜻하지 않는다.')
 b.save()

def joint_atlas():
 b=Board('05_Overlap_Atlas');header(b,'ONE RULE, DIFFERENT SHARED SPACES','중첩이 크고 작아지는 것뿐 아니라, 만나는 각도와 경계의 형태도 달라진다','05 / CONTACTS')
 eligible=[c for c in C['contacts'] if c['usable']]
 thin=min(C['contacts'],key=lambda c:c['diameter'])
 parallel=min(eligible,key=lambda c:c['delta_angle'])
 broad=max(eligible,key=lambda c:c['diameter'])
 oblique=max(eligible,key=lambda c:c['delta_angle'])
 triple=max(polys(C['triples']),key=lambda p:p.area)
 court=next(u for u in C['units'] if u['id']=='13');intrusion=court['court'].intersection(unary_union([u['envelope'] for u in C['units'] if u!=court]))
 items=[('01  THIN THRESHOLD',thin,'가는 경계 / 보조 접점','좁게 겹치는 틈은 주요 동선으로 세지 않는다. 시선·경계 조정 대상으로 남긴다.'),('02  SMALL ANGLE DIFFERENCE',parallel,'작은 상대 회전 / 비대칭 접합','모듈 전체의 방향은 가깝지만 서로 다른 날개가 만나 비대칭 공유 영역을 만든다.'),('03  OBLIQUE CONTACT',oblique,'사선 교차 / 방향 전환','두 방향이 큰 각도로 만나 진입 방향과 시선이 전환되는 공유 영역을 만든다.'),('04  BROAD OVERLAP',broad,'넓은 접합 / 협업 장소','넓어진 공유 영역은 팀 사이의 공동 작업이나 협의 공간으로 우선 검토한다.'),('05  THREE-MOTIF NODE',None,'세 모듈 결절 / 공동 자원','서로 다른 모듈의 접속이 집중되는 곳. 여러 팀이 함께 쓰는 실내로 유지한다.'),('06  COURT PROTECTION',None,'중정 보존 / 최소 절삭','모듈 13의 중정에 들어온 이웃 바닥 0.00875u²를 제거해 기존 비움을 유지한다.')]
 for n,(title,contact,kr,description) in enumerate(items):
  x=18+(n%3)*188;y=68+(n//3)*166;b.text(x,y,title,11,'EN',RED)
  if contact:
   a=next(u for u in C['units'] if u['id']==contact['a']);d=next(u for u in C['units'] if u['id']==contact['b']);g=contact['geometry'];centre=g.centroid;context=[a,d]
   meta=f"{a['id']} / {d['id']} · Δθ {contact['delta_angle']:.1f}° · Ø {contact['diameter']:.2f}u"
  elif n==4:
   g=triple;centre=g.centroid;context=[u for u in C['units'] if u['floor'].intersection(g).area>g.area*.99];meta=' / '.join(u['id'] for u in context)+f' · {g.area:.3f}u²'
  else:
   g=intrusion;centre=court['court'].centroid;context=[u for u in C['units'] if u['envelope'].distance(court['court'])<1e-6];meta='모듈 13 · 적색 = 제거할 침범 부분'
  frame=box(centre.x-1.35,centre.y-1.10,centre.x+1.35,centre.y+1.10);T=fit(frame,x,y+9,176,102)
  for u in context:drawgeom(b,u['envelope'].intersection(frame),T,'#F1F0ED','#888',.17)
  drawgeom(b,C['courts'].intersection(frame),T,'#FFF','#BBB',.1)
  drawgeom(b,g.intersection(frame),T,RED if n>=4 else BLACK)
  b.text(x,y+119,meta,8.3)
  b.text(x,y+130,kr,10);b.wrap(x,y+140,description,174,9,4.8)
 footer(b,'모든 확대도는 동일 축척의 실제 교집합이다. 맥락 외곽은 표시 창에서 잘렸다. 용도는 공용 오피스 설계 제안이며 세부 실치수·가구 배치는 미확정.');b.save()

if __name__=='__main__':
 rule_board();hero();hero(hatching=True);joint_atlas();hero(clean=True);hero(hatching=True,clean=True)
