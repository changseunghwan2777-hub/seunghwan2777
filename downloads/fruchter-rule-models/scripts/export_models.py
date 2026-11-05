"""Native Rhino + OBJ schematic models. Height is a declared diagram assumption."""
from pathlib import Path
import json
import rhino3dm as r
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from shapely import constrained_delaunay_triangles
J=Path(__file__).resolve().parents[1];S=json.loads((J/'design/study.json').read_text());H=.55
file=r.File3dm();file.Settings.ModelUnitSystem=getattr(r.UnitSystem,'None');file.Settings.ModelAbsoluteTolerance=1e-7
file.Strings['units']='Relative u, not metres; u = sqrt(original summed traced ABC area / 3).'
file.Strings['height']='0.55 u uniform schematic massing assumption. Not an existing height or a resolved structure.'
file.Strings['layout']='Five massing models arranged along X with 4 u spacing. Selected M4 at x=12 u. 2D drawings aligned below at y=-4 u.'
layers={}
def layer(name,color):
 if name not in layers:
  l=r.Layer();l.Name=name;l.Color=color;layers[name]=file.Layers.Add(l)
 return layers[name]
def attr(name,color):
 a=r.ObjectAttributes();a.LayerIndex=layer(name,color);a.Name=name;return a
def curve(ps,name,color,offset=(0,0),z=0,closed=True):
 pts=[r.Point3d(x+offset[0],y+offset[1],z) for x,y in ps]
 if closed and pts[0]!=pts[-1]:pts.append(pts[0])
 file.Objects.AddCurve(r.PolylineCurve(pts),attr(name,color))
def extrude(poly,offset=(0,0)):
 p=orient(poly,1);mesh=r.Mesh();idx={};verts=[];faces=[]
 def v(x,y,z):
  key=(round(x+offset[0],9),round(y+offset[1],9),round(z,9))
  if key not in idx:idx[key]=len(verts);verts.append(key);mesh.Vertices.Add(*key)
  return idx[key]
 for tri in constrained_delaunay_triangles(p).geoms:
  xy=list(orient(tri,1).exterior.coords)[:3]
  top=[v(x,y,H) for x,y in xy];bot=[v(x,y,0) for x,y in reversed(xy)]
  mesh.Faces.AddFace(*top);mesh.Faces.AddFace(*bot);faces.extend([top,bot])
 for ring in [p.exterior]+list(p.interiors):
  coords=list(ring.coords)
  for (x1,y1),(x2,y2) in zip(coords[:-1],coords[1:]):
   q=[v(x1,y1,0),v(x2,y2,0),v(x2,y2,H),v(x1,y1,H)];mesh.Faces.AddFace(*q);faces.append(q)
 mesh.Normals.ComputeNormals();mesh.Compact();assert mesh.IsValid and mesh.IsClosed
 return mesh,verts,faces
reports=[]
for i,m in enumerate(S['models']):
 dx=i*4;name=m['id']+'_'+m['name'].replace(' ','_')
 for g in m['floor']:
  mesh,_,_=extrude(Polygon(g['outer'],g['holes']),(dx,0));file.Objects.AddMesh(mesh,attr(name+'_Solid',(210,217,214,255)));reports.append({'model':m['id'],'closed_mesh':bool(mesh.IsClosed),'faces':len(mesh.Faces),'vertices':len(mesh.Vertices)})
 for k,gs in m['regions'].items():
  for g in gs:curve(g['outer'],name+'_Module_Guides',(125,135,133,255),(dx,0),H+.002)
 for k,gs in m['double'].items():
  for g in gs:curve(g['outer'],name+'_Double_'+k,(188,107,63,255),(dx,0),H+.004)
 for k,gs in m['regions'].items():
  for g in gs:curve(g['outer'],name+'_Plan_'+k,(80,90,88,255),(dx,-4))
 for g in m['triple']:curve(g['outer'],name+'_Triple_Void',(68,132,108,255),(dx,-4))
 file.Objects.AddTextDot(name,r.Point3d(dx,-1.8,0),attr(name+'_Label',(80,90,88,255)))
# Detailed plan shares the selected model's 2D position.
for w in S['plan']['walls']:curve([w['a'],w['b']],'M4_Plan_'+w['kind'],(71,124,160,255) if w['kind']=='glazing' else (30,40,40,255),(12,-4),closed=False)
for f in S['plan']['furniture']:
 for g in f['geometry']:curve(g['outer'],'M4_Plan_Furniture',(110,120,115,255),(12,-4))
for name,ps in S['plan']['routes'].items():curve(ps,'M4_Plan_Routes',(188,107,63,255),(12,-4),closed=False)
p=J/'output/Fruchter_Rule_Models.3dm';assert file.Write(str(p),8)
check=r.File3dm.Read(str(p));assert len(check.Objects)==len(file.Objects);assert all(o.Geometry.IsValid for o in check.Objects)
selected=S['models'][3]['floor'][0];mesh,vertices,faces=extrude(Polygon(selected['outer'],selected['holes']))
obj=['# M4 schematic solid; coordinates in relative u, height 0.55 u, not metres.','o M4_Selected_Triple_Void']+['v %.9f %.9f %.9f'%v for v in vertices]+['f '+' '.join(str(i+1) for i in face) for face in faces]
(J/'output/M4_Selected_Massing.obj').write_text('\n'.join(obj)+'\n')
report={'models':reports,'native_3dm_roundtrip':True,'native_objects':len(check.Objects),'native_layers':len(check.Layers),'obj_vertices':len(vertices),'obj_faces':len(faces),'height_u':H,'Rhino_desktop_executed':False,'scope':'Closed schematic mass meshes, not resolved walls, glazing or construction.'}
(J/'review/model-checks.json').write_text(json.dumps(report,indent=2));print(report)
