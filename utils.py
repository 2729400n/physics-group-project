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
def laplace_ode_solver(size:'tuple[int,int]|np.ndarray[int,int]',fixedCondtions:'function'=doNothing,startingshape:'function'=doNothing,resoultion:'str|tuple[int,int]|np.ndarray[int,int]'=(1,1)):
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
    pixel_w_X_h = w_x_h/preception
    
    # two frames to allow rotation/Cyling and comparisons
    
    Xs= np.arange(0,w_x_h[0]+resoultion[0],resoultion[0])
    Ys = np.arange(0,w_x_h[1]+resoultion[1],resoultion[1])
    # Frames  = np.zeros((2,int(pixel_w_X_h[1]),int(pixel_w_X_h[0])))
    Frames  = np.zeros((2,Ys.shape[0],Xs.shape[0]))
    Frames[0] = startingshape(Frames[0])
    print(Xs.shape[0],Ys.shape[0])
    i = 0
    # TODO: possibly remove while loop, its too messy.
    while True:
        ForwardHSpace_A2f = Frames[i%2, 1:-1, 2:]
        BackwardHSpace_A2f = Frames[i%2, 1:-1, :-2]
        ForwardVSpace_A2f = Frames[i%2, 2:, 1:-1]
        BackwardVSpace_A2f = Frames[i%2, :-2, 1:-1]

        Frames[(i+1)%2, 1:-1, 1:-1] = 0.25*(ForwardHSpace_A2f+BackwardHSpace_A2f+ForwardVSpace_A2f+BackwardVSpace_A2f)
        Frames[(i+1)%2] = fixedCondtions(Frames[(i+1)%2])
        i= (i+1)%2
        # TODO: Make the change relative easier to tell the precentage change
        if np.max(np.abs((Frames[0]-Frames[1]))) < 1e-6:
            break
    # TODO: Tranform into a vector field 
    return Ys,Xs,Frames[i]



        
def endToEndLine(Grid:np.ndarray):
    height,width=Grid.shape
    Grid[:,(0,-1)]=1.0
    midx = width//2
    startx=midx-width//8
    endx=midx+width//8

    midy = height//2
    starty=midy-height//8
    endy=midy+width//8
    Grid[starty:endy,startx:endx]=-1.0
    return Grid

def BoxinBox(Grid:np.ndarray):
    height,width=Grid.shape
    Grid[:,(0,-1)]=Grid[(0,-1),:]=1.0
    return Grid

# Example 1: End-to-End Line
ys, xs, potential = laplace_ode_solver((200, 100), endToEndLine, endToEndLine)
Xs, Ys = np.meshgrid(xs, ys)
u, v = np.gradient(potential, xs[1]-xs[0], ys[1]-ys[0])  # Correct gradient calculation

plt.figure(figsize=(18, 18),dpi=320)  # Adjust figure size for better visualization
plt.imshow(potential, cmap='viridis', origin='lower')  # Set origin for consistency
plt.quiver(Xs, Ys, u, v, color='w', scale=10, scale_units='xy') # Adjust scale and color
plt.colorbar(label='Electric Potential')
plt.title('Electric Potential Distribution (End-to-End)')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig(fname='BoxInBox.png')
plt.show()

# Example 2: Box in Box
ys, xs, potential = laplace_ode_solver((200, 200), BoxinBox, BoxinBox)
Xs, Ys = np.meshgrid(xs, ys)
u, v = np.gradient(potential*400, xs[1]-xs[0], ys[1]-ys[0])  # Correct gradient calculation

plt.figure(figsize=(18, 18),dpi=320)  # Adjust figure size
plt.imshow(potential, cmap='viridis')  # Set origin
plt.quiver(Xs, Ys, u, v, scale=20, scale_units='xy',alpha=0.5) # Adjust scale and color
plt.colorbar(label='Electric Potential')
plt.title('Electric Potential Distribution (Box in Box)')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig(fname='BoxInBox.png')
plt.show()