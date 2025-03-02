import numpy as np
from ...utils.geometry import circle

def geometryFactory(val=1.0,r=35,cx=50,cy=100,relative=False):
    Gridder = None
    def endToEndLine(Grid:np.ndarray, overlay=None, retoverlay=False, *args, **kwargs):
        nonlocal Gridder
        Grid[(0,-1), 1:-1] = 0.25*(Grid[(0,-1), 2:]+Grid[(0,-1), :-2]+Grid[(-1,-2), 1:-1]+Grid[(1,0), 1:-1])
        Grid[:,:2]=val

        Grid[:,-2:]=-val

        if overlay is None:
            if Gridder is None:
                Gridder = overlay = circle(cx,cy,r,fill=True,clear=True,Grid=(*Grid.shape,))
            else:
                overlay = Gridder
        Grid = overlay*Grid
        return Grid
    return endToEndLine