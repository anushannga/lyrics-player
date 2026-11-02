from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
verse='''මනමල් හිනාවේ මුහුණේ|manamal hinaawe muhune
උරුමෙන් ගෙනා|urumen genaa
පෙති පීදේ මලක් වී මෙදා|pethi peede malak wee medaa
කැටයම් වුණානේ හර්දේ|kaetayam wunaane harde
නමකින් මනා|namakin manaa
සුභ හීනේ හඳක් පායලා|subha heene handak paayalaa'''
pre='''නෑරාම දෑතේ මෙතෙකින් එහා|naeraama daethe methekin ehaa
හැමදේදී ළඟින් ඉන්නවා|haemadedi langin innawaa'''
hook='''සඳත් මාගේ නුඹ|sandath maage numba
ඉරත් මාගේ නුඹ|irath maage numba
ඉතින් මා නුඹව බැන්දා|ithin maa numbawa baendaa
අදත් මාගේ නුඹ|adath maage numba
හෙටත් මාගේ නුඹ|hetath maage numba
වඩම්මාන යම් කැන්දා|wadammaana yam kaendaa'''
bridge='''මගෙ අභියස ලෝකයක් තියා|mage abhiyasa lokayak thiyaa
වටිනම දෙය තෝරගන් කියා|watinama deya thoragan kiyaa
කියුවොතින් එකපාරින් නුඹ වෙත එනවා|kiyuwothin ekapaarin numba wetha enawaa
මගෙ හදවත මාලයක් තනා|mage hadawatha maalayak thanaa
නුඹෙ හදවතෙහි ළඟින් තියා|numbe hadawathehi langin thiyaa
හැමදාටම පලඳන්නෙමි මා|haemadaatama palandannemi maa'''
rows=[]
for section,text in [('verse1',verse),('pre1',pre),('hook1',hook),('hook2',hook),('bridge',bridge),('pre2',pre),('hook3',hook),('hook4',hook),('hook5',hook)]:
 for j,line in enumerate(text.splitlines()):
  lyric,phon=line.split('|');assert len(lyric.split())==len(phon.split()),lyric
  rows.append(dict(id=len(rows),section=section,section_line=j,language='si',text=lyric,alignment_text=phon))
(R/'lyrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(R/'lyrics_unicode.txt').write_text('\n'.join(v['text'] for v in rows)+'\n');print(len(rows),'lines')
