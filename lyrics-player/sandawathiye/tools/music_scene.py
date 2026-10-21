"""Four animated music-note groups for the instrumental break."""
from PIL import Image,ImageDraw

def music_scene(phase):
    im=Image.new('1',(128,64));d=ImageDraw.Draw(im)
    for i,(x,y) in enumerate(((5,24),(69,24),(5,54),(69,54))):
        y+=(-1 if (phase+i)%4<2 else 1)
        d.ellipse((x,y-3,x+7,y+1),fill=1)
        d.line((x+7,y-1,x+7,y-18),fill=1,width=2)
        d.line((x+7,y-18,x+13,y-13),fill=1,width=2)
        for k in range(6 if i<3 else 5):
            px=x+20+k*6
            d.point((px,y),fill=1)
            if k==(phase+i)%6:d.rectangle((px,y-1,px+1,y),fill=1)
    return im
