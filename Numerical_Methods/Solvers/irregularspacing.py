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
def laplace_ode_solver(size: 'tuple[int,int]|np.ndarray[int,int]', fixedCondtions: 'function' = doNothing, startingshape: 'function' = doNothing, resoultion: 'str|tuple[int,int]|np.ndarray[int,int]' = (1, 1)):
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

    w_x_h = np.array(size, int)
    preception = np.array(resoultion, int)
    # pixel_w_X_h = w_x_h/preception

    # two frames to allow rotation/Cyling and comparisons

    Xs = np.arange(0, w_x_h[0]+resoultion[0], resoultion[0])
    Ys = np.arange(0, w_x_h[1]+resoultion[1], resoultion[1])
    # Frames  = np.zeros((2,int(pixel_w_X_h[1]),int(pixel_w_X_h[0])))
    Frames = np.zeros((2, Ys.shape[0], Xs.shape[0]))
    Frames[0] = startingshape(Frames[0])
    print(Xs.shape[0], Ys.shape[0])
    i = 0
    # TODO: possibly remove while loop, its too messy.
    while True:
        ForwardHSpace_A2f = Frames[i % 2, 1:-1, 2:]
        BackwardHSpace_A2f = Frames[i % 2, 1:-1, :-2]
        ForwardVSpace_A2f = Frames[i % 2, 2:, 1:-1]
        BackwardVSpace_A2f = Frames[i % 2, :-2, 1:-1]

        Frames[(i+1) % 2, 1:-1, 1:-1] = 0.25*(ForwardHSpace_A2f +
                                              BackwardHSpace_A2f+ForwardVSpace_A2f+BackwardVSpace_A2f)
        Frames[(i+1) % 2] = fixedCondtions(Frames[(i+1) % 2])
        indexes = Frames[i % 2] != 0
        diff = (np.abs((Frames[0][indexes]-Frames[1]
                [indexes]))/Frames[i % 2][indexes])
        i = (i+1)

        # TODO: Make the change relative easier to tell the precentage change
        if np.max(diff) < 1e-6 and i > 1:
            break
    retvals = (Ys, Xs, Frames[i % 2])

    return retvals


# We gonna solve this in a suitably fashion guys ☺
def laplace_ode_solver_continue(Grid: 'np.ndarray[np.ndarray[np.float64]]', fixedCondtions: 'function' = doNothing, startingshape: 'function' = doNothing, resoultion: 'str|tuple[int,int]|np.ndarray[int,int]' = (1.0, 1.0),):
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
    Xs = np.arange(0, Grid.shape[1]+1, 1)
    Ys = np.arange(0, Grid.shape[0]+1, 1)
    print(Xs.shape[0], Ys.shape[0])
    i = 0
    # TODO: possibly remove while loop, its too messy.
    while True:
        ForwardHSpace_A2f = Frames[i % 2, 1:-1, 2:]
        BackwardHSpace_A2f = Frames[i % 2, 1:-1, :-2]
        ForwardVSpace_A2f = Frames[i % 2, 2:, 1:-1]
        BackwardVSpace_A2f = Frames[i % 2, :-2, 1:-1]

        Frames[(i+1) % 2, 1:-1, 1:-1] = 0.25*(ForwardHSpace_A2f +
                                              BackwardHSpace_A2f+ForwardVSpace_A2f+BackwardVSpace_A2f)
        Frames[(i+1) % 2] = fixedCondtions(Frames[(i+1) % 2])
        indexes = Frames[i % 2] != 0
        diff = (np.abs((Frames[0][indexes]-Frames[1]
                [indexes]))/Frames[i % 2][indexes])
        i = (i+1)

        # TODO: Make the change relative easier to tell the precentage change
        if np.max(diff) < 1e-6 and i > 1:
            break
    retvals = (Ys, Xs, Frames[i % 2])

    return retvals


