import os
import os.path as pth
import tkinter as tk
import tkinter.ttk as ttk

from ... import Boundaries as tasks_module
from .. import py_iface

import matplotlib.backend_tools as mb_tools, matplotlib.backend_managers as mb_managers, matplotlib.backends.backend_tkagg as mb_tkagg
import matplotlib.figure
from ..extended_widgets.realtime_update_figure import RealTimeFigure

import numpy as np

__base__ = pth.abspath(pth.dirname(__file__))

class TasksFrame(tk.Frame):
    name='TaskSolver'
    def __init__(self, master=None,*args,**kwargs):
        
        super().__init__( master)
        self.current_task = None
        self.createWidgets()
        self.propagate(True)
        self.update()
    
    def load_Tasks(self):
        self.taskMap = taskMap = self.controlSets = dict()
        for task in tasks_module.tasks:
           curr_task:tasks_module.Task=task(self._heatmap)
           taskMap[curr_task.name]=curr_task

    
    def createWidgets(self):
        
        # Create root label
        L1 = tk.Label(self, text='Solver',justify=tk.LEFT)
        L1.grid(row=0,sticky='NE',column=0,columnspan=1,)
        L1.grid_propagate(True)
        L1.grid_columnconfigure(0,weight=1)
        
        self._heatmap = matplotlib.figure.Figure(figsize=(3,3),dpi=64,tight_layout=True)
        
        labelframe = tk.LabelFrame(self)
        labelframe.grid(row=1,sticky='NW',padx=5)
        
        self.load_Tasks()
        
        taskList=self.taskList=tk.Listbox(labelframe, selectmode=tk.SINGLE)
        self.Iframe :'ttk.Frame|tk.Frame|tk.LabelFrame'=None
        taskList.insert(0,*self.taskMap)
        taskList.grid(row=1,sticky='NW')
        taskList.grid_propagate(True)
        taskList.bind('<<ListboxSelect>>',self.selected_cmap,add='+')
        taskList.bind('<KeyPress-Up>',self.handle_keys,'+')
        taskList.bind('<KeyPress-Down>',self.handle_keys,'+')
        taskList.selection_handle(self.selected_cmap)
        self.current_sel = taskList.get(0,0)
        self.key = None
        
        
        button = tk.Button(labelframe, text='Select Task', command=self.submit)
        button.grid(row=2,sticky='NW')
        button.grid_propagate(True)
        button.grid_columnconfigure(0)
        
        
        
        self._axes = None
        self._display = mb_tkagg.FigureCanvasTkAgg(self._heatmap,master=self)
        self._canvas=self._display.get_tk_widget()
        self._canvas.grid(row=1,column=1,sticky='NE',padx=5,pady=5)
        self._display.draw()
        
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
            curr_task =self.currnent_task = self.taskMap[key]
            print(curr_task)

            
    
    def handle_keys(self,evt:'tk.Event[tk.Listbox]',*args,**kwargs):
        index:tuple = self.taskList.curselection()
        print(evt)
        if(index.__len__()==0):
            return
        index = index[0]
        
        if(evt.keysym=='Up'):
            new_index =  max(0,(index -1) % self.cmaps.size())
            self.taskList.selection_clear(index)
            self.taskList.selection_set(new_index)
            self.taskList.activate(new_index)
            self.taskList.event_generate('<<ListboxSelect>>')
            
        elif(evt.keysym=='Down'):
            new_index =  (index +1) % self.cmaps.size()
            self.taskList.selection_clear(index)
            self.taskList.selection_set(new_index)
            self.taskList.activate(new_index)
            self.taskList.event_generate('<<ListboxSelect>>')

    def submit(self,*args):
        print(self.key)
        if self.key is None:
            return
        if self.key not in self.file:
            return
        key = self.key
        if(self.current_sel!=key) or (self.cmap is None):
            self.current_sel=key
            self.cmap =  self.file[key]
            print(self.cmap)
           
        print(args)
        
scene = TasksFrame