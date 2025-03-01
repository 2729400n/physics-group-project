from enum import Enum
import tkinter as tk
import tkinter.ttk as ttk
from typing import Generator
import typing
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox as msgbox
import pathlib
import time
import tkinter.filedialog as fdiag
from ...utils.nfile_io import walkDirectory
from ...utils.nfile_io.extensions import numpy_io, image_io
from ...Solvers import errors


class FTYPES(Enum):
    DIRECTORY = 'DIRECTORY'
    NPZ = 'Numpy Package File'
    NPY = 'Numpy Binary File'


from enum import Enum
import tkinter as tk
import tkinter.ttk as ttk
from typing import Generator
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox as msgbox
import pathlib
import time
import tkinter.filedialog as fdiag
from ...utils.nfile_io import walkDirectory
from ...utils.nfile_io.extensions import numpy_io, image_io
from ...Solvers import errors


class FTYPES(Enum):
    DIRECTORY = 'DIRECTORY'
    NPZ = 'Numpy Package File'
    NPY = 'Numpy Binary File'


from enum import Enum
import tkinter as tk
import tkinter.ttk as ttk
from typing import Generator
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox as msgbox
import pathlib
import time
import tkinter.filedialog as fdiag
from ...utils.nfile_io import walkDirectory
from ...utils.nfile_io.extensions import numpy_io, image_io
from ...Solvers import errors


class FTYPES(Enum):
    DIRECTORY = 'DIRECTORY'
    NPZ = 'Numpy Package File'
    NPY = 'Numpy Binary File'


