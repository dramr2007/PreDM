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
 en(d,f'HAI-C0048   |   {i+1}/6',(W//2,1243),18,MUTED)
 return im,d







# Illustrative height values in cm: 150, 170, 190 -> MinMax: 0, 0.5, 1.
def bar(d,x,y,h,v,color=TURQ):
 d.rounded_rectangle((x,y,x+100,y+h),radius=19,fill='#27516B',outline=CYAN,width=3)
 filled=max(8,int(h*v))
 d.rounded_rectangle((x+5,y+h-filled,x+95,y+h-5),radius=12,fill=color)
def pill(d,rect,text,english=None,col=TURQ):
 box(d,rect,fill='#1E4B61',outline=col,rad=22,width=3)
 x0,y0,x1,y1=rect
 ar(d,text,((x0+x1)//2,y0+44),30,WHITE,True)
 if english:en(d,english,((x0+x1)//2,y1-33),21,YELLOW)

# 1. Hook: show why raw height values can be mapped.
im,d=base(0,'١٥٠، ١٧٠، ١٩٠؟','DATA NORMALIZATION','هل نحولها إلى أرقام بين صفر وواحد؟')
for x,label,h,c in [(192,'١٥٠',154,TURQ),(355,'١٧٠',224,CYAN),(517,'١٩٠',298,YELLOW)]:
 d.line((x-7,809-h,x-7,844),fill=WHITE,width=4)
 d.ellipse((x-34,702-h,x+34,764-h),fill=c)
 d.rounded_rectangle((x-26,762-h,x+26,845),radius=20,fill=c)
 ar(d,label,(x,914),30,WHITE,True)
ar(d,'قيم بالسنتيمتر',(W//2,980),26,YELLOW)
im.save(P/'corrected_00.png')

# 2. Explain that Min-Max is a specific scaling method.
im,d=base(1,'طريقة مين ماكس','MIN–MAX SCALING','نستخدم أصغر وأكبر قيمة من التدريب')
pill(d,(101,445,618,591),'أصغر قيمة: ١٥٠','MIN = 150',TURQ)
pill(d,(101,642,618,790),'أكبر قيمة: ١٩٠','MAX = 190',YELLOW)
en(d,'(x - min) / (max - min)',(W//2,901),28,WHITE,heavy=True)
ar(d,'قاعدة حساب واضحة',(W//2,973),27,CYAN)
im.save(P/'corrected_01.png')

# 3. Show explicit input-to-output mapping.
im,d=base(2,'شاهد التحويل','VALUE MAPPING','كل قيمة تُقاس بالنسبة إلى الحدود')
for y,a,b,c in [(473,'١٥٠','٠',TURQ),(662,'١٧٠','٠٫٥',CYAN),(851,'١٩٠','١',YELLOW)]:
 box(d,(105,y,309,y+121),fill='#204A5E',outline=c,rad=21)
 box(d,(414,y,615,y+121),fill='#26536A',outline=c,rad=21)
 ar(d,a,(209,y+61),37,WHITE,True)
 ar(d,b,(515,y+61),37,WHITE,True)
 d.line((326,y+62,393,y+62),fill=c,width=6)
 d.polygon([(387,y+46),(411,y+62),(387,y+78)],fill=c)
im.save(P/'corrected_02.png')

# 4. Model-dependent benefit and difference from standardization.
im,d=base(3,'متى يفيد؟','SCALE-SENSITIVE MODELS','بعض الخوارزميات تتأثر بحجم الأرقام')
for j,(name,e,col) in enumerate([('قبل التوحيد','BEFORE',RED),('بعد مين ماكس','AFTER MIN–MAX',TURQ)]):
 y=441+j*250
 box(d,(101,y,617,y+204),fill='#1C4E62',outline=col,rad=24)
 ar(d,name,(W//2,y+54),31,WHITE,True)
 en(d,e,(W//2,y+100),23,YELLOW)
 for k,v in enumerate(([.14,.45,.9] if j==0 else [0,.5,1])):
  xx=213+145*k
  d.rounded_rectangle((xx-36,y+142,xx+36,y+178),radius=9,fill='#163449')
  d.rectangle((xx-34,y+176-int(32*v),xx+34,y+176),fill=col)
ar(d,'ليس ضروريًا لكل نموذج',(W//2,958),26,YELLOW)
im.save(P/'corrected_03.png')

# 5. No leakage. Train min/max ONLY on train.
im,d=base(4,'انتبه لتسرّب المعلومات','AVOID DATA LEAKAGE','تعلّم الحدود من التدريب فقط')
pill(d,(102,452,621,600),'التدريب: نحسب الحدود','FIT TRAIN',TURQ)
pill(d,(102,648,621,794),'الاختبار: نطبّقها','TRANSFORM TEST',YELLOW)
ar(d,'لا نتعلم الحدود من الاختبار',(W//2,953),28,RED,True)
im.save(P/'corrected_04.png')

# 6. The quiz: new values may exceed training range.
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','حدود التدريب لا تشمل كل المستقبل')
ar(d,'ماذا لو جاء طول ٢٠٠؟',(W//2,487),38,WHITE,True)
box(d,(94,612,630,770),fill='#1D606A',outline=TURQ,rad=28)
ar(d,'قد تكون النتيجة أكبر من ١',(W//2,674),31,WHITE,True)
en(d,'(200 - 150) / (190 - 150) = 1.25',(W//2,736),20,YELLOW)
ar(d,'إذن لا نعمّم بلا اختبار',(W//2,942),28,CYAN,True)
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

with wave.open(str(P/'output/HAI-C0048_arabic_voice_master.wav')) as wf: duration=wf.getnframes()/wf.getframerate()
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
cmd=[ffmpeg_bin,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(P/'scenes.ffconcat'),'-i',str(P/'output/HAI-C0048_arabic_voice_master.wav'),'-r','30','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(duration),'-shortest',str(P/'HAI-C0048-normalization-AR-fixed.mp4')]
subprocess.run(cmd,cwd=P,check=True)
print('Created',str(P/'HAI-C0048-normalization-AR-fixed.mp4'))