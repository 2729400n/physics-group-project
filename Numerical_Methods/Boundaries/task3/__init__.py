from matplotlib.figure import Figure
from .boundary import highSpeedFactory as Boundary

from matplotlib import pyplot as plt
import numpy as np
from ...Solvers import laplace_ode_solver, findUandV,laplace_ode_solver_step,laplace_ode_solver_continue
import typing
import tkinter as tk
from matplotlib.axes import Axes
from ..task import Task

class Task3(Task):
    name = "HighSpeed"
    def __init__(self, figure: 'Axes|Figure' = None, *args, **kwargs):
        super().__init__(figure,*args,**kwargs)

    def setup(self, height: int, width: int):
        grid = np.zeros(shape=(height,width),dtype=np.float64)
        self.boundaryCondition=Boundary(width=width,height=height)
        self.grid =grid=self.boundaryCondition(Grid=grid,retoverlay=False)
        axes = self.axes
        axes.imshow(grid)
        axes.set_title('Electrostatic Potential')
        
    def _show_Efield(self):
        u_v = self.Efield*25
        axes = self.axes
        Xs, Ys = self.Xs,self.Ys
        axes.quiver(Xs, Ys, u_v[:,:,0], u_v[:,:,1], color='b', scale=0.1, scale_units='xy') # Adjust scale and color
        

    def run(self):
        xs,ys,self.grid=laplace_ode_solver_continue(self.grid,self.boundaryCondition)
        self.Xs, self.Ys = np.meshgrid(xs[:-1:5], ys[:-1:5])
        self.Efield = findUandV(grid=self.grid)[::5,::5]
        self.axes.imshow(self.grid)


    def _cleanup(self):
        pass

    def reset(self):
        pass