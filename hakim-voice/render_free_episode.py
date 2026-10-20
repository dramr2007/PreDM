#!/usr/bin/env python3
"""Hakim AI metadata-driven free Piper/Pillow/FFmpeg renderer; NOT hardcoded to C0041."""
import sys, json, subprocess, shutil, wave, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, features

BASE=Path(__file__).resolve().parent
EPFILE=Path(sys.argv[1])
E=json.loads(EPFILE.read_text(encoding="utf-8"))
ID=E["id"]
OUTPUT=BASE/"output"/ID
OUTPUT.mkdir(parents=True,exist_ok=True)
FF=shutil.which("ffmpeg")
if not FF: raise RuntimeError("ffmpeg is required")
VOICE=BASE/"model/ar_JO-kareem-medium.onnx"
CONF=BASE/"model/ar_JO-kareem-medium.onnx.json"
if not VOICE.exists() or not CONF.exists(): raise RuntimeError("Arabic Piper voice files missing")
if not features.check("raqm"): raise RuntimeError("Arabic RAQM text support required")
FONT="/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf"
BOLD="/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf"
LAT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
if not Path(FONT).exists(): raise RuntimeError("Noto Arabic font missing")
W,H=720,1280
C={"ink":"#0E2132","dark":"#071725","teal":"#2CE6CC","pale":"#D8EFF4","yellow":"#FFD366","dim":"#AAC9D5","orange":"#FA8E74","blue":"#77CCF5"}
def font(sz,b=False,latin=False): return ImageFont.truetype(LAT if latin else (BOLD if b else FONT),sz)
def ar(d,s,x,y,sz=38,c="#FFFFFF",bold=False):
    d.text((x,y),s,fill=c,font=font(sz,bold),anchor="mm",direction="rtl",language="ar",stroke_width=0)
def en(d,s,x,y,sz=28,c="#2CE6CC",bold=False):
    d.text((x,y),s,fill=c,font=font(sz,bold,True),anchor="mm")
def rect(d,p,fill,r=24,outline=None,w=2):
    d.rounded_rectangle(p,radius=r,fill=fill,outline=outline,width=w)
def robot(d):
    # Simple original geometric Hakim AI pictogram, not a borrowed character
    d.line((360,78,360,98),fill=C["teal"],width=4)
    d.ellipse((354,69,366,81),fill=C["yellow"])
    rect(d,(317,94,403,151),"#164C5E",20,C["teal"],2)
    for x in (342,378): d.ellipse((x-9,113,x+9,131),fill=C["teal"])
    d.arc((340,124,380,146),8,172,fill=C["yellow"],width=3)
