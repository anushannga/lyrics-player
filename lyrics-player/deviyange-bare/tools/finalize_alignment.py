import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rows={v['id']:v for name in ['combined_alignment.json','rap_alignment.json','rap_refinements.json','chorus1_alignment.json','chorus2_alignment.json'] if (R/name).exists() for v in json.loads((R/name).read_text())}
# Keep the chorus ending visible during its held vowel before the final rap.
rows[106]['words'][0]['start']=362.60
rows[105]['words'][-1]['end']=362.60
a=[rows[i] for i in range(130)];flat=[w for row in a for w in row['words']];repairs=[]
for i,w in enumerate(flat):
 if i and w['start']<=flat[i-1]['start']:
  repairs.append(dict(word=w['word'],old=w['start'],new=round(flat[i-1]['start']+.025,3)));w['start']=round(flat[i-1]['start']+.025,3)
 w['end']=max(w['end'],w['start']+.025)
for w,n in zip(flat,flat[1:]):w['end']=min(w['end'],n['start'])
for row in a:row['start']=row['words'][0]['start'];row['end']=row['words'][-1]['end']
(R/'alignment.json').write_text(json.dumps(a,indent=2));(R/'final_alignment_repairs.json').write_text(json.dumps(repairs,indent=2));print(len(a),'lines,',len(flat),'words,',len(repairs),'collapsed onset repairs')
