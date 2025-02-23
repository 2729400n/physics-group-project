# License: None
# Author: P3 Comp. 2025 Lab Group B ( Electrostatics )
# Description: A module of utilities for the Numerical Solver

# Load modules and imports neceasasary

from typing import Literal
import numpy as np

# we will be using 64bit floating point representation
# Stay clear of recursion if possible it a bad game to play unless you have
# a hop up or hop out scheme


# Some easy to remember utils for readability
def doNothing(x: 'np.ndarray | tuple[int,int]' = None, *args, **kwargs):
    if isinstance(x, tuple):
        return np.zeros(x, np.float64)
    return x


# We gonna solve this in a suitably fashion guys ☺
def laplace_ode_solver(size: 'tuple[int,int]|np.ndarray[int,int]', fixedCondtions: 'function' = doNothing, startingshape: 'function' = doNothing, resoultion: 'str|tuple[int,int]|np.ndarray[int,int]' = (1, 1), overlaySaver: bool = False, stencil: 'Literal[5,9]' = 5, gamma: float = 0.0):
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

    w_x_h = np.array(size, dtype=np.float64)
    preception = np.array(resoultion, dtype=np.float64)
    pixel_w_X_h = w_x_h/preception

    # two frames to allow rotation/Cyling and comparisons

    Xs = np.arange(0, w_x_h[0]+resoultion[0], resoultion[0])
    Ys = np.arange(0, w_x_h[1]+resoultion[1], resoultion[1])
    # Frames  = np.zeros((2,int(pixel_w_X_h[1]),int(pixel_w_X_h[0])))

    Frames = np.zeros((2, Ys.shape[0], Xs.shape[0]))

    if overlaySaver:
        Frames[0], overlay = startingshape(Frames[0], retoverlay=True)
    else:
        Frames[0] = startingshape(Frames[0])
        overlay = None

    if stencil == 9:
        diagamult = gamma*(1/8)
        adjacentmult = (1-gamma*(1/2))/4
    elif stencil == 5:
        diagamult = 0
        adjacentmult = 0.25
    else:
        raise ValueError(f'Cannot use a {stencil}-point stencil')

    i = 0
    # TODO: possibly remove while loop, its too messy.
    while True:
        ForwardHSpace_A2f = Frames[i % 2, 1:-1, 2:]
        BackwardHSpace_A2f = Frames[i % 2, 1:-1, :-2]
        ForwardVSpace_A2f = Frames[i % 2, 2:, 1:-1]
        BackwardVSpace_A2f = Frames[i % 2, :-2, 1:-1]

        DiagForwardUp = Frames[i % 2, 2:, 2:]
        DiagForwardDown = Frames[i % 2, :-2, 2:]
        DiagBackUp = Frames[i % 2, 2:, :-2]
        DiagBackDown = Frames[i % 2, :-2, :-2]

        Frames[(i+1) % 2, 1:-1, 1:-1] = adjacentmult*(ForwardHSpace_A2f+BackwardHSpace_A2f+ForwardVSpace_A2f +
                                                      BackwardVSpace_A2f) + diagamult*(DiagBackUp+DiagBackDown+DiagForwardDown+DiagForwardUp)
        if overlay is not None:
            Frames[(i+1) % 2] = fixedCondtions(Frames[(i+1) %
                                                      2], overlay=overlay)
        else:
            Frames[(i+1) % 2] = fixedCondtions(Frames[(i+1) % 2])

        indexes = Frames[i % 2] != 0
        if np.size(indexes)>0:
            diff = np.abs(((Frames[0][indexes]-Frames[1]
                    [indexes]))/Frames[i % 2][indexes])

            # TODO: Make the change relative easier to tell the precentage change
            if np.max(diff) < 1e-2 and i > 1:
                break
        else:
            diff = np.abs((Frames[0][indexes]-Frames[1]
                    [indexes]))

            # TODO: Make the change relative easier to tell the precentage change
            if np.max(diff) < 1e-6 and i > 1:
                break
        i=(i+1)
    retvals = (Ys, Xs, Frames[i % 2])
    # TODO: Tranform into a vector field

    return retvals


