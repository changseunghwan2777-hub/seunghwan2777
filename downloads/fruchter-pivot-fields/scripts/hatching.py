from selected import *
from draw import fit
import random

def hatch(case,spacing=.013,seed=42):
 rng=random.Random(seed);out=[]
 for u in case['units']:
  for k,g in u['wings'].items():
   a=M['angles'][k]+u['angle'];local=rotate(g.intersection(case['floor']),-a,origin=(0,0));a0,b0,a1,b1=local.bounds
   y=math.floor(b0/spacing)*spacing
   n=0
   while y<=b1:
    yy=y+rng.uniform(-spacing*.08,spacing*.08)
    segment=LineString([(a0-.1,yy),(a1+.1,yy)]).intersection(local)
    for l in lines(segment):
     if l.length<.003:continue
     l=rotate(l,a,origin=(0,0));out.append(dict(pts=list(l.coords),kind=k,unit=u['id'],weight=.85+rng.random()*.3,index=n))
    y+=spacing;n+=1
 return out

def make_viewer(case):
 T=fit(case['floor'],40,32,514,356);data=[dict(pts=[[2*x,2*y] for x,y in map(T,p['pts'])],kind=p['kind'],index=p['index']) for p in hatch(case)]
 for polygon in polys(case['overlap']):
  for ring in [polygon.exterior,*polygon.interiors]:
   data.append(dict(pts=[[2*x,2*y] for x,y in map(T,ring.coords)],kind='overlap_boundary',index=0,closed=True))
 template=(J/'assets/Pardesco-viewer-template.html').read_text()
 start=template.index('const ART = {');end=template.index('/*',template.index('\n};',start)+3)
 art='''const ART = {
 title:'Moving Centres / directional graphite', subtitle:'M4 · 20 independent pivots · counter-rotation field / seed changes marks only',
 width:1188,height:840,mm:[594,420],paper:'#ffffff',ink:'#242424',lineWidth:0.40,
 params:{seed:{value:42,min:1,max:99999,step:1},density:{value:1,min:1,max:3,step:1,label:'Line stride (1 = dense)'},weight:{value:0.40,min:0.12,max:0.5,step:0.02,label:'Stroke weight'}},
 data: DATA,
 paths(p,rng){return this.data.filter(q=>q.index%p.density===0).map(q=>{if(q.closed)return q;const [a,b]=q.pts,t=rng()*0.018;return {kind:q.kind,pts:[[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t],[b[0]-(b[0]-a[0])*t,b[1]-(b[1]-a[1])*t]]};});},
 render(ctx,p,rng,noise,t,env){ctx.fillStyle='#fff';ctx.fillRect(0,0,1188,840);ctx.strokeStyle='#242424';ctx.lineCap='butt';for(const q of this.paths(p,rng)){ctx.lineWidth=q.closed?p.weight*.45:p.weight*(.85+rng()*.3);ctx.beginPath();ctx.moveTo(...q.pts[0]);for(const pt of q.pts.slice(1))ctx.lineTo(...pt);if(q.closed)ctx.closePath();ctx.stroke();}}
};
'''.replace('DATA',json.dumps(data,separators=(',',':')))
 out=template[:start]+art+template[end:]
 out=out.replace('stroke-width="0.1" stroke-linecap="round"', 'stroke-width="${p.weight * (ART.mm?.[0] || AW) / AW}" stroke-linecap="round"')
 out=out.replace('${p.weight * (ART.mm?.[0] || AW) / AW}', "${(kind === 'overlap_boundary' ? .45 : 1) * p.weight * (ART.mm?.[0] || AW) / AW}")
 (J/'output/Directional_Hatch_Studio.html').write_text(out)
 (J/'design/hatch-paths.json').write_text(json.dumps(hatch(case)))
 print('Hatch segments',len(data))
if __name__=='__main__':make_viewer(C)
