from matplotlib import rc
from matplotlib.colorbar import Colorbar
from matplotlib.quiver import Quiver
import numpy as np
from .boundary import geometryFactory as Boundary
from ...Solvers import laplace_ode_solver, findUandV,laplace_ode_solver_step,laplace_ode_solver_continue
import typing
import tkinter as tk
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from ..task import Task



class Task1(Task):
    name="Anulus"
    def __init__(self, axes: 'Axes' = None, *args, **kwargs):
        super().__init__()
        self.Image : AxesImage = None

    def setup(self, height: int, width: int):
        grid = np.zeros(shape=(height+1,width+1),dtype=np.float64)
        self.boundaryCondition=Boundary()
        self.cbar:Colorbar = None
        self.quivers:Quiver=None
        self.grid = grid=self.boundaryCondition(Grid=grid,retoverlay=False)
        self.Xs,self.Ys = np.mgrid[:grid.shape[1], :grid.shape[0]]
        axes = self.axes
        img=self.Image = axes.imshow(grid)
        
        axes.set_title('Electrostatic Potential')
        self.figure.canvas.figure = None
        self.figure.canvas.figure = self.figure
        self.figure.canvas.draw_idle()
        print(self.grid)
        
    def _show_Efield(self):
        u_v= findUandV(grid=self.grid)[::5,::5]*25
        axes = self.axes
        Xs = self.Xs[::5,::5]
        Ys = self.Ys[::5,::5]
        if self.quivers is not None:
            self.quivers.set_visible(False)
            self.quivers.remove()
            self.quivers = None
        quiv=axes.quiver(Xs, Ys, u_v[:,:,0], u_v[:,:,1], color='b', scale=0.1, scale_units='xy') # Adjust scale and color
        self.quivers=quiv
        
        
        
    def run(self):
        Xs,Ys,self.grid=laplace_ode_solver_continue(self.grid,self.boundaryCondition)
        if self.cbar is not None:
            self.cbar.remove()
            self.cbar = None
            self.figure.clear()
            axes=self.figure.add_subplot(111)
            self.axes = axes
        self.axes.imshow(self.grid)
        
        self.figure.draw_without_rendering()
        self.figure.colorbar(self.axes.images[0])
        
        self.figure.canvas.draw()
        


    def _cleanup(self):
        pass

    def reset(self):
        pass
