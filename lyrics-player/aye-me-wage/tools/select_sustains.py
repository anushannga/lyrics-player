"""Choose long vocal words from isolated audio, including internal held words."""
import json
from pathlib import Path
import numpy as np
from scipy.io import wavfile
R=Path(__file__).resolve().parents[1];sr,a=wavfile.read(R/'analysis/song-vocals.wav')
lyrics=json.loads((R/'lyrics.json').read_text());rows=json.loads((R/'alignment.json').read_text());selected=[];evidence=[]
short={'හා','මා','මේ','මට','තව','නුබ','ඔබ','මං','අපි','ආ','ඒ','සේ','ඉනු','බෑ','මත','කැට','පිට'}
for lyric,row in zip(lyrics,rows):
 for j,(text,w) in enumerate(zip(lyric['text'].split(),row['words'])):
  clean=text.strip('.');duration=w['end']-w['start'];clip=a[round(w['start']*sr):round(w['end']*sr)]
  env=np.array([np.sqrt(np.mean(clip[k:k+320]**2)) for k in range(0,max(0,len(clip)-320),160)])
  voiced=0
  if len(env):voiced=float(np.sum(env>max(float(np.percentile(env,90))*.18,.004)))*.01
  limit=1.25 if j==len(row['words'])-1 else 1.6
  if clean in short:limit=max(limit,1.8)
  choose=duration>=limit and voiced>=limit*.75
  if choose:selected.append([lyric['id'],j])
  evidence.append(dict(line=lyric['id'],word=j,text=clean,duration=round(duration,3),voiced=round(voiced,3),selected=choose))
(R/'sustain_selection.json').write_text(json.dumps(dict(words=selected,evidence=evidence,listening_confirmed=False,method='Long aligned content words with isolated vocal activity; punctuation is not a timing cue'),ensure_ascii=False,indent=2))
print(len(selected),'sustained words selected')
