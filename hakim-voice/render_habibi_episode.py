#!/usr/bin/env python3
"""Produce a Hakim AI 9:16 video with *licensed* Specialized MSA Habibi-TTS.
No paid APIs and no use of the noncommercial Unified/SAU/UAE weights.
One six-scene episode per run; public publishing is a separate QC gate.
"""
import json, math, os, subprocess, sys, wave
from pathlib import Path
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont, features
from cached_path import cached_path
from f5_tts.infer.utils_infer import load_model,load_vocoder,preprocess_ref_audio_text
from habibi_tts.infer.utils_infer import infer_process
from hydra.utils import get_class
from omegaconf import OmegaConf
from importlib.resources import files

ROOT=Path(__file__).resolve().parent
DOC=Path(sys.argv[1]); E=json.loads(DOC.read_text(encoding='utf-8'))
assert E['id']=='HAI-C0069' and len(E['segments'])==6
OUT=ROOT/'output'/E['id'];OUT.mkdir(parents=True,exist_ok=True)
FF='ffmpeg'; W=720;H=1280
BG='#061D2E';PANEL='#0F354B';TEAL='#33D9C5';IVORY='#EAF7FF';GOLD='#FFCF70';RED='#FB787E';DIM='#AACAD6'
AR='/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf'
BOLD='/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf'
EN='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
assert features.check('raqm'),'Pillow requires Arabic RAQM support'
assert Path(AR).exists() and Path(BOLD).exists()

