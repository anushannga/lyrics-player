import json
from pathlib import Path
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
R=Path(__file__).resolve().parents[1]
MP3=next((Path.home()/'Downloads').glob('Mal Peththak Se Susinidu Sitha*6th Lane*mp3'))
a=decode_audio(str(MP3));m=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
rows=[]
for start in range(0,273,24):
 clip=a[start*16000:min(len(a),(start+28)*16000)]
 if not len(clip):continue
 segs,_=m.transcribe(clip,language='en',beam_size=1,temperature=0,condition_on_previous_text=False,max_new_tokens=160,no_repeat_ngram_size=3,compression_ratio_threshold=None,log_prob_threshold=None,word_timestamps=True)
 for s in segs:
  row={'window':start,'start':round(s.start+start,3),'end':round(s.end+start,3),'text':s.text,'words':[{**vars(w),'start':round(w.start+start,3),'end':round(w.end+start,3)} for w in s.words or []]};rows.append(row)
  print(row['start'],row['end'],s.text,flush=True)
 (R/'transcript_windows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
