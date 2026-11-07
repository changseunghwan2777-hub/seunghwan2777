from pathlib import Path
import json
J=Path(__file__).resolve().parents[1]
cases=json.loads((J/'design/cases.json').read_text());hatches=json.loads((J/'design/hatch-paths.json').read_text())
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Moving Centres / Fruchter</title><style>
*{box-sizing:border-box}body{margin:0;background:white;color:#222;font:15px/1.6 system-ui,sans-serif}header{padding:24px 32px;border-bottom:1px solid #ddd}h1{font-size:26px;margin:0}p{margin:5px 0;color:#666}main{display:grid;grid-template-columns:285px 1fr;min-height:80vh}aside{padding:24px;border-right:1px solid #ddd}label{display:block;margin-top:18px}select,button{font:inherit;padding:8px;border:1px solid #bbb;background:#fff;width:100%}button{margin-top:25px;cursor:pointer}svg{width:100%;height:auto}#stats{margin-top:24px}small{color:#666}#message{color:#a73732;margin-top:15px} @media(max-width:800px){main{display:block}aside{border-right:0}}
</style><header><h1>Moving Centres — 20 independent pivots</h1><p>세 날개를 하나의 모듈로 유지하고, 모듈 전체의 중심 위치와 각도를 연속적인 규칙으로 바꾼다.</p></header><main><aside>
<label for="family">배열 규칙</label><select id="family"><option value="FAN">부채꼴 / Fan</option><option value="COUNTER" selected>두 기준점 / Counter</option><option value="STREAM">접선 방향 / Stream</option></select>
<label for="amount">변화 강도</label><select id="amount"><option>0.65</option><option selected>1.00</option><option>1.35</option></select>
<label for="mode">표현</label><select id="mode"><option value="overlap">중첩 위계</option><option value="figure">Figure–ground</option><option value="hatch">방향 해치 / 선정안</option></select>
<label><input type="checkbox" id="pivots" checked> 개별 중심과 회전각</label><label><input type="checkbox" id="ghost"> 이동 전 중심 → 현재 중심</label>
<div id="stats"></div><p id="message" role="status"></p><button id="export">현재 도면 SVG 저장</button><p><small>F1/F2는 제어점. 실제 회전축은 20개의 개별 P입니다. u는 상대 단위이며 0.18u 접합 기준은 통로 폭이나 법규 기준이 아닙니다.</small></p></aside><section><svg id="view" viewBox="0 0 594 420" xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" role="img" aria-label="독립 중심과 회전 규칙 비교"></svg></section></main>
<script>__D3__</script><script>
const cases=__CASES__,hatches=__HATCHES__;
const svg=d3.select('#view');svg.append('rect').attr('width',594).attr('height',420).attr('fill','white');
const projection=d3.geoIdentity().reflectY(true).fitExtent([[20,30],[574,390]],{type:'Polygon',coordinates:[[[-5.6,-4.5],[5.6,-4.5],[5.6,4.8],[-5.6,4.8],[-5.6,-4.5]]]});
const path=d3.geoPath(projection),layers={};['floor','overlap','triple','hatch','boundary','ghost','pivot'].forEach(k=>layers[k]=svg.append('g').attr('id','layer-'+k));
function update(){const f=document.querySelector('#family').value,a=+document.querySelector('#amount').value;let mode=document.querySelector('#mode').value;const c=cases.find(x=>x.family===f&&x.amount===a),chosen=c.id==='COUNTER-1.00';if(mode==='hatch'&&!chosen){mode='overlap';document.querySelector('#mode').value=mode;}document.querySelector('#message').textContent=chosen?'선정안 · 개별 중심에 마우스를 올려 회전각 확인':'해치 표현은 발전시킨 선정안에서 제공합니다.';
const bind=(k,data,fill,stroke,width)=>layers[k].selectAll('path').data(data).join('path').attr('d',path).attr('fill',fill).attr('fill-rule','evenodd').attr('stroke',stroke).attr('stroke-width',width);
bind('floor',mode==='hatch'?[]:[c.floor],mode==='figure'?'#111':'#ddd',null,0);bind('overlap',mode==='overlap'?[c.overlap]:[],'#222',null,0);bind('triple',mode==='overlap'?[c.triples]:[],'#a73732',null,0);
bind('hatch',mode==='hatch'?hatches.map(q=>({type:'LineString',coordinates:q.pts})):[],'none','#242424',.16);bind('boundary',mode==='hatch'?[c.overlap]:[],'none','#444',.08);
bind('ghost',document.querySelector('#ghost').checked?c.units.map(u=>({type:'LineString',coordinates:[u.q,u.pivot]})):[],'none','#a73732',.3);
const ps=document.querySelector('#pivots').checked?c.units:[];const groups=layers.pivot.selectAll('g').data(ps,d=>d.id).join(enter=>{const g=enter.append('g');g.append('circle');g.append('text');g.append('title');return g;}).attr('transform',d=>`translate(${projection(d.pivot).join(',')})`);
groups.select('circle').attr('r',.8).attr('fill','#a73732');groups.select('text').attr('y',3.4).attr('font-size',2.7).attr('font-family','sans-serif').attr('text-anchor','middle').attr('fill','#a73732').text(d=>`${d.id} / ${d.angle.toFixed(1)}°`);groups.select('title').text(d=>`Module ${d.id}: P=(${d.x.toFixed(3)},${d.y.toFixed(3)})u; θ=${d.angle.toFixed(2)}°`);
const m=c.metrics;d3.select('#stats').html(`<strong>${c.id}</strong><br>각도 ${m.min_angle.toFixed(1)}° ~ ${m.max_angle.toFixed(1)}°<br>전체 접합 ${m.contacts} / 주요 ${m.usable_contacts}<br>주요 접합 연결망 ${m.usable_graph_components}개<br>중첩률 ${m.overlap_pct.toFixed(1)}%<br>접합 면적 변동계수 ${m.area_cv.toFixed(2)}`);window.currentCase=c.id;}
d3.selectAll('select,input').on('change',update);update();
d3.select('#export').on('click',()=>{const source=new XMLSerializer().serializeToString(svg.node()),url=URL.createObjectURL(new Blob([source],{type:'image/svg+xml'})),a=document.createElement('a');a.href=url;a.download='Moving_Centres_'+window.currentCase+'.svg';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
</script></html>'''
html=html.replace('__D3__',(J/'assets/d3.v7.min.js').read_text()).replace('__CASES__',json.dumps(cases)).replace('__HATCHES__',json.dumps(hatches))
(J/'output/Moving_Centres_Explorer.html').write_text(html)
