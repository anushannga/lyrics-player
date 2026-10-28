"""Remove silent lead-ins and tails from locally aligned vocal words."""
import json
from pathlib import Path
import numpy as np
from scipy.io import wavfile
R=Path(__file__).resolve().parents[1];sr,a=wavfile.read(R/'analysis/song-vocals.wav')
rows=json.loads((R/'alignment.json').read_text());changes=[]
windows={ids[0]:(start,end) for ids,start,end in json.loads((R/'alignment_windows.json').read_text()) if len(ids)==1}
for row in rows:
 # The alignment decoder often truncates a held last vowel. Include the vocal
 # tail within the independently bounded phrase, never the next phrase.
 if row['id'] in windows:
  left,right=windows[row['id']]
  last=row['words'][-1];segment=a[round(last['start']*sr):round(right*sr)]
  energy=np.array([np.sqrt(np.mean(segment[i:i+320]**2)) for i in range(0,max(0,len(segment)-320),160)])
  if len(energy):
   voiced=np.flatnonzero(energy>max(float(np.percentile(energy,95))*.14,.004))
   if len(voiced):last['end']=min(right,round(last['start']+(voiced[-1]+2)*.01+.04,3))
 for j,w in enumerate(row['words']):
  start,end=w['start'],w['end'];clip=a[round(start*sr):round(end*sr)]
  env=np.array([np.sqrt(np.mean(clip[i:i+320]**2)) for i in range(0,max(0,len(clip)-320),160)])
  if not len(env):continue
  threshold=max(float(np.percentile(env,95))*.12,.003)
  active=env>threshold
  # Require several voiced frames to avoid a tiny residual music transient.
  stable=np.convolve(active.astype(int),np.ones(6,dtype=int),'same')>=4
  indices=np.flatnonzero(stable)
  if not len(indices):continue
  newstart=round(max(start,start+indices[0]*.01-.04),3)
  newend=round(min(end,start+(indices[-1]+2)*.01+.06),3)
  if newend-newstart<.08:continue
  if newstart-start>.12:
   w['start']=newstart;changes.append(dict(line=row['id'],word=j,old=start,new=newstart,reason='silent lead-in in isolated vocals'))
  if end-newend>.2:w['end']=max(newend,w['start']+.08)
 row['start']=row['words'][0]['start'];row['end']=row['words'][-1]['end']
flat=[word for row in rows for word in row['words']]
for word,following in zip(flat,flat[1:]):
 word['end']=min(word['end'],following['start']-.001)
 assert word['end']>word['start'], 'Vocal boundary overlaps next word'
for row in rows:
 row['start']=row['words'][0]['start'];row['end']=row['words'][-1]['end']
(R/'alignment.json').write_text(json.dumps(rows,indent=2));(R/'vocal_boundary_changes.json').write_text(json.dumps(changes,indent=2));print(len(changes),'silent lead-ins removed')
