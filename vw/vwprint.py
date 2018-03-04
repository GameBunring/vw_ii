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
        # self.backend = parent.backend
        self.parent = parent
        self.printer = parent.printer
        
        # 0 means plate infomation
        if values[0] == 0:
            self.type = 0
            self.plates = values[1]
            self.values = values[2]
            _img = self._gen_plate_img()
        # 1 means plate name
        elif values[0] == 1:
            self.type = 1
            self.values = values[1]
            _img = self._gen_meta_img()

        
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
        print(time.time() - _t)


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
        _left_qrcode = int(config['paras']['left_qrcode'])
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
        if len(plates) == 1:
            plateImage = cls.concate(plates[0])
            plateImage.thumbnail((_length_main, _height_main), Image.ANTIALIAS)
            new_im.paste(plateImage, (x_offset, y_offset))
            y_offset = _top_sub
            x_offset = _left_qrcode
        elif len(plates) == 2:
            if plates[1][:2].lower() in ("mq", 'ep', 'sv'):
                y_offset += 80
                plateImage = cls.concate('VIN#'+plates[0], )
                plateImage.thumbnail((_length_main, _height_main - 50), Image.ANTIALIAS)
                new_im.paste(plateImage, (x_offset, y_offset))
                y_offset = _top_sub - 70
                subPlateImage = cls.concate(plates[1][:2] + "试车#" + plates[1][2:])
                subPlateImage.thumbnail([_length_sub, _height_sub + 20], Image.ANTIALIAS)
                new_im.paste(subPlateImage, (x_offset, y_offset))
                x_offset = _left_qrcode
                y_offset = _top_sub - 90
                
            else:
                plateImage = cls.concate(plates[0])
                plateImage.thumbnail((_length_main, _height_main), Image.ANTIALIAS)
                new_im.paste(plateImage, (x_offset, y_offset))
                y_offset = _top_sub + 20
                # subImage = cls.concate("副")
                # subImage.thumbnail((9999, A4[0] // 7), Image.ANTIALIAS)
                # new_im.paste(subImage, (x_offset, y_offset))
                # x_offset += A4[1] // 8
                subPlateImage = cls.concate(plates[1])
                subPlateImage.thumbnail([900, 220], Image.ANTIALIAS)
                new_im.paste(subPlateImage, (x_offset, y_offset))
                x_offset = _left_qrcode
                y_offset = _top_sub

        qrImage = cls.generate_qrcode_image(values[0], values[1], values[7])

        qrImage.thumbnail((280,280), Image.ANTIALIAS)
        new_im.paste(qrImage, (x_offset, y_offset))
        # send_imgs_to_printer(new_im)
        return new_im

    def on_click_print(self):
        self.printer.print_img(self._img)        
        self.parent.backend.set_ids_printed([self.values[7]])
        self.top.destroy()
        self.parent.search()
    
    def on_click_save(self):
        if self.type == 0:
            self._img.save('plate_{}.jpg'.format(self.values[7]),'jpeg')
            tkinter.messagebox.showinfo('保存成功','车牌图片已保存为: plate_{}.jpg'.format(self.values[7]))
        if self.type == 1:
            self._img.save('plate_name_{}.jpg'.format(self.values[7]),'jpeg')
            tkinter.messagebox.showinfo('保存成功','车牌名图片已保存为: plate_name_{}.jpg'.format(self.values[7]))
        
    @classmethod
    def generate_qrcode_image(cls, apt, name, _id):
        import hashlib, base64, zlib, qrcode
        _salt = b'$6$pxvEXy6TgUKs62Xt'
        _show = '{}∆{}ø{}'.format(apt, name, _id)
        # qrcode.make(_show).save('/Users/burning/Desktop/test_origin.jpg', 'jpeg')
        rep = (('£', '上海大众'), ('∑', '有限公司'), ('ß' ,'上海'), ('ƒ', '公司'))
        for s, t in rep:
            _show = _show.replace(t, s)
        _sig_t = hashlib.pbkdf2_hmac(hashlib.sha1().name, str.encode(_show), base64.b64encode(_salt), 100000, dklen=6)
        _sig = [chr(i + 256) for i in _sig_t]
        _show += ''.join(_sig)

        def ugly(text):
            b = bytearray(text, 'utf-8')
            for i in range(len(b)):
                if b[i] & 128 and (not b[i] & 64):
                    if b[i] & 4:
                        b[i] -= 4
                    else:
                        b[i] += 4
                if 40 <= b[i] <= 120:
                    b[i] = 160 - b[i]
            return b.decode('utf-8')

        return qrcode.make(ugly(_show))


    @classmethod
    def generate_meta_image(cls, text, **options):
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        _font_size = int(config['paras']['font_size'])
        _left = int(config['paras']['left_back'])
        _top = int(config['paras']['top_back'])
        im = Image.new('RGB', (3368, 2384), (255,)*3)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SIMHEI.ttf", _font_size)

        _apt = text[0]
        if len(_apt) > 4:
            _apt = _apt[:4] + "#"
        draw.text((_left,_top), "部  门:", font=font, fill=0, **options)
        draw.text((_left + int(3.5 * _font_size), _top), _apt, font=font, fill=0, **options)
        twidth, theight = draw.textsize(_apt, font=font)

        lx, ly = _left + int(3.5 * _font_size), _top + theight
        draw.line((lx, ly, lx + twidth, ly), fill=0)

        _name = text[1]
        if len(_name) > 5:
            _name = _name[:5] + "#"
        draw.text((_left,_top+_font_size), "姓  名:", font=font, fill=0, **options)
        draw.text((_left + int(3.5 * _font_size), _top+_font_size), _name, font=font, fill=0, **options)
        twidth, theight = draw.textsize(_name, font=font)
        lx, ly = _left + int(3.5 * _font_size), _top+_font_size + theight
        draw.line((lx, ly, lx + twidth, ly), fill=0)

        _plate = text[2]
        # if len(_plate) > 8:
        #     _plate = _plate[:8] + "#"
        draw.text((_left,_top+_font_size*2), "车牌号:", font=font, fill=0, **options)
        draw.text((_left + int(3.5 * _font_size), _top+_font_size*2), _plate, font=font, fill=0, **options)
        twidth, theight = draw.textsize(_plate, font=font)
        lx, ly = (_left + int(3.5 * _font_size), _top+_font_size*2+theight)
        draw.line((lx, ly, lx + twidth, ly), fill=0)
        return im
    
    def send_to_printer(self, _img, left, top, bottom, right):
        pass


if __name__ == '__main__':
    VWPrintDialog.generate_qrcode_image(apt='我森上海大众机场有限(asd)公司无线公司', name='高泊宁', _id=15)
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