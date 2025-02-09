from ...utilis.geometry import circle,annulus
import numpy as np


def geometryFactory(val=1.0,r1=35,r2=50,cx=50,cy=100,relative=False):
    Gridder = None
    def endToEndLine(Grid:np.ndarray,overlay=None,retoverlay=False):
        width,height = Grid.shape
        circ1 = annulus(100,100,50,r1,r2,fill=True,clear=False,Grid=grid)
        return Grid
    return endToEndLine