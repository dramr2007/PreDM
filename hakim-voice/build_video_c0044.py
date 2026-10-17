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
 en(d,f'HAI-C0044   |   {i+1}/6',(W//2,1243),18,MUTED)
 return im,d




# HAI-C0044: visually accurate, fictional examples, six scenes.
def arrow(d,start,end,color=RED,w=10):
 d.line([start,end],fill=color,width=w)
 ex,ey=end;sx,sy=start;import math
 angle=math.atan2(ey-sy,ex-sx)
 a=angle+2.55;b=angle-2.55
 d.polygon([(ex,ey),(ex+25*math.cos(a),ey+25*math.sin(a)),(ex+25*math.cos(b),ey+25*math.sin(b))],fill=color)
def card(d,x,y,w,h,txt,eng,col):
 box(d,(x,y,x+w,y+h),fill='#1D5060',outline=col,rad=22,width=3)
 ar(d,txt,(x+w//2,y+int(h*.38)),30,WHITE,True)
 en(d,eng,(x+w//2,y+int(h*.74)),22,col)

# 1: The surprising hook
im,d=base(0,'دقّة عالية... ثم فشل؟','DATA LEAKAGE','قد تكون الإجابة تسرّبت إلى النموذج')
card(d,98,450,235,190,'التدريب','TRAIN',TURQ)
card(d,384,450,235,190,'الاختبار','TEST',YELLOW)
arrow(d,(495,677),(230,705),RED,10)
ar(d,'معلومة دخلت قبل موعدها!',(W//2,831),33,RED,True)
ar(d,'ليست كل دقة عالية دليلًا على الجودة',(W//2,934),24,WHITE)
im.save(P/'corrected_00.png')

# 2: Separate evaluation properly
im,d=base(1,'افصل التدريب والاختبار','SEPARATE THE DATA','امنع مرور معلومات الاختبار إلى التدريب')
card(d,97,467,238,223,'تدريب','TRAIN',TURQ)
card(d,383,467,238,223,'اختبار','TEST',YELLOW)
d.line((360,416,360,893),fill=RED,width=12)
d.ellipse((340,623,380,663),fill=RED)
ar(d,'حد فاصل',(W//2,929),31,YELLOW,True)
im.save(P/'corrected_01.png')

# 3: duplicate participants when generalizing to new people
im,d=base(2,'المريض نفسه مرتين؟','PATIENT OVERLAP','عند التوقع لمرضى جدد: افصل المرضى')
card(d,98,440,240,188,'تدريب','TRAIN',TURQ)
card(d,383,440,240,188,'اختبار','TEST',YELLOW)
for cx,cy in [(218,725),(502,725)]:
 d.ellipse((cx-27,cy-55,cx+27,cy-1),fill=PALE)
 d.rounded_rectangle((cx-46,cy,cx+46,cy+88),radius=20,fill='#4C869A')
 en(d,'ID A',(cx,cy+122),25,YELLOW)
arrow(d,(300,745),(428,745),RED,10)
ar(d,'قد يحفظ هوية المريض',(W//2,948),29,RED,True)
im.save(P/'corrected_02.png')

# 4: future information
im,d=base(3,'معلومة من المستقبل','FUTURE LEAKAGE','لا تستخدم بيانات لم تكن متاحة وقت التوقع')
card(d,112,453,496,168,'قرار اليوم','PREDICTION TIME',TURQ)
card(d,112,740,496,168,'نتيجة لاحقة','FUTURE RESULT',RED)
arrow(d,(358,726),(358,649),RED,12)
ar(d,'المستقبل لا يسبق القرار',(W//2,984),27,YELLOW,True)
im.save(P/'corrected_03.png')

# 5: proper engineering sequence
im,d=base(4,'كيف نمنع التسرّب؟','SAFE EVALUATION','خطوات قبل أي ادعاء عن دقة النموذج')
for j,(name,eng,c) in enumerate([
 ('قسّم البيانات أولًا','SPLIT FIRST',TURQ),
 ('عالِج التدريب وحده','FIT ON TRAIN',YELLOW),
 ('اختبر بشكل مستقل','TEST INDEPENDENTLY',CYAN)]):
 y=415+j*196
 box(d,(85,y,635,y+157),fill='#1D4B5E',outline=c,rad=24,width=3)
 ar(d,name,(W//2,y+57),32,WHITE,True)
 en(d,eng,(W//2,y+116),23,c)
im.save(P/'corrected_04.png')

# 6: audience interactive close
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','التحقّق أهم من الرقم الجميل')
ar(d,'هل الدقة العالية وحدها تكفي؟',(W//2,515),33,WHITE,True)
box(d,(94,638,627,775),fill='#175C64',outline=TURQ,rad=28)
ar(d,'لا، افحص تسرّب البيانات!',(W//2,708),31,WHITE,True)
ar(d,'شارك المثال مع من يتعلم الذكاء الاصطناعي',(W//2,933),24,YELLOW)
im.save(P/'corrected_05.png')

with wave.open(str(P/'output/HAI-C0044_arabic_voice_master.wav')) as wf: duration=wf.getnframes()/wf.getframerate()
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
cmd=[ffmpeg_bin,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(P/'scenes.ffconcat'),'-i',str(P/'output/HAI-C0044_arabic_voice_master.wav'),'-r','30','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(duration),'-shortest',str(P/'HAI-C0044-data-leakage-AR-fixed.mp4')]
subprocess.run(cmd,cwd=P,check=True)
print('Created',str(P/'HAI-C0044-data-leakage-AR-fixed.mp4'))