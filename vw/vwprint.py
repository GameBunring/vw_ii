from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox
import qrcode
import os, sys
from PIL import Image, ImageTk, ImageWin, ImageFont, ImageDraw
import platform
import time

class VWPrintDialog():
    def __init__(self, parent, values):
        _t = time.time()
        self.top = top = Toplevel(parent)
        self.top.title("打印预览")
        self.parent = parent
        self.printer = parent.printer
        
        self.type = 0
        self.plates = values[1]
        self.values = values[2]
        _img = self._gen_plate_img()
        self._img = _img.copy()
        _img.thumbnail((600,400), Image.ANTIALIAS)

        canvas = Canvas(top, width=_img.size[0], height=_img.size[1], bd=2)
        canvas.grid(row=0, columnspan=2)
        tk_photo = ImageTk.PhotoImage(_img)
        canvas.image = tk_photo
        canvas.create_image(_img.size[0]//2, _img.size[1]//2, image=tk_photo)
        sep = ttk.Separator(top)
        sep.grid(row=1, columnspan=2, sticky=EW)
        print_button = Button(top, text='打印', command=self.on_click_print)
        print_button.grid(row=2, column=1, sticky='e')
        save_button = Button(top, text='保存', command=self.on_click_save)
        save_button.grid(row=2, column=0, sticky='w')


    @classmethod
    def concate(cls, plate_chrs, size=512):
        import configparser, logging
        config = configparser.ConfigParser()
        config.read('config.ini')
        gap = int(config['paras']['gap_10'])
        if len(plate_chrs) == 8:
            gap = int(config['paras']['gap_6'])
        if len(plate_chrs) == 7:
            gap = int(config['paras']['gap_5'])
        listofimages = ['images/{}.jpg'.format(i) for i in plate_chrs]
        size = (size, size)
        def my_thumb(image_file, s):
            try:
                image = Image.open(image_file)
                image.thumbnail(s, Image.ANTIALIAS)
            except FileNotFoundError:
                # TODO add logging handler
                pass
            return image

        thumbs = (my_thumb(i, size) for i in listofimages)
        widths, heights = zip(*(i.size for i in thumbs))
        total_width = sum(widths) + gap * (len(widths) - 1)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height), (255,255,255))

        x_offset = 0
        thumbs = (my_thumb(i, size) for i in listofimages)
        for im in thumbs:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0] + gap
        return new_im

    def _gen_meta_img(self):
        text = list(self.values[:3])
        if len(text[2]) > 10:
            text[2] = self.values[3]
        meta_im = self.generate_meta_image(text)
        return meta_im
    
    def _gen_plate_img(self):
        new_im = self.generate_plate_image(self.plates, self.values)
        return new_im

    @classmethod
    def generate_plate_image(cls, plates, values):
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        _left_main = int(config['paras']['left_main'])
        _top_main = int(config['paras']['top_main'])
        _length_main = int(config['paras']['length_main'])
        _height_main = int(config['paras']['height_main'])

        _length_sub = int(config['paras']['length_sub'])
        _height_sub = int(config['paras']['height_sub'])
        _top_sub = _top_main + int(config['paras']['separate']) + _height_main

        A4 = (2384, 3368)
        new_im = Image.new('RGB', (A4[1], A4[0]), (255, 255, 255))
        assert plates
        x_offset = _left_main
        y_offset = _top_main

        plateImage = cls.concate(plates[0])
        plateImage.thumbnail((_length_main, _height_main), Image.ANTIALIAS)
        plateImage.size
        new_im.paste(plateImage, (x_offset, y_offset))

        if plates[1]:
            subPlateImage = cls.concate(plates[1])
            subPlateImage.thumbnail([_length_sub, _height_sub], Image.ANTIALIAS)
            y_offset = _top_sub
            x_offset = plateImage.size[0] - subPlateImage.size[0]
            new_im.paste(subPlateImage, (x_offset, y_offset))

        # send_imgs_to_printer(new_im)
        return new_im

    def on_click_print(self):
        self.printer.print_img(self._img)        
        self.top.destroy()
        self.parent.search()
    
    def on_click_save(self):
        self._img.save('.jpg'.format(self.plates[0]),'jpeg')
        tkinter.messagebox.showinfo('保存成功','车牌图片已保存为: {}.jpg'.format(self.plates[0]))
        
if __name__ == '__main__':
    pass
    # VWPrintDialog.generate_qrcode_image(apt='我森上海大众机场有限(asd)公司无线公司', name='高泊宁', _id=15)
    # root = Tk()
    # pd = VWPrintDialog(root, (0, ['沪H21263', '沪A2M2B1'], [1] * 12))
    # image1 = pd._gen_plate_img()
    # image1.thumbnail((800, 600), Image.ANTIALIAS)
    # #image1 = PrintDialog.concate('沪H582B1')
    # #image1.thumbnail((500, 200), Image.ANTIALIAS)
    # tkpi = ImageTk.PhotoImage(image1)
    # label_image = Label(root, image=tkpi)
    # root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
    # label_image.place(x=0, y=0, width=image1.size[0], height=image1.size[1])
    # root.mainloop()