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
    def __init__(self, parent, backend):
        '''
        Constructor
        '''
        _style = ttk.Style()
        _style.theme_use('alt')
        _style.configure('TFrame', background='maroon')
        Frame.__init__(self, parent, background='#000000')
        self.parent = parent
        self.parent.minsize(600, 400)
        self.parent.geometry("400x300+100+100")
        self.backend = backend
        self.printer = VWPrinter()
        self.initialize_user_interface()

    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type
        items and insert them into the treeview
        """
        self.parent.title("上海大众通行证管理系统 - V1.0")
        #self.parent.grid_rowconfigure(0, weight=1)
        #self.parent.grid_columnconfigure(0, pad=10)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.config(background="lavender")
        self.main_label = Label(self.parent, text="主车牌", padx=5)
        self.main_entry = Entry(self.parent)
        self.main_label.grid(row=0, sticky=W)        
        self.main_entry.grid(row=0, column=1, columnspan=3, sticky=EW)

        self.sub_label = Label(self.parent, text="副车牌", padx=5)
        self.sub_entry = Entry(self.parent)
        self.sub_label.grid(row=1, sticky=W)        
        self.sub_entry.grid(row=1, column=1, columnspan=3, sticky=EW)

        self.print_button = Button(text="打印车牌", command=self.print_one, state='disabled')
        self.print_button.grid(row=2, column=3, sticky=E)
    
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
        
        VWPrintDialog(self, ((main_plate, sub_plate), values))


        values = self.tree.item(item[0], "values")
        plates = values[2:4] if values[3] != "None" else [values[2]]
        if not item:
            print("No item selected when print!!!")
        else:
            VWPrintDialog(self, (0, plates, values))
