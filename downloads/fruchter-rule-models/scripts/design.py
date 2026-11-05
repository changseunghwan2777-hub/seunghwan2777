from pathlib import Path
import math,json
from shapely.geometry import Polygon,LineString,Point,box
from shapely.affinity import rotate,translate
from shapely.ops import unary_union,polylabel,linemerge
from shapely import set_precision
J=Path(__file__).resolve().parents[1]
SRC=json.loads((J/'source/rotation-study.json').read_text());orig=SRC['original']['regions'];source_areas={k:Polygon(orig[k]).area for k in 'ABC'};unit=math.sqrt(sum(source_areas.values())/3)
L,W=1.25,.80;rect=box(-L/2,-W/2,L/2,W/2);theta={'A':150,'B':30,'C':270}
def clean(g):return set_precision(g,1e-8)
def shape(g):return [{'outer':list(p.exterior.coords)[:-1],'holes':[list(h.coords)[:-1] for h in p.interiors]} for p in getattr(g,'geoms',[g]) if p.geom_type=='Polygon' and p.area>1e-9]
def fromdata(gs):return unary_union([Polygon(g['outer'],g.get('holes',[])) for g in gs])
def cnt(g):return len(shape(g))
def xy(p):return [p.x,p.y]
def radial(radius,phase):
 centres={k:[radius*math.cos(math.radians(t)),radius*math.sin(math.radians(t))] for k,t in theta.items()}
 polys={k:clean(translate(rotate(rect,t+phase,origin=(0,0)),*centres[k])) for k,t in theta.items()}
 return polys,centres,{k:t+phase for k,t in theta.items()}
def stats(polys):
 pair={a+b:clean(polys[a].intersection(polys[b])) for a,b in [('A','B'),('B','C'),('C','A')]}
 triple=clean(polys['A'].intersection(polys['B']).intersection(polys['C']));envelope=clean(unary_union(list(polys.values())))
 double={k:clean(p.difference(triple)) for k,p in pair.items()};overlap=clean(unary_union(list(pair.values())))
 single={k:clean(p.difference(overlap)) for k,p in polys.items()};floor=clean(envelope.difference(triple))
 natural=unary_union([Polygon(h) for p in getattr(envelope,'geoms',[envelope]) if p.geom_type=='Polygon' for h in p.interiors])
 diam={}
 for k,p in double.items():
  if p.is_empty:diam[k]=0;continue
  largest=max(getattr(p,'geoms',[p]),key=lambda x:x.area);c=polylabel(largest,tolerance=.0001);diam[k]=2*c.distance(largest.boundary)
 return dict(pair=pair,triple=triple,envelope=envelope,double=double,single=single,floor=floor,natural=natural,overlap=overlap,diam=diam)
def serialize(id,name,rule,polys,centres,angles):
 q=stats(polys);metrics={'module_sum':sum(p.area for p in polys.values()),'union':q['envelope'].area,'triple':q['triple'].area,'double_total':sum(p.area for p in q['double'].values()),'joint_areas':{k:p.area for k,p in q['double'].items()},'joint_diameters':q['diam'],'floor_after_triple_cut':q['floor'].area,'floor_components':cnt(q['floor']),'natural_void':q['natural'].area,'pair_connections':sum(p.area>1e-5 for p in q['pair'].values())}
 return {'id':id,'name':name,'rule':rule,'centres':centres,'angles':angles,'regions':{k:shape(p) for k,p in polys.items()},**{k:shape(q[k]) for k in ['triple','envelope','floor','natural','overlap']},**{k:{n:shape(p) for n,p in q[k].items()} for k in ['pair','double','single']},'metrics':metrics}
