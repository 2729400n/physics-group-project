from enum import Enum
import tkinter as tk
import tkinter.ttk as ttk
from typing import Generator
import typing
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox as msgbox
from tkinter import simpledialog as simp_diag
import pathlib
import time
import tkinter.filedialog as fdiag
from ...utils.nfile_io import walkDirectory
from ...utils.nfile_io.extensions import numpy_io, image_io
from ...Solvers import errors

# print('Compare Res',__name__)
class FTYPES(Enum):
    DIRECTORY = 'DIRECTORY'
    NPZ = 'Numpy Package File'
    NPY = 'Numpy Binary File'



class MagicClass(typing.Collection):
    def __getitem__(self,*args):
        if self.side:
            ret = self.bottom
            self.bottom+=1
        else:
            ret=self.top
            self.top-=1
        self.side=not self.side
        return ret
    
    def __next__(self):
        return self.__getitem__()
    def __contains__(self, x):
        return False
    def __iter__(self):
        return self
    def __len__(self):
        return np.inf
    def __init__(self,a=None,b=None,a_first=True):
        self.bottom=0
        self.top=-1
        if a is not None:
            self.bottom=a
        if a is not None:
            self.top=b
        self.side=a_first
        

def scale_to_fit(a1,a2,copya1=True,copya2=True):
    f1:np.ndarray = np.array(a1,copy=copya1)
    f2:np.ndarray = np.array(a2,copy=copya2)
    
        # Ensure same number of dimensions by padding the smaller array
    while f1.ndim < f2.ndim:
        f1 = f1.reshape((1,) + f1.shape)
    while f2.ndim < f1.ndim:
        f2 = f2.reshape((1,) + f2.shape)

    # Adjust shapes explicitly for each dimension
    
    if f1.shape != f2.shape:
        
        wantedShapef1=[f1.shape[int(i//2)] if ((i%2)==0) else 1  for i in range(2*f1.ndim)]
        wantedShapef2=[f2.shape[int(i//2)] if ((i%2)==0) else 1  for i in range(2*f2.ndim)]
        
        f1slices =[slice(0,wantedShapef1[i],1) if ((i%2)==0) else None  for i in range(2*f1.ndim)]
        f2slices =[slice(0,wantedShapef2[i],1) if ((i%2)==0) else None  for i in range(2*f2.ndim)]
        finalslice1 = [0 for i in range(f1.ndim)]
        finalslice2 = [0  for i in range(f1.ndim)]
        finalshape1 = [i for i in f1.shape]
        finalshape2 = [i for i in f2.shape]
        for i in range(f1.ndim):
            if f1.shape[i] == f2.shape[i]:
                continue

            if f1.shape[i] < f2.shape[i]:  # Expand f1 by repeating cyclically
                repeats = f2.shape[i] // f1.shape[i]  # Full repeats
                remainder = f2.shape[i] % f1.shape[i]  # Leftover elements
                # wantedShapef1[i*2]=f2.shape[i]
                n=repeats
                wantedShapef1[1+(i*2)] =n
                finalshape1[i]=f1.shape[i]*n
                finalslice1[i] = remainder

            elif f1.shape[i] > f2.shape[i]:  # Expand f2 by repeating cyclically
                repeats = f1.shape[i] // f2.shape[i]  # Full repeats
                remainder = f1.shape[i] % f2.shape[i]  # Leftover elements
                # wantedShapef2[i*2]=f1.shape[i]
                n =repeats 
                wantedShapef2[1+(i*2)]=n
                finalshape2[i]=f2.shape[i]*n
                finalslice2[i] = remainder
        
        
        f1=np.broadcast_to(f1[*f1slices],wantedShapef1).reshape(tuple(finalshape1))
        f2=np.broadcast_to(f2[*f2slices],wantedShapef2).reshape(tuple(finalshape2))
        
        del finalshape1,finalshape2,f1slices,f2slices,wantedShapef1,wantedShapef2
        f1magic = MagicClass()
        for i in range(len(finalslice1)):
            if finalslice1[i] !=0:
                newindex=[]
                for z in range(2*len(f1.shape)):
                    
                    if (z%2)==0:
                        k=int(z//2)
                        if k!=i: 
                            newindex+=[slice(None,None),None]
                        else:
                            newindex+=[(tuple(int(j//2) for j in range(2*int(np.ceil(finalslice1[i]/2))))+
                                        tuple(range(f1.shape[k]))[int(np.ceil(finalslice1[i]/2)):((int(finalslice1[i]//2)//2)+1)]+
                                        tuple(f1.shape[i]-(int(j//2)+1) for j in range(2*int(finalslice1[i]//2)))),None]
#                print('f1',newindex)
                f1 = f1[*newindex].reshape(tuple(f1.shape[z] if z != i else (f1.shape[i]+finalslice1[i]) for z in range(len(f1.shape))))
        
        del f1magic
        
        f2magic = MagicClass()
        
        for i in range(len(finalslice2)):
            if finalslice2[i] !=0:
                newindex=[]
                
                for z in range(2*len(f2.shape)):
                    if (z%2)==0:
                        k=int(z//2)
                        if k!=i: 
                            newindex+=[slice(None,None),None]
                        else:
                            newindex+=[(tuple(int(j//2) for j in range(finalslice2[i]))+tuple(range(f2.shape[k]))[int(finalslice2[i]//2):] + tuple(int(j//2) for j in range(finalslice2[i]))),None]
                
                f2 = f2[*newindex].reshape(tuple(f2.shape[z] if z != i else (f2.shape[i]+finalslice2[i]) for z in range(len(f2.shape))))
        
        del f2magic
        return f1,f2

def scale_to_scale(a1,a2,copya1=True,copya2=True):
    f1:np.ndarray = np.array(a1,copy=copya1)
    f2:np.ndarray = np.array(a2,copy=copya2)
    
        # Ensure same number of dimensions by padding the smaller array
    while f1.ndim < f2.ndim:
        f1 = f1.reshape((1,) + f1.shape)
    while f2.ndim < f1.ndim:
        f2 = f2.reshape((1,) + f2.shape)

    # Adjust shapes explicitly for each dimension
    
    if f1.shape != f2.shape:
        
        wantedShapef1=[f1.shape[int(i//2)] if ((i%2)==0) else 1  for i in range(2*f1.ndim)]
        wantedShapef2=[f2.shape[int(i//2)] if ((i%2)==0) else 1  for i in range(2*f2.ndim)]
        
        f1slices =[slice(0,wantedShapef1[i],1) if ((i%2)==0) else None  for i in range(2*f1.ndim)]
        f2slices =[slice(0,wantedShapef2[i],1) if ((i%2)==0) else None  for i in range(2*f2.ndim)]
        finalslice = [slice(0,1,1)  for i in range(f1.ndim)]
        finalshape1 = [i for i in f1.shape]
        finalshape2 = [i for i in f2.shape]
        for i in range(f1.ndim):
            if f1.shape[i] == f2.shape[i]:
                continue

            if f1.shape[i] < f2.shape[i]:  # Expand f1 by repeating cyclically
                repeats = f2.shape[i] // f1.shape[i]  # Full repeats
                remainder = f2.shape[i] % f1.shape[i]  # Leftover elements
                # wantedShapef1[i*2]=f2.shape[i]
                n=(repeats + (1 if remainder else 0))
                wantedShapef1[1+(i*2)] =n
                finalshape1[i]=f1.shape[i]*n
                finalslice[i] = slice(0,f2.shape[i],1)

            elif f1.shape[i] > f2.shape[i]:  # Expand f2 by repeating cyclically
                repeats = f1.shape[i] // f2.shape[i]  # Full repeats
                remainder = f1.shape[i] % f2.shape[i]  # Leftover elements
                # wantedShapef2[i*2]=f1.shape[i]
                n =(repeats + (1 if remainder else 0))
                wantedShapef2[1+(i*2)]=n
                finalshape2[i]=f2.shape[i]*n
                finalslice[i] = slice(0,f1.shape[i],1)
                
        print('f1slices',f1slices)
        print('f2slices',f2slices)
        print('wantedShapef1',wantedShapef1)
        print('wantedShapef2',wantedShapef2)
        print('finalShape1',finalshape1)
        print('finalShape1',finalshape1)
        f1=np.broadcast_to(f1[*f1slices],wantedShapef1).reshape(tuple(finalshape1))[*finalslice]
        f2=np.broadcast_to(f2[*f2slices],wantedShapef2).reshape(tuple(finalshape2))[*finalslice]
        
        return f1,f2

def tile_scale(a1,a2,copya1=True,copya2=True):
    f1:np.ndarray = np.array(a1,copy=copya1)
    f2:np.ndarray = np.array(a2,copy=copya2)
    # Ensure same number of dimensions by padding the smaller array
    while f1.ndim < f2.ndim:
        f1 = f1.reshape((1,) + f1.shape)
    while f2.ndim < f1.ndim:
        f2 = f2.reshape((1,) + f2.shape)

    # Adjust shapes explicitly for each dimension
    
    if f1.shape != f2.shape:
        wantedShapef1 =[slice(i) for i in f1.shape]
        wantedShapef2 =[slice(i) for i in f1.shape]
        for i in range(f1.ndim):
            if f1.shape[i] == f2.shape[i]:
                continue

            if f1.shape[i] < f2.shape[i]:  # Expand f1 by repeating cyclically
                repeats = f2.shape[i] // f1.shape[i]  # Full repeats
                remainder = f2.shape[i] % f1.shape[i]  # Leftover elements
                f1 = np.tile(f1, (repeats + (1 if remainder else 0),) + (1,) * (f1.ndim - i - 1))
                wantedShapef1[i]=slice(f2.shape[i])
                f1 = f1[*wantedShapef1]  # Trim excess from the end

            elif f1.shape[i] > f2.shape[i]:  # Expand f2 by repeating cyclically
                repeats = f1.shape[i] // f2.shape[i]
                remainder = f1.shape[i] % f2.shape[i]
                f2 = np.tile(f2, (repeats + (1 if remainder else 0),) + (1,) * (f2.ndim - i - 1))
                wantedShapef2[i]=slice(f1.shape[i])
                f2 = f2[*wantedShapef2]  # Trim excess from the end
    
    return f1,f2
class CompareScene(ttk.Frame):
    name = 'Compare'

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._results_dir = pathlib.Path.cwd()
        # Configure grid for responsiveness
        self.treeFrame = ttk.Frame(self)
        self.treeFrame.pack(fill=tk.BOTH, anchor=tk.NW, expand=True, padx=5, pady=5, side='left')
        self.treeFrame.propagate(True)
        
        self.ToggleFrame = ttk.Frame(self)
        self.ToggleFrame.pack(fill=tk.BOTH, side='right', anchor=tk.NW, expand=True, padx=5, pady=5, before=self.treeFrame)
        self.ToggleFrame.columnconfigure(0, weight=1)
        self.ToggleFrame.rowconfigure(0, weight=1)
        self.ToggleFrame.propagate(True)

        # Create TreeView for file structure
        self.create_tree()

        self.main_frame = ttk.Frame(self.ToggleFrame)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Add additional frames, labels, and functionality (plot, comparison buttons, etc.)
        self.value_text = tk.StringVar(self,"Select Some files to compare them!")
        self.value_label = ttk.Label(self.main_frame, textvariable=self.value_text)
        self.value_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.grid(row=1, column=0, sticky="nsew")
        self.plot_frame.columnconfigure(0, weight=1)
        self.plot_frame.rowconfigure(0, weight=1)
        
        self.compare_buttons_frame=None
        self.abs_diff_button = None
        self.rel_diff_button = None
        

        self.create_plot()

        # Bind resize event for dynamic adjustments
        self.plot_frame.bind("<Configure>", self.on_resize)

        # Initialize the data variables
        self.cursel = []
        self.data = None
        self.Grid_obj: np.ndarray = None
        self.currGrid:np.ndarray=None
        self.dx = 1.0
        self.dy = 1.0
        
        self.first_file_name=None
        self.second_file_name = None
        self.first_file = None
        self.second_file = None

    @property
    def results_dir(self) -> pathlib.Path:
        return self._results_dir

    @results_dir.setter
    def results_dir(self, value: pathlib.Path) -> None:
        if isinstance(value, bytes):
            value = value.decode()
        if isinstance(value, str):
            value = pathlib.Path(value)
        if not isinstance(value, pathlib.Path):
            raise TypeError('Value must be a PathLike object')
        value = value.resolve().absolute()
        self._results_dir = value
        self._reload_tree_view()

    # TODO : Fix the tree handling
    def _on_tree_item_selected(self, evt: tk.Event):
        
        cursel =self.treeView.selection()
        for i in cursel:
            if i not in self.cursel:
                break
        else:
            return
        selection =[]
        for i in cursel:
#             print(i)
            item_type=self.treeView.item(i).get('values',['UNK'])[0]
            if 'DIRECTORY'==item_type.upper().strip():
                continue
            selection.append(i)
            
        if selection is None:
            return None
        

        if len(selection) == 0:
            return
        
        self.cursel.extend(selection)
        if len(self.cursel) > 2:
            self.cursel = self.cursel[-2:]
#             print(self.cursel)
            self.treeView.selection_set(self.cursel)
        self.value_text.set(f'Selected files:\n{' and\n'.join([f"{chr(0x2e)*2}/{pathlib.Path(i).name}" for i in self.cursel])}')

        if len(self.cursel) == 2:
            self.show_comparison_buttons()
        else:
            self.hide_comparison_buttons()

    def _clear_selection(self):
        self.hide_comparison_buttons()
        self.treeView.selection_remove(*self.cursel)
        self.cursel.clear()
        self.first_file=None
        self.second_file=None
        self.value_text.set("Select Some files to compare them!")
        
    def hide_comparison_buttons(self):
        if self.compare_buttons_frame is not None:
            if self.compare_buttons_frame.winfo_exists():
                self.compare_buttons_frame.grid_remove()
    
    def show_comparison_buttons(self):
        """Displays buttons for comparing the selected files."""
        if self.compare_buttons_frame is None:
            self.compare_buttons_frame = ttk.Frame(self.ToggleFrame)
            self.compare_buttons_frame.grid(row=2, column=0, sticky="nsew")

            self.abs_diff_button = ttk.Button(self.compare_buttons_frame, text="Compare Absolute Difference",
                                            command=self.compare_absolute_difference)
            self.rel_diff_button = ttk.Button(self.compare_buttons_frame, text="Compare Relative Difference",
                                            command=self.compare_relative_difference)

            self.abs_diff_button.grid(row=0, column=0, padx=5, pady=5)
            self.rel_diff_button.grid(row=0, column=1, padx=5, pady=5)
        else:
            self.compare_buttons_frame.grid()

    def _save_data(self):
        pass
    
    def compare_absolute_difference(self):
        """Compares two files by absolute difference."""
        if self.first_file is None or self.second_file is None:
            msgbox.showerror(message="Please select two files for comparison.")
            return
        f1:np.ndarray = self.first_file
        f2:np.ndarray = self.second_file

        if not (isinstance(f1,(np.ndarray,typing.Iterable,typing.Collection,list,tuple)) and isinstance(f2,(np.ndarray,typing.Iterable,typing.Collection,list,tuple))):
            msgbox.showerror(message="Files cannot be arrayified.")
            return
        
        
        
        f1 = np.array(f1,copy=True)
        f2 = np.array(f2,copy=True)
        if f1.shape!=f2.shape:
            dg=simp_diag.SimpleDialog(self,
                               "The data(s) you have chosen are of different dimensions!\nHow would you like to rescale?",
                               ["Homogenously","Inhomogenously","Repeat","Dont"],
                               default=3,cancel=3)
        
            opt = dg.go()
            match opt:
                case 0:
                    f1,f2 = scale_to_fit(f1,f2,copya1=False,copya2=False)
                case 1:
                    f1,f2 = scale_to_scale(f1,f2,copya1=False,copya2=False)
                case 2:
                    f1,f2 = tile_scale(f1,f2,copya1=False,copya2=False)
                case _:
                    return
            del dg,opt
        
        
        
        
        
        # Compare absolute difference
        diff = np.abs(f1-f2)
        self.plot_comparison(diff, title="Absolute Difference")

    def compare_relative_difference(self):
        """Compares two files by relative difference."""
        if self.first_file is None or self.second_file is None:
            msgbox.showerror(message="Please select two files for comparison.")
            return
        f1:np.ndarray = self.first_file
        f2:np.ndarray = self.second_file

        if not (isinstance(f1,(np.ndarray,typing.Iterable,typing.Collection,list,tuple)) and isinstance(f2,(np.ndarray,typing.Iterable,typing.Collection,list,tuple))):
            msgbox.showerror(message="Files cannot be arrayified.")
            return
        f1 = np.array(f1,copy=True)
        f2 = np.array(f2,copy=True)
        if f1.shape!=f2.shape:
            dg=simp_diag.SimpleDialog(self,
                               "The data(s) you have chosen are of different dimensions!\nHow would you like to rescale?",
                               ["Homogenously","Inhomogenously","Repeat","Dont"],
                               default=3,cancel=3)
        
            opt = dg.go()
            match opt:
                case 0:
                    f1,f2 = scale_to_fit(f1,f2,copya1=False,copya2=False)
                case 1:
                    f1,f2 = scale_to_scale(f1,f2,copya1=False,copya2=False)
                case 2:
                    f1,f2 = tile_scale(f1,f2,copya1=False,copya2=False)
                case _:
                    return
            del dg,opt
        # zmask =f1==0
        # fz = np.zeros_like(f1)
        # fz[zmask]=np.spacing(f2)[zmask]
        # Compare relative difference
        diff = np.abs((f1 - f2) / (f1))
        self.plot_comparison(diff, title="Relative Difference")

    def plot_comparison(self, diff, title):
        """Plots the difference data."""
        self.currGrid = diff
        fig = Figure(figsize=(8, 8))
        ax = fig.add_subplot(111)

        ax.imshow(diff)
        ax.set_title(title)

        canvas = self.canvas
        if canvas is not None:
            canvas.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew")
        
        canvas.draw()
        self.canvas = canvas
        
        # Add Navigation Toolbar
        if self.toolbar is not None:
            self.toolbar.destroy()
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame, pack_toolbar=False)
        
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0, sticky="nsew")
        
        
        
        

    def _choose_data(self):
        cursel = self.cursel

        if len(cursel) != 2:
            msgbox.showerror(message="Please select exactly two files.")
            return

        files = [self.treeView.item(sel)['values'][-1] for sel in cursel]
        self.first_file = self.load_file(files[0])
        self.second_file = self.load_file(files[1])

    def load_file(self, file_path):
        """Loads a file (npy or npz) into a numpy array."""
#         print(file_path)
        try:
            file_path = pathlib.Path(file_path)
            if file_path.suffix == '.npy':
                return numpy_io.loadArray(file_path, True)
            elif file_path.suffix == '.npz':
                data = numpy_io.loadArray(file_path, True)
                # Assuming the file contains a dictionary, we take the first array as the target
                return list(data.values())[0]
            else:
                msgbox.showerror(message="Unsupported file type. Only .npy and .npz are allowed.")
                return None
        except Exception as e:
            msgbox.showerror(message=f"Error loading file: {e}")
            return None

    def _reload_tree_view(self) -> None:
        """Reload the tree view to reflect changes in the directory."""
        self._clear_tree_view()
        self._load_tree_view()

    def _clear_tree_view(self) -> None:
        """Clears all items in the Treeview."""
        self.treeView.delete(*self.treeView.get_children())

    def _load_tree_view(self):
        """Load directory structure into the TreeView."""
        results_dir = self.results_dir
        stats = results_dir.stat()
        cc = self.treeView.insert('', 0, results_dir.name, text=results_dir.name, values=('Directory', stats.st_size, time.ctime(stats.st_mtime), str(results_dir)))

        # Walk directory and insert files and subdirectories
        k: 'Generator[pathlib.Path]' = walkDirectory(results_dir, extension=['.png', '.npz', '.npy'])
        for dtree in k:
            for i in dtree:
                store = False
                if not i.is_file():
                    continue
                for part in reversed(i.parents):
                    if results_dir.samefile(part) and not store:
                        store = True
                        currentindex = cc
                        continue
                    if store:
                        itemname = part.absolute().as_posix()
                        if not self.treeView.exists(itemname):
                            if part.is_dir():
                                part_type = 'Directory'
                            else:
                                part_type = 'File'
                            stats = part.stat()
                            currentindex = self.treeView.insert(currentindex, 'end', iid=itemname, text=part.name,
                                                                 values=(part_type, stats.st_size, time.ctime(stats.st_mtime), part))
                        else:
                            currentindex = itemname
                stats = i.stat()
                ftype = i.suffix.upper()
                currentindex = self.treeView.insert(currentindex, 'end', iid=i.absolute().resolve().as_posix(), text=i.stem,
                                                     values=(ftype, stats.st_size, time.ctime(stats.st_mtime), i))

    def create_tree(self):
        """Create the Treeview widget and set up buttons."""
        self.treeView = ttk.Treeview(self.treeFrame, columns=('Type', 'Size', 'Age', "Path"), selectmode=tk.EXTENDED)
        self.treeView.column('#0', width=100, minwidth=100, stretch=tk.NO)
        self.treeView.heading('#0', text="Name")

        self.treeView.column('Type', width=100, minwidth=100)
        self.treeView.heading('Type', text="Type")

        self.treeView.column('Size', width=100, minwidth=100)
        self.treeView.heading('Size', text="Size")

        self.treeView.column('Age', width=100, minwidth=100)
        self.treeView.heading('Age', text="Age")

        self.treeView.column('Path', width=250, minwidth=250)
        self.treeView.heading('Path', text="Path")

        self.treeView.pack(expand=True, fill=tk.BOTH, side=tk.TOP, anchor=tk.NW, padx=5, pady=5)
        self.treeView.bind('<<TreeviewSelect>>', self._on_tree_item_selected, add='+')

        self.reloadButton = ttk.Button(self.treeFrame, text='Reload', command=self._reload_tree_view)
        self.newDirectoryButton = ttk.Button(self.treeFrame, text='Change Directory', command=self._pick_directory)
        self.chooseDataButton = ttk.Button(self.treeFrame, text='Choose Data', command=self._choose_data)
        self.clearFiles = ttk.Button(self.treeFrame, text='Clear Selection', command=self._clear_selection)
        self.errorFinderButton = ttk.Button(self.treeFrame, text='Error Finder', command=self._error_finder)

        self.reloadButton.pack(fill=tk.X, padx=5, pady=5)
        self.newDirectoryButton.pack(fill=tk.X, padx=5, pady=5)
        self.chooseDataButton.pack(fill=tk.X, padx=5, pady=5)
        self.clearFiles.pack(fill=tk.X, padx=5, pady=5)

        self._load_tree_view()

    def create_plot(self):
        """Create the initial plot."""
        fig = Figure(figsize=(8, 8))
        ax = fig.add_subplot(111)

        ax.plot([1, 2, 3], [1, 4, 9])  # Example plot
        ax.set_title("Example Plot")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew")
        canvas.draw()
        self.canvas = canvas
        
        # Add Navigation Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame, pack_toolbar=False)
        
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0, sticky="nsew")

    def on_resize(self, event):
        """Handle resizing of the plot area."""
        self.canvas.get_tk_widget().config(width=event.width, height=event.height)

    def _pick_directory(self):
        """Open a file dialog to select a directory."""
        directory = fdiag.askdirectory()
        if directory:
            self._clear_selection()
            self.results_dir = pathlib.Path(directory)
            

    def _error_finder(self):
        """Method for error finding or handling."""
        msgbox.showinfo("Error Finder", "This is a placeholder function.")




scene = CompareScene