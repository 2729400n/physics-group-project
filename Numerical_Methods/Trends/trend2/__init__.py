from matplotlib import pyplot as plt
import numpy as np
from .boundary import geometryFactory as Boundary
from ...Solvers import laplace_ode_solver, findUandV,laplace_ode_solver_step,laplace_ode_solver_continue
import typing
import tkinter as tk
from matplotlib.axes import Axes
from ..task import Task

class Task2(Task):
    name="EndtoEndLine"
    def __init__(self, axes: 'Axes' = None, *args, **kwargs):
        super().__init__()
        self.dx=1.0
        self.dy=1.0
        

    def setup(self, height: float, width: float,V:float=1.0,r:float=35.0,cx:float=50,cy:float=100,dy:float=1.0,dx:float=1.0):
        self.dx=dx
        self.dy=dy
        grid = np.zeros(shape=(height,width),dtype=np.float64)
        self.boundaryCondition=Boundary(val=V,r=r,cx=cx,cy=cy)
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

    def run(self,maxruns=10000,gamma:float=0,stencil:int=5,abs_tol:float=1e-9,rel_tol:float=1e-6):
        xs,ys,self.grid=laplace_ode_solver_continue(self.grid,self.boundaryCondition,max_iterations=maxruns,abs_tol=abs_tol,rel_tol=rel_tol,stencil=stencil,gamma=gamma)
        self.Xs, self.Ys = np.meshgrid(xs[:-1:5], ys[:-1:5])
        self.Efield = findUandV(grid=self.grid)[::5,::5]
        self.axes.imshow(self.grid)


    def _cleanup(self):
        pass

    def reset(self):
        pass