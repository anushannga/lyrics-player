"""Conservative ellipses: only long phrase-final vocals, never punctuation alone."""
import json
from pathlib import Path
import numpy as np
from scipy.io import wavfile
R=Path(__file__).resolve().parents[1]
sr,a=wavfile.read(R/'analysis/song-vocals.wav')
lyrics=json.loads((R/'lyrics.json').read_text());alignment=json.loads((R/'alignment.json').read_text())
selected=[];evidence=[]
for lyric,row in zip(lyrics,alignment):
 j=len(row['words'])-1;w=row['words'][j];start=w['start'];end=w['end']
 clip=a[round(start*sr):round(end*sr)]
 env=np.array([np.sqrt(np.mean(clip[i:i+320]**2)) for i in range(0,max(0,len(clip)-320),160)])
 voiced=0;span=0
 if len(env):
  # Reject quiet tails relative to the song's vocal level as well as local noise.
  threshold=max(float(np.percentile(env,90))*.18,.004)
  active=np.flatnonzero(env>threshold)
  voiced=len(active)*.01
  if len(active):span=(active[-1]-active[0]+1)*.01
 duration=end-start
 choose=duration>=1.25 and voiced>=.95 and lyric['text'].split()[-1].strip('.') not in {'මා','හා','මේ','මම','ඔබ','දැන්'}
 if choose:selected.append([lyric['id'],j])
 evidence.append(dict(line=lyric['id'],word=j,text=lyric['text'].split()[-1],duration=round(duration,3),voiced_seconds=round(voiced,3),voice_span=round(span,3),selected=choose))
(R/'sustain_selection.json').write_text(json.dumps(dict(words=selected,evidence=evidence,listening_confirmed=False,method='Phrase-final content word; at least 1.25s aligned duration and 0.95s isolated vocal activity'),ensure_ascii=False,indent=2))
print(len(selected),'conservative phrase-final ellipses')
