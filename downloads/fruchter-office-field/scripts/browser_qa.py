from pathlib import Path
from playwright.sync_api import sync_playwright
import json,base64,xml.etree.ElementTree as ET
J=Path(__file__).resolve().parents[1];report={}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1500,'height':1100},accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((J/'output/Office_Field_Explorer.html').read_text());page.wait_for_function('window.currentCase')
 cases=[]
 for f in ['GRID','STAGGER','ALTERNATE']:
  page.select_option('#family',f)
  for d in ['1.45','1.65','1.85']:
   page.select_option('#spacing',d);assert page.locator('#layer-floor path').count()==1;cases.append(page.evaluate('window.currentCase'))
 page.select_option('#family','STAGGER');page.select_option('#spacing','1.65');page.select_option('#mode','hatch');assert page.locator('#layer-hatch path').count()>2000
 page.check('#route');assert page.locator('#layer-route path').count()==1
 with page.expect_download() as download:page.click('#export')
 download.value.save_as(J/'review/d3-export.svg');root=ET.parse(J/'review/d3-export.svg').getroot();assert root.get('width')=='594mm'
 page.screenshot(path=str(J/'review/d3-explorer.png'),full_page=True);report['d3_cases']=cases
 page.set_content((J/'output/Directional_Hatch_Studio.html').read_text());page.wait_for_function('window.__art')
 a=page.evaluate('window.__art.still(42,1)');b=page.evaluate('window.__art.still(42,1)');assert a==b
 page.evaluate('window.__art.setSeed(42)');r=page.evaluate('window.__art.svg()');(J/'review/studio-export.svg').write_text(r['svg']);root=ET.fromstring(r['svg']);assert root.get('width')=='594mm'
 report.update(errors=errors,hatch_deterministic=True,hatch_svg_stats=r['stats']);assert not errors
 browser.close()
(J/'review/browser-qa.json').write_text(json.dumps(report,indent=2));print(report)
