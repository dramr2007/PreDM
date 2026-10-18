"""HAI-C0053 six concise Arabic RTL infographics + voiced H264/AAC MP4, no source-voice files checked in."""
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
 en(d,f'HAI-C0053  |  {k+1}/6',360,1228,17,MUTED)
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
#1 Hook about arranging unlabeled buttons
im,d=base(0,'كيف نرتبها؟','UNLABELED ITEMS','أنماط بلا أسماء جاهزة')
for x,y,color,shape in [(194,545,TURQ,'circle'),(320,522,TURQ,'square'),(489,585,GOLD,'circle'),(182,794,GOLD,'square'),(369,741,CYAN,'circle'),(525,823,TURQ,'square')]:
 token(d,x,y,color,shape,1.25)
en(d,'NO LABELS',360,930,22,GOLD)
im.save(P/'voice53_scene_0.png')
#2 Describe clustering
im,d=base(1,'هذا هو التجميع','CLUSTERING','نبحث عن التقارب بين العناصر')
box(d,(114,450,613,638),fill='#145563',outline=TURQ)
ar(d,'متشابهة',360,524,49,WHITE)
en(d,'SIMILAR ITEMS',360,603,24,GOLD)
for xx,cc in [(210,TURQ),(360,CYAN),(514,GOLD)]:
 token(d,xx,804,cc,'circle',1.4)
im.save(P/'voice53_scene_1.png')
#3 Define selected features explicitly
im,d=base(2,'نقارن صفاتها','FEATURES','اللون، الحجم، الشكل')
for idx,(txt,eng,col) in enumerate([('لون','COLOR',TURQ),('حجم','SIZE',CYAN),('شكل','SHAPE',GOLD)]):
 yy=440+idx*166
 box(d,(123,yy,601,yy+137),fill='#214E63',outline=col)
 ar(d,txt,360,yy+50,38)
 en(d,eng,360,yy+112,21,col)
im.save(P/'voice53_scene_2.png')
#4 Groups illustrate sorting
im,d=base(3,'تظهر مجموعات','GROUPS','طريقة التشابه تحدد النتيجة')
box(d,(103,444,343,851),fill='#174B59',outline=TURQ)
box(d,(378,444,619,851),fill='#53462F',outline=GOLD)
for x,y in [(181,561),(274,602),(200,735),(274,776)]:
 token(d,x,y,TURQ,'circle',.8)
for x,y in [(453,561),(545,612),(461,719),(547,783)]:
 token(d,x,y,GOLD,'square',.8)
en(d,'GROUP A',221,911,22,CYAN)
en(d,'GROUP B',499,911,22,GOLD)
im.save(P/'voice53_scene_3.png')
#5 Caution about metrics
im,d=base(4,'قد تتغيّر النتائج','DISTANCE MATTERS','غيّر معيار التشابه فتختلف المجموعات')
box(d,(91,455,619,638),fill='#1A5761',outline=TURQ)
ar(d,'التشابه باللون',360,528,33)
en(d,'COLOR',360,599,24,GOLD)
box(d,(91,701,619,882),fill='#405067',outline=CYAN)
ar(d,'التشابه بالشكل',360,761,33)
en(d,'SHAPE',360,846,24,GOLD)
im.save(P/'voice53_scene_4.png')
#6 Quiz answer
im,d=base(5,'سؤال حكيم','THE TAKEAWAY','هل المجموعات حقيقة نهائية؟')
box(d,(104,500,613,779),fill='#1A5961',outline=TURQ,r=28)
ar(d,'لا',360,566,65,GOLD)
ar(d,'تعتمد على الطريقة',360,689,37,WHITE)
en(d,'METHOD DEPENDENT',360,880,22,CYAN)
im.save(P/'voice53_scene_5.png')

sound=P/'HAI-C0053_clustering_approved_voice.wav'
assert sound.is_file() and sound.stat().st_size > 10000,'Voice missing'
sample,sr=sf.read(sound)
duration=len(sample)/sr
assert 10 < duration < 65
weights=[.17,.15,.21,.20,.17,.10]
times=[round(duration*w,3) for w in weights]
times[-1]=round(duration-sum(times[:-1])+.35,3)
assert sum(times)>duration
movie=P/'HAI-C0053-clustering-VOICE-REVIEW.mp4'
args=['ffmpeg','-hide_banner','-loglevel','error','-y']
for i,sec in enumerate(times):
 args+=['-loop','1','-framerate','30','-t',str(sec),'-i',str(P/f'voice53_scene_{i}.png')]
args+=['-i',str(sound)]
flt=[f'[{i}:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v{i}]' for i in range(6)]
flt+=['[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[vo]','[6:a]apad=pad_dur=0.35,aresample=44100[ao]']
args+=['-filter_complex',';'.join(flt),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','fast','-crf','21','-c:a','aac','-b:a','192k','-ar','44100','-t',str(round(duration+.35,3)),'-movflags','+faststart',str(movie)]
subprocess.run(args,check=True)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(movie),'-f','null','-'],check=True)
print('RENDER SUCCESS',movie,round(duration,2),movie.stat().st_size,flush=True)