def scene(i,seg):
    im=Image.new("RGB",(W,H),C["dark"]);d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H;d.line((0,y,W,y),fill=(int(7+8*t),int(23+19*t),int(37+19*t)))
    d.ellipse((495,-160,870,210),outline="#1B5860",width=5)
    d.ellipse((-300,935,170,1400),outline="#175064",width=5)
    rect(d,(40,32,680,184),"#10384C",26,"#255E65",2)
    en(d,"HAKIM AI",360,58,23,C["teal"],True);robot(d)
    en(d,ID+" • "+str(i+1)+"/"+str(len(E["segments"])),360,171,17,C["dim"])
    ar(d,seg["head"],360,253,43,"#FFFFFF",True)
    en(d,E.get("english","ARTIFICIAL INTELLIGENCE"),360,310,24,C["yellow"],True)
    rect(d,(55,362,665,1010),"#133347",32,"#246076",3)
    v=seg.get("visual","takeaway")
    if v=="question":
        en(d,"AI MODEL",360,470,37,C["blue"],True)
        for x in (200,360,520):
            rect(d,(x-55,562,x+55,705),"#1D6680",20,C["teal"],3)
            for y in (590,623,656):d.line((x-28,y,x+28,y),fill="#CBF4F3",width=6)
        ar(d,"هل يمكن أن يصبح أخف؟",360,853,39,C["yellow"],True)
    elif v=="bits":
        en(d,"FP32",201,467,35,C["blue"],True)
        en(d,"INT8",522,467,35,C["teal"],True)
        for j in range(32):
            x=95+(j%8)*26;y=526+(j//8)*34
            rect(d,(x,y,x+21,y+28),"#3870A3",4)
        for j in range(8):
            x=423+(j%4)*44;y=550+(j//4)*62
            rect(d,(x,y,x+35,y+47),"#1DAF9B",6)
        d.line((332,604,393,604),fill=C["yellow"],width=7)
        d.polygon([(381,587),(406,604),(381,621)],fill=C["yellow"])
        ar(d,"أرقام بدقة أقل",360,862,38,C["yellow"],True)
    elif v=="memory":
        ar(d,"تمثيل الأوزان",360,465,37,"#FFFFFF",True)
        rect(d,(125,557,595,618),"#336185",15)
        rect(d,(125,557,595,618),"#4E91C9",15)
        rect(d,(125,698,595,759),"#204A5A",15)
        rect(d,(125,698,260,759),"#24CCAD",15)
        en(d,"32 bit / weight",360,652,24,C["blue"])
        en(d,"8 bit / weight",360,799,24,C["teal"])
        ar(d,"لا يعني ربع حجم التطبيق كله",360,890,28,C["yellow"],True)
    elif v=="device":
        rect(d,(136,487,318,811),"#143F56",26,C["teal"],5)
        rect(d,(159,537,296,743),"#235C71",13)
        d.ellipse((218,767,237,786),fill=C["yellow"])
        rect(d,(384,526,584,719),"#23546C",18,C["blue"],4)
        for x in (423,459,495,531):
            for y in (555,591,627,663):rect(d,(x,y,x+21,y+21),"#339AAB",4)
        ar(d,"الجهاز يحدد المكسب",360,865,35,C["yellow"],True)
    elif v=="tradeoff":
        ar(d,"حجم النموذج",215,481,29,C["teal"],True)
        ar(d,"جودة الإجابات",518,481,29,C["orange"],True)
        d.line((360,518,360,729),fill="#6CBFCC",width=9)
        d.line((192,577,528,668),fill=C["yellow"],width=13)
        d.ellipse((183,567,202,587),fill=C["teal"])
        d.ellipse((518,658,537,677),fill=C["orange"])
        rect(d,(135,752,585,835),"#25546A",20)
        ar(d,"المهم اختبار النتائج",360,795,34,"#FFFFFF",True)
    else:
        for j,(cap,eng) in enumerate([("الجودة","QUALITY"),("الذاكرة","MEMORY"),("السرعة","LATENCY")]):
            y=462+j*152
            rect(d,(116,y,601,y+121),"#21576B",19,C["teal"] if j==0 else "#347489",2)
            ar(d,cap,360,y+43,37,C["yellow"],True)
            en(d,eng,360,y+90,19,C["pale"],True)
    sub=seg.get("sub","")
    if sub.isascii(): en(d,sub,360,1067,27,C["teal"])
    else: ar(d,sub,360,1067,29,C["teal"])
    d.line((59,1151,660,1151),fill="#1A6571",width=2)
    en(d,r"Dr\Amr kamel kahlil ahmed",360,1203,20,C["dim"])
    file=OUTPUT/("scene_%02d.png"%i);im.save(file);return file

def run(cmd,stdin=None):
    r=subprocess.run(cmd, input=stdin, text=(stdin is not None),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.returncode: raise RuntimeError("Failed: "+" ".join(map(str,cmd[:4]))+"\n"+r.stderr.decode(errors="replace")[-2000:] if isinstance(r.stderr,bytes) else r.stderr[-2000:])
    return r

durations=[];wav_files=[]
for i,seg in enumerate(E["segments"]):
    raw=OUTPUT/("audio_%02d_raw.wav"%i)
    wav=OUTPUT/("audio_%02d.wav"%i)
    run(["piper","--model",str(VOICE),"--config",str(CONF),"--output_file",str(raw)],stdin=seg["text"]+"\n")
    run([FF,"-y","-loglevel","error","-i",str(raw),"-filter:a","atempo=1.13,loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ac", "1","-ar","22050","-c:a","pcm_s16le",str(wav)])
    with wave.open(str(wav),"rb") as f: dur=f.getnframes()/f.getframerate()
    if dur<1: raise RuntimeError("Unexpected short audio in segment "+str(i))
    durations.append(dur); wav_files.append(wav)
    scene(i,seg)
af=OUTPUT/"audio.ffconcat"
vf=OUTPUT/"video.ffconcat"
af.write_text("ffconcat version 1.0\n"+"".join("file '"+str(x)+"'\n" for x in wav_files),encoding="utf8")
vf.write_text("ffconcat version 1.0\n"+"".join("file '"+str(OUTPUT/('scene_%02d.png'%i))+"'\n"+"duration %.5f\n"%d for i,d in enumerate(durations))+
    "file '"+str(OUTPUT/('scene_%02d.png'%(len(durations)-1)))+"'\n",encoding="utf8")
full=OUTPUT/"full.wav"
run([FF,"-y","-loglevel","error","-safe","0","-f","concat","-i",str(af),"-ar","22050","-ac","1","-c:a","pcm_s16le",str(full)])
with wave.open(str(full),"rb") as f: full_duration=f.getnframes()/f.getframerate()
if full_duration>120: raise RuntimeError("Video too long")
video=OUTPUT/(ID+"-FREE-MALE.mp4")
run([FF,"-y","-loglevel","error","-safe","0","-f","concat","-i",str(vf),
     "-i",str(full),"-vf","fps=30,format=yuv420p","-r","30","-c:v","libx264","-preset","fast","-crf","23",
     "-c:a","aac","-b:a","128k","-movflags","+faststart","-t",str(full_duration),"-shortest",str(video)])
report={"id":ID,"duration_s":round(full_duration,2),"segment_durations_s":[round(x,2) for x in durations],
 "video":str(video),"bytes":video.stat().st_size,"voice":"Piper ar_JO-kareem-medium, atempo=1.13",
 "caption":E.get("caption",""),"references":[E.get("reference","")]}
(OUTPUT/"production_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
print(json.dumps(report,ensure_ascii=False))
