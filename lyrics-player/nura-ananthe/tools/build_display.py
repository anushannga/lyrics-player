"""Render complete words and three timed, persistent sustain dots."""
import hashlib,json
import copy
import regex
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

R=Path(__file__).resolve().parents[1]
(R/'previews').mkdir(exist_ok=True)
lyrics=json.loads((R/'lyrics.json').read_text())
aligned={v['id']:v for v in json.loads((R/'alignment.json').read_text())}
selected=json.loads((R/'sustain_selection.json').read_text())
rules=json.loads((R/'assets/isi-rules.json').read_text())
S=4
fonts={'si':ImageFont.truetype(str(R/'assets/isigurul_0.ttf'),24*S)}
frames=[];cache={};pages=[];cues=[];thumbs=[];sustains=[]
def bitmap(im):
    key=im.tobytes()
    if key not in cache:
        raw=key
        if raw not in frames:frames.append(raw)
        cache[key]=frames.index(raw)
    return cache[key]
def convert(w,language):
    if language=='si':
        for a,b in rules:w=w.replace(a,b)
    return w
def paint(rows,visible,font,dot_counts):
    im=Image.new('L',(128*S,64*S));draw=ImageDraw.Draw(im)
    height=sum(row['height'] for row in rows)+3*S*(len(rows)-1)
    assert height<=60*S
    y=(64*S-height)//2
    dots=[]
    for row in rows:
        x=(128*S-row['width'])//2
        for j,w,b,width in row['words']:
            if j<=visible:
                draw.text((x-b[0],y-row['top']),w,font=font,fill=255,stroke_width=1)
                if dot_counts.get(j):
                    # One typographic baseline per row; descenders and vowel
                    # marks must not push the ellipsis down for individual words.
                    baseline=(y-row['top']+font.getmetrics()[0])//S
                    dots.append(((x+b[2]-b[0])//S+1,baseline-1,dot_counts[j]))
            x+=width+3*S
        y+=row['height']+3*S
    im=im.resize((128,64),Image.Resampling.LANCZOS).point(lambda v:255 if v>=155 else 0).convert('1')
    draw=ImageDraw.Draw(im)
    for x,y,count in dots:
        for k in range(count):draw.ellipse((x+k*3,y,x+k*3+1,y+1),fill=1)
    return im
units=[[lyric] for lyric in lyrics]
for unit in units:
    lyric=unit[0];language=lyric['language'];font=fonts[language]
    source=[];timed=[];origins=[];row_breaks=set()
    for item in unit:
        if source:row_breaks.add(len(source))
        offset=item.get('_word_offset',0);count=len(item['text'].split())
        source.extend(item['text'].split());timed.extend(aligned[item['id']]['words'][offset:offset+count])
        origins.extend((item['id'],offset+j) for j in range(count))
    line={'words':timed}
    words=[convert(w.replace('.','').replace('…',''),language) for w in source]
    dotted=set()
    short_function_words={'මේ','මා','මට','හා','ඈ','නුඹ','නෑ','ඒ'}
    for j,w in enumerate(source):
        duration=line['words'][j]['end']-line['words'][j]['start']
        grapheme_count=len(regex.findall(r'\X',w))
        # Punctuation supplied with lyrics is not evidence of a held vocal.
        # Use the reviewed selection derived from the isolated vocal signal.
        if [origins[j][0],origins[j][1]] in selected['words']:
            dotted.add(j)
            sustains.append({'line':origins[j][0],'word':origins[j][1],'text':w,'duration':round(duration,3),'basis':'isolated vocal duration; sustained content word'})
    assert len(words)==len(line['words']),(lyric['id'],'word count')
    rows=[];row=[];total=0
    for j,w in enumerate(words):
        b=font.getbbox(w,stroke_width=1);width=b[2]-b[0]+(10*S if j in dotted else 0)
        assert width<=124*S,(w,width,lyric['text'])
        if row and (j in row_breaks or total+3*S+width>124*S):rows.append(row);row=[];total=0
        row.append((j,w,b,width));total+=width+(3*S if len(row)>1 else 0)
    if row:rows.append(row)
    for start in range(0,len(rows),2):
        group=[]
        for row in rows[start:start+2]:
            top=min(v[2][1] for v in row);bottom=max(v[2][3] for v in row)
            group.append({'words':row,'width':sum(v[3] for v in row)+3*S*(len(row)-1),'height':bottom-top,'top':top})
        previous_pixels=bytes(1024)
        dot_counts={}
        for j,w,b,width in sum([v['words'] for v in group],[]):
            im=paint(group,j,font,dot_counts)
            stable=bytes(a|b for a,b in zip(previous_pixels,im.tobytes()))
            im=Image.frombytes('1',(128,64),stable);previous_pixels=stable
            pages.append({'layout':len(thumbs),'line':origins[j][0],'word':origins[j][1],'language':language,'bitmap':bitmap(im)})
            cues.append({'time':line['words'][j]['start'],'page':len(pages)-1,'style':'melodic','kind':'word'})
            if j in dotted:
                onset=line['words'][j]['start'];end=line['words'][j]['end']
                # Spread Mage's dots across its whole held scene, including
                # the pause before the next sung line, without moving onsets.
                if False:
                    following=[v['start'] for v in aligned.values() if v['start']>onset]
                    if following:end=min(following)
                duration=end-onset
                for count in range(1,4):
                    at=round(onset+duration*count/4,4)
                    if at>=end-.04:continue
                    dot_counts[j]=count
                    im=paint(group,j,font,dot_counts)
                    stable=bytes(a|b for a,b in zip(previous_pixels,im.tobytes()))
                    im=Image.frombytes('1',(128,64),stable);previous_pixels=stable
                    pages.append({'layout':len(thumbs),'line':origins[j][0],'word':origins[j][1],'dots':count,'language':language,'bitmap':bitmap(im)})
                    cues.append({'time':at,'page':len(pages)-1,'style':'melodic','kind':'sustain'})
        thumbs.append(im)
# Only actual lyric text is displayed; no titles, instructions or effect notes.
ordered=sorted(aligned.values(),key=lambda v:v['start'])
cues.append({'time':0,'page':-1,'kind':'silence','style':'melodic'})
for prev,nxt in zip(ordered,ordered[1:]):
    if (lyrics[prev['id']]['text'].strip()!='මගේ' and nxt['section']!=prev['section'] and nxt['start']-prev['end']>=1.2):
        cues.append({'time':round(prev['end']+.15,3),'page':-1,'kind':'silence','style':'melodic'})
if ordered[-1]['end']<150.267551:cues.append({'time':round(ordered[-1]['end']+.15,3),'page':-1,'kind':'silence','style':'melodic'})
cues.sort(key=lambda v:v['time'])
assert all(a['time']<b['time'] for a,b in zip(cues,cues[1:])), 'Cue collision'
raw=b''.join(frames);identity=hashlib.sha256((R/'lyrics.json').read_bytes()+raw).hexdigest()[:16]
(R/'frames.bin').write_bytes(raw)
(R/'manifest.json').write_text(json.dumps({'id':identity,'pixel_format':'st7920-horizontal-msb','font':'ISI Gurulugomi','font_size':24,'effect':'word-reveal-with-progressive-sustain-dots','line_count':len(lyrics),'bitmap_count':len(frames),'pages':pages},indent=2))
(R/'sustain_marks.json').write_text(json.dumps({'selection':'Long phrase-final isolated vocals; punctuation alone does not add dots; not listening-confirmed','words':sustains},ensure_ascii=False,indent=2))
mp3=next((Path.home()/'Downloads').glob('Cozzy - Nura Ananthe*mp3'))
(R/'timings.json').write_text(json.dumps({'lyrics_id':identity,'audio_sha256':hashlib.sha256(mp3.read_bytes()).hexdigest(),'duration':150.517551,'listening_confirmed':False,'method':'Known sung/spoken text locally aligned, repeated choruses checked spectrally','cues':cues},indent=2))
sheet=Image.new('RGB',(512*3,280*((len(thumbs)+2)//3)),'#14251c');draw=ImageDraw.Draw(sheet)
for i,im in enumerate(thumbs):
    x=i%3*512;y=i//3*280;draw.text((x+6,y+4),f'Page {i+1}',fill='white')
    colored=Image.new('RGB',(128,64),'#b5ce83');colored.paste('#172814',mask=im)
    sheet.paste(colored.resize((512,256),Image.Resampling.NEAREST),(x,y+24))
sheet.save(R/'previews/all-pages.png')
print(len(lyrics),'lyric lines;',len(thumbs),'page layouts;',len(frames),'unique frames;',len(cues),'cues')
