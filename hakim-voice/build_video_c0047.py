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
 en(d,f'HAI-C0047   |   {i+1}/6',(W//2,1243),18,MUTED)
 return im,d






# Six original educational scenes: 47 Data Augmentation.
# All leaves illustrative; medically unsafe transforms never demonstrated as validated.
from PIL import ImageEnhance

def leaf(d,cx,cy,rotation=0,shade=TURQ,size=110):
 # rotate only the illustrated leaf, not text; natural leaf with central vein
 cut=Image.new('RGBA',(size*3,size*3),(0,0,0,0))
 z=ImageDraw.Draw(cut)
 c=size*1.5
 z.ellipse((c-size*.72,c-size*.43,c+size*.72,c+size*.43),fill=shade)
 z.line((c-size*.85,c,c+size*.9,c),fill='#E5F6E7',width=4)
 for j in (-.45,-.22,.22,.45):
  x=c+size*j
  z.line((x,c,x+size*.14,c-size*.24*(1 if j<0 else -1)),fill='#E5F6E7',width=3)
 cut=cut.rotate(rotation,resample=Image.Resampling.BICUBIC,expand=False)
 return cut,(int(cx-cut.width/2),int(cy-cut.height/2))
def add_leaf(im,x,y,rot=0,shade=TURQ,size=112):
 pic,loc=leaf(None,x,y,rot,shade,size)
 im.paste(pic,loc,pic)

# Scene 1: Hook
im,d=base(0,'صورة واحدة... أم أمثلة أكثر؟','DATA AUGMENTATION','التنوّع يساعد عند التدريب')
add_leaf(im,204,618,0,TURQ,116)
add_leaf(im,500,618,27,CYAN,116)
d=ImageDraw.Draw(im)
ar(d,'الصورة الأصلية',(204,841),25,WHITE,True)
ar(d,'نسخة معدّلة',(500,841),25,YELLOW,True)
ar(d,'تعلّم الفكرة في أقل من دقيقة',(W//2,970),27,CYAN)
im.save(P/'corrected_00.png')

# Scene 2: Appropriate transform
im,d=base(1,'الورقة من زوايا مختلفة','SMALL ROTATIONS','تغيّر طفيف مع بقاء المعنى')
for x,rot in [(171,0),(354,18),(537,-18)]:
 add_leaf(im,x,630,rot,TURQ,91)
d=ImageDraw.Draw(im)
en(d,'0°',(171,839),24,YELLOW,heavy=True)
en(d,'+18°',(354,839),24,YELLOW,heavy=True)
en(d,'-18°',(537,839),24,YELLOW,heavy=True)
ar(d,'لا تعني التحويلات بيانات جديدة مستقلة',(W//2,965),22,WHITE)
im.save(P/'corrected_01.png')

# Scene 3: Suitable lighting
im,d=base(2,'تغيير الإضاءة','BRIGHTNESS','بحذر وبما يحفظ معلومة الصورة')
for j,(x,fill) in enumerate([(188,'#159D82'),(359,TURQ),(536,'#80FFE3')]):
 box(d,(x-90,474,x+90,792),fill='#1A3949',outline=CYAN,rad=19)
 add_leaf(im,x,642,0,fill,90)
d=ImageDraw.Draw(im)
ar(d,'أمثلة تدريبية متعددة',(W//2,923),30,YELLOW,True)
im.save(P/'corrected_02.png')

# Scene 4: Important medical safeguard
im,d=base(3,'في الطب، احذر!','MEDICAL IMAGING','قد يحذف التعديل علامة تشخيصية')
box(d,(100,458,620,866),fill='#263849',outline=RED,rad=31,width=4)
ar(d,'القلب أو تغيير الألوان',(W//2,552),36,WHITE,True)
ar(d,'ليس آمنًا تلقائيًا',(W//2,641),33,RED,True)
ar(d,'تحقق من صحة كل تحويل',(W//2,766),27,YELLOW)
im.save(P/'corrected_03.png')

# Scene 5: No test leakage
im,d=base(4,'عدّل التدريب فقط','TRAIN ONLY','التقييم يحتاج بيانات مستقلة')
box(d,(94,486,325,782),fill='#1B4C59',outline=TURQ,rad=24)
box(d,(398,486,629,782),fill='#243B55',outline=YELLOW,rad=24)
ar(d,'تدريب',(208,567),29,WHITE,True)
ar(d,'اختبار',(515,567),29,WHITE,True)
add_leaf(im,208,660,19,TURQ,69);add_leaf(im,515,660,0,YELLOW,69)
d=ImageDraw.Draw(im)
ar(d,'نوّع',(208,753),29,TURQ,True)
ar(d,'لا تسرّب',(515,753),29,RED,True)
ar(d,'قسّم أولًا، ثم طبّق التحويلات',(W//2,948),27,WHITE)
im.save(P/'corrected_04.png')

# Scene 6: Question
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','كل تحويل يجب أن يحفظ المعنى')
ar(d,'هل كل تعديل للصورة مفيد؟',(W//2,507),34,WHITE,True)
box(d,(105,612,615,774),fill='#175D68',outline=TURQ,rad=29)
ar(d,'لا... اختبر قبل التعميم',(W//2,698),30,WHITE,True)
ar(d,'تابع حكيم AI للتعلّم خطوة بخطوة',(W//2,930),25,YELLOW)
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

with wave.open(str(P/'output/HAI-C0047_arabic_voice_master.wav')) as wf: duration=wf.getnframes()/wf.getframerate()
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
cmd=[ffmpeg_bin,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(P/'scenes.ffconcat'),'-i',str(P/'output/HAI-C0047_arabic_voice_master.wav'),'-r','30','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(duration),'-shortest',str(P/'HAI-C0047-data-augmentation-AR-fixed.mp4')]
subprocess.run(cmd,cwd=P,check=True)
print('Created',str(P/'HAI-C0047-data-augmentation-AR-fixed.mp4'))