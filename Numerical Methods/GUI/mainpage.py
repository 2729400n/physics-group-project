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


class NumericalDisplay(tk.Tk,tk.Wm):

    def decorateWindow(self):
        self.wm_geometry('640x480+0+0')
        self.title('Eletrostatic Project')
    
    def __init__(self, master=None, *args,**kw):
        
        tk.Tk.__init__(self, None, 'numericaldisplay',*args, **kw)
        self.decorateWindow()

root = NumericalDisplay()
root.mainloop()