from pathlib import Path
import json,math
from shapely import set_precision
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union,polylabel,nearest_points,linemerge
J=Path(__file__).resolve().parents[1]
S=json.loads((J/'source/rotation-study.json').read_text());BASE=S['original'];U=S['U']
angles={'A':-14,'B':18,'C':10}
def clean(p):return set_precision(p,.001)
def tf(p,k,translations):
 a,b=S['pivots'][k];r=math.radians(angles[k]);dx,dy=translations[k];x,y=p[0]-a,p[1]-b
 return [a+x*math.cos(r)-y*math.sin(r)+dx,b+x*math.sin(r)+y*math.cos(r)+dy]
def regions(tr):return {k:clean(Polygon([tf(p,k,tr) for p in BASE['regions'][k]])) for k in 'ABC'}
def data(g):
 return [{'outer':list(p.exterior.coords)[:-1],'holes':[list(h.coords)[:-1] for h in p.interiors]} for p in getattr(g,'geoms',[g]) if p.geom_type=='Polygon' and p.area>.1]
def lines(g):
 return [p for p in getattr(g,'geoms',[g]) if p.geom_type=='LineString' and p.length>.1]
def point(p):return [p.x,p.y]
def count(g):return len(data(g))
def serwall(a,b,id,kind='wall',thickness=5):return {'id':id,'a':list(a),'b':list(b),'kind':kind,'thickness':thickness}

# A / Pull apart: a courtyard develops from facing edges of three rotated wings.
TA={'A':[-40,-12],'B':[109,-25],'C':[-40,65]};pa=regions(TA)
ps={k:[tf(p,k,TA) for p in BASE['regions'][k]] for k in 'ABC'}
central=clean(Polygon([ps['A'][2],ps['A'][1],ps['B'][0],ps['B'][3],ps['C'][1],ps['C'][0]]))
acourt=central.buffer(-34,join_style='mitre');aenv=clean(unary_union(list(pa.values())+[central]));afloor=aenv.difference(acourt)
A={'id':'A','name':'Expanded Court','translations':TA,'regions':{k:data(p) for k,p in pa.items()},'envelope':data(aenv),'void':data(acourt),'shared':data(central.difference(acourt)),'floor':data(afloor),'origin':'Courtyard from the enlarged pre-existing gap; facing edges generate its boundary. A 34-unit perimeter strip is reserved for indoor linkage, a design assumption.'}

# B / Fold inward: actual footprint overlaps, not a crossing of diagram arrows.
TB={'A':[125,55],'B':[-120,20],'C':[0,-90]};pb=regions(TB)
pairs={a+b:clean(pb[a].intersection(pb[b])) for a,b in [('A','B'),('B','C'),('C','A')]}
overlap=clean(unary_union(list(pairs.values())));env=clean(unary_union(list(pb.values())))
full_subtraction=env.difference(overlap)
# Taking every overlap out disconnects the plan. Retain a band around its edge,
# then take out only the inner core. This is an explicit second design choice.
retained_band=34
void=clean(overlap.buffer(-retained_band,join_style='mitre').simplify(5,preserve_topology=True))
assert overlap.buffer(-30,join_style='mitre').buffer(.01).covers(void)
floor=clean(env.difference(void));shared=clean(overlap.difference(void))
exclusive={k:clean(p.difference(overlap)) for k,p in pb.items()}
assert all(p.geom_type=='Polygon' for p in exclusive.values()),[(k,p.geom_type) for k,p in exclusive.items()]
loop=LineString(void.buffer(17,join_style='mitre').exterior.coords)

