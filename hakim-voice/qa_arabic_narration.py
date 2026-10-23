#!/usr/bin/env python3
"""Automated Arabic pronunciation screen. Not a replacement for human listening.
Rejects missing, hallucinated, or strongly mismatched narration before social upload.
"""
import json, re, sys
from pathlib import Path
from difflib import SequenceMatcher
from faster_whisper import WhisperModel

root=Path(sys.argv[1]); doc=Path(sys.argv[2]); e=json.loads(doc.read_text(encoding='utf8'))
output=root/'arabic_speech_qa.json'; episode=root/'production_report.json'
model=WhisperModel('base',device='cpu',compute_type='int8')
def clean(s):
    s=re.sub(r'[\u064b-\u065f\u0670\u0640]','',s)
    s=s.translate(str.maketrans({'أ':'ا','إ':'ا','آ':'ا','ى':'ي','ؤ':'و','ئ':'ي'}))
    return ' '.join(re.findall(r'[\u0621-\u064a]+',s)).strip()
rows=[]
for i,seg in enumerate(e['segments']):
    p=root/('audio_%02d.wav'%i)
    chunks,info=model.transcribe(str(p),language='ar',beam_size=5,condition_on_previous_text=False,vad_filter=False)
    got=' '.join(x.text.strip() for x in chunks).strip()
    expected=seg['text']
    a,b=clean(expected),clean(got)
    ratio=SequenceMatcher(None,a,b).ratio() if a and b else 0
    w1=set(a.split());w2=set(b.split())
    recall=len(w1&w2)/max(1,len(w1))
    row={'scene':i+1,'expected':expected,'heard_by_asr':got,'char_similarity':round(ratio,3),'unique_word_recall':round(recall,3)}
    rows.append(row)
    print(json.dumps(row,ensure_ascii=False),flush=True)
avg=sum(z['char_similarity'] for z in rows)/len(rows)
avgwords=sum(z['unique_word_recall'] for z in rows)/len(rows)
# Arabic ASR is imperfect, but publication screening must reject scene-level corruption.
# Require strong aggregate agreement plus no weak scene; human listening remains mandatory.
passed=(avg>=0.90 and avgwords>=0.70 and
        all(z['char_similarity']>=0.86 and z['unique_word_recall']>=0.60 for z in rows))
status='ASR_PASS_PENDING_FINAL_AUDIO_LISTENING_QA' if passed else 'ASR_FAILED_DO_NOT_PUBLISH'
report={'status':status,'mean_char_similarity':round(avg,3),'mean_unique_word_recall':round(avgwords,3),'scenes':rows,'is_publication_approved':False}
output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
p=json.loads(episode.read_text(encoding='utf8'));p.update({'status':status,'published':False,'arabic_asr_gate':{'mean_char_similarity':round(avg,3),'mean_word_recall':round(avgwords,3)},'requires_listening_review':True})
episode.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
if not passed:raise SystemExit('Arabic narration is not intelligible enough for Hakim AI publication; see '+str(output))
print('Arabic ASR passed; human auditory review and final visual checks still required.')
