import sys
from PIL import Image

def concate(plate_nums):
    listofimages = ['{}.jpg'.format(i) for i in plate_nums]
    images = map(Image.open, listofimages)
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height), (255,255,255))

    x_offset = 0
    images = map(Image.open, listofimages)
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return new_im

if __name__ == '__main__':
    concate('沪0121', )
