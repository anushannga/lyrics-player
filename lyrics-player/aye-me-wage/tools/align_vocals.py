import json
from pathlib import Path
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio,pad_or_trim
from faster_whisper.tokenizer import Tokenizer
R=Path(__file__).resolve().parents[1];lyrics=json.loads((R/'lyrics.json').read_text())
p=next((Path.home()/'Downloads').glob('Aye Me Wage.mp3'));audio=decode_audio(str(R/'analysis/song-vocals.wav'))
m=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
tok=Tokenizer(m.hf_tokenizer,True,task='transcribe',language='si');rows=[];evidence=[]
for ids,start,end in json.loads((R/'alignment_windows.json').read_text()):
 group=[lyrics[i] for i in ids];clip=audio[round(start*16000):round(end*16000)]
 enc=m.encode(pad_or_trim(m.feature_extractor(clip)))
 tokens=tok.encode('... '+' '.join(v['alignment_text'] for v in group)+' ...')
 result=m.find_alignment(tok,[tokens],enc,len(clip)//160)[0]
 words=[{'word':w['word'].strip(),'start':round(float(w['start'])+start,3),'end':round(float(w['end'])+start,3),'probability':float(w.get('probability',0))} for w in result if w['word'].strip() not in ['...','.']]
 expected=sum(len(v['alignment_text'].split()) for v in group);assert len(words)==expected,(ids,len(words),expected)
 evidence.append(dict(ids=ids,window=[start,end],words=words));pos=0
 for v in group:
  n=len(v['alignment_text'].split());w=words[pos:pos+n];pos+=n
  rows.append(dict(id=v['id'],section=v['section'],section_line=v['section_line'],start=w[0]['start'],end=w[-1]['end'],words=w))
  print(v['id'],w[0]['start'],w[-1]['end'],v['text'],flush=True)
 (R/'vocal_alignment_raw.json').write_text(json.dumps(rows,indent=2));(R/'alignment_evidence.json').write_text(json.dumps(evidence,indent=2))
flat=[w for row in rows for w in row['words']];repairs=[]
for i,w in enumerate(flat):
 if i and w['start']<=flat[i-1]['start']:
  repairs.append(dict(index=i,old=w['start']));w['start']=round(flat[i-1]['start']+.04,3)
 w['end']=max(w['end'],w['start']+.04)
for i,w in enumerate(flat[:-1]):w['end']=min(w['end'],flat[i+1]['start'])
for row in rows:row['start']=row['words'][0]['start'];row['end']=row['words'][-1]['end']
(R/'alignment.json').write_text(json.dumps(rows,indent=2));(R/'alignment_repairs.json').write_text(json.dumps(repairs,indent=2))
