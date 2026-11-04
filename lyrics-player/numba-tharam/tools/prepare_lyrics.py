from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
hook='''නුඹ තරම් කවුරුද ආදරේ|numba tharam kawuruda aadare
පැතුවාට අදහන්න බෑ වගේ|paethuwaata adahanna bae wage
ඇරඹුමත් නුඹමයි ජීවිතේ|aerambumath numbamayi jeewithe
නුඹ ඉන්න මා ලගින්|numba inna maa langin
සුසුමන් සරේ මගේ හුස්මවී|susuman sare mage husmawee
මගේ ජීවිතේ අලුත් පිටුවක් පෙරළුනා|mage jeewithe aluth pituwak peralunaa
මේ ආදරේ අරුත නුඹ බව වැටහුනා|me aadare arutha numba bawa waetahunaa
මා හා බැදී ආදරේ තවරනා|maa haa baendee aadare thawaranaa
ආදරේ මා සනසනා|aadare maa sanasanaa'''
verse='''ආවාට මා හා සරා|aawaata maa haa saraa
අතැරෙන්න නම් දෙන්න එපා|athaerenna nam denna epaa
හිනැහෙන්න ඕනේ නුඹේ සිනා|hinaehenna one numbe sinaa
හිත හොයන දේ ඒ නිසා|hitha hoyana de e nisaa
මේ භවයේ මාගේ වෙලා|me bhawaye maage welaa
මතු සසරේ ඉමු ලංවෙලා|mathu sasare imu lanwelaa'''
a=[]
for section,data in [('hook1',hook),('verse',verse),('hook2',hook)]:
 for j,line in enumerate(data.splitlines()):
  text,phon=line.split('|');assert len(text.split())==len(phon.split()),text
  a.append(dict(id=len(a),section=section,section_line=j,language='si',text=text,alignment_text=phon))
(R/'lyrics.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));(R/'lyrics_unicode.txt').write_text('\n'.join(x['text'] for x in a)+'\n');print(len(a),'lines')
