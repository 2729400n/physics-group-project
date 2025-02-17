import typing
from matplotlib.axes import Axes


class Task( typing.Protocol):
    
    'An Iterface for the Tasks class only useful for intelisense.'
    
    name:str='Task'
    def __init__(self, axes: 'Axes' = None, *args, **kwargs): ...

    def setup(self, height: int, width: int): ...
        
    def _show_Efield(self): ...
        

    def run(self): ...
        


    def _cleanup(self): ...
        

    def reset(self): ...