from pathlib import Path
import json,hashlib,zipfile,shutil,subprocess
import fitz
from PIL import Image
J=Path(__file__).resolve().parents[1]
skills=[]
for name in ['rhino-modeling','canvas-design','d3-viz','algorithmic-art']:
 p=Path('/workspace/seunghwan2777/.agents/skills')/name/'SKILL.md'
 assert p.is_file()
 skills.append(dict(name=name,path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),applied=True))
(J/'design/skills-installed.json').write_text(json.dumps(skills,indent=2))
boards=['01_Field_Alternatives','02_Independent_Pivots','03_Organic_Figure_Ground','04_Organic_Hatch','05_Overlap_Atlas','Clean_Organic_Figure_Ground','Clean_Organic_Hatch']
combined=fitz.open();checks=[]
for name in boards:
 p=J/'output'/f'{name}.pdf';doc=fitz.open(p);assert len(doc)==1;r=doc[0].rect
 assert abs(r.width*25.4/72-594)<.01 and abs(r.height*25.4/72-420)<.01
 im=Image.open(J/'output'/f'{name}.png').convert('RGB');assert im.getpixel((0,0))==(255,255,255)
 checks.append(dict(name=name,width_mm=r.width*25.4/72,height_mm=r.height*25.4/72,pdf_bytes=p.stat().st_size,png_size=im.size))
 combined.insert_pdf(doc)
combined.set_metadata({'title':'Fruchter House — Moving Centres / Shared Office Study','author':'Spatial reconstruction study','subject':'Rotation, repetition, inter-module overlap; relative study units'})
combined.save(J/'Fruchter_Moving_Centres_A2.pdf',garbage=4,deflate=True)
(J/'review/file-checks.json').write_text(json.dumps(checks,indent=2))
# Keep previous deliveries untouched; only populate a fresh folder.
D=Path('/workspace/seunghwan2777/downloads/fruchter-pivot-fields');D.mkdir(parents=True,exist_ok=True)
for name in ['output','assets','design','scripts','review']:
 shutil.copytree(J/name,D/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
for name in ['README.md','requirements.txt','Fruchter_Moving_Centres_A2.pdf']:shutil.copy2(J/name,D/name)
files=[p for p in D.rglob('*') if p.is_file() and p.name not in ['manifest.json','Fruchter_Moving_Centres_Editable.zip']]
manifest=[dict(path=str(p.relative_to(D)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(files)]
(D/'manifest.json').write_text(json.dumps(manifest,indent=2))
z=D/'Fruchter_Moving_Centres_Editable.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as archive:
 for p in sorted(D.rglob('*')):
  if p.is_file() and p!=z:archive.write(p,Path('Fruchter_Moving_Centres')/p.relative_to(D))
with zipfile.ZipFile(z) as archive:assert archive.testzip() is None
print('PDF pages',len(combined),'files',len(manifest))
for p in [D/'Fruchter_Moving_Centres_A2.pdf',z,D/'output/Clean_Organic_Figure_Ground.png',D/'output/Clean_Organic_Hatch.png',D/'output/Moving_Centres_2D.3dm']:
 print(p.name,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
