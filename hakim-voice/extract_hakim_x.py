from PIL import Image
from pathlib import Path
import subprocess,os
P=Path(__file__).resolve().parent
movie=P/'reference_14oct.mp4'
out=P/'hakim_x_robot.png'
if not movie.exists(): raise FileNotFoundError(str(movie))
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','1','-i',str(movie),'-frames:v','1',str(P/'ref_frame.png')],check=True)
frame=Image.open(P/'ref_frame.png').convert('RGB')
crop=frame.crop((270,313,453,588))
bg=(7,29,39)
robot=Image.new('RGBA',crop.size)
for y in range(crop.height):
 for x in range(crop.width):
  rgb=crop.getpixel((x,y))
  contrast=max(abs(rgb[i]-bg[i]) for i in range(3))
  alpha=min(255,max(0,int((contrast-17)*255/35)))
  robot.putpixel((x,y),(*rgb,alpha))
robot.save(out)
print('EXTRACTED',out)
