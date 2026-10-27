from pathlib import Path
import json, re, statistics, unicodedata
from difflib import SequenceMatcher
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

P=Path(__file__).resolve().parent/'out'
report=json.loads((P/'production_report.json').read_text())
a,sr=sf.read(P/'narration.wav')
assert sr==24000 and 15 < len(a)/sr < 95
assert np.isfinite(a).all()
assert float(np.max(np.abs(a))) < 0.99
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFKD',s) if unicodedata.category(c)!='Mn')
    s=s.translate(str.maketrans({'أ':'ا','إ':'ا','آ':'ا','ى':'ي','ة':'ه','ؤ':'و','ئ':'ي'}))
    return re.sub(r'[^\u0621-\u064a0-9 ]+',' ',s).strip()
model=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=4)
segments,info=model.transcribe(str(P/'narration.wav'),language='ar',beam_size=3,condition_on_previous_text=False)
heard=' '.join(s.text.strip() for s in segments)
expected=' '.join(report['narration'])
ref,hyp=norm(expected),norm(heard)
similarity=SequenceMatcher(None,ref,hyp,autojunk=False).ratio()
expected_words=ref.split(); heard_words=set(hyp.split())
recall=sum(w in heard_words for w in expected_words)/max(1,len(expected_words))
report.update({'automatic_asr_model':'Whisper base Arabic CPU int8','transcript':heard,'char_similarity':round(similarity,3),'exact_word_recall':round(recall,3),'automated_audio_status':'PASS' if similarity>=0.62 and recall>=0.45 else 'HOLD_ASR_MISMATCH','human_listening':'not_performed'})
(P/'production_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'status':report['automated_audio_status'],'char_similarity':similarity,'word_recall':recall,'transcript':heard},ensure_ascii=False),flush=True)
assert report['automated_audio_status']=='PASS', 'Arabic narration held for review: automated transcription did not match sufficiently'
