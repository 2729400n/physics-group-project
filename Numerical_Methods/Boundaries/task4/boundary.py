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


def geometryFactory(radius, seperation, plate_seperation, V, cx, cy:'float|str'=0.0, center:bool=True,NNCount:int=1,dx:float=1.0,dy:float=1.0):
    cache:'list' = []
    def bounds(Grid:np.ndarray, x_axis:bool = True, x_offset=0, y_offset=0):
        nonlocal cache,cy,cx,center,radius,seperation,plate_seperation,V,NNCount
        grid = Grid
        grid_shape = grid.shape
        
        if center:
                cy = grid.shape[0]/2
                cx = grid.shape[1]/2
            
                
        center_distance = 2*np.abs(radius)+np.abs(seperation)
        cx_s=cx+np.array([center_distance*i for i in range(-NNCount,1+NNCount,1)])
        circles = []
        canvas = np.zeros_like(grid)
        for cx_i in cx_s:
            c1 = geometry.circle(cx_i, cy, radius, 1.0, 1.0,
                                val=1.0, fill=True, clear=True,Grid=tuple(grid.shape))
            circles.append(c1)
            canvas = canvas*c1
        grid[:,:] = canvas[:,:]
        grid[:2,:] =1
        grid[:-2,:] =1
        return grid
    return bounds

