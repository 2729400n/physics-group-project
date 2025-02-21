import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ..task import Task

class Task4(Task):
    def __init__(self):
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
