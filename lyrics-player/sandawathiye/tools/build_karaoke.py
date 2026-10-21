"""Build stable word-by-word Nikini pages and explicitly drawn music/dots."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from pixel_format import native
from music_scene import music_scene

R=Path(__file__).resolve().parents[1]
S=4
FONT_SIZE=20
font=ImageFont.truetype(str(R/'assets/tharudigitalnikini.ttf'),FONT_SIZE*S)
lines=(R/'lyrics_isi.txt').read_text().splitlines()
alignment={}
for name in ['alignment.json','alignment_bridge.json','alignment_tail.json','alignment_refined.json','alignment_audio_rechecked.json']:
    p=R/name
    if p.exists():
        values=json.loads(p.read_text())
        if name=='alignment_audio_rechecked.json' and len(values)!=23:continue
        alignment.update({v['line']:v for v in values})
frames=[];pages=[];cues=[];thumbs=[];frame_cache={}
def addframe(im):
    key=im.tobytes()
    if key not in frame_cache:
        data=native(im)
        if data not in frames:frames.append(data)
        frame_cache[key]=frames.index(data)
    return frame_cache[key]
def addcue(t,im,kind,line=-1,word=-1,animation=None):
    page={'bitmap':addframe(im),'line':line,'word':word,'kind':kind}
    if animation:page['animation']=[addframe(v) for v in animation]
    pages.append(page);cues.append({'time':round(t,3),'page':len(pages)-1,'style':'melodic','kind':kind})
DOTW=10*S
def measure(w):return font.getbbox(w,stroke_width=1)
def render(items,revealed,dot_counts=None):
    # Position the complete page once; later words never move earlier words.
    im=Image.new('L',(128*S,64*S));d=ImageDraw.Draw(im)
    total=sum(row['height'] for row in items)+3*S*(len(items)-1)
    y=(60*S-total)//2
    dot_counts=dot_counts or {}
    dot_positions=[]
    for row in items:
        x=(128*S-row['width'])//2
        for index,w,b,dot in row['words']:
            if index<=revealed:
                d.text((x-b[0],y-row['top']),w,font=font,fill=255,stroke_width=1)
                if dot_counts.get(index):dot_positions.append((x+(b[2]-b[0]),y-row['top']+b[3]-4*S,dot_counts[index]))
            x+=b[2]-b[0]+(DOTW if dot else 0)+4*S
        y+=row['height']+3*S
    im=im.resize((128,64),Image.Resampling.LANCZOS).point(lambda v:255 if v>=150 else 0).convert('1')
    d=ImageDraw.Draw(im)
    for endx,doty,count in dot_positions:
        cy=doty//S
        for k in range(count):d.ellipse((endx//S+2+k*4,cy-1,endx//S+3+k*4,cy),fill=1)
    return im
def reveal(old,new,fraction):
    # Dither just the newly appearing pixels; existing words remain solid.
    bayer=((0,8,2,10),(12,4,14,6),(3,11,1,9),(15,7,13,5))
    im=old.copy()
    for y in range(64):
        for x in range(128):
            if new.getpixel((x,y)) and bayer[y%4][x%4]<fraction*16:im.putpixel((x,y),1)
    return im
for line_index,line in enumerate(lines):
    if line_index==17:continue
    source_words=line.split()
    words=[w.replace('...','') for w in source_words]
    rowdata=alignment[line_index]
    times=[dict(w) for w in rowdata['words']]
    assert len(words)==len(times),(line_index,len(words),len(times))
    # Repair zero-length DTW words by splitting their shared neighbour interval.
    for j in range(len(times)-1):
        if times[j]['end']<=times[j]['start']:
            mid=(times[j]['start']+times[j+1]['end'])/2
            times[j]['end']=mid;times[j+1]['start']=mid
    rows=[];row=[];width=0
    dotted={}
    for j,w in enumerate(words):
        dotted[j]='...' in source_words[j]
    for j,w in enumerate(words):
        b=measure(w);ww=b[2]-b[0]+(DOTW if dotted[j] else 0)
        assert ww<=124*S,(w,ww)
        if row and width+4*S+ww>124*S:
            rows.append(row);row=[];width=0
        row.append((j,w,b,dotted[j]));width+=ww+(4*S if len(row)>1 else 0)
    if row:rows.append(row)
    for start in range(0,len(rows),2):
        group=rows[start:start+2];items=[]
        for row in group:
            top=min(v[2][1] for v in row);bottom=max(v[2][3] for v in row)
            items.append({'words':row,'top':top,'height':bottom-top,'width':sum(v[2][2]-v[2][0]+(DOTW if v[3] else 0) for v in row)+4*S*(len(row)-1)})
        assert sum(v['height'] for v in items)+3*S*(len(items)-1)<=58*S
        old=Image.new('1',(128,64))
        dot_counts={}
        for j,w,b,dot in sum(group,[]):
            if dotted[j]:dot_counts[j]=3
            target=render(items,j,dot_counts)
            # Keep a short two-step dissolve within the LCD's measured transfer budget.
            addcue(times[j]['start'],target,'word',line_index,j,[reveal(old,target,0.5)])
            old=target
        thumbs.append(render(items,group[-1][-1][0],dot_counts))
    alignment[line_index]['words']=times

# Show music throughout intro, instrumental breaks, outro and real phrase gaps.
intervals=[(0,min(v['words'][0]['start'] for v in alignment.values()))]
ordered=sorted(alignment.values(),key=lambda v:v['words'][0]['start'])
for prev,nxt in zip(ordered,ordered[1:]):
    end=prev['words'][-1]['end'];start=nxt['words'][0]['start']
    if start-end>=1.35:intervals.append((end+0.2,start))
intervals.append((ordered[-1]['words'][-1]['end']+0.35,240.483265))
solo_start=alignment[16]['words'][-1]['end']+0.2
solo_end=alignment[18]['words'][0]['start']
for start,end in intervals:
    if abs(start-solo_start)<0.01:
        phase=0;t=start
        while t<end-0.2:
            addcue(t,music_scene(phase),'music');phase+=1;t=start+phase*0.24
    else:
        cues.append({'time':round(start,3),'page':-1,'kind':'silence','style':'melodic'})
cues.sort(key=lambda c:c['time'])
assert all(a['time']<b['time'] for a,b in zip(cues,cues[1:])), 'Duplicate cue times'
blob=b''.join(frames)
identity=hashlib.sha256((R/'lyrics_isi.txt').read_bytes()+blob).hexdigest()[:16]
(R/'frames.bin').write_bytes(blob)
(R/'manifest.json').write_text(json.dumps({'id':identity,'pixel_format':'st7920-horizontal-msb','font':'THARU DIGITAL NIKINI','font_size':FONT_SIZE,'line_count':len(lines),'bitmap_count':len(frames),'pages':pages},indent=2))
mp3=Path.home()/'Downloads/Sandawathiye Ridma Weerawardena Charitha Attalage.mp3'
(R/'timings.json').write_text(json.dumps({'lyrics_id':identity,'audio_sha256':hashlib.sha256(mp3.read_bytes()).hexdigest(),'method':'Local phonetic word alignment; not listening-confirmed','cues':cues},indent=2))
(R/'alignment_used.json').write_text(json.dumps(ordered,indent=2))
sheet=Image.new('RGB',(512*3,280*((len(thumbs)+2)//3)),'#14251c');d=ImageDraw.Draw(sheet)
for i,im in enumerate(thumbs):
    x=i%3*512;y=i//3*280
    d.text((x+5,y+3),f'Page {i+1} / 20px',fill='white')
    color=Image.new('RGB',(128,64),'#b5ce83');color.paste('#172814',mask=im)
    sheet.paste(color.resize((512,256),Image.Resampling.NEAREST),(x,y+24))
sheet.save(R/'previews/karaoke-pages.png')
print(f'{len(thumbs)} layouts, {len(frames)} unique frames, {len(cues)} word/sustain/music cues; {identity}')
