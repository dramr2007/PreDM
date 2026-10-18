"""HAI-C0054 six concise Arabic RTL infographics + voiced H264/AAC MP4, no source-voice files checked in."""
from pathlib import Path
import subprocess, json, math
from PIL import Image, ImageDraw, ImageFont
import soundfile as sf
P=Path(__file__).resolve().parent
W,H=720,1280
NAVY='#071A2D'; DARK='#092638'; TURQ='#2CE4C6'; CYAN='#87DAE5'; GOLD='#F9CD55'; WHITE='#FFFFFF'; MUTED='#AACBD3'; CORAL='#F88172'
AR='/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf'
ARB='/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf'
EN='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
if not Path(AR).exists(): AR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
if not Path(ARB).exists(): ARB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def ff(n,b=False): return ImageFont.truetype(ARB if b else AR,n)
def fe(n): return ImageFont.truetype(EN,n)
def ar(d,s,x,y,n=34,color=WHITE,b=True):d.text((x,y),s,font=ff(n,b),fill=color,anchor='mm',direction='rtl',language='ar',stroke_width=0)
def en(d,s,x,y,n=24,color=CYAN):d.text((x,y),s,font=fe(n),fill=color,anchor='mm')
def box(d,b,fill=DARK,outline=None,r=23,w=3):d.rounded_rectangle(b,fill=fill,radius=r,outline=outline,width=w)
def robot(d,x,y,scale=1):
 # original vector robot mascot, not a reproduction of the HeyGen video
 def pt(a,b):return (int(x+a*scale),int(y+b*scale))
 d.rounded_rectangle((*pt(-65,-55),*pt(65,62)),radius=int(30*scale),fill='#B3EDF0',outline=TURQ,width=4)
 d.rounded_rectangle((*pt(-49,-36),*pt(49,22)),radius=int(16*scale),fill='#10455B')
 for off in (-25,25):d.ellipse((*pt(off-8,-14),*pt(off+8,2)),fill=TURQ)
 d.arc((*pt(-25,-8),*pt(25,27)),start=25,end=155,fill=GOLD,width=3)
 d.line([pt(0,-54),pt(0,-81)],fill=CYAN,width=5)
 d.ellipse((*pt(-8,-93),*pt(8,-77)),fill=GOLD)
 d.rounded_rectangle((*pt(-36,48),*pt(36,76)),radius=12,fill='#386879')
def base(k,title,sub,kicker):
 im=Image.new('RGB',(W,H),NAVY);d=ImageDraw.Draw(im)
 for y in range(H):
  d.line((0,y,W,y),fill=(7+int(4*y/H),25+int(12*y/H),44+int(12*y/H)))
 # visual spine
 box(d,(28,29,692,116),fill='#134B55',r=22)
 en(d,'HAKIM AI',275,72,38,TURQ)
 robot(d,614,70,.24)
 ar(d,title,360,201,42)
 en(d,sub,360,274,25,GOLD)
 box(d,(42,342,678,1000),fill='#123549',outline='#357687',r=30)
 ar(d,kicker,360,1051,25,CYAN)
 en(d,'Dr\\Amr kamel kahlil ahmed',360,1184,20,MUTED)
 en(d,f'HAI-C0054  |  {k+1}/6',360,1228,17,MUTED)
 return im, d
def arrow(d,x0,y0,x1,y1,col=TURQ,width=9):
 d.line((x0,y0,x1,y1),fill=col,width=width)
 t=math.atan2(y1-y0,x1-x0)
 d.polygon([(x1,y1),(x1-24*math.cos(t-.55),y1-24*math.sin(t-.55)),(x1-24*math.cos(t+.55),y1-24*math.sin(t+.55))],fill=col)
def road(d):
 d.line((110,832,610,832),fill='#608397',width=12)
 for x in range(118,615,77):d.line((x,832,x+32,832),fill=GOLD,width=5)

def token(d,x,y,color,shape='circle',scale=1):
 r=int(28*scale)
 if shape=='circle': d.ellipse((x-r,y-r,x+r,y+r),fill=color)
 elif shape=='square': d.rounded_rectangle((x-r,y-r,x+r,y+r),radius=10,fill=color)
 else: d.polygon([(x,y-r),(x-r,y+r),(x+r,y+r)],fill=color)

