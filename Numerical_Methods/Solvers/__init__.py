# License: None
# Author: P3 Comp. 2025 Lab Group B ( Electrostatics )
# Description: The solver submodule initializer 

from .ftcs import laplace_ode_solver,laplace_ode_solver_step,laplace_ode_solver_continue
import numpy as np


def findUandV(grid:np.ndarray[np.ndarray[np.float64]]):
    E_field = np.zeros([*grid.shape,2],np.float64)
    E_field[:,:-1,0] = grid[:,1:] - grid[:,:-1]
    E_field[:-1,:,1] = grid[1:,:] - grid[:-1,:]
    return -E_field

def relative_tolerance_check(grid:'np.ndarray[np.ndarray[np.float64]]',tol:'np.float64'=1e-6):
    return

def abs_diff_tolerance_check(grid:'np.ndarray[np.ndarray[np.float64]]',tol:'np.float64'=1e-6):
    return

electricFieldFromPotential = findUandV
