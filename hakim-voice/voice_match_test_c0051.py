"""Noncommercial speech quality test of the user's publicly published Hakim AI sample.
Never commit or upload any reference audio / original video. Preview only.
Any use for publication requires source-voice license confirmation.
"""
from pathlib import Path
import time, json
import soundfile as sf
import torch
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
base=Path(__file__).resolve().parent
reference=base/"voice_test51_reference.wav"
if not reference.exists():
    raise SystemExit("Missing permitted reference: do not substitute another speaker")
torch.set_num_threads(4)
print("MODEL loading Chatterbox Multilingual V3 on CPU",flush=True)
started=time.time()
model=ChatterboxMultilingualTTS.from_pretrained(device="cpu",t3_model="v3")
print("MODEL loaded",round(time.time()-started,1),flush=True)
text="كيف يميّز الذكاء الاصطناعي الدائرة عن المثلث؟ هذا يُسمّى التصنيف. النموذج يختار فئة، وليس رقمًا مستمرًّا."
print("SYNTHESIZING",text,flush=True)
speech=model.generate(text,language_id="ar",audio_prompt_path=str(reference),cfg_weight=0.3,exaggeration=0.5)
wave=speech.detach().cpu().float().numpy().reshape(-1)
path=base/"HAI-C0051_voice_match_test.wav"
sf.write(path,wave,model.sr,subtype="PCM_16")
stats={"duration_s":round(len(wave)/model.sr,2),"sample_rate":model.sr,"peak":float(abs(wave).max()),"text":text,"model":"Chatterbox Multilingual V3","target":"approved user supplied HAI-C0040 reference","voice_match_verified":False,"publication_allowed":False}
(base/"HAI-C0051_voice_test_QA.json").write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding="utf-8")
print("VOICE_TEST_READY",stats,flush=True)
