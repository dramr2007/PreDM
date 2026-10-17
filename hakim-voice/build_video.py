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
 en(d,f'HAI-C0041   |   {i+1}/6',(W//2,1243),18,MUTED)
 return im,d

# 1: conceptual hook
im,d=base(0,'هل يفشل النموذج؟','OVERFITTING','درجة التدريب وحدها لا تكفي')
ar(d,'نتيجة التدريب',(560,465),28,PALE);ar(d,'نتيجة الاختبار',(560,755),28,PALE)
for y,ratio,c in [(530,.90,TURQ),(820,.32,RED)]:
 box(d,(110,y,110+int(480*ratio),y+65),fill=c,rad=16)
ar(d,'مرتفع',(180,575),23,NAVY); ar(d,'أضعف',(180,865),23,WHITE)
im.save(P/'corrected_00.png')
# 2: misleading cue
im,d=base(1,'احفظ الشكل لا الخلفية','LEARN THE RIGHT SIGNAL','بعض النماذج تحفظ إشارة مضللة')
box(d,(95,410,338,816),fill='#336F5D',rad=26);box(d,(381,410,624,816),fill='#806A24',rad=26)
ar(d,'تفاح',(216,480),32,WHITE,True);ar(d,'موز',(501,480),32,WHITE,True)
d.ellipse((154,557,280,683),fill=RED);d.ellipse((440,571,562,677),fill=YELLOW)
ar(d,'خلفية خضراء',(216,748),25,WHITE);ar(d,'خلفية صفراء',(501,748),25,WHITE)
ar(d,'هل تعلّم نوع الفاكهة؟',(W//2,943),32,YELLOW,True)
im.save(P/'corrected_01.png')
# 3: new images
im,d=base(2,'اختبار بصور جديدة','UNSEEN DATA','تبديل الخلفية يكشف الخطأ')
box(d,(96,434,625,756),fill='#244359',rad=26)
ar(d,'تغيّرت الخلفيات!',(W//2,494),36,WHITE,True)
d.ellipse((154,548,260,654),fill=RED);d.ellipse((453,548,559,654),fill=YELLOW)
d.line([(290,601),(430,601)],fill=TURQ,width=7);d.polygon([(416,584),(444,601),(416,618)],fill=TURQ)
ar(d,'قد يخطئ النموذج',(W//2,863),39,RED,True)
im.save(P/'corrected_02.png')
# 4: comparison
im,d=base(3,'ممتاز في التدريب','TRAIN vs. TEST','لكن الأداء الجديد قد يكون أضعف')
for y,col,label,frac in [(496,TURQ,'التدريب',0.89),(716,RED,'الاختبار',0.35)]:
 ar(d,label,(W//2,y-48),36,WHITE,True)
 box(d,(118,y,602,y+74),fill='#284A5B',rad=18)
 box(d,(118,y,118+int(484*frac),y+74),fill=col,rad=18)
ar(d,'الفرق يدعونا للتحقّق',(W//2,931),33,YELLOW,True)
im.save(P/'corrected_03.png')
# 5 solutions
im,d=base(4,'كيف نُحسّن التعميم؟','IMPROVE GENERALIZATION','لا يوجد حل سحري واحد')
for j,(t,desc) in enumerate([('بيانات متنوعة','صور وخلفيات مختلفة'),('اختبار مستقل','أمثلة لم تُرَ أثناء التدريب'),('ضبط التعقيد','تقليل الحفظ غير المفيد')]):
 y=416+174*j
 box(d,(98,y,624,y+138),fill='#205166',outline='#33849B',rad=22,width=2)
 ar(d,t,(W//2,y+46),32,YELLOW,True)
 ar(d,desc,(W//2,y+96),25,WHITE)
im.save(P/'corrected_04.png')
# 6 outro
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','تعلّم ثم تحقّق')
ar(d,'هل نجاح التدريب يكفي؟',(W//2,492),35,WHITE,True)
box(d,(125,587,595,699),fill='#156C67',rad=25)
ar(d,'لا، اختبر أمثلة جديدة',(W//2,642),34,WHITE,True)
ar(d,'تابع قناة حكيم',(W//2,875),43,YELLOW,True)
im.save(P/'corrected_05.png')

with wave.open(str(P/'output/HAI-C0041_arabic_voice_master.wav')) as wf: duration=wf.getnframes()/wf.getframerate()
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
cmd=[ffmpeg_bin,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(P/'scenes.ffconcat'),'-i',str(P/'output/HAI-C0041_arabic_voice_master.wav'),'-r','30','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(duration),'-shortest',str(P/'HAI-C0041-overfitting-AR-fixed.mp4')]
subprocess.run(cmd,cwd=P,check=True)
print('Created',str(P/'HAI-C0041-overfitting-AR-fixed.mp4'))