from geometry import *
import numpy as np

def make_units(family,amount=1.,d=1.60,cols=5,rows=4):
 units=[]
 for j in range(rows):
  for i in range(cols):
   qx=d*(i+(j%2)/2-2.25);qy=d*math.sqrt(3)/2*(j-1.5)
   if family=='FAN':
    R=9/amount;t=qx/R
    x=(R+qy)*math.sin(t);y=(R+qy)*math.cos(t)-R;a=-math.degrees(t)
   elif family=='COUNTER':
    x,y=qx,qy;angle=0
    for fx,sign in [(-2.4,1),(2.4,-1)]:
     dx,dy=qx-fx,qy;weight=math.exp(-(dx*dx+dy*dy)/(2*2.5**2));t=math.radians(44*amount*sign*weight)
     x+=.62*(dx*math.cos(t)-dy*math.sin(t)-dx);y+=.62*(dx*math.sin(t)+dy*math.cos(t)-dy);angle+=math.degrees(t)
    a=angle+amount*6*qy
   elif family=='STREAM':
    A=.62*amount;k=.62;phase=.38*qy
    x=qx+.22*amount*math.sin(.7*qy+.3*qx)
    y=qy+A*math.sin(k*qx+phase)
    a=math.degrees(math.atan(A*k*math.cos(k*qx+phase)))+amount*9*qy
   elif family=='BASE':x,y,a=qx,qy,0
   units.append(dict(id=f'{j+1}{i+1}',i=i,j=j,q=[qx,qy],x=x,y=y,angle=a,pivot=[x,y],envelope=tf(ENVELOPE,x,y,a),court=tf(COURT,x,y,a),wings={k:tf(g,x,y,a) for k,g in BASE.items()}))
 return units

def evaluate(units,family,amount,d):
 courts=unary_union([u['court'] for u in units]);envelope=unary_union([u['envelope'] for u in units]);floor=envelope.difference(courts)
 for u in units:u['floor']=u['envelope'].difference(courts)
 contacts=[]
 for a,b in itertools.combinations(units,2):
  g=a['floor'].intersection(b['floor'])
  if g.area>1e-6:
   dia=max((maximum_inscribed_circle(p,tolerance=.001).length*2 for p in polys(g)),default=0)
   contacts.append(dict(a=a['id'],b=b['id'],geometry=g,area=g.area,diameter=dia,delta_angle=abs((a['angle']-b['angle']+60)%120-60),usable=dia>=.18))
 overlap=unary_union([c['geometry'] for c in contacts]);triples=unary_union([a['floor'].intersection(b['floor']).intersection(c['floor']) for a,b,c in itertools.combinations(units,3)])
 holes=unary_union([Polygon(r) for p in polys(envelope) for r in p.interiors]).difference(courts)
 intrusion=sum(unary_union([v['envelope'] for v in units if v is not u]).intersection(u['court']).area for u in units)
 parent={u['id']:u['id'] for u in units}
 def root(x):
  while parent[x]!=x:x=parent[x]
  return x
 for c in contacts:
  if c['usable']:parent[root(c['a'])]=root(c['b'])
 diam=[c['diameter'] for c in contacts];areas=[c['area'] for c in contacts]
 return dict(id=f'{family}-{amount:.2f}',family=family,amount=amount,d=d,units=units,courts=courts,envelope=envelope,floor=floor,overlap=overlap,triples=triples,holes=holes,contacts=contacts,metrics=dict(area=floor.area,overlap_pct=100*overlap.area/floor.area,components=components(floor),inset_components=components(floor.buffer(-.04)),usable_graph_components=len(set(root(x) for x in parent)),contacts=len(contacts),usable_contacts=sum(c['usable'] for c in contacts),min_diameter=min(diam),max_diameter=max(diam),area_cv=float(np.std(areas)/np.mean(areas)),courts=components(courts),natural_voids=components(holes),court_intrusion=intrusion,min_angle=min(u['angle'] for u in units),max_angle=max(u['angle'] for u in units)))

def build_field(family,amount=1.,d=1.60):return evaluate(make_units(family,amount,d),family,amount,d)
if __name__=='__main__':
 cases=[build_field(f,a) for f in ['FAN','COUNTER','STREAM'] for a in [.65,1,1.35]]
 for c in cases:print(c['id'],{k:round(v,3) if isinstance(v,float) else v for k,v in c['metrics'].items()})
 (J/'design/cases.json').write_text(json.dumps(serial(cases)))
