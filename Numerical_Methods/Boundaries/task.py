import typing
from matplotlib.axes import Axes
from matplotlib.figure import Figure

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
        self.exposed_methods = [self.setup,self.run,self._show_Efield]

    def setup(self, height: int, width: int) -> None: ...
    
    def canDraw(self) -> bool: 
        return True

    def redraw(self) -> None:
        pass
        
    def _show_Efield(self) -> None: ...
        

    def run(self) ->None: ...
        


    def _cleanup(self) -> None: ...
        

    def reset(self) -> None: ...