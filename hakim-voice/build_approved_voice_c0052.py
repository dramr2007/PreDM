"""HAI-C0052 six concise Arabic RTL infographics + voiced H264/AAC MP4, no source-voice files checked in."""
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
 en(d,f'HAI-C0052  |  {k+1}/6',360,1228,17,MUTED)
 return im, d
def arrow(d,x0,y0,x1,y1,col=TURQ,width=9):
 d.line((x0,y0,x1,y1),fill=col,width=width)
 t=math.atan2(y1-y0,x1-x0)
 d.polygon([(x1,y1),(x1-24*math.cos(t-.55),y1-24*math.sin(t-.55)),(x1-24*math.cos(t+.55),y1-24*math.sin(t+.55))],fill=col)
def road(d):
 d.line((110,832,610,832),fill='#608397',width=12)
 for x in range(118,615,77):d.line((x,832,x+32,832),fill=GOLD,width=5)
#1
im,d=base(0,'توقّع زمن الرحلة؟','REGRESSION','رقم مُتوقَّع... وليس فئة')
box(d,(122,479,598,681),fill='#204A63',outline=TURQ,r=26)
ar(d,'٢٠ دقيقة',360,563,61,GOLD)
en(d,'ESTIMATED TIME',360,628,24,CYAN)
road(d)
ar(d,'هل هذا وعدٌ بالوصول؟',360,935,29,WHITE)
im.save(P/'voice52_scene_0.png')
#2
im,d=base(1,'ما هو الانحدار؟','REGRESSION','يتوقّع قيمةً عددية')
box(d,(119,476,600,628),fill='#1F5B66',outline=TURQ)
ar(d,'الانحدار',360,537,48,WHITE)
en(d,'PREDICT A NUMBER',360,595,23,GOLD)
for i,(u,v) in enumerate([(170,810),(258,743),(343,720),(428,630),(531,584)]):
 d.ellipse((u-9,v-9,u+9,v+9),fill=CYAN)
d.line([(170,811),(531,585)],fill=GOLD,width=6)
im.save(P/'voice52_scene_1.png')
#3
im,d=base(2,'ما البيانات التي تدخل؟','DISTANCE + TRAFFIC','المسافة والازدحام')
box(d,(82,454,315,652),fill='#234C60',outline=CYAN)
box(d,(408,454,638,652),fill='#234C60',outline=CYAN)
ar(d,'مسافة',198,531,39)
ar(d,'زحام',524,531,39)
en(d,'KM',198,599,23,GOLD)
en(d,'TRAFFIC',524,599,21,GOLD)
arrow(d,360,674,360,786,GOLD,8)
box(d,(178,796,542,909),fill='#136161',outline=TURQ)
ar(d,'الوقت المُتوقَّع',360,851,30,WHITE)
im.save(P/'voice52_scene_2.png')
#4
im,d=base(3,'توقّع، لا ضمان','ESTIMATE != GUARANTEE','قد تتغير ظروف الطريق')
box(d,(104,448,617,657),fill='#1F5064',outline=GOLD)
ar(d,'٢٠ دقيقة',360,532,55,WHITE)
en(d,'MODEL PREDICTION',360,608,23,CYAN)
box(d,(104,707,617,882),fill='#64363E',outline=CORAL)
ar(d,'الزحام قد يزيد',360,779,37,WHITE)
en(d,'REAL WORLD CAN CHANGE',360,838,20,GOLD)
im.save(P/'voice52_scene_3.png')
#5
im,d=base(4,'سؤال حكيم','CLASSIFICATION VS REGRESSION','ما الفرق بين التصنيف والانحدار؟')
box(d,(97,466,619,634),fill='#214D66',outline=CYAN)
ar(d,'التصنيف: اختيار فئة',360,529,32)
en(d,'CIRCLE / TRIANGLE',360,591,22,GOLD)
box(d,(97,697,619,868),fill='#215660',outline=TURQ)
ar(d,'الانحدار: توقّع رقم',360,755,32)
en(d,'20 MINUTES',360,820,24,GOLD)
im.save(P/'voice52_scene_4.png')
#6
im,d=base(5,'الخلاصة في ثانيتين','ONE SIMPLE RULE','خُذها معك')
box(d,(114,499,610,766),fill='#195C68',outline=TURQ,r=28)
ar(d,'الانحدار',360,576,40,GOLD)
ar(d,'يُقدِّر رقمًا',360,685,44,WHITE)
en(d,'REGRESSION => NUMBER',360,837,24,CYAN)
im.save(P/'voice52_scene_5.png')
sound=P/'HAI-C0052_regression_approved_voice.wav'
assert sound.is_file() and sound.stat().st_size > 10000,'Voice missing'
sample,sr=sf.read(sound)
duration=len(sample)/sr
assert 10 < duration < 65
weights=[.19,.16,.19,.20,.19,.07]
times=[round(duration*w,3) for w in weights]
times[-1]=round(duration-sum(times[:-1])+.35,3)
assert sum(times)>duration
movie=P/'HAI-C0052-regression-VOICE-REVIEW.mp4'
args=['ffmpeg','-hide_banner','-loglevel','error','-y']
for i,sec in enumerate(times):
 args+=['-loop','1','-framerate','30','-t',str(sec),'-i',str(P/f'voice52_scene_{i}.png')]
args+=['-i',str(sound)]
flt=[f'[{i}:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v{i}]' for i in range(6)]
flt+=['[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[vo]','[6:a]apad=pad_dur=0.35,aresample=44100[ao]']
args+=['-filter_complex',';'.join(flt),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','fast','-crf','21','-c:a','aac','-b:a','192k','-ar','44100','-t',str(round(duration+.35,3)),'-movflags','+faststart',str(movie)]
subprocess.run(args,check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(movie),'-f','null','-'],check=True)
print('RENDER SUCCESS',movie,round(duration,2),movie.stat().st_size,flush=True)
