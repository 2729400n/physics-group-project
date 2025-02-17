import importlib.machinery
import importlib.metadata
import importlib.simple
import importlib.util
import tkinter as tk
import tkinter.ttk as ttk
from typing import Iterable

import importlib
import os, os.path as pth

__base__ = pth.abspath(pth.dirname(__file__))

 
 

class IScene(tk.Widget):
    name:str
class TabbedView(ttk.Notebook):
    def __init__(self, master=None,  **kw):
        super().__init__(master,width=640, height=480, **kw)

    def buildTab(self,dir):
        for i in os.listdir(dir) :
            print(i)
            if i.startswith('gui_scene'):
                # print(i)
                ldr = importlib.machinery.SourceFileLoader
                finder =importlib.machinery.FileFinder(dir,(ldr,['.py']))
                mod= finder.find_spec(i.removesuffix('.py'))
                scene_module=importlib.util.module_from_spec(mod)
                importlib.machinery.SourcelessFileLoader.exec_module(scene_module.__loader__,scene_module)
                scene =(scene_module.__dict__.get('scene'))
                if scene != None:
                    curr_scene:IScene = scene(self)
                    self.add(curr_scene,state='normal',sticky='nesw',text=curr_scene.name or '',)
                else:
                    print(scene_module, 'No Scene')
                
        self.pack()

if __name__=='__main__':
    root=tk.Tk()
    tabsolder = TabbedView(root)
    tabsolder.buildTab(pth.abspath(pth.join(__base__,'../scenes')))
    root.mainloop()