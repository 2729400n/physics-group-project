from ...utils.geometry import circle,annulus,circle_bool
import numpy as np


# Will employ the use of a closure to ensure uniqueness for multi-threading
def geometryFactory(val1:float=1.0,val2:float=-1.0,val3:float=0.0,r1:float=35,r2:float=50,r3:float=100,cx:float=100,cy:float=100,relative=False):
    
    # A simple cacher 
    Gridder:'list[np.ndarray[np.ndarray[np.float64]], np.ndarray[np.ndarray[np.bool]]]' = None
    
    def AnnulusField(Grid:np.ndarray,overlay:bool=None,retoverlay:bool=False):
        nonlocal Gridder
        temp1 = Grid.copy()
        if Gridder is None:
            width,height = Grid.shape
            circ1 = circle_bool(cx,cy,r1,val=True,fill=True,clear=False,Grid=(width,height))
            circ2 = circle_bool(cx,cy,r2,val=True,fill=False,clear=False,Grid=(width,height))
            circ3 = circle_bool(cx,cy,r3,val=True,fill=False,clear=False,Grid=(width,height))
            circ4 = circle(cx,cy,np.max(np.abs([r1,r2,r3])),val=1,fill=True,clear=False,Grid=(width,height))
            Gridder = [circ1,circ2,circ3,circ4]
        
        temp1[Gridder[0]] = val1
        temp1[Gridder[1]] = val2
        temp1[Gridder[2]] = val3
        temp1 = temp1*Gridder[3]
        
        return temp1
    return AnnulusField