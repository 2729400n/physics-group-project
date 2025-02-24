import types
import typing
from matplotlib import pyplot as plt
import numpy as np
from ...utils import geometry



class GeometryFactory(typing.Callable):
    def __int__(self,seperation, plate_seperation, V, cx, cy:'float|str'='centre'):
        self.grnd1:'str' = None
        self.V_plus: 'str' = None
        self.grnd2:'str' = None
        self.V_negative: 'str' = None


def geometryFactory(radius, seperation, plate_seperation, V, cx, cy:'float|str'='centre'):
    cache:'list' = []
    def bounds(grid:np.ndarray, x_axis:bool = True, x_offset=0, y_offset=0, NNCount:int=3):
        nonlocal cache
        grid_shape = grid.shape
        
        
        if isinstance(cy,str):
            if cy == 'centre':
                cy = grid.shape[0]/2
        center_distance = 2*np.abs(radius)+np.abs(seperation)
        print(center_distance)
        cx_s=cx+np.array([center_distance*i for i in range(-NNCount,1+NNCount,1)])
        circles = []
        canvas = np.ones_like(grid)
        for cx_i in cx_s:
            c1 = geometry.circle(cx_i, cy, radius, 1.0, 1.0,
                                val=1.0, fill=True, clear=True,Grid=tuple(grid.shape))
            circles.append(c1)
            canvas = canvas*c1
        canvas[:,(0,-1)]=-V
        grid[:,:] = canvas[:,:]
        return grid
    return bounds


if __name__ == "__main__":
    EGrid = np.ones((500,500))
    EGrid=bounds(EGrid,40,40,90,5,100,'centre',True,0,0,3)
    plt.figure(figsize=(15,15))
    plt.imshow(EGrid)
    plt.colorbar()
    plt.show()