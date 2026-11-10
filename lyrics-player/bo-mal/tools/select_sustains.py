from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];a=json.loads((R/'alignment.json').read_text());l=json.loads((R/'lyrics.json').read_text());words=[]
for i,row in enumerate(a):
 for j,w in enumerate(row['words']):
  end=w['end'];last=j==len(row['words'])-1
  # Dots follow the sung interval; the final frame still holds until the next lyric.
  explicit='..' in l[i]['text'].split()[j]
  if end-w['start']>=(.75 if explicit else (1.25 if last else 1.8)):words.append([i,j])
(R/'sustain_selection.json').write_text(json.dumps(dict(words=words,listening_confirmed=False,method='Long aligned words including explicitly sustained internal words'),indent=2))
print(len(words),'held words')
