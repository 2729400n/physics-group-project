import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.backends.backend_tkagg as tkagg
import matplotlib.backend_managers as bmans
import matplotlib.backend_tools as btools
import matplotlib.backend_bases as bb

class ResultsScene(ttk.Frame):
    name='Results'
    def __init__(self,master=None,*args,**kwargs):
        
        super().__init__(master,*args,text='Results',**kwargs)
        self.mainFrame:'ttk.Frame|tk.Frame|tk.LabelFrame' = None
        self.mainwind_id:int=0
        self.scrollX:'ttk.Scrollbar|tk.Scrollbar' = None
        self.scrollY:'ttk.Scrollbar|tk.Scrollbar' = None
        self.setupFrame()
    
    def _addButtons(self):
        self.obutton = ttk.Button(master=self.mainFrame,text='Open')
        self.obutton.pack()
    
    def _addTextLabels(self):
        pass
    
    def setupFrame(self):
        self.mainWindowCanvas = tk.Canvas(self)
        self.mainWindowCanvas.pack()
        
        self.mainFrame = ttk.Frame(self.mainWindowCanvas)
        self.mainFrame.pack(fill=tk.BOTH,expand=True)
        
        
        self.mainwind_id=self.mainWindowCanvas.create_window(0,0,anchor=tk.NW,window=self)
        
        self.scrollY = ttk.Scrollbar(self,orient='vertical',command=self.mainWindowCanvas.yview)
        self.scrollX = ttk.Scrollbar(self,orient='horizontal',command=self.mainWindowCanvas.xview)
        
        self.scrollX.pack(side=tk.BOTTOM,fill=tk.X)
        self.scrollY.pack(side=tk.RIGHT,fill=tk.Y)
        bb.
        
        self._addButtons()

        
scene = ResultsScene

if __name__=='__main__':
    root  =tk.Tk()
    root.wm_geometry('640x480')
    frame = tk.LabelFrame(root,text='SomeLabel',height=480,width=640)
    frame.pack()
    root.mainloop()