import win32print
import win32ui
import tkinter.messagebox
from PIL import Image, ImageWin, ImageFont, ImageFilter, ImageDraw

# Constants for GetDeviceCaps
#
#
# HORZRES / VERTRES = printable area
#
HORZRES = 8
VERTRES = 10
#
# LOGPIXELS = dots per inch
#
LOGPIXELSX = 88
LOGPIXELSY = 90
#
# PHYSICALWIDTH/HEIGHT = total area
#
PHYSICALWIDTH = 110
PHYSICALHEIGHT = 111
#
# PHYSICALOFFSETX/Y = left / top margin
#
PHYSICALOFFSETX = 112
PHYSICALOFFSETY = 113

class VWPrinter():
    def __init__(self):
        self.printer_name = win32print.GetDefaultPrinter ()
        self.count = 1
        #
        # You can only write a Device-independent bitmap
        #  directly to a Windows device context; therefore
        #  we need (for ease) to use the Python Imaging
        #  Library to manipulate the image.
        #
        # Create a device context from a named printer
        #  and assess the printable size of the paper.
        #
                # printer_margins = self.hDC.GetDeviceCaps (PHYSICALOFFSETX), self.hDC.GetDeviceCaps (PHYSICALOFFSETY)

    def print_img(self, img):
        self.print_imgs([img])

    def print_imgs(self, imgs):
        self.hDC = win32ui.CreateDC ()
        self.hDC.CreatePrinterDC (self.printer_name)
        self.printable_area = self.hDC.GetDeviceCaps (HORZRES), self.hDC.GetDeviceCaps (VERTRES)
        self.printer_size = self.hDC.GetDeviceCaps (PHYSICALWIDTH), self.hDC.GetDeviceCaps (PHYSICALHEIGHT)

        try:
            print('I am here1')
            self.hDC.StartDoc ("test_{}".format(self.count))
            print('I am here2')
        except win32ui.error:
            tkinter.messagebox.showinfo("打印出错", '请重启软件或联系系统管理员')
            return False


        for _img in imgs:
            try:
                self.hDC.StartPage ()
                if _img.size[0] > _img.size[1]:
                    img = _img.rotate (90, expand=1)
                else:
                    img = img
                dib = ImageWin.Dib (img)
                ratios = [1.0 * self.printable_area[0] / img.size[0], 1.0 * self.printable_area[1] / img.size[1]]
                scale = min(ratios)
                scaled_width, scaled_height = [int (scale * j) for j in img.size]
                x1 = int ((self.printer_size[0] - scaled_width) / 2)
                y1 = int ((self.printer_size[1] - scaled_height) / 2)
                x2 = x1 + scaled_width
                y2 = y1 + scaled_height
                dib.draw (self.hDC.GetHandleOutput (), (x1, y1, x2, y2))

                self.hDC.EndPage ()
            except Exception:
                return False

        self.hDC.EndDoc ()
        self.hDC.DeleteDC ()
        return True
        