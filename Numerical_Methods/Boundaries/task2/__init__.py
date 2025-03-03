import io
from matplotlib import pyplot as plt
import numpy as np
# from .boundary import geometryFactory as Boundary
from ..task2_analytical import Boundary
from ...Solvers import laplace_ode_solver, findUandV,laplace_ode_solver_step,laplace_ode_solver_continue
import typing
import tkinter as tk
from matplotlib.axes import Axes
from ..task import Task
import matplotlib.colors as mcolors

class Task2(Task):
    name="EndtoEndLine"
    def __init__(self, axes: 'Axes' = None, *args, **kwargs):
        super().__init__()
        self.dx=1.0
        self.dy=1.0
        self.resdx=1.0
        self.resdy=1.0
        

    def setup(self, height: float, width: float,V:float=1.0,r:float=35.0,cx:float=50,cy:float=100,dy:float=1.0,dx:float=1.0):
        self.dx=dx
        self.dy=dy
        self.resdx=dx
        self.resdy=dy
        grid = np.zeros(shape=(height,width),dtype=np.float64)
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
        u_v=self.Efield = findUandV(grid=self.grid)
        axes = self.axes
        Xs, Ys = self.Xs, self.Ys
        
        # Remove previous quivers if they exist
        if self._quivers:
            self._quivers.remove()

        Xs,Ys,U,V=(Xs[::5,::5], Ys[::5,::5], u_v[::5, ::5, 0], u_v[::5, ::5, 1])
            
        # Compute the magnitude of the vectors
        M = np.sqrt(U**2 + V**2)

        # Normalize the vectors (avoid division by zero)
        U_norm = U / (M + 1e-10)
        V_norm = V / (M + 1e-10)

        # Create a color map based on the magnitudes
        norm = mcolors.Normalize(vmin=M.min(), vmax=M.max())
        # Plot the quiver with normalized vectors and colored by magnitude
        axes.quiver(Xs, Ys, U_norm, V_norm, M, scale=0.1, scale_units='xy', angles='xy',  norm=norm)
        
    def redraw(self):
        '''Redraw the grid and other plot elements.'''
        if self.grid is None:
            return
        if self.axes is not None:
            self.axes.clear()
            
            self._Image = self.axes.imshow(self.grid)
            if self.cbar is None:
                self.cbar = self.figure.colorbar(self._Image,ax=self.axes)

    def run(self,maxruns:int=1000,stencil:int=5,gamma:float=0.0,abs_tol:float=1e-9,rel_tol:float=1e-6):
        '''Solve the Laplace equation and update the grid and electric field.'''
        Xs, Ys, self.grid = laplace_ode_solver_continue(self.grid, self.boundaryCondition,max_iterations=maxruns,
                                                        abs_tol=abs_tol,rel_tol=rel_tol,resolution=(self.resdx,self.resdy),
                                                        stencil=stencil,gamma=gamma,wrap=True,wrap_direction='both')
        
        # Remove the previous colorbar and reset it
        if self._cbar is not None:
            try:
                self._cbar.remove()
            except:
                pass

        self.axes.imshow(self.grid, )
        # self._cbar = self.figure.colorbar(self._Image, ax=self.axes)

        self.figure.canvas.draw()


    def _cleanup(self):
        '''Remove all artists from the axes and reset class attributes.'''
        if self._Image:
            try:
                self._Image.remove()
            except:
                pass
        if self._quivers is not None:
            try:
                self._quivers.remove()
            except:
                pass
        if self._cbar is not None:
            try:
                self._cbar.remove()
            except:
                pass

        self._Image = None
        self._quivers = None
        self._cbar = None
        self.grid = None
        if self.axes is not None:
            self.axes.remove()
            self.axes=self.figure.add_subplot(1,1,1)

    def reset(self):
        '''Reset the grid and boundary condition to initial state.'''
        if self.grid is not None:
            self.grid[:, :] = 0

    def save_grid(self):
        '''Save the grid to a file.'''
        if self.grid is None:
            return (None, None)
        outfile = io.BytesIO()
        np.save(outfile, self.grid, allow_pickle=True)
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_grid.npy', outfile.read()

    def save_figure(self):
        '''Save the current figure to a file.'''
        if self.figure is None:
            return
        outfile = io.BytesIO()
        self.figure.savefig(outfile, format='png')
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_figure.png', outfile.read()