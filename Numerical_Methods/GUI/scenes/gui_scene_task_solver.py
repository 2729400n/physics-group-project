import os
import os.path as pth
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox_

from ...utils import nfile_io

from ... import Boundaries as tasks_module
from .. import py_iface

import matplotlib.backends.backend_tkagg as mb_tkagg
import matplotlib.figure
import numpy as np

__base__ = pth.abspath(pth.dirname(__file__))


class TasksFrame(tk.Frame):
    name = "TaskSolver"

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master)

        self.taskMap: dict = None
        self.current_task = None
        self.stores: dict[str, tk.Variable] = {}
        self._to_clear = {}
        self.WindowID: int = None
        self.canvasEntry: tk.Canvas = None
        self.inner_frame: ttk.Frame = None

        self._heatmap = matplotlib.figure.Figure(figsize=(3, 3), dpi=64, tight_layout=True)

        self.createWidgets()

    def load_Tasks(self):
        """Load available tasks into taskMap."""
        if self.taskMap is None:
            self.taskMap = {}

        for task in tasks_module.tasks:
            curr_task = task()
            self.taskMap[curr_task.name] = curr_task

    def createWidgets(self):
        """Setup all UI components for the Task Solver window."""
        # Sidebar for Task Selection
        self.create_sidebar()

        # Main View Panel (Right Side)
        self.create_main_view()

        # Task List
        self.load_Tasks()
        self.update_task_list()

    def create_sidebar(self):
        """Create the left panel with task list and action buttons."""
        sidebar = tk.LabelFrame(self, text="Tasks")
        sidebar.pack(fill=tk.Y, side=tk.LEFT, padx=5, pady=5)

        # Task Listbox
        self.taskList = tk.Listbox(sidebar, selectmode=tk.SINGLE)
        self.taskList.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.taskList.bind("<<ListboxSelect>>", self.selected_task)
        self.taskList.bind("<KeyPress-Up>", self.handle_keys)
        self.taskList.bind("<KeyPress-Down>", self.handle_keys)

        # Buttons
        ttk.Button(sidebar, text="Select Task", command=self.submit).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(sidebar, text="Pop Out Canvas", command=self.pop_out_canvas).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(sidebar, text="Reload Tasks", command=self.reload).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(sidebar, text="Save Data", command=self.save_data).pack(fill=tk.X, padx=5, pady=5)

    def create_main_view(self):
        """Create the right panel with task controls and graph display."""
        right_panel = ttk.Frame(self)
        right_panel.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, padx=5, pady=5)

        # Task Control Canvas
        self.create_task_control_panel(right_panel)

        # Graph Display
        self.create_canvas_panel(right_panel)

    def create_task_control_panel(self, parent):
        """Create scrollable task control frame."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollable Canvas
        self.canvasEntry = tk.Canvas(frame)
        self.canvasEntry.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbars
        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.canvasEntry.xview)
        y_scroll = ttk.Scrollbar(frame, orient="vertical", command=self.canvasEntry.yview)
        x_scroll.pack(fill=tk.X, side=tk.BOTTOM)
        y_scroll.pack(fill=tk.Y, side=tk.RIGHT)

        self.canvasEntry.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

        # Inner Frame for Controls
        self.inner_frame = ttk.Frame(self.canvasEntry)
        self.WindowID = self.canvasEntry.create_window(0, 0, anchor=tk.NW, window=self.inner_frame)

        # Scroll Adjustments
        frame.bind("<Configure>", self._configure_scroll)

    def create_canvas_panel(self, parent):
        """Create the panel for displaying task graphs."""
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._display = mb_tkagg.FigureCanvasTkAgg(self._heatmap, master=canvas_frame)
        self._canvas = self._display.get_tk_widget()
        self._canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._display.draw()

    def _configure_scroll(self, event):
        """Adjust scroll region to match inner frame size."""
        size = (self.inner_frame.winfo_reqwidth(), self.inner_frame.winfo_reqheight())
        self.canvasEntry.config(scrollregion=(0, 0, *size))

    def reload(self):
        """Reload tasks into the listbox."""
        self.load_Tasks()
        self.update_task_list()

    def update_task_list(self):
        """Update the task list in the UI."""
        self.taskList.delete(0, tk.END)
        self.taskList.insert(0, *self.taskMap)

    def selected_task(self, event):
        """Handle task selection change."""
        index = self.taskList.curselection()
        if not index:
            return

        key = self.taskList.get(index[0])
        if key == self.current_task:
            return

        self._heatmap.clf()
        self.current_task = self.taskMap[key]

        # Update canvas with new figure
        self._display.figure = self.current_task.figure
        self._display.draw()

    def handle_keys(self, event):
        """Handle Up/Down key navigation in the task list."""
        index = self.taskList.curselection()
        if not index:
            return

        index = index[0]
        if event.keysym == "Up":
            new_index = max(0, index - 1)
        elif event.keysym == "Down":
            new_index = min(self.taskList.size() - 1, index + 1)
        else:
            return

        self.taskList.selection_clear(index)
        self.taskList.selection_set(new_index)
        self.taskList.activate(new_index)
        self.taskList.event_generate("<<ListboxSelect>>")

    def submit(self):
        """Handle task submission."""
        if not self.current_task:
            return

        # Clear previous controls
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Add controls for the selected task
        for method in self.current_task.exposed_methods or ["setup", "run"]:
            self.stores.update(py_iface.makeFunctionCallable(method, self.inner_frame, instance=self.current_task))

    def pop_out_canvas(self):
        """Create a separate window for the task figure."""
        if not self.current_task:
            return

        new_window = tk.Toplevel(self)
        canvas_frame = ttk.Frame(new_window)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        display = mb_tkagg.FigureCanvasTkAgg(self.current_task.figure, master=canvas_frame)
        canvas = display.get_tk_widget()
        canvas.pack(fill=tk.BOTH, expand=True)
        display.draw()

    def save_data(self):
        """Save task data."""
        if not self.current_task or not self.current_task.savables:
            msgbox_.showinfo("Save", "No Task Selected or Nothing to Save")
            return

        for name, save_func in self.current_task.savables.items():
            if msgbox_.askyesno(f"Would you like to save {name}?", "Save"):
                data = save_func()
                if data and nfile_io.saveFileGui(data, initname=name):
                    msgbox_.showinfo("Save", f"Saved Successfully: {name}")

scene = TasksFrame
