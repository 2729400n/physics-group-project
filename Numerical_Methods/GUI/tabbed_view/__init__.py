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

 



def buildTab(dir):
    tk.Tk()
    nb=ttk.Notebook(width=640,height=480)
    for i in os.listdir(dir) :
        # print(i)
        if i.startswith('gui_scene'):
            # print(i)
            ldr = importlib.machinery.SourceFileLoader
            finder =importlib.machinery.FileFinder(dir,(ldr,['.py']))
            mod= finder.find_spec(i.removesuffix('.py'))
            scene_module=importlib.util.module_from_spec(mod)
            importlib.machinery.SourcelessFileLoader.exec_module(scene_module.__loader__,scene_module)
            scene =(scene_module.__dict__.get('scene'))
            if scene != None:
                curr_scene = scene(nb)
                nb.add(curr_scene,state='normal',sticky='nesw',text='mainFrame',)
                
    
    # mf=tk.Frame(nb,width=640,height=480)
    # nb.add(mf,state='normal',sticky='nesw',text='mainFrame',)
    nb.pack()
    tk.mainloop()

if __name__=='__main__':
    buildTab(pth.abspath(pth.join(__base__,'../scenes')))