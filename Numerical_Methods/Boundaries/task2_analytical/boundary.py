import numpy as np
from ...utils.geometry import circle


import typing
from ...utils.geometry import circle,annulus,circle_bool
import numpy as np


class GeometryFactory(typing.Callable):
    
        
    def __init__(self,val=1.0,r=35,cx=50,cy=100,dx:float=1.0,dy:float=1.0,relative=False):
        
        self.cx=cx
        self.cy=cy
        
        self.r=r
        
        self.val =val
        
        self.dx=dx
        self.dy = dy
        
        self.cache=None
        
        
    def __call__(self,Grid:np.ndarray, overlay=None, retoverlay=False, *args, **kwargs):
        
        cx =self.cx
        cy = self.cy
        r=self.r
        val = self.val
        Grid = Grid.copy()
        if overlay is None:
            if self.cache is None:
                self.cache = overlay = circle_bool(cx,cy,r,fill=True,clear=False,Grid=(*Grid.shape,))
            else:
                overlay = self.cache
        
        
        
        Grid[overlay] = 0
        Grid[:, :2]=val

        Grid[:,-2:]=-val
        return Grid

    def calculateField(self, Grid:np.ndarray[np.float64]=None):
        # Parameters
        r1 = self.r  # Inner radius for the potential region
        V = self.val   # Potential scaling constant

        cx=self.cx
        cy=self.cy
        
        dy=self.dy
        dx=self.dx
        height=Grid.shape[0]/dy
        width = Grid.shape[1]/dx
        
        temp1=Grid.copy()
        
        pot = np.zeros_like(temp1)
        
        y_grid,x_grid=np.mgrid[:height:dy,:width:dx]
        
        # Mask: Only consider points where r1 <= r <= r2
        
        r_2_grid=(y_grid-cy)**2+(x_grid-cx)**2
        
        mask_grid = (r_2_grid> (r1**2)) 
        r_grid=np.sqrt(r_2_grid)

        # Initialize the potential and electric field arrays
        u_v = np.zeros((*pot.shape,2),dtype=np.float64)
        theta = np.zeros_like(pot)
        
        theta[mask_grid] = np.arctan2(y_grid-cy, x_grid-cx)[mask_grid]
        
        pot=temp1

        # Radial component (dV/dr)
        dV_dr = ((V/width)*(np.cos(theta)*(r1**2)/r_grid**2 + np.cos(theta)))

        # Angular component (dV/dtheta)
        dV_dtheta = (V/width)*(np.sin(theta)*(r1**2)/r_grid**2 - np.sin(theta))

        # Convert the polar electric field components to Cartesian components
        u_v[mask_grid,0] = (-dV_dr * np.cos(theta) + dV_dtheta * np.sin(theta))[mask_grid]
        u_v[mask_grid,0] = (-dV_dr * np.sin(theta) + dV_dtheta * np.cos(theta))[mask_grid]

        # Now, let's calculate the potential based on the mask condition
        pot[mask_grid] = ((r_grid - ((r1**2)/((r_grid)))) * ((-V/width) * np.cos(theta)))[mask_grid]
        return pot,u_v
    
