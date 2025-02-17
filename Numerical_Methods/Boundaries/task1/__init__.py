from .boundary import geometryFactory as Boundary
from ...Solvers import laplace_ode_solver,findUandV
import typing
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Task1(typing.Callable,typing.Protocol):
    def __init__(self,frame_or_canvas:'tk.Frame|tk.Canvas|FigureCanvasTkAgg'=None,*args,**kwargs):
        self.canvas = frame_or_canvas
    def setup(self,):
        pass
    def __call__(self,*args,**kwargs):
        pass
    def run(self):
        pass
    def _cleanup(self):
        pass
    def reset(self):
        pass
    

    