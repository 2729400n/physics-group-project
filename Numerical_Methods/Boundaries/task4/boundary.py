import types
import typing
from matplotlib import pyplot as plt
import numpy as np
from ...utils import geometry



class GeometryFactory(typing.Callable):
    def __init__(self,seperation:float=3.0, plate_seperation:float=5.0,  V:float=1.0,
                cx:float=0.0, cy:float=0.0,radius:float=3.0, center:bool=True,half_plate_sep:bool=False,
                NNCount:int=1,dx:float=1.0,dy:float=1.0):
        self.Gridder = None
        self.center = center
        self.radius = radius
        self.seperation = seperation
        self.plate_seperation = np.abs(plate_seperation)
        self.half_plate_sep = half_plate_sep
        self.V = V
        self.cx = cx
        self.cy = cy
        self.NNCount = NNCount
        self.dx = dx
        self.dy = dy
        self.circles:'list[np.ndarray[np.float64]]'=None
        self.grid_shape= None
    
    def __call__(self,Grid: np.ndarray, overlay=None, retoverlay=False, *args, **kwargs):
        grid = Grid.copy()
        if (self.circles is None) or (self.grid_shape != grid.shape):
            self.circles = []
            self.grid_shape = grid.shape
        
            if self.center:
                cy = (grid.shape[0]/2)*self.dy
                cx = (grid.shape[1]/2)*self.dx
            else:
                cy = self.cy
                cx = self.cx
                
                    
            center_distance = 2*np.abs(self.radius)+np.abs(self.seperation)
            cx_s=cx+np.array([center_distance*i for i in range(-self.NNCount,1+self.NNCount,1)])
            
            for cx_i in cx_s:
                c1 = geometry.circle_bool(cx_i, cy, self.radius, 1.0, 1.0, fill=True, clear=False,Grid=tuple(grid.shape))
                self.circles.append(c1)
                grid[c1]=0
        else:
            for i in self.circles:
                grid[i]=0
        if self.half_plate_sep:
            grid[-1,:] =-self.V
            grid[0,:] =-self.V
            return grid
        midy=(grid.shape[0]/2)*self.dy
        # midx=(grid.shape[1]/2)*self.dx
        eachsep = (self.plate_seperation/2)
        topPlate=midy+eachsep
        bottomPlate=midy-eachsep
        # print(eachsep)
        
        topPlate=int(np.ceil(topPlate/self.dy))
        bottomPlate=int(np.floor(bottomPlate/self.dy))
        
        if topPlate>(grid.shape[0]+1):
            topPlate=(topPlate%grid.shape[0])
        if bottomPlate<0:
            bottomPlate=(bottomPlate%grid.shape[0])
        
        grid[(topPlate),:] =-self.V
        grid[bottomPlate,:] =-self.V
        return grid
    
    def shift_circle(self,cirlce_index:int=0,cx:float=0.0,cy:float=0.0):
        self.circles[cirlce_index] = geometry.circle_bool(cx, cy, self.radius, 1.0, 1.0, fill=True, clear=True,Grid=tuple(self.circles[cirlce_index].shape))
    
    def shift_circle_displace(self,cirlce_index:int=0,d_x:float=0.0,d_y:float=0.0):
        self.circles[cirlce_index] = geometry.circle_bool(self.cx+d_x, self.cy+d_y, self.radius, 1.0, 1.0, fill=True, clear=True,Grid=tuple(self.circles[cirlce_index].shape))


