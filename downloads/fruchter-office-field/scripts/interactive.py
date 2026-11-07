from pathlib import Path
import json
J=Path(__file__).resolve().parents[1]
cases=json.loads((J/'design/cases.json').read_text());selected=json.loads((J/'design/selected.json').read_text());hatches=json.loads((J/'design/hatch-paths.json').read_text())
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fruchter / Shared Edges</title><style>
*{box-sizing:border-box}body{margin:0;background:white;color:#222;font:15px/1.6 system-ui,sans-serif}header{padding:24px 32px;border-bottom:1px solid #ddd}h1{font-size:26px;margin:0}header p{margin:5px 0;color:#666}main{display:grid;grid-template-columns:280px 1fr;min-height:80vh}aside{padding:24px;border-right:1px solid #ddd}label{display:block;margin-top:18px}select,button{font:inherit;padding:8px;border:1px solid #bbb;background:#fff;width:100%}button{margin-top:25px;cursor:pointer}svg{width:100%;height:auto}#stats{margin-top:24px}small{color:#666}#message{color:#a73732} @media(max-width:800px){main{display:block}aside{border-right:0}}
</style><header><h1>Shared Edges — Fruchter House Reconstruction</h1><p>회전된 세 날개를 하나의 모듈로 반복한다. 배열 규칙과 공유 영역의 차이를 비교한다.</p></header><main><aside>
<label for="family">배열 규칙</label><select id="family"><option value="GRID">직교 격자</option><option value="STAGGER" selected>반 간격 어긋난 배열 / 선정</option><option value="ALTERNATE">60° 교대 회전</option></select>
<label for="spacing">모듈 간격</label><select id="spacing"><option>1.45</option><option selected>1.65</option><option>1.85</option></select>
<label for="mode">표현</label><select id="mode"><option value="overlap">중첩 위계</option><option value="figure">Figure–ground</option><option value="hatch">방향별 해치 / 선정안</option></select>
<label><input type="checkbox" id="route"> 선정안 공유 동선</label><label><input type="checkbox" id="ghost"> 모듈 경계선</label>
<div id="stats"></div><p id="message" role="status"></p><button id="export">현재 도면 SVG 저장</button><p><small>u는 상대 단위. 접합 내접원은 통로 폭을 의미하지 않습니다. 실치수·대지·구조가 미확정인 설계 스터디입니다.</small></p></aside><section><svg id="view" viewBox="0 0 594 420" xmlns="http://www.w3.org/2000/svg" width="594mm" height="420mm" role="img" aria-label="모듈 반복 및 중첩 비교"></svg></section></main>
<script>__D3__</script><script>
const cases=__CASES__,selected=__SELECTED__,hatches=__HATCHES__;
const svg=d3.select('#view');svg.append('rect').attr('width',594).attr('height',420).attr('fill','white');
const projection=d3.geoIdentity().reflectY(true).fitExtent([[22,32],[572,388]],{type:'Polygon',coordinates:[[[-1.2,-1.2],[7.1,-1.2],[7.1,4.9],[-1.2,4.9],[-1.2,-1.2]]]});
const path=d3.geoPath(projection);const layers={};['floor','overlap','triple','hatch','ghost','route'].forEach(k=>layers[k]=svg.append('g').attr('id','layer-'+k));
function update(){const f=document.querySelector('#family').value,d=+document.querySelector('#spacing').value;let mode=document.querySelector('#mode').value;const c=cases.find(x=>x.family===f&&x.d===d),chosen=c.id==='STAGGER-1.65';if(mode==='hatch'&&!chosen){mode='overlap';document.querySelector('#mode').value=mode;}document.querySelector('#message').textContent=chosen?'선정안: 공유 띠와 세 모듈 결절점이 공존':'해치·동선은 발전시킨 선정안에서 제공합니다.';
const bind=(k,data,fill,stroke,width)=>layers[k].selectAll('path').data(data).join('path').attr('d',path).attr('fill',fill).attr('fill-rule','evenodd').attr('stroke',stroke).attr('stroke-width',width);
bind('floor',mode==='hatch'?[]:[c.floor],mode==='figure'?'#111':'#ddd',null,0);bind('overlap',mode==='overlap'?[c.overlap]:[],'#222',null,0);bind('triple',mode==='overlap'?[c.triples]:[],'#a73732',null,0);
bind('hatch',mode==='hatch'?hatches.map(q=>({type:'LineString',coordinates:q.pts})):[],'none','#242424',.16);
bind('ghost',document.querySelector('#ghost').checked?c.units.map(u=>u.envelope):[],'none','#999',.12);layers.ghost.attr('stroke-dasharray','1 .8');bind('route',chosen&&document.querySelector('#route').checked?[selected.routes]:[],'none','#b44335',.45);
const m=c.metrics;d3.select('#stats').html(`<strong>${c.id}</strong><br>모듈 12개 · 접합 ${m.contacts}개<br>중첩 면적률 ${m.overlap_pct.toFixed(1)}%<br>최소 접합 내접원 Ø ${m.min_contact_diameter.toFixed(2)}u<br>중정 ${m.courts}개 / 자연 틈 ${m.natural_voids}개`);window.currentCase=c.id;}
d3.selectAll('select,input').on('change',update);update();
d3.select('#export').on('click',()=>{const source=new XMLSerializer().serializeToString(svg.node()),url=URL.createObjectURL(new Blob([source],{type:'image/svg+xml'})),a=document.createElement('a');a.href=url;a.download='Fruchter_'+window.currentCase+'.svg';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
</script></html>'''
html=html.replace('__D3__',(J/'assets/d3.v7.min.js').read_text()).replace('__CASES__',json.dumps(cases)).replace('__SELECTED__',json.dumps(selected)).replace('__HATCHES__',json.dumps(hatches))
(J/'output/Office_Field_Explorer.html').write_text(html)
