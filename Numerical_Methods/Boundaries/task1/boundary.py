from ...geometry import circle
import numpy as np


def geometryFactory(val=1.0,r1=35,r2=50,cx=50,cy=100,relative=False):
    Gridder = None
    def endToEndLine(Grid:np.ndarray,overlay=None,retoverlay=False):
        width,height = Grid.shape
        circ1 = circle(width//2, height//2, r,1,1,fill=True,clear=False,Grid=Grid)
        circ2 = circle(width//2, height//2, 50,1,1,fill=True,clear=True,Grid=Grid)
        Grid = circ2+circ1

        return Grid
    return endToEndLine