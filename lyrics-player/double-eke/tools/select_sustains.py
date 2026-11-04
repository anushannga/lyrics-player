from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
lyrics=json.loads((R/'lyrics.json').read_text());rows=json.loads((R/'alignment.json').read_text());selected=[];evidence=[]
for lyric,row in zip(lyrics,rows):
 j=len(row['words'])-1;word=row['words'][j];duration=word['end']-word['start']
 # Fast rap words do not receive dots solely because of punctuation.
 choose=duration>=1.35 and (25<=lyric['id']<=32 or lyric['id']>=56)
 if choose:selected.append([lyric['id'],j])
 evidence.append(dict(line=lyric['id'],word=j,text=lyric['text'].split()[-1],duration=round(duration,3),selected=choose))
(R/'sustain_selection.json').write_text(json.dumps(dict(words=selected,evidence=evidence,listening_confirmed=False,method='Conservative long final words in repeated hook; full-mix local alignment'),ensure_ascii=False,indent=2))
print(len(selected),'long hook words selected')