# A generous forecourt sits outside the southeast re-entrant corner. It is an
# exterior arrival space; it is not counted as enclosed library floor area.
pB=[tf(p,'B',TB) for p in BASE['regions']['B']];pC=[tf(p,'C',TB) for p in BASE['regions']['C']]
joint=pb['B'].boundary.intersection(pb['C'].boundary)
joint_pts=[p for p in getattr(joint,'geoms',[joint]) if p.geom_type=='Point']
se=max(joint_pts,key=lambda p:p.x+p.y)
forecourt=clean(Polygon([point(se),pB[2],[705,590],[500,735],pC[2]]))
assert forecourt.intersection(env).area<.1

def uv(k,u,v):
 p=BASE['regions'][k];return tf([sum([p[0][i]*(1-u)*(1-v),p[1][i]*u*(1-v),p[2][i]*u*v,p[3][i]*(1-u)*v]) for i in [0,1]],k,TB)
def rectuv(k,a,b,c,d):return clean(Polygon([uv(k,u,v) for u,v in [(a,b),(c,b),(c,d),(a,d)]]))
# Programme follows the new geometry; all dimensions and uses are proposals.
service=rectuv('C',.08,.65,.40,.93)
assert exclusive['C'].buffer(.01).covers(service)
rooms=[{'id':'A','name':'조용한 열람·학습','geometry':data(exclusive['A']),'color':'#DBE8EC'},
       {'id':'B','name':'열린 서가·모임','geometry':data(exclusive['B']),'color':'#F2DEB5'},
       {'id':'C','name':'공유작업·자료 보수','geometry':data(exclusive['C'].difference(service)),'color':'#DFE6CF'},
       {'id':'S','name':'위생·운영 유보','geometry':data(service),'color':'#E0DCE3'},
       {'id':'G','name':'실내 공유 갤러리','geometry':data(shared),'color':'#F0D7CF'}]

# Three interfaces and thresholds. B opens onto the shared gallery; A and C
# receive glazed separators. Windows and door spans are explicit assumptions.
interfaces={};ports={};walls=[];openings=[]
for k in 'ABC':
 interface=clean(exclusive[k].boundary.intersection(shared.boundary));ls=lines(interface)
 merged=linemerge(ls) if len(ls)>1 else ls[0]
 # Pick the longest contiguous interface; the host-authored target locates the door.
 target=Point({'A':[350,290],'B':[460,290],'C':[370,430]}[k])
 portal_line=min(lines(merged),key=lambda l:l.distance(target));q=portal_line.interpolate(portal_line.project(target));ports[k]=point(q)
 interfaces[k]=[list(l.coords) for l in ls]
 for i,l in enumerate(ls):
  if l.distance(q)<.01:
   at=l.project(q);lo=max(0,at-24);hi=min(l.length,at+24)
   for j,(a,b) in enumerate([(0,lo),(hi,l.length)]):
    if b-a>1:walls.append(serwall(l.interpolate(a).coords[0],l.interpolate(b).coords[0],f'interface-{k}-{i}-{j}','glazing' if k in 'AC' else 'open'))
   openings.append({'id':'T-'+k,'a':point(l.interpolate(lo)),'b':point(l.interpolate(hi)),'point':ports[k],'kind':'indoor threshold / type and clear size unverified'})
  elif k in 'AC':walls.append(serwall(l.coords[0],l.coords[-1],f'interface-{k}-{i}','glazing'))

# Main entrance at B's southeast face; C receives a separate operations door.
shell_segments=[LineString([a,b]) for a,b in zip(list(env.exterior.coords)[:-1],list(env.exterior.coords)[1:])]
door_targets={'ENTRY':Point(535,430),'SERVICE':Point(420,535)}
external_ports={}
for i,l in enumerate(shell_segments):
 active=[key for key,target in door_targets.items() if l==min(shell_segments,key=lambda line:line.distance(target))]
 spans=[]
 if active:
  key=active[0];q=l.interpolate(l.project(door_targets[key]));at=l.project(q);lo=max(6,at-20);hi=min(l.length-6,at+20);external_ports[key]=point(q)
  spans=[(0,lo,'wall'),(hi,l.length,'wall')];openings.append({'id':key,'a':point(l.interpolate(lo)),'b':point(l.interpolate(hi)),'point':point(q),'kind':'external doorway proposal'})
 else:
  # Daylight strips interrupt long exterior faces; short corners stay solid.
  spans=[(0,l.length*.18,'wall'),(l.length*.18,l.length*.82,'glazing'),(l.length*.82,l.length,'wall')] if l.length>110 else [(0,l.length,'wall')]
 for j,(a,b,kind) in enumerate(spans):
  if b-a>1:walls.append(serwall(l.interpolate(a).coords[0],l.interpolate(b).coords[0],f'shell-{i}-{j}',kind,7))

