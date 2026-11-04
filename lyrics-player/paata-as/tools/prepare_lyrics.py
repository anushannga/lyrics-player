from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
intro='''ඈත පේන තාරුකා වල පාට තේරුවා මන්|aetha pena thaarukaa wala paata theruwaa man
නුඹනම් ඒ දේවදුන්න සඳ දෙව්ලිය අහසෙ මැව්|numbanam e dewadunna sanda dewliya ahase maew
මායාවකි චන්ද්‍ර කොපුළ වළාකුලට හාදු දුන්|maayaawaki chandra kopula walaakulata haadu dun
හිත දවනා නාරිලතා මල නුඹයි හීනෙ සැඟව උන්|hitha dawanaa naarilathaa mala numbayi heene saengawa un'''
hook='''මට කියාගන්න බැරි ආදරේ|mata kiyaaganna baeri aadare
මම ලියාදුන්න එක සීරුවේ|mama liyaadunna eka seeruwe
හද හඬා ගලන පෙම් මාරුතේ|hada handaa galana pem maaruthe
තියේ හිත් මායිමේ පුරා|thiye hith maayime puraa
අඩ සඳට මම තනුව මිමිණුවේ|ada sandata mama thanuwa miminuwe
මල් සුවඳ නුඹ තමයි තේරුවේ|mal suwanda numba thamayi theruwe
අඩමාන පෙම් රාව වෑහුනේ|adamaana pem raawa waehune
දෙව්ලියක් නොවෙදෝ ඔයා|dewliyak nowedo oyaa'''
post='''මරතෝණ්ඩි ඇඳි නුඹෙ දෑත මට කීව|marathondi aendi numbe daetha mata keewa
රහස කාටත් කියන්නට බැරිද|rahasa kaatath kiyannata baerida
පාට ඇස් ලඟ තාම මන් තනිවෙලා|paata aes langa thaama man thaniwelaa
සුදු පාට තවරපු සේද වළාවක|sudu paata thawarapu seda walaawaka
ආදරේ මම ලියා එවන්නද|aadare mama liyaa ewannada
තියාගන්න එය ආදරේ තවරලා|thiyaaganna eya aadare thawaralaa'''
bridge='''දම් පාට ඇස් අතරේ කෝමළ රේඛා තිබුනේ|dam paata aes athare komala rekhaa thibune
මේ හිතට ආශා මවා|me hithata aashaa mawaa
තව ඉන්න බෑ අඳුරේ ලං වෙන්න මට සොඳුරේ|thawa inna bae andure lan wenna mata sondure
හිත ආදරෙන් මත්වෙලා|hitha aadaren mathwelaa'''
a=[]
for section,data in [('intro',intro),('hook1',hook),('post1',post),('post1_repeat',post),('bridge',bridge),('hook2',hook),('post2',post),('post2_repeat',post)]:
 for j,line in enumerate(data.splitlines()):
  text,phon=line.split('|');assert len(text.split())==len(phon.split()),text
  a.append(dict(id=len(a),section=section,section_line=j,language='si',text=text,alignment_text=phon))
(R/'lyrics.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));(R/'lyrics_unicode.txt').write_text('\n'.join(x['text'] for x in a)+'\n');print(len(a),'lines')
