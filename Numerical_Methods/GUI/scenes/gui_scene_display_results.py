import tkinter as tk
import tkinter.ttk as ttk

class ResultsScene(tk.LabelFrame):
    def __init__(self,master=None,*args,**kwargs):
        
        super().__init__(master,*args,text='Results',**kwargs)
    
    def _addButtons(self):
        pass
    
    def _addTextLabels(self):
        pass
    
    def setupFrame(self):
        self.button = tk.Button(self,width=50,height=75,text="Lol")
        self.button.pack()
    def resize(self,width,height):
        self.config(width=width,height=height)
    def display(self):
        self.pack()
scene = ResultsScene
if __name__=='__main__':
    root  =tk.Tk()
    root.wm_geometry('640x480')
    frame = tk.LabelFrame(root,text='SomeLabel',height=480,width=640)
    frame.pack()
    root.mainloop()