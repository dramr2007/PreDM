from pathlib import Path
import sys, re, numpy as np, soundfile as sf
from huggingface_hub import snapshot_download
ROOT = Path(__file__).resolve().parent
model_path = snapshot_download(
    repo_id="oddadmix/Nabra-Saudi-7M",
    allow_patterns=["*.py", "af_msa.pt", "nabra_saudi_7m.pth", "*.json", "kokoro_patched/**", "arabic_g2p/**", "arabic/**", "phonemizer/**"],
    ignore_patterns=["training/**", "samples/**", "*/training/**", "nabra_saudi_7m_v1_direct.pth"],
)
sys.path.insert(0, model_path)
from load_model import load
print("Loading the original Nabra-Saudi-7M voice af_msa", flush=True)
model, pipeline, voice = load()
text = (ROOT / "input_HAI-C0045.txt").read_text(encoding="utf-8")
parts = [x.strip() for x in re.split(r"(?<=[.!؟،؛])\s+", text) if x.strip()]
audios=[]
for i,part in enumerate(parts):
    for item in pipeline(part, voice=voice):
        waveform=item[2]
        if waveform is None: continue
        if hasattr(waveform,"detach"): waveform=waveform.detach().cpu().numpy()
        waveform=np.asarray(waveform,dtype=np.float32).reshape(-1)
        audios.append(waveform)
    if i<len(parts)-1:
        audios.append(np.zeros(int(0.20 * 24000), dtype=np.float32))
if not audios:
    raise RuntimeError("Nabra returned no audio")
audio=np.concatenate(audios)
audio=np.nan_to_num(audio,nan=0,posinf=0,neginf=0)
peak=np.max(np.abs(audio))
if peak<=0.0001: raise RuntimeError("Silence: model produced no valid signal")
# Master to -1.8 dBFS peak, not to 0dBFS.
audio=audio*min(2.5,10**(-1.8/20)/peak)
dest=ROOT/"output"/"HAI-C0045_arabic_voice_master.wav"
dest.parent.mkdir(exist_ok=True)
sf.write(str(dest),audio,24000,subtype="PCM_16")
print("SUCCESS",dest,"duration",round(len(audio)/24000,2),"s", "peak",float(np.max(np.abs(audio))),flush=True)