# Court is open to the sky, with a glazed perimeter and one garden access opening.
vc=list(void.exterior.coords);court_segments=[LineString([a,b]) for a,b in zip(vc[:-1],vc[1:])]
garden_target=Point(400,420);gl=min(court_segments,key=lambda l:l.distance(garden_target));gq=gl.interpolate(gl.project(garden_target));garden_port=point(gq)
for i,l in enumerate(court_segments):
 if l==gl:
  at=l.project(gq);lo=max(0,at-14);hi=min(l.length,at+14)
  for j,(a,b) in enumerate([(0,lo),(hi,l.length)]):
   if b-a>1:walls.append(serwall(l.interpolate(a).coords[0],l.interpolate(b).coords[0],f'court-{i}-{j}','glazing',3))
  openings.append({'id':'GARDEN','a':point(l.interpolate(lo)),'b':point(l.interpolate(hi)),'point':garden_port,'kind':'garden access; level drainage unresolved'})
 else:walls.append(serwall(l.coords[0],l.coords[-1],f'court-{i}','glazing',3))

# Service reservation: enclosed rectangle with a gap on its upper edge.
sc=list(service.exterior.coords)
for i,l in enumerate([LineString([a,b]) for a,b in zip(sc[:-1],sc[1:])]):
 if i==0:
  for j,(a,b) in enumerate([(0,.3),(.75,1)]):walls.append(serwall(l.interpolate(a,normalized=True).coords[0],l.interpolate(b,normalized=True).coords[0],f'S-{i}-{j}'))
  service_port=point(l.interpolate(.525,normalized=True));openings.append({'id':'S-ACCESS','a':point(l.interpolate(.3,normalized=True)),'b':point(l.interpolate(.75,normalized=True)),'point':service_port,'kind':'service reservation opening'})
 else:walls.append(serwall(l.coords[0],l.coords[-1],f'S-{i}'))

furniture=[]
def frect(cx,cy,w,h,angle):
 r=math.radians(angle)
 return clean(Polygon([(cx+x*math.cos(r)-y*math.sin(r),cy+x*math.sin(r)+y*math.cos(r)) for x,y in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]]))
for id,k,x,y,w,h,ang,kind in [
 ('A-1','A',328,191,34,18,28,'reading'),('A-2','A',300,290,32,18,28,'reading'),('A-3','A',258,328,24,8,28,'shelf'),
 ('B-1','B',551,280,8,46,-5,'shelf'),('B-2','B',525,345,34,22,-5,'reading'),('B-3','B',540,402,28,9,-5,'counter'),
 ('C-1','C',370,485,38,22,18,'work'),('C-2','C',425,480,27,18,18,'work'),('C-3','C',380,530,40,12,18,'storage')]:
 g=frect(x,y,w,h,ang);assert exclusive[k].buffer(.01).covers(g),(id,g.difference(exclusive[k]).area)
 furniture.append({'id':id,'group':k,'kind':kind,'geometry':data(g)})
# Pause/display positions occupy the side of the shared loop, not its centre line.
for id,x,y,angle,kind in [('G-1',410,225,-4,'reading-edge'),('G-2',406,444,18,'display')]:
 g=frect(x,y,24,7,angle);assert shared.covers(g) and g.distance(loop)>7
 furniture.append({'id':id,'group':'G','kind':kind,'geometry':data(g)})
