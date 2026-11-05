from pathlib import Path
import json
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
J=Path(__file__).resolve().parents[1];S=json.loads((J/'design/study.json').read_text());B=S['alternatives']['B']
def geom(gs):return unary_union([Polygon(g['outer'],g.get('holes',[])) for g in gs])
checks={}
for k in 'AB':
 m=S['alternatives'][k];f=geom(m['floor']);v=geom(m['void']);e=geom(m['envelope']);assert all(p.is_valid for p in [f,v,e]);assert f.geom_type=='Polygon';assert f.intersection(v).area<.001;assert f.union(v).symmetric_difference(e).area<.01
checks['valid_connected_floor_and_courtyard_partition']=True
assert len(B['full_subtraction'])==3;checks['full_subtraction_components']=3
obs=geom([g for f in B['furniture'] for g in f['geometry']]);floor=geom(B['floor'])
for f in B['furniture']:
 area=geom(B['shared'] if f['group']=='G' else B['exclusive'][f['group']]);assert area.buffer(.001).covers(geom(f['geometry']))
checks['furniture_within_assigned_areas']=len(B['furniture'])
for key,ps in {'loop':B['loop'],**B['routes']}.items():
 line=LineString(ps);assert floor.buffer(.05).covers(line);assert line.intersection(obs).is_empty
 for w in B['walls']:
  if w['kind']!='open':assert line.intersection(LineString([w['a'],w['b']])).is_empty,(key,w['id'])
checks['routes_not_crossing_walls_furniture_or_void']=True
checks['scope']='Centre lines only, not code clear widths, evacuation or structural validation.'
checks['area_metrics']={k:v['metrics'] for k,v in S['alternatives'].items()}
(J/'review/geometry-checks.json').write_text(json.dumps(checks,indent=2));print('Geometry checks passed')
