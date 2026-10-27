#!/usr/bin/env python3
"""Render Hakim AI episode HAI-M0009 with an Arabic female narration.

Frames follow the creator's supplied C0055 reference; no patient data is used.
When invoked with --frames-only, generate preview images without speech.
"""
from pathlib import Path
import json, math, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out_edge_m0009'
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
 {'headline':'صمّم الفكرة على ورقة', 'caption':['تحدٍّ تعليمي بلا بيانات مرضى'],
  'voice':'هل تقدر تصمم ذكاء طبي على ورقة؟ جرب معي!'},
 {'headline':'الخطوة الأولى: المهمة', 'caption':['ترتيب أشعة افتراضية للمراجعة'],
  'voice':'اكتب مهمة واحدة: ترتيب صور أشعة افتراضية لتحديد ما يحتاج مراجعة أسرع.'},
 {'headline':'حدّد المدخل والمخرج', 'caption':['صورة تخيلية ثم درجة اشتباه'],
  'voice':'حدد المدخل: صورة خيالية، والمخرج: درجة اشتباه، لا تشخيص نهائي.'},
 {'headline':'جرّب ثلاث حالات', 'caption':['واضحة، ناقصة، وملتبسة'],
  'voice':'ارسم ثلاث حالات تخيلية: واضحة، وناقصة، وملتبسة. متى تطلب صورة أخرى أو مراجعة بشرية؟'},
 {'headline':'كيف نختبر الفكرة لاحقًا؟', 'caption':['اختبار مستقل ومرجع مناسب'],
  'voice':'قبل الاستخدام الحقيقي، نحتاج اختبارًا مستقلًا، ومرجعًا مناسبًا، وبيانات تمثل المرضى.'},
 {'headline':'هل الورشة تثبت الأمان؟', 'caption':['لا، إنها خطة أولية فقط'],
  'voice':'هل تنجح الورشة وحدها في إثبات أمان المنتج؟ لا. إنها خطة أولية فقط. حكيم أي آي: الدليل أولًا.'},
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
    center_ar(d,'هل تصمم فكرة ذكاء طبي على ورقة؟',155,38,WHITE,True)
    center_ar(d,'الذكاء الاصطناعي الطبي • الحلقة ٩',212,22,TEAL)
    d.line((55,250,665,250),fill='#23616B',width=2)
    if i==0:
        mascot(im,(350,540),350); en(d,'?',570,433,112,GOLD,True)
    else:
        box(d,(54,306,666,840),fill=CARD)
        if i==1:
            box(d,(109,393,610,552),fill='#1A5361',outline=TEAL)
            center_ar(d,'مهمة افتراضية',440,30,TEAL,True)
            center_ar(d,'ترتيب الأشعة للمراجعة',505,28,WHITE,True)
            center_ar(d,'اكتب هدفًا واحدًا واضحًا',704,27,GOLD,True)
        elif i==2:
            box(d,(91,433,286,580),fill='#1A5361',outline=TEAL)
            d.text((188,479),'صورة',font=ff(27,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            d.text((188,536),'تخيلية',font=ff(24,True),anchor='mm',fill=TEAL,direction='rtl',language='ar')
            arrow(d,(299,506,412,506))
            box(d,(430,433,629,580),fill='#1A5361',outline=GOLD)
            d.text((529,479),'درجة',font=ff(27,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            d.text((529,536),'اشتباه',font=ff(24,True),anchor='mm',fill=GOLD,direction='rtl',language='ar')
            center_ar(d,'ليست تشخيصًا نهائيًا',711,27,GOLD,True)
        elif i==3:
            rows=[('حالة واضحة','01'),('حالة ناقصة','02'),('حالة ملتبسة','03')]
            for n,(txt,num) in enumerate(rows):
                y=362+n*130;box(d,(92,y,628,y+98),fill='#1A5361',outline=BORDER,radius=16)
                en(d,num,143,y+49,22,GOLD,True)
                d.text((400,y+49),txt,font=ff(27,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
            center_ar(d,'متى تحتاج مساعدة بشرية؟',780,23,GOLD,True)
        elif i==4:
            rows=[('اختبار مستقل','01'),('مرجع مناسب','02'),('بيانات ممثلة','03')]
            for n,(txt,num) in enumerate(rows):
                y=367+n*130;box(d,(92,y,628,y+98),fill='#1A5361',outline=BORDER,radius=16)
                en(d,num,143,y+49,22,GOLD,True)
                d.text((400,y+49),txt,font=ff(27,True),anchor='mm',fill=WHITE,direction='rtl',language='ar')
        else:
            en(d,'?',360,463,105,GOLD,True)
            center_ar(d,'هل الورقة تثبت الأمان؟',595,30,WHITE,True)
            center_ar(d,'لا، نحتاج تقييمًا فعليًا',685,27,TEAL,True)
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
movie=OUT/'HAI-M0009-female-edge.mp4'
args+=['-filter_complex',';'.join(filters),'-map','[vo]','-map','[ao]','-c:v','libx264','-preset','veryfast','-crf','21','-c:a','aac','-b:a','128k','-r','30','-t',str(round(sum(durations),3)),'-movflags','+faststart',str(movie)]
subprocess.run(args,check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
report={'id':'HAI-M0009','duration_seconds':round(sum(durations),2),'scenes_seconds':durations,'speaker':'Microsoft ar-SA-ZariyahNeural','voice_reference':'female voice selected by user 27 October 2026','audio_peak':round(float(np.max(np.abs(joined))),5),'full_decode':'passed','narration':[s['voice'] for s in SCENES],'source':['https://www.fda.gov/media/153486/download','https://www.nature.com/articles/s41591-022-01772-9'],'human_listening':'not_performed','visual_review':'pending'}
(OUT/'production_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('RENDER_SUCCESS',movie,round(sum(durations),2),flush=True)
