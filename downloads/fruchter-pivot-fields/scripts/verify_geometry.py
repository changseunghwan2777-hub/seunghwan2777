from selected import *
from hatching import hatch
import csv
checks={}
checks['twenty_units']=len(C['units'])==20
checks['unique_pivots']=len({tuple(u['pivot']) for u in C['units']})==20
checks['unique_angles']=len({round(u['angle'],5) for u in C['units']})==20
checks['rigid_envelope_areas']=all(abs(u['envelope'].area-ENVELOPE.area)<1e-7 for u in C['units'])
checks['rigid_wing_areas']=all(abs(g.area-BASE[k].area)<1e-7 for u in C['units'] for k,g in u['wings'].items())
checks['valid_floor']=C['floor'].is_valid
checks['protected_courts']=C['floor'].intersection(C['courts']).area<1e-8
checks['one_floor_component']=components(C['floor'])==1
checks['one_primary_contact_graph']=C['metrics']['usable_graph_components']==1
checks['one_component_after_004u_inset']=components(C['floor'].buffer(-.04))==1
checks['all_hatch_inside_floor']=all(C['floor'].buffer(1e-7).covers(LineString(h['pts'])) for h in hatch(C))
checks['each_unit_floor_connected']=all(components(u['floor'])==1 for u in C['units'])
assert all(checks.values()),checks
(J/'review/geometry-checks.json').write_text(json.dumps(dict(checks=checks,metrics=C['metrics']),indent=2))
with (J/'design/pivots-and-angles.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['module','initial_x_u','initial_y_u','pivot_x_u','pivot_y_u','angle_degrees'])
 for u in C['units']:w.writerow([u['id'],*u['q'],*u['pivot'],u['angle']])
print(checks)
