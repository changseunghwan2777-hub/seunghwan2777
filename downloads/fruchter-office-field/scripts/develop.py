from geometry import *
import heapq
SELECTED=build('STAGGER',1.65)
def visibility_path(domain,start,end):
 vertices=[start,end]+[tuple(q) for p in polys(domain) for ring in [p.exterior,*p.interiors] for q in list(ring.coords)[:-1]]
 allowed=domain.buffer(1e-8);adj=[[] for _ in vertices]
 for i,a in enumerate(vertices):
  for j in range(i):
   b=vertices[j];l=LineString([a,b])
   if allowed.covers(l):adj[i].append((j,l.length));adj[j].append((i,l.length))
 dist={0:0};prev={};q=[(0,0)]
 while q:
  d,i=heapq.heappop(q)
  if i==1:break
  if d>dist[i]:continue
  for j,w in adj[i]:
   v=d+w
   if v<dist.get(j,1e20):dist[j]=v;prev[j]=i;heapq.heappush(q,(v,j))
 if 1 not in dist:raise ValueError('Disconnected route')
 route=[1]
 while route[-1]!=0:route.append(prev[route[-1]])
 return LineString([vertices[i] for i in route[::-1]])
def develop(case):
 # A 0.06u inset is a comparative design allowance, not a regulatory width.
 domains={u['id']:u['floor'].buffer(-.06,join_style=2) for u in case['units']}
 anchors={u['id']:[] for u in case['units']};nodes=[]
 for c in case['contacts']:
  available=c['geometry'].intersection(domains[c['a']]).intersection(domains[c['b']])
  p=maximum_inscribed_circle(available,tolerance=.001).coords[0]
  anchors[c['a']].append(p);anchors[c['b']].append(p);nodes.append(p)
 work=[]
 for u in case['units']:
  for k,g in u['wings'].items():
   private=g.difference(case['overlap']).difference(case['courts']).buffer(-.08,join_style=2)
   if private.is_empty:continue
   for p in polys(private):
    if p.area<.025:continue
    pt=maximum_inscribed_circle(p,tolerance=.001).coords[0]
    if domains[u['id']].covers(Point(pt)):anchors[u['id']].append(pt);work.append(dict(unit=u['id'],wing=k,geometry=p,point=pt,angle=M['angles'][k]+u['angle']))
 # One perimeter entry per row at the left edge; entries are hypotheses.
 entries=[]
 for row in range(3):
  u=next(u for u in case['units'] if u['i']==0 and u['j']==row)
  p=min(list(u['envelope'].exterior.coords),key=lambda q:q[0]);p=Point(p)
  # Use left wing exterior midpoint to avoid corner entrances.
  boundary=list(u['wings']['A'].exterior.coords);edges=[LineString([a,b]) for a,b in zip(boundary,boundary[1:])]
  edge=min(edges,key=lambda e:e.centroid.x);outer=edge.interpolate(.5,normalized=True)
  from shapely.ops import nearest_points
  inner=nearest_points(domains[u['id']],outer)[0];anchors[u['id']].append(tuple(inner.coords[0]));entries.append((tuple(outer.coords[0]),tuple(inner.coords[0])))
 routes=[]
 for uid,points in anchors.items():
  # Connect targets by a minimum spanning tree of valid within-floor shortest paths.
  cand=[]
  for i,a in enumerate(points):
   for j in range(i):
    r=visibility_path(domains[uid],a,points[j]);cand.append((r.length,i,j,r))
  parents=list(range(len(points)))
  def root(i):
   while parents[i]!=i:i=parents[i]
   return i
  for _,i,j,r in sorted(cand,key=lambda x:x[0]):
   a,b=root(i),root(j)
   if a!=b:parents[a]=b;routes.append(r)
 routes.extend(LineString(e) for e in entries)
 network=unary_union(routes);corridor=network.buffer(.055,join_style=2).intersection(case['floor'])
 assert case['floor'].buffer(1e-7).covers(network)
 case.update(routes=network,corridor=corridor,work=work,entries=entries,nodes=nodes)
 # Route graph should be physically connected, including links across shared nodes.
 case['metrics']['route_components']=components(network.buffer(.00001))
 assert case['metrics']['route_components']==1,case['metrics']
 return case
if __name__=='__main__':
 case=develop(SELECTED);(J/'design/selected.json').write_text(json.dumps(serial(case)));print(case['metrics'])
