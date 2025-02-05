import numpy as np


def geometryFactory(val=1.0,r=35,cx=50,cy=100,relative=False):
    Gridder = None
    def endToEndLine(Grid:np.ndarray,overlay=None,retoverlay=False):
        Grid[(0,-1), 1:-1] = 0.25*(Grid[(0,-1), 2:]+Grid[(0,-1), :-2]+Grid[(-1,-2), 1:-1]+Grid[(1,0), 1:-1])
        height,width=Grid.shape
        Grid[:,:2]=val
        midx = width//2
        startx=midx-width//8
        endx=midx+width//8


        height,width=Grid.shape
        Grid[:,-2:]=-val
        midx = width//2
        startx=midx-width//8
        endx=midx+width//8

        if overlay is None:
            overlay = geometry.circle(cx,cy,r,fill=True,clear=True,Grid=(*Grid.shape,))
        debug = False
        Grid = overlay*Grid
        if retoverlay:
            return Grid,overlay
        return Grid
    return endToEndLine