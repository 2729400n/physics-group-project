import matplotlib.artist,matplotlib.patches,matplotlib.path,matplotlib.pyplot as plt
import numpy as np


def circleQuadrant(cx,cy,r,dx,dy,val=1.0,fill=False,clear=False,Grid=None):
    # First solve for a qudrant the apply rotations
    operations = [[lambda x,y,z:np.abs(x-y)<z]*2,[lambda x,y,z:x<=y,lambda x,y,z:x>=y]]
    r1 = np.array([0,r])
    r2 = np.array([r,0])
    theta = np.linspace(0,np.pi/4,1000)
    grid_x, grid_y = np.mgrid[:2*int(r//dx), :2*int(r//dy)]
    circle_mask = operations[bool(fill)][bool(clear)]((grid_x - cx)**2 + (grid_y - cy)**2 , r**2,1e-9)

    # Apply anti-aliasing using Gaussian blur
    # blurred_circle = gaussian_filter(circle_mask.astype(float), sigma=antialias_sigma)

    # Threshold to create a binary image (0 or 1)
    pixelated_circle = np.where(circle_mask > 0.5, 1, 0)
    grid[int(cy-r//dx):(4*int(r//dx))//2+int(r//dx),(4*int(r//dy))//2-int(r//dy):(4*int(r//dy))//2+int(r//dy)] = pixelated_circle
    return grid

circ=circleQuadrant(50,50,50,1,1,fill=True)
    
plt.imshow(circ, cmap='gray')
plt.title('Pixelated Circle with Anti-aliasing')
plt.show()