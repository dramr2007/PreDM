#!/usr/bin/env python3
"""Render Hakim AI episode HAI-M0006 with an Arabic female narration.

Frames follow the creator's supplied C0055 reference; no patient data is used.
When invoked with --frames-only, generate preview images without speech.
"""
from pathlib import Path
import json, math, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
OUT.mkdir(exist_ok=True)
W,H=720,1280
NAVY='#071C25'; TEAL='#45D5CC'; WHITE='#F6FFFF'; GOLD='#F7C966'; MUTED='#9ABDC0'; CARD='#103A46'; BORDER='#2A7180'; RED='#E96E72'
ROB = HERE / 'hakim_x.png'
arabic_font=Path('/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf')
arabic_bold=Path('/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf')
latin_font=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
latin_bold=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
if not arabic_font.exists(): arabic_font=latin_font
if not arabic_bold.exists(): arabic_bold=latin_bold

SCENES = [
 {'headline':'هل يمكن للذكاء الاصطناعي', 'caption':['أن يوفر وقتًا للمريض؟'],
  'voice':'هل يمكن للذكاء الاصطناعي أن يوفر دقيقة مهمة للمريض؟'},
 {'headline':'صور كثيرة تنتظر المراجعة', 'caption':['قد تساعد الأداة على ترتيب الحالات'],
  'voice':'تخيل صور أشعة كثيرة تنتظر المراجعة. قد يرتب البرنامج الصور، لتصل الحالات المقلقة إلى الطبيب أولًا.'},
 {'headline':'درجة الاشتباه', 'caption':['ليست تشخيصًا نهائيًا'],
  'voice':'لكن درجة الاشتباه ليست تشخيصًا، وقد يفوت البرنامج حالات حقيقية.'},
 {'headline':'ماذا وجدت دراسة بريطانية؟', 'caption':['لم ينخفض زمن المسار معنويًا'],
  'voice':'في دراسة بريطانية على صور طلبتها الرعاية الأولية، لم ينخفض زمن التصوير المقطعي أو تشخيص سرطان الرئة بشكل معنوي.'},
 {'headline':'لا نكتفي بسرعة الشاشة', 'caption':['نقيس أثر التقنية على مسار المريض'],
  'voice':'لذلك لا نكتفي بسرعة الشاشة. نسأل: هل تحسن مسار المريض؟ وكم حالة فاتت؟'},
 {'headline':'هل السرعة وحدها تكفي؟', 'caption':['الفائدة الحقيقية تحتاج دليلًا'],
  'voice':'حكيم أي آي: الفائدة الحقيقية تحتاج دليلًا، وليست وعدًا مسبقًا.'},
]

