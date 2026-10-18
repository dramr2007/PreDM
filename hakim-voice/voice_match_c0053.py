"""HAI-C0053: zero-shot Arabic TTS from the owner's *published* HAI-C0040 voice reference.
Generate only the new audio, do not commit/upload the original voice sample or video.
Chatterbox voice resemblance requires listening; this is not native HeyGen voice ID rendering.
"""
from pathlib import Path
import re, time, json
import numpy as np, soundfile as sf, torch
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

P=Path(__file__).resolve().parent
ref=P/'voice_test53_reference.wav'
if not ref.exists() or ref.stat().st_size < 30000:
 raise SystemExit('Missing reference clip. No fallback voice permitted.')
text=(P/'input_HAI-C0053.txt').read_text(encoding='utf8').strip().replace('\n',' ')
if not text or len(text)<60: raise SystemExit('Narration script too short')
torch.set_num_threads(4)
print('Loading Chatterbox multilingual source voice model',flush=True)
model=ChatterboxMultilingualTTS.from_pretrained(device='cpu',t3_model='v3')
print('Synthesizing 53',text,flush=True)
start=time.time()
out=model.generate(text,language_id='ar',audio_prompt_path=str(ref),cfg_weight=0.3,exaggeration=0.5)
x=out.detach().cpu().float().numpy().reshape(-1)
if not np.all(np.isfinite(x)): raise SystemExit('NaN/Inf audio')
duration=len(x)/model.sr
peak=float(np.max(np.abs(x)))
rms=float(np.sqrt(np.mean(x*x)))
if not (10<duration<65) or peak<0.03 or rms<0.005:
 raise SystemExit(f'Invalid voice characteristics: duration {duration:.2f}s peak {peak:.3f} rms {rms:.3f}')
dest=P/'HAI-C0053_clustering_approved_voice.wav'
sf.write(str(dest),x,model.sr,subtype='PCM_16')
qa={'episode':'HAI-C0053','duration_sec':round(duration,3),'sample_rate':int(model.sr),'peak_dbfs':round(20*np.log10(peak+1e-9),2),'rms_dbfs':round(20*np.log10(rms+1e-9),2),'engine':'Chatterbox-Multilingual-V3','reference':'public HAI-C0040, ephemeral','voice_similarity':'not independently verified','human_audio_qa':'required','minutes_elapsed':round((time.time()-start)/60,2)}
(P/'HAI-C0053_voice_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf8')
print('SUCCESS',dest,qa,flush=True)
