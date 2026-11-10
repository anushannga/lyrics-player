from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
hook='''කොටන පොලන තැන පොල් අඹරන තැන|kotana polana thaena pol ambarana thaena
කොස් වතු කන්දේ අලවතු කන්දේ නෑනාලා|kos wathu kande alawathu kande naenaalaa
ඕප හොයන තැන කැකිරි පලන තැන|opa hoyana thaena kaekiri palana thaena
පාර තොටේ මඟ බලන බලන තැන නෑනාලා|paara thote maga balana balana thaena naenaalaa'''
v1='''මූනට මල් හතයි කියාගෙන|muunata mal hathayi kiyaagena
ඊට යටින් කටු හුඟක් තියාගෙන|eeta yatin katu hungak thiyaagena
මගෙ නංගි වගේ කියලා බදාගෙන|mage nangi wage kiyalaa badaagena
අනෙක් අතට නැට්ටිච්චි කියාගෙන|anek athata naettichchi kiyaagena'''
p1='''නෑනා නෑනා අපෙ ගිනි ගෙඩි නෑනා|naenaa naenaa ape gini gedi naenaa
නෑනා නෑනා අපෙ ගිනිදෙන නෑනා|naenaa naenaa ape ginidena naenaa'''
v2='''මාලය අතගා බරත් අසාගෙන|maalaya athagaa barath asaagena
සාරිය අතගා ගණන් අසාගෙන|saariya athagaa ganan asaagena
අනේ නංගියේ හැඩයි කියාගෙන|ane nangiye haedayi kiyaagena
බොරු සෝබන ඕවනම් ෆේක්|boru sobana owanam fake'''
p2='''නෑනා නෑනා අපේ ජෙලස් නෑනා|naenaa naenaa ape jelas naenaa
නෑනා නෑනා හිත හොද නැති නෑනා|naenaa naenaa hitha honda naethi naenaa'''
v3='''හොද වැඩකට අත ගහන සැරේටම|honda waedakata atha gahana saeraetama
වස්කට ඇරගෙන පේන බලාඑන|waskata aeragena penaa balaaena
හරියන්නෑ බං ඕවා කියාගෙන|hariyan nae ban owaa kiyaagena
වැරදෙද්දි මං කිව්වා කියා එන|waeradeddi man kiwwaa kiyaa ena'''.replace('hariyan nae','hariyannae')
p3='''නෑනා නෑනා කට හොද නැති නෑනා|naenaa naenaa kata honda naethi naenaa
නෑනා නෑනා කට වහ ඇති නෑනා|naenaa naenaa kata waha aethi naenaa'''
a=[]
for section,data in [('hook1',hook),('verse1',v1),('post1',p1),('verse2',v2),('post2',p2),('verse3',v3),('post3',p3),('hook2',hook)]:
 for j,line in enumerate(data.splitlines()):
  text,phon=line.split('|');assert len(text.split())==len(phon.split()),text
  a.append(dict(id=len(a),section=section,section_line=j,language='si',text=text,alignment_text=phon))
(R/'lyrics.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));(R/'lyrics_unicode.txt').write_text('\n'.join(x['text'] for x in a)+'\n');print(len(a),'lines')
