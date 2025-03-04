# License: None
# Author: P3 Comp. 2025 Lab Group B ( Electrostatics )
# Description: The solver submodule initializer 

from .ftcs import laplace_ode_solver,laplace_ode_solver_step,laplace_ode_solver_continue
import numpy as np


def findUandV(grid: np.ndarray, dx: float = 1.0, dy: float = 1.0):
    E_field = np.zeros((*grid.shape, 2), dtype=np.float64)

    # Compute Ex = -dΦ/dx using central differences
    E_field[1:-1, :, 0] = -(grid[2:, :] - grid[:-2, :]) / (2 * dx)
    E_field[0, :, 0] = -(grid[1, :] - grid[0, :]) / dx  # Forward difference at first row
    E_field[-1, :, 0] = -(grid[-1, :] - grid[-2, :]) / dx  # Backward difference at last row

    # Compute Ey = -dΦ/dy using central differences
    E_field[:, 1:-1, 1] = -(grid[:, 2:] - grid[:, :-2]) / (2 * dy)
    E_field[:, 0, 1] = -(grid[:, 1] - grid[:, 0]) / dy  # Forward difference at first column
    E_field[:, -1, 1] = -(grid[:, -1] - grid[:, -2]) / dy  # Backward difference at last column

    return E_field

def relative_tolerance_check(grid:'np.ndarray[np.ndarray[np.float64]]',tol:'np.float64'=1e-6):
    return

def abs_diff_tolerance_check(grid:'np.ndarray[np.ndarray[np.float64]]',tol:'np.float64'=1e-6):
    return

electricFieldFromPotential = findUandV
