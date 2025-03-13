# License: None
# Author: P3 Comp. 2025 Lab Group B ( Electrostatics )
# Description: A module of utilities for the Numerical Solver

# Load modules and imports neceasasary

from typing import Callable, Literal
import numpy as np

# we will be using 64bit floating point representation
# Stay clear of recursion if possible it a bad game to play unless you have
# a hop up or hop out scheme


# Some easy to remember utils for readability
def doNothing(x: 'np.ndarray | tuple[int,int]' = None, *args, **kwargs):
    if isinstance(x, tuple):
        return np.zeros(x, np.float64)
    return x # Some COMMNT


# We gonna solve this in a suitably fashion guys ☺
def laplace_ode_solver(size: 'tuple[int,int]|np.ndarray[int,int]',
    fixedConditions: 'Callable' = doNothing,
    startingShape: 'Callable' = doNothing,
    resolution: tuple[float, float] | str = (1.0, 1.0),
    overlaySaver: bool = False,
    stencil: Literal[5, 9] = 5,
    gamma: float = 0.0,
    wrap: bool = False,
    wrap_direction: Literal["both", "x", "y", "none"] = "none",
    rel_tol: float = 1e-6,
    abs_tol: float = 1e-12,
    max_iterations: int = 10_000):
    # TODO: Fix docstrings adding more detail to params
    """Solves the Laplace equation using a finite difference scheme.

    Args:
        size: A tuple (x_size, y_size) specifying the grid dimensions.
        resolution: A tuple (dx, dy) specifying the grid spacing or a string 'auto' for automatic resolution.
        fixedCondtions: A function that enforces boundary conditions on the potential grid.
        startingshape: A function that defines the initial shape of the potential grid.
        overlaySaver: A flag to ensure that the user can use overlay returning boundary functions
        stencil: A flag that tells wether to use 5-point or nine point stencils
        gamma: The factor by which he diagonals matter if using 9 point stencil 

    Returns:
        A NumPy array representing the electric potential at all grid points.
    """

    dx, dy = resolution if isinstance(resolution, tuple) else (1.0, 1.0)
    w_x_h = np.array(size, dtype=np.float64)
    preception = np.array(resolution, dtype=np.float64)
    pixel_w_X_h = w_x_h/preception

    # two frames to allow rotation/Cyling and comparisons

    Xs = np.arange(0, w_x_h[0]+resolution[0], resolution[0])
    Ys = np.arange(0, w_x_h[1]+resolution[1], resolution[1])
    # Frames  = np.zeros((2,int(pixel_w_X_h[1]),int(pixel_w_X_h[0])))

    sqrt_a = dy / dx
    a = sqrt_a**2
    
    b = dy**2 + dx**2
    sqrt_b = np.sqrt(b)
    
    Frames = np.zeros((2, Ys.shape[0], Xs.shape[0]))

    if overlaySaver:
        Frames[0], overlay = startingShape(Frames[0], retoverlay=True)
    else:
        Frames[0] = startingShape(Frames[0])
        overlay = None

    if stencil == 9:
        diagamult = gamma*(1/8)
        adjacentmult = (1-gamma*(1/2))/4
    elif stencil == 5:
        diagamult = 0
        adjacentmult = 0.25
    else:
        raise ValueError(f'Cannot use a {stencil}-point stencil')

    # print("Multipliers=", (adjacentmult, diagamult))
    # print(Xs.shape[0], Ys.shape[0])
    
    i = 0
    while i < max_iterations:
        ForwardHSpace_A2f = Frames[i % 2, 1:-1, 2:]
        BackwardHSpace_A2f = Frames[i % 2, 1:-1, :-2]
        ForwardVSpace_A2f = Frames[i % 2, 2:, 1:-1]
        BackwardVSpace_A2f = Frames[i % 2, :-2, 1:-1]
        
        DiagForwardUp = Frames[i % 2, 2:, 2:]
        DiagForwardDown = Frames[i % 2, :-2, 2:]
        DiagBackUp = Frames[i % 2, 2:, :-2]
        DiagBackDown = Frames[i % 2, :-2, :-2]
        
        Frames[(i+1) % 2, 1:-1, 1:-1] = adjacentmult * (
            a * (ForwardHSpace_A2f + BackwardHSpace_A2f) + (ForwardVSpace_A2f + BackwardVSpace_A2f)
        ) + diagamult * (DiagBackUp + DiagBackDown + DiagForwardDown + DiagForwardUp)
        
        if wrap:
            if wrap_direction in ["both", "y"]:
                Frames[(i+1) % 2, (0, -1), 1:-1] = adjacentmult * (
                    a * (Frames[i % 2, (0, -1), 2:] + Frames[i % 2, (0, -1), :-2]) +
                    (Frames[i % 2, (-1, -2), 1:-1] + Frames[i % 2, (1, 0), 1:-1])
                )  + diagamult * (
                    Frames[i % 2, (1, 0), 2:] + Frames[i % 2, (-1, -2), 2:] +
                    Frames[i % 2, (1, 0), :-2] + Frames[i % 2, (-1, -2), :-2]
                ) 
            if wrap_direction in ["both", "x"]:
                Frames[(i+1) % 2, 1:-1, (0, -1)] = adjacentmult * (
                    a * (Frames[i % 2, 1:-1, (-1, -2)] + Frames[i % 2, 1:-1, (1, 0)]) +
                    (Frames[i % 2, 2:, (0, -1)] + Frames[i % 2, :-2, (0, -1)])
                )  + diagamult * (
                    Frames[i % 2, :-2, (-1, -2)] + Frames[i % 2, 2:, (-1, -2)] +
                    Frames[i % 2, :-2, (1, 0)] + Frames[i % 2, 2:, (1, 0)]
                ) 
        
        Frames[(i+1) % 2] = fixedConditions(Frames[(i+1) % 2])
        
        indexes = Frames[(i+1) % 2] != 0
        diff = np.abs((Frames[0][indexes] - Frames[1][indexes]) / Frames[(i+1) % 2][indexes])
        
        # Convergence check
        absdiff = np.abs((Frames[i % 2] - Frames[(i+1) % 2]))
        indexes = Frames[(i+1) % 2] > np.spacing(absdiff) 
        reldiff = np.abs(absdiff[indexes] / Frames[(i+1) % 2][indexes])
        
        at_equilibrium = False
        if np.size(reldiff) > 0:
            max_diff = np.max(reldiff)
            if max_diff < rel_tol:
                at_equilibrium = True
        else:
            if np.max(absdiff) < abs_tol:
                at_equilibrium = True
                
        if at_equilibrium:
            break
        
        i += 1
    
    return Ys, Xs, Frames[i % 2]


