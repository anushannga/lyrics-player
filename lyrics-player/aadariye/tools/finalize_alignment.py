import json,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rows={v['id']:v for v in json.loads((R/'alignment_raw.json').read_text())}
rows.update({v['id']:v for v in json.loads((R/'hook3_refined.json').read_text())})
corrections_path=R/'vocal_onset_corrections.json'
if corrections_path.exists():
 corrections=json.loads(corrections_path.read_text())
 for change in corrections['changes']:
  rows[change['line']]['words'][change.get('word_index',0)]['start']=change['new_onset']
 for change in corrections.get('end_corrections',[]):
  rows[change['line']]['words'][change.get('word_index',-1)]['end']=change['end']
ordered=sorted(rows.values(),key=lambda v:v['id']);repairs=[]
flat=[w for row in ordered for w in row['words']]
for i,w in enumerate(flat):
 if i and w['start']<=flat[i-1]['start']:
  before=w['start'];w['start']=round(flat[i-1]['start']+.025,3);repairs.append({'word':w['word'],'old':before,'new':w['start']})
 w['end']=max(w['end'],w['start']+.025)
for i,w in enumerate(flat[:-1]):w['end']=min(w['end'],flat[i+1]['start'])
for row in ordered:row['start']=row['words'][0]['start'];row['end']=row['words'][-1]['end']
assert len(ordered)==57
assert all(a['start']<b['start'] for a,b in zip(flat,flat[1:]))
(R/'alignment.json').write_text(json.dumps(ordered,indent=2))
(R/'timing_notes.json').write_text(json.dumps({'method':'Local phonetic forced alignment with unprompted ASR section windows and independent spectral repeat checks','first_word_seconds':ordered[0]['start'],'section_starts':{v['section']:v['start'] for v in ordered if v['section_line']==0},'repairs':repairs,'hook3_refinement':'Window expanded to include the full leading vocal, which began before the initial window.','listening_confirmed':False},indent=2))
print(len(ordered),'lyric lines,',len(flat),'words;',len(repairs),'collapsed onset repairs')
