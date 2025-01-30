# Load modules and imports neceasasary 
import numpy as np
import scipy.optimize as optimist
import matplotlib.pyplot as plt
import sys,os

print(os.name and sys.platform)
# Some easy to remember utils for readability 
doNothing  = lambda x:x

defualtResolutions = {''}

# We gonna solve this in a suitably fashion guys ☺
def laplace_ode_solver(size:'tuple[int,int]|np.ndarray[int,int]',resoultion:'str|tuple[int,int]|np.ndarray[int,int]',fixedCondtions:'function'=doNothing,startingshape:'function'=doNothing):
    """Solves the Laplace equation using a finite difference scheme.

    Args:
        size: A tuple (x_size, y_size) specifying the grid dimensions.
        resolution: A tuple (dx, dy) specifying the grid spacing or a string 'auto' for automatic resolution.
        fixedCondtions: A function that enforces boundary conditions on the potential grid.
        startingshape: A function that defines the initial shape of the potential grid.

    Returns:
        A NumPy array representing the electric potential at all grid points.
    """
    # wow Gemini Docstrings kinda magic and good. Also rotationless solver
    
