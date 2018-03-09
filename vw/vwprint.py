from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox
import qrcode
import os, sys
from PIL import Image, ImageTk, ImageWin, ImageFont, ImageDraw
import platform
import time

class VWPrintDialog():
    def __init__(self, parent=None, plates=None):
        if parent:
            _t = time.time()
            self.top = top = Toplevel(parent)
            self.top.title("打印预览")
            self.parent = parent
            self.printer = parent.printer
            self.plates = plates
            if plates[1]:
                self.read_config(2)
            else:
                self.read_config(1)

            _img = self.generate_plate_img()
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


    def read_config(self, plates_num):
        import configparser, logging
        config = configparser.ConfigParser()
        config.read('config.ini')
        if plates_num == 2:
            param_name = 'paras'
            self.gap_fuzheng = int(config['paras']['gap_fuzheng'])
            self.gap_6 = int(config['paras']['gap_6'])
            self.gap_5 = int(config['paras']['gap_5'])
            self.top_main = int(config[param_name]['top_main'])
            self.height_sub = int(config[param_name]['max_height_sub'])
            self.height_main = int(config[param_name]['max_height_main'])
            self.top_sub = self.top_main + int(config[param_name]['separate']) + self.height_main


        elif plates_num == 1:
            param_name = 'paras_1'
            self.gap_5 = int(config['paras_1']['gap_5'])
            self.gap_6 = int(config['paras_1']['gap_6'])
            self.top_main = int(config[param_name]['top_main'])
            self.height_main = int(config[param_name]['max_height_main'])

        self.right_margin = int(config[param_name]['right_margin'])
        self.length_main = int(config[param_name]['max_length_main'])



    def concate(self, plate_chrs, size=512, gap=None):
        listofimages = ['images/{}.jpg'.format(i) for i in plate_chrs]
        size = (size, size)
        def my_thumb(image_file, s):
            try:
                image = Image.open(image_file)
                image.thumbnail(s, Image.ANTIALIAS)
            except FileNotFoundError:
                # TODO add logging handler
                print(image_file)
                pass
            return image

        gap = 0
        if len(plate_chrs) == 2:
            gap = self.gap_fuzheng
        elif len(plate_chrs) == 7:
            gap = self.gap_5
        elif len(plate_chrs) == 8:
            gap = self.gap_6

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

    def generate_plate_image(self, plates=None):
        if plates:
            if plates[1]:
                self.read_config(2)
            else:
                self.read_config(1)

        A4 = (2384, 3368)
        new_im = Image.new('RGB', (A4[1], A4[0]), (255, 255, 255))

        plateImage = self.concate(plates[0])
        plateImage.thumbnail((self.length_main, self.height_main), Image.ANTIALIAS)
        _left_main = A4[1] - self.right_margin - plateImage.size[0]
        y_offset = self.top_main
        x_offset = _left_main

        new_im.paste(plateImage, (x_offset, y_offset))

        if plates[1]:
            subLabelImage = self.concate('副证')
            subLabelImage.thumbnail([2000, self.height_sub], Image.ANTIALIAS)

            subPlateImage = self.concate(plates[1])
            subPlateImage.thumbnail([plateImage.size[0] - subLabelImage.size[0] - 80, self.height_sub], Image.ANTIALIAS)

            y_offset = self.top_sub
            x_offset = _left_main
            new_im.paste(subLabelImage, (x_offset, y_offset))
            
            x_offset = _left_main + plateImage.size[0] - subPlateImage.size[0]
            new_im.paste(subPlateImage, (x_offset, y_offset))

        return new_im

    def on_click_print(self):
        self.printer.print_img(self._img)        
        self.top.destroy()
    
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