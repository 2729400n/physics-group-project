import numpy as np


# TODO Fix all Circular constraints : The cirlce seems to have an r value that is 1 greater than expected

def circle(cx,cy,r,dx=1,dy=1,val=1.0,fill=False,clear=False,Grid:'np.ndarray[np.ndarray[np.float64]]'=None):
    # First solve for a qudrant the apply rotations
    operations = [[lambda x,y,z:np.abs(x-y)<=z]*2,[lambda x,y,z:x<=y,lambda x,y,z:x>=y]]
    
    # === Fast Slow pointer ===
    # r1 = np.array([0,r])
    # r2 = np.array([r,0])
    # theta = np.linspace(0,np.pi/4,1000)
    # =======
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

def annulus(cx, cy, r1, r2, dx=1, dy=1, val=1.0, fill=False, clear=False, Grid:'np.ndarray[np.ndarray[np.float64]]'=None):
    # First solve for a qudrant the apply rotations
    # TODO Add Finer Control: Could someone add finer controls to allow for control over the inner and outer values of the annulus 
    operations = [[lambda w,x,y,z,zz:np.logical_or(np.abs(w-x)<=z,np.abs(w-y)<=zz)]*2,[lambda w,x,y,z,zz:np.logical_and(x<=w,w<=y),lambda w,x,y,z,zz:(np.logical_or(x>w,w>y))]]

    grid_class=type(Grid)
    
    if type(Grid) == tuple:
        Grid = np.full(Grid,1)
    # if we inplace into a grid
    if Grid is not None:
        y,x = Grid.shape
        # print(x,y)

    grid_x, grid_y = np.mgrid[:y, :x]
    annulus_mask = operations[bool(fill)][bool(clear)]( ((grid_x-cx)**2 + (grid_y-cy)**2 ), r1**2, r2**2,r1,r2 )
    # Apply anti-aliasing using Gaussian blur
    # blurred_circle = gaussian_filter(circle_mask.astype(float), sigma=antialias_sigma)
    vals = (1,0) 
    # Threshold to create a binary image (0 or 1)
    pixelated_annulus = np.where(annulus_mask == True, *vals)

    # mul mask
    if Grid is not  None:
        if(grid_class!=tuple):
            return Grid*pixelated_annulus
    
    return pixelated_annulus

def rectangle(x,y,w,h,dx=1,dy=1,val=1.0,fill=False,clear=False,Grid:'np.ndarray[np.ndarray[np.float64]]'=None):
    operations = []
    if type(Grid) == tuple:
        Grid = np.full(Grid,1)
    if Grid is not None:
        y,x = Grid.shape
        # print(x,y)
    grid_x, grid_y = np.full((max(0,x0)))
    # Apply anti-aliasing using Gaussian blur
    # blurred_circle = gaussian_filter(circle_mask.astype(float), sigma=antialias_sigma)
    vals = (1,0) 
    # Threshold to create a binary image (0 or 1)
    pixelated_annulus = np.where(annulus_mask == True, *vals)

    # mul mask
    if Grid is not  None:
        if(grid_class!=tuple):
            return Grid*pixelated_annulus
    
    return pixelated_annulus 

def rectangle(x,y,w,h,dx=1,dy=1,val=1.0,fill=False,clear=False,Grid:'np.ndarray[np.ndarray[np.float64]]'=None):
    operations = []
    if type(Grid) == tuple:
        Grid = np.full(Grid,1)
    if Grid is not None:
        y,x = Grid.shape
        # print(x,y)
    grid_x, grid_y = np.full((max(0,x0)))
    # Apply anti-aliasing using Gaussian blur
    # blurred_circle = gaussian_filter(circle_mask.astype(float), sigma=antialias_sigma)
    vals = (1,0) 
    # Threshold to create a binary image (0 or 1)
    pixelated_annulus = np.where(annulus_mask == True, *vals)

    # mul mask
    if Grid is not  None:
        if(grid_class!=tuple):
            return Grid*pixelated_annulus
    
    return pixelated_annulus 

# deal with essy overlays
def identityOverlay(Grid:np.ndarray):
    return np.full_like(Grid,1)


def rectangle(x0,y0,x1,y1,theta=0,dx=1,dy=1,val=1.0,fill=False,clear=False,Grid:'np.ndarray[np.ndarray[np.float64]]'=None)->np.ndarray:
    grid_x, grid_y = np.mgrid[y0:y1, x0:x1]

if __name__ == '__main__':
    import matplotlib.artist,matplotlib.patches,matplotlib.path,matplotlib.pyplot as plt
    grid = np.zeros((500,500))
    grid[:,:]=1
    circ=annulus(100,100,25,100,2,fill=False,clear=False,Grid=grid)
        
    plt.imshow(circ, cmap='gray')
    plt.colorbar()
    plt.title('Pixelated Circle with Anti-aliasing')
    plt.show()