from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
intro='''සන්සුන් පවන් සුවඳින් හමාවී ඈ වරලේ ගැටෙනා|sansun pawan suwandin hamaawee ae warale gaetenaa
නිල්වන් සිහිල් නෙතගින් බලාවී ඈ මා සිතේ ඇඳෙනා|nilwan sihil nethagin balaawee ae maa sithe aenden aa'''.replace('aenden aa','aenden aa')
intro=intro.replace('aenden aa','aenden aa')
hook='''මේ දෙව් දූ සුරලෝකෙන් ආවාදෝ|me dew du suraloken aawaado
තරු අතරින් ආවාදෝ|tharu atharin aawaado
රෑ සිහිනෙන් පේනා නුඹ කාගෙදෝ? මාගේ දෝ|rae sihinen penaa numba kaagedo maage do
නුඹ කාගේදෝ|numba kaagedo
නුඹ මාගේදෝ|numba maagedo
නුඹ කාගේදෝ|numba kaagedo'''
post='''කෝලම් පාවී දෑසින් ඈගේ|kolam paawee daesin aege
මායම් කලා සිත් මාගේ|maayam kalaa sith maage
මායාවියක් දෝ ඈ නෙත් යාවෙනා|maayaawiyak do ae neth yaawenaa'''
bridge='''දකින දකින සිහිනෙදි මට නුඹවම මැවුනා|dakina dakina sihinedi mata numbawama maewunaa
දකින දකින හැම සිහිනෙම|dakina dakina haema sihinema
ගැයෙන වැයෙන තිස්සෙම ගී කවි නුඹට ලියවුනා|gaeyena waeyena thissema gee kawi numbata liyawunaa
නුඹ හින්දා මේ පෙම් කුමරා|numba hindaa me pem kumaraa
නටාවී රඟ මඩලේ පෙම් තනු වයලා|nataawee ranga madale pem thanu wayalaa
හද මැදුරේ මේ දොර ඇරලා|hada maedure me dora aeralaa
තියාවී මගෙ කුමරී නුඹටම කියලා|thiyaawee mage kumaree numbatama kiyalaa'''
# One phonetic token per displayed word.
intro=intro.replace('aenden aa','aenden aa')
rows=[]
for section,text in [('intro',intro),('hook1',hook),('post1',post),('post1_repeat',post),('bridge',bridge),('hook2',hook),('post2',post),('post2_repeat',post)]:
 for j,line in enumerate(text.splitlines()):
  lyric,phon=line.split('|')
  if len(lyric.split())!=len(phon.split()):phon=phon.replace('aenden aa','aenden aa'.replace(' ',''))
  assert len(lyric.split())==len(phon.split()),lyric
  rows.append(dict(id=len(rows),section=section,section_line=j,language='si',text=lyric,alignment_text=phon))
(R/'lyrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(R/'lyrics_unicode.txt').write_text('\n'.join(v['text'] for v in rows)+'\n');print(len(rows),'lines')
