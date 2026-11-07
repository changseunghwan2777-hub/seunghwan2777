"""Create a layered 2D Rhino model. u is an abstract study unit, not metres."""
from selected import *
from hatching import hatch
import rhino3dm as rh
case=C;model=rh.File3dm();model.Settings.ModelUnitSystem=getattr(rh.UnitSystem, 'None')
model.Strings['study_units']='Relative u; no metric conversion established'
model.Strings['source']='M4 normalized Fruchter study; proposed shared office repetition'
counts={}
def layer(name,color):
 l=rh.Layer();l.Name=name;l.Color=(*color,255);idx=model.Layers.Add(l);counts[name]=0;return idx

def curve(points,idx):
 pts=[rh.Point3d(float(x),float(y),0) for x,y in points]
 if len(pts)<2:return
 a=rh.ObjectAttributes();a.LayerIndex=idx;model.Objects.AddCurve(rh.PolylineCurve(pts),a);counts[model.Layers[idx].Name]+=1

def geom(g,idx):
 for p in polys(g):
  curve(p.exterior.coords,idx)
  for ring in p.interiors:curve(ring.coords,idx)
 for l in lines(g):curve(l.coords,idx)
for k in ['A','B','C']:
 idx=layer('01_Wing_'+k,(140,140,140))
 for u in case['units']:geom(u['wings'][k],idx)
for name,g,color in [('02_Built_floor',case['floor'],(20,20,20)),('03_Module_courts',case['courts'],(100,100,100)),('04_Interstitial_courts',case['holes'],(160,160,160)),('05_Intermodule_overlap',case['overlap'],(166,91,62)),('06_Triple_shared_nodes',case['triples'],(167,55,50)),('07_Motif_boundaries',unary_union([u['envelope'].boundary for u in case['units']]),(167,55,50))]:geom(g,layer(name,color))
for k in ['A','B','C']:
 idx=layer('08_Hatch_'+k,(60,60,60))
 for h in hatch(case):
  if h['kind']==k:curve(h['pts'],idx)
idx=layer('09_Local_pivots',(167,55,50))
for u in case['units']:
 x,y=u['pivot'];curve([(x-.05,y),(x+.05,y)],idx);curve([(x,y-.05),(x,y+.05)],idx)
p=J/'output/Moving_Centres_2D.3dm';assert model.Write(str(p),8);r=rh.File3dm.Read(str(p));assert r and len(r.Objects)==sum(counts.values());(J/'review/rhino-roundtrip.json').write_text(json.dumps(dict(objects=len(r.Objects),layers=counts,units='None / relative u',z='all 0; 2D model',desktop_tested=False),indent=2));print('Rhino objects',len(r.Objects))
