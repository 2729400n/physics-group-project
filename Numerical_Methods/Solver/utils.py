# Load modules and imports neceasasary 

import numpy as np

# we will be using 64bit floating point representation
# Stay clear of recursion if possible it a bad game to play unless you have 
# a hop up or hop out scheme



# Some easy to remember utils for readability 
doNothing  = lambda x:x

defualtResolutions = {'1080i':'Nice Try!☺'}




# We gonna solve this in a suitably fashion guys ☺
def laplace_ode_solver(size:'tuple[int,int]|np.ndarray[int,int]', fixedCondtions:'function'=doNothing,startingshape:'function'=doNothing,resoultion:'str|tuple[int,int]|np.ndarray[int,int]'=(1,1)):
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
    
    w_x_h = np.array(size,int)
    preception = np.array(resoultion,int)
    # pixel_w_X_h = w_x_h/preception
    
    # two frames to allow rotation/Cyling and comparisons
    
    Xs= np.arange(0,w_x_h[0]+resoultion[0],resoultion[0])
    Ys = np.arange(0,w_x_h[1]+resoultion[1],resoultion[1])
    # Frames  = np.zeros((2,int(pixel_w_X_h[1]),int(pixel_w_X_h[0])))
    Frames  = np.zeros((2,Ys.shape[0],Xs.shape[0]))
    Frames[0],overlay = startingshape(Frames[0],retoverlay=True)
    print(Xs.shape[0],Ys.shape[0])
    i = 0
    # TODO: possibly remove while loop, its too messy.
    while True:
        ForwardHSpace_A2f = Frames[i%2, 1:-1, 2:]
        BackwardHSpace_A2f = Frames[i%2, 1:-1, :-2]
        ForwardVSpace_A2f = Frames[i%2, 2:, 1:-1]
        BackwardVSpace_A2f = Frames[i%2, :-2, 1:-1]

        Frames[(i+1)%2, 1:-1, 1:-1] = 0.25*(ForwardHSpace_A2f+BackwardHSpace_A2f+ForwardVSpace_A2f+BackwardVSpace_A2f)
        Frames[(i+1)%2] = fixedCondtions(Frames[(i+1)%2],overlay=overlay)
        indexes=Frames[i%2]!=0
        diff = (np.abs((Frames[0][indexes]-Frames[1][indexes]))/Frames[i%2][indexes])
        i= (i+1)
        
        # TODO: Make the change relative easier to tell the precentage change
        if np.max(diff) < 1e-6 and i>1:
            break
    retvals = (Ys,Xs,Frames[i%2])
    # TODO: Tranform into a vector field
    
    return retvals

def findUandV(grid:np.ndarray[np.ndarray[np.float64]]):
    E_field = np.zeros([*grid.shape,2],np.float64)
    E_field[:,:-1,0] = grid[:,1:] - grid[:,:-1]
    E_field[:-1,:,1] = grid[1:,:] - grid[:-1,:]
    return E_field
