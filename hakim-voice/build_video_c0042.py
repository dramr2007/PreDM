from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, math, wave, os, shutil
P=Path(__file__).parent
W,H=720,1280
NAVY='#08172C'; BG='#0A2133'; TURQ='#28E1C0'; CYAN='#65DBEF'; WHITE='#FFFFFF'; PALE='#E1F1F7'; MUTED='#ABC5D0'; YELLOW='#F9CC54'; RED='#FF6F81'; CARD='#142F45'
font_candidates=[
'/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf',
'/usr/share/fonts/truetype/noto/NotoSansArabicUI-Regular.ttf',
'/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
]
font_bold_candidates=[
'/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf',
'/usr/share/fonts/truetype/noto/NotoKufiArabic-Bold.ttf',
'/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
]
regular=next((f for f in font_candidates if Path(f).exists()),font_candidates[-1]); bold=next((f for f in font_bold_candidates if Path(f).exists()),font_bold_candidates[-1]); latin='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def font(size,heavy=False,english=False):return ImageFont.truetype(latin if english else (bold if heavy else regular),size)

def ar(d,txt,xy,size=37,color=WHITE,heavy=False,anchor='mm'):
 d.text(xy,txt,font=font(size,heavy),anchor=anchor,fill=color,direction='rtl',language='ar')
def en(d,txt,xy,size=29,color=CYAN,anchor='mm',heavy=False):
 d.text(xy,txt,font=ImageFont.truetype(latin,size),anchor=anchor,fill=color)
def box(d,coords,fill=CARD,outline=None,rad=24,width=2):d.rounded_rectangle(coords,radius=rad,fill=fill,outline=outline,width=width)

