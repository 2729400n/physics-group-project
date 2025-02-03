import tkinter.colorchooser as tkcc
import tkinter as tk
import tkinter.commondialog as tkcommon
import tkinter.dnd as tkdnd
import tkinter.filedialog as tkfd
import tkinter.font as tkfont
import tkinter.messagebox as tkmb
import tkinter.dialog as tkdiag
import tkinter.ttk as ttk
import tkinter.scrolledtext as tksrolltxt


class NumericalDisplay(tk.Widget):

    def _on_submit(self, event):
        pass
    
    def __init__(self, master=None, *args,**kw):
        tk.Widget.__init__(self, master, 'numericaldisplay',*args, **kw)
        self.bind('<Configure>', self._on_configure)

root = tk.Tk()
tk.StringVar(root.master, value='Numerical Solver')
tk.Label(root.master, text='Numerical Solver').pack()
root.mainloop()