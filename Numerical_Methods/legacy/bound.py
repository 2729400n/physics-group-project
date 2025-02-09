from geometry import circle
import numpy as np


if __name__ == '__main__':
    import matplotlib.artist,matplotlib.patches,matplotlib.path,matplotlib.pyplot as plt
    grid = np.zeros((202,202))
    grid[:,:]=1
    circ=circle(101,101,100,1,1,fill=True,clear=False,Grid=grid)
    
        
    plt.imshow(circ, cmap='gray')
    plt.colorbar()
    plt.title('Pixelated Circle with Anti-aliasing')
    plt.show()
    
    grid[:,:] = 1
    circ2 = circle(101,101,50,1,1,fill=True,clear=True,Grid=grid)
    plt.imshow(circ2+circ, cmap='gray')
    plt.colorbar()
    plt.title('Pixelated Circle with Anti-aliasing')
    plt.show()