def neural_graph(d,values=None):
 xs=[160,315,480,603]
 ys=[[575,720,855],[500,615,730,845],[570,710,850],[710]]
 for col in range(3):
  for yy in ys[col]:
   for zz in ys[col+1]:
    d.line((xs[col],yy,xs[col+1],zz),fill='#4B8991',width=2)
 for col in range(4):
  for yy in ys[col]:
   d.ellipse((xs[col]-19,yy-19,xs[col]+19,yy+19),fill=TURQ if col<3 else GOLD,outline=WHITE,width=2)
#1 
im,d=base(0,'كيف تتعلم الآلة؟','NEURAL NETWORK','شبكة من وحدات حسابية')
neural_graph(d)
ar(d,'حسابات مترابطة',360,958,29,GOLD)
im.save(P/'voice54_scene_0.png')
#2
im,d=base(1,'شبكة عصبية اصطناعية','ARTIFICIAL NEURAL NETWORK','مدخلات، طبقات، نتيجة')
neural_graph(d)
en(d,'INPUT',159,933,18,GOLD)
en(d,'HIDDEN LAYERS',384,933,18,CYAN)
en(d,'OUTPUT',602,933,18,GOLD)
im.save(P/'voice54_scene_1.png')
#3
im,d=base(2,'الأوزان تتغير','LEARNED WEIGHTS','نعدّل الروابط أثناء التدريب')
neural_graph(d)
box(d,(139,422,594,505),fill='#21515D',outline=TURQ,r=21)
en(d,'WEIGHTS',366,462,32,GOLD)
im.save(P/'voice54_scene_2.png')
#4
im,d=base(3,'تمر البيانات عبر الطبقات','FEATURES -> PREDICTION','مثال: تقدير شكلٍ من صورة')
neural_graph(d)
box(d,(134,903,584,981),fill='#145866',outline=TURQ,r=19)
ar(d,'مدخلات ← نتيجة متوقعة',358,941,25)
im.save(P/'voice54_scene_3.png')
#5
im,d=base(4,'لكنها ليست دماغًا','NOT A HUMAN BRAIN','تشبيه مفيد، وليس تطابقًا')
box(d,(103,494,623,781),fill='#2A3B56',outline=CORAL,r=25)
ar(d,'نموذج رياضي',362,578,39,WHITE)
en(d,'MATHEMATICAL MODEL',362,660,24,GOLD)
ar(d,'قابل للتقييم',362,729,28,CYAN)
im.save(P/'voice54_scene_4.png')
#6
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','هل رسم الدوائر يثبت أنها تفكر؟')
box(d,(104,517,614,775),fill='#185B66',outline=TURQ,r=25)
ar(d,'لا',360,591,57,GOLD)
ar(d,'هي حسابات وتعلّم',360,696,32,WHITE)
en(d,'VERIFY BEFORE YOU TRUST',360,858,22,CYAN)
im.save(P/'voice54_scene_5.png')

sound=P/'HAI-C0054_neural-network_approved_voice.wav'
assert sound.is_file() and sound.stat().st_size > 10000,'Voice missing'
sample,sr=sf.read(sound)
duration=len(sample)/sr
assert 10 < duration < 65
weights=[.17,.15,.21,.20,.17,.10]
times=[round(duration*w,3) for w in weights]
times[-1]=round(duration-sum(times[:-1])+.35,3)
assert sum(times)>duration
movie=P/'HAI-C0054-neural-network-VOICE-REVIEW.mp4'
args=['ffmpeg','-hide_banner','-loglevel','error','-y']
for i,sec in enumerate(times):
 args+=['-loop','1','-framerate','30','-t',str(sec),'-i',str(P/f'voice54_scene_{i}.png')]
args+=['-i',str(sound)]
flt=[f'[{i}:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v{i}]' for i in range(6)]
flt+=['[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[vo]','[6:a]apad=pad_dur=0.35,aresample=44100[ao]']
args+=['-filter_complex',';'.join(flt),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','fast','-crf','21','-c:a','aac','-b:a','192k','-ar','44100','-t',str(round(duration+.35,3)),'-movflags','+faststart',str(movie)]
subprocess.run(args,check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(movie),'-f','null','-'],check=True)
print('RENDER SUCCESS',movie,round(duration,2),movie.stat().st_size,flush=True)
