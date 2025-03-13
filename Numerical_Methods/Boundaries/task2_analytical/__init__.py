from matplotlib import pyplot as plt
import numpy as np
from .boundary import GeometryFactory as Boundary
from ...Solvers import laplace_ode_solver, findUandV,laplace_ode_solver_step,laplace_ode_solver_continue
import typing
import tkinter as tk
from matplotlib.axes import Axes
from ..task import Task
import matplotlib.colors as mcolors

class Task2_A(Task):
    name="EndtoEndLine Analytical"
    def __init__(self, axes: 'Axes' = None, *args, **kwargs):
        super().__init__()
        self.Efield = None
        self.dx=1.0
        self.dy=1.0
        self.Xs=None
        self.Ys=None
        self.resXs = None
        self.resYs = None
        self.resdx = None
        self.resdy = None
        

    def setup(self, height: float, width: float,V:float=1.0,r:float=35.0,cx:float=50,cy:float=100,dy:float=1.0,dx:float=1.0):
        self.dx=dx
        self.dy=dy
        self.Ys,self.Xs = np.mgrid[0:height:dy, :width:dx]
        grid = np.zeros_like(self.Xs,dtype=np.float64)
        self.boundaryCondition=Boundary(val=V,r=r,cx=cx,cy=cy)
        self.grid =grid=self.boundaryCondition(Grid=grid,retoverlay=False)
        self.Xs, self.Ys = np.mgrid[:grid.shape[1], :grid.shape[0]]
        self.resXs = self.Xs
        self.resYs = self.Ys
        self.resdx = dx
        self.resdy = dy
        self.dx=dx#
        self.dy=dy
        axes = self.axes
        axes.imshow(grid)
        axes.set_title('Electrostatic Potential')
        
    def _show_Efield(self):
        '''Display the electric field as quivers.'''
        if(self.Efield is None):
            return
        axes = self.axes
        Xs, Ys = self.Xs, self.Ys
        
        # Remove previous quivers if they exist
        if self._quivers:
            self._quivers.remove()

        Xs,Ys,U,V=(Xs[::5,::5], Ys[::5,::5], self.Efield[::5, ::5, 0], self.Efield[::5, ::5, 1])
            
        # Compute the magnitude of the vectors
        M = np.sqrt(U**2 + V**2)

        # Normalize the vectors (avoid division by zero)
        U_norm = U / (M + 1e-10)
        V_norm = V / (M + 1e-10)

        # Create a color map based on the magnitudes
        norm = mcolors.Normalize(vmin=M.min(), vmax=M.max())
                    
        # Plot the quiver with normalized vectors and colored by magnitude
        axes.quiver(Xs, Ys, U_norm, V_norm, M, scale=0.1, scale_units='xy', angles='xy',  norm=norm)
        
    def __call__(self, *args, **kwargs):
        pass

    def run(self):
        '''Solve the Laplace equation and update the grid and electric field.'''
        self.grid,self.Efield = self.boundaryCondition.calculateField(self.grid)
        
        # Remove the previous colorbar and reset it
        if self._cbar is not None:
            try:
                self._cbar.remove()
            except:
                pass

        self.axes.imshow(self.grid, )
        self._cbar = self.figure.colorbar(self._Image, ax=self.axes)

        self.figure.canvas.draw()


    def _cleanup(self):
        pass

    def reset(self):
        pass