def ff(size,bold=False): return ImageFont.truetype(str(arabic_bold if bold else arabic_font),size)
def lf(size,bold=False): return ImageFont.truetype(str(latin_bold if bold else latin_font),size)
def center_ar(d,text,y,size=35,color=WHITE,bold=False):
    font=ff(size,bold)
    while d.textlength(text,font=font,direction='rtl',language='ar')>620 and size>18:
        size-=1;font=ff(size,bold)
    d.text((W//2,y),text,font=font,fill=color,anchor='mm',direction='rtl',language='ar')
def en(d,text,x,y,size=24,color=MUTED,bold=False):
    d.text((x,y),text,font=lf(size,bold),fill=color,anchor='mm')
def box(d,coords,fill=CARD,outline=BORDER,width=2,radius=25):
    d.rounded_rectangle(coords,radius=radius,fill=fill,outline=outline,width=width)
def arrow(d,xy,color=TEAL,width=7):
    x0,y0,x1,y1=xy; d.line(xy,fill=color,width=width)
    t=math.atan2(y1-y0,x1-x0);n=20
    d.polygon([(x1,y1),(x1-n*math.cos(t-.5),y1-n*math.sin(t-.5)),(x1-n*math.cos(t+.5),y1-n*math.sin(t+.5))],fill=color)
def mascot(im,center,size):
    if ROB.exists():
        r=Image.open(ROB).convert('RGBA');r.thumbnail((size,size))
        im.paste(r,(int(center[0]-r.width/2),int(center[1]-r.height/2)),r)

def make_frame(i):
    im=Image.new('RGB',(W,H),NAVY);d=ImageDraw.Draw(im)
    for x,y in [(44,70),(680,118),(55,500),(667,798),(72,900),(654,1022)]:d.ellipse((x,y,x+3,y+3),fill='#24616B')
    en(d,'HAKIM AI',360,57,25,TEAL,True)
    center_ar(d,'حكيم • نتعلم معًا',92,20,MUTED)
    center_ar(d,'هل يسرّع الذكاء قرار الطبيب؟',155,38,WHITE,True)
    center_ar(d,'الذكاء الاصطناعي الطبي • الحلقة ٦',212,22,TEAL)
    d.line((55,250,665,250),fill='#23616B',width=2)
    if i==0:
        mascot(im,(350,540),350); en(d,'?',570,433,112,GOLD,True)
        d.ellipse((86,350,150,414),outline=TEAL,width=5);d.line((118,366,118,383,132,390),fill=TEAL,width=5)
    else:
        box(d,(54,306,666,840),fill=CARD)
        if i==1:
            for j in range(3):
                box(d,(100,384+j*98,280,452+j*98),fill='#1A5361',outline=TEAL,radius=15)
                d.text((190,419+j*98),['صورة ١','صورة ٢','صورة ٣'][j],font=ff(25,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            arrow(d,(300,515,430,515)); box(d,(447,446,620,578),fill='#26636D',outline=GOLD,radius=18)
            en(d,'AI',534,482,30,GOLD,True)
            d.text((534,538),'مراجعة أولًا',font=ff(20,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
        elif i==2:
            box(d,(100,412,300,592),fill='#1A5361',outline=TEAL);en(d,'AI',200,456,36,TEAL,True)
            d.text((200,534),'اشتباه',font=ff(29,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            arrow(d,(310,505,408,505)); box(d,(425,412,616,592),fill='#1A5361',outline=GOLD)
            d.text((520,490),'طبيب',font=ff(32,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            d.text((520,548),'يراجع',font=ff(26),anchor='mm',fill=GOLD,direction='rtl',language='ar')
            center_ar(d,'قد تحدث أخطاء أو حالات فائتة',705,26,GOLD,True)
        elif i==3:
            en(d,'LungIMPACT 2026',360,385,24,TEAL,True)
            box(d,(93,448,335,640),fill='#1A5361',outline=TEAL); box(d,(385,448,627,640),fill='#1A5361',outline=GOLD)
            d.text((214,489),'مع الترتيب',font=ff(22,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            d.text((506,489),'دون الترتيب',font=ff(22,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            en(d,'53',214,556,54,TEAL,True); en(d,'53',506,556,54,GOLD,True)
            center_ar(d,'الوسيط إلى التصوير المقطعي: أيام',705,23,WHITE)
            center_ar(d,'صور من الرعاية الأولية في بريطانيا',754,20,MUTED)
        elif i==4:
            rows=[('زمن الرعاية','01'),('الحالات الفائتة','02'),('التحقق الخارجي','03')]
            for j,(txt,num) in enumerate(rows):
                y=380+j*123;box(d,(98,y,620,y+96),fill='#1A5361',outline=BORDER,radius=16)
                en(d,num,145,y+48,23,GOLD,True);d.text((400,y+48),txt,font=ff(27,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
        else:
            en(d,'?',360,482,115,GOLD,True)
            center_ar(d,'لا تكفي وحدها',645,37,TEAL,True)
            center_ar(d,'الفائدة تحتاج إلى دليل',709,29,WHITE)
        mascot(im,(606,842),115)
    center_ar(d,SCENES[i]['headline'],885,30,TEAL,True)
    box(d,(58,955,662,1078),fill='#0B303C',outline=BORDER,radius=18)
    for j,line in enumerate(SCENES[i]['caption']):center_ar(d,line,1018+j*35,28,WHITE,True)
    en(d,f'{i+1} / 6',82,917,17,MUTED)
    en(d,'Dr\\Amr kamel kahlil ahmed',360,1166,18,MUTED)
    d.line((58,1220,662,1220),fill='#28525A',width=4);d.line((58,1220,58+int(604*(i+1)/6),1220),fill=TEAL,width=5)
    im.save(OUT/f'scene-{i+1}.png',optimize=True)
    return im

frames=[make_frame(i) for i in range(6)]
sheet=Image.new('RGB',(720,854),NAVY)
for i,im in enumerate(frames):sheet.paste(im.resize((240,427)),((i%3)*240,(i//3)*427))
sheet.save(OUT/'contact.png')
if '--frames-only' in sys.argv:
    print('FRAMES_READY',OUT);sys.exit(0)

import os
import numpy as np
import soundfile as sf
import torch
from huggingface_hub import snapshot_download
torch.set_num_threads(4)
path=snapshot_download(repo_id='oddadmix/Nabra-Saudi-7M',allow_patterns=['*.py','af_msa.pt','nabra_saudi_7m.pth','*.json','kokoro_patched/**','arabic_g2p/**','arabic/**','phonemizer/**'],ignore_patterns=['training/**','samples/**','*/training/**','nabra_saudi_7m_v1_direct.pth'])
sys.path.insert(0,path)
from load_model import load
model,pipeline,voice=load(device='cpu')
audios=[];durations=[]
for i,scene in enumerate(SCENES):
    chunks=[]
    for sentence in re.split(r'(?<=[.!؟])\s+',scene['voice']):
        for result in pipeline(sentence,voice=voice,speed=1.0):
            if result[2] is not None:
                chunks.append(result[2].detach().cpu().numpy().astype(np.float32).reshape(-1))
        chunks.append(np.zeros(2400,dtype=np.float32))
    if len(chunks)<2: raise RuntimeError(f'No speech generated for scene {i+1}')
    audio=np.nan_to_num(np.concatenate(chunks)); peak=float(np.max(np.abs(audio)))
    if peak<0.001: raise RuntimeError(f'Silence detected in scene {i+1}')
    durations.append(round(len(audio)/24000,4));audios.append(audio)
    print('SPEECH_SCENE',i+1,durations[-1],flush=True)
joined=np.concatenate(audios);peak=float(np.max(np.abs(joined)))
joined=joined*min(2.0,(10**(-2/20))/peak)
sf.write(OUT/'narration.wav',joined,24000,subtype='PCM_16')
args=['ffmpeg','-hide_banner','-loglevel','error','-y']
for i,duration in enumerate(durations):args+=['-loop','1','-framerate','30','-t',str(duration),'-i',str(OUT/f'scene-{i+1}.png')]
args+=['-i',str(OUT/'narration.wav')]
filters=[f'[{i}:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v{i}]' for i in range(6)]
filters+=['[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0[vo]','[6:a]aresample=48000[ao]']
movie=OUT/'HAI-M0006-female.mp4'
args+=['-filter_complex',';'.join(filters),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','veryfast','-crf','21','-c:a','aac','-b:a','128k','-r','30','-t',str(round(sum(durations),3)),'-movflags','+faststart',str(movie)]
subprocess.run(args,check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
report={'id':'HAI-M0006','duration_seconds':round(sum(durations),2),'scenes_seconds':durations,'speaker':'Nabra-Saudi-7M af_msa','voice_reference':'female voice selected by user 27 October 2026','audio_peak':round(float(np.max(np.abs(joined))),5),'full_decode':'passed','narration':[s['voice'] for s in SCENES],'source':['https://www.nature.com/articles/s41591-026-04253-5','https://www.who.int/publications/i/item/9789240029200'],'human_listening':'not_performed','visual_review':'pending'}
(OUT/'production_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('RENDER_SUCCESS',movie,round(sum(durations),2),flush=True)
