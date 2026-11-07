"""Repeated M4 motif; all lengths in relative u, not metres."""
from pathlib import Path
import json, math, itertools
from shapely.geometry import Polygon, LineString, Point, box, mapping
from shapely.ops import unary_union
from shapely.affinity import rotate,translate
from shapely import maximum_inscribed_circle
J=Path(__file__).resolve().parents[1]
SOURCE=json.loads((J/'design/source-study.json').read_text())
M=next(m for m in SOURCE['models'] if m['id']=='M4')
def decode(ps):return unary_union([Polygon(p['outer'],p.get('holes',[])) for p in ps])
BASE={k:decode(v) for k,v in M['regions'].items()}
COURT=decode(M['triple']);ENVELOPE=decode(M['envelope'])
def polys(g):
 if g.is_empty:return []
 if g.geom_type=='Polygon':return [g]
 return [p for a in getattr(g,'geoms',[]) for p in polys(a)]
def lines(g):
 if g.is_empty:return []
 if g.geom_type in ['LineString','LinearRing']:return [g]
 return [p for a in getattr(g,'geoms',[]) for p in lines(a)]
def tf(g,x,y,a):return translate(rotate(g,a,origin=(0,0)),x,y)
def components(g):return len(polys(g))
def build(family,d,cols=4,rows=3):
 units=[]
 for j in range(rows):
  for i in range(cols):
   x=d*(i+(j%2)/2 if family!='GRID' else i)
   y=d*j*(math.sqrt(3)/2 if family!='GRID' else 1)
   a=60*((i+j)%2) if family=='ALTERNATE' else 0
   units.append(dict(id=f'{j+1}{i+1}',i=i,j=j,x=x,y=y,angle=a,envelope=tf(ENVELOPE,x,y,a),court=tf(COURT,x,y,a),wings={k:tf(g,x,y,a) for k,g in BASE.items()}))
 courts=unary_union([u['court'] for u in units]);envelope=unary_union([u['envelope'] for u in units]);floor=envelope.difference(courts)
 for u in units:u['floor']=u['envelope'].difference(courts)
 contacts=[]
 for a,b in itertools.combinations(units,2):
  g=a['floor'].intersection(b['floor'])
  if g.area>1e-7:
   dia=max((maximum_inscribed_circle(p,tolerance=.0005).length*2 for p in polys(g)),default=0)
   contacts.append(dict(a=a['id'],b=b['id'],geometry=g,area=g.area,diameter=dia))
 overlap=unary_union([c['geometry'] for c in contacts])
 triples=unary_union([a['floor'].intersection(b['floor']).intersection(c['floor']) for a,b,c in itertools.combinations(units,3)])
 # These are natural interstitial holes, distinct from designated motif courts.
 holes=unary_union([Polygon(r) for p in polys(envelope) for r in p.interiors]).difference(courts)
 intrusion=sum(unary_union([v['envelope'] for v in units if v is not u]).intersection(u['court']).area for u in units)
 return dict(id=f'{family}-{d:.2f}',family=family,d=d,units=units,courts=courts,envelope=envelope,floor=floor,overlap=overlap,triples=triples,holes=holes,contacts=contacts,metrics=dict(area=floor.area,overlap=overlap.area,overlap_pct=100*overlap.area/floor.area,triple=triples.area,components=components(floor),inset_components=components(floor.buffer(-.04)),contacts=len(contacts),min_contact_diameter=min((c['diameter'] for c in contacts),default=0),courts=components(courts),natural_voids=components(holes),court_intrusion_before_cut=intrusion))
def serial(o):
 if hasattr(o,'geom_type'):return mapping(o)
 if isinstance(o,dict):return {k:serial(v) for k,v in o.items()}
 if isinstance(o,list):return [serial(v) for v in o]
 return o
if __name__=='__main__':
 cases=[build(f,d) for f in ['GRID','STAGGER','ALTERNATE'] for d in [1.45,1.65,1.85]]
 for x in cases:print(x['id'],{k:round(v,3) if isinstance(v,float) else v for k,v in x['metrics'].items()})
 (J/'design/cases.json').write_text(json.dumps(serial(cases)))
