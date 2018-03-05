import tkinter
from tkinter import *
from datetime import date, timedelta
import pickle
import sys
from vw.vwgui import VWGui
import hashlib

class VWActivate(tkinter.Frame):
    def __init__(self, parent, expire_date, status):
        _style = ttk.Style()
        _style.theme_use('alt')
        _style.configure('TFrame', background='maroon')
        Frame.__init__(self, parent, background='#000000')
        self.parent = parent
        self.parent.minsize(300, 80)
        self.parent.geometry("300x80+300+300")
        self.expire_date = expire_date
        self.dead_date = expire_date + timedelta(days=30)
        self.status = status
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.title("续期请求")

        self.label = Label(self.parent, text="软件在{}到期，请在{}前完成续期，\n过期将无法使用。谢谢！".\
            format(self.expire_date, self.dead_date, padx=5))
        self.register_label = Label(self.parent, text='注册码', padx=5)
        self.register_entry = Entry()
        self.register_button = Button(text='注册', command=self.activate)
        self.skip_button = Button(text='跳过', command=self.skip)

        if status == 1:
            self.skip_button.config(state='active')
        elif status == -1:
            self.skip_button.config(state='disabled')

        self.label.grid(row=0, columnspan=4)
        self.register_label.grid(row=1, column=0)
        self.register_entry.grid(row=1, column=1, sticky='we', padx=5)
        self.register_button.grid(row=1, column=2)
        self.skip_button.grid(row=1, column=3)

    def activate(self):
        input_code = self.register_entry.get().strip()
        if len(input_code) < 10:
            tkinter.messagebox.showwarning('注册码错误', '注册码位数有误，请检查')
            return
        if input_code in hashlib.md5(str.encode('xddd{}'.format(self.expire_date.year))).hexdigest():    
            new_expire_date = date(self.expire_date.year + 1, self.expire_date.month, self.expire_date.day)
            pickle.dump(new_expire_date, open('ttime', 'wb'))
            tkinter.messagebox.showinfo('注册成功', '注册成功，感谢您续期！软件使用期更新为{}！'.format(new_expire_date))
            self.destroy()
            self.parent.destroy()
            VWGui(Tk())
        else:
            tkinter.messagebox.showwarning('注册码错误', '注册码错误，请检查')

    def skip(self):
        self.destroy()
        self.parent.destroy()
        VWGui(Tk())