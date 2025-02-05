import matplotlib.artist,matplotlib.patches,matplotlib.path,matplotlib.pyplot as plt
import numpy as np


def circle(cx,cy,r,dx,dy,val=1.0,fill=False,clear=False,Grid:'np.ndarray[np.ndarray[np.float64]]'=None):
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
    
    # if we inplace into a grid
    if Grid is not None:
        y,x = Grid.shape
        print(x,y)

    grid_x, grid_y = np.mgrid[:x, :y]
    circle_mask = operations[bool(fill)][bool(clear)]((grid_x-x/2)**2 + (grid_y-y/2)**2 , r**2,1e-9)
    # Apply anti-aliasing using Gaussian blur
    # blurred_circle = gaussian_filter(circle_mask.astype(float), sigma=antialias_sigma)

    # Threshold to create a binary image (0 or 1)
    pixelated_circle = np.where(circle_mask > 0.5, 0, 1)

    # mul mask
    if Grid is not  None:
        Grid = Grid*pixelated_circle
    
    return pixelated_circle
grid = np.zeros((200,200))
grid[:,:]=1
circ=circle(50,50,50,1,1,fill=True,clear=True,Grid=grid)
    
plt.imshow(circ, cmap='gray')
plt.title('Pixelated Circle with Anti-aliasing')
plt.show()