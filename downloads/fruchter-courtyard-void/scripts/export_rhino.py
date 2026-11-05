"""Build an editable 2D Rhino file. Relative U coordinates, no invented height.
Parameters: selected geometry comes from design/study.json. To change the design,
edit angles/translations/retained_band in design.py and regenerate all outputs.
"""
from pathlib import Path
import json,rhino3dm as r
J=Path(__file__).resolve().parents[1];S=json.loads((J/'design/study.json').read_text());U=S['U']
f=r.File3dm();f.Settings.ModelUnitSystem=getattr(r.UnitSystem,'None');f.Settings.ModelAbsoluteTolerance=.00001
f.Strings['units']='Relative U: original A inward-edge length. All geometry at Z=0. Not a 3D building model.'
f.Strings['scope']='Proposed reconstruction; no real height, structure or metric scale is asserted.'
colors={'original':(130,140,140,255),'wings':(80,90,90,255),'shared':(188,107,63,255),'void':(68,132,108,255),'walls':(35,45,48,255),'glazing':(71,124,160,255),'furniture':(100,110,105,255),'flows':(188,107,63,255),'forecourt':(68,132,108,255)}
layers={}
def addline(ps,name,kind,offset=0,closed=False):
 lname=name+'_'+kind
 if lname not in layers:
  lay=r.Layer();lay.Name=lname;lay.Color=colors.get(kind,colors['wings']);layers[lname]=f.Layers.Add(lay)
 pts=[r.Point3d(p[0]/U+offset,-p[1]/U,0) for p in ps]
 if closed and pts[0]!=pts[-1]:pts.append(pts[0])
 attr=r.ObjectAttributes();attr.LayerIndex=layers[lname];attr.Name=lname;attr.SetUserString('source','study.json');attr.SetUserString('units','U relative; no metric scale')
 f.Objects.AddCurve(r.PolylineCurve(pts),attr)
def shapes(gs,name,kind,offset):
 for g in gs:
  addline(g['outer'],name,kind,offset,True)
  for h in g.get('holes',[]):addline(h,name,kind,offset,True)
for k,ps in S['original']['regions'].items():addline(ps,'01_Original_'+k,'original',0,True)
A=S['alternatives']['A'];B=S['alternatives']['B']
for k,gs in A['regions'].items():shapes(gs,'02_Expanded_'+k,'wings',5)
for key in ['shared','void']:shapes(A[key],'02_Expanded',key,5)
for k,gs in B['regions'].items():shapes(gs,'03_Overlap_'+k,'wings',10)
shapes(B['overlap'],'03_Overlap','shared',10)
for key in ['shared','void','forecourt']:shapes(B[key],'04_Selected',key,15)
for w in B['walls']:
 if w['kind']!='open':addline([w['a'],w['b']],'04_Selected', 'glazing' if w['kind']=='glazing' else 'walls',15)
for g in B['furniture']:shapes(g['geometry'],'04_Selected_'+g['id'],'furniture',15)
for ps in [B['loop']]+list(B['routes'].values()):addline(ps,'04_Selected','flows',15)
path=J/'output/Fruchter_Courtyard_Editable_2D.3dm';assert f.Write(str(path),8)
reread=r.File3dm.Read(str(path));assert len(reread.Objects)==len(f.Objects)
assert all(ob.Geometry.IsValid for ob in reread.Objects)
report={'format':'Rhino 3DM v8','objects':len(reread.Objects),'layers':len(reread.Layers),'all_curves_valid':True,'roundtrip_read':True,'units':'U / no metric scale','all_geometry':'2D at Z=0','Rhino_desktop_tested':False}
(J/'review/rhino-file-checks.json').write_text(json.dumps(report,indent=2));print(report)