def f(n,b=False,latin=False):return ImageFont.truetype(EN if latin else(BOLD if b else AR),n)
def ar(d,x,y,txt,n=30,col=IVORY):d.text((x,y),txt,font=f(n,True),fill=col,direction='rtl',language='ar',anchor='mm')
def en(d,x,y,txt,n=30,col=IVORY):d.text((x,y),txt,font=f(n,True,True),fill=col,anchor='mm')
def panel(d,xy,col=PANEL,r=21):d.rounded_rectangle(xy,fill=col,radius=r,outline='#236E7C',width=2)
def main_scene(idx,seg):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    for y in range(H):
        a=y/H;d.line((0,y,W,y),fill=(int(6+10*a),int(29+11*a),int(46+14*a)))
    d.ellipse((480,-260,900,160),outline='#1A5965',width=6)
    panel(d,(39,26,681,137),'#123B4B');en(d,175,72,'HAKIM AI',29,TEAL)
    en(d,550,72,E['id']+'  |  '+str(idx+1)+'/6',16,DIM)
    # Original Hakim-X character: geometric scientist robot, not an existing IP character
    d.line((366,61,366,80),fill=TEAL,width=5);d.ellipse((360,53,372,65),fill=GOLD)
    panel(d,(321,78,412,126),'#1C5861')
    d.ellipse((339,95,350,106),fill=TEAL);d.ellipse((383,95,394,106),fill=TEAL)
    d.arc((344,103,393,119),start=6,end=168,fill=GOLD,width=2)
    ar(d,360,215,seg['head'],36,IVORY);en(d,360,264,'CONFIDENCE INTERVAL',23,GOLD)
    panel(d,(55,320,665,1027))
    if idx==0:
        en(d,360,450,'95% CI',85,GOLD)
        d.line((124,614,600,614),fill=DIM,width=10)
        d.line((220,614,500,614),fill=TEAL,width=16)
        for x in (220,500):d.line((x,580,x,648),fill=TEAL,width=7)
        d.ellipse((346,599,374,629),fill=GOLD)
        ar(d,360,792,'هل تعني احتمالًا خاصًا',31,IVORY)
        ar(d,360,860,'بهذه الفترة الواحدة؟',36,GOLD)
    elif idx==1:
        en(d,360,405,'SAMPLES',39,TEAL)
        for j in range(40):
            xx=126+(j%8)*68;yy=496+(j//8)*66
            d.ellipse((xx-12,yy-12,xx+12,yy+12),fill=GOLD if j%11==0 else '#348F8A')
        d.line((115,878,605,878),fill=DIM,width=6)
        for x in (198,275,350,460,540):d.line((x,858,x,898),fill=GOLD,width=4)
        ar(d,360,954,'كل عينة قد تعطي تقديرًا مختلفًا',23,GOLD)
    elif idx==2:
        en(d,360,414,'TRUE MEAN',28,GOLD)
        d.line((360,474,360,927),fill=GOLD,width=7)
        for j in range(20):
            y=491+j*21
            if j==13: left,right=428,590;col=RED
            else: left=110+(j*23)%100;right=610-(j*31)%100;col=TEAL
            d.line((left,y,right,y),fill=col,width=5)
            for x in (left,right):d.line((x,y-7,x,y+7),fill=col,width=3)
        en(d,360,985,'19 / 20  •  ILLUSTRATION',23,DIM)
    elif idx==3:
        en(d,360,435,'ONE INTERVAL',31,TEAL)
        d.line((142,621,578,621),fill=DIM,width=10)
        d.line((241,621,470,621),fill=TEAL,width=19)
        for x in (241,470):d.line((x,576,x,663),fill=TEAL,width=7)
        en(d,360,755,'FIXED LIMITS',39,GOLD)
        ar(d,360,870,'بعد الحساب تصبح الحدود ثابتة',28,IVORY)
    elif idx==4:
        en(d,213,451,'SMALL N',29,RED);en(d,510,451,'LARGE N',27,TEAL)
        d.line((125,610,306,610),fill=RED,width=18);d.line((451,610,563,610),fill=TEAL,width=18)
        for x in (215,508):d.line((x,558,x,660),fill=GOLD,width=7)
        ar(d,360,786,'في الظروف المتشابهة',29,IVORY)
        ar(d,360,866,'العينة الأكبر غالبًا أضيق فترة',28,GOLD)
    elif idx==5:
        for j,(number,cap) in enumerate([('01','التقدير'),('02','حجم العينة'),('03','افتراضات الطريقة')]):
            y=464+j*161
            panel(d,(120,y,603,y+123),'#205364')
            en(d,192,y+62,number,34,GOLD)
            ar(d,428,y+62,cap,31,IVORY)
        ar(d,360,970,'قيّم عدم اليقين قبل القرار',24,TEAL)
    if seg.get('sub'):
        ar(d,360,1084,seg['sub'],27,TEAL)
    d.line((44,1168,676,1168),fill='#2F6B79',width=3)
    en(d,360,1220,r'Dr\Amr kamel kahlil ahmed',19,DIM)
    p=OUT/('scene_%02d.png'%idx);im.save(p,optimize=True)
    return p

# Commercially permitted weights: SWivid Habibi-TTS Specialized MSA only (Apache-2.0).
print('Loading Apache-2.0 Specialized MSA checkpoint and model...',flush=True)
cfg=OmegaConf.load(str(files('f5_tts').joinpath('configs/F5TTS_v1_Base.yaml')))
klass=get_class('f5_tts.model.'+cfg.model.backbone)
checkpoint=str(cached_path('hf://SWivid/Habibi-TTS/Specialized/MSA/model_200000.safetensors'))
vocab=str(cached_path('hf://SWivid/Habibi-TTS/Specialized/MSA/vocab.txt'))
model=load_model(klass,cfg.model.arch,checkpoint,mel_spec_type=cfg.model.mel_spec.mel_spec_type,vocab_file=vocab,device='cpu')
vocoder=load_vocoder(vocoder_name=cfg.model.mel_spec.mel_spec_type,device='cpu')
refaudio=str(files('habibi_tts').joinpath('assets/MSA.mp3'))
reftext='كان اللعيب حاضرًا في العديد من الأنشطة والفعاليات المرتبطة بكأس العالم، مما سمح للجماهير بالتفاعل معه والتقاط الصور التذكارية.'
refaudio,reftext=preprocess_ref_audio_text(refaudio,reftext)
wavefiles=[];durations=[]
for i,seg in enumerate(E['segments']):
    # One model load; six independent narrations with consistent voice & volume
    audio,sr,_=infer_process(refaudio,reftext,seg['text'],model,vocoder,nfe_step=24,speed=1.00,device='cpu',dialect_id=None)
    raw=OUT/('audio_%02d_raw.wav'%i);wav=OUT/('audio_%02d.wav'%i)
    sf.write(raw,audio,sr)
    subprocess.run([FF,'-y','-loglevel','error','-i',str(raw),'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','24000','-ac','1',str(wav)],check=True)
    with wave.open(str(wav),'rb') as fp: duration=fp.getnframes()/fp.getframerate()
    if not 1<duration<28:raise RuntimeError('Suspicious scene voice duration '+str(i)+': '+str(duration))
    durations.append(duration);wavefiles.append(wav);main_scene(i,seg)
print('Audio scene durations',durations,flush=True)
ffA=OUT/'audio.ffconcat';ffV=OUT/'video.ffconcat'
ffA.write_text('ffconcat version 1.0\n'+''.join('file '+repr(str(x))+'\n' for x in wavefiles),encoding='utf8')
ffV.write_text('ffconcat version 1.0\n'+''.join("file "+repr(str(OUT/('scene_%02d.png'%i)))+"\nduration %.5f\n"%d for i,d in enumerate(durations))+"file "+repr(str(OUT/('scene_%02d.png'%(len(durations)-1))))+"\n",encoding='utf8')
full=OUT/'full.wav'
subprocess.run([FF,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(ffA),'-ac','1','-ar','24000',str(full)],check=True)
with wave.open(str(full),'rb') as fp: duration=fp.getnframes()/fp.getframerate()
if not 22<duration<120:raise RuntimeError('Invalid total duration: '+str(duration))
video=OUT/(E['id']+'-HABIBI-MSA.mp4')
subprocess.run([FF,'-y','-loglevel','error','-safe','0','-f','concat','-i',str(ffV),'-i',str(full),'-vf','fps=30,format=yuv420p','-c:v','libx264','-crf','22','-preset','fast','-c:a','aac','-b:a','128k','-movflags','+faststart','-t',str(duration),'-shortest',str(video)],check=True)
report={'episode':E['id'],'media':str(video),'bytes':video.stat().st_size,'duration_s':round(duration,2),'voice':'Habibi-TTS Specialized MSA Apache-2.0 natural speed 1.00, no atempo, 24 denoising steps',
'authored_segments':6,'status':'RENDER_COMPLETE_PENDING_ARABIC_ASR_QA_NOT_PUBLISHED','requires_listening_review':True,
'voice_terms':'Only Specialized MSA checkpoint. Reference MSA sample bundled with public repository.',
'source':E.get('source'), 'scene_durations_s':[round(x,2) for x in durations]}
(OUT/'production_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False),flush=True)