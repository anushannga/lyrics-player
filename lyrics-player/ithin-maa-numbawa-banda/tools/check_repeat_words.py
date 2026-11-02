from pathlib import Path
import json
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
R=Path(__file__).resolve().parents[1];a=decode_audio(str(Path.home()/'Downloads/Ithin Maa Numbawa Banda.mp3'));m=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True);rows=[]
for start,end in [(53,64),(64,76),(117,128),(128,139),(139,151)]:
 seg,_=m.transcribe(a[start*16000:end*16000],language='si',beam_size=1,temperature=0,condition_on_previous_text=False,max_new_tokens=90,no_repeat_ngram_size=3,initial_prompt='sandath maage numba irath maage numba ithin maa numbawa baendaa adath maage numba hetath maage numba wadammaana yam kaendaa')
 for s in seg:
  row=dict(window=[start,end],start=start+s.start,end=start+s.end,text=s.text);rows.append(row);print(row,flush=True)
 (R/'repeat_transcript.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
