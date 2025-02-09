from Numerical_Methods.utils import geometry
import matplotlib.artist,matplotlib.patches,matplotlib.path,matplotlib.pyplot as plt
import numpy as np
import check_user_approval

class Test_Geometries:
    
    def test_circle(self):
        grid = np.zeros((200,200))
        grid[:,:]=1
        circ=geometry.annulus(100,100,50,100,2,fill=False,clear=False,Grid=grid)
        
        fig=plt.figure()
        plt.imshow(circ, cmap='gray')
        plt.colorbar()
        plt.title('Pixelated Circle with Anti-aliasing')
        plt.show(block=False)
        
        assert(check_user_approval.didItWorkAsIntended()==0)
        plt.close()