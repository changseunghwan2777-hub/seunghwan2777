from draw import *
from develop import develop
from hatching import hatch
from shapely.ops import nearest_points
C=develop(build('STAGGER',1.65))
H=hatch(C)
def rule_board():
 b=Board('02_Module_and_Overlap');header(b,'ONE MOTIF, THREE KINDS OF SHARING','모듈 내부의 중첩과 반복 모듈 사이의 중첩을 분리해서 읽는다','02 / ANATOMY')
 for n in range(4):
  x=18+n*142;b.text(x,69,['01 / THREE WINGS','02 / SUBTRACT THE COURT','03 / ONE WORK NEIGHBOURHOOD','04 / REPEAT ON A LATTICE'][n],9,'EN')
  if n<3:
   T=fit(box(-1.2,-1.2,1.2,1.2),x,80,130,115)
   if n==0:
    for k,g in BASE.items():
     drawgeom(b,g,T,None,'#777',.32)
     p=g.centroid;b.text(*T((p.x,p.y)),k,13,'EN')
     for k,ct in M['centres'].items():b.cross(*T(ct),1.4,ACCENT)
   else:
    drawgeom(b,ENVELOPE.difference(COURT),T,BLACK)
    if n==1:
     drawgeom(b,COURT,T,'#F6E8E3',ACCENT,.25)
    if n==2:
     for g in M['double'].values():drawgeom(b,decode(g),T,'#B97A61')
   captions=[('L = 1.25u / W = 0.80u','중심 간격 R = 0.45u · 120° 간격\n각 공간군의 장축에 공통 비틀림 +15°'),('U = (A ∪ B ∪ C) − T','T = A ∩ B ∩ C\n이전 스터디의 삼중 중첩을 중정으로 유지'),('U = one repeatable motif','세 개의 날개와 하나의 중정을 묶어 반복\n개별 날개를 임의로 재배치하지 않는다')]
   b.text(x,209,captions[n][0],11,'EN');b.wrap(x,218,captions[n][1],129,9,5)
  else:
   small=build('STAGGER',1.65,3,2);T=fit(small['floor'],x,80,130,115);drawgeom(b,small['floor'],T,'#D8D8D5');drawgeom(b,small['overlap'],T,BLACK);drawgeom(b,small['triples'],T,ACCENT)
   b.text(x,209,'d = 1.65u / offset = d / 2',11,'EN');b.wrap(x,218,'x = d [i + (j mod 2) / 2]\ny = (√3 / 2) d j · 전체 모듈 회전 0°',129,9,5)
 b.line((18,245),(576,245),'#CCC',.2)
 types=[('01  LOCAL JOINT',decode(M['double']['AB']),'한 모듈 내부의 교류','개별 업무 날개 사이의 소규모 협의 공간.\n세 방향의 경계에서 짧게 만나는 장소.'),('02  SHARED SEAM',C['contacts'][0]['geometry'].difference(C['triples']),'두 이웃 모듈의 공유 띠','팀 경계를 가로지르는 공동 작업·검토 장소.\n삼중 결절점으로 넓어지는 진입부.'),('03  COLLECTIVE NODE',C['triples'],'세 이웃 모듈의 공유 노드','서로 다른 팀이 만나는 공동 자원·회의 장소.\n이 중첩은 실내로 유지하고 중정과 구분한다.')]
 for i,(title,g,kr,desc) in enumerate(types):
  x=18+i*188;b.text(x,260,title,11,'EN',ACCENT)
  p=max(polys(g),key=lambda p:p.area);T=fit(box(p.centroid.x-.6,p.centroid.y-.6,p.centroid.x+.6,p.centroid.y+.6),x,270,65,80)
  drawgeom(b,p,T,BLACK if i<2 else ACCENT)
  b.text(x+72,286,kr,11);b.wrap(x+72,299,desc,100,9,5)
  b.text(x,367,'형상 확대도 / 각 유형에서 대표 접합 1개 추출',7.5,'KR','#666')
 b.text(18,393,'비우는 규칙: 모듈 안의 T는 중정. 모듈 사이의 중첩은 공유 실내. 반복으로 남는 자연 틈은 별도의 외부 마당.',10)
 footer(b,'발표자료 마지막 M4 스터디의 정규화 모듈을 계승한 설계 가설. 원본 Fruchter House의 정확한 치수 또는 원래 용도를 뜻하지 않는다.');b.save()

