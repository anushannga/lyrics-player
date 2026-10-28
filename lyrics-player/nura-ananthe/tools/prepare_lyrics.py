from pathlib import Path
import json,unicodedata
R=Path(__file__).resolve().parents[1]
v1='''ආදරෙන් වෙලා ඔබ රාගෙක මා හට පෙම් කරනා|aadaren welaa oba raageka maa hata pem karanaa
මා ලයේ රගා නෙතගේ නුබෙ ආලය මා සතපා|maa laye ragaa nethage nube aalaya maa sathapaa'''
pre='''සිපගන්නට ඔය රුව මා ලග|sipagannata oya ruwa maa langa
නැලවෙන්නට ඔය වත මා ලග|naelawennata oya watha maa langa
ඇගෙ ඉග මට බෑ ඉවසන්නට|aege iga mata bae iwasannata
මේ රෑ පුරා|me rae puraa'''
hook='''ඔහේ ගියාම තේරුනා|ohe giyaama therunaa
නුරා අනන්තෙ ඈ වුනා|nuraa ananthe ae wunaa
අගේ හිනා ඇගේ කතා|age hinaa aege kathaa
මගේ වෙලා|mage welaa'''
post='''ඔබ මා ලගින් වෙලා හඩන්නෙපා|oba maa langin welaa handannepaa
ඔබ මා ලගින් වෙලා දුවන්නෙපා|oba maa langin welaa duwannepaa'''
v2='''මා ලගින් වෙලා සයනේ වැතිරී ඔබ පෙම් කෙරුවා|maa langin welaa sayane waethiree oba pem keruwaa
ආදරේ කලා තනිවෙන්නට නෑ හිත බෑ රවටා|aadare kalaa thaniwennata nae hitha bae rawataa'''
rows=[]
for section,text in [('verse1',v1),('pre1',pre),('hook1',hook),('post1',post),('verse2',v2),('pre2',pre),('hook2',hook),('post2',post),('post3',post)]:
 for j,line in enumerate(text.splitlines()):
  lyric,phon=line.split('|');lyric=unicodedata.normalize('NFC',lyric);assert len(lyric.split())==len(phon.split()),lyric
  rows.append(dict(id=len(rows),section=section,section_line=j,language='si',text=lyric,alignment_text=phon))
(R/'lyrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(R/'lyrics_unicode.txt').write_text('\n'.join(v['text'] for v in rows)+'\n');print(len(rows),'lines',sum(len(v['text'].split()) for v in rows),'words')
