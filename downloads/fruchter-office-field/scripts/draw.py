from geometry import *
from graphics import *
from shapely.geometry import shape
BLACK='#151515';ACCENT='#A73732'
def drawgeom(b,g,T,fill=None,stroke=None,lw=.2):
 for p in polys(g):b.shape([T(q) for q in p.exterior.coords],[[T(q) for q in r.coords] for r in p.interiors],fill,stroke,lw)
def fit(g,x,y,w,h):
 a,b,c,d=g.bounds;s=min(w/(c-a),h/(d-b));return lambda p:(x+(w-(c-a)*s)/2+(p[0]-a)*s,y+(h-(d-b)*s)/2+(d-p[1])*s)
def matrix():
 b=Board('01_Array_Rules');header(b,'A FIELD OF SHARED EDGES','단일 모듈의 회전에서, 반복 모듈 사이의 중첩으로','01 / RULES')
 names={'GRID':'01  ORTHOGONAL','STAGGER':'02  STAGGERED','ALTERNATE':'03  ALTERNATING 60°'}
 for row,f in enumerate(names):
  for col,d in enumerate([1.45,1.65,1.85]):
   case=build(f,d);m=case['metrics'];x=18+col*188;y=65+row*106
   if f=='STAGGER' and d==1.65:b.rect(x-3,y-5,183,103,'#F6F2EF',None)
   b.text(x,y,names[f]+f' / d = {d:.2f}u',10,'EN',ACCENT if f=='STAGGER' else BLACK)
   T=fit(box(-1.2,-1.2,7.1,4.9),x,y+5,175,74)
   drawgeom(b,case['floor'],T,'#D8D8D5')
   drawgeom(b,case['overlap'],T,BLACK)
   drawgeom(b,case['triples'],T,ACCENT)
   b.text(x,y+85,f"겹침 {m['overlap_pct']:.1f}% · 접합 {m['contacts']} · 최소 접합 내접원 Ø {m['min_contact_diameter']:.2f}u",7.8)
   notes={('GRID',1.45):'면적은 크지만 일부 접합은 가는 조각으로 남는다.',('GRID',1.65):'직교 연결은 명료하나 중첩의 종류가 제한된다.',('GRID',1.85):'최소 접합이 0.03u로 줄어든다.',('STAGGER',1.45):'공유 영역이 커지며 업무 영역의 독립성이 약해진다.',('STAGGER',1.65):'선정: 넓은 두 모듈 접합 + 세 모듈 공유 노드.',('STAGGER',1.85):'중정은 유지되지만 세 모듈 공유 노드가 작아진다.',('ALTERNATE',1.45):'60° 교대가 중첩 크기의 편차를 만든다.',('ALTERNATE',1.65):'접합 수가 줄며 연결 방향이 편중된다.',('ALTERNATE',1.85):'외곽은 다양하지만 공유 영역은 얇아진다.'}
   b.text(x,y+92,notes[(f,d)],8)
 b.text(18,395,'회색: 한 모듈 영역   검정: 두 개 이상 중첩   적색: 세 개 이상 중첩   |   12개 모듈 · 동일 축척 / 방향',9)
 footer(b,'u는 상대 단위. 내접원은 접합 형상 비교값이며 실제 통로 폭이 아니다. 중첩률 = 중첩 합집합 / 전체 바닥. 모든 안은 하나로 연결됨.');b.save()
if __name__=='__main__':matrix()
