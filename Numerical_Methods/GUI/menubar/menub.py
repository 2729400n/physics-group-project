import tkinter as tk
from typing import Iterable

class MenuBar(tk.Frame):
    def __init__(self,master, menuitems:'Iterable[MenuItem]',*args,**kwargs):
        self._item_names=[]
        for i in menuitems:
            self._item_names += [i]
            
        super().__init__(master,*args,**kwargs)
    def additem(self,item):
        self.menuitems+=[item]

from . import MenuItem


class NavBar(MenuBar):
    def additem(self, item:MenuItem):
        super().additem(item)
        item._add_to_Menu(self,self.change_scene)
    def change_scene(self,item):
        masterFrame = self.master
        masterFrame.stage