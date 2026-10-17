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
 en(d,f'HAI-C0046   |   {i+1}/6',(W//2,1243),18,MUTED)
 return im,d





def shape(d,x,y,minor=False,s=1):
 r=int(18*s)
 if minor:d.polygon([(x,y-r),(x-r,y+r),(x+r,y+r)],fill=RED)
 else:d.ellipse((x-r,y-r,x+r,y+r),fill=TURQ)
def group(d,nmajor,nminor,y0=500,spacing=67):
 for j in range(nmajor+nminor):
  shape(d,170+(j%6)*spacing,y0+(j//6)*spacing,j>=nmajor,1.0)

im,d=base(0,'دقة عالية... وخطأ كبير؟','CLASS IMBALANCE','احذر خداع متوسط الدقة')
group(d,9,1,514,80)
ar(d,'تسع دوائر ومثلث واحد',(W//2,946),29,YELLOW,True)
im.save(P/'corrected_00.png')

im,d=base(1,'فئة أكثر من أخرى','UNBALANCED CLASSES','في هذا المثال: تسعين دائرة وعشرة مثلثات')
for row in range(4):
 for col in range(8):
  shape(d,156+col*59,485+row*89,(row==3 and col>=4),.8)
ar(d,'فئات غير متساوية',(W//2,954),29,YELLOW,True)
im.save(P/'corrected_01.png')

im,d=base(2,'توقع الدائرة دائمًا','ALWAYS GUESS CIRCLE','قد تبدو الدقة العامة مرتفعة')
for j in range(10):
 shape(d,150+j*43,543,j==9,.65)
box(d,(144,675,575,781),fill='#1A5660',outline=TURQ,rad=21)
ar(d,'جميع التوقعات: دائرة',(W//2,727),27,WHITE,True)
ar(d,'هل تعلّم المثلث؟',(W//2,930),31,RED,True)
im.save(P/'corrected_02.png')

im,d=base(3,'المثلثات لم تُكتشف','MINORITY CLASS','نموذج مهمل لفئة كاملة')
for j in range(6):
 shape(d,168+j*75,550,True,1.0)
d.line((168,650,545,850),fill=RED,width=7)
ar(d,'الدقة وحدها لا تكفي',(W//2,963),30,YELLOW,True)
im.save(P/'corrected_03.png')

im,d=base(4,'افحص كل فئة','PRECISION • RECALL','قيّم الاسترجاع والأخطاء لكل فئة')
for i,(txt,eng) in enumerate([('الدقة حسب الفئة','PER-CLASS'),('الاسترجاع','RECALL'),('اختبار مستقل','TEST SET')]):
 y=420+i*188
 box(d,(98,y,623,y+143),fill='#195064',outline=TURQ,rad=23)
 ar(d,txt,(W//2,y+55),31,WHITE,True)
 en(d,eng,(W//2,y+112),23,YELLOW)
im.save(P/'corrected_04.png')

im,d=base(5,'سؤال حكيم','THE TAKEAWAY','توازن الفئات مهم لتقييم أفضل')
ar(d,'هل تسعين بالمئة تكفي؟',(W//2,514),34,WHITE,True)
box(d,(100,616,622,768),fill='#175E67',outline=TURQ,rad=26)
ar(d,'ليس لو أهمل المثلثات!',(W//2,684),30,WHITE,True)
ar(d,'اختبر كل فئة لا المجموع فقط',(W//2,929),28,YELLOW,True)
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

with wave.open(str(P/'output/HAI-C0046_arabic_voice_master.wav')) as wf: duration=wf.getnframes()/wf.getframerate()
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
cmd=[ffmpeg_bin,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(P/'scenes.ffconcat'),'-i',str(P/'output/HAI-C0046_arabic_voice_master.wav'),'-r','30','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(duration),'-shortest',str(P/'HAI-C0046-class-imbalance-AR-fixed.mp4')]
subprocess.run(cmd,cwd=P,check=True)
print('Created',str(P/'HAI-C0046-class-imbalance-AR-fixed.mp4'))