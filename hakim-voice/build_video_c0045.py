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
 en(d,f'HAI-C0045   |   {i+1}/6',(W//2,1243),18,MUTED)
 return im,d




# HAI-C0045: visually accurate, fictional examples, six scenes.

# Illustrations deliberately conceptual, not measured performance.
def vehicle(d,x,y,color=TURQ):
 d.rounded_rectangle((x-75,y,x+75,y+49),radius=15,fill=color)
 d.polygon([(x-40,y),(x-25,y-34),(x+33,y-34),(x+55,y)],fill=color)
 d.ellipse((x-54,y+34,x-23,y+66),fill=NAVY,outline=WHITE,width=2)
 d.ellipse((x+28,y+34,x+59,y+66),fill=NAVY,outline=WHITE,width=2)
def sky(d,x,y,night=False):
 if night:
  d.ellipse((x-35,y-35,x+35,y+35),fill=PALE)
  d.ellipse((x-14,y-41,x+42,y+20),fill='#20344D')
 else:
  d.ellipse((x-36,y-36,x+36,y+36),fill=YELLOW)

im,d=base(0,'هل ينجح ليلًا؟','DATA REPRESENTATION','ما يتعلّمه نهارًا قد لا يكفي ليلًا')
for x,night in [(205,False),(505,True)]:
 box(d,(x-114,425,x+114,882),fill='#295C66' if not night else '#1D3556',rad=26)
 sky(d,x,530,night);vehicle(d,x,716,CYAN if night else TURQ)
 ar(d,'ليل' if night else 'نهار',(x,859),34,WHITE,True)
im.save(P/'corrected_00.png')

im,d=base(1,'انحياز التمثيل','REPRESENTATION BIAS','هل شملت بيانات التدريب كل الظروف؟')
for x in (190,355,520):
 sky(d,x,527);vehicle(d,x,721,TURQ)
ar(d,'أمثلة كثيرة في النهار',(W//2,944),29,YELLOW,True)
im.save(P/'corrected_01.png')

im,d=base(2,'تغيّرت الإضاءة','NEW LIGHTING','اختبار النموذج على صور لم يرها')
box(d,(156,433,561,876),fill='#1E3456',rad=32)
sky(d,350,527,True);vehicle(d,350,730,CYAN)
ar(d,'قد تنخفض الدقة',(W//2,936),31,RED,True)
im.save(P/'corrected_02.png')

im,d=base(3,'المتوسط قد يخدع','GROUP EVALUATION','قارن ظروف الاستخدام المختلفة')
for y,txt,fraction,col in [(500,'النهار',.85,TURQ),(758,'الليل',.38,RED)]:
 ar(d,txt,(W//2,y-60),35,WHITE,True)
 box(d,(110,y,610,y+82),fill='#2A4C62',rad=16)
 box(d,(110,y,110+int(500*fraction),y+82),fill=col,rad=16)
ar(d,'أشرطة توضيحية وليست نتائج حقيقية',(W//2,946),22,YELLOW)
im.save(P/'corrected_03.png')

im,d=base(4,'كيف تختبر بعدل؟','TEST EACH CONDITION','تنوع البيانات لا يلغي ضرورة التقييم')
for j,txt in enumerate(['اختبر النهار والليل','قارن أخطاء كل ظرف','راجع بيانات التدريب']):
 y=420+j*181
 box(d,(97,y,623,y+136),fill='#1D4D62',outline=TURQ,rad=20)
 ar(d,txt,(W//2,y+70),31,WHITE,True)
im.save(P/'corrected_04.png')

im,d=base(5,'سؤال حكيم','CHECK YOUR MODEL','ما وراء الرقم أهم من الرقم')
ar(d,'هل متوسط الدقة يكفي؟',(W//2,506),37,WHITE,True)
box(d,(100,623,621,759),fill='#195D67',outline=TURQ,rad=27)
ar(d,'لا، افحص كل حالة',(W//2,690),34,WHITE,True)
ar(d,'شارِك الحلقة لتعمّ الفائدة',(W//2,925),27,YELLOW,True)
im.save(P/'corrected_05.png')

with wave.open(str(P/'output/HAI-C0045_arabic_voice_master.wav')) as wf: duration=wf.getnframes()/wf.getframerate()
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
cmd=[ffmpeg_bin,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(P/'scenes.ffconcat'),'-i',str(P/'output/HAI-C0045_arabic_voice_master.wav'),'-r','30','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','fast','-crf','22','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(duration),'-shortest',str(P/'HAI-C0045-bias-AR-fixed.mp4')]
subprocess.run(cmd,cwd=P,check=True)
print('Created',str(P/'HAI-C0045-bias-AR-fixed.mp4'))