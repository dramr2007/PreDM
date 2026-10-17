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
 en(d,f'HAI-C0043   |   {i+1}/6',(W//2,1243),18,MUTED)
 return im,d



def circle(d,x,y,r,color,thickness=9):
 d.ellipse((x-r,y-r,x+r,y+r),outline=color,width=thickness)

# Scene 1: Hook — old knowledge facing something new.
im,d=base(0,'هل يعرف الرسم الجديد؟','GENERALIZATION','التعميم يعني نجاحًا على أمثلة جديدة')
circle(d,260,598,82,TURQ,11);circle(d,463,598,82,RED,11)
en(d,'TRAIN',(261,746),30,PALE,heavy=True)
en(d,'NEW',(463,746),30,YELLOW,heavy=True)
d.line((333,597,384,597),fill=WHITE,width=6);d.polygon([(374,582),(398,597),(374,612)],fill=WHITE)
ar(d,'النموذج يستخدم ما تعلّمه',(W//2,946),29,WHITE,True)
im.save(P/'corrected_00.png')

# Scene 2: Training set examples.
im,d=base(1,'أمثلة من التدريب','TRAINING EXAMPLES','دوائر زرقاء بأساليب متقاربة')
for (x,y,r,w) in [(210,554,61,6),(480,554,68,11),(350,780,82,15)]:
 circle(d,x,y,r,TURQ,w)
ar(d,'يتعلّم خصائص الدائرة',(W//2,960),30,YELLOW,True)
im.save(P/'corrected_01.png')

# Scene 3: Unseen example and a prediction.
im,d=base(2,'دائرة بخط مختلف','UNSEEN EXAMPLE','المثال جديد والهدف نفسه')
circle(d,350,625,125,RED,18)
box(d,(174,845,546,933),fill='#1A625E',outline=TURQ,rad=22)
ar(d,'تعرّف عليها: دائرة',(W//2,888),32,WHITE,True)
im.save(P/'corrected_02.png')

# Scene 4: Changing context should be evaluated.
im,d=base(3,'لكن هل ينجح دائمًا؟','DOMAIN SHIFT','اختبر التنوع قبل التعميم')
for x,y,r,c,w in [(201,553,60,RED,6),(488,553,67,YELLOW,13),(201,799,71,TURQ,17),(488,799,58,WHITE,5)]:
 circle(d,x,y,r,c,w)
ar(d,'ألوان وأساليب ورُسوم متنوعة',(W//2,972),27,YELLOW)
im.save(P/'corrected_03.png')

# Scene 5: Clean separation of train/validation/test.
im,d=base(4,'تقييم أكثر عدلًا','TRAIN  •  VALIDATE  •  TEST','استخدم أمثلة جديدة مستقلة')
for y,t,enlabel,col in [(440,'التدريب','TRAIN',TURQ),(627,'التحقق','VALIDATION',YELLOW),(814,'الاختبار','TEST',RED)]:
 box(d,(102,y,618,y+145),fill='#224C60',outline=col,rad=26,width=3)
 ar(d,t,(W//2,y+53),35,WHITE,True)
 en(d,enlabel,(W//2,y+109),23,col)
im.save(P/'corrected_04.png')

# Scene 6: Short question and caveat.
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','الاختبار الواحد ليس ضمانًا')
ar(d,'هل نجاح واحد يكفي؟',(W//2,510),38,WHITE,True)
box(d,(112,628,608,762),fill='#165E67',outline=TURQ,rad=25)
ar(d,'لا، نحتاج تقييمًا أوسع',(W//2,686),34,WHITE,True)
ar(d,'التعميم هو هدف التعلّم',(W//2,905),31,YELLOW,True)
im.save(P/'corrected_05.png')

with wave.open(str(P/'output/HAI-C0043_arabic_voice_master.wav')) as wf: duration=wf.getnframes()/wf.getframerate()
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
cmd=[ffmpeg_bin,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(P/'scenes.ffconcat'),'-i',str(P/'output/HAI-C0043_arabic_voice_master.wav'),'-r','30','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(duration),'-shortest',str(P/'HAI-C0043-generalization-AR-fixed.mp4')]
subprocess.run(cmd,cwd=P,check=True)
print('Created',str(P/'HAI-C0043-generalization-AR-fixed.mp4'))