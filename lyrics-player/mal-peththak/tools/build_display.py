"""Build mixed Sinhala/English letter-reveal frames for the existing USB LCD."""
import hashlib,json,math
import regex
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops

R=Path(__file__).resolve().parents[1]
lyrics=json.loads((R/'lyrics.json').read_text())
aligned={v['id']:v for v in json.loads((R/'alignment.json').read_text())}
rules=json.loads((R/'assets/isi-rules.json').read_text())
S=4
english_font=next((p for p in [R/'assets/Arial.ttf',Path('/System/Library/Fonts/Supplemental/Arial.ttf'),Path('/Library/Fonts/Arial.ttf')] if p.is_file()),None)
if english_font is None:raise SystemExit('Arial.ttf is needed to rebuild English captions; install it or place a licensed copy in assets/. Playback uses the saved frames and does not need it.')
fonts={'si':ImageFont.truetype(str(R/'assets/isigurul_0.ttf'),24*S),
       'en':ImageFont.truetype(str(english_font),18*S)}
frames=[];cache={};pages=[];cues=[];thumbs=[]
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
def paint(rows,visible,font,dotted,partial=None):
    im=Image.new('L',(128*S,64*S));draw=ImageDraw.Draw(im)
    height=sum(row['height'] for row in rows)+3*S*(len(rows)-1)
    assert height<=60*S
    y=(64*S-height)//2
    dots=[]
    for row in rows:
        x=(128*S-row['width'])//2
        for j,w,b,width in row['words']:
            if j<=visible:
                if j==visible and partial is not None:
                    # Clip the final glyph image at a whole grapheme boundary.
                    # Earlier characters never move or change their ink pattern.
                    layer=Image.new('L',im.size)
                    ImageDraw.Draw(layer).text((x-b[0],y-row['top']),w,font=font,fill=255,stroke_width=1)
                    edge=max(0,min(im.width,x+partial))
                    clipped=Image.new('L',im.size)
                    clipped.paste(layer.crop((0,0,edge,im.height)),(0,0))
                    im=ImageChops.lighter(im,clipped)
                    draw=ImageDraw.Draw(im)
                else:
                    draw.text((x-b[0],y-row['top']),w,font=font,fill=255,stroke_width=1)
                if j in dotted and partial is None:dots.append(((x+b[2]-b[0])//S+2,(y-row['top']+b[3])//S-4))
            x+=width+3*S
        y+=row['height']+3*S
    im=im.resize((128,64),Image.Resampling.LANCZOS).point(lambda v:255 if v>=155 else 0).convert('1')
    draw=ImageDraw.Draw(im)
    for x,y in dots:
        for k in range(3):draw.ellipse((x+k*3,y,x+k*3+1,y+1),fill=1)
    return im
for lyric in lyrics:
    line=aligned[lyric['id']];language=lyric['language'];font=fonts[language]
    source=lyric['text'].split();words=[convert(w.replace('...',''),language) for w in source]
    dotted={j for j,w in enumerate(source) if '...' in w}
    assert len(words)==len(line['words']),(lyric['id'],'word count')
    rows=[];row=[];total=0
    for j,w in enumerate(words):
        b=font.getbbox(w,stroke_width=1);width=b[2]-b[0]+(10*S if j in dotted else 0)
        assert width<=124*S,(w,width,lyric['text'])
        if row and total+3*S+width>124*S:rows.append(row);row=[];total=0
        row.append((j,w,b,width));total+=width+(3*S if len(row)>1 else 0)
    if row:rows.append(row)
    for start in range(0,len(rows),2):
        group=[]
        for row in rows[start:start+2]:
            top=min(v[2][1] for v in row);bottom=max(v[2][3] for v in row)
            group.append({'words':row,'width':sum(v[3] for v in row)+3*S*(len(row)-1),'height':bottom-top,'top':top})
        previous_pixels=bytes(1024)
        for j,w,b,width in sum([v['words'] for v in group],[]):
            units=regex.findall(r'\X',source[j].replace('...',''))
            start_time=line['words'][j]['start'];end_time=line['words'][j]['end']
            if j+1<len(line['words']):end_time=min(end_time,line['words'][j+1]['start'])
            duration=max(.025,end_time-start_time)
            # Respect the measured 50–85ms/frame transport budget. In fast rap,
            # several characters share an update rather than delaying the song.
            steps=min(len(units),max(1,int(duration/.11)+1))
            last_edge=0
            for step in range(1,steps+1):
                count=math.ceil(len(units)*step/steps)
                prefix=convert(''.join(units[:count]),language)
                edge=max(last_edge,font.getbbox(prefix,stroke_width=1)[2]-b[0]);last_edge=edge
                complete=step==steps
                im=paint(group,j,font,dotted,None if complete else edge)
                stable=bytes(a|b for a,b in zip(previous_pixels,im.tobytes()))
                im=Image.frombytes('1',(128,64),stable);previous_pixels=stable
                pages.append({'layout':len(thumbs),'line':lyric['id'],'word':j,'characters_visible':count,'character_count':len(units),'language':language,'bitmap':bitmap(im)})
                cues.append({'time':round(start_time+duration*(step-1)/steps,4),'page':len(pages)-1,'style':'melodic' if language=='si' else 'rap','kind':'letter'})
        thumbs.append(im)
# Only actual lyric text is displayed; no titles, instructions or effect notes.
ordered=sorted(aligned.values(),key=lambda v:v['start'])
cues.append({'time':0,'page':-1,'kind':'silence','style':'melodic'})
for prev,nxt in zip(ordered,ordered[1:]):
    if nxt['start']-prev['end']>=1.2:cues.append({'time':round(prev['end']+.15,3),'page':-1,'kind':'silence','style':'melodic'})
if ordered[-1]['end']<272.1:cues.append({'time':round(ordered[-1]['end']+.15,3),'page':-1,'kind':'silence','style':'melodic'})
cues.sort(key=lambda v:v['time'])
assert all(a['time']<b['time'] for a,b in zip(cues,cues[1:])), 'Cue collision'
raw=b''.join(frames);identity=hashlib.sha256((R/'lyrics.json').read_bytes()+raw).hexdigest()[:16]
(R/'frames.bin').write_bytes(raw)
(R/'manifest.json').write_text(json.dumps({'id':identity,'pixel_format':'st7920-horizontal-msb','font':'ISI Gurulugomi + Arial for English','font_size':{'si':24,'en':18},'effect':'stable-grapheme-typewriter','line_count':len(lyrics),'bitmap_count':len(frames),'pages':pages},indent=2))
mp3=next((Path.home()/'Downloads').glob('Mal Peththak Se Susinidu Sitha*6th Lane*mp3'))
(R/'timings.json').write_text(json.dumps({'lyrics_id':identity,'audio_sha256':hashlib.sha256(mp3.read_bytes()).hexdigest(),'duration':272.300408,'listening_confirmed':False,'method':'Known sung/spoken text locally aligned, repeated choruses checked spectrally','cues':cues},indent=2))
sheet=Image.new('RGB',(512*3,280*((len(thumbs)+2)//3)),'#14251c');draw=ImageDraw.Draw(sheet)
for i,im in enumerate(thumbs):
    x=i%3*512;y=i//3*280;draw.text((x+6,y+4),f'Page {i+1}',fill='white')
    colored=Image.new('RGB',(128,64),'#b5ce83');colored.paste('#172814',mask=im)
    sheet.paste(colored.resize((512,256),Image.Resampling.NEAREST),(x,y+24))
sheet.save(R/'previews/all-pages.png')
print(len(lyrics),'lyric lines;',len(thumbs),'page layouts;',len(frames),'unique frames;',len(cues),'cues')
