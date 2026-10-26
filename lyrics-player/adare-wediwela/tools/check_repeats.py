import json
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft,correlate
R=Path(__file__).resolve().parents[1];sr,a=wavfile.read(R/'analysis/song-vocals.wav')
_,times,z=stft(a,fs=sr,nperseg=512,noverlap=352);f=np.log1p(abs(z)*1000)
# Normalize spectral shape to compare the repeated vocal, rather than loudness.
f=f-f.mean(axis=0,keepdims=True);f/=np.maximum(np.linalg.norm(f,axis=0,keepdims=True),1e-8)
rows=json.loads((R/'alignment.json').read_text());evidence=[]
for j in range(12):
 first=rows[5+j];second=rows[21+j];start=first['start'];duration=min(2.5,first['end']-start)
 left=round(start*100);n=round(duration*100);template=f[:,left:left+n]
 expected=round((start+101.05)*100);lo=expected-70;hi=expected+70
 scores=[]
 for k in range(lo,hi+1):scores.append(float(np.mean(np.sum(template*f[:,k:k+n],axis=0))))
 best=int(np.argmax(scores))+lo;score=max(scores);delta=best/100-start
 evidence.append(dict(first=first['id'],second=second['id'],offset=round(delta,3),score=round(score,4)))
 if score>.9:
  for w,original in zip(second['words'],first['words']):
   w['start']=round(original['start']+delta,3);w['end']=round(original['end']+delta,3)
  second['start']=second['words'][0]['start'];second['end']=second['words'][-1]['end']
(R/'repeat_evidence.json').write_text(json.dumps(evidence,indent=2));(R/'alignment.json').write_text(json.dumps(rows,indent=2));print(evidence)
