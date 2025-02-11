from ...utils.geometry import circle,annulus
import numpy as np


# Will employ the use of a closure to ensure uniqueness for multi-threading
def geometryFactory(val:float=1.0,r1:float=35,r2:float=50,cx:float=50,cy:float=100,relative=False):
    # A simple cacher 
    Gridder = None
    def AnnulusField(Grid:np.ndarray,overlay:bool=None,retoverlay:bool=False):
        nonlocal Gridder
        if Gridder is None:
            width,height = Grid.shape
            circ1 = annulus(100,100,50,r1,r2,val=val,fill=True,clear=False,Grid=Grid)
            Gridder = circ1
        return Grid*Gridder
    return AnnulusField