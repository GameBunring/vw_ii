import tkinter
from tkinter import *
from datetime import date
import pickle
import sys

class VWActivate(tkinter.Frame):
    def __init__(self, parent, expire_date, dead_date, status):
        _style = ttk.Style()
        _style.theme_use('alt')
        _style.configure('TFrame', background='maroon')
        Frame.__init__(self, parent, background='#000000')
        self.parent = parent
        self.expire_date = expire_date
        self.dead_date = dead_date
        self.status = status
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.title("续期请求")

        self.label = Label(self.parent, text="软件在{}到期，请在{}前完成续期，否则将无法使用。谢谢！", padx=5)
        self.register_label = Label(self.parent, text='注册码', padx=5)
        self.register_entry = Entry(self,parent)
        self.register_button = Button(text='注册', command=self.activate)
        self.skip_button = Button(text='跳过', command=self.skip)
        if status == 1:
            self.skip_button.config(state='enabled')
        elif status == -1:
            self.skip_button.config(state='disabled')

        self.label.grid(row=0, colomnspan=3)
        self.register_label.grid(row=1, colomn=0)
        self.register_entry.grid(row=1, colomnspan=3)
        self.register_button.grid(row=1, colomn=2)

    def activate(self):
        input_code = self.register_entry.get().strip()
        if len(input_code) < 10:
            tkinter.messagebox.showwarning('注册码位数有误，请检查')
            return
        if input_code in str(hash('xddd{}'.format(self.expire_date.year))):    
            new_expire_date = date(self.expire_date.year + 1, self.expire_date.month, self.expire_date.day)
            pickle.dump(new_expire_date, open('tcl/time', 'wb'))
            tkinter.messagebox.showwarning('注册成功，感谢您续期！软件使用期更新为{}，请重新打开软件！'.format(new_expire_date))
            self.parent.destroy()
            sys.exit()
        else:
            tkinter.messagebox.showwarning('注册码错误，请检查')

    def skip(self):
        self.destroy()