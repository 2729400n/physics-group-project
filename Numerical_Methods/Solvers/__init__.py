# License: None
# Author: P3 Comp. 2025 Lab Group B ( Electrostatics )
# Description: The solver submodule initializer 

from .ftcs import laplace_ode_solver
import numpy as np


def findUandV(grid:np.ndarray[np.ndarray[np.float64]]):
    E_field = np.zeros([*grid.shape,2],np.float64)
    E_field[:,:-1,0] = grid[:,1:] - grid[:,:-1]
    E_field[:-1,:,1] = grid[1:,:] - grid[:-1,:]
    return E_field

electricFieldFromPotential = findUandV
