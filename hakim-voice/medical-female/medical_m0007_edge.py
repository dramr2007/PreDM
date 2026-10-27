#!/usr/bin/env python3
"""Render Hakim AI episode HAI-M0007 with an Arabic female narration.

Frames follow the creator's supplied C0055 reference; no patient data is used.
When invoked with --frames-only, generate preview images without speech.
"""
from pathlib import Path
import json, math, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out_edge_m0007'
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
 {'headline':'هل مراجعة الطبيب تكفي؟', 'caption':['هل تضمن الأمان دائمًا؟'],
  'voice':'لو راجع الطبيب إجابة الذكاء الاصطناعي، هل هذا يضمن أنها صحيحة؟'},
 {'headline':'المساعد يقترح', 'caption':['وقد تكون المعلومات ناقصة'],
  'voice':'قد يقترح المساعد إجابة اعتمادًا على معلومات ناقصة، وقد يقع في الخطأ.'},
 {'headline':'المراجعة الحقيقية تحتاج', 'caption':['وقتًا ومعلومات وصلاحية الرفض'],
  'voice':'المراجعة الحقيقية تحتاج وقتًا ومعلومات، وقدرة على رفض الاقتراح أو تعديله.'},
 {'headline':'الإنسان قد يخطئ أيضًا', 'caption':['لذلك نختبر النظام في العمل الفعلي'],
  'voice':'ومع ذلك قد يفوّت الإنسان خطأً، أو يثق بالآلة أكثر من اللازم.'},
 {'headline':'ماذا وجدت تجربة كينيا؟', 'caption':['لم ينخفض فشل العلاج بشكل معنوي'],
  'voice':'في تجربة عشوائية في كينيا، لم ينخفض فشل العلاج خلال أربعة عشر يومًا بشكل معنوي عند استخدام المساعد.'},
 {'headline':'الإشراف مسؤولية فعلية', 'caption':['نقيس أداء الإنسان والنظام معًا'],
  'voice':'لذلك نقيس أداء النظام والإنسان معًا. حكيم أي آي: الدليل أولًا.'},
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
    center_ar(d,'هل مراجعة الطبيب تضمن الأمان؟',155,38,WHITE,True)
    center_ar(d,'الذكاء الاصطناعي الطبي • الحلقة ٧',212,22,TEAL)
    d.line((55,250,665,250),fill='#23616B',width=2)
    if i==0:
        mascot(im,(350,540),350); en(d,'?',570,433,112,GOLD,True)
    else:
        box(d,(54,306,666,840),fill=CARD)
        if i==1:
            box(d,(82,445,238,565),fill='#1A5361',outline=TEAL,radius=15)
            d.text((160,505),'معلومات',font=ff(23,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            arrow(d,(245,505,300,505));box(d,(308,445,418,565),fill='#1A5361',outline=GOLD,radius=15)
            en(d,'AI',363,505,33,GOLD,True)
            arrow(d,(425,505,480,505));box(d,(488,445,638,565),fill='#1A5361',outline=TEAL,radius=15)
            d.text((563,505),'اقتراح',font=ff(23,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            center_ar(d,'قد تكون المعلومات ناقصة',702,25,GOLD,True)
        elif i==2:
            rows=[('وقت كافٍ','01'),('معلومات واضحة','02'),('صلاحية الرفض','03')]
            for n,(txt,num) in enumerate(rows):
                y=374+n*126;box(d,(98,y,620,y+96),fill='#1A5361',outline=BORDER,radius=16)
                en(d,num,145,y+48,23,GOLD,True)
                d.text((400,y+48),txt,font=ff(27,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
        elif i==3:
            box(d,(105,414,305,600),fill='#1A5361',outline=TEAL)
            en(d,'AI',205,470,40,TEAL,True)
            d.text((205,550),'اقتراح',font=ff(26,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            arrow(d,(315,505,410,505))
            box(d,(423,414,618,600),fill='#1A5361',outline=GOLD)
            d.text((520,483),'مراجع',font=ff(29,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            en(d,'?',520,552,42,GOLD,True)
            center_ar(d,'قد يفوت الخطأ الإنسان أيضًا',705,26,GOLD,True)
        elif i==4:
            en(d,'KENYA 2026',360,385,24,TEAL,True)
            center_ar(d,'تجربة عشوائية',468,34,WHITE,True)
            box(d,(125,513,595,650),fill='#1A5361',outline=GOLD)
            center_ar(d,'فشل العلاج خلال ١٤ يومًا',559,27,WHITE,True)
            center_ar(d,'لم ينخفض بشكل معنوي',614,25,GOLD,True)
            center_ar(d,'النتيجة تخص ظروف الدراسة',738,22,MUTED)
        else:
            en(d,'?',360,480,110,GOLD,True)
            center_ar(d,'المراجعة تستطيع التعديل',644,30,TEAL,True)
            center_ar(d,'والدليل يختبر الفائدة',711,28,WHITE)
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

import asyncio
import edge_tts
import numpy as np
import soundfile as sf
audios=[];durations=[]
for i,scene in enumerate(SCENES):
    mp3=OUT/f'scene-{i+1}.mp3';wav=OUT/f'scene-{i+1}.wav'
    async def generate():
        await edge_tts.Communicate(scene['voice'],voice='ar-SA-ZariyahNeural',rate='+0%').save(str(mp3))
    asyncio.run(generate())
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(mp3),'-ac','1','-ar','24000',str(wav)],check=True)
    audio,sr=sf.read(wav,dtype='float32')
    if sr!=24000 or len(audio)<1000: raise RuntimeError(f'No speech generated for scene {i+1}')
    audio=np.nan_to_num(np.concatenate([audio,np.zeros(3600,dtype=np.float32)])); peak=float(np.max(np.abs(audio)))
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
movie=OUT/'HAI-M0007-female-edge.mp4'
args+=['-filter_complex',';'.join(filters),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','veryfast','-crf','21','-c:a','aac','-b:a','128k','-r','30','-t',str(round(sum(durations),3)),'-movflags','+faststart',str(movie)]
subprocess.run(args,check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
report={'id':'HAI-M0007','duration_seconds':round(sum(durations),2),'scenes_seconds':durations,'speaker':'Microsoft ar-SA-ZariyahNeural','voice_reference':'female voice selected by user 27 October 2026','audio_peak':round(float(np.max(np.abs(joined))),5),'full_decode':'passed','narration':[s['voice'] for s in SCENES],'source':['https://www.nature.com/articles/s41591-026-04503-6','https://www.who.int/publications/i/item/9789240029200'],'human_listening':'not_performed','visual_review':'pending'}
(OUT/'production_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('RENDER_SUCCESS',movie,round(sum(durations),2),flush=True)
