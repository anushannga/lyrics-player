"""ST7920 U8g2 buffer layout: horizontal scanlines, MSB is the left pixel."""
def native(image):
    if image.size != (128,64):raise ValueError('Expected 128x64 LCD image')
    return bytes(sum(int(bool(image.getpixel((x+b,y))))<<(7-b) for b in range(8)) for y in range(64) for x in range(0,128,8))
