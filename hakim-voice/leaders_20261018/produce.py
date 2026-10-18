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

import os, sys, numpy as np, torch, time
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
DATA=json.loads((P/'episodes.json').read_text())
OUT=P/'outputs'; OUT.mkdir(exist_ok=True)
ref=P/'reference.wav'
torch.set_num_threads(4)
torch.manual_seed(42)
model=ChatterboxMultilingualTTS.from_pretrained(device='cpu',t3_model='v3')
def wrap_ar(text, font, max_width=560):
 words=text.split(); lines=[]; row=''
 for word in words:
  attempt=(row+' '+word).strip()
  if font.getlength(attempt,direction='rtl')>max_width and row: lines.append(row);row=word
  else: row=attempt
 if row:lines.append(row)
 return lines
def icon(d,kind,step):
 cx,cy=360,580
 if kind=='rocket':
  d.polygon([(cx,405),(cx-48,500),(cx-48,670),(cx+48,670),(cx+48,500)],fill=WHITE)
  d.ellipse((cx-24,510,cx+24,558),fill=TURQ)
  d.polygon([(cx-48,610),(cx-105,710),(cx-48,680)],fill=TURQ)
  d.polygon([(cx+48,610),(cx+105,710),(cx+48,680)],fill=TURQ)
  d.polygon([(cx-35,680),(cx,770),(cx+35,680)],fill=GOLD)
 elif kind=='car':
  box(d,(170,550,550,670),fill=TURQ,r=30)
  d.polygon([(230,550),(280,465),(430,465),(480,550)],fill=CYAN)
  for x in [250,475]:d.ellipse((x-35,640,x+35,710),fill=NAVY,outline=GOLD,width=7)
  d.line((150,735,580,735),fill=MUTED,width=5)
 elif kind=='chip':
  box(d,(255,475,465,685),fill='#1D5362',outline=TURQ,r=20)
  for i in range(5):
   x=280+i*40
   d.line((x,440,x,475),fill=GOLD,width=7);d.line((x,685,x,720),fill=GOLD,width=7)
   y=500+i*40
   d.line((220,y,255,y),fill=GOLD,width=7);d.line((465,y,500,y),fill=GOLD,width=7)
  en(d,'AI',360,580,70,WHITE)
 elif kind in ['team','network']:
  pts=[(360,475),(220,575),(500,575),(280,720),(440,720)]
  for a,b in zip(pts,pts[1:]+pts[:1]):d.line((*a,*b),fill='#397D8B',width=6)
  for j,(x,y) in enumerate(pts):
   d.ellipse((x-36,y-36,x+36,y+36),fill=GOLD if j==0 else TURQ)
   if kind=='team':d.arc((x-25,y-18,x+25,y+22),0,180,fill=NAVY,width=5)
 elif kind in ['shield','check']:
  d.polygon([(360,440),(485,490),(465,665),(360,748),(255,665),(235,490)],fill='#205767',outline=TURQ,width=6)
  d.line([(295,585),(342,635),(425,535)],fill=GOLD,width=16)
 elif kind=='chat':
  box(d,(175,470,545,675),fill='#205767',outline=TURQ,r=34)
  d.polygon([(245,675),(225,735),(320,675)],fill=TURQ)
  for y,w in [(525,240),(575,180),(625,210)]:d.line((215,y,215+w,y),fill=GOLD,width=9)
 else:
  d.ellipse((245,465,475,695),fill='#205767',outline=TURQ,width=6)
  en(d,'?' if kind=='question' else '!',360,580,135,GOLD)
def frame(ep,k):
 title,sub,narr,kind=ep['scenes'][k]
 im=Image.new('RGB',(W,H),NAVY);d=ImageDraw.Draw(im)
 box(d,(30,30,690,114),fill='#134B55',r=22);en(d,'HAKIM AI',270,72,36,TURQ);robot(d,610,70,.24)
 ar(d,ep['name'],360,170,42)
 en(d,ep['en'],360,233,22,GOLD)
 ar(d,title,360,320,32)
 en(d,sub,360,375,20,CYAN)
 icon(d,kind,k)
 # Short exact narrated excerpt. No claim of full subtitles.
 words=narr.split();summary=' '.join(words[:18])
 lines=wrap_ar(summary,ff(28),560)
 for j,line in enumerate(lines):ar(d,line,360,825+j*52,28,WHITE,False)
 ar(d,'سلسلة خاصة • قادة وفرق الابتكار',360,1080,24,CYAN,False)
 en(d,'Dr\\Amr kamel kahlil ahmed',360,1173,20,MUTED)
 en(d,f"SPECIAL • {ep['id']} • {k+1}/6",360,1220,16,MUTED)
 im.save(OUT/f"{ep['id']}_{k}.png")
 return im
for ep in DATA['episodes']:
 if os.environ.get('EPISODE') and ep['id']!=os.environ['EPISODE']:continue
 print('START',ep['id'],flush=True)
 segments=[];durations=[];qa=[]
 # Individual scenes have real speech boundaries, no estimated timing.
 for k,scene in enumerate(ep['scenes']):
  wav=model.generate(scene[2],language_id='ar',audio_prompt_path=str(ref),cfg_weight=.3,exaggeration=.5)
  x=wav.detach().cpu().float().numpy().reshape(-1)
  dur=len(x)/model.sr; peak=float(abs(x).max());rms=float(np.sqrt(np.mean(x*x)))
  assert np.isfinite(x).all() and 2<dur<22 and peak>.03 and rms>.005,(ep['id'],k,dur,peak,rms)
  x=np.concatenate([x,np.zeros(int(.18*model.sr),dtype=np.float32)])
  segments.append(x);durations.append(len(x)/model.sr)
  qa.append({'scene':k,'seconds':dur,'rms':rms,'peak':peak,'script':scene[2]})
  frame(ep,k)
 audio=OUT/f"{ep['id']}.wav";sf.write(audio,np.concatenate(segments),model.sr)
 movie=OUT/f"HAI-S20261018-{ep['id']}.mp4"
 args=['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','2']
 for k,dur in enumerate(durations):args+=['-loop','1','-framerate','30','-t',str(dur),'-i',str(OUT/f"{ep['id']}_{k}.png")]
 args+=['-i',str(audio)]
 # Animated reveal keeps text at native resolution and within the safe area.
 flt=[f"[{k}:v]fps=30,setsar=1,format=yuv420p,fade=t=in:st=0:d=0.16,drawbox=x=48:y=1125:w='624*t/{dur}':h=4:color=0x2CE4C6:t=fill[v{k}]" for k,dur in enumerate(durations)]
 # drawbox evaluates time differently across ffmpeg versions; use a fixed progress footer instead.
 flt=[f"[{k}:v]fps=30,setsar=1,format=yuv420p,fade=t=in:st=0:d=0.16[v{k}]" for k,dur in enumerate(durations)]
 flt+=['[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[vo]','[6:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[ao]']
 args+=['-filter_complex_threads','1','-filter_complex',';'.join(flt),'-map','[vo]','-map','[ao]','-c:v','libx264','-threads','2','-preset','fast','-crf','21','-c:a','aac','-b:a','192k','-t',str(sum(durations)),'-movflags','+faststart',str(movie)]
 subprocess.run(args,check=True)
 subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
 (OUT/f"{ep['id']}_QA.json").write_text(json.dumps({'id':ep['id'],'voice':DATA['voice'],'seconds':sum(durations),'scenes':qa,'full_decode':'pass','human_listening':False,'sources':ep['sources']},ensure_ascii=False,indent=2))
 print('COMPLETE',ep['id'],sum(durations),flush=True)
 audio.unlink()
