from pathlib import Path
import subprocess,sys,shutil
p=Path(__file__).resolve().parent
(p/'input_HAI-C0045.txt').write_text((p/'input_HAI-C0046.txt').read_text(encoding='utf-8'),encoding='utf-8')
subprocess.run([sys.executable,str(p/'nabra_tts_c0045.py')],check=True)
shutil.copyfile(p/'output/HAI-C0045_arabic_voice_master.wav',p/'output/HAI-C0046_arabic_voice_master.wav')
