from matplotlib import pyplot as plt
from matplotlib.colorbar import Colorbar
from matplotlib.quiver import Quiver
import numpy as np
from .boundary import geometryFactory as Boundary
from ...Solvers import laplace_ode_solver, findUandV, laplace_ode_solver_step, laplace_ode_solver_continue
import typing
import tkinter as tk
from matplotlib.axes import Axes
from ..task import Task

class Task6(Task):
    name = "EndtoEndLine_9_Point"

    def __init__(self, axes: 'Axes' = None, *args, **kwargs):
        super().__init__(axes=axes, *args, **kwargs)

    def setup(self, height: int, width: int):
        """Setup the grid and boundary condition, display the initial potential."""
        grid = np.zeros(shape=(height, width), dtype=np.float64)
        self.boundaryCondition = Boundary()
        self.grid = self.boundaryCondition(Grid=grid, retoverlay=False)
        
        # Remove old image if it exists
        if self._Image:
            self._Image.remove()
        
        # Display the grid as an image
        self._Image = self.axes.imshow(self.grid, )
        # self._Image.set_clim(vmin=0, vmax=np.max(self.grid))  # Set color limits
        self.axes.set_title('Electrostatic Potential')

    def _show_Efield(self):
        """Display the electric field as quivers."""
        if self.Efield is None:
            raise ValueError('Electric field not computed yet.')
        u_v = self.Efield  # Do not multiply by 25, use as is.
        axes = self.axes
        Xs, Ys = self.Xs, self.Ys
        
        # Remove old quivers if they exist
        if self._quivers:
            self._quivers.remove()

        # Adjust the quiver scale so arrow heads are visible
        self._quivers = axes.quiver(Xs[:-1:5,:-1:5], Ys[:-1:5,:-1:5], u_v[::5, ::5, 0], u_v[::5, ::5, 1], color='b', scale=1, scale_units='xy')

    def __call__(self, *args, **kwargs):
        pass

    def run(self):
        """Solve the Laplace equation and update the grid and electric field."""
        xs, ys, self.grid = laplace_ode_solver_continue(self.grid, self.boundaryCondition, stencil=9, gamma=0.5)
        
        # Create meshgrid for visualization
        self.Xs, self.Ys = np.meshgrid(xs, ys)

        # Compute the electric field components
        self.Efield = findUandV(grid=self.grid)
        
        # Update the image with the new grid
        if self._Image:
            self._Image.remove()
        self._Image = self.axes.imshow(self.grid, )
        # self._Image.set_clim(vmin=0, vmax=np.max(self.grid))  # Set color limits

    def _cleanup(self):
        """Remove all artists from the axes."""
        if self._Image:
            self._Image.remove()
        if self._quivers:
            self._quivers.remove()
        self._Image = None
        self._quivers = None

    def reset(self):
        """Reset the grid and boundary condition."""
        self.grid = np.zeros_like(self.grid)
        self.boundaryCondition = Boundary()  # Reinitialize the boundary condition
        self.setup(self.grid.shape[0], self.grid.shape[1])  # Reset the figure with the grid


