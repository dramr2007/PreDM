"""HAI-C0058 six concise Arabic RTL infographics + voiced H264/AAC MP4, no source-voice files checked in."""
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
 en(d,f'HAI-C0058  |  {k+1}/6',360,1228,17,MUTED)
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


def chain(d,layer_count=4,low=520,high=830):
 start,end=130,590
 xs=[start+(end-start)*k/(layer_count-1) for k in range(layer_count)]
 ys=[]
 for j in range(layer_count):
  num=2 if j in (0,layer_count-1) else 3
  ys.append([low+(high-low)*(m+1)/(num+1) for m in range(num)])
 for j in range(layer_count-1):
  for v in ys[j]:
   for w in ys[j+1]:
    d.line((xs[j],v,xs[j+1],w),fill='#42899D',width=2)
 for j in range(layer_count):
  for v in ys[j]:
   d.ellipse((xs[j]-15,v-15,xs[j]+15,v+15),fill=GOLD if j==layer_count-1 else TURQ,outline=WHITE,width=2)


def model_rect(d,y,title,sub,color=TURQ):
 box(d,(120,y,601,y+145),fill='#245064',outline=color,r=22)
 ar(d,title,361,y+52,32,WHITE)
 en(d,sub,360,y+109,20,color)
# 1
im,d=base(0,'رفعت ملفًا.. هل درّبت النموذج؟','FINE-TUNING','ملف السياق ليس تدريبًا جديدًا')
model_rect(d,465,'ملف مرفق','CONTEXT FILE',GOLD)
arrow(d,360,637,360,754,CYAN,8)
model_rect(d,775,'سؤال وإجابة','USE AS CONTEXT',TURQ)
im.save(P/'voice58_scene_0.png')
# 2
im,d=base(1,'ما هو الضبط الدقيق؟','FINE-TUNING','نواصل تدريب نموذج موجود')
model_rect(d,445,'النموذج الأساسي','BASE MODEL',TURQ)
arrow(d,360,606,360,716,GOLD,9)
model_rect(d,739,'تدريب إضافي','ADDITIONAL TRAINING',GOLD)
ar(d,'قد تتغير الأوزان',360,950,26,WHITE)
im.save(P/'voice58_scene_1.png')
# 3
im,d=base(2,'ما الذي يتغيّر؟','TRAINABLE WEIGHTS','خلال التدريب يتعلّم النموذج من أمثلة')
for k,(txt,eng,col) in enumerate([('بيانات تدريب','TRAINING EXAMPLES',TURQ),('تحديث الأوزان','WEIGHT UPDATES',GOLD),('تقييم الجودة','EVALUATION',CYAN)]):
 y=436+k*174;model_rect(d,y,txt,eng,col)
im.save(P/'voice58_scene_2.png')
# 4
im,d=base(3,'لكن رفع الملف مختلف','CONTEXT VS TRAINING','إرفاق السياق لا يغيّر الأوزان تلقائيًا')
model_rect(d,460,'رفع ملف','ATTACH A FILE',CYAN)
model_rect(d,724,'الضبط الدقيق','TRAINING WEIGHTS',GOLD)
ar(d,'طريقتان مختلفتان',360,970,27,WHITE)
im.save(P/'voice58_scene_3.png')
# 5
im,d=base(4,'مثال على التدريب','EDUCATIONAL ANSWERS','أمثلة تعليمية مع تقييم مستمر')
for k,(word,eng,color) in enumerate([('أمثلة مراجَعة','CURATED SAMPLES',TURQ),('تدريب إضافي','FINE-TUNING',GOLD),('تقييم مستقل','HOLDOUT TEST',CYAN)]):
 y=435+k*179;model_rect(d,y,word,eng,color)
im.save(P/'voice58_scene_4.png')
# 6
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','هل كل ملف مرفق يغيّر النموذج؟')
box(d,(120,512,610,787),fill='#185E69',outline=TURQ,r=28)
ar(d,'لا',360,589,60,GOLD)
ar(d,'السياق لا يساوي التدريب',360,703,30,WHITE)
en(d,'CONTEXT ≠ FINE-TUNING',360,884,20,CYAN)
im.save(P/'voice58_scene_5.png')

sound=P/'HAI-C0058_fine-tuning_approved_voice.wav'
assert sound.is_file() and sound.stat().st_size > 10000,'Voice missing'
sample,sr=sf.read(sound)
duration=len(sample)/sr
assert 10 < duration < 65
weights=[.17,.15,.21,.20,.17,.10]
times=[round(duration*w,3) for w in weights]
times[-1]=round(duration-sum(times[:-1])+.35,3)
assert sum(times)>duration
movie=P/'HAI-C0058-fine-tuning-VOICE-REVIEW.mp4'
args=['ffmpeg','-hide_banner','-loglevel','error','-y']
for i,sec in enumerate(times):
 args+=['-loop','1','-framerate','30','-t',str(sec),'-i',str(P/f'voice58_scene_{i}.png')]
args+=['-i',str(sound)]
flt=[f'[{i}:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v{i}]' for i in range(6)]
flt+=['[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[vo]','[6:a]apad=pad_dur=0.35,aresample=44100[ao]']
args+=['-filter_complex',';'.join(flt),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','fast','-crf','21','-c:a','aac','-b:a','192k','-ar','44100','-t',str(round(duration+.35,3)),'-movflags','+faststart',str(movie)]
subprocess.run(args,check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(movie),'-f','null','-'],check=True)
print('RENDER SUCCESS',movie,round(duration,2),movie.stat().st_size,flush=True)
