from pathlib import Path
import subprocess,sys,shutil
p=Path(__file__).resolve().parent
source=p/'input_HAI-C0047.txt'
target=p/'input_HAI-C0045.txt'
prior=target.read_bytes()
try:
 target.write_bytes(source.read_bytes())
 subprocess.run([sys.executable,str(p/'nabra_tts_c0045.py')],check=True)
 shutil.copyfile(p/'output/HAI-C0045_arabic_voice_master.wav',p/'output/HAI-C0047_arabic_voice_master.wav')
finally:
 target.write_bytes(prior)
