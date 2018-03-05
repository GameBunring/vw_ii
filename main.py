import pickle
from tkinter import *
import tkinter
from tkinter.ttk import Treeview
from vw.backend import VWBackend
from vw.vwactivate import VWActivate
from vw.vwgui import VWGui
from datetime import date, timedelta

def main():
    root = Tk()
    root.iconbitmap('icon/vw.ico')

    expire_date = pickle.load(open('ttime', 'rb'))

    today = date.today()

    if today < expire_date - timedelta(days=30):
        VWGui(root)

    elif today < expire_date + timedelta(days=30):
        VWActivate(root, expire_date, 1)

    else:
        VWActivate(root, expire_date, -1)
             
    root.mainloop()

if __name__=="__main__":
   # main()
   expire_day = date(year=2018, month=3, day=12)
   pickle.dump(expire_day, open('ttime', 'wb'))
   main()
   

