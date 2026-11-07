from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,json
J=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1400,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((J/'output/Directional_Hatch_Studio.html').read_text());page.wait_for_function('window.__art !== undefined')
 page.evaluate('window.__art.setParams({density:1,weight:0.40})')
 url=page.evaluate('window.__art.contactSheet([1,2,3,4,5,6,7,8,9],480)');(J/'review/hatch-round2.png').write_bytes(base64.b64decode(url.split(',')[1]));url=page.evaluate('window.__art.still(42,4)');(J/'review/hatch-print-check.png').write_bytes(base64.b64decode(url.split(',')[1]));print('errors',errors)
 browser.close()
