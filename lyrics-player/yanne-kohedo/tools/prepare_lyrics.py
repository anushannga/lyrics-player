from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]
v1='''අහසේ තරුසේ දිලෙනා මිනිසා ජීවිතේ|ahase tharuse dilenaa minisaa jeewithe
පොලොවේ වැලි සේ හෙලනා අවසන් සුසුමේ|polowe waeli se helanaa awasan susume
සයුරේ රලසේ නැගෙනා බිදෙනා මේ හිතේ|sayure ralase naegenaa binden aa me hithe
ප්‍රාර්ථනා පොදිබැඳන් සමුගනී මිනිසා ජීවිතෙන්|praarthanaa podibaendan samuganee minisaa jeewithen'''.replace('binden aa','bindenaa')
hook='''වේදනා අහස උසක ලා|wedanaa ahasa usaka laa
යන්නේ කොහෙදෝ හීන සොයලා|yanne kohedo heena soyalaa
තාරුකා සොයාන පියඹලා|thaarukaa soyaana piyambalaa
යන්නේ කොහෙදෝ|yanne kohedo
යන්නේ කොහෙදෝ|yanne kohedo
යන්නේ කොහෙදෝ|yanne kohedo'''
v2='''සිතුදේ පැතුදේ සොයනා සිංහාසනයේ|sithude paethude soyanaa sinhaasanaye
සුවිසල් නගරේ සෙව්වාදෝ සැනසුම් මිතුරේ|suwisal nagare sewwaado saenasum mithure
සිහිනයෙන් අවදි වී එනතුරා යනෙනා භවයේ|sihinayen awadi wee enathuraa yanenaa bhawaye
කළ කී සෑමදේ දිගහැරේ අවසන් මොහොතේ|kala kee saemade digahaere awasan mohothe'''
a=[]
for section,data in [('verse1',v1),('hook1',hook),('verse2',v2),('hook2',hook)]:
 for j,line in enumerate(data.splitlines()):
  text,phon=line.split('|');assert len(text.split())==len(phon.split()),text
  a.append(dict(id=len(a),section=section,section_line=j,language='si',text=text,alignment_text=phon))
(r/'lyrics.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));(r/'lyrics_unicode.txt').write_text('\n'.join(v['text'] for v in a)+'\n');print(len(a),'supplied lines')
