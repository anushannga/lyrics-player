"""Rasterize supplied ISI lyrics into word-wrapped native ST7920 frames."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from pixel_format import native
ROOT=Path(__file__).resolve().parents[1]
font=ImageFont.truetype(str(ROOT/'assets/isigurul_0.ttf'),24*4)
def ink(text):
    b=font.getbbox(text,stroke_width=1)
    im=Image.new('L',(b[2]-b[0]+8,b[3]-b[1]+8))
    ImageDraw.Draw(im).text((4-b[0],4-b[1]),text,font=font,fill=255,stroke_width=1)
    return im.crop(im.getbbox())
def fits(text):return ink(text).width<=124*4
def wrap(words,base=0):
    rows=[];start=base;row=[]
    for i,word in enumerate(words,base):
        if not fits(word):raise ValueError('Word exceeds LCD: '+word)
        if row and not fits(' '.join(row+[word])):
            rows.append((' '.join(row),start,i));row=[];start=i
        row.append(word)
    rows.append((' '.join(row),start,base+len(words)))
    return rows
def frame(rows):
    strips=[]
    for text in rows:
        im=ink(text)
        im=im.resize(((im.width+3)//4,(im.height+3)//4),Image.Resampling.LANCZOS)
        strips.append(im.point(lambda v:255 if v>=170 else 0).convert('1'))
    height=sum(s.height for s in strips)+3*(len(strips)-1)
    assert height<=62,(rows,height)
    out=Image.new('1',(128,64)); y=(64-height)//2
    for s in strips:out.paste(s,((128-s.width)//2,y));y+=s.height+3
    return out
lines=[s.strip() for s in (ROOT/'lyrics_isi.txt').read_text().splitlines() if s.strip()]
pages=[];bitmaps=[];thumbs=[]
for line_index,line in enumerate(lines):
    words=line.split();rows=wrap(words)
    groups=[rows]
    if len(rows)>2:
        # Balance long lyric halves so the final page is not one fleeting word.
        candidates=[]
        for cut in range(1,len(words)):
            left=wrap(words[:cut]);right=wrap(words[cut:],cut)
            if len(left)<=2 and len(right)<=2:
                score=abs(sum(ink(w).width for w in words[:cut])-sum(ink(w).width for w in words[cut:]))
                candidates.append((score,[left,right]))
        if not candidates:raise ValueError('Lyric requires more than two pages')
        groups=min(candidates,key=lambda v:v[0])[1]
    for pair in groups:
        im=frame([p[0] for p in pair]);data=native(im)
        if data not in bitmaps:bitmaps.append(data)
        pages.append({'line':line_index,'word_start':pair[0][1],'word_end':pair[-1][2],'rows':[p[0] for p in pair],'bitmap':bitmaps.index(data)})
        thumbs.append(im)
        if len(pages)<=16:im.resize((768,384),Image.Resampling.NEAREST).save(ROOT/'previews'/f'page-{len(pages):03}.png')
blob=b''.join(bitmaps);(ROOT/'frames.bin').write_bytes(blob)
identity=hashlib.sha256((ROOT/'lyrics_isi.txt').read_bytes()+blob).hexdigest()[:16]
(ROOT/'manifest.json').write_text(json.dumps({'id':identity,'pixel_format':'st7920-horizontal-msb','font':'IsiGurulugomi','font_size':24,'line_count':len(lines),'bitmap_count':len(bitmaps),'pages':pages},ensure_ascii=False,indent=2)+'\n')
sheet=Image.new('RGB',(512*3,284*((len(thumbs)+2)//3)),'#14251c');draw=ImageDraw.Draw(sheet)
for i,im in enumerate(thumbs):
    x=(i%3)*512;y=(i//3)*284;draw.text((x+8,y+4),f"Page {i+1} / lyric {pages[i]['line']+1}",fill='#ddf2bf')
    colored=Image.new('RGB',(128,64),'#b5ce83');colored.paste('#172814',mask=im)
    sheet.paste(colored.resize((512,256),Image.Resampling.NEAREST),(x,y+28))
sheet.save(ROOT/'previews/all-pages.png')
print(f'{len(lines)} lyrics; {len(pages)} pages; {len(bitmaps)} unique frames; {len(blob)} bytes; {identity}')
