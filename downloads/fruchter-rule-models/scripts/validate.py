from pathlib import Path
import json,math,xml.etree.ElementTree as ET
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union
from shapely.affinity import rotate
from graphics import FM
J=Path(__file__).resolve().parents[1];S=json.loads((J/'design/study.json').read_text())
def g(gs):return unary_union([Polygon(x['outer'],x.get('holes',[])) for x in gs])
report={'area_partition':{},'symmetry':{},'void_policy_components':{}}
for m in S['models']+S['parameter_grid']+[S['original_outline_check']]:
 one=sum(g(z).area for z in m['single'].values());two=sum(g(z).area for z in m['double'].values());three=g(m['triple']).area;union=g(m['envelope']);floor=g(m['floor']);sum_area=sum(g(z).area for z in m['regions'].values())
 assert union.is_valid and floor.is_valid
 assert abs(one+2*two+3*three-sum_area)<1e-6
 assert abs(one+two+three-union.area)<1e-6
 assert abs(floor.area-(one+two))<1e-6
 report['area_partition'][m['id']]=True
for m in S['models'][2:]:
 error=g(m['floor']).symmetric_difference(rotate(g(m['floor']),120,origin=(0,0))).area;assert error<1e-6;report['symmetry'][m['id']]=error
m=S['models'][3]
for a,b in [('AB','BC'),('BC','CA'),('CA','AB')]:assert g(m['double'][b]).symmetric_difference(rotate(g(m['double'][a]),-120,origin=(0,0))).area<1e-6
for p,expected in zip(S['void_policies'],[1,3,4,1]):assert p['components']==expected;report['void_policy_components'][p['id']]=expected
plan=S['plan'];floor=g(plan['floor']);furn=unary_union([g(f['geometry']) for f in plan['furniture']]);wall=unary_union([LineString([w['a'],w['b']]) for w in plan['walls']]);assert floor.buffer(-1e-6).geom_type=='Polygon'
for ps in plan['routes'].values():
 line=LineString(ps);assert floor.buffer(1e-6).covers(line);assert line.intersection(furn).is_empty;assert line.intersection(wall).is_empty
for f in plan['furniture']:
 region=m['double'][f['room'][1:]] if f['room'].startswith('J') else m['single'][f['room']];assert g(region).buffer(1e-7).covers(g(f['geometry']))
report['route_centre_lines_no_wall_furniture_or_void_crossing']=True
report['furniture_in_assigned_regions']=len(plan['furniture'])
# The claimed arrival sequence is checked as an ordered segment, not just length.
a=math.radians(m['angles']['A']);c=m['centres']['A'];axis=LineString([(c[0]+v*math.cos(a),c[1]+v*math.sin(a)) for v in [.625,-.625]])
j=axis.intersection(g(m['double']['AB']));t=axis.intersection(g(m['triple']));jmin=min(axis.project(Point(p)) for p in j.coords);tmin=min(axis.project(Point(p)) for p in t.coords);assert jmin<tmin
report['twofold_before_triple_on_module_axis']={'start_joint':jmin,'start_triple':tmin,'joint_segment':j.length}
missing=[]
stems=['01_Overlap_Model_Families_A2','02_Parameter_Selection_A2','03_Void_Policy_And_Lineage_A2','04_Overlap_Development_A2','05_Selected_Model_Plan_A2']
for stem in stems:
 root=ET.parse(J/'output'/(stem+'.svg')).getroot()
 for node in root.iter('{http://www.w3.org/2000/svg}text'):
  font=node.get('data-font','KR')
  for char in node.text or '':
   if ord(char) not in FM[font]['cmap']:missing.append([stem,char,font])
assert not missing,missing
report['no_missing_svg_font_glyphs']=True
report['scope']='Geometry, positive-area topology with 1e-6 u probe, route centre lines and glyph coverage only. No code, structure, effective clear widths, daylight or real site validation.'
(J/'review/geometry-checks.json').write_text(json.dumps(report,indent=2));print('Geometry and glyph checks passed')
