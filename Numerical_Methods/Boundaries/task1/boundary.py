from ...utils.geometry import circle,annulus
import numpy as np


# Will employ the use of a closure to ensure uniqueness for multi-threading
def geometryFactory(val:float=1.0,r1:float=35,r2:float=50,cx:float=100,cy:float=100,relative=False):
    # A simple cacher 
    Gridder = None
    def AnnulusField(Grid:np.ndarray,overlay:bool=None,retoverlay:bool=False):
        nonlocal Gridder
        if Gridder is None:
            width,height = Grid.shape
            circ1 = circle(cx,cy,50,val=1.0,fill=True,clear=True,Grid=Grid)
            circ2 = circle(cx,cy,100,val=1.0,fill=True,clear=False,Grid=Grid)
            circ3 = circle(cx,cy,100,val=(True,False),fill=False,clear=False,Grid=Grid)
            
            Gridder = [circ1*circ2,circ3]
        temp1 = Grid*Gridder[0]
        temp1[Gridder[1]] = val
        return temp1
    return AnnulusField