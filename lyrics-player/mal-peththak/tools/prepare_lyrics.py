import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
chorus='''මල් පෙත්තක් සේ සුසිනිඳු සිත
මගෙන් නුඹ කොහින්දෝ හොරකම් කරා
තව රිදෙන්න නෑ ඉඩක්
මගේ හදවතේ
මට දුකද සතුට වේ
කවුළුවෙන් එපිට මහා වර්ෂා වැටෙනවා
ඔබ තිළිණ දුන් රෝස පඳුරේ
පිපුණු මලේ පෙති කඩා හැලෙනවා
මට පේනවා...'''.splitlines()
phonetic='''mal peththak se susinidu sitha
magen numba kohindo horakam kara
thawa ridenna ne idak
mage hadawathe
mata dukada sathuta we
kawuluwen epita maha warsha watenawa
oba thilina dun rosa pandure
pipunu male pethi kada halenawa
mata penawa'''.splitlines()
rap1='''Hey, my name is Shane
My girlfriend's name is Rose
She has a friend called Jane
Who's got a boyfriend named John
Nigga, this is really damn
John makes love to girls
Plus sends three-page letters
Every day to Jane
Hey, what's wrong with that nigga?
Just asked Rose
Nothing wrong with him
She said, so like you
You don't love me, Shane
Of course I love you, Rose
I offered the warmest kiss
I could ever give to prove
She groaned and pulled her bag
Over the head
Ooh, she didn't want to converse
With me anymore
You don't love me enough, she said
How much you want?
I said, I'm in love with you
I said, I wanted to explain
But it was in vain
You've got to write me, Shane
Write me one page, man
Damn, you don't even phone
Like John does to Jane
I don't believe you, girl
I send two letters a week
There may be a problem
With postmen or something
Don't lie to me, Shane
I think that someone is you
Your love is a pain
No more I see you'''.splitlines()
rap2='''Dear Rose, babe
I send two letters a week
If you miss them, it can't be
There's a problem with the...
I tried to write you more than
Babe, it's not easy
Been in hard work
Please don't be so crazy
Make you understand, babe
Never hate me back
I'm your candy
You're acting like a lady, man
You may know the girls
Are trying to get involved with you
They're jealous
Three sixty-five, I'm thinking of you
Even things I like
I'm doing so, pretty girl
You just screw me down
For no reason at all
In the cold morn
I feel alone
I walk along the Sixth Lane
Insane, you don't phone
I'm in pain
You never know
What Jane's nigga do
If Jane knows
She might call it off too
Look, I'm really glad
Being steady with you
I don't wanna miss you
I wanna kiss you
P.S. we need each other
When you read this letter
Please treat me better
See you later'''.splitlines()
dialogue=['Hello?','Hello?','Hello?','What the hell?',"Who's calling me?",'A nuisance call!']
sections=[('chorus1','si',chorus),('rap1','en',rap1),('chorus2','si',chorus),('rap2','en',rap2),('chorus3','si',chorus),('dialogue','en',dialogue),('chorus4','si',chorus),('chorus5','si',chorus),('chorus6','si',chorus)]
rows=[]
for section,lang,lines in sections:
 for j,text in enumerate(lines):
  rows.append({'id':len(rows),'section':section,'section_line':j,'language':lang,'text':text,'alignment_text':phonetic[j] if lang=='si' else text})
(R/'lyrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(R/'lyrics_unicode.txt').write_text('\n'.join(v['text'] for v in rows)+'\n')
rules=json.loads((R/'assets/isi-rules.json').read_text())
for row in rows:
 text=row['text']
 if row['language']=='si':
  for a,b in rules:text=text.replace(a,b)
  assert not any('\u0d80'<=c<='\u0dff' for c in text),text
 row['display_text']=text
(R/'lyrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(len(rows),'clean lyric lines; section titles and sound-effect comments excluded')
