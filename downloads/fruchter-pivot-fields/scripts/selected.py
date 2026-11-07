from fields import *
C=build_field('COUNTER',1.)
# Persist the exact rigid transforms and measured overlaps for every output.
if __name__=='__main__':
 (J/'design/selected.json').write_text(json.dumps(serial(C)))
 for u in C['units']:print(u['id'],[round(v,3) for v in [u['x'],u['y'],u['angle']]])
 print('intruded',[(u['id'],round(u['court'].intersection(unary_union([v['envelope'] for v in C['units'] if v is not u])).area,6)) for u in C['units'] if u['court'].intersection(unary_union([v['envelope'] for v in C['units'] if v is not u])).area>1e-6])
