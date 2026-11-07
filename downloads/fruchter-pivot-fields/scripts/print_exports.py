from pathlib import Path
import cairosvg
J=Path(__file__).resolve().parents[1]
for n in ['Clean_Organic_Figure_Ground','Clean_Organic_Hatch']:
 cairosvg.svg2png(url=str(J/'output'/f'{n}_outlined.svg'),write_to=str(J/'output'/f'{n}.png'),output_width=7016,output_height=4961)
 print(n,'7016 x 4961')
