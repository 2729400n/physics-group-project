from matplotlib import pyplot as plt
import numpy as np
from .boundary import geometryFactory as Boundary
from ...Solvers import laplace_ode_solver, findUandV,laplace_ode_solver_step,laplace_ode_solver_continue
import typing
import tkinter as tk
from matplotlib.axes import Axes
from ..task import Task

class Task6(Task):
    name="EndtoEndLine_9_Point"
    def __init__(self, axes: 'Axes' = None, *args, **kwargs):
        super().__init__()
        

    def setup(self, height: int, width: int):
        grid = np.zeros(shape=(height,width),dtype=np.float64)
        self.boundaryCondition=Boundary()
        self.grid =grid=self.boundaryCondition(Grid=grid,retoverlay=False)
        axes = self.axes
        axes.imshow(grid)
        axes.set_title('Electrostatic Potential')
        
    def _show_Efield(self):
        u_v = self.Efield*25
        axes = self.axes
        Xs, Ys = self.Xs,self.Ys
        axes.quiver(Xs, Ys, u_v[:,:,0], u_v[:,:,1], color='b', scale=0.1, scale_units='xy') # Adjust scale and color
        
    def __call__(self, *args, **kwargs):
        pass

    def run(self):
        xs,ys,self.grid=laplace_ode_solver_continue(self.grid,self.boundaryCondition,stencil=5,stencil=9,gamma=0.5)
        self.Xs, self.Ys = np.meshgrid(xs[:-1:5], ys[:-1:5])
        self.Efield = findUandV(grid=self.grid)[::5,::5]
        self.axes.imshow(self.grid)


    def _cleanup(self):
        pass

    def reset(self):
        pass