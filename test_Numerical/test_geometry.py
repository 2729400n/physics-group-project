# import  os
# os.chdir('C:\\Users\\Kevnn\\GroupProject\\physics-group-project\\')
import sys
sys.path.append('C:\\Users\\Kevnn\\GroupProject\\physics-group-project\\')

import Numerical_Methods.utils.geometry as geometry
import matplotlib.patches,matplotlib.path,matplotlib.pyplot as plt
import numpy as np

methods = ['none']#, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
           #'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
           #'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']

class Test_Geometries:
    
    def test_circle(self):
        grid = np.zeros((400,400))
        grid[:,:]=1
        # circ=geometry.annulus(200,200,100,200,1,fill=False,clear=False,Grid=grid)
        circ = geometry.circle(500,500,500,thickness=3)
        
        # Fixing random state for reproducibility

        fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(18, 18),
                                subplot_kw={'xticks': [], 'yticks': []},squeeze=False)

        for ax, interp_method in zip(axs.flat, methods):
            ax.imshow(circ, cmap='gray',interpolation=interp_method)
            # ax.set_title(str(interp_method))
        plt.suptitle('Pixelated Circle with Anti-aliasing')
        plt.tight_layout()
        plt.show()
        

if __name__ == '__main__':
    geom = Test_Geometries()
    geom.test_circle()