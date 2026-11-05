from pathlib import Path
import json,hashlib,shutil,zipfile,xml.etree.ElementTree as ET
import fitz
from PIL import Image
J=Path(__file__).resolve().parents[1];O=J/'output';P=J/'package';P.mkdir(exist_ok=True)
stems=['01_Overlap_Model_Families_A2','02_Parameter_Selection_A2','03_Void_Policy_And_Lineage_A2','04_Overlap_Development_A2','05_Selected_Model_Plan_A2']
combined=fitz.open();checks=[]
for stem in stems:
 p=O/(stem+'.pdf');doc=fitz.open(p);assert len(doc)==1;mm=[doc[0].rect.width*25.4/72,doc[0].rect.height*25.4/72];assert abs(mm[0]-594)<.03 and abs(mm[1]-420)<.03;combined.insert_pdf(doc);checks.append({'file':p.name,'pages':1,'size_mm':[594,420]})
 for suffix in ['.pdf','.png','.svg','_outlined.svg']:shutil.copy2(O/(stem+suffix),P/(stem+suffix))
 image=Image.open(O/(stem+'.png')).convert('RGB');assert image.size==(2800,1980);assert all(image.getpixel(p)==(255,255,255) for p in [(0,0),(2799,0),(0,1979),(2799,1979)])
 for suffix in ['.svg','_outlined.svg']:
  root=ET.parse(O/(stem+suffix)).getroot();assert root.get('width')=='594mm' and root.get('height')=='420mm'
  if suffix.startswith('_'):assert len(list(root.iter('{http://www.w3.org/2000/svg}text')))==0
combined.save(O/'Fruchter_Rule_Based_Overlap_A2.pdf');assert len(combined)==5
for name in ['Fruchter_Rule_Based_Overlap_A2.pdf','Overlap_Rule_Explorer.html','Fruchter_Rule_Models.3dm','M4_Selected_Massing.obj']:shutil.copy2(O/name,P/name)
# Round-trip OBJ topology: every undirected mesh edge must belong to two faces.
obj=(O/'M4_Selected_Massing.obj').read_text().splitlines();verts=[s for s in obj if s.startswith('v ')];faces=[[int(v) for v in line.split()[1:]] for line in obj if line.startswith('f ')];edges={}
for f in faces:
 assert all(1<=v<=len(verts) for v in f)
 for a,b in zip(f,f[1:]+f[:1]):key=tuple(sorted([a,b]));edges[key]=edges.get(key,0)+1
assert all(n==2 for n in edges.values())
checks.append({'file':'M4_Selected_Massing.obj','vertices':len(verts),'faces':len(faces),'manifold_edge_incidence':2})
for directory in ['design','source','assets']:
 shutil.copytree(J/directory,P/directory,dirs_exist_ok=True)
(P/'review').mkdir(exist_ok=True)
for name in ['geometry-checks.json','model-checks.json','browser-checks.json']:shutil.copy2(J/'review'/name,P/'review'/name)
(P/'review/file-checks.json').write_text(json.dumps(checks,indent=2))
(P/'scripts').mkdir(exist_ok=True)
for name in ['graphics.py','design.py','draw.py','export_models.py','build_explorer.py','validate.py','check_browser.py','package_outputs.py']:shutil.copy2(J/'scripts'/name,P/'scripts'/name)
shutil.copy2(J/'README.md',P/'README.md')
(P/'requirements.txt').write_text('shapely==2.2.0\ncairosvg==2.9.1\nfonttools==4.61.1\npillow==12.3.0\npymupdf==1.26.6\nrhino3dm==8.35.0\nplaywright\n')
manifest=[]
for p in sorted(P.rglob('*')):
 if p.is_file() and p.name!='manifest.json':manifest.append({'path':str(p.relative_to(P)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
archive=O/'Fruchter_Rule_Models_Package.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(P.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(P)))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print('Verified package files',len(manifest)+1)
for p in [O/'Fruchter_Rule_Based_Overlap_A2.pdf',archive,O/'Fruchter_Rule_Models.3dm',O/'M4_Selected_Massing.obj']:print(p.name,p.stat().st_size)
