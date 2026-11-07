from fields import *
from graphics import *
BLACK='#171717';RED='#A73732'
def drawgeom(b,g,T,fill=None,stroke=None,lw=.2):
 for p in polys(g):b.shape([T(q) for q in p.exterior.coords],[[T(q) for q in r.coords] for r in p.interiors],fill,stroke,lw)
def fit(g,x,y,w,h):
 a,b,c,d=g.bounds;s=min(w/(c-a),h/(d-b));return lambda p:(x+(w-(c-a)*s)/2+(p[0]-a)*s,y+(h-(d-b)*s)/2+(d-p[1])*s)
def matrix():
 cases=[build_field(f,a) for f in ['FAN','COUNTER','STREAM'] for a in [.65,1,1.35]];frame=unary_union([c['floor'] for c in cases]).envelope
 b=Board('01_Field_Alternatives');header(b,'FROM REPETITION TO A ROTATION FIELD','하나의 세 날개 모듈을 유지하고, 각 중심점의 위치와 회전각을 연속적으로 바꾼다','01 / COMPARE')
 for index,c in enumerate(cases):
  row=index//3;col=index%3;x=18+col*188;y=65+row*106;m=c['metrics'];T=fit(frame,x,y+5,176,75)
  if c['id']=='COUNTER-1.00':b.rect(x-3,y-5,184,103,'#F7F1EC',None)
  title={'FAN':'FAN / 곡률에 따른 회전','COUNTER':'COUNTER / 두 기준점의 방향장','STREAM':'STREAM / 접선 방향의 변화'}[c['family']]
  b.text(x,y,title+f" / {c['amount']:.2f}",9)
  drawgeom(b,c['floor'],T,'#DAD9D5');drawgeom(b,c['overlap'],T,BLACK);drawgeom(b,c['triples'],T,RED)
  b.text(x,y+85,f"각도 {m['min_angle']:.0f}° ~ {m['max_angle']:.0f}° · 겹침 {m['overlap_pct']:.1f}%",8.2)
  b.text(x,y+93,f"주요 접합 {m['usable_contacts']} · 연결망 {m['usable_graph_components']}개 · 접합 면적 CV {m['area_cv']:.2f}",8)
 b.text(18,394,'회색: 실내 바닥   검정: 두 모듈 이상 겹침   적색: 세 모듈 이상 겹침   |   20개 모듈 / 동일 방향·축척',9)
 footer(b,'주요 접합: 내접원 지름 ≥ 0.18u인 형상 비교 기준. 법규상 통로 폭이 아님. CV는 면적 변동계수이며 형상 다양성 전체를 나타내지 않는다.');b.save()
if __name__=='__main__':matrix()
