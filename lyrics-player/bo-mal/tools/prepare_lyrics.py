from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
verse='''මෝසම් මල් පෙති යායේ|mosam mal pethi yaaye
නුබ හා ගෙවුනූ කාලේ|nuba haa gewunuu kaale
නුබ හා ගෙවුනූ කාලේ|nuba haa gewunuu kaale
තොල් පෙති අස්සෙන රිංගන්|thol pethi assena ringan
නුබ හා ගෙවුනූ යාමේ|nuba haa gewunuu yaame
නුබ හා ගෙවුනූ යාමේ|nuba haa gewunuu yaame'''
pre='''මානෙල් මල් විරසක වීලා දැන්|maanel mal wirasaka weelaa daen
රෑ නැවතීලා දැන්|rae naewatheelaa daen
නුබ හා වී|nuba haa wee
යායේ පිපි මල් ඈතට වී|yaaye pipi mal aethata wee
නුබ නොදොඩා ඇයි|nuba nododaa aeyi
තරහා වී|tharahaa wee'''
hook='''බෝ මල් මා රෑ වෙනා|bo mal maa rae wenaa
වාරේ වැහි පා වෙනා|waare waehi paa wenaa
ආලේ ගං දැන් හුඟක්|aale gang daen hungak
මෝසම් කවි ගායනා|mosam kawi gaayanaa'''
bridge='''අරලිය මල් පාවී ඇවිදින්|araliya mal paawee aewidin
නුබ ළඟ හිඳ හොරැහින් බලනා|nuba langa hinda horaehin balanaa
රූ ධාරී... මායාවී...|ru dhaaree maayaawee
පැන් ගෙනැවිත් වෘන්දා වනයෙන්|paen genaewith wrundaa wanayen
මා ලඟ හිද ඔච්චම් කරනා|maa langa hida ochcham karanaa
වර්ණාවී.. මායාවී...|warnaawi maayaawee'''
a=[]
for section,data in [('verse1',verse),('pre1',pre),('hook1',hook),('hook1_repeat',hook),('bridge',bridge),('pre2',pre),('hook2',hook),('hook2_repeat',hook),('verse2',verse)]:
 for j,line in enumerate(data.splitlines()):
  text,phon=line.split('|');assert len(text.split())==len(phon.split()),text
  a.append(dict(id=len(a),section=section,section_line=j,language='si',text=text,alignment_text=phon))
(R/'lyrics.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));(R/'lyrics_unicode.txt').write_text('\n'.join(x['text'] for x in a)+'\n');print(len(a),'lines')
