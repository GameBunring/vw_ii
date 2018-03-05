import pickle
from tkinter import *
import tkinter
from tkinter.ttk import Treeview
from vw.backend import VWBackend
from vw.vwactivate import VWActivate
# from vw.vwgui import VWGui
from datetime import date, timedelta

def main():
    root = Tk()
    root.iconbitmap('icon/vw.ico')

    expire_date = pickle.load(open('tcl/time', 'rb'))
    expire_dates = (expire_date.year, expire_date.month, expire_date.day)

    today = date.today()
    if today < expire_date - timedelta(days=30):
        pass
    elif today < expire_date + timedelta(days=30):
        VWActivate(root, expire_dates[0], expire_dates[1]， 1)
    else:
        VWActivate(root, expire_dates[0], expire_dates[1]， -1)
    
    if today >= expire_date + timedelta(days=30):
        tkinter.messagebox.showerror('软件已过期，请注册后使用')
        root.destroy()
        sys.exit()
             
    gui = VWGui(root)
    root.mainloop()

if __name__=="__main__":
   # main()
   expire_day = date(year=2018, month=2, day=26)
   pickle.dump(expire_day, open('tcl/time', 'wb'))
   print(status())
   

