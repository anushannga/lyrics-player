from pathlib import Path
import json,numpy as np
from scipy.signal import stft,correlate,find_peaks
from faster_whisper.audio import decode_audio
R=Path(__file__).resolve().parents[1];audio=decode_audio(str(Path.home()/'Downloads/Ithin Maa Numbawa Banda.mp3'))
_,_,z=stft(audio,fs=16000,nperseg=512,noverlap=192);f=np.log1p(abs(z)*1000);f-=f.mean(axis=0,keepdims=True);f/=np.maximum(np.linalg.norm(f,axis=0,keepdims=True),1e-8)
left=round(43.46*50);n=round(8*50);template=f[:,left:left+n]
score=np.zeros(f.shape[1]-n+1)
for k in range(len(f)):score+=correlate(f[k],template[k],mode='valid',method='fft')
score/=n
peaks,_=find_peaks(score,distance=round(8*50),height=.65)
report=[dict(start=round(float(p)/50,3),score=round(float(score[p]),4)) for p in peaks]
print(report,flush=True);(R/'repeat_evidence.json').write_text(json.dumps(report,indent=2))
