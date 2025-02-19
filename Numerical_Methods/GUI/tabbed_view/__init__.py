import importlib.machinery
import importlib.metadata
import importlib.simple
import importlib.util
from importlib.machinery import ModuleSpec,SourceFileLoader,PathFinder
from importlib.util import find_spec,module_from_spec

import tkinter as tk
import tkinter.ttk as ttk
from typing import Iterable

import importlib
import os, os.path as pth
import sys


__base__ = pth.abspath(pth.dirname(__file__))
__base_package__ = pth.abspath(pth.join(__base__,'..','..'))



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
                # finder =importlib.machinery.FileFinder(dir,(ldr,['.py']))
                
                # mod= finder.find_spec(i.removesuffix('.py'))
                modname =f'Numerical_Methods.GUI.scenes.{i.removesuffix('.py')}'
                modorigin = pth.join(dir,i)
                mod =ModuleSpec(modname,origin=modorigin,loader=SourceFileLoader(modname,modorigin),is_package=False)
                # mod.name=f'{i.removesuffix('.py')}'
                scene_module=importlib.util.module_from_spec(mod)
                scene_module.__file__ = modorigin
                importlib.machinery.SourcelessFileLoader.exec_module(scene_module.__loader__,scene_module)
                scene =(scene_module.__dict__.get('scene'))
                if scene != None:
                    curr_scene:IScene = scene(self)
                    self.add(curr_scene,state='normal',sticky='nesw',text=curr_scene.name or '',)
                    
                else:
                    print(scene_module, 'No Scene')
        self.bind('<Configure>',self.resize_subviews,'+')
    def resize_subviews(self,evt:'tk.Event[tk.Frame]'):
        
        print(evt.type,evt.width,evt.height)
        if(evt.type == 22):
            tabs:'list[tk.Wm|tk.Tk|tk.Toplevel|tk.Frame]' = self.tabs()
            tabs = [] if tabs is None else tabs
            


if __name__=='__main__':
    root=tk.Tk()
    tabsolder = TabbedView(root)
    tabsolder.buildTab(pth.abspath(pth.join(__base__,'../scenes')))
    root.mainloop()