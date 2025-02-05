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

from .menubar import MenuBar

class NumericalDisplay(tk.Tk,tk.Wm):

    def decorateWindow(self):
        self.wm_geometry('640x480+0+0')
        self.title('Eletrostatic Project')
    
    def populateWindow(self):
        pass
    
    def __init__(self, master=None, *args,**kw):
        
        tk.Tk.__init__(self, None, 'numericaldisplay',*args, **kw)
        self.decorateWindow()

class DefaultNumericalDisplay(tk.Tk,tk.Wm):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

    def populateWindow(self):
        from . import scenes
        self.mbar = MenuBar(self,scenes)
        self.mbar.grid(in_=self,column=0,row=0,sticky=True,ipadx=4)
        self.mbar.grid_columnconfigure(0,weight=1)
        tk.Frame(self,height=480,width=self.winfo_width()-2,padx=2,pady=2)
        
            
def testProd():
    root = NumericalDisplay()
    root.mainloop()

if __name__=='__main__':
    testProd()