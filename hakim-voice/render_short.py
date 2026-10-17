#!/usr/bin/env python3
"""Produce original educational motion-graphic reel from Piper narration.
No user-identifiable recording or patient data. Public sandbox demonstration.
"""
import os,subprocess,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

OUT=Path("output"); OUT.mkdir(exist_ok=True)
W,H=720,1280
NAVY="#06152C"; TEAL="#14C8C2"; WHITE="#FFFFFF"; LIGHT="#E5FBF6"; MUTE="#93B0C2"; YELLOW="#FFD166"
def sh(s):
    return get_display(arabic_reshaper.reshape(s))
def font(size=38,bold=False):
    names=(["/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
           if bold else ["/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
    for fn in names:
        if Path(fn).exists(): return ImageFont.truetype(fn,size)
    raise FileNotFoundError(names)
def txt(d,y,s,size=41,color=WHITE,bold=False):
    f=font(size,bold); t=sh(s)
    box=d.textbbox((0,0),t,font=f)
    d.text(((W-(box[2]-box[0]))/2,y),t,font=f,fill=color)
def card(d,xy,fill=(17,43,72),r=28):
    d.rounded_rectangle(xy,radius=r,fill=fill,outline=(40,104,112),width=3)
def emoji(d,x,y,r,color):
    d.ellipse((x-r,y-r,x+r,y+r),fill=color,outline=WHITE,width=5)
def make_scene(idx,title,subtitle,label):
    im=Image.new("RGB",(W,H),NAVY)
    d=ImageDraw.Draw(im)
    for y in range(0,H,8):
        n=int(10*math.sin((y/90)+(idx*.65))); d.line((0,y,W,y),fill=(6+n,23+n,42+n),width=8)
    d.ellipse((W-240,-220,W+360,370),outline=(11,67,78),width=18)
    d.rounded_rectangle((40,35,680,112),radius=22,fill=(9,56,68))
    txt(d,47,"حكيم AI",34,WHITE,True)
    txt(d,148,title,48,WHITE,True)
    txt(d,228,subtitle,31,LIGHT)
    card(d,(46,318,674,916))
    if idx==0:
        d.rectangle((120,700,260,870),fill=(23,197,151));d.rectangle((390,790,530,870),fill=(239,93,97))
        txt(d,480,"التدريب",37,WHITE,True);txt(d,745,"الاختبار",37,WHITE,True)
        d.line((97,877,628,877),fill=WHITE,width=5)
    elif idx in (1,2):
        emoji(d,215,540,94,(235,73,77)); emoji(d,503,540,94,(246,197,67))
        txt(d,700,"تفاح",43,WHITE,True);txt(d,805,"موز",43,WHITE,True)
        d.line((350,625,350,780),fill=TEAL,width=6)
    elif idx==3:
        emoji(d,205,540,100,(235,73,77));emoji(d,505,540,100,(246,197,67))
        d.line((180,760,550,760),fill=YELLOW,width=8)
        txt(d,810,"خلفيات جديدة",34,YELLOW,True)
    elif idx==4:
        for k,x in enumerate((135,335,535)):
            d.rounded_rectangle((x-74,500,x+74,675),radius=24,fill=(9,105+25*k,104))
            txt(d,750,("تنوع","اختبار","تبسيط")[k],26,WHITE,True)
    else:
        d.rounded_rectangle((130,510,590,735),radius=38,fill=(14,91,90))
        txt(d,565,"اختبر على بيانات جديدة",34,WHITE,True)
        txt(d,785,"افهم ثم راجع",40,YELLOW,True)
    txt(d,945,label,31,TEAL,True)
    d.rounded_rectangle((42,1080,678,1170),radius=18,fill=(13,53,70))
    txt(d,1104,"Dr\\Amr kamel kahlil ahmed",20,LIGHT)
    path=OUT/f"scene_{idx:02d}.png"; im.save(path)
    return path

scenes=[
("فرط التكيّف","Overfitting","عندما ينجح التدريب ويفشل الاختبار"),
("هل حفظ النموذج؟","Fruit classifier","قد يتعلّم لون الخلفية"),
("المعلومة المضللة","Shortcut learning","بدل أن يتعلم شكل الفاكهة"),
("الاختبار الحقيقي","New unseen images","تغيير الخلفية قد يكشف الخطأ"),
("كيف نعالجه؟","Practical safeguards","بيانات متنوعة وتقييم مستقل"),
("سؤال حكيم","Does training score suffice?","لا؛ المهم نجاح التعميم")
]
paths=[make_scene(i,*v) for i,v in enumerate(scenes)]
audio=OUT/"HAI-C0041-voice-master.wav"
dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(audio)]).decode())
# Scene length derived from real narration, not fabricated.
step=dur/len(paths)
clips=[]
for i,p in enumerate(paths):
    clip=OUT/f"clip_{i:02d}.mp4"
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error",
        "-loop","1","-framerate","30","-i",str(p),
        "-filter_complex","scale=720:1280,format=yuv420p,fade=t=in:st=0:d=0.35,fade=t=out:st="+str(max(step-.4,0))+":d=0.35",
        "-t",str(step),"-r","30","-c:v","libx264","-preset","veryfast","-crf","27",
        "-pix_fmt","yuv420p",str(clip)],check=True)
    clips.append(clip)
manifest=OUT/"concat.txt"
manifest.write_text("".join(f"file '{p.name}'\n" for p in clips),encoding="utf-8")
result=OUT/"HAI-C0041-overfitting-final.mp4"
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0","-i",str(manifest),"-i",str(audio),
"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","160k","-ar","48000","-shortest","-movflags","+faststart",str(result)],check=True)
print(f"RENDER_OK={result} duration_audio={dur} bytes={result.stat().st_size}")
subprocess.run(["ffmpeg","-v","error","-i",str(result),"-f","null","-"],check=True)