def laplace_ode_solver_step(Grid: 'np.ndarray[np.ndarray[np.float64]]',
                            fixedCondtions: 'function' = doNothing, startingshape: 'function' = doNothing,
                            dx: float = 1.0, dy: float = 1.0, x0: float = 0.0, y0: float = 0.0,
                            rel_tol: np.float64 = 1e-3, abs_tol: np.float64 = 1e-10,stencil:int=5,gamma:float=1.0,
                            wrap:bool=False,wrap_direction:Literal['both','x','y','none']='none',):
    # TODO: Fix docstrings adding more detail to params
    """
    Solves the Laplace equation using a finite difference scheme.

    Args:
        size: A tuple (x_size, y_size) specifying the grid dimensions.
        resolution: A tuple (dx, dy) specifying the grid spacing or a string 'auto' for automatic resolution.
        fixedCondtions: A function that enforces boundary conditions on the potential grid.
        startingshape: A function that defines the initial shape of the potential grid.

    Returns:
        A NumPy array representing the electric potential at all grid points.
    """
    
    # Calculate x and y propotionality constant
    sqrt_a = dy/dx
    a = sqrt_a**2
    
    b = dy**2+dx**2
    sqrt_b = np.sqrt(b)

    # Create a frame Array to hold the current Frame and next Frame
    Frames = np.zeros((2, *Grid.shape), dtype=np.float64, order='C')
    Frames[0] = startingshape(Grid)

    # Find end points
    x1 = (Grid.shape[1]-x0)/dx
    y1 = (Grid.shape[1]-x0)/dy

    # Create list of distinct elements
    Xs = np.arange(x0, x1+dx, dx)
    Ys = np.arange(y0, y1+dx, dy)
    
    DX_s = [dx for i in range(len(Xs))]
    DY_s = [dy for i in range(len(Ys))]
    
    if stencil == 9:
        diagamult = gamma*(1/8)
        adjacentmult = (1-gamma*(1/2))/4
    elif stencil == 5:
        diagamult = 0
        adjacentmult = 0.25
    else:
        raise ValueError(f'Cannot use a {stencil}-point stencil')
    
    shrinker = np.full((Grid.shape[0]-1,Grid.shape[1]-1),False,dtype=np.bool_)
    
    newGrid = Grid.copy()
    interstingPart = newGrid[1:-1,1:-1]
    
    ForwardHSpace_A1f = Grid[1:-1, 1:]
    ForwardVSpace_A1f = Grid[1:, 1:-1]
    BackwardHSpace_A1f = Grid[1:-1, :-1]
    BackwardVSpace_A1f = Grid[:-1, 1:-1]
    
    nonZeroHForward=(ForwardHSpace_A1f>np.spacing(BackwardHSpace_A2f))
    nonZeroVForward=(ForwardVSpace_A1f>np.spacing(BackwardVSpace_A1f))
    
    ZeroHForward=np.logical_not(nonZeroHForward)
    ZeroVForward=np.logical_not(nonZeroVForward)
    
    
    
    hdiff = np.abs(ForwardHSpace_A1f-BackwardHSpace_A1f)
    vdiff = np.abs(ForwardVSpace_A1f-BackwardVSpace_A1f)
    
    
    # Have to use geometric mean 
    
    shrinker[nonZeroHForward] = np.abs((hdiff[nonZeroHForward])/(ForwardHSpace_A1f[nonZeroHForward]))<=rel_tol
    shrinker[ZeroHForward] = hdiff[ZeroHForward]<=abs_tol
    
    shrinker[nonZeroVForward] = np.abs((vdiff[nonZeroVForward])/(ForwardHSpace_A1f[nonZeroVForward]))<=rel_tol
    shrinker[ZeroVForward] = vdiff[ZeroVForward]<=abs_tol
    
    i=0
    p=0
    for  i in range(shrinker.shape[0]-1):
        slice_ = shrinker[i,:]
        
        if slice_.all() == True:
            geomslice = interstingPart[nonZeroHForward[p,:-1]]
            arithmeticslice = interstingPart[ZeroHForward[p,:-1]]
            
            geomslice = np.sqrt(geomslice* interstingPart[nonZeroHForward[p+1,:-1]])
            arithmeticslice=(arithmeticslice+interstingPart[ZeroHForward[p+1,:-1]])/2
            
            interstingPart[nonZeroHForward[p,:-1]]=geomslice
            interstingPart[ZeroHForward[p,:-1]]=arithmeticslice
            
            newGrid = np.delete(newGrid,p,axis=1)
            interstingPart = newGrid[1:-1,1:-1]
            p-=1
        p+=1
        
    for  i in range(shrinker.shape[-2]-1):
        slice_ = shrinker[i,:]
        
        if slice_.all() == True:
            geomslice = interstingPart[nonZeroHForward[p,:-1]]
            arithmeticslice = interstingPart[ZeroHForward[p,:-1]]
            
            geomslice = np.sqrt(geomslice* interstingPart[nonZeroHForward[p+1,:-1]])
            arithmeticslice=(arithmeticslice+interstingPart[ZeroHForward[p+1,:-1]])/2
            
            interstingPart[nonZeroHForward[p,:-1]]=geomslice
            interstingPart[ZeroHForward[p,:-1]]=arithmeticslice
            
            newGrid = np.delete(newGrid,p,axis=1)
            interstingPart = newGrid[1:-1,1:-1]
            p-=1
        p+=1
        
    for  i in range(shrinker.shape[-1]-1):
        slice_ = shrinker[i,:]
        
        if slice_.all() == True:
            geomslice = interstingPart[nonZeroHForward[p,:-1]]
            arithmeticslice = interstingPart[ZeroHForward[p,:-1]]
            
            geomslice = np.sqrt(geomslice* interstingPart[nonZeroHForward[p+1,:-1]])
            arithmeticslice=(arithmeticslice+interstingPart[ZeroHForward[p+1,:-1]])/2
            
            interstingPart[nonZeroHForward[p,:-1]]=geomslice
            interstingPart[ZeroHForward[p,:-1]]=arithmeticslice
            
            newGrid = np.delete(newGrid,p,axis=1)
            interstingPart = newGrid[1:-1,1:-1]
            p-=1
        p+=1
    
    
    

    ForwardHSpace_A2f = Frames[0, 1:-1, 2:]
    BackwardHSpace_A2f = Frames[0, 1:-1, :-2]
    ForwardVSpace_A2f = Frames[0, 2:, 1:-1]
    BackwardVSpace_A2f = Frames[0, :-2, 1:-1]

    DiagForwardUp = Frames[0, 2:, 2:]
    DiagForwardDown = Frames[0, :-2, 2:]
    DiagBackUp = Frames[0, 2:, :-2]
    DiagBackDown = Frames[0, :-2, :-2]
    
    
    
    Frames[1, 1:-1, 1:-1] = adjacentmult*((a*(ForwardHSpace_A2f +
                                        BackwardHSpace_A2f)+(ForwardVSpace_A2f+BackwardVSpace_A2f))/(2.0*(a+1)))+diagamult*(DiagBackUp+DiagBackDown+DiagForwardDown+DiagForwardUp)/b
    
    
    if wrap:
            if wrap_direction in ['both', 'y']:
                ForwardHSpace_A2f = Frames[0, (0, -1), 2:]
                BackwardHSpace_A2f = Frames[0, (0, -1), :-2]
                ForwardVSpace_A2f = Frames[0, (-1, -2), 1:-1]
                BackwardVSpace_A2f = Frames[0, (1, 0), 1:-1]

                DiagForwardUp = Frames[0, (1, 0), 2:]
                DiagForwardDown = Frames[0, (-1, -2), 2:]
                DiagBackUp = Frames[0, (1, 0), :-2]
                DiagBackDown = Frames[0, (-1, -2), :-2]

                Frames[1,(0, -1), 1:-1] = adjacentmult*((a*(ForwardHSpace_A2f +
                                        BackwardHSpace_A2f)+(ForwardVSpace_A2f+BackwardVSpace_A2f))/(2.0*(a+1)))+diagamult*(DiagBackUp+DiagBackDown+DiagForwardDown+DiagForwardUp)/b
            if wrap_direction in ['both', 'x']:
                ForwardHSpace_A2f = Frames[0, 1:-1, (-1, -2)]
                BackwardHSpace_A2f = Frames[0, 1:-1, (1, 0)]
                ForwardVSpace_A2f = Frames[0, 2:, (0, -1)]
                BackwardVSpace_A2f = Frames[0, :-2, (0, -1)]

                DiagForwardUp = Frames[0, :-2, (-1, -2)]
                DiagForwardDown = Frames[0, 2:, (-1, -2)]
                DiagBackUp = Frames[0, :-2, :(1, 0)]
                DiagBackDown = Frames[0, 2:, :(1, 0)]

                Frames[1, 1:-1,(0, -1)] = adjacentmult*((a*(ForwardHSpace_A2f +
                                        BackwardHSpace_A2f)+(ForwardVSpace_A2f+BackwardVSpace_A2f))/(2.0*(a+1)))+diagamult*(DiagBackUp+DiagBackDown+DiagForwardDown+DiagForwardUp)/b
                
    Frames[1] = fixedCondtions(Frames[1])
    
    Frames[1] = fixedCondtions(Frames[1])
    indexes:np.ndarray[np.bool_] = Frames[0] != 0
    retvals = (Ys, Xs, Frames[1])
    
    try:
        if indexes.all(where=False) == False:
            diff = np.abs(((Frames[0][indexes]-Frames[1]
                [indexes]))/Frames[0][indexes])
            shouldStop = diff<=rel_tol
            return (*retvals,shouldStop)
    except *(RuntimeError,ZeroDivisionError):
        pass
    
    try:
        diff = np.abs((Frames[0]-Frames[1]))
        shouldStop = diff<=abs_tol
        return (*retvals,shouldStop)
    except *(RuntimeError,ValueError):
        shouldStop=True
    
    return (*retvals,shouldStop)
