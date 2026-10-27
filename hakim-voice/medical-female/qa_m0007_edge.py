from pathlib import Path
import json, re, unicodedata
from difflib import SequenceMatcher
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

P=Path(__file__).resolve().parent/'out_edge_m0007'
report=json.loads((P/'production_report.json').read_text())
a,sr=sf.read(P/'narration.wav')
assert sr==24000 and 15 < len(a)/sr < 95 and np.isfinite(a).all()
assert float(np.max(np.abs(a))) < 0.99
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFKD',s) if unicodedata.category(c)!='Mn')
    s=s.translate(str.maketrans({'أ':'ا','إ':'ا','آ':'ا','ى':'ي','ة':'ه','ؤ':'و','ئ':'ي'}))
    return re.sub(r'[^\u0621-\u064a0-9 ]+',' ',s).strip()
def fuzzy_recall(ref,hyp):
    source=ref.split(); heard=hyp.split()
    if not heard:return 0.0
    return sum(any(SequenceMatcher(None,w,h).ratio()>=.78 for h in heard) for w in source)/max(len(source),1)
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4)
checks=[]
for i,expected in enumerate(report['narration']):
    segments,_=model.transcribe(str(P/f'scene-{i+1}.wav'),language='ar',beam_size=5,condition_on_previous_text=False)
    heard=' '.join(s.text.strip() for s in segments)
    ref,hyp=norm(expected),norm(heard)
    char=SequenceMatcher(None,ref,hyp,autojunk=False).ratio(); recall=fuzzy_recall(ref,hyp)
    critical=[]
    if i==2:
        words=hyp.split()
        if not any('رفض' in w for w in words): critical.append('reviewer_refusal')
    if i==4:
        words=hyp.split()
        if 'لم' not in words: critical.append('negation')
        if not any('فشل' in w for w in words): critical.append('treatment_failure')
        if not any('علاج' in w for w in words): critical.append('treatment')
    ok=char>=.75 and recall>=.75 and not critical
    checks.append({'scene':i+1,'transcript':heard,'char_similarity':round(char,3),'fuzzy_word_recall':round(recall,3),'critical_missing':critical,'pass':ok})
report.update({'automatic_asr_model':'Whisper small Arabic CPU int8','scene_checks':checks,'automated_audio_status':'PASS' if all(x['pass'] for x in checks) else 'HOLD_ASR_MISMATCH','human_listening':'not_performed'})
(P/'production_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'status':report['automated_audio_status'],'scenes':checks},ensure_ascii=False),flush=True)
assert report['automated_audio_status']=='PASS','Arabic narration held: one or more scenes failed the stricter pronunciation check.'
