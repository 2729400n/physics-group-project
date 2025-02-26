import io
import typing
from matplotlib.axes import Axes
from matplotlib.colorbar import Colorbar
from matplotlib.figure import Figure
from matplotlib.image import AxesImage
from matplotlib.quiver import Quiver
import numpy as np

    
tasks:'set[Task]' = set()
# Our task Class
class Task( typing.Protocol):
    
    'An Iterface for the Tasks class should be subclassed to add new tasks'
    
    name:str='Task'
    def __init__(self, figure: 'Figure|Axes' = None, *args, **kwargs):
        self.figure=None
        self.axes=None
        if isinstance(figure,Figure):
            self.figure:Figure = figure
            if figure.axes:
                figure.clf()
            self.axes:Axes = figure.add_subplot(111)
        elif isinstance(figure,Axes):
            self.axes:Axes = figure
            self.figure:Figure = figure.figure
        elif figure is None:
            self.figure = Figure()
            self.axes = self.figure.add_subplot(111)
        else:
            raise TypeError(f'Got Class {figure.__class__} \r\nfigure= Must be a Figure or Axes Object')
        self.boundaryCondition = None
        
        self.Image: AxesImage = None
        self.grid = None
        self.cbar: Colorbar = None
        self.quivers: Quiver = None
        self.exposed_methods = [self.setup,self.run,self._show_Efield]
        self.savables:'dict[str,typing.Callable[[],tuple[str,bytes]]]'  = {'Grid': self.save_grid,'Figure':self.save_figure}
        
    def setup(self, height: int, width: int) -> None: ...
    
    def __init_subclass__(cls):
        global tasks
        tasks.add(cls)
        return super().__init_subclass__()
    
    def canDraw(self) -> bool: 
        return True

    def redraw(self) -> None:
        pass
        
    def _show_Efield(self) -> None: ...
        

    def run(self) ->None: ...
        


    def _cleanup(self) -> None: ...
        

    def reset(self) -> None: ...
    
    def save_grid(self):
        if self.grid is None:
            return (None,None)
        outfile = io.BytesIO()
        np.save(outfile,self.grid,allow_pickle=True)
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_grid.npy',outfile.read()
    
    def save_figure(self):
        if self.figure is None:
            return
        outfile = io.BytesIO()
        self.figure.savefig(outfile,format='png')
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_figure.png',outfile.read()