def laplace_ode_solver_continue(
    Grid: np.ndarray,
    fixedConditions: 'Callable' = doNothing,
    startingShape: 'Callable' = doNothing,
    resolution: tuple[float, float] = (1.0, 1.0),
    overlaySaver: bool = False,
    stencil: Literal[5, 9] = 5,
    gamma: float = 0.0,
    wrap: bool = False,
    wrap_direction: Literal["both", "x", "y", "none"] = "none",
    rel_tol: float = 1e-6,
    abs_tol: float = 1e-9,
    max_iterations: int = 10_000
):
    """Solves the Laplace equation using a finite difference scheme.

    Args:
        Grid: A 2D NumPy array representing the initial grid.
        fixedConditions: A function that enforces boundary conditions on the potential grid.
        startingShape: A function that defines the initial shape of the potential grid.
        resolution: A tuple (dx, dy) specifying the grid spacing or 'auto' for automatic resolution.
        stencil: Choose between a 5-point or 9-point stencil.
        gamma: A parameter controlling diagonal weighting for the 9-point stencil.
        wrap: If True, applies periodic boundary conditions.
        wrap_direction: Determines which axes wrap ('both', 'x', 'y', or 'none').
        rel_tol: Relative tolerance for convergence.
        abs_tol: Absolute tolerance for convergence.
        max_iterations: Maximum number of iterations to prevent infinite loops.

    Returns:
        A tuple containing the Y and X coordinate arrays and the final potential grid.
    """
    dx, dy = resolution if isinstance(resolution, tuple) else (1.0, 1.0)
    
    sqrt_a = dy / dx
    a = sqrt_a**2
    
    b = dy**2 + dx**2
    sqrt_b = np.sqrt(b)
    
    Frames = np.zeros((2, *Grid.shape), dtype=np.float64)
    Frames[0] = startingShape(Grid)
    
    Xs = np.arange(0, Grid.shape[1], 1)
    Ys = np.arange(0, Grid.shape[0], 1)
    
    if stencil == 9:
        diagamult = gamma / (2.0*b)
        adjacentmult = (1 - gamma) / (2.0 * (a + 1))
    elif stencil == 5:
        diagamult = 0
        adjacentmult = 1 / (2.0 * (a + 1))
    else:
        raise ValueError(f"Cannot use a {stencil}-point stencil. Only offer 9 and 5 point stencils")
    
    # print("Multipliers=", (adjacentmult, diagamult))
    # print(Xs.shape[0], Ys.shape[0])
    
    i = 0
    while True if ((max_iterations < 0) or (max_iterations  is None)) else (i < max_iterations):
        ForwardHSpace_A2f = Frames[i % 2, 1:-1, 2:]
        BackwardHSpace_A2f = Frames[i % 2, 1:-1, :-2]
        ForwardVSpace_A2f = Frames[i % 2, 2:, 1:-1]
        BackwardVSpace_A2f = Frames[i % 2, :-2, 1:-1]
        
        DiagForwardUp = Frames[i % 2, 2:, 2:]
        DiagForwardDown = Frames[i % 2, :-2, 2:]
        DiagBackUp = Frames[i % 2, 2:, :-2]
        DiagBackDown = Frames[i % 2, :-2, :-2]
        
        Frames[(i+1) % 2, 1:-1, 1:-1] = adjacentmult * (
            a * (ForwardHSpace_A2f + BackwardHSpace_A2f) + (ForwardVSpace_A2f + BackwardVSpace_A2f)
        ) + diagamult * (DiagBackUp + DiagBackDown + DiagForwardDown + DiagForwardUp)
        
        if wrap:
            if wrap_direction in ["both", "y"]:
                Frames[(i+1) % 2, (0, -1), 1:-1] = adjacentmult * (
                    a * (Frames[i % 2, (0, -1), 2:] + Frames[i % 2, (0, -1), :-2]) +
                    (Frames[i % 2, (-1, -2), 1:-1] + Frames[i % 2, (1, 0), 1:-1])
                )  + diagamult * (
                    Frames[i % 2, (1, 0), 2:] + Frames[i % 2, (-1, -2), 2:] +
                    Frames[i % 2, (1, 0), :-2] + Frames[i % 2, (-1, -2), :-2]
                ) 
            if wrap_direction in ["both", "x"]:
                Frames[(i+1) % 2, 1:-1, (0, -1)] = adjacentmult * (
                    a * (Frames[i % 2, 1:-1, (-1, -2)] + Frames[i % 2, 1:-1, (1, 0)]) +
                    (Frames[i % 2, 2:, (0, -1)] + Frames[i % 2, :-2, (0, -1)])
                )  + diagamult * (
                    Frames[i % 2, :-2, (-1, -2)] + Frames[i % 2, 2:, (-1, -2)] +
                    Frames[i % 2, :-2, (1, 0)] + Frames[i % 2, 2:, (1, 0)]
                ) 
        
        Frames[(i+1) % 2] = fixedConditions(Frames[(i+1) % 2])
        
        
        # Convergence check
        absdiff = np.abs((Frames[i % 2] - Frames[(i+1) % 2]))
        indexes = np.abs(Frames[(i+1) % 2]) > 2*np.spacing(absdiff) 
        reldiff = np.abs(absdiff[indexes] / Frames[(i+1) % 2][indexes])
        
        at_equilibrium = False
        if np.size(reldiff) > 0:
            max_diff = np.max(reldiff)
            print(max_diff)
            if max_diff <= rel_tol:
                # print('rel_max_Diff',max_diff)
                at_equilibrium = True
        else:
            if np.max(absdiff) <= abs_tol:
                # print('abs_max_Diff',np.max(absdiff))
                at_equilibrium = True
        
        if at_equilibrium and i>1:
            # print('Reached equilibrium')
            break
        
        i += 1
    # print(f'finished {i} evlas')
    return Ys, Xs, Frames[i % 2]


