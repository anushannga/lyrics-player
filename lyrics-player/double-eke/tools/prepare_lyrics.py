from pathlib import Path
import json,re,unicodedata
R=Path(__file__).resolve().parents[1]
cons=dict(zip('කඛගඝඞඟචඡජඣඤඥඦටඨඩඪණඬතථදධනඳපඵබභමඹයරලවශෂසහළෆ', ['k','kh','g','gh','ng','ng','ch','ch','j','jh','ny','gn','nj','t','th','d','dh','n','nd','th','th','d','dh','n','nd','p','ph','b','bh','m','mb','y','r','l','w','sh','sh','s','h','l','f']))
vowels={'අ':'a','ආ':'aa','ඇ':'ae','ඈ':'ae','ඉ':'i','ඊ':'ee','උ':'u','ඌ':'uu','ඍ':'ru','එ':'e','ඒ':'e','ඓ':'ai','ඔ':'o','ඕ':'o','ඖ':'au'}
marks={'ා':'aa','ැ':'ae','ෑ':'ae','ි':'i','ී':'ee','ු':'u','ූ':'uu','ෘ':'ru','ෲ':'ruu','ෙ':'e','ේ':'e','ෛ':'ai','ො':'o','ෝ':'o','ෞ':'au','්':''}
def roman(word):
 out='';i=0
 while i<len(word):
  c=word[i]
  if c in cons:
   i+=1;v='a'
   if i<len(word) and word[i] in marks:v=marks[word[i]];i+=1
   out+=cons[c]+v;continue
  out+=vowels.get(c,{'ං':'ng','ඃ':'h'}.get(c,c if c.isascii() and c.isalnum() else ''));i+=1
 return out or 'a'
rows=[]
for section,block in enumerate((R/'lyrics_unicode.txt').read_text().strip().split('\n\n')):
 for j,line in enumerate(block.splitlines()):
  text=unicodedata.normalize('NFC',line.strip());text=re.sub(r'\s+-\s+',' ',text)
  rows.append(dict(id=len(rows),section=f'section{section+1}',section_line=j,language='si',text=text,alignment_text=' '.join(roman(w) for w in text.split())))
import copy
hook=copy.deepcopy(rows[25:33])
for repeat in [1,2]:
 for j,row in enumerate(hook):
  v=copy.deepcopy(row);v.update(id=len(rows),section=f'hook_repeat{repeat}',section_line=j);rows.append(v)
(R/'lyrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(len(rows),'lines',sum(len(v['text'].split()) for v in rows),'words')