models=[]
p={k:clean(rotate(rect,i*30,origin=(0,0))) for i,k in enumerate('ABC')};models.append(serialize('M1','Concentric Fan','같은 중심 / 30°씩 회전',p,{k:[0,0] for k in 'ABC'},{k:i*30 for i,k in enumerate('ABC')}))
c={k:[(i-1)*.70,0] for i,k in enumerate('ABC')};a={'A':0,'B':90,'C':180};p={k:clean(translate(rotate(rect,a[k],origin=(0,0)),*c[k])) for k in 'ABC'};models.append(serialize('M2','Alternating Chain','0.70 u 등간격 / 90° 교대',p,c,a))
for id,name,R,phi in [('M3','Mirror Triad',.45,0),('M4','Chiral Triad',.45,15),('M5','Perimeter Cycle',.55,90)]:
 p,c,a=radial(R,phi);m=serialize(id,name,f'중심 간격 120° / R={R:.2f} u / 공통 위상 {phi}°',p,c,a);m['radius']=R;m['phase']=phi;models.append(m)
grid=[]
for R in [.4,.45,.5]:
 for phi in [0,15,30]:
  p,c,a=radial(R,phi);m=serialize(f'R{R:.2f}_P{phi}','Parameter Study','R와 공통 위상만 변경',p,c,a);m.update(radius=R,phase=phi)
  # Length of a module's longitudinal entry axis inside a two-way overlap.
  t=math.radians(a['A']);cx,cy=c['A'];axis=LineString([(cx+L/2*math.cos(t),cy+L/2*math.sin(t)),(cx-L/2*math.cos(t),cy-L/2*math.sin(t))])
  m['axis_twofold_length']=axis.intersection(fromdata(m['double']['AB'])).length+axis.intersection(fromdata(m['double']['CA'])).length
  grid.append(m)
selected=models[3];P={k:fromdata(v) for k,v in selected['regions'].items()};Q=stats(P);T=Q['triple'];F=Q['floor'];centres=selected['centres'];angles=selected['angles']
# Explicit same-area module proposal, not an unchanged historical outline.
regularisation={'source_areas':source_areas,'source_coordinate_units_per_u':unit,'module_area_source_units':unit**2,'module_dimensions_u':[L,W],'area_change_percent':{k:(unit**2/source_areas[k]-1)*100 for k in 'ABC'},'note':'Common rectangular modules preserve the summed traced area; individual outlines, aspect ratios and areas are adjusted as a declared design hypothesis.'}
# Applying the same centre/angle rule to unregularised source quadrilaterals checks lineage.
raw_original={}
for k in 'ABC':
 p=Polygon([(x/unit,-y/unit) for x,y in orig[k]]);centre=p.centroid;coords=list(p.exterior.coords);edge=max([(coords[i],coords[i+1]) for i in range(4)],key=lambda ab:LineString(ab).length);ang=math.degrees(math.atan2(edge[1][1]-edge[0][1],edge[1][0]-edge[0][0]));p=translate(p,-centre.x,-centre.y);p=rotate(p,angles[k]-ang,origin=(0,0));raw_original[k]=clean(translate(p,*centres[k]))
