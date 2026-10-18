"""HAI-C0059 six concise Arabic RTL infographics + voiced H264/AAC MP4, no source-voice files checked in."""
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
 en(d,f'HAI-C0059  |  {k+1}/6',360,1228,17,MUTED)
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



def model(d,x,y,scale,label,col):
 ww=int(240*scale);hh=int(205*scale)
 box(d,(x-ww//2,y-hh//2,x+ww//2,y+hh//2),fill='#1A5163',outline=col,r=23)
 ar(d,label,x,y-13,29 if scale>=1 else 25,WHITE)
 en(d,'MODEL',x,y+45,18,col)
#1
im,d=base(0,'هل يتعلّم الصغير من الكبير؟','DISTILLATION','نموذج يساعد على تدريب آخر')
model(d,217,616,1.2,'المعلم',GOLD)
model(d,510,667,.8,'الطالب',TURQ)
arrow(d,343,622,415,655,CYAN,9)
ar(d,'المعرفة ليست مجرد نسخ',360,937,26,WHITE)
im.save(P/'voice59_scene_0.png')
#2
im,d=base(1,'ما هو تقطير المعرفة؟','KNOWLEDGE DISTILLATION','استخدام إشارات معلم لتدريب طالب')
model(d,218,594,1.15,'نموذج كبير',GOLD)
model(d,517,748,.75,'نموذج أصغر',TURQ)
arrow(d,355,611,430,723,CYAN,10)
ar(d,'تدريب على مخرجات المعلم',360,971,23,WHITE)
im.save(P/'voice59_scene_1.png')
#3
im,d=base(2,'توقعات المعلم','TEACHER PREDICTIONS','مثال على مهمة محددة')
for i,(word,english,color) in enumerate([('بيانات أمثلة','INPUT EXAMPLES',TURQ),('توقعات المعلم','SOFT TARGETS',GOLD),('تدريب الطالب','STUDENT TRAINING',CYAN)]):
 y=422+i*174;box(d,(108,y,613,y+143),fill='#1C5164',outline=color,r=20)
 ar(d,word,360,y+58,31)
 en(d,english,360,y+113,20,color)
im.save(P/'voice59_scene_2.png')
#4
im,d=base(3,'نموذج أخفّ أحيانًا','MODEL COMPRESSION','لكن الحجم الأصغر ليس ضمانًا')
model(d,210,623,1.2,'كبير',GOLD)
model(d,519,623,.7,'صغير',CYAN)
ar(d,'قارن الذاكرة والسرعة والدقة',360,937,25,WHITE)
im.save(P/'voice59_scene_3.png')
#5
im,d=base(4,'قد يرث الأخطاء','ERROR PROPAGATION','اختبر الطالب على بيانات مستقلة')
box(d,(110,458,610,626),fill='#21535E',outline=TURQ,r=24)
ar(d,'المعلم قد يخطئ',360,528,32,WHITE)
box(d,(110,707,610,876),fill='#543C43',outline=CORAL,r=24)
ar(d,'الطالب قد يقلّده',360,777,32,WHITE)
im.save(P/'voice59_scene_4.png')
#6
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','هل تقليد المعلم يضمن أداءً أفضل؟')
box(d,(110,500,611,776),fill='#165B66',outline=TURQ,r=27)
ar(d,'لا',360,590,62,GOLD)
ar(d,'التقييم المستقل ضروري',360,699,29,WHITE)
en(d,'EVALUATE INDEPENDENTLY',360,879,22,CYAN)
im.save(P/'voice59_scene_5.png')

sound=P/'HAI-C0059_distillation_approved_voice.wav'
assert sound.is_file() and sound.stat().st_size > 10000,'Voice missing'
sample,sr=sf.read(sound)
duration=len(sample)/sr
assert 10 < duration < 65
weights=[.17,.15,.21,.20,.17,.10]
times=[round(duration*w,3) for w in weights]
times[-1]=round(duration-sum(times[:-1])+.35,3)
assert sum(times)>duration
movie=P/'HAI-C0059-distillation-VOICE-REVIEW.mp4'
args=['ffmpeg','-hide_banner','-loglevel','error','-y']
for i,sec in enumerate(times):
 args+=['-loop','1','-framerate','30','-t',str(sec),'-i',str(P/f'voice59_scene_{i}.png')]
args+=['-i',str(sound)]
flt=[f'[{i}:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v{i}]' for i in range(6)]
flt+=['[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[vo]','[6:a]apad=pad_dur=0.35,aresample=44100[ao]']
args+=['-filter_complex',';'.join(flt),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','fast','-crf','21','-c:a','aac','-b:a','192k','-ar','44100','-t',str(round(duration+.35,3)),'-movflags','+faststart',str(movie)]
subprocess.run(args,check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(movie),'-f','null','-'],check=True)
print('RENDER SUCCESS',movie,round(duration,2),movie.stat().st_size,flush=True)
