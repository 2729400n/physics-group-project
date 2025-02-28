
from .boundary import GeometryFactory as Boundary
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
from ...Solvers import laplace_ode_solver, findUandV,laplace_ode_solver_step,laplace_ode_solver_continue
import typing
import tkinter as tk
from matplotlib.axes import Axes
from ..task import Task

class Task4(Task):
    name="MWPC"
    def __init__(self, axes: 'Axes' = None, *args, **kwargs):
        super().__init__()
        

    def setup(self, x1: float, y1: float, a: float, cx: float,
              cy: float, v: float = 1.0, x0: float = 0.0, y0: float = 0.0,l:float=1.0,
              dy: float = 1.0, dx: float = 1.0,centre:bool=True,nncount:int=1):
        x0, x1 = (x0, x1) if x0 <= x1 else (x1, x0)
        y0, y1 = (y0, y1) if y0 <= y1 else (y1, y0)
        
        print(x0, x1, dx)
        Xs = np.arange(x0, x1+dx, dx)
        Ys = np.arange(y0, y1+dy, dy)

        grid = np.zeros(shape=(Ys.shape[0], Xs.shape[0]), dtype=np.float64)
        self.boundaryCondition=Boundary(radius=a,cx=cx,cy=cy,V=v,seperation=l,center=centre,plate_seperation=l,NNCount=nncount)
        self.grid =grid=self.boundaryCondition(Grid=grid)
        axes = self.axes
        self.Image=axes.imshow(grid)
        axes.set_title('Electrostatic Potential')
        self.cbar= self.figure.colorbar(self.Image)
        
    def _show_Efield(self):
        u_v = self.Efield*25
        axes = self.axes
        Xs, Ys = self.Xs,self.Ys
        axes.quiver(Xs, Ys, u_v[:,:,0], u_v[:,:,1], color='b', scale=0.1, scale_units='xy') # Adjust scale and color
        
    def __call__(self, *args, **kwargs):
        pass

    def run(self):
        Xs, Ys, self.grid = laplace_ode_solver_continue(
            self.grid, self.boundaryCondition)
        if self.cbar is not None:
            self.cbar.remove()
            self.cbar = None
            self.figure.clear()
            axes = self.figure.add_subplot(111)
            self.axes = axes
        self.Image=self.axes.imshow(self.grid)

        self.figure.draw_without_rendering()
        self.figure.colorbar(self.Image)

        self.figure.canvas.draw()


    def _cleanup(self):
        pass

    def reset(self):
        pass


# def poisson(rmax, ymax, xmax, maxpoints, dxy, V):
#     """Solve the Poisson equation with the given parameters using a finite difference method."""
#     # Create the space grids
#     x = np.arange(-xmax, xmax, dxy)
#     y = np.arange(-ymax, ymax, dxy)
#     X, Y = np.meshgrid(x, y)  # Create meshgrid for 2D space
    
#     u = np.zeros_like(X)
#     r = np.sqrt((X-6)**2 + (Y+6)**2)

#     def shape(grid,what,where,howbig,Volt):
#         if what=="circle":
#             r = np.sqrt((X-where[0])**2 + (Y-where[1])**2)
#             grid[r < howbig[0]] = 0
#         elif what=="rectangle":
            
#             # Correcting the conditional slicing
#             x_start = int(where[0] - howbig[0]/2)
#             x_end = int(where[0] + howbig[0]/2)
#             y_start = int(-where[1] - howbig[1]/2)
#             y_end = int(-where[1] + howbig[1]/2)
            
#             # Apply the mask inside the rectangle to set values to 0
#             grid[(X >= x_start) & (X <= x_end) & (Y >= y_start) & (Y <= y_end)] = Volt
        
#     # Apply initial conditions
#     """def bounds(grid):
        
#         #shape(grid,"circle or rectangle",[x,y],[width,height],volt)
#         shape(grid,"rectangle",[0,12],[3,4],0)
#         shape(grid,"rectangle",[0,4],[3,4],V)
#         shape(grid,"rectangle",[0,-4],[3,4],-V)
#         shape(grid,"rectangle",[0,-12],[3,4],0)
        
#         grid[:, 0] = 0        # Left boundary
#         grid[:, -1] = 0      # Right boundary
        
#         # Update the top and bottom boundaries using neighboring points
#         grid[(0,-1), 1:-1] = 0.25*(grid[(0,-1), 2:]+grid[(0,-1), :-2]+grid[(-1,-2), 1:-1]+grid[(1,0), 1:-1])"""
#     def bounds(grid,moving_to_a_side):
        
#         #shape(grid,"circle or rectangle",[x,y],[width,height],volt)
#         shape(grid,"circle",[0,18],[4],0)
#         shape(grid,"circle",[moving_to_a_side,6],[4],0)
#         shape(grid,"circle",[0,-6],[4],0)
#         shape(grid,"circle",[0,-18],[4],0)
        
#         grid[:, 0] = -V        # Left boundary
#         grid[:, -1] = -V      # Right boundary
        
#         # Update the top and bottom boundaries using neighboring points
#         grid[(0,-1), 1:-1] = 0.25*(grid[(0,-1), 2:]+grid[(0,-1), :-2]+grid[(-1,-2), 1:-1]+grid[(1,0), 1:-1])
      
    
#     bounds(u,0)  # Apply the boundary conditions initially
    
    
#     # FTCS scheme for solving the Poisson equation (relaxed elliptical solver)
#     for _ in range(maxpoints):  # You can adjust the number of iterations as needed
#         u_new = u.copy()  # Create a copy of u to avoid overwriting values during updates
        
#         # Update the internal points (ignoring boundaries)
#         for i in range(1, u.shape[0] - 1):
#             for j in range(1, u.shape[1] - 1):
#                 u_new[i, j] = 0.25 * (u[i + 1, j] + u[i - 1, j] + u[i, j + 1] + u[i, j - 1])

        
        
#         # Convergence check: Stop if the difference is small enough
#         diff = np.max(np.abs(u_new - u))
#         if diff < 1e-23:
#             break
#         if _ > (maxpoints-100):
#             bounds(u_new,-4)
#         else: bounds(u_new,0)  # Apply the boundary conditions again after updating the grid
#         u = u_new  # Update the solution
        
#     return u, X, Y

# # Parameters
# rmax = 10   # Radius of internal region set to 0
# ymax = 30  # Maximum y value
# xmax = 10  # Maximum x value
# maxpoints = 1000  # Number of iterations
# dxy = 0.5  # Grid resolution
# V = 10

# # Solve the Poisson equation
# pot, X, Y = poisson(rmax, ymax, xmax, maxpoints, dxy, V)

# grad_x, grad_y = np.gradient(pot, axis=(1,0))

# # Plot the result
# plt.figure(figsize=(7,17))
# Y=Y[::-1,:]
# plt.quiver(X, Y, -grad_x, grad_y, scale=50 , headlength=3, headaxislength=2)
# plt.imshow(pot, extent=(-xmax, xmax, -ymax, ymax), aspect='auto', cmap='pink')

# plt.xlabel('X')
# plt.ylabel('Y')
# plt.colorbar(label='potential')
# plt.title('Solution to the Poisson Equation')

# plt.show()
