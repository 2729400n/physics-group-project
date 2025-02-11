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

# from .menubar import MenuBar

class NumericalDisplay(tk.Tk):

    def decorateWindow(self):
        self.wm_geometry('640x480+0+0')
        self.title('Eletrostatic Project')
    
    def populateWindow(self):
        pass
    
    def __init__(self, master=None, baseName = None, className = "Tk", useTk = True, sync = False, use = None,**kw):
        
        tk.Tk.__init__(self, None, baseName,className=className,useTk=useTk,sync=sync,use=use,**kw)
        self.decorateWindow()
        self.populateWindow()
        self.update()

class DefaultNumericalDisplay(NumericalDisplay):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

    def setupMenuBar(self):
        self.winfo_toplevel().option_add('*tearOff', False)
        self.mbar = tk.Menu(self)
        
        # A File Menu
        self.file_menu = tk.Menu(self.mbar,name='file_menu')
        self.mbar.add_cascade(menu=self.file_menu,label='File')
        self.mbar.add_separator()
        
        self.edit_menu = tk.Menu(self.mbar,name='edit_menu')
        self.mbar.add_cascade(menu=self.edit_menu,label='Edit')
        self['menu'] = self.mbar
        
    def populateWindow(self):
        self.setupMenuBar()
        
        # self.mbar.grid(in_=self,column=0,row=0,sticky='w',ipadx=4)
        # self.mbar.grid_columnconfigure(-1,weight=1)
        tk.Frame(self,height=480,width=self.winfo_width()-2,padx=2,pady=2)
        
            
def testProd():
    import sys
    root = DefaultNumericalDisplay()
    print(root.mbar,file=sys.stderr)
    root.mainloop()

if __name__=='__main__':
    testProd()