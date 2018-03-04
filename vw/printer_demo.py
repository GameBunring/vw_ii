import tkinter as tk
from tkinter.filedialog import askopenfilename
import subprocess
from pprint import pprint
import platform
import sys

def which(program):
    # http://stackoverflow.com/a/377028/3924118
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


class FilePrinterDialog(tk.Toplevel):

    def __init__(self, root, *args, **kwargs):
        tk.Toplevel.__init__(self, root, *args, **kwargs)
        self.root = root

        self.body = tk.Frame(self, bg="lightblue")
        self.body.pack(expand=True, fill="both")

        self.title_frame = tk.Frame(self.body, pady=5)
        self.title_frame.pack(fill="both", pady=(15, 5))

        self.title = tk.Label(self.title_frame,  text="Let's print!")
        self.title.pack(fill="x")

        # Current selected printer of your system
        self.system_default_destination = self._find_system_default_destination()

        # Finds printer names
        self.printers_names = self._find_printers_names()

        self.selected_file = None  # To hold the selected file's name
        self.data_bytes = None  # Bytes read from the selected file to print
        self.selected_printer = None  # Hols name of selected printer

        # Display them
        self.printers_frame = tk.Frame(self.body, bg="lightblue", padx=10, pady=10)
        self.printers_frame.pack(expand=True, fill="both")
        self._display_printers()

        self.bottom_frame = tk.Frame(self.body, pady=5)
        self.bottom_frame.pack(fill="both", pady=(5, 16))
        self.open_file_chooser = tk.Button(self.bottom_frame,
                                           text="Open file chooser",
                                           command=self._select_file)
        self.open_file_chooser.pack(side="left", padx=10)

        self.print_file = tk.Button(self.bottom_frame,
                                           text="Print",
                                           command=self._print_selected_file)
        self.print_file.pack(side="right", padx=10)


        self._make_modal()

    def _read_file(self):
        # NOT USED!
        if not self.selected_file:
            raise ValueError("No file chosen")
        with open(self.selected_file, "rb") as in_file: # opening for [r]eading as [b]inary
            return in_file.read() # if you only wanted to read 512 bytes, do .read(512)

    def _print_selected_file(self):
        if not self.selected_file:
            print("No file selected yet!")
        else:
            subprocess.call(["lpr", self.selected_file])

    def _select_file(self):
        self.selected_file = askopenfilename(title = "Choose file to print")
        print(self.selected_file)

    def _on_listbox_selection(self, event):
        self.selected_printer = self._find_current_selected_printer()

        # Sets the printer on your system
        subprocess.call(["lpoptions", "-d", self.selected_printer])
        print("Selected printer:", self.selected_printer)

    def _find_current_selected_printer(self):
        curselection = self.listbox.curselection()
        if len(curselection) > 0:
            return self.listbox.get(curselection[0])   
        else:
            return None

    def _display_printers(self):
        self.scrollbar = tk.Scrollbar(self.printers_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(self.printers_frame,
                                  yscrollcommand=self.scrollbar.set,
                                  selectbackground="yellow",
                                  selectmode="single",
                                  height=6)

        for printer_name in self.printers_names:
            self.listbox.insert("end", printer_name)

        # Keep track of selected listbox
        self.listbox.bind("<<ListboxSelect>>", self._on_listbox_selection)

        # Sets first listbox as selected
        self.listbox.select_set(0) # Sets focus
        self.listbox.event_generate("<<ListboxSelect>>")

        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.listbox.yview)

    def _find_system_default_destination(self):
        return subprocess.getoutput("lpstat -d").split(": ")[1]

    def _find_printers_names(self):
        # Command to obtain printer names based on: https://superuser.com/a/1016825/317323
        return subprocess.getoutput("lpstat -a | awk '{print $1}'").split("\n")

    def _make_modal(self):
        # Makes the window modal
        self.transient(self.root)
        self.grab_set()
        self.wait_window(self)


if __name__ == "__main__":
    if not which("lpoptions") or not which("lpr") or not which("awk") or not which("lpstat"):        
        sys.stderr.write("Requirements: lopotions, lpr, lpstat and awk not satisfied")
    else:
        root = tk.Tk()
        opener = tk.Button(root, text="Open printer chooser", command=lambda: FilePrinterDialog(root))
        opener.pack()
        root.mainloop()
