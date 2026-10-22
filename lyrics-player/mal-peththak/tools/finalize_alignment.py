import json,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
lyrics=json.loads((R/'lyrics.json').read_text());raw={v['id']:v for v in json.loads((R/'alignment_raw.json').read_text())}
rows=copy.deepcopy(raw)
rows.update({v['id']:v for v in json.loads((R/'rap_alignment_refined.json').read_text())})
base=[copy.deepcopy(v) for v in raw.values() if v['section']=='chorus3']
# The first word absorbed leading silence in the forced alignment. ASR and the
# strongly matching repeated audio place the actual refrain entry near 151.52s.
base[0]['words'][0]['start']=151.52
matches={v['section']:v['matches'][0][1]-151.52 for v in json.loads((R/'chorus_repeat_matches.json').read_text())}
matches['chorus3']=0
for section,offset in matches.items():
 for source in base:
  item=next(v for v in lyrics if v['section']==section and v['section_line']==source['section_line'])
  dst=copy.deepcopy(source);dst.update(id=item['id'],section=section)
  for w in dst['words']:
   w['start']=round(w['start']+offset,3);w['end']=round(w['end']+offset,3)
  rows[item['id']]=dst
# Independently recognized telephone words, rather than the silent lead-in.
spoken=[[(200.52,201.48)],[(202.0,202.96)],[(203.76,204.22)],[(204.9,204.98),(204.98,205.18),(205.18,205.44)],[(205.76,205.86),(205.86,206.16),(206.16,206.58)],[(207.08,207.15),(207.15,207.43),(207.43,207.8)]]
for row,times in zip([v for v in lyrics if v['section']=='dialogue'],spoken):
 for word,(start,end) in zip(rows[row['id']]['words'],times):word.update(start=start,end=end)
# Give collapsed attention timestamps distinct short slots, keeping word order.
flat=[w for row in sorted(rows.values(),key=lambda v:v['id']) for w in row['words']]
repairs=[]
for i,w in enumerate(flat):
 if i and w['start']<=flat[i-1]['start']:
  original=w['start'];w['start']=round(flat[i-1]['start']+.025,3);repairs.append({'word':w['word'],'old':original,'new':w['start']})
 w['end']=max(w['end'],w['start']+.025)
for i,w in enumerate(flat[:-1]):
 if w['end']>flat[i+1]['start']:w['end']=flat[i+1]['start']
for row in rows.values():
 row['start']=row['words'][0]['start'];row['end']=row['words'][-1]['end']
assert len(rows)==134
assert all(a['start']<b['start'] for a,b in zip(flat,flat[1:]))
(R/'alignment.json').write_text(json.dumps(sorted(rows.values(),key=lambda v:v['id']),indent=2))
(R/'timing_notes.json').write_text(json.dumps({'chorus_entry_seconds':{s:round(151.52+v,3) for s,v in matches.items()},'collapsed_timestamp_repairs':repairs,'listening_confirmed':False,'notes':['Known supplied words aligned locally with small Whisper model.','Repeated refrains match independently in spectral features.','Only spoken/sung text is rendered; annotations and instrumental labels are omitted.','Exact vocal synchronization still requires listening confirmation.']},indent=2))
print('134 aligned lyric lines;',len(flat),'words;',len(repairs),'collapsed onset repairs')
