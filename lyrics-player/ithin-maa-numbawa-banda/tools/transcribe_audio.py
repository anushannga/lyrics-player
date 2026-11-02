from pathlib import Path
import json
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
R=Path(__file__).resolve().parents[1];p=next((Path.home()/'Downloads').glob('Ithin Maa Numbawa Banda.mp3'));a=decode_audio(str(p))
m=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True);rows=[]
for start in range(0,int(len(a)/16000),20):
 segments,_=m.transcribe(a[start*16000:(start+20)*16000],language='si',beam_size=1,temperature=0,condition_on_previous_text=False,max_new_tokens=90,no_repeat_ngram_size=3,initial_prompt='manamal hinaawe muhune urumen genaa pethi peede malak wee medaa kaetayam wunaane harde namakin manaa subha heene handak paayalaa naeraama daethe methekin ehaa haemadedi langin innawaa sandath maage numba irath maage numba ithin maa numbawa baendaa mage abhiyasa lokayak thiyaa')
 for s in segments:
  row=dict(start=start+s.start,end=start+s.end,text=s.text);rows.append(row);print(row,flush=True)
 (R/'transcript_windows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