robust=serialize('R0','Original outlines reapplied','같은 배치·회전 규칙 / 원래 외곽·면적 재적용',raw_original,centres,angles)
# Readable points and room interfaces. Spatial programme follows overlap multiplicity.
rooms=[]
for k,name,col in [('A','조용한 열람','#E1E7EC'),('B','열린 서가·대화','#ECE5D5'),('C','자료 작업·배움','#E3E9DE')]:rooms.append({'id':k,'name':name,'geometry':shape(Q['single'][k]),'color':col})
for k,name in [('AB','자료 함께 읽기'),('BC','작업·전시 공유'),('CA','작은 토론·피드백')]:rooms.append({'id':'J'+k,'name':name,'geometry':shape(Q['double'][k]),'color':'#EDD3BE'})
joint_centres={k:xy(polylabel(p,tolerance=.0001)) for k,p in Q['double'].items()}
# Leave openings on both sides of each joint. This creates A–AB–B–BC–C–CA–A.
def lineparts(g):return [p for p in getattr(g,'geoms',[g]) if p.geom_type=='LineString' and p.length>1e-7]
walls=[];doors=[];ports={}
def wall(a,b,id,kind='wall'):walls.append({'id':id,'a':list(a),'b':list(b),'kind':kind})
for pair,g in Q['double'].items():
 for k in pair:
  boundary=clean(g.boundary.intersection(Q['single'][k].boundary));parts=lineparts(boundary);assert parts,(pair,k)
  host=max(parts,key=lambda p:p.length);q=host.interpolate(.58 if k==pair[0] else .42,normalized=True);at=host.project(q);span=min(.15,host.length*.45);lo=at-span/2;hi=at+span/2
  assert lo>0 and hi<host.length
  port=xy(q);ports[pair+'-'+k]=port
  for i,l in enumerate(parts):
   if l.equals(host):
    for j,(a,b) in enumerate([(0,lo),(hi,l.length)]):wall(l.interpolate(a).coords[0],l.interpolate(b).coords[0],f'{pair}-{k}-{i}-{j}','glazing' if k=='A' else 'screen')
    doors.append({'id':pair+'-'+k,'a':xy(l.interpolate(lo)),'b':xy(l.interpolate(hi)),'point':port,'kind':'sliding' if k=='A' else 'open'})
   else:wall(l.coords[0],l.coords[-1],f'{pair}-{k}-{i}','glazing' if k=='A' else 'screen')
# Exterior entries are centred on the outer longitudinal end of each module.
entries={};exit_host={}
for k in 'ABC':
 ang=math.radians(angles[k]);cx,cy=centres[k];q=Point(cx+L/2*math.cos(ang),cy+L/2*math.sin(ang));entries[k]=xy(q)
coords=list(Q['envelope'].exterior.coords)
for i,(a,b) in enumerate(zip(coords[:-1],coords[1:])):
 line=LineString([a,b]);key=next((k for k,q in entries.items() if line.distance(Point(q))<1e-6),None)
 if key:
  at=line.project(Point(entries[key]));lo=at-.085;hi=at+.085;assert lo>0 and hi<line.length
  for j,(a,b) in enumerate([(0,lo),(hi,line.length)]):wall(line.interpolate(a).coords[0],line.interpolate(b).coords[0],f'outer-{i}-{j}')
  doors.append({'id':'ENTRY-'+key,'a':xy(line.interpolate(lo)),'b':xy(line.interpolate(hi)),'point':entries[key],'kind':'external'})
 else:
  for j,(a,b,kind) in enumerate([(0,.18,'wall'),(.18,.82,'glazing'),(.82,1,'wall')]):wall(line.interpolate(a,normalized=True).coords[0],line.interpolate(b,normalized=True).coords[0],f'outer-{i}-{j}',kind if line.length>.24 else 'wall')
# Actual triple-intersection boundary becomes the court glazing; no offset polygon.
cs=list(T.exterior.coords)
for i,(a,b) in enumerate(zip(cs[:-1],cs[1:])):wall(a,b,f'court-{i}','glazing')
# Paths are authored in the programme plan. The joint medials are used as waypoints.
centres_single={k:xy(polylabel(p,tolerance=.0001)) for k,p in Q['single'].items()}
routes={}
for pair in ['AB','BC','CA']:
 k,l=pair;routes['through-'+pair]=[centres_single[k],ports[pair+'-'+k],joint_centres[pair],ports[pair+'-'+l],centres_single[l]]
