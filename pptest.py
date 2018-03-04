from PIL import Image, ImageDraw, ImageFont, ImageFilter

#configuration
font_size=36
width=500
height=100
back_ground_color=(255,255,255)
font_size=36
font_color=(0,0,0)
unicode_text = u"\u2605" + u"\u2606" + u"我爱你"

im  =  Image.new ( "RGB", (width,height), back_ground_color )
draw  =  ImageDraw.Draw ( im )
unicode_font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SIMHEI.ttf", font_size)
draw.text ( (10,10), unicode_text, font=unicode_font, fill=font_color )

im.save("i1111.jpg")

def draw_underlined_text(draw, pos, text, font, **options):
    twidth, theight = draw.textsize(text, font=font)
    lx, ly = pos[0], pos[1] + theight
    draw.text(pos, text, font=font, **options)
    draw.line((lx, ly, lx + twidth, ly), **options)

im = Image.new('RGB', (3508, 2480), (255,)*3)
draw = ImageDraw.Draw(im)
font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SIMHEI.ttf", 60)

draw_underlined_text(draw, (20, 20), '姓名:', font, fill=0)
draw_underlined_text(draw, (20, 80), '车牌号', font, fill=0)

im.show()
