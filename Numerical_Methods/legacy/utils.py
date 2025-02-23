# Load modules and imports neceasasary 
import numpy as np
import scipy.optimize as optimist
import matplotlib.pyplot as plt, matplotlib.colors as mcolors, matplotlib.colorbar as mcolorbar
import sys,os
import matplotlib.cm as cm


def circle(cx,cy,r,dx=1,dy=1,val=1.0,fill=False,clear=False,Grid:'np.ndarray[np.ndarray[np.float64]]'=None):
    # First solve for a qudrant the apply rotations
    operations = [[lambda x,y,z:np.abs(x-y)<=z]*2,[lambda x,y,z:x<=y,lambda x,y,z:x>=y]]
    

    grid_class=type(Grid)
    # if all we want is a  circle
    x = 2*int(r//dx)+5
    y=2*int(r//dy)+5
    if type(Grid) == tuple:
        Grid = np.full(Grid,1)
    # if we inplace into a grid
    if Grid is not None:
        y,x = Grid.shape
        # print(x,y)

    grid_x, grid_y = np.mgrid[:y, :x]
    
    # TODO Variate Tolerance : the cirlces tolerance for a non filled circle should be a function of the radius 
    # Currently not implemented correctly it causes a band instead of a line this band width can variet based on the tolerance
     
    circle_mask = operations[bool(fill)][bool(clear)]((grid_x-cx)**2 + (grid_y-cy)**2 , r**2, r)
    # Apply anti-aliasing using Gaussian blur
    # blurred_circle = gaussian_filter(circle_mask.astype(float), sigma=antialias_sigma)
    vals = (1,0) 
    # Threshold to create a binary image (0 or 1)
    pixelated_circle = np.where(circle_mask == True, *vals)

    # mul mask
    if Grid is not  None:
        if(grid_class!=tuple):
            return Grid*pixelated_circle
    return pixelated_circle

# we will be using 64bit floating point representation
# Stay clear of recursion if possible it a bad game to play unless you have 
# a hop up or hop out scheme



# Some easy to remember utils for readability 
doNothing  = lambda x,*args,**kwargs:x

defualtResolutions = {'1080i':'Nice Try!☺'}




# We gonna solve this in a suitably fashion guys ☺
def laplace_ode_solver(size:'tuple[int,int]|np.ndarray[int,int]',fixedCondtions:'function'=doNothing,startingshape:'function'=doNothing,resoultion:'str|tuple[int,int]|np.ndarray[int,int]'=(1,1),overlaySaver=True):
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
    if overlaySaver:
        Frames[0],overlay = startingshape(Frames[0],retoverlay=True)
    else:
        Frames[0] = startingshape(Frames[0])
        overlay=None
    i = 0
    # TODO: possibly remove while loop, its too messy.
    while True:
        ForwardHSpace_A2f = Frames[i%2, 1:-1, 2:]
        BackwardHSpace_A2f = Frames[i%2, 1:-1, :-2]
        ForwardVSpace_A2f = Frames[i%2, 2:, 1:-1]
        BackwardVSpace_A2f = Frames[i%2, :-2, 1:-1]
        
        
        DiagForwardUp  = Frames[i%2, 2:, 2:]
        DiagForwardDown  = Frames[i%2, :-2, 2:]
        DiagBackUp  = Frames[i%2, 2:, :-2]
        DiagBackDown  = Frames[i%2, :-2, :-2]

        Frames[(i+1)%2, 1:-1, 1:-1] = 0.125*(ForwardHSpace_A2f+BackwardHSpace_A2f+ForwardVSpace_A2f+BackwardVSpace_A2f)+0.125*(DiagBackUp+DiagBackDown+DiagForwardDown+DiagForwardUp)
        if overlay is not None:
            Frames[(i+1)%2] = fixedCondtions(Frames[(i+1)%2],overlay=overlay)
        else:
            Frames[(i+1)%2] = fixedCondtions(Frames[(i+1)%2])
        
        indexes=Frames[i%2]!=0
        diff = (np.abs((Frames[0][indexes]-Frames[1][indexes]))/Frames[i%2][indexes])
        i= (i+1)
        
        # TODO: Make the change relative easier to tell the precentage change
        if np.max(diff) < 1e-2 and i>1:
            break
    retvals = (Ys,Xs,Frames[i%2])
    # TODO: Tranform into a vector field
    
    return retvals

def findUandV(grid:np.ndarray[np.ndarray[np.float64]]):
    E_field = np.zeros([*grid.shape,2],np.float64)
    E_field[:,:-1,0] = grid[:,1:] - grid[:,:-1]
    E_field[:-1,:,1] = grid[1:,:] - grid[:-1,:]
    return E_field




def makeGeometry2(val=1.0,r=35,cx=50,cy=150,relative=False):
    Gridder = None
    def endToEndLine(Grid:np.ndarray,overlay=None,retoverlay=False):
        
        nonlocal Gridder
        
        Grid[:,:2]=val
        Grid[:,-2:]=-val
        
        ForwardHSpace_A2f = Grid[(0,-1), 2:]
        BackwardHSpace_A2f = Grid[(0,-1), :-2]
        ForwardVSpace_A2f = Grid[(-1,-2), 1:-1]
        BackwardVSpace_A2f = Grid[(1,0), 1:-1]
        
        
        DiagForwardUp  = Grid[(1,0), 2:]
        DiagForwardDown  = Grid[(-1,-2), 2:]
        DiagBackUp  = Grid[(1,0), :-2]
        DiagBackDown  = Grid[(-1,-2), :-2]
        
        Grid[(0,-1), 1:-1] = 0.125*(ForwardHSpace_A2f+BackwardHSpace_A2f+ForwardVSpace_A2f+BackwardVSpace_A2f)+0.125*(DiagBackUp+DiagBackDown+DiagForwardDown+DiagForwardUp)
        
        

        if overlay is None:
            if Gridder is None:
                Gridder = overlay = circle(cx,cy,r,fill=True,clear=True,Grid=(*Grid.shape,))
            else:
                overlay = Gridder
            
        Grid = overlay*Grid
        
        if retoverlay:
            return Grid,overlay
        return Grid
    return endToEndLine

endToEndLine_ = makeGeometry2()
def BoxinBox(Grid:np.ndarray,r=1):
    height,width=Grid.shape
    Grid[:,(0,-1)]=Grid[(0,-1),:]=1.0

    return Grid

# Example 1: End-to-End Line
ys, xs, potential = laplace_ode_solver((200, 200), endToEndLine_, endToEndLine_)
Xs, Ys = np.meshgrid(xs[::5], ys[::5])
u, v = np.gradient(potential, xs[1]-xs[0], ys[1]-ys[0])  # Correct gradient calculation

graph=-findUandV(potential)[::5,::5]*25

# print(graph[:,:,0], graph[:,:,1],sep='\r\n===\r\n===\r\n')
plt.figure(figsize=(18, 18),dpi=320)  # Adjust figure size for better visualization
plt.imshow(potential, cmap='PiYG', origin='lower')  # Set origin for consistency
plt.colorbar(label='Electric Potential')
plt.quiver(Xs, Ys, graph[:,:,0], graph[:,:,1], color='b', scale=0.1, scale_units='xy') # Adjust scale and color

plt.title('Electric Potential Distribution (End-to-End)')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig(fname='BoxInBox.png')
plt.show(block=True)
