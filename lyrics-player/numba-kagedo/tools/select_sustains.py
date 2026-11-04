import json
from pathlib import Path
R=Path(__file__).resolve().parents[1];a=json.loads((R/'alignment.json').read_text());words=[]
for i,row in enumerate(a):
 j=len(row['words'])-1;w=row['words'][j];end=w['end']
 if i+1<len(a) and a[i+1]['start']-end<10:end=a[i+1]['start']
 if end-w['start']>=1.5:words.append([row['id'],j])
(R/'sustain_selection.json').write_text(json.dumps(dict(words=words,listening_confirmed=False,method='Hold phrase-final words until next lyric, excluding long instrumental breaks'),indent=2))
print(len(words),'held phrase endings')
