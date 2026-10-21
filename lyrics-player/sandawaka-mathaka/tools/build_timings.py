"""Build song-specific cues from local phonetic alignment and repetition checks."""
import hashlib
import json
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
audio=Path.home()/'Downloads/Sandawaka Mathaka.mp3'
report=json.loads((ROOT/'render_report.json').read_text())
sections=json.loads((ROOT/'section_alignment.json').read_text())
refined=json.loads((ROOT/'refined_alignment.json').read_text())
assert len(report['lines'])==30

def line_starts(words,lines):
    words=[w for w in words if w['word'].strip()!='...']
    starts=[]; index=0
    for line in lines:
        starts.append(round(words[index]['start'],3))
        index+=len(line.split())
    assert index==len(words)
    return starts

starts=[]
for section in sections:
    words=section['words']
    if section['first']==0:words=refined[0]
    if section['first']==12:words=refined[1]
    if section['first']==28:
        # Humming has no reliable text alignment. The unprompted vocal
        # transcription detects its onset at 140.76s; final phrase at 145.22s.
        starts.extend([140.760,145.220])
    else:starts.extend(line_starts(words,section['lines']))

assert len(starts)==30
assert all(b-a>1 for a,b in zip(starts,starts[1:]))
cues=[{'time':0.0,'line':-1}]
cues.extend({'time':t,'line':i} for i,t in enumerate(starts))
# Measured vocal end 65.74s; the next phrase begins 87.86s.
cues.append({'time':67.0,'line':-1})
cues.append({'time':149.0,'line':-1})
cues.sort(key=lambda c:c['time'])
data={
    'status':'audio-aligned lyric starts (local phonetic alignment)',
    'lyrics_id':report['id'],
    'audio_sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),
    'audio_duration':156.14,
    'method':'Known phonetic lyric text aligned in short vocal sections; repeated choruses checked against spectral correlation. Humming onset anchored to unprompted transcription.',
    'verified_by_listening':False,
    'cues':cues,
}
path=ROOT/'timings.json'
if path.exists():
    backup=ROOT/('timings-backup-'+time.strftime('%Y%m%d-%H%M%S')+'.json')
    backup.write_bytes(path.read_bytes())
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Saved',len(starts),'lyric starts and 3 clear events')
for i,t in enumerate(starts):print(f'{i+1:02d} {t:7.3f}s')