def field(clean=False,hatchmode=False):
 name=('Clean_Layered_Hatch' if hatchmode else 'Clean_Figure_Ground') if clean else ('04_Directional_Overlap' if hatchmode else '03_Figure_Ground')
 b=Board(name);T=fit(C['floor'],40,32 if clean else 67,514,356 if clean else 298)
 if not clean:header(b,'DIRECTION BECOMES DENSITY' if hatchmode else 'COURTS WITHIN A CONTINUOUS FIELD','회전 방향을 따라 쌓이는 선: 중첩 횟수와 방향의 차이가 명암을 만든다' if hatchmode else '검정은 실내 바닥, 흰색은 중정과 외부: 공유 공간도 검정 안에 포함한다','04 / HATCH' if hatchmode else '03 / FIGURE–GROUND')
 if hatchmode:
  for k in ['A','B','C']:
   b.layer('Wing_'+k+'_directional_hatch')
   for h in H:
    if h['kind']==k:b.path([T(p) for p in h['pts']],None,'#242424',.20*h['weight'],closed=False)
 else:
  b.layer('Built_floor');drawgeom(b,C['floor'],T,'#111111')
 if not clean:
  b.layer('Legend');b.line((18,375),(576,375),'#CCC',.18)
  if hatchmode:
   b.text(18,386,'A / 165°',10,'EN');b.text(150,386,'B / 45°',10,'EN');b.text(282,386,'C / 285°',10,'EN');b.text(414,386,'2391 clipped vector strokes',10,'EN')
   b.text(18,397,'선은 각 날개의 실제 바닥 경계에서 잘린다. 중정은 모든 해치에서 비운다. 진하기는 층수나 건물 높이를 뜻하지 않는다.',9)
  else:
   b.text(18,387,'12  WORK NEIGHBOURHOODS',11,'EN');b.text(211,387,'12  MODULE COURTS',11,'EN');b.text(410,387,'6  INTERSTITIAL COURTS',11,'EN')
   b.text(18,398,'같은 모듈이 만든 두 종류의 비움: 내부 삼중 중첩에서 뺀 중정 + 반복 모듈 사이에 남는 외부 틈.',9)
  footer(b,'동일한 배열·방향·축척을 사용한 한 쌍의 도면. 흰 배경 / 가상 배치이며 실제 대지·방위·층수는 설정하지 않았다.');
 b.save()

