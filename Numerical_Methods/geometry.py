import matplotlib.artist,matplotlib.patches,matplotlib.path,matplotlib.pyplot as plt
import numpy as np


def circle(cx,cy,r,dx=1,dy=1,val=1.0,fill=False,clear=False,Grid:'np.ndarray[np.ndarray[np.float64]]'=None):
    # First solve for a qudrant the apply rotations
    operations = [[lambda x,y,z:np.abs(x-y)<z]*2,[lambda x,y,z:x<=y,lambda x,y,z:x>=y]]
    
    # === Fast Slow pointer ===
    # r1 = np.array([0,r])
    # r2 = np.array([r,0])
    # theta = np.linspace(0,np.pi/4,1000)
    # =======
    
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
    circle_mask = operations[bool(fill)][bool(clear)]((grid_x-cx)**2 + (grid_y-cy)**2 , r**2,7)
    # Apply anti-aliasing using Gaussian blur
    # blurred_circle = gaussian_filter(circle_mask.astype(float), sigma=antialias_sigma)
    vals = (1,0) if clear else (0,1)
    # Threshold to create a binary image (0 or 1)
    pixelated_circle = np.where(circle_mask == True, *vals)

    # mul mask
    if Grid is not  None:
        return Grid*pixelated_circle
    
    return pixelated_circle


# deal with essy overlays
def identityOverlay(Grid:np.ndarray):
    return np.full_like(Grid,1)

if __name__ == '__main__':
    grid = np.zeros((200,200))
    grid[:,:]=1
    circ=circle(50,50,50,1,1,fill=False,clear=True,Grid=grid)
        
    plt.imshow(circ, cmap='gray')
    plt.colorbar()
    plt.title('Pixelated Circle with Anti-aliasing')
    plt.show()