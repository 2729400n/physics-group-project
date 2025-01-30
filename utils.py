# Load modules and imports neceasasary 
import numpy as np
import scipy.optimize as optimist
import matplotlib.pyplot as plt
import sys,os


# we will be using 64bit floating point representation
# Stay clear of recursion if possible it a bad game to play unless you have 
# a hop up or hop out scheme



# Some easy to remember utils for readability 
doNothing  = lambda x:x

defualtResolutions = {'1080i':'Nice Try!☺'}

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
    w_x_h = np.array(size,np.float64)
    preception = np.array(resoultion,np.float64)
    pixel_w_X_h = w_x_h/preception

    # Three frames to allow rotation/Cyling and comparisons
    # TODO: Check if it works with 2 Frames saved will make it less memory  expensive
    Frames  = np.zeros((3,*pixel_w_X_h))

    

