import numpy as np
from .geometry import circleQuadrant
def BoxinBox(Grid:np.ndarray,r):
    height,width=Grid.shape

    circleQuadrant(50,50,50,1,1,fill=True,Grid=Grid)
    Grid[:,(0,-1)]=Grid[(0,-1),:]=1.0

    return Grid