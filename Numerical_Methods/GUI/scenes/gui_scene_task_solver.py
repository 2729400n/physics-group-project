import os
import os.path as pth
import tkinter as tk
import tkinter.ttk as ttk

from ... import Boundaries as tasks_module
from .. import py_iface

import matplotlib.backend_tools as mb_tools, matplotlib.backend_managers as mb_managers, matplotlib.backends.backend_tkagg as mb_tkagg
import matplotlib.figure
import matplotlib.animation as animation
from ..extended_widgets.realtime_update_figure import RealTimeFigure

import numpy as np

__base__ = pth.abspath(pth.dirname(__file__))

class TasksFrame(tk.Frame):
    name='TaskSolver'
    def __init__(self, master=None,*args,**kwargs):
        
        super().__init__( master)
        self.taskMap:dict=None
        self.current_task = None
        self.createWidgets()
        self.propagate(True)
        self.update()
    
    def load_Tasks(self):
        self.taskMap = taskMap = self.controlSets = dict() if self.taskMap is None else self.taskMap
        print(self._heatmap)
        for task in tasks_module.tasks:
           curr_task:tasks_module.Task=task()
           taskMap[curr_task.name]=curr_task

    
    
    def createWidgets(self):
        
        
        
        self._heatmap = matplotlib.figure.Figure(figsize=(3,3),dpi=64,tight_layout=True)
        
        labelframe = tk.LabelFrame(self)
        labelframe.pack(fill=tk.BOTH,expand=False,side=tk.LEFT,padx=5,pady=5)
        labelframe.propagate(True)
        
        self.load_Tasks()
        
        sideView = self.SideView = ttk.Frame(self)
        
        self.Iframe :'ttk.Frame|tk.Frame|tk.LabelFrame'=ttk.Frame(sideView)
        Iframe  = self.Iframe
        Iframe.pack(fill=tk.X,expand=True,side=tk.TOP,padx=5,pady=5,anchor=tk.NW)
        Iframe.propagate(True)
        
        self.__innerFrame = None
        
        
        self._axes = None
        self._display = mb_tkagg.FigureCanvasTkAgg(self._heatmap,master=sideView)
        self._canvas=self._display.get_tk_widget()
        self._canvas.pack(fill=tk.BOTH,expand=True,side=tk.BOTTOM,padx=5,pady=5,anchor=tk.SW)
        self._display.draw()
        
        sideView.pack(fill=tk.BOTH,expand=True,side=tk.RIGHT,padx=5,pady=5,anchor=tk.NE)
        
        # Create root label
        L1 = tk.Label(self, text='Solver',justify=tk.LEFT)
        L1.pack(fill=tk.X,side=tk.TOP,padx=5,pady=5,before=labelframe)
        L1.propagate(True)
        
        
        # Create LalebFrames Childeren
         
        taskList=self.taskList=tk.Listbox(labelframe, selectmode=tk.SINGLE)
        taskList.insert(0,*self.taskMap)
        taskList.bind('<<ListboxSelect>>',self.selected_cmap,add='+')
        taskList.bind('<KeyPress-Up>',self.handle_keys,'+')
        taskList.bind('<KeyPress-Down>',self.handle_keys,'+')
        taskList.selection_handle(self.selected_cmap)
        self.current_sel = taskList.get(0,0)
        taskList.pack(fill=tk.Y,expand=True,side=tk.TOP,padx=5,pady=5,anchor=tk.NW)
        taskList.propagate(True)
        self.key = None
        
        
        button = tk.Button(labelframe, text='Select Task', command=self.submit)
        button.pack(fill=tk.BOTH,expand=False,side=tk.TOP,padx=5,pady=5,anchor=tk.NW)
        button.propagate(True)
        self.test_grid, _ = np.mgrid[:1024,:100]
        


    def selected_cmap(self,*args):
        index:tuple = self.taskList.curselection()
        
        if(index.__len__()==0):
            return
        
        key:tasks_module.Task =self.taskList.get(index[0])
        print(key)
        
        if self.key!=key:
            self._display.blit()
            self._heatmap.clf()
            curr_task:tasks_module.Task = self.taskMap[key]
            self.current_task = curr_task
            self._display.figure.tight_layout()
            
            curr_task.figure.draw_without_rendering()
            w,h = self._display.figure.get_size_inches()
            self._display.figure = self.current_task.figure
            self._display.figure.set_size_inches(w,h)
            self._display.renderer.clear()
            self._display.draw()
            print(curr_task)

            
    
    def handle_keys(self,evt:'tk.Event[tk.Listbox]',*args,**kwargs):
        index:tuple = self.taskList.curselection()
        print(evt)
        if(index.__len__()==0):
            return
        index = index[0]
        
        if(evt.keysym=='Up'):
            new_index =  max(0,(index -1) % self.taskList.size())
            self.taskList.selection_clear(index)
            self.taskList.selection_set(new_index)
            self.taskList.activate(new_index)
            self.taskList.event_generate('<<ListboxSelect>>')
            
        elif(evt.keysym=='Down'):
            new_index =  (index +1) % self.taskList.size()
            self.taskList.selection_clear(index)
            self.taskList.selection_set(new_index)
            self.taskList.activate(new_index)
            self.taskList.event_generate('<<ListboxSelect>>')

    def submit(self,*args):
        print(self.key)
        if self.current_task is None:
            return
        if self.__innerFrame is not None:
            self.__innerFrame.destroy()
        self.__innerFrame = ttk.Frame(self.Iframe)
        self.__innerFrame.pack(fill=tk.BOTH,expand=True,side=tk.TOP,padx=5,pady=5,anchor=tk.NW)
        py_iface.makeFunctionCallable(self.current_task.setup,self.__innerFrame,classType=True,instance=self.current_task)
        py_iface.makeFunctionCallable(self.current_task.run,self.__innerFrame,classType=True,instance=self.current_task)
        py_iface.makeFunctionCallable(self.current_task._show_Efield,self.__innerFrame,classType=True,instance=self.current_task)
        
        print(args)
        
scene = TasksFrame