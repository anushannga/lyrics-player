import json
from pathlib import Path
R=Path(__file__).resolve().parents[1];a=json.loads((R/'alignment.json').read_text());words=[]
for row in a:
 j=len(row['words'])-1;w=row['words'][j];duration=w['end']-w['start']
 if duration>=1.0 or (w['word']=='kohedo' and duration>=.75):words.append([row['id'],j])
(R/'sustain_selection.json').write_text(json.dumps(dict(words=words,listening_confirmed=False,method='Aligned final word holds; progressive dots remain on the sung interval'),indent=2))
print(len(words),'held endings')
