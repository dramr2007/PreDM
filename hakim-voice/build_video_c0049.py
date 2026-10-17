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
 en(d,f'HAI-C0049   |   {i+1}/6',(W//2,1243),18,MUTED)
 return im,d








def measurement_table(d,highlight=1):
 headers=['السبت','الأحد','الاثنين']
 values=['١٢ سم','؟','١٦ سم']
 for j,(day,val) in enumerate(zip(headers,values)):
  y=450+j*172
  box(d,(104,y,622,y+141),fill='#1E5063',outline=YELLOW if j==highlight else TURQ,rad=22)
  ar(d,day,(508,y+48),30,WHITE,True)
  ar(d,val,(226,y+84),37,RED if j==highlight else WHITE,True)
  d.line((382,y+19,382,y+125),fill='#427A84',width=3)

# 1. Opening question: does a blank mean zero?
im,d=base(0,'الخانة فارغة!','MISSING DATA','هل القيمة المفقودة تساوي صفرًا؟')
measurement_table(d)
im.save(P/'corrected_00.png')

# 2. Actual missing data.
im,d=base(1,'مفقود لا يعني صفرًا','MISSING ≠ ZERO','لم نرصد القياس، فلا نخترع النتيجة')
measurement_table(d)
im.save(P/'corrected_01.png')

# 3. Bad decision example.
im,d=base(2,'لا تملأ الفراغ بصفر','NOT ALWAYS ZERO','هذا قد يُفسد معنى البيانات')
box(d,(142,478,579,747),fill='#3D334D',outline=RED,rad=29,width=4)
ar(d,'صفر؟',(W//2,567),58,RED,True)
d.line((238,650,478,650),fill=RED,width=10)
d.line((241,695,476,593),fill=RED,width=9)
ar(d,'غياب التسجيل ليس صفرًا',(W//2,876),29,WHITE,True)
im.save(P/'corrected_02.png')

# 4. Reasons matter.
im,d=base(3,'لماذا غاب القياس؟','INVESTIGATE THE CAUSE','السبب يحدد طريقة المعالجة')
for j,(artext,entext,col) in enumerate([
 ('تعطّل جهاز','DEVICE ISSUE',TURQ),
 ('لم يُجرَ القياس','NOT COLLECTED',YELLOW),
 ('الغياب قد يرتبط بالحالة','RELATED TO CONDITION',RED)]):
 y=416+j*181
 box(d,(97,y,624,y+149),fill='#1F4E63',outline=col,rad=23)
 ar(d,artext,(W//2,y+61),29,WHITE,True)
 en(d,entext,(W//2,y+117),21,col)
im.save(P/'corrected_03.png')

# 5. Appropriate train/test split.
im,d=base(4,'عالج دون تسريب','FIT ON TRAIN ONLY','تعلّم قاعدة التعويض من التدريب')
for j,(label,term,col) in enumerate([
 ('التدريب','FIT IMPUTER',TURQ),
 ('الاختبار','APPLY ONLY',YELLOW)]):
 y=460+j*226
 box(d,(113,y,607,y+178),fill='#1C5064',outline=col,rad=26)
 ar(d,label,(W//2,y+58),37,WHITE,True)
 en(d,term,(W//2,y+127),26,col)
im.save(P/'corrected_04.png')

# 6. Question and concise answer.
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','افهم سبب الفقد قبل التعويض')
ar(d,'هل الفراغ يساوي صفرًا؟',(W//2,500),37,WHITE,True)
box(d,(104,624,615,774),fill='#176364',outline=TURQ,rad=28)
ar(d,'لا! لا تَخْتَرِع قيمة',(W//2,695),34,WHITE,True)
ar(d,'افحص السبب ثم اختبر الحل',(W//2,940),30,YELLOW,True)
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

with wave.open(str(P/'output/HAI-C0049_arabic_voice_master.wav')) as wf: duration=wf.getnframes()/wf.getframerate()
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
cmd=[ffmpeg_bin,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(P/'scenes.ffconcat'),'-i',str(P/'output/HAI-C0049_arabic_voice_master.wav'),'-r','30','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(duration),'-shortest',str(P/'HAI-C0049-missing-data-AR-fixed.mp4')]
subprocess.run(cmd,cwd=P,check=True)
print('Created',str(P/'HAI-C0049-missing-data-AR-fixed.mp4'))