import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'manifest.json').read_text())
overrides=json.loads((ROOT/'timing_overrides.json').read_text())['line_starts']
aligned={r['line']:r for r in json.loads((ROOT/'alignment.json').read_text())}
for row in json.loads((ROOT/'alignment_refined.json').read_text()):
    if row['line']<69:aligned[row['line']]=row
for row in json.loads((ROOT/'alignment_tail.json').read_text()):
    if row['line']>=70:aligned[row['line']]=row
assert set(aligned)==set(range(77))
cues=[{'time':0.,'page':-1}]
for i,page in enumerate(manifest['pages']):
    row=aligned[page['line']]
    time=row['words'][page['word_start']]['start']
    if page['word_start']==0 and str(page['line']) in overrides:time=overrides[str(page['line'])]
    style='melodic' if 16<=page['line']<32 or page['line']>=49 else 'rap'
    cues.append({'time':round(time,3),'page':i,'line':page['line'],'style':style})
cues.append({'time':236.,'page':-1})
assert all(a['time']<b['time'] for a,b in zip(cues,cues[1:])),[(a,b) for a,b in zip(cues,cues[1:]) if a['time']>=b['time']]
audio=Path.home()/'Downloads/Sellakkaraya - Kaizer Kaiz Ft. Lil Neo.mp3'
data={'status':'locally audio-aligned phonetic lyric timing','lyrics_id':manifest['id'],'audio_sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),'duration':296.10,'verified_by_listening':False,'cues':cues}
previous=ROOT/'timings.json'
if previous.exists():
    saved=json.loads(previous.read_text())
    if saved.get('lyrics_id')==manifest['id']:
        for field in ('font_verified_by_user','rap_timing_verified_by_user'):
            if field in saved:data[field]=saved[field]
(ROOT/'timings.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Saved',len(cues),'events; minimum page interval',round(min(b['time']-a['time'] for a,b in zip(cues,cues[1:])),3),'seconds')
