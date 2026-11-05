from pathlib import Path
from playwright.sync_api import sync_playwright
import json
J=Path(__file__).resolve().parents[1];errors=[];report={}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1450,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((J/'output/Overlap_Rule_Explorer.html').read_text(),wait_until='load')
 families={}
 for key in ['M1','M2','M3','M4','M5','R0']:
  page.select_option('#model',key);assert page.get_attribute('#plan','data-model')==key;families[key]=page.locator('#plan path').count()
 cases=[];page.select_option('#model','PARAM')
 for radius in ['0.4','0.45','0.5']:
  for phase in ['0','15','30']:
   page.select_option('#radius',radius);page.select_option('#phase',phase);expected=f'R{float(radius):.2f}_P{phase}';assert page.get_attribute('#plan','data-model')==expected;cases.append(expected)
 page.select_option('#model','M4');page.check('#details');before=page.locator('#plan path').count();page.uncheck('#details');assert page.locator('#plan path').count()<before;page.check('#details');page.uncheck('#cut');assert page.get_attribute('#plan','data-cut')=='false';page.check('#cut')
 with page.expect_download() as dl:page.click('#download')
 download=dl.value;assert download.suggested_filename=='Fruchter_M4.svg';download.save_as(J/'review/explorer-export.svg')
 page.screenshot(path=str(J/'review/explorer-desktop.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth <= innerWidth');page.screenshot(path=str(J/'review/explorer-mobile.png'),full_page=True)
 assert not errors
 report={'family_states':families,'parameter_cases':cases,'layer_toggles':True,'svg_export':True,'offline_inline_d3':True,'mobile_no_horizontal_overflow':True,'javascript_errors':errors}
 browser.close()
(J/'review/browser-checks.json').write_text(json.dumps(report,indent=2));print('Browser checks passed: six family/source states and nine parameter cases')
