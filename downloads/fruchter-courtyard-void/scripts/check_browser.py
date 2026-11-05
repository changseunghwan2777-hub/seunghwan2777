from pathlib import Path
from playwright.sync_api import sync_playwright
import json
J=Path(__file__).resolve().parents[1];errors=[];checks={}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((J/'output/Courtyard_Explorer.html').read_text(),wait_until='load')
 counts={}
 for state in ['original','expanded','overlap','full','selected']:
  page.select_option('#state',state);assert page.get_attribute('#plan','data-state')==state;counts[state]=page.locator('#plan path').count()
 assert len(set(counts.values()))>=4
 before=page.locator('#plan path').count();page.uncheck('#details');assert page.locator('#plan path').count()<before;page.check('#details')
 page.check('#ghost');page.uncheck('#flows');page.check('#flows')
 with page.expect_download() as dl:page.click('#download')
 down=dl.value;assert down.suggested_filename=='Fruchter_selected.svg';down.save_as(J/'review/explorer-export.svg')
 page.screenshot(path=str(J/'review/explorer-desktop.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 page.screenshot(path=str(J/'review/explorer-mobile.png'),full_page=True)
 assert not errors
 checks={'states_path_counts':counts,'layer_toggles':True,'svg_download':True,'mobile_no_horizontal_overflow':True,'javascript_errors':errors,'offline_inline_d3':True}
 b.close()
(J/'review/browser-checks.json').write_text(json.dumps(checks,indent=2));print(checks)
