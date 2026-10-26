import json,unicodedata
from pathlib import Path
R=Path(__file__).resolve().parents[1]
verse1='''කවදාක හිතුණාද
මේ තරම් ආදරේ
නොදැනීම දින යාද
ලතවෙමි මේ හිතේ
දුටුවාද පෙරදාක
මේ හිඩැස පපුතුරේ
මතුදාක නිමවේද'''.splitlines()
v1phon='''kawadaka hithunada
me tharam aadare
nodaneema dina yaada
lathawemi me hithe
dutuwada peradaka
me hidasa paputhure
mathudaka nimaweda'''.splitlines()
pre=['ආයේ ආයේ මා හදේ','මන්දාරම් කතා විඳිම් මේ ආදරේ']
prephon=['aaye aaye maa hade','mandaaram kathaa vindim me aadare']
hook='''ආදරියේ
මගේ
ආදරියේ
රැයේ
මා දිහා බලා
හීනෙකින් මිදෙන්නකෝ
ආදරියේ
මගේ'''.splitlines()
hookphon='''aadariye
maage
aadariye
raye
maa diha bala
heenekin midennako
aadariye
maage'''.splitlines()
verse2='''රිදුණාද කිසිදාක
මේ සියුම් පපුතුරේ
නොහිතාම දෙඩුවාද
පෑරෙනා හදවතේ
මතුදාක නුඹ වේද
ආයෙමත් ආදරේ
මගේ නේද
මගේ නේද'''.splitlines()
v2phon='''ridunada kisidaaka
me siyum paputhure
nohithaama deduwada
paarenaa hadawathe
mathudaka numba weda
aayemath aadare
maage neda
maage neda'''.splitlines()
bridge='''හීනෙන් ඈ හා ළංවීම වින්දා
ගෙව්වේ ආදරේ මා හා
දෑහින් මා නිවාදෝ ආදරේ
ඈ හා මතකේ
වින්දාද පාරා
මා හිඳීදෝ ඈ හා
කවදා ළංවේදෝ ආදරේ'''.splitlines()
bphon='''heenen ae haa lanweema vindaa
gewwe aadare maa haa
daehin maa niwaado aadare
ae haa mathake
windaada paara
maa hindido ae haa
kawada lanwedo aadare'''.splitlines()
sections=[('verse1',verse1,v1phon),('pre1',pre,prephon),('hook1',hook,hookphon),('verse2',verse2,v2phon),('pre2',pre,prephon),('hook2',hook,hookphon),('bridge1',bridge,bphon),('hook3',hook,hookphon),('bridge2',bridge,bphon)]
rules=json.loads((R/'assets/isi-rules.json').read_text());rows=[]
for name,lines,phonetic in sections:
 for j,(text,phon) in enumerate(zip(lines,phonetic)):
  assert len(text.split())==len(phon.split()),text
  display=unicodedata.normalize('NFC',text)
  for a,b in rules:display=display.replace(a,b)
  assert not any('\u0d80'<=c<='\u0dff' for c in display),display
  rows.append({'id':len(rows),'section':name,'section_line':j,'language':'si','text':text,'alignment_text':phon,'display_text':display})
(R/'lyrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');(R/'lyrics_unicode.txt').write_text('\n'.join(v['text'] for v in rows)+'\n');(R/'lyrics_phonetic.txt').write_text('\n'.join(v['alignment_text'] for v in rows)+'\n')
print(len(rows),'supplied Sinhala lyric lines prepared')
