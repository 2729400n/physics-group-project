import os
import os.path as pth
import tkinter as tk
import tkinter.ttk as ttk

from ... import Boundaries as tasks_module
from .. import py_iface

import matplotlib.backend_tools as mb_tools
import matplotlib.backend_managers as mb_managers
import matplotlib.backends.backend_tkagg as mb_tkagg
import matplotlib.figure

import numpy as np

__base__ = pth.abspath(pth.dirname(__file__))


class TasksFrame(tk.Frame):
    name = 'TaskSolver'

    def __init__(self, master=None, *args, **kwargs):

        super().__init__(master)
        self.taskMap: dict = None
        self.current_task = None
        self.createWidgets()
        self.propagate(True)

    def load_Tasks(self):
        self.taskMap = taskMap = self.controlSets = dict(
        ) if self.taskMap is None else self.taskMap
        print(self._heatmap)
        for task in tasks_module.tasks:
            curr_task: tasks_module.Task = task()
            taskMap[curr_task.name] = curr_task

    def createWidgets(self):

        # Create The Figure
        self._heatmap = matplotlib.figure.Figure(
            figsize=(3, 3), dpi=64, tight_layout=True)

        # Create A label Frame to hold ListBox
        labelframe = tk.LabelFrame(self)
        labelframe.pack(fill=tk.BOTH, expand=False,
                        side=tk.LEFT, padx=5, pady=5)
        labelframe.propagate(True)

        # Create a side view to hold canvas and options
        sideView = self.SideView = ttk.Frame(self)

        # Load tasks into a list of task
        self.load_Tasks()

        self.Iframe: 'ttk.Frame|tk.Frame|tk.LabelFrame' = ttk.Frame(sideView)
        Iframe = self.Iframe
        Iframe.pack(fill=tk.X, expand=True, side=tk.TOP,
                    padx=5, pady=5, anchor=tk.NW)
        Iframe.propagate(True)

        self.__innerFrame = None

        self.__canvas_view = canvas_view = tk.Frame(sideView)
        self._axes = None
        self._display = mb_tkagg.FigureCanvasTkAgg(
            self._heatmap, master=canvas_view)
        self._canvas = self._display.get_tk_widget()
        self._canvas.pack(fill=tk.BOTH, expand=True,
                          side=tk.BOTTOM, padx=5, pady=5, anchor=tk.SW)
        self._display.draw()
        canvas_view.pack(fill=tk.BOTH, expand=True,
                         side=tk.BOTTOM, padx=5, pady=5, anchor=tk.SW)
        canvas_view.propagate(False)

        sideView.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT,
                      padx=5, pady=5, anchor=tk.NE)

        # Create root label
        L1 = tk.Label(self, text='Solver', justify=tk.LEFT)
        L1.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5, before=labelframe)
        L1.propagate(True)

        # Create LabelFrames Childeren

        taskList = self.taskList = tk.Listbox(labelframe, selectmode=tk.SINGLE)
        taskList.insert(0, *self.taskMap)
        taskList.bind('<<ListboxSelect>>', self.selected_cmap, add='+')
        taskList.bind('<KeyPress-Up>', self.handle_keys, '+')
        taskList.bind('<KeyPress-Down>', self.handle_keys, '+')
        taskList.selection_handle(self.selected_cmap)
        self.current_sel = taskList.get(0, 0)
        taskList.pack(fill=tk.Y, expand=True, side=tk.TOP,
                      padx=5, pady=5, anchor=tk.NW)
        taskList.propagate(True)
        self.key = None

        self.inFrame_Window = None

        self.select_button = sel_button = tk.Button(
            labelframe, text='Select Task', command=self.submit)
        sel_button.pack(fill=tk.BOTH, expand=False,
                        side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        sel_button.propagate(True)

        pop_out_canvas_button = ttk.Button(
            labelframe, command=self.pop_out_canvas, text='Pop Out Canvas')
        pop_out_canvas_button.pack()

        pop_out_canvas_button = ttk.Button(
            labelframe, command=self.reload, text='Reload Tasks')
        pop_out_canvas_button.pack()

        self.test_grid, _ = np.mgrid[:1024, :100]

    def reload(self):
        self.load_Tasks()
        self.taskList.delete(0, tk.END)
        self.taskList.insert(0, *self.taskMap)

    def pop_out_canvas(self):
        # root = self.winfo_toplevel()
        nroot = tk.Toplevel(self,)
        canvas_view = tk.Frame(nroot)
        _display = mb_tkagg.FigureCanvasTkAgg(
            self.current_task.figure, master=canvas_view)
        # _display.new_manager(self.current_task.figure,0)
        _canvas = _display.get_tk_widget()
        _canvas.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM,
                     padx=5, pady=5, anchor=tk.SW)
        _display.draw()
        # _display.new_timer(300,[(lambda:_display.draw())])
        canvas_view.pack(fill=tk.BOTH, expand=True,
                         side=tk.BOTTOM, padx=5, pady=5, anchor=tk.SW)
        # canvas_view.propagate(True)

    def selected_cmap(self, *args):
        index: tuple = self.taskList.curselection()

        if (index.__len__() == 0):
            return

        key: tasks_module.Task = self.taskList.get(index[0])
        print(key)

        if self.key != key:
            self._display.blit()
            self._heatmap.clf()
            curr_task: tasks_module.Task = self.taskMap[key]
            self.current_task = curr_task
            self._display.figure.tight_layout()

            curr_task.figure.draw_without_rendering()
            w, h = self._display.figure.get_size_inches()
            self._display.new_manager(self.current_task.figure, 0)
            self._display.figure = self.current_task.figure
            self._display.figure.set_size_inches(w, h)
            self._display.renderer.clear()
            self._display.draw()
            print(curr_task)

    def handle_keys(self, evt: 'tk.Event[tk.Listbox]', *args, **kwargs):
        index: tuple = self.taskList.curselection()
        print(evt)
        if (index.__len__() == 0):
            return
        index = index[0]

        if (evt.keysym == 'Up'):
            new_index = max(0, (index - 1) % self.taskList.size())
            self.taskList.selection_clear(index)
            self.taskList.selection_set(new_index)
            self.taskList.activate(new_index)
            self.taskList.event_generate('<<ListboxSelect>>')

        elif (evt.keysym == 'Down'):
            new_index = (index + 1) % self.taskList.size()
            self.taskList.selection_clear(index)
            self.taskList.selection_set(new_index)
            self.taskList.activate(new_index)
            self.taskList.event_generate('<<ListboxSelect>>')

    def submit(self, *args):
        print(self.key)
        if self.current_task is None:
            return
        if self.__innerFrame is not None:
            self.__innerFrame.destroy()
        self.__innerFrame = ttk.Frame(self.Iframe)
        self.__innerFrame.pack(fill=tk.BOTH, expand=True,
                               side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        if len(self.current_task.exposed_methods) == 0:

            py_iface.makeFunctionCallable(
                self.current_task.setup, self.__innerFrame, classType=True,
                instance=self.current_task)

            py_iface.makeFunctionCallable(
                self.current_task.run, self.__innerFrame, classType=True,
                instance=self.current_task)

            py_iface.makeFunctionCallable(
                self.current_task._show_Efield, self.__innerFrame,
                classType=True, instance=self.current_task)
        else:
            for i in self.current_task.exposed_methods:
                py_iface.makeFunctionCallable(
                    i, self.__innerFrame, classType=True,
                    instance=self.current_task)

        print(args)


scene = TasksFrame