def base(i,title,english,tagline):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 for y in range(H):
  t=y/H;v=(int(8+7*t),int(26+10*t),int(43+12*t));d.line((0,y,W,y),fill=v)
 d.ellipse((450,-230,850,180),outline='#0E5A68',width=4)
 d.ellipse((-260,930,160,1340),outline='#0B4255',width=5)
 box(d,(38,38,W-38,121),fill='#103D50',rad=28)
 en(d,'HAKIM AI',(W//2,81),35,TURQ,heavy=True)
 ar(d,title,(W//2,214),50,WHITE,heavy=True)
 en(d,english,(W//2,285),29,YELLOW)
 box(d,(54,340,666,1040),fill='#13334C',outline='#235C70',rad=40,width=3)
 ar(d,tagline,(W//2,1085),29,CYAN)
 en(d,'Dr\\Amr kamel kahlil ahmed',(W//2,1198),21,MUTED)
 en(d,f'HAI-C0042   |   {i+1}/6',(W//2,1243),18,MUTED)
 return im,d


# Demo plot for an illustrative curved pattern. All drawn observations are fictional.
def plot(d, variant, show_curve=False, show_line=False, show_errors=False):
 x0,y0,x1,y1=104,450,622,860
 d.line((x0,y1,x1,y1),fill=PALE,width=3)
 d.line((x0,y1,x0,y0),fill=PALE,width=3)
 coords=[]
 for j in range(9):
  t=j/8
  # A smooth U-shaped pattern centered around x=0.5; illustration, not measured data.
  y=0.83-0.64*(2*t-1)**2
  coords.append((x0+42+t*430,y0+25+(1-y)*327))
 if show_curve:
  curve=[]
  for k in range(80):
   t=k/79
   y=0.83-0.64*(2*t-1)**2
   curve.append((int(x0+42+t*430),int(y0+25+(1-y)*327)))
  d.line(curve,fill=TURQ,width=8,joint='curve')
 if show_line:
  line_y=y0+25+(1-0.42)*327
  d.line((x0+42,line_y,x0+472,line_y),fill=RED,width=9)
 if show_errors:
  line_y=y0+25+(1-0.42)*327
  for x,y in coords:
   d.line((x,y,x,line_y),fill=YELLOW,width=3)
 for x,y in coords:
  d.ellipse((x-9,y-9,x+9,y+9),fill=WHITE,outline=NAVY,width=2)
 ar(d,'أمثلة تدريبية',(W//2,920),28,PALE)

# 1. The hook: model fails even on its training set.
im,d=base(0,'لماذا لا يتعلّم النموذج؟','UNDERFITTING','فشل حتى مع بيانات التدريب')
plot(d,'hook',show_line=True)
box(d,(188,984,532,1028),fill='#743C4B',rad=18)
ar(d,'تنبؤات بعيدة عن الأمثلة',(W//2,1005),24,WHITE)
im.save(P/'corrected_00.png')

# 2. Curved relationship in the observations.
im,d=base(1,'البيانات فيها نمط','CURVED PATTERN','قد تكون العلاقة غير خطيّة')
plot(d,'data')
ar(d,'نقاط على مسار منحني',(W//2,992),28,YELLOW,True)
im.save(P/'corrected_01.png')

# 3. Very simple model fitted to curved data.
im,d=base(2,'خط مستقيم لا يكفي','TOO SIMPLE MODEL','النموذج لا يلتقط شكل العلاقة')
plot(d,'line',show_line=True,show_errors=True)
ar(d,'الخط الأحمر بعيد عن كثير من النقاط',(W//2,985),24,YELLOW)
im.save(P/'corrected_02.png')

# 4. Training error still high; no invented measured percentages.
im,d=base(3,'خطأ حتى في التدريب','TRAINING ERROR','هذا يختلف عن فرط التكيّف')
plot(d,'training',show_line=True,show_errors=True)
box(d,(165,976,555,1022),fill='#713844',rad=17)
ar(d,'التعلّم لم يلتقط النمط',(W//2,998),27,WHITE,True)
im.save(P/'corrected_03.png')

# 5. A more suitable model and responsible checks.
im,d=base(4,'نموذج أنسب','MODEL SELECTION','التعقيد الأقصى ليس حلًا')
plot(d,'fit',show_curve=True)
ar(d,'نقارن التدريب والتحقّق',(W//2,990),27,YELLOW,True)
im.save(P/'corrected_04.png')

# 6. Short quiz.
im,d=base(5,'سؤال حكيم','CHECK UNDERSTANDING','افهم ثم تحقّق')
ar(d,'هل فحص التدريب وحده يكفي؟',(W//2,490),32,WHITE,True)
box(d,(115,585,605,717),fill='#165E67',outline=TURQ,rad=26)
ar(d,'لا، نختبر على بيانات جديدة',(W//2,640),30,WHITE,True)
ar(d,'النموذج الجيد يتعلّم ويُعمّم',(W//2,871),30,YELLOW,True)
im.save(P/'corrected_05.png')

with wave.open(str(P/'output/HAI-C0042_arabic_voice_master.wav')) as wf: duration=wf.getnframes()/wf.getframerate()
print('audio duration:', duration)
segments=[duration/6]*6
with (P/'scenes.ffconcat').open('w') as f:
 f.write('ffconcat version 1.0\n')
 for i,t in enumerate(segments): f.write(f'file corrected_{i:02d}.png\nduration {t:.8f}\n')
 f.write('file corrected_05.png\n')
ffmpeg_bin=shutil.which('ffmpeg')
if not ffmpeg_bin:
 import imageio_ffmpeg
 ffmpeg_bin=imageio_ffmpeg.get_ffmpeg_exe()
cmd=[ffmpeg_bin,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(P/'scenes.ffconcat'),'-i',str(P/'output/HAI-C0042_arabic_voice_master.wav'),'-r','30','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(duration),'-shortest',str(P/'HAI-C0042-underfitting-AR-fixed.mp4')]
subprocess.run(cmd,cwd=P,check=True)
print('Created',str(P/'HAI-C0042-underfitting-AR-fixed.mp4'))