routes={
 'arrival':[external_ports['ENTRY'],[515,419],[465,419]],
 'A':[[357,291],ports['A'],[322,290]],
 'B':[[477,319],ports['B'],[516,305]],
 'C':[[372,429],ports['C'],[375,464]],
 'operations':[external_ports['SERVICE'],[424,555],[315,550],service_port],
 'garden':[[407,423],garden_port]
}
# Check authored route centre lines against the closed plan and furniture.
for o in openings:
 if o['id'] in ['T-A','T-C','GARDEN','S-ACCESS']:o['kind']='proposed sliding door; clear width unverified'
obstacles=unary_union([Polygon(f['geometry'][0]['outer']) for f in furniture])
for key,pts in routes.items():
 l=LineString(pts);assert floor.buffer(.05).covers(l),(key,'outside floor')
 assert l.intersection(obstacles).length<.01,(key,'furniture conflict')
assert floor.buffer(.05).covers(loop),'loop outside floor'
assert loop.intersection(obstacles).length<.01

raw={'A':A,'B':{'id':'B','name':'Overlap / Selective Subtraction','translations':TB,'regions':{k:data(p) for k,p in pb.items()},'pairs':{k:data(p) for k,p in pairs.items()},'overlap':data(overlap),'triple_overlap':data(pb['A'].intersection(pb['B']).intersection(pb['C'])),'envelope':data(env),'full_subtraction':data(full_subtraction),'void':data(void),'shared':data(shared),'floor':data(floor),'forecourt':data(forecourt),'exclusive':{k:data(p) for k,p in exclusive.items()},'retained_band_U':retained_band/U,'court_simplification_U':5/U,'rooms':rooms,'routes':routes,'interfaces':interfaces,'ports':ports,'walls':walls,'openings':openings,'furniture':furniture,'loop':list(loop.coords),'external_ports':external_ports,'service_port':service_port,'garden_port':garden_port}}
for key,m in raw.items():
 e=aenv if key=='A' else env;v=acourt if key=='A' else void;f=afloor if key=='A' else floor;sh=central.difference(acourt) if key=='A' else shared
 m['metrics']={'enclosed_floor_U2':f.area/U**2,'open_court_U2':v.area/U**2,'shared_floor_U2':sh.area/U**2,'envelope_U2':e.area/U**2,'court_boundary_U':v.length/U,'floor_components':count(f)}
result={'title':'Fruchter House — Courtyard Expansion and Overlap Subtraction','original':BASE,'U':U,'angles':angles,'units':'Source drawing coordinates; U is original A inward-edge length. No real metre scale. All new boundaries and programme assignments are proposals.','alternatives':raw,'selected':'B','concept':'Rotation changes facing relationships. Expansion makes an external common court. Overlap creates actual double-counted footprint; full subtraction fails connectivity, selective core subtraction preserves an indoor gallery. The southeast forecourt provides the expanded exterior counterpart.','reference_reading':['Reference 1: shared outdoor field between independent wings; do not copy site orientation.','Reference 2: crossing directions generate differentiated voids, not arbitrary decorative polygons.','Reference 3: preserve corner identity while allowing cross-connections.','Reference 4: rotating volumes, actual atria and shared indoor connectors work together; translate process, not campus scale.'],'hearth_status':'Original triangular hearth shown only as a source reference in process diagrams; its location/use is not fixed in the selected non-residential design.'}
(J/'design/study.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('Metrics',json.dumps({k:v['metrics'] for k,v in raw.items()},indent=2))
print('full subtraction components',count(full_subtraction),'selected voids',len(data(void)))
print('ports',ports,external_ports,'service',service_port)
print('furniture outside',[(f['id'],Polygon(f['geometry'][0]['outer']).difference((shared if f['group']=='G' else exclusive[f['group']])).area) for f in furniture])
