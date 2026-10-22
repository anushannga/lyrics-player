"""Force-align only supplied sung/spoken text; no headings or effect notes."""
import json,re
from pathlib import Path
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio,pad_or_trim
from faster_whisper.tokenizer import Tokenizer
R=Path(__file__).resolve().parents[1];lyrics=json.loads((R/'lyrics.json').read_text())
MP3=next((Path.home()/'Downloads').glob('Mal Peththak Se Susinidu Sitha*6th Lane*mp3'))
a=decode_audio(str(MP3));m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
# Audio structure: six sung refrains, two rap verses and the short telephone speech.
chunks=[('chorus1',0,9,12,39),('rap1',0,19,37,59),('rap1',19,37,56,80),('chorus2',0,9,79,102),('rap2',0,16,100,125),('rap2',16,37,122,152),('chorus3',0,9,151,176),('dialogue',0,6,199.5,209),('chorus4',0,9,209,231),('chorus5',0,9,230,252),('chorus6',0,9,250,272.3)]
results={};evidence=[]
for section,first,last,start,end in chunks:
 rows=[v for v in lyrics if v['section']==section][first:last]
 lang='si' if rows[0]['language']=='si' else 'en';tok=Tokenizer(m.hf_tokenizer,True,task='transcribe',language=lang)
 texts=[re.sub(r'[^A-Za-z0-9\s]','',v['alignment_text']) for v in rows]
 clip=a[round(start*16000):min(len(a),round(end*16000))]
 enc=m.encode(pad_or_trim(m.feature_extractor(clip)))
 tokens=tok.encode('... '+' '.join(texts)+' ...')
 aligned=m.find_alignment(tok,[tokens],enc,len(clip)//160)[0]
 words=[{'word':w['word'].strip(),'start':round(float(w['start'])+start,3),'end':round(float(w['end'])+start,3),'probability':float(w.get('probability',0))} for w in aligned if w['word'].strip() not in ['...','.']]
 counts=[len(v.split()) for v in texts]
 evidence.append({'section':section,'line_range':[first,last],'audio_range':[start,end],'words':words,'expected_words':sum(counts)})
 (R/'alignment_evidence.json').write_text(json.dumps(evidence,indent=2))
 if len(words)!=sum(counts):raise ValueError((section,first,'Word segmentation mismatch',len(words),sum(counts)))
 pos=0
 for row,n in zip(rows,counts):
  group=words[pos:pos+n];pos+=n
  result={'id':row['id'],'section':section,'section_line':row['section_line'],'start':group[0]['start'],'end':group[-1]['end'],'words':group}
  results[row['id']]=result
  print(row['id'],section,round(result['start'],2),round(result['end'],2),row['text'],flush=True)
 (R/'alignment_raw.json').write_text(json.dumps(list(results.values()),indent=2))
print('Aligned',len(results),'supplied lyric lines',flush=True)
