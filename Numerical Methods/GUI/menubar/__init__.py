import tkinter as tk

class MenuBar(tk.Frame):
    def __init__(self,master,menuitems,*args,**kwargs):
        self.menuitems = menuitems
        super().__init__(master,*args,**kwargs)
    def additem(self,item):
        self.menuitems+=[item]
        self.update()