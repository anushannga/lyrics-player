from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
verse1='''නැවතෙන්නට හිතනා|naewathennata hithanaa
හදවත මත අතපා|hadawatha matha athapaa
තව ඉවසන්නට මා|thawa iwasannata maa
තරවටූ උනා|tharawatuu unaa
නෙතඟින් පිට පනිනා|nethangin pita paninaa
කඳුලැලි කැට පිසලා|kandulaeli kaeta pisalaa
නෙතු පතුලෙම හංගන්නට|nethu pathulema hangannata
වෑයමේ මෙමා|waeyame memaa'''
pre1='''ඔබ හා රැඳෙන්න මොහොතක් පවා|oba haa raendenna mohothak pawaa
යදිනා හදේ විඩා|yadinaa hade widaa
මට බෑ නිවෙන්න ඇතුලින් මෙමා|mata bae niwenna aethulin memaa
ගිනියම්ව ඇවිලිලා|giniyamwa aewililaa'''
hook='''ආයේ මේ වාගේ|aaye me waage
අවසන රිදෙනා ඒ|awasana ridenaa e
ප්‍රේමේ කතා.. තව එපා|preme kathaa thawa epaa
නුබ නොරිදෙන විලසේ මං|nuba noridena wilase man
නුබ ලඟ ඉන්නම්|nuba langa innam
කඳුලැල් හංගලා.. හිනෑහිලා|kandulael hangalaa hinaehilaa'''
verse2='''පිය සටහන් මැකිලා|piya satahan maekilaa
අපි ආ දුර නොතකා|api aa dura nothakaa
මෙතනින් නවතිමු|methanin nawathimu
තව නොහඬා|thawa nohandaa
අවසන් හාදුව සේ|awasan haaduwa se
නලලත තවරා හාදූ මා|nalalatha thawaraa haaduu maa
ආදරෙ දරා|aadare daraa'''
pre2='''නුබ හා රැඳෙන්න මොහොතක් පවා|nuba haa raendenna mohothak pawaa
යදිනා හදේ විඩා|yadinaa hade widaa
ඉවසා දරාන ඉනු කෝම මා|iwasaa daraana inu koma maa
සමුදෙන්නෙ පෙමට මා|samudenne pemata maa'''
rows=[]
for section,text in [('verse1',verse1),('pre1',pre1),('hook1',hook),('verse2',verse2),('pre2',pre2),('hook2',hook.replace('හිනෑහිලා','හිනැහිලා')),('hook3',hook.replace('වාගේ','වාගෙ').replace('හිනෑහිලා','හිනැහිලා'))]:
 for j,line in enumerate(text.splitlines()):
  lyric,phon=line.split('|');assert len(lyric.split())==len(phon.split()),lyric
  rows.append(dict(id=len(rows),section=section,section_line=j,language='si',text=lyric,alignment_text=phon))
(R/'lyrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
(R/'lyrics_unicode.txt').write_text('\n'.join(x['text'] for x in rows)+'\n')
print(len(rows),'lines',sum(len(x['text'].split()) for x in rows),'words')
