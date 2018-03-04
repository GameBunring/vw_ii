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
        self.parent.geometry("800x600+100+100")
        self.backend = backend
        self.printer = VWPrinter()
        self.printable_ids = set()
        self.table_values = None
        load = self.backend.load_xls()
        self.columns = (
            ('appartment', '部门'),
            ('name', '姓名'),
            ('main', '主车牌'),
            ('sub', '副车牌'),
            ('type', '证件类型'),
            ('zhongwai', '中外'),
            ('approver', '审批人'),
            ('ID', 'ID'),
            ('year', '年限'),
            ('phone', '移动手机'),
            ('printed', '已打印'),
            ('printdate', '打印时间'),
            ('verified', '已验证')
        )
        self.initialize_user_interface()
        if load:
            tkinter.messagebox.showinfo('车牌重复','{}车牌已存在，请核对信息。或点击“+”添加车牌。'.format(load))

    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type
        items and insert them into the treeview
        """
        self.parent.title("上海大众通行证管理系统 - V1.0")
        #self.parent.grid_rowconfigure(0, weight=1)
        #self.parent.grid_columnconfigure(0, pad=10)
        self.parent.grid_columnconfigure(3, weight=1)
        self.parent.grid_rowconfigure(2, weight=1)
        # self.parent.config(background="lavender")
        # Define the different GUI widgets
        self.search_label = Label(self.parent, text="要查找的姓名/车牌/部门(@月-日)", padx=5)
        self.search_entry = Entry(self.parent)
        # self.dose_label.grid(row=0, column=0, sticky=W)
        self.search_label.grid(row=0, columnspan=3, sticky=W)        
        self.search_entry.grid(row=0, column=3, columnspan=3, sticky=NSEW)
        self.show_printed = BooleanVar()
        c = Checkbutton(self.parent, text="显示已打印的车牌", padx=5, variable=self.show_printed, command=self.search)
        c.grid(row=0, column=6, sticky=W)

        self.submit_button = Button(self.parent, text="查找", command=self.search)
        self.submit_button.grid(row=0, column=7, columnspan=2, sticky=NSEW)
        # self.exit_button = Button(self.parent, text="Exit", command=self.parent.quit)
        # self.exit_button.grid(row=0, column=3, sticky=W)
        # Set the treeview
        self.tree = ttk.Treeview(self.parent, columns=[i[0] for i in self.columns], show="headings")

        def sortby(tree, col, descending):
            """Sort tree contents when a column is clicked on."""
            # grab values to sort
            data = [(tree.set(child, col), child) for child in tree.get_children('')]
            # reorder data
            if col in ('ID', 'year'):
                data[:] = [(int(i[0]), i[1]) for i in data]
            data.sort(reverse=descending)
            for indx, item in enumerate(data):
                tree.move(item[1], '', indx)
            # switch the heading so that it will sort in the opposite direction
            tree.heading(col,
                command=lambda col=col: sortby(tree, col, int(not descending)))

        for (col, trans) in self.columns:
            self.tree.heading(col, text=trans,
                command=lambda c=col: sortby(self.tree, c, 0))
        # self.tree.column('#1', stretch=YES)
        # self.tree.column('#2', stretch=YES)
        # self.tree.column('#0', stretch=YES)
        w_ceil = ttk.Separator()
        w_ceil.grid(row=1, columnspan=9, sticky=EW)
        self.tree.grid(row=2, columnspan=8, sticky=NSEW)
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.grid(column=8, row=2, sticky='NSE')
        hsb.grid(row=3, columnspan=8, sticky='EW')
        self.add_button = Button(text="+", command=self.add_one)
        self.add_button.grid(row=3, column=0, pady=2, padx=1, sticky=W)
        self.treeview = self.tree
        self.tree.bind("<Double-1>", self.on_doubleclick)
        self.tree.tag_configure('verified', background='#ffffff')
        self.tree.tag_configure('unverified', background='#d0d0d0')
        w_bottom = ttk.Separator()
        w_bottom.grid(row=4, columnspan=9, sticky=EW)
        self.verify_button = Button(text="全部验证", command=self.verify, state='disabled')
        self.verify_button.grid(columnspan=1, row=5, sticky=EW)
        self.deverify_button = Button(text="全部解密", command=self.deverify, state='disabled')
        self.deverify_button.grid(column=1, padx=2, row=5, sticky=EW)
        self.print_button = Button(text="打印车牌", command=self.print_one, state='disabled')
        self.print_meta_button = Button(text='打印车牌名', state='disabled', command=self.print_meta)
        self.print_all_meta_button = Button(text='批量打印车牌名', state='disabled', command=self.print_all_meta)
        self.print_all_button = Button(text='批量打印车牌', command=self.print_all, state='disabled')        
        self.print_meta_button.grid(column=4, row=5, sticky=E)
        self.print_all_meta_button.grid(column=6, row=5, sticky=E)
        self.print_button.grid(column=5, row=5, sticky=E)        
        self.print_all_button.grid(column=7, columnspan=2, row=5, sticky=E)
        self.tree.bind("<<TreeviewSelect>>", self.toggle_buttons)
        self.search()
    
    def init_width(self):
        self.tree.column('appartment', width=100)
        self.tree.column('name', width=80)
        self.tree.column('main', width=100)
        self.tree.column('sub', width=100)
        self.tree.column('type', width=90)
        self.tree.column('zhongwai', width=100)
        self.tree.column('approver', width=80)
        self.tree.column('ID', width=40)
        self.tree.column('year', width=70)
        self.tree.column('phone', width=120)
        self.tree.column('printed', width=40)
        self.tree.column('printdate', width=100)
        self.tree.column('verified', width=40)
    
    def add_one(self):
        _id = self.backend.get_min_id()
        ChangeDialog(parent=self, values=None, title='添加车牌', _id=_id)
    
    def print_one(self):
        item = self.tree.selection()
        print(item)
        values = self.tree.item(item[0], "values")
        plates = values[2:4] if values[3] != "None" else [values[2]]
        # _plate_img = PrintDialog.generate_plate_image(plates, values)
        # _plate_img.show()
        # self.backend.set_ids_printed([values[7]])
        # self.search()
        # if plates[1] == "None":
        #     plates = [plates[0]]
        if not item:
            print("No item selected when print!!!")
        else:
            VWPrintDialog(self, (0, plates, values))
    
    def print_all(self):
        # ids = []
        # for child in self.tree.get_children():
        #     values = self.tree.item(child)['values']
        #     # print(values)
        #     if values[-3] == '否':
        #         ids.append(values[-6])
        # print('what happened')
        # values = [self.backend.getvalues_with_id(i) for i in self.printable_ids]
        # print(values)
        if(tkinter.messagebox.askyesno('全部打印','确定要打印这{}个车牌吗?'.format(len(self.table_values)))):
            plates = [(i[2], i[3]) if i[3] else (i[2], ) for i in self.table_values]
            print(plates)
            _plate_imgs = (VWPrintDialog.generate_plate_image(value[2:4] if value[3] else value[2:3], value) \
                for value in self.table_values)
            if self.printer.print_imgs(_plate_imgs):
                self.backend.set_ids_printed([i[7] for i in self.table_values])
                self.search()
            else:
                tkinter.messagebox.showinfo('打印失败', '请重新启动软件或联系管理员')

    def print_all_meta(self):
        # ids = []
        # for child in self.tree.get_children():
        #     values = self.tree.item(child)['values']
        #     # print(values)
        #     if values[-3] == '否':
        #         ids.append(values[-6])
        # values = (self.backend.getvalues_with_id(i) for i in self.printable_ids)
        if(tkinter.messagebox.askyesno('全部打印','确定要打印这{}个车牌名吗?'.format(len(self.table_values)))):
            _meta_imgs = (VWPrintDialog.generate_meta_image(value[:3]) for value in self.table_values)
            self.printer.print_imgs(_meta_imgs)        
    
    def print_meta(self):
        item = self.tree.selection()
        print(item)
        values = self.tree.item(item[0], "values")
        # metas = values[:3]
        # _img = PrintDialog.generate_meta_image(metas)
        # self.backend.set_ids_printed([values[7]])
        #self.search()
        #_img.show()

        # TODO
        if not item:
            print("No item selected when printmeta!!!")
        else:
            VWPrintDialog(self, (1, values))
    
    def toggle_buttons(self, event):
        # print(event)
        # print(self.printable_ids)
        # if self.printable_ids:
        #     self.print_all_button.config(state='normal')
        #     self.print_all_meta_button.config(state='normal')
        # else:
        #     self.print_all_button.config(state='disabled')
        #     self.print_all_meta_button.config(state='disabled')
        _item = self.tree.selection()
        # print(_item)
        # print('toggle')
        # print(_item)  
        if not _item:
            return
        else:
            values = self.tree.item(_item[0], "values")
            verified = self.backend.check_verified(values[7])[0]
            if verified:
                print('1')
                # self.verify_button.config(text='解验', command=self.deverify, state='normal')
                self.print_button.config(state='normal')
                self.print_meta_button.config(state='normal')
            else:
                print('0')
                # self.verify_button.config(text='验证', command=self.verify, state='normal')
                self.print_button.config(state='disabled')
                self.print_meta_button.config(state='disabled')
        # self.verify_button.update()
        # self.print_button.update()
        # self.print_all_button.update()
        # self.print_meta_button.update()
        # self.print_all_meta_button.update()
        pass
        
    def verify(self):
        # item = self.tree.selection()
        # _values = self.tree.item(item[0], "values")
        # _id = _values[7]
        # self.backend.verify_plate(_id)
        
        for child in self.tree.get_children():
            _values = self.tree.item(child)['values']
            _id = _values[7]
            self.backend.verify_plate(_id)
            self.tree.item(child, values=_values[:12] + ['是'], tags=('verified', ))
        
        
        self.print_button.config(state='normal')
        self.print_meta_button.config(state='normal')
        self.print_all_button.config(state='normal')
        self.print_all_meta_button.config(state='normal')
        tkinter.messagebox.showinfo("验证", "列表中的车牌已全部验证")
        self.verify_button.config(state='disabled')
        self.deverify_button.config(state='normal')
        
        # self.verify_button.config(text='解验', command=self.deverify, state='normal')
        
        # self.search()
        # self.treeview.selection_add(item[0])
        # self.printable_ids.add(int(_id))
        
        # self.tree.item(item[0], values=_values[:12] + ('是',))
        # self.toggle_buttons(None)

    def deverify(self):
        # _values = self.tree.item(item[0], "values")
        # _id = _values[7]
        # self.backend.deverify_plate(_id)
        # self.printable_ids.remove(int(_id))
        # self.tree.item(item[0], values=_values[:12] + ['否'])
        # self.toggle_buttons(None)
        for child in self.tree.get_children():
            _values = self.tree.item(child)['values']
            _id = _values[7]
            self.backend.deverify_plate(_id)
            self.tree.item(child, values=_values[:12] + ['否'], tags=('unverified', ))

        self.print_button.config(state='disabled')
        self.print_meta_button.config(state='disabled')
        self.print_all_button.config(state='disabled')
        self.print_all_meta_button.config(state='disabled')
        tkinter.messagebox.showinfo("解密", "列表中的车牌已全部解密")
        self.verify_button.config(state='normal')
        self.deverify_button.config(state='disabled')
        # self.verify_button.config(text='验证', command=self.verify, state='normal')

    def search(self):
        """
        Insertion method.
        """
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        self.init_width()
        print('show printed is {}'.format(self.show_printed.get()))
        date_format, _p_ids, res = self.backend.search(self.search_entry.get(), self.show_printed.get())
        res = [] if not res else res
        self.printable_ids = set(_p_ids) if _p_ids else set()
        print('printable_ids:', self.printable_ids)
        # if self.printable_ids:
        #     self.print_all_button.config(state='normal')
        #     self.print_all_meta_button.config(state='normal')
        # else:
        #     self.print_all_button.config(state='disabled')
        #     self.print_all_meta_button.config(state='disabled')
        if len(self.printable_ids) < len(res):
            self.verify_button.config(state='normal')
            self.deverify_button.config(state='normal' if self.printable_ids else 'disabled')
            self.print_button.config(state='disabled')
            self.print_meta_button.config(state='disabled')
            self.print_all_button.config(state='disabled')
            self.print_all_meta_button.config(state='disabled')
            
        else:
            self.verify_button.config(state='disabled')
            self.deverify_button.config(state='normal' if res else 'disabled')
            # self.print_meta_button.config(state='normal')
            self.print_all_button.config(state='normal' if res else 'disabled')
            self.print_all_meta_button.config(state='normal' if res else 'disabled')

        self.print_button.config(state='disabled')
        self.print_meta_button.config(state='disabled')
        self.print_button.update()
        self.print_all_button.update()
        self.print_meta_button.update()
        self.print_all_meta_button.update()
        if date_format == 1:
            tkinter.messagebox.showinfo('错误的日期格式','日期格式应该是：月-日')
            return
        self.table_values = []
        for r in res:
            r = list(r)
            r[-3] = '是' if r[-3] else '否'
            # r[-1] = '是' if r[-1] else '否'
            self.table_values.append(r)
            if r[-1]:
                r[-1] = '是'
                self.treeview.insert('', 'end', values=r, tags=('verified'))
            else:
                r[-1] = '否'
                self.treeview.insert('', 'end', values=r, tags=('unverified'))

            for indx, val in enumerate(r):
                ilen = tkinter.font.nametofont("TkDefaultFont").measure(str(val))
                # print('{},{}'.format(self.columns[indx], indx))
                if self.tree.column(self.columns[indx][0], width=None) < ilen:
                    self.tree.column(self.columns[indx][0], width=ilen+20)
        
    
    def on_doubleclick(self, event):
        item = self.tree.selection()
        if not item:
            print("No item selected when doubleclicked???")
        else:
            ChangeDialog(self, self.tree.item(item[0], "values")[:-3], '更新信息')
        # dialog = ChangeDialog(self, )


class ChangeDialog():
    def __init__(self, parent, values, title, _id=None):
        self.top = Toplevel(parent)
        self.backend = parent.backend
        self.top.title(title)
        self.parent = parent
        self.entries = []
        for i, (_, label) in enumerate(parent.columns[:-3]):
            l = Label(self.top, text=label)
            l.grid(row=i//2, column=2 if i%2 else 0, sticky=tkinter.W)
            if label == "ID":
                self.id = values[i] if not _id else _id
                e = Label(self.top, text=str(self.id))
            else:
                e = Entry(self.top)
                self.entries.append(e)
                if values:
                    e.insert(END, values[i])
            e.grid(row=i//2, column=3 if i%2 else 1, sticky=tkinter.W)
        if values:
            self.update_button = Button(self.top, text=title, command=self.update)
        else:
            self.update_button = Button(self.top, text=title, command=self.add_plate)
        self.update_button.grid(row=(len(parent.columns)-1)//2+1, column=3, sticky=tkinter.E)


    def update(self):
        entry_list = [i.get() for i in self.entries]
        self.backend.update(entry_list, self.id)
        self.parent.search()
        self.top.destroy()
    
    def add_plate(self):
        entry_list = [i.get() for i in self.entries]
        value_list = entry_list[:7] + [self.id] + entry_list[7:]
        self.backend.add_plate(value_list)
        self.parent.search()
        self.top.destroy()