class CompareScene(ttk.Frame):
    name = 'Compare'

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._results_dir = pathlib.Path.cwd()
        # Configure grid for responsiveness
        self.treeFrame = ttk.Frame(self)
        self.treeFrame.pack(fill=tk.BOTH, anchor=tk.NW, expand=True, padx=5, pady=5, side='left')

        self.ToggleFrame = ttk.Frame(self)
        self.ToggleFrame.pack(fill=tk.BOTH, side='right', anchor=tk.NW, expand=True, padx=5, pady=5, before=self.treeFrame)
        self.ToggleFrame.columnconfigure(0, weight=1)
        self.ToggleFrame.rowconfigure(0, weight=1)

        # Create TreeView for file structure
        self.create_tree()

        self.main_frame = ttk.Frame(self.ToggleFrame)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Add additional frames, labels, and functionality (plot, comparison buttons, etc.)
        self.value_label = ttk.Label(self.main_frame, text="Click on the plot to see value")
        self.value_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.grid(row=1, column=0, sticky="nsew")
        self.plot_frame.columnconfigure(0, weight=1)
        self.plot_frame.rowconfigure(0, weight=1)

        self.create_plot()

        # Bind resize event for dynamic adjustments
        self.plot_frame.bind("<Configure>", self.on_resize)

        # Initialize the data variables
        self.cursel = []
        self.data = None
        self.Grid_obj: np.ndarray = None
        self.dx = 1.0
        self.dy = 1.0
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
            print(i)
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
            print(self.cursel)
            self.treeView.selection_set(self.cursel)


        if len(self.cursel) == 2:
            self.show_comparison_buttons()

    def show_comparison_buttons(self):
        """Displays buttons for comparing the selected files."""
        self.compare_buttons_frame = ttk.Frame(self.ToggleFrame)
        self.compare_buttons_frame.grid(row=1, column=0, sticky="nsew")

        self.abs_diff_button = ttk.Button(self.compare_buttons_frame, text="Compare Absolute Difference",
                                          command=self.compare_absolute_difference)
        self.rel_diff_button = ttk.Button(self.compare_buttons_frame, text="Compare Relative Difference",
                                          command=self.compare_relative_difference)

        self.abs_diff_button.grid(row=0, column=0, padx=5, pady=5)
        self.rel_diff_button.grid(row=0, column=1, padx=5, pady=5)

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
        
        
        f1:np.ndarray = np.array(f1)
        f2:np.ndarray = np.array(f2)
        
            # Ensure same number of dimensions by padding the smaller array
        while f1.ndim < f2.ndim:
            f1 = f1.reshape((1,) + f1.shape)
        while f2.ndim < f1.ndim:
            f2 = f2.reshape((1,) + f2.shape)

        # Adjust shapes explicitly for each dimension
        if f1.shape != f2.shape:
            for i in range(f1.ndim):
                if f1.shape[i] == f2.shape[i]:
                    continue

                if f1.shape[i] < f2.shape[i]:  # Expand f1 by repeating cyclically
                    repeats = f2.shape[i] // f1.shape[i]  # Full repeats
                    remainder = f2.shape[i] % f1.shape[i]  # Leftover elements
                    f1 = np.tile(f1, (repeats + (1 if remainder else 0),) + (1,) * (f1.ndim - i - 1))
                    f1 = f1[:f2.shape[i]]  # Trim excess from the end

                elif f1.shape[i] > f2.shape[i]:  # Expand f2 by repeating cyclically
                    repeats = f1.shape[i] // f2.shape[i]
                    remainder = f1.shape[i] % f2.shape[i]
                    f2 = np.tile(f2, (repeats + (1 if remainder else 0),) + (1,) * (f2.ndim - i - 1))
                    f2 = f2[:f1.shape[i]]  # Trim excess from the end

        
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
        
        
        f1:np.ndarray = np.array(f1,copy=True)
        f2:np.ndarray = np.array(f2,copy=True)
        
            # Ensure same number of dimensions by padding the smaller array
        while f1.ndim < f2.ndim:
            f1 = f1.reshape((1,) + f1.shape)
        while f2.ndim < f1.ndim:
            f2 = f2.reshape((1,) + f2.shape)

        # Adjust shapes explicitly for each dimension
        if f1.shape != f2.shape:
            for i in range(f1.ndim):
                if f1.shape[i] == f2.shape[i]:
                    continue

                if f1.shape[i] < f2.shape[i]:  # Expand f1 by repeating cyclically
                    repeats = f2.shape[i] // f1.shape[i]  # Full repeats
                    remainder = f2.shape[i] % f1.shape[i]  # Leftover elements
                    f1 = np.tile(f1, (repeats + (1 if remainder else 0),) + (1,) * (f1.ndim - i - 1))
                    f1 = f1[:f2.shape[i]]  # Trim excess from the end

                elif f1.shape[i] > f2.shape[i]:  # Expand f2 by repeating cyclically
                    repeats = f1.shape[i] // f2.shape[i]
                    remainder = f1.shape[i] % f2.shape[i]
                    f2 = np.tile(f2, (repeats + (1 if remainder else 0),) + (1,) * (f2.ndim - i - 1))
                    f2 = f2[:f1.shape[i]]  # Trim excess from the end
        zmask =f1==0
        fz = np.zeros_like(f1)
        # fz[zmask]=np.spacing(f2)[zmask]
        # Compare relative difference
        diff = np.abs((f1 - f2) / (f1+fz))
        self.plot_comparison(diff, title="Relative Difference")

    def plot_comparison(self, diff, title):
        """Plots the difference data."""
        self.currGrid = diff
        fig = Figure(figsize=(8, 8))
        ax = fig.add_subplot(111)

        ax.imshow(diff)
        ax.set_title(title)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew")
        
        canvas.draw()
        self.canvas = canvas
        # Add Navigation Toolbar
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
        print(file_path)
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
        self.insightButton = ttk.Button(self.treeFrame, text='Get Insight', command=self._error_finder)

        self.reloadButton.pack(fill=tk.X, padx=5, pady=5)
        self.newDirectoryButton.pack(fill=tk.X, padx=5, pady=5)
        self.chooseDataButton.pack(fill=tk.X, padx=5, pady=5)
        self.insightButton.pack(fill=tk.X, padx=5, pady=5)

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

    def on_resize(self, event):
        """Handle resizing of the plot area."""
        self.canvas.get_tk_widget().config(width=event.width, height=event.height)

    def _pick_directory(self):
        """Open a file dialog to select a directory."""
        directory = fdiag.askdirectory()
        if directory:
            self.results_dir = pathlib.Path(directory)

    def _error_finder(self):
        """Dummy method for error finding or handling."""
        msgbox.showinfo("Error Finder", "This is a placeholder function.")




scene = CompareScene