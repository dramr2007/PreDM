"""HAI-C0056 six concise Arabic RTL infographics + voiced H264/AAC MP4, no source-voice files checked in."""
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
 en(d,f'HAI-C0056  |  {k+1}/6',360,1228,17,MUTED)
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
#1 hook
im,d=base(0,'هل لكلمة «عين» معنى واحد؟','TRANSFORMER','السياق يحدّد المعنى')
for x,txt,col in [(145,'عين',GOLD),(360,'ماء',TURQ),(575,'رؤية',CYAN)]:
 box(d,(x-80,575,x+80,710),fill='#205265',outline=col)
 ar(d,txt,x,642,31)
d.line((225,642,280,642),fill=TURQ,width=7); d.line((440,642,495,642),fill=CYAN,width=7)
en(d,'CONTEXT CHANGES MEANING',360,895,23,GOLD)
im.save(P/'voice56_scene_0.png')
#2 definition
im,d=base(1,'ما هو المحوّل؟','TRANSFORMER','انتباه يربط عناصر التسلسل')
chain(d,6)
en(d,'ATTENTION CONNECTS CONTEXT',360,930,21,CYAN)
im.save(P/'voice56_scene_1.png')
#3 change from simple to sophisticated
im,d=base(2,'كل كلمة تنظر للسياق','SELF-ATTENTION','روابط مفيدة تحصل على وزن أكبر')
for i,(txt,eng,col) in enumerate([('الكلمة','TOKEN',TURQ),('السياق','CONTEXT',CYAN),('الوزن','WEIGHT',GOLD)]):
 y=453+i*163
 box(d,(103,y,616,y+138),fill='#205265',outline=col)
 ar(d,txt,360,y+48,36)
 en(d,eng,360,y+105,22,col)
im.save(P/'voice56_scene_2.png')
#4 example
im,d=base(3,'المعنى يتبدّل بالسياق','CONTEXTUAL MEANING','الكلمات المحيطة تغيّر التمثيل')
for y,phrase,col in [(510,'عين الماء',TURQ),(735,'عين الإنسان',GOLD)]:
 box(d,(120,y,600,y+125),fill='#205265',outline=col)
 ar(d,phrase,360,y+62,34)
arrow(d,360,855,360,910)
ar(d,'تمثيل مختلف',360,950,28)
im.save(P/'voice56_scene_3.png')
#5 caveat
im,d=base(4,'الانتباه ليس وعيًا','ATTENTION ≠ CONSCIOUSNESS','بنية حسابية تحتاج تقييمًا')
for i,(v,clr) in enumerate([('حساب أوزان',TURQ),('سياق محدود',CYAN),('تقييم مستقل',GOLD)]):
 y=440+i*176
 box(d,(96,y,622,y+132),fill='#205363',outline=clr)
 ar(d,v,360,y+66,29)
im.save(P/'voice56_scene_4.png')
#6 Q&A
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','هل المحوّلات للنص فقط؟')
box(d,(113,506,610,773),fill='#1B5966',outline=TURQ,r=29)
ar(d,'لا',360,585,59,GOLD)
ar(d,'تعمل مع صور وصوت أيضًا',360,704,30)
en(d,'TEXT • IMAGE • AUDIO',360,873,22,CYAN)
im.save(P/'voice56_scene_5.png')

sound=P/'HAI-C0056_transformer_approved_voice.wav'
assert sound.is_file() and sound.stat().st_size > 10000,'Voice missing'
sample,sr=sf.read(sound)
duration=len(sample)/sr
assert 10 < duration < 65
weights=[.17,.15,.21,.20,.17,.10]
times=[round(duration*w,3) for w in weights]
times[-1]=round(duration-sum(times[:-1])+.35,3)
assert sum(times)>duration
movie=P/'HAI-C0056-transformer-VOICE-REVIEW.mp4'
args=['ffmpeg','-hide_banner','-loglevel','error','-y']
for i,sec in enumerate(times):
 args+=['-loop','1','-framerate','30','-t',str(sec),'-i',str(P/f'voice56_scene_{i}.png')]
args+=['-i',str(sound)]
flt=[f'[{i}:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v{i}]' for i in range(6)]
flt+=['[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[vo]','[6:a]apad=pad_dur=0.35,aresample=44100[ao]']
args+=['-filter_complex',';'.join(flt),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','fast','-crf','21','-c:a','aac','-b:a','192k','-ar','44100','-t',str(round(duration+.35,3)),'-movflags','+faststart',str(movie)]
subprocess.run(args,check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(movie),'-f','null','-'],check=True)
print('RENDER SUCCESS',movie,round(duration,2),movie.stat().st_size,flush=True)
