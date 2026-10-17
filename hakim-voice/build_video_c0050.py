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
 en(d,f'HAI-C0050   |   {i+1}/6',(W//2,1243),18,MUTED)
 return im,d








def dots(d,isolated=True):
 box(d,(117,447,599,888),fill='#193B56',outline='#376777',rad=24)
 d.line((160,838,562,838),fill=PALE,width=3)
 d.line((160,838,160,486),fill=PALE,width=3)
 for x,y,c in [(240,796,TURQ),(308,780,CYAN),(380,765,TURQ)]:
  d.ellipse((x-16,y-16,x+16,y+16),fill=c)
 if isolated:
  d.ellipse((517,525,554,562),fill=RED)
  en(d,'1400',(537,486),25,RED,heavy=True)
 ar(d,'١٢   ١٣   ١٤',(W//2,926),28,YELLOW,True)

# 1: strong illustrative visual hook.
im,d=base(0,'١٤... ثم ١٤٠٠؟','AN OUTLIER!','هل الرقم الغريب خطأ أم حدث حقيقي؟')
dots(d)
im.save(P/'corrected_00.png')

# 2: clear definition.
im,d=base(1,'ما هي القيمة المتطرفة؟','OUTLIER','قيمة بعيدة عن النمط المعتاد')
dots(d)
ar(d,'لا تحذف النقطة الحمراء فورًا',(W//2,990),23,RED,True)
im.save(P/'corrected_01.png')

# 3: plausible causes, no invented facts.
im,d=base(2,'قبل الحذف: افحص','CHECK THE SOURCE','قد يكون الخطأ في الوحدة أو الإدخال')
for j,(artext,enlabel,c) in enumerate([
 ('إدخال خاطئ','DATA ENTRY',RED),
 ('وحدة مختلفة','WRONG UNIT',YELLOW),
 ('حالة نادرة حقيقية','REAL RARE EVENT',TURQ)]):
 y=426+j*172
 box(d,(104,y,619,y+135),fill='#204D62',outline=c,rad=22)
 ar(d,artext,(W//2,y+51),30,WHITE,True)
 en(d,enlabel,(W//2,y+107),22,c)
im.save(P/'corrected_02.png')

# 4: significance in research medicine.
im,d=base(3,'الغرابة قد تكون مهمة','CLINICAL CONTEXT','لا تفقد المعلومة النادرة')
box(d,(122,478,609,798),fill='#214159',outline=TURQ,rad=30)
ar(d,'ليس كل خارج عن المعتاد',(W//2,568),34,WHITE,True)
ar(d,'مجرد خطأ!',(W//2,665),43,YELLOW,True)
ar(d,'راجع المعنى والسياق',(W//2,938),29,CYAN)
im.save(P/'corrected_03.png')

# 5: defensible process and train/test independence.
im,d=base(4,'خطة مراجعة علمية','VALIDATE THE DATA','افهم القياس قبل أي قرار')
for j,text in enumerate(['افحص المصدر والوحدة','حدّد السبب إن أمكن','قيّم أثر الاحتفاظ أو الحذف']):
 y=432+j*179
 box(d,(105,y,613,y+139),fill='#1D5064',outline=TURQ,rad=20)
 ar(d,text,(W//2,y+70),28,WHITE,True)
im.save(P/'corrected_04.png')

# 6: call and response.
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','كل رقم بعيد يستحق التحقق')
ar(d,'هل كل قيمة بعيدة خطأ؟',(W//2,519),36,WHITE,True)
box(d,(113,629,607,764),fill='#195E68',outline=TURQ,rad=26)
ar(d,'لا... افحصها أولًا',(W//2,695),37,WHITE,True)
ar(d,'شارك الحلقة مع متعلم جديد',(W//2,941),26,YELLOW)
im.save(P/'corrected_05.png')


robot_path = P / 'hakim_x_robot.png'
if robot_path.exists():
 sprite=Image.open(robot_path).convert('RGBA')
 sprite.thumbnail((80,110))
 for idx in range(6):
  path=P/f'corrected_{idx:02d}.png'
  slide=Image.open(path).convert('RGBA')
  slide.alpha_composite(sprite,(555,948))
  slide.convert('RGB').save(path)

with wave.open(str(P/'output/HAI-C0050_arabic_voice_master.wav')) as wf: duration=wf.getnframes()/wf.getframerate()
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
cmd=[ffmpeg_bin,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(P/'scenes.ffconcat'),'-i',str(P/'output/HAI-C0050_arabic_voice_master.wav'),'-r','30','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(duration),'-shortest',str(P/'HAI-C0050-outliers-AR-fixed.mp4')]
subprocess.run(cmd,cwd=P,check=True)
print('Created',str(P/'HAI-C0050-outliers-AR-fixed.mp4'))