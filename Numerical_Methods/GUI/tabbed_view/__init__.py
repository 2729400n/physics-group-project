import importlib.machinery
import importlib.util
import tkinter as tk
import tkinter.ttk as ttk
from typing import Iterable

import importlib

mod :importlib.machinery.ModuleSpec = importlib.util.spec_from_file_location()
mod.loader.load_module()
def buildTab(dir):
    tk.Tk()
    nb=ttk.Notebook(width=640,height=480)
    mf=tk.Frame(nb,width=640,height=480)
    nb.add(mf,state='normal',sticky='nesw',text='mainFrame',)
    nb.pack()
    tk.mainloop()

if __name__=='__main__':
    buildTab()