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

import tkinter.dnd as dnd
from ...utils.naming import slugify

__base__ = pth.abspath(pth.dirname(__file__))
__base_package__ = pth.abspath(pth.join(__base__,'..','..'))



class IScene(tk.Widget):
    name:str
class TabbedView(ttk.Notebook):
    def __init__(self, master=None,  **kw):
        super().__init__(master,width=640, height=480, **kw)
        self.loaded_scenes={}
        

    def buildTab(self,dir):
        k=0
        for i in os.listdir(dir) :
            print(i)
            if i.startswith('gui_scene'):
                
                ldr = importlib.machinery.SourceFileLoader
                
                modname =f'Numerical_Methods.GUI.scenes.{i.removesuffix('.py')}'
                modorigin = pth.join(dir,i)
                mod =ModuleSpec(modname,origin=modorigin,loader=SourceFileLoader(modname,modorigin),is_package=False)
                
                scene_module=importlib.util.module_from_spec(mod)
                scene_module.__file__ = modorigin
                importlib.machinery.SourcelessFileLoader.exec_module(scene_module.__loader__,scene_module)
                scene =(scene_module.__dict__.get('scene'))
                if scene != None:
                    k+=1
                    curr_scene:IScene = scene(self)
                    try: 
                        text = curr_scene.__getattribute__('name')
                    except AttributeError:
                        text = f'Tab-{k}'
                    except Exception as e:
                        print(e)
                        raise e
                    if text in self.loaded_scenes:
                        text = f'Tab-{k}'
                    
                    self.loaded_scenes.update({text:curr_scene})
                    
                else:
                    print(scene_module, 'No Scene')
                    
        
        for i in self.loaded_scenes:
            self.add(self.loaded_scenes[i],state='normal',sticky='nesw',text=i)
        
        self.bind('<Button-1>',self.resize_subviews,'+')
    
    
    def dnd_accept(self,*args,**kwargs):
        print('dnd_accept',args,kwargs)
    
    def dnd_enter(self,*args,**kwargs):
        print('dnd_enter',args,kwargs)
    
    def dnd_leave(self,*args,**kwargs):
        print('dnd_leave',args,kwargs)
    
    def dnd_motion(self,*args,**kwargs):
        print('dnd_motion',args,kwargs)
    
    def dnd_drop(self,*args,**kwargs):
        print('dnd_drop',args,kwargs)

    def dnd_commit(self,*args,**kwargs):
        print('dnd_commit',args,kwargs)    
    
    def dnd_end(self,*args,**kwargs):
        print('dnd_end',args,kwargs)
    def resize_subviews(self,evt:'tk.Event[tk.Frame]'):
        try:
            tabindex = self.index(f'@{evt.x},{evt.y}')
            print('identify',tabindex)
            tab=self.tab(tabindex)
            print(tab,tab.__class__)
            print(self.tab(0))
            hndler = dnd.dnd_start(self,event=evt)
        except:
            return
            


if __name__=='__main__':
    root=tk.Tk()
    tabsolder = TabbedView(root)
    dndEvent = tk.Event()
    dndEvent.widget = tabsolder 
    tabsolder.buildTab(pth.abspath(pth.join(__base__,'../scenes')))
    root.mainloop()