# We gonna solve this in a suitably fashion guys ☺
def laplace_ode_solver_continue(Grid: 'np.ndarray[np.ndarray[np.float64]]', fixedCondtions: 'function' = doNothing, startingshape: 'function' = doNothing, resoultion: 'str|tuple[int,int]|np.ndarray[int,int]' = (1, 1), overlaySaver: bool = False, stencil: 'Literal[5,9]' = 5, gamma: float = 0.0, wrap: bool = False, wrap_direction: Literal["both", "x", "y"] = 'none',rel_tol:float=1e-6,abs_tol:float=1e-9):
    # TODO: Fix docstrings adding more detail to params
    """Solves the Laplace equation using a finite difference scheme.

    Args:
        size: A tuple (x_size, y_size) specifying the grid dimensions.
        resolution: A tuple (dx, dy) specifying the grid spacing or a string 'auto' for automatic resolution.
        fixedCondtions: A function that enforces boundary conditions on the potential grid.
        startingshape: A function that defines the initial shape of the potential grid.

    Returns:
        A NumPy array representing the electric potential at all grid points.
    """

    Frames = np.zeros((2, *Grid.shape), dtype=np.float64)

    Frames[0] = startingshape(Grid)

    Xs = np.arange(0, Grid.shape[1]+resoultion[0], resoultion[0])
    Ys = np.arange(0, Grid.shape[0]+resoultion[1], resoultion[1])

    if stencil == 9:
        diagamult = gamma*(1/8)
        adjacentmult = (1-gamma*(1/2))/4
    elif stencil == 5:
        diagamult = 0
        adjacentmult = 0.25
    else:
        raise ValueError(f'Cannot use a {stencil}-point stencil')
    print('Multipliers=',(adjacentmult,diagamult))
    print(Xs.shape[0], Ys.shape[0])
    i = 0
    # TODO: possibly remove while loop, its too messy.
    while True:
        ForwardHSpace_A2f = Frames[i % 2, 1:-1, 2:]
        BackwardHSpace_A2f = Frames[i % 2, 1:-1, :-2]
        ForwardVSpace_A2f = Frames[i % 2, 2:, 1:-1]
        BackwardVSpace_A2f = Frames[i % 2, :-2, 1:-1]

        DiagForwardUp = Frames[i % 2, 2:, 2:]
        DiagForwardDown = Frames[i % 2, :-2, 2:]
        DiagBackUp = Frames[i % 2, 2:, :-2]
        DiagBackDown = Frames[i % 2, :-2, :-2]

        Frames[(i+1) % 2, 1:-1, 1:-1] = adjacentmult*(ForwardHSpace_A2f+BackwardHSpace_A2f+ForwardVSpace_A2f +
                                                      BackwardVSpace_A2f) + diagamult*(DiagBackUp+DiagBackDown+DiagForwardDown+DiagForwardUp)

        if wrap:
            if wrap_direction in ['both', 'y']:
                ForwardHSpace_A2f = Frames[i % 2, (0, -1), 2:]
                BackwardHSpace_A2f = Frames[i % 2, (0, -1), :-2]
                ForwardVSpace_A2f = Frames[i % 2, (-1, -2), 1:-1]
                BackwardVSpace_A2f = Frames[i % 2, (1, 0), 1:-1]

                DiagForwardUp = Frames[i % 2, (1, 0), 2:]
                DiagForwardDown = Frames[i % 2, (-1, -2), 2:]
                DiagBackUp = Frames[i % 2, (1, 0), :-2]
                DiagBackDown = Frames[i % 2, (-1, -2), :-2]

                Frames[(i+1)%2,(0, -1), 1:-1] = adjacentmult*(ForwardHSpace_A2f+BackwardHSpace_A2f+ForwardVSpace_A2f +
                                                    BackwardVSpace_A2f)+diagamult*(DiagBackUp+DiagBackDown+DiagForwardDown+DiagForwardUp)
            if wrap_direction in ['both', 'x']:
                ForwardHSpace_A2f = Frames[i % 2, 1:-1, (-1, -2)]
                BackwardHSpace_A2f = Frames[i % 2, 1:-1, (1, 0)]
                ForwardVSpace_A2f = Frames[i % 2, 2:, (0, -1)]
                BackwardVSpace_A2f = Frames[i % 2, :-2, (0, -1)]

                DiagForwardUp = Frames[i % 2, :-2, (-1, -2)]
                DiagForwardDown = Frames[i % 2, 2:, (-1, -2)]
                DiagBackUp = Frames[i % 2, :-2, :(1, 0)]
                DiagBackDown = Frames[i % 2, 2:, :(1, 0)]

                Frames[(i+1)%2, 1:-1,(0, -1)] = adjacentmult*(ForwardHSpace_A2f+BackwardHSpace_A2f+ForwardVSpace_A2f +
                                                    BackwardVSpace_A2f)+diagamult*(DiagBackUp+DiagBackDown+DiagForwardDown+DiagForwardUp)

        
        Frames[(i+1) % 2] = fixedCondtions(Frames[(i+1) % 2])


        indexes = Frames[(i+1) % 2] != 0
        
        diff = np.abs(((Frames[0][indexes]-Frames[1]
                [indexes]))/Frames[(i+1) % 2][indexes])
        if(np.size(diff)>0):
            # TODO: Make the change relative easier to tell the precentage change
            max_diff = np.max(diff)
            if max_diff < rel_tol and i > 1:
                print(max_diff)
                break
            
        else:
            diff = np.abs((Frames[0]-Frames[1]))
            # TODO: Make the change relative easier to tell the precentage change
            if np.max(diff) < abs_tol and i > 1:
                break
        i=(i+1)
    retvals = (Ys, Xs, Frames[i % 2])

    return retvals


