from tkinter import *
import tkinter
import tkinter.font
import tkinter.messagebox
import tkinter.ttk as ttk
from vw.vwprint import VWPrintDialog
from vw.vwprinter import VWPrinter

class VWGui(tkinter.Frame):
    '''
    classdocs
    '''
    def __init__(self, parent):
        '''
        Constructor
        '''
        _style = ttk.Style()
        _style.theme_use('alt')
        _style.configure('TFrame', background='maroon')
        Frame.__init__(self, parent, background='#000000')
        self.parent = parent
        self.parent.minsize(200, 100)
        self.parent.geometry("400x100+300+300")
        self.printer = VWPrinter()
        self.initialize_user_interface()

    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type
        items and insert them into the treeview
        """
        self.parent.title("上海大众停车证打印系统-v0.8")
        #self.parent.grid_rowconfigure(0, weight=1)
        #self.parent.grid_columnconfigure(0, pad=10)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)
        self.main_label = Label(self.parent, text="主车牌", padx=5)
        self.main_entry = Entry(self.parent)
        self.main_label.grid(row=0, sticky=W)        
        self.main_entry.grid(row=0, column=1, columnspan=3, padx=5, sticky=EW)

        self.sub_label = Label(self.parent, text="副车牌", padx=5)
        self.sub_entry = Entry(self.parent)
        self.sub_label.grid(row=1, sticky=W)        
        self.sub_entry.grid(row=1, column=1, columnspan=3, padx=5, sticky=EW)

        self.print_button = Button(text="打印车牌", command=self.print_one)
        self.print_button.grid(row=2, column=3, sticky=E)

        self.print_all_button = Button(text="批量打印", command=self.print_all)
        self.print_all_button.grid(row=2, column=0, sticky=W)
    
    def print_one(self):
        main_plate = self.main_entry.get().strip()
        sub_plate = self.sub_entry.get().strip()
        if not main_plate:
            tkinter.messagebox.showinfo('车牌为空','没有填写主车牌！')
            return
        elif " " in main_plate or " " in sub_plate:
            tkinter.messagebox.showinfo('车牌中含有空格','车牌中含有空格，请删掉空格重试！')
            return
        elif len(main_plate) not in (7, 8) or len(sub_plate) not in (0, 7, 8):
            tkinter.messagebox.showinfo('车牌位数有误', '车牌位数有误，请核对无误再打印！')
        
        VWPrintDialog(self, (main_plate, sub_plate))

    def print_all(self):
        plates = self.load_xls()
        if len(plates) > 30:
            tkinter.messagebox.showerror('车牌过多', '表格里有{}个车牌，一次最多打印30个车牌，请删除部分车牌后重试！'.format(len(plates)))
            return
        if(tkinter.messagebox.askyesno('全部打印','确定要打印这{}个车牌吗?可能需要等待较长时间！'.format(len(plates)))):
            _plate_imgs = (VWPrintDialog().generate_plate_image(plate) for plate in plates)
            if self.printer.print_imgs(_plate_imgs):
                tkinter.messagebox.showinfo('打印成功', '打印成功！')
            else:
                tkinter.messagebox.showinfo('打印失败', '请重新启动软件或联系管理员')
    
    def load_xls(self):
        import xlrd
        worksheet = xlrd.open_workbook('2018停车证导入模板.xls').sheet_by_index(0)
        res = []
        for i in range(1, worksheet.nrows):
            row_value = worksheet.row_values(i)
            res.append((row_value[0], row_value[1]))
        return res