def laplace_ode_solver_step(
    Grid: np.ndarray,
    fixedConditions: Callable = doNothing,
    startingShape: Callable = doNothing,
    resolution: tuple[float, float] = (1.0, 1.0),
    stencil: Literal[5, 9] = 5,
    gamma: float = 0.0,
    wrap: bool = False,
    wrap_direction: Literal["both", "x", "y", "none"] = "none",
    rel_tol: float = 1e-6,
    abs_tol: float = 1e-9
):
    """Solves the Laplace equation using a finite difference scheme with anisotropy and periodic boundary conditions.

    Args:
        Grid: A 2D NumPy array representing the initial grid.
        fixedConditions: A function that enforces boundary conditions on the potential grid.
        startingShape: A function that defines the initial shape of the potential grid.
        resolution: A tuple (dx, dy) specifying the grid spacing or 'auto' for automatic resolution.
        stencil: Choose between a 5-point or 9-point stencil.
        gamma: A parameter controlling diagonal weighting for the 9-point stencil.
        wrap: If True, applies periodic boundary conditions.
        wrap_direction: Determines which axes wrap ('both', 'x', 'y', or 'none').
        rel_tol: Relative tolerance for convergence.
        abs_tol: Absolute tolerance for convergence.

    Returns:
        A tuple containing the Y and X coordinate arrays, the final potential grid, and a boolean indicating equilibrium status.
    """
    dx, dy = resolution if isinstance(resolution, tuple) else (1.0, 1.0)
    
    sqrt_a = dy / dx
    a = sqrt_a**2
    
    b = dy**2 + dx**2
    sqrt_b = np.sqrt(b)
    
    Frames = np.zeros((2, *Grid.shape), dtype=np.float64)
    Frames[0] = startingShape(Grid)
    
    Xs = np.arange(0, Grid.shape[1], 1)
    Ys = np.arange(0, Grid.shape[0], 1)
    
    if stencil == 9:
        diagamult = gamma / b
        adjacentmult = (1 - gamma) / (2.0 * (a + 1))
    elif stencil == 5:
        diagamult = 0
        adjacentmult = 1 / (2.0 * (a + 1))
    else:
        raise ValueError(f"Cannot use a {stencil}-point stencil. Only offer 9 and 5 point stencils")
    
    # print("Multipliers=", (adjacentmult, diagamult))
    # print(Xs.shape[0], Ys.shape[0])
    
    i = 0
    # while True if ((2 == -1) ) else i < 1:
    ForwardHSpace_A2f = Frames[i % 2, 1:-1, 2:]
    BackwardHSpace_A2f = Frames[i % 2, 1:-1, :-2]
    ForwardVSpace_A2f = Frames[i % 2, 2:, 1:-1]
    BackwardVSpace_A2f = Frames[i % 2, :-2, 1:-1]
    
    DiagForwardUp = Frames[i % 2, 2:, 2:]
    DiagForwardDown = Frames[i % 2, :-2, 2:]
    DiagBackUp = Frames[i % 2, 2:, :-2]
    DiagBackDown = Frames[i % 2, :-2, :-2]
    
    Frames[(i+1) % 2, 1:-1, 1:-1] = adjacentmult * (
        a * (ForwardHSpace_A2f + BackwardHSpace_A2f) + (ForwardVSpace_A2f + BackwardVSpace_A2f)
    ) + diagamult * (DiagBackUp + DiagBackDown + DiagForwardDown + DiagForwardUp)
    
    if wrap:
        if wrap_direction in ["both", "y"]:
            Frames[(i+1) % 2, (0, -1), 1:-1] = adjacentmult * (
                a * (Frames[i % 2, (0, -1), 2:] + Frames[i % 2, (0, -1), :-2]) +
                (Frames[i % 2, (-1, -2), 1:-1] + Frames[i % 2, (1, 0), 1:-1])
            )  + diagamult * (
                Frames[i % 2, (1, 0), 2:] + Frames[i % 2, (-1, -2), 2:] +
                Frames[i % 2, (1, 0), :-2] + Frames[i % 2, (-1, -2), :-2]
            ) 
        if wrap_direction in ["both", "x"]:
            Frames[(i+1) % 2, 1:-1, (0, -1)] = adjacentmult * (
                a * (Frames[i % 2, 1:-1, (-1, -2)] + Frames[i % 2, 1:-1, (1, 0)]) +
                (Frames[i % 2, 2:, (0, -1)] + Frames[i % 2, :-2, (0, -1)])
            )  + diagamult * (
                Frames[i % 2, :-2, (-1, -2)] + Frames[i % 2, 2:, (-1, -2)] +
                Frames[i % 2, :-2, (1, 0)] + Frames[i % 2, 2:, (1, 0)]
            ) 
    
    Frames[(i+1) % 2] = fixedConditions(Frames[(i+1) % 2])
    
    
    # Convergence check
    absdiff = np.abs((Frames[i % 2] - Frames[(i+1) % 2]))
    indexes = np.abs(Frames[(i+1) % 2]) > 2*np.spacing(absdiff) 
    reldiff = np.abs(absdiff[indexes] / Frames[(i+1) % 2][indexes])
    
    at_equilibrium = False
    if np.size(reldiff) > 0:
        
        max_diff = np.max(reldiff)
        print(max_diff)
        if max_diff <= rel_tol:
            # print('rel_max_Diff',max_diff)
            at_equilibrium = True
    else:
        if np.max(absdiff) <= abs_tol:
            # print('abs_max_Diff',np.max(absdiff))
            at_equilibrium = True
    
    # if at_equilibrium and i>1:
    #     # print('Reached equilibrium')
    #     break
        
    i += 1
    # print(f'finished {i} evlas')
    return Ys, Xs, Frames[i % 2], at_equilibrium