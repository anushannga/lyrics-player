from pathlib import Path
import json,unicodedata
R=Path(__file__).resolve().parents[1]
intro='''බෝවිටියා මල් සුලගෙ වැනෙනකොට|bowitiya mal sulage waenenakota
කෙවිට තියාපන් අහකින්|kewita thiyaapan ahakin
කබරගොයින් දැක නියර උඩින් පැන|kabaragoyin daeka niyara udin paena
දුවලා වරේං මගෙ මලේ…|duwala waren mage male'''
govinda='''ගෝවින්දා හේ කදු මැද්දෙන්|govindaa he kadu maedden
වහීන්නත් වගේ|waheennath wage
ගෝවින්දා ඒ කදු මැද්දෙන්|govindaa e kadu maedden
වහීන්නත් වගේ|waheennath wage'''
hook='''ගගුලැල්ලේ පවනැල්ලේ හසරැල්ලේ පියඹන්නේ|gangulaelle pawanaelle hasaraelle piyambanne
අකුරක් ඒ නොදනිම්…|akurak e nodanim
ගගුලැල්ලේ පවනැල්ලේ හසරැල්ලේ පියඹන්නේ|gangulaelle pawanaelle hasaraelle piyambanne
අකුරක් ඒ නොදනිම්…|akurak e nodanim'''
rap='''පැන්සල දෙකට කඩාගෙන|paensala dekata kadaagena
මදටිය ඇට එකතු කරාගෙන|madatiya aeta ekathu karaagena
පෑන පොතට පිරියක් නෑ මට|paena pothata piriyak nae mata
වාගේ ඒවා නෑ මේ හරිත කලාවට|waage ewa nae me haritha kalaawata
මී අඹ ගස් අත්තෙ පැහිල හොද|mee amba gas atthe paehila honda
මාල ගිරව් වට ගනන් හදනවද|maala giraw wata ganan hadanawada
චක්කරේට වඩා දන්නව මං|chakkareta wadaa dannawa man
මන්තරෙ මේ කදු කතා කරන හඩ|manthare me kadu kathaa karana handa
නැව්ගල කන්දෙන් ඒ එහාට|naewgala kanden e ehaata
මල් පිපිලා ඇති මලින බරව|mal pipilaa aethi malina barawa
යන්න ඕනෙ දවසක බලං ඉන්න|yanna one dawasaka balan inna
හත් කදු පිසගෙන ඉර වඩිනා රග|hath kadu pisagena ira wadinaa ranga
අමර ඉතිං මං එන්නෑ හෙට|amara ithin man ennae heta
වේවැල කෙවිටක් වෙන් නෑ තව|wewaela kewitak wen nae thawa
බාන එක්ක යාය පුරාවට|baana ekka yaaya puraawata
ගොපලු රජා වෙන්නම් මේ යායට|gopalu rajaa wennam me yaayata'''
rows=[]
for section,data in [('intro',intro),('govinda',govinda),('hook',hook),('rap',rap)]:
 for j,line in enumerate(data.splitlines()):
  text,phon=line.split('|');text=unicodedata.normalize('NFC',text)
  assert len(text.split())==len(phon.split()),text
  rows.append(dict(id=len(rows),section=section,section_line=j,language='si',text=text,alignment_text=phon))
for oldsection,newsection in [('govinda','govinda2'),('hook','hook2'),('intro','intro2'),('intro','intro3')]:
 for item in [x for x in rows if x['section']==oldsection][:2 if oldsection=='govinda' else 999]:
  rows.append(dict(item,id=len(rows),section=newsection))
(R/'lyrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(R/'lyrics_unicode.txt').write_text('\n'.join(v['text'] for v in rows)+'\n');print(len(rows),'lines',sum(len(v['text'].split()) for v in rows),'words')