def office_plan():
 b=Board('05_Shared_Office');header(b,'WORK AT THE EDGES, SHARE AT THE SEAMS','개별 업무는 바깥 날개에, 공동 작업은 모듈 사이의 중첩에 배치한다','05 / SHARED OFFICE')
 T=fit(C['floor'],18,76,365,265)
 b.layer('Floor_and_shared_regions');drawgeom(b,C['floor'],T,'#F0EFEC','#242424',.36);drawgeom(b,C['overlap'],T,'#D4B4A4');drawgeom(b,C['triples'],T,'#AC5344')
 b.layer('Public_route_allowance');drawgeom(b,C['corridor'],T,'#FFFFFF')
 b.layer('Paths')
 for l in lines(C['routes']):b.path([T(p) for p in l.coords],None,ACCENT,.3,closed=False)
 b.layer('Indicative_workstations')
 desk_count=0
 for item in C['work']:
  a=item['angle'];available=item['geometry'].difference(C['corridor'].buffer(.018));local=rotate(available,-a,origin=(0,0))
  if local.is_empty:continue
  x0,y0,x1,y1=local.bounds
  x=x0+.105
  while x<x1-.08:
   y=y0+.08
   while y<y1-.06:
    desk=rotate(box(x-.07,y-.035,x+.07,y+.035),a,origin=(0,0))
    chair=rotate(box(x-.018,y+.045,x+.018,y+.073),a,origin=(0,0))
    if available.covers(desk) and available.covers(chair):
     drawgeom(b,desk,T,'#FFF','#555',.16);drawgeom(b,chair,T,'#BBB',None);desk_count+=1
    y+=.22
   x+=.25
 print('Indicative desks',desk_count)
 for outer,inner in C['entries']:
  o=T(outer);q=T(inner);dx,dy=o[0]-q[0],o[1]-q[1];norm=math.hypot(dx,dy);start=(o[0]+dx/norm*8,o[1]+dy/norm*8);b.arrow([start,q],ACCENT,.5,2)
 b.layer('Labels')
 for u in C['units']:
  p=u['court'].centroid;b.text(*T((p.x,p.y)),u['id'],7,'EN','#666','middle')
 b.text(18,358,'전체 공유 동선 / 12개 모듈의 접합을 통해 하나의 연결망 형성',11)
 b.wrap(18,370,'적색선: 중정을 우회하며 각 업무 영역과 공유 노드를 연결하는 경로. 흰 띠: 동선 여유 영역. 외부 공간인 흰 중정과 구분한다.',350,9,5)
 b.line((397,68),(397,398),'#CCC',.2)
 b.text(414,71,'THE SHARED NODE',14,'EN')
 # Detail around first three-motif intersection, shown with context clipped to a study window.
 node=max(polys(C['triples']),key=lambda p:p.area);c=node.centroid;window=box(c.x-.92,c.y-.92,c.x+.92,c.y+.92);T2=fit(window,414,82,162,162)
 drawgeom(b,C['floor'].intersection(window),T2,'#ECEBE8','#444',.28)
 drawgeom(b,C['overlap'].intersection(window),T2,'#D4B4A4')
 drawgeom(b,C['triples'].intersection(window),T2,'#AC5344')
 drawgeom(b,C['corridor'].intersection(window),T2,'#FFF')
 for l in lines(C['routes'].intersection(window)):b.path([T(p) for p in l.coords],None,ACCENT,.4,closed=False)
 # Actual module limits remain visible as fine dashed construction lines.
 for u in C['units']:
  for l in lines(u['envelope'].boundary.intersection(window)):b.path([T(p) for p in l.coords],None,'#777',.15,[1,.8],False)
 b.rect(414,82,162,162,None,'#AAA',.2)
 b.text(414,254,'공동 자원·협의 공간',12);b.wrap(414,265,'세 팀의 경계가 만나는 중심은 비우지 않는다. 두 모듈 사이의 공유 띠가 여기에서 넓어져 함께 쓰는 장소가 된다.',162,10,5.5)
 b.text(414,301,'PROGRAMME GRADIENT',11,'EN')
 for i,(color,title,desc) in enumerate([('#ECEBE8','개별 업무','날개 외곽: 집중 업무·팀 작업'),('#D4B4A4','인접 팀 공유','두 모듈 접합: 협업·검토'),('#AC5344','전체 공유','세 모듈 접합: 공동 자원·협의')]):
  y=315+i*24;b.rect(414,y-4,4,4,color,None);b.text(423,y,title,10);b.text(423,y+7,desc,9)
 footer(b,'공용 오피스 개념 평면. 가구·진입·동선은 제안. 실치수·수용 인원·피난·설비·구조는 미확정이며 실시설계 도면이 아니다.');b.save()
if __name__=='__main__':
 rule_board();field();field(hatchmode=True);office_plan();field(clean=True);field(clean=True,hatchmode=True)