def laplace_ode_solver_step(Grid: 'np.ndarray[np.ndarray[np.float64]]', fixedCondtions: 'function' = doNothing, startingshape: 'function' = doNothing, resoultion: 'str|tuple[int,int]|np.ndarray[int,int]' = (1, 1)):
    # TODO: Fix docstrings adding more detail to params
    """Solves the Laplace equation using a finite difference scheme.

    Args:
        size: A tuple (x_size, y_size) specifying the grid dimensions.
        resolution: A tuple (dx, dy) specifying the grid spacing or a string 'auto' for automatic resolution.
        fixedCondtions: A function that enforces boundary conditions on the potential grid.
        startingshape: A function that defines the initial shape of the potential grid.

    Returns:
        A NumPy array representing the electric potential at all grid points.
    """

    Frames = np.zeros((2, *Grid.shape), dtype=np.float64)
    Frames[0], overlay = startingshape(Grid, retoverlay=True)
    Xs = np.arange(0, Grid.shape[1], 1)
    Ys = np.arange(0, Grid.shape[0]+1, 1)
    print(Xs.shape[0], Ys.shape[0])

    # TODO CLEANUP : remove dependencey on i
    i = 0
    ForwardHSpace_A2f = Frames[i % 2, 1:-1, 2:]
    BackwardHSpace_A2f = Frames[i % 2, 1:-1, :-2]
    ForwardVSpace_A2f = Frames[i % 2, 2:, 1:-1]
    BackwardVSpace_A2f = Frames[i % 2, :-2, 1:-1]

    Frames[(i+1) % 2, 1:-1, 1:-1] = 0.25*(ForwardHSpace_A2f +
                                          BackwardHSpace_A2f+ForwardVSpace_A2f+BackwardVSpace_A2f)
    Frames[(i+1) % 2] = fixedCondtions(Frames[(i+1) % 2], overlay=overlay)
    indexes = Frames[i % 2] != 0
    diff = (np.abs((Frames[0][indexes]-Frames[1]
            [indexes]))/Frames[i % 2][indexes])
    i = (i+1)

    retvals = (Ys, Xs, Frames[i % 2])

    return retvals
