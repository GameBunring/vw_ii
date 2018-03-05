import pickle
from tkinter import *
from tkinter.ttk import Treeview
from vw.backend import VWBackend
from vw.vwgui import VWGui

# root = Tk()
# tree = Treeview(root)
# tree['columns'] = ("name", "main", "sub", "type", "zhongwai", "approver", "ID", "year", "phone")
# tree.heading('#0', text='部门')
# tree.heading('name', text='姓名')
# tree.heading('main', text='主车牌')
# tree.heading('sub', text='副车牌')
# tree.heading('type', text='证件类型')
# tree.heading('zhongwai', text='中外')
# tree.heading('approver', text='审批人')
# tree.heading('ID', text='ID')
# tree.heading('year', text='年限')
# tree.heading('phone', text='移动手机')

# tree.insert("", "end", text="haha", values=("2A","2B"))

# tree.pack()

# root.mainloop()
# root.filename = fileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

def main():
    root = Tk()
    root.iconbitmap('icon/vw.ico')
    gui = VWGui(root, _b)
    root.mainloop()

if __name__=="__main__":
    main()