for k in 'ABC':routes['entry-'+k]=[entries[k],centres_single[k]]
# Furniture placed after the route skeleton. Candidate placement is checked, not clipped.
def oriented_rect(cx,cy,w,h,angle):return clean(translate(rotate(box(-w/2,-h/2,w/2,h/2),angle,origin=(0,0)),cx,cy))
furniture=[]
# Search a small, deterministic local grid for two pieces in each single domain,
# favouring the outer daylight edge. This is a placement aid, not programme inference.
route_lines=unary_union([LineString(ps) for ps in routes.values()]);wall_lines=unary_union([LineString([w['a'],w['b']]) for w in walls]);occupied=[]
for k in 'ABC':
 ang=angles[k];a=math.radians(ang);cx,cy=centres[k]
 for j,(w,h,kind) in enumerate([(.24,.10,'table'),(.27,.06,'shelf')]):
  candidates=[]
  for u in [.12,.24,.36,.45]:
   for v in [-.27,-.22,.22,.27]:
    x=cx+u*math.cos(a)-v*math.sin(a);y=cy+u*math.sin(a)+v*math.cos(a);g=oriented_rect(x,y,w,h,ang)
    if Q['single'][k].buffer(1e-7).covers(g) and g.distance(route_lines)>.055 and g.distance(wall_lines)>.02 and all(g.distance(q)>.05 for q in occupied):candidates.append((abs(u-.24)+abs(v-(.22 if j==0 else -.22)),g))
  assert candidates,(k,j)
  g=min(candidates,key=lambda x:x[0])[1];occupied.append(g);furniture.append({'id':k+str(j+1),'room':k,'kind':kind,'geometry':shape(g)})
# Joint-side ledges remain outside the two-threshold path and within the overlap.
for pair,g in Q['double'].items():
 c=polylabel(g,tolerance=.0001);candidates=[]
 for dx in [-.10,-.075,-.05,.05,.075,.10]:
  for dy in [-.10,-.075,-.05,.05,.075,.10]:
   r=oriented_rect(c.x+dx,c.y+dy,.105,.035,angles[pair[0]])
   if g.covers(r) and r.distance(route_lines)>.025 and r.distance(wall_lines)>.008:candidates.append((r.distance(route_lines),r))
 if candidates:
  f=max(candidates,key=lambda x:x[0])[1];occupied.append(f);furniture.append({'id':'J'+pair,'room':'J'+pair,'kind':'shared-ledge','geometry':shape(f)})
# Geometry and room connectivity are tested before drawing.
obstacles=unary_union(occupied)
for key,ps in routes.items():
 line=LineString(ps);assert F.buffer(1e-6).covers(line),(key,'outside floor');assert line.intersection(obstacles).is_empty,(key,'furniture')
 for w in walls:assert line.intersection(LineString([w['a'],w['b']])).is_empty,(key,w['id'])
assert cnt(F)==1 and len(F.interiors)==1
sym_error=F.symmetric_difference(rotate(F,120,origin=(0,0))).area
assert sym_error<1e-6,sym_error
final={'rooms':rooms,'joint_centres':joint_centres,'single_centres':centres_single,'entries':entries,'walls':walls,'doors':doors,'ports':ports,'routes':routes,'furniture':furniture,'floor':shape(F),'court':shape(T),'symmetry_error_u2':sym_error,'note':'All walls, glazing, openings, furniture and uses are proposals. Route centre lines checked; no metric clear width, code, structure or lighting compliance asserted.'}
policies=[]
for id,name,void in [('P0','Keep all',Polygon()),('P1','Remove all overlaps',Q['overlap']),('P2','Remove exactly double',unary_union(list(Q['double'].values()))),('P3','Remove triple only',T)]:
 floor=clean(Q['envelope'].difference(void));policies.append({'id':id,'name':name,'void':shape(void),'floor':shape(floor),'components':cnt(floor.buffer(-1e-6,join_style='mitre')),'raw_polygon_count':cnt(floor),'connectivity_probe_u':1e-6,'floor_area':floor.area})
result={'void_policies':policies,'title':'Fruchter House — Rule-Based Overlap Models','coordinate_convention':'Mathematical X right, Y up; diagram orientation is not a verified site north.','unit':'u = sqrt(sum of traced A+B+C areas / 3); no metric scale. This differs from the previous U edge-length unit.','regularisation':regularisation,'models':models,'parameter_grid':grid,'selected':'M4','selected_radius':.45,'selected_phase':15,'theta':theta,'original_outline_check':robust,'plan':final}
(J/'design/study.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
for m in models:print(m['id'],m['metrics'])
print('Final furniture',len(furniture),'walls',len(walls),'doors',len(doors),'symmetry',sym_error)
