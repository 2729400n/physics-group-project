import io
import typing
from matplotlib.axes import Axes
from matplotlib.colorbar import Colorbar
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.quiver import Quiver
from matplotlib.text import Text
import numpy as np
from ..Solvers import laplace_ode_solver, findUandV,laplace_ode_solver_step,laplace_ode_solver_continue
from ..utils.naming import slugify
from time import strftime
tasks:'set[Task]' = set()

    
# Our task Class
class Task(typing.Protocol):
    
    'An Interface for the Tasks class should be subclassed to add new tasks'
    
    name: str = 'Task'
    instance: 'Task'
    

    def __init__(self, figure: 'Figure|Axes' = None, *args, **kwargs):
        self.figure = None
        self.axes = None
        if isinstance(figure, Figure):
            self.figure: Figure = figure
            if figure.axes:
                figure.clf()
            self.axes: Axes = figure.add_subplot(111)
        elif isinstance(figure, Axes):
            self.axes: Axes = figure
            self.figure: Figure = figure.figure
        elif figure is None:
            self.figure = Figure()
            self.axes = self.figure.add_subplot(111)
        else:
            raise TypeError(f'Got Class {figure.__class__} \r\nfigure= Must be a Figure or Axes Object')
        self.boundaryCondition = None
        
        self._Image: AxesImage = None
        self.grid = None
        self._cbar: Colorbar = None
        self._quivers: Quiver = None
        self.exposed_methods = [self.setup, self.run, self._show_Efield,self.adjust_plot]
        self.savables: 'dict[str,typing.Callable[[],tuple[str,bytes]]]' = {'Grid': self.save_grid, 'Figure': self.save_figure,'ALL_DATA':self.save_all_numerical}
        self.Efield = None
        self.all_data =None
        


    def setup(self, height: int, width: int) -> None: ...
    
    def __init_subclass__(cls):
        global tasks
        tasks.add(cls)
        return super().__init_subclass__()

    def canDraw(self) -> bool:
        return True

    def redraw(self) -> None:
        pass

    def _find_Efield(self) ->None:
        '''Display the electric field as quivers.'''
        self.Efield = findUandV(grid=self.grid)
        
        
        # Remove previous quivers if they exist
        if self._quivers:
            self._quivers.remove()
    
    def _show_Efield(self)->None:...

    def run(self) -> None: ...

    def _cleanup(self) -> None: 
        self.grid=None
        self.Efield=None
        self.Image=None
        self.cbar=None
        self.quivers=None
        self.__init__()


    def reset(self) -> None: ...
    
    @classmethod
    def make_task(self):
        if (self.instance):
            pass
            

    def save_grid(self):
        if self.grid is None:
            return (None, None)
        outfile = io.BytesIO()
        np.save(outfile, self.grid, allow_pickle=True)
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_grid.npy', outfile.read()

    def save_figure(self):
        if self.figure is None:
            return
        outfile = io.BytesIO()
        self.figure.savefig(outfile, format='png')
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_figure.png', outfile.read()

    @property
    def Image(self) -> AxesImage:
        return self._Image

    @Image.setter
    def Image(self, img_data: np.ndarray):
        """Sets a new image and removes the previous one if it exists."""
        if img_data is None:
            self._Image = None
            return
        if self._Image:
            try:
                self._Image.remove()
            except:
                pass
        if isinstance(img_data, (list,tuple,np.ndarray)):
            img_data = np.array(img_data)
        if isinstance(img_data,np.ndarray):
            self._Image = self.axes.imshow(img_data)
        elif isinstance(img_data,AxesImage):
            self._Image=img_data

    @property
    def cbar(self) -> Colorbar:
        return self._cbar

    @cbar.setter
    def cbar(self, value: Colorbar):
        """Sets a new colorbar and removes the previous one if it exists."""
        if self._cbar is not None:
            try:
                self._cbar.remove()
            except:
                pass
        self._cbar = value

    @property
    def quivers(self) -> Quiver:
        return self._quivers

    @quivers.setter
    def quivers(self, value: Quiver):
        """Sets new quivers and removes the previous ones if they exist."""
        if self._quivers is not None:
            try:
                self._quivers.remove()
            except:
                pass
        self._quivers = value

    def update_plot(self):
        """Update the figure to reflect changes."""
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        
    # New method to adjust figure size, font size, and axis limits
    def adjust_plot(self, figsize_w: float=12, figsize_h:float = 12, fontsize: float = 12,FigTitle:str="",XLabel:str='',YLabel:str='',axesTitle:str='',
                    FigTitlefontSize:float=16,axesTitlefontSize:float=16, ylabelfontsize:float=16,xlabelFontSize:float=16,tight_layout:bool=False,dpi:int=64):
        """Adjust figure size, font size, and axis limits."""
        if self.figure is None or self.axes is None:
            raise Exception('Cannot save to empty Figure')
        self.figure.draw_without_rendering()
        if (figsize_w is not None) and (figsize_h is not None):
            self.figure.set_dpi(dpi)
            self.figure.set_size_inches(figsize_w, figsize_h, forward=False,)
        
        for label in self.axes.get_xticklabels() + self.axes.get_yticklabels():
            label.set_fontsize(fontsize)
            
        ylabel =self.axes.set_ylabel(YLabel)
        xlabel=self.axes.set_xlabel(XLabel)
        #
        
        ylabel.set_fontsize(ylabelfontsize)
        xlabel.set_fontsize(ylabelfontsize)
        #
        #
        self.axes.set_title(axesTitle)
        self.axes.title.set_fontsize(axesTitlefontSize)
        #
        #
        title=self.figure.suptitle(FigTitle,)
        title.set_fontsize(FigTitlefontSize)
        
        self.figure.draw_without_rendering()
        if (figsize_w is not None) and (figsize_h is not None):
            self.figure.set_size_inches(figsize_w, figsize_h, forward=True)
        
        if tight_layout:
            self.figure.tight_layout()
    
    
    def save_grid(self):
        '''Save the grid to a file.'''
        if self.grid is None:
            return (None, None)
        outfile = io.BytesIO()
        np.save(outfile, self.grid, allow_pickle=True)
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_grid.npy', outfile.read()

    def save_figure(self):
        '''Save the current figure to a file.'''
        if self.figure is None:
            return
        outfile = io.BytesIO()
        self.figure.savefig(outfile, format='png')
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_figure.png', outfile.read()
    
    def _load_data(self):
        self.all_data = {'potential':self.grid,'e_field':self.Efield}
        return
    
    def save_all_numerical(self):
        '''Save the grid to a file.'''
        for i in self.all_data:
            if i is None:
                raise 'Cannot save all data if you havent generated it yet'
        outfile = io.BytesIO()
        np.savez(outfile, allow_pickle=True,kwds=self.all_data)
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return f'{slugify(self.name)}_{strftime("%Y-%m-%d_%H_%M_%S")}_data.npz', outfile.read()