from enum import Enum
import tkinter as tk
import tkinter.ttk as ttk
from typing import Generator, Iterator
import typing
import matplotlib.backends.backend_tkagg as tkagg
import matplotlib.backend_managers as bmans
import matplotlib.backend_tools as btools
import matplotlib.backend_bases as bb
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ...utils.nfile_io import walkDirectory
from ...utils.nfile_io.extensions import numpy_io,image_io
from ...Solvers import errors
import pathlib
import time
import glob
import tkinter.filedialog as fdiag
import tkinter.messagebox as msgbox

class FTYPES(Enum):
    DIRECTORY = 'DIRECTORY'
    NPZ = 'Numpy Package File'
    NPY='Numpy Binary File'

class ResultsScene(ttk.Frame):
    name='Results'
    # hiden_files_regex = glob.translate('.vscode',recursive=True,)
    def __init__(self,master=None,*args,**kwargs):
        
        super().__init__(master,*args,**kwargs)
        
        # Configure grid for responsiveness
        self.treeFrame = ttk.Frame(self)
        self.treeFrame.pack(fill=tk.BOTH, anchor=tk.NW,expand=True,padx=5,pady=5,side='left')
        self.treeView:'ttk.Treeview' = None
        # Configure grid for responsiveness
        self.ToggleFrame = ttk.Frame(self)
        self.ToggleFrame.pack(fill=tk.BOTH,side='right', anchor=tk.NW,expand=True,padx=5,pady=5, before=self.treeFrame)
        self.ToggleFrame.columnconfigure(0,weight=1)
        self.ToggleFrame.rowconfigure(0,weight=1)

        self._results_dir = pathlib.Path('./').resolve().absolute()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.ToggleFrame)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Label to display data value from mouse click events
        self.value_label = ttk.Label(self.main_frame, text="Click on the plot to see value")
        self.value_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Frame for plot and toolbar
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.grid(row=1, column=0, sticky="nsew")
        self.plot_frame.columnconfigure(0, weight=1)
        self.plot_frame.rowconfigure(0, weight=1)

        self.create_plot()
        
        # Bind resize event for dynamic adjustments
        self.plot_frame.bind("<Configure>", self.on_resize)
        
        
        self.data=None
        self.Grid_obj :np.ndarray=None
        self.dx=1.0
        self.dy=1.0
        self.cursel = None
    @property
    def results_dir(self)->pathlib.Path:
        return self._results_dir
    @results_dir.setter
    def results_dir(self,value:pathlib.Path)->None:
        if isinstance(value,bytes):
            value = value.decode()
        if isinstance(value,str):
            value = pathlib.Path(value)
        if not isinstance(value,pathlib.Path):
            raise TypeError('Value must be a PathLike object')
        value = value.resolve().absolute()
        self._results_dir = value
        self._reload_tree_view()
    
    
    def _on_tree_item_selected(self,evt:tk.Event):
        selection =self.treeView.selection()
        if selection is None:
            return None
        
        if len(selection)==0:
            return
        
        self.cursel=selection
    
    def _error_finder(self):
        
        if self.Grid_obj is None:
            msgbox.showerror(message="Make sure you have selected an insightable file.")
            return
        
        fig = Figure(figsize=(8, 8),)
        ax = fig.add_subplot(111)
        
        
        newErrorWindow =tk.Toplevel(self,)
        mainframe = ttk.Frame(newErrorWindow)
        plot_frame = ttk.Frame(mainframe)
        button_frame = ttk.Frame(mainframe)
        
        newErrorWindow.propagate(True)
        mainframe.propagate(True)
        plot_frame.propagate(True)
        button_frame.propagate(True)
        
        plot_frame.columnconfigure(0,weight=1)
        plot_frame.rowconfigure(0,weight=1)
        plot_frame.columnconfigure(0,weight=1)
        plot_frame.rowconfigure(1,weight=1)
        # Plot data
        mainframe.columnconfigure(0,weight=1)
        mainframe.rowconfigure(0,weight=1)
        mainframe.columnconfigure(0,weight=1)
        mainframe.rowconfigure(1,weight=1)
        # Embed figure into Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew")
        canvas_widget.configure(width=640,height=480)
        canvas.draw()
        # Add Navigation Toolbar
        toolbar = NavigationToolbar2Tk(canvas, plot_frame,pack_toolbar=False)
        
        toolbar.update()
        toolbar.grid(row=1, column=0, sticky="ew")
        
        plot_frame.grid(column=0,row=0)
        button_frame.grid(column=0,row=1)
        
        mainframe.pack(anchor=tk.NW,side=tk.TOP,fill=tk.BOTH,expand=True)
        
        
        ax.set_title("The Laplacian Absolute Error")
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        # self.ax.legend()
        
        resi,absresi=errors.laplaceify(self.Grid_obj,self.dx,self.dy)
        ax.imshow(absresi)
        # Connect event for mouse clicks on the canvas
        # canvas.mpl_connect("button_press_event", self.on_click)
        
    def _choose_data(self):
        cursel = self.cursel
        
        
        item=self.treeView.item(cursel,option=None)
        
        if not isinstance(item,(dict)):
            msgbox.showerror(message="Could not find File in tree")
            return
        vals=item.get('values',['',-1,'ANY',cursel])
        selcfile=pathlib.Path(vals[-1])
        if selcfile.is_dir():
            msgbox.showwarning(message="Cannot Open a Directory")
            return
        match selcfile.suffix:
            case '.npy':
                try:
                    fil =numpy_io.loadArray(selcfile,True)
                    self.ax.clear()
                    self.line=self.ax.imshow(fil)
                    self.canvas.draw()
                    self.Grid_obj = fil
                except Exception as e:
                    msgbox.showerror(message=f"{e}",title='Exception')
            case '.npz':
                try:
                    fil =numpy_io.loadArray(selcfile,True)
                    print(fil)
                    print(fil.__class__)
                    print(fil.__dir__())
                except Exception as e:
                    msgbox.showerror(message=f"{e}",title='Exception')
            case '.png':
                try:
                    fil =image_io.openImage(selcfile)
                    self.ax.clear()
                    self.line = self.ax.imshow(fil)
                    self.ax
                    self.canvas.draw()
                except Exception as e:
                    msgbox.showerror(message=f"{e}",title='Exception')
        
        
        
        
        
    
    def _create_color_bar() -> None:
        pass
    
    def _remove_color_bar()->None:
        pass
    
    def _reload_color_bar()->None:
        pass
    
    def _pick_directory(self) -> None:
        self.results_dir = fdiag.askdirectory(initialdir=self.results_dir,mustexist=True,title='Choose results Directory')
    
    def _reload_tree_view(self) -> None:
        self._clear_tree_view()
        self._load_tree_view()
    
    def _clear_tree_view(self) -> None:
        self.treeView.delete(*self.treeView.get_children())
    
    def _load_tree_view(self)->None:
        results_dir =self.results_dir
        stats =results_dir.stat()
        cc=self.treeView.insert('',0,results_dir.name,text=results_dir.name,values=('Directory',stats.st_size,time.ctime(stats.st_mtime),results_dir))
        
        k:'Generator[pathlib.Path]' = walkDirectory(results_dir,extension=['.png','.npz','.npy'])
        for dtree in k:
            for i in dtree:
                
                store = False
                if not i.is_file():
                    continue
                for part in reversed(i.parents):
                    if results_dir.samefile(part) and not store:
                        store=True
                        currentindex = cc
                        continue
                    if store:
                        itemname =part.absolute().as_posix()
                        if(not self.treeView.exists(itemname)):
                            if part.is_dir():
                                part_type = 'Directory'
                            else:
                                part_type = 'File'
                            stats =  part.stat()
                            currentindex=self.treeView.insert(currentindex,'end',iid=itemname,text=part.name,values=(part_type,stats.st_size,time.ctime(stats.st_mtime),part))
                        else:
                            currentindex = itemname
                stats =  i.stat()
                match i.suffix.lower():
                    case '.npy':
                        ftype='Numpy Binary File'
                    case '.npz':
                        ftype='Numpy Package File'
                    case '.csv':
                        ftype='Comma seperated values'
                    case _:
                        ftype=f'{i.suffix.upper()} File'
                currentindex=self.treeView.insert(currentindex,'end',i.absolute().resolve().as_posix(),text=i.stem,values=(ftype,stats.st_size,time.ctime(stats.st_mtime),i))
                
                    
                
    def _load_listview(self)->None:
        pass
    def create_tree(self):
        self.treeView= treeView =ttk.Treeview(self.treeFrame,columns=('Type','Size','Age',"Path"),selectmode=tk.BROWSE)
        
        treeView['columns']=('Type','Size','Age','Path')
        treeView.column('Type',width=100)
        treeView.heading('Type',text="Type")
        
        treeView.column('Size',width=100)
        treeView.heading('Size',text="Size")
        
        treeView.column('Age',width=100)
        treeView.heading('Age',text="Age")
        
        treeView.column('#0',width=100)
        treeView.heading('#0',text="Name")
        
        
        treeView.pack(expand=True,fill=tk.BOTH,side=tk.TOP,anchor=tk.NW,padx=5,pady=5)
        treeView.bind('<<TreeviewSelect>>',self._on_tree_item_selected,add='+')
        
        self.reloadButton = ttk.Button(self.treeFrame,text='Reload',command=self._reload_tree_view)
        self.newDirectoryButton = ttk.Button(self.treeFrame,text='Change Directory',command=self._pick_directory)
        self.chooseDataButton = ttk.Button(self.treeFrame,text='Choose Data',command=self._choose_data)
        self.insightButton = ttk.Button(self.treeFrame,text='Get Insight',command=self._error_finder)
        
        self.insightButton.pack()
        self.reloadButton.pack()
        self.newDirectoryButton.pack()
        self.chooseDataButton.pack()

        
        self._load_tree_view()
        
    
    def create_plot(self):
        """Creates a Matplotlib figure, embeds it, and sets up tools."""
        # Create figure and axis
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Generate some data
        self.x = np.linspace(0, 10, 100)
        self.y = np.sin(self.x)
        self.line = self.ax.imshow(np.random.rand(256, 256))
        self.fig.colorbar(self.line, ax=self.ax)

        # Plot data

        self.ax.set_title("A Random Art to make Your day")
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        # self.ax.legend()

        # Embed figure into Tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")

        # Add Navigation Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame,pack_toolbar=False)
        
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0, sticky="ew")

        # Connect event for mouse clicks on the canvas
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.create_tree()

    def on_resize(self, event):
        """Handles frame resize event to adjust the plot size."""
        new_width = event.width / self.fig.dpi
        new_height = (event.height - self.toolbar.winfo_height()) / self.fig.dpi
        self.fig.set_size_inches(new_width, new_height)
        self.canvas.draw()

    def on_click(self, event):
        """Displays the y value for the point closest to the click."""
        if event.inaxes == self.ax:
            # Calculate closest data point index using first principles: minimize distance in x
            click_x = event.xdata
            index = (np.abs(self.x - click_x)).argmin()
            closest_x = self.x[index]
            closest_y = self.y[index]
            self.value_label.config(text=f"Clicked near x={closest_x:.2f}, y={closest_y:.2f}")
        
scene = ResultsScene

if __name__=='__main__':
    root  =tk.Tk()
    # root.wm_geometry('640x480')
    frame = ResultsScene(root)
    frame.pack(expand=True,fill='both',padx= 5,pady=5,in_=root,side='top',anchor=tk.NW)
    root.mainloop()