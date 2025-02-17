from matplotlib import rc
import numpy as np
from .boundary import geometryFactory as Boundary
from ...Solvers import laplace_ode_solver, findUandV,laplace_ode_solver_step,laplace_ode_solver_continue
import typing
import tkinter as tk
from matplotlib.axes import Axes


rc('image', cmap='PiYG')

class Task1(typing.Callable, typing.Protocol):
    def __init__(self, axes: 'Axes' = None, *args, **kwargs):
        self.axes = axes
        self.boundaryCondition = None

    def setup(self, height: int, width: int):
        grid = np.zeros(shape=(height+1,width+1),dtype=np.float64)
        self.boundaryCondition=Boundary()
        self.grid =grid=self.boundaryCondition(Grid=grid,retoverlay=False)
        self.Xs,self.Ys = np.mgrid[:grid.shape[1], :grid.shape[0]]
        axes = self.axes
        axes.imshow(grid)
        axes.set_title('Electrostatic Potential')
        
    def _show_Efield(self):
        u_v= findUandV(grid=self.grid)[::5,::5]*25
        axes = self.axes
        Xs = self.Xs[::5,::5]
        Ys = self.Ys[::5,::5]
        axes.quiver(Xs, Ys, u_v[:,:,0], u_v[:,:,1], color='b', scale=0.1, scale_units='xy') # Adjust scale and color
        
    def __call__(self, *args, **kwargs):
        pass

    def run(self):
        Xs,Ys,self.grid=laplace_ode_solver_continue(self.grid,self.boundaryCondition)
        self.axes.imshow(self.grid)
        self.axes.figure.colorbar(self.axes.images[0])


    def _cleanup(self):
        pass

    def reset(self):
        pass
