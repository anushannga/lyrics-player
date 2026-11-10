from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
hook='''වැහි පාවී දෝ... කෝලම් නා මල් පිපිලා|waehi paawee do kolam naa mal pipilaa
ගං යා වේ දෝ... රෑ පිනි බාවී කියලා|gang yaa we do rae pini baawee kiyalaa
මෙරු ආපිට පලයන් ඉල් වැහි මාසේ නැතුවා|meru aapita palayan il waehi maase naethuwaa
වැහි කෝලම නටපන් මේ වැහි මාසේ...|waehi kolama natapan me waehi maase'''
v1='''නා අතු වැටිලා දැන් මයෙ ළඟ|naa athu waetilaa daen maye langa
දන්තුර එන රණසෙන් ඇහුණා ද|danthura ena ranasen aehunaa da
උඹේ පණ අරගෙන පලයන්|umbe pana aragena palayan
දළදා වැහි මල් නොතෙමා...|daladaa waehi mal nothemaa'''
v2='''ගං ඉවුරක මල් පූදිනකොට|gang iwuraka mal puudinakota
පිපි මල් ඇහුවා බිඟු නරක ද|pipi mal aehuwaa bingu naraka da
උඹේ පණ අරගෙන පලයන්|umbe pana aragena palayan
දළදා වැහි මල් නොතෙමා...|daladaa waehi mal nothemaa'''
pre='''බලන් කුසුමාසන දේවී|balan kusumaasana devi
වඩින් ඔය නාමල් පාරේ|wadin oya naamal paare
රොනුත් නැති කෙකටියා මල් දැන්|ronuth naethi kekatiyaa mal daen
හොරෙන් බැලුවා...|horen baeluwaa'''
bridge='''වැහි පූදින වාරෙක මන් නුඹට ම පේ වී|waehi puudina waareka man numbata ma pe wee
ඉල් පොද ගණිනා තරමක් හීතල දේ වී|il poda ganinaa tharamak heethala de wee
නුඹ දකින දකින දින ගෙවෙන ගෙවෙන මල් පරව ගියා නටුවෙන්|numba dakina dakina dina gewena gewena mal parawa giyaa natuwen
නොදැන ඉකි බිඳින බිඳින හිත දවන දවන පෙති තුරුලු වෙලා...|nodaena iki bindina bindina hitha dawana dawana pethi thurulu welaa'''
a=[]
for section,data in [('hook1',hook),('verse1',v1),('verse2',v2),('pre1',pre),('pre1_repeat',pre),('bridge',bridge),('verse1_repeat',v1),('verse2_repeat',v2),('pre2',pre),('pre2_repeat',pre),('hook2',hook)]:
 for j,line in enumerate(data.splitlines()):
  text,phon=line.split('|');assert len(text.split())==len(phon.split()),text
  a.append(dict(id=len(a),section=section,section_line=j,language='si',text=text,alignment_text=phon))
(R/'lyrics.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));(R/'lyrics_unicode.txt').write_text('\n'.join(x['text'] for x in a)+'\n');print(len(a),'lines')
