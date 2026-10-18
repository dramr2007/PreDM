from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
W,H=720,1280
NAVY='#08172C'; BG='#0A2133'; TURQ='#28E1C0'; CYAN='#65DBEF'; WHITE='#FFFFFF'; YELLOW='#F9CC54'; MUTED='#ABC5D0'
fonts=['/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
bolds=['/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
arfont=next((z for z in fonts if Path(z).exists()),fonts[-1])
arbold=next((z for z in bolds if Path(z).exists()),bolds[-1])
latin='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def fa(sz,b=False):return ImageFont.truetype(arbold if b else arfont,sz)
def en(d,v,x,y,n=26,c=CYAN,b=False):d.text((x,y),v,font=ImageFont.truetype(latin,n),fill=c,anchor='mm')
def ar(d,v,x,y,n=42,c=WHITE,b=True):d.text((x,y),v,font=fa(n,b),fill=c,anchor='mm',direction='rtl',language='ar')
def rect(d,b,fill,outline=None,radius=24):d.rounded_rectangle(b,radius=radius,fill=fill,outline=outline,width=3)
def base(i,title,eng,tag):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 for y in range(H):
  col=(8+int(7*y/H),26+int(11*y/H),43+int(9*y/H))
  d.line((0,y,W,y),fill=col)
 rect(d,(35,36,W-35,125),'#103D50',radius=26)
 en(d,'HAKIM AI',360,79,36,TURQ,True)
 ar(d,title,360,208,48)
 en(d,eng,360,287,27,YELLOW)
 rect(d,(56,346,664,1030),'#15364B',outline='#275F75',radius=30)
 ar(d,tag,360,1074,28,CYAN)
 en(d,'Dr\\Amr kamel kahlil ahmed',360,1199,21,MUTED)
 en(d,f'HAI-C0051 | {i+1}/3',360,1241,18,MUTED)
 return im,d
# Narration approx 9.17s; three meaningful beats, same order as audio.
im,d=base(0,'دائرة أم مثلث؟','WHAT SHAPE IS IT?','كيف يتعرّف النموذج على الشكل؟')
d.ellipse((128,534,319,725),fill=TURQ)
d.polygon([(466,530),(364,742),(568,742)],fill=YELLOW)
en(d,'A',225,813,35,WHITE)
en(d,'B',465,813,35,WHITE)
im.save(ROOT/'voice51_scene_0.png')
im,d=base(1,'هذا يُسمّى التصنيف','CLASSIFICATION','نموذج الذكاء الاصطناعي يختار فئة')
rect(d,(98,482,328,823),'#1B5365',outline=TURQ,radius=28)
rect(d,(396,482,625,823),'#51462B',outline=YELLOW,radius=28)
d.ellipse((159,533,268,642),fill=TURQ)
d.polygon([(511,530),(456,650),(570,650)],fill=YELLOW)
ar(d,'دائرة',214,736,37)
ar(d,'مثلث',511,736,37)
im.save(ROOT/'voice51_scene_1.png')
im,d=base(2,'فئة... وليس رقمًا','CLASS VS NUMBER','التصنيف يختلف عن الانحدار')
rect(d,(111,461,613,607),'#1C5B63',outline=TURQ)
ar(d,'تصنيف: دائرة أو مثلث',360,535,32)
rect(d,(111,654,613,800),'#334B68',outline=YELLOW)
ar(d,'انحدار: قيمة مستمرة',360,729,32)
en(d,'LIKE HEIGHT OR TEMPERATURE',360,867,22,YELLOW)
im.save(ROOT/'voice51_scene_2.png')
src=ROOT/'HAI-C0051_voice_match_test.wav'
out=ROOT/'HAI-C0051-classification-VOICE-TEST.mp4'
assert src.is_file() and src.stat().st_size>10000, 'Missing voice artifact'
args=['ffmpeg','-hide_banner','-loglevel','error','-y']
for i,t in enumerate([3.1,2.8,3.3]):args+=['-loop','1','-framerate','30','-t',str(t),'-i',str(ROOT/f'voice51_scene_{i}.png')]
args+=['-i',str(src)]
filters=[f'[{i}:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v{i}]' for i in range(3)]
filters+=['[v0][v1][v2]concat=n=3:v=1:a=0[v]']
args+=['-filter_complex',';'.join(filters),'-map','[v]','-map','3:a:0','-c:v','libx264','-preset','fast','-crf','21','-c:a','aac','-b:a','192k','-ar','44100','-t','9.17','-movflags','+faststart',str(out)]
subprocess.run(args,check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
print('VIDEO READY',out,out.stat().st_size)
