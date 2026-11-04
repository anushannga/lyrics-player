from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
verse='''අකාලෙට පිපෙනා රෑ මනමාලි වගේ|akaaleta pipenaa rae manamaali wage
ඔබ ලග සිටියා|oba langa sitiyaa
කියන්නට කතා ගොඩක් මගේ හිතේ තියන්|kiyannata kathaa godak mage hithe thiyan
මම දිනගෙව්වා|mama dinagewwaa
ඔබ එය නොදනී වගේ නම්|oba eya nodanee wage nam
වෙන්වී යන්නේ මාගෙන්|wenwee yanne maagen
යලි නාවටත් කාරි නෑ කියා සිතෙනවා|yali naawatath kaari nae kiyaa sithenawaa
තව බෑ දරාගන්න කාලෙ මගෙ ගෙවේනවා|thawa bae daraaganna kaale mage gewenawaa'''
bridge='''නුබ නොමැති අඩුව මං තව කෙනෙක් ගෙන් දැන්|nuba nomaethi aduwa man thawa kenek gen daen
පියවන්නේ කෙසේද පවසන්|piyawanne keseda pawasan
කියා ගන්න බැරි තරමට මගේ හිත රිදවන්|kiyaa ganna baeri tharamata mage hitha ridawan
මම ඉන්නේ කෙසේද විමසන්|mama inne keseda wimasan
තේරුමක් නැතැයි වැටහුනා|therumak naethayi waetahunaa
වරද මා ලගයි දන්නවා|warada maa langayi dannawaa
සොයමි තවම කවුරුදෝ මා කියා|soyami thawama kawurudo maa kiyaa
සතුට නුබ ලගින් සෙවු නිසා|sathuta nuba langin sewu nisaa
සිටි නමුත් මටත් වැරදුනා|siti namuth matath waeradunaa
අතරමංව මං මාව සොයනවා|atharamanwa man maawa soyanawaa
නුබ තවම ඉන්නවා වගෙ දැනෙනවා|nuba thawama innawaa wage daenenawaa'''
outro='''ඔබ එය නොදනී වගේනම් වෙන්වී යන්නේ මාගෙන්|oba eya nodanee wagenam wenwee yanne maagen
යලි නාවටත් කාරි නෑ කියා සිතෙනවා|yali naawatath kaari nae kiyaa sithenawaa
තව බෑ දරාගන්න කාලෙ මගෙ ගෙවේනවා|thawa bae daraaganna kaale mage gewenawaa
මං තාම නුඹ ගාව ආලකම් සොයනවා|man thaama numba gaawa aalakam soyanawaa
නුඹ නොඑන බව දැනම හීන පොත ලියනවා|numba noena bawa daenama heena potha liyanawaa'''
rows=[]
for section,text in [('verse1',verse),('bridge',bridge),('outro',outro)]:
 for j,line in enumerate(text.splitlines()):
  lyric,phon=line.split('|');assert len(lyric.split())==len(phon.split()),lyric
  rows.append(dict(id=len(rows),section=section,section_line=j,language='si',text=lyric,alignment_text=phon))
(R/'lyrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(R/'lyrics_unicode.txt').write_text('\n'.join(v['text'] for v in rows)+'\n');print(len(rows),'lines',sum(len(v['text'].split()) for v in rows),'words')
