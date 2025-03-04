import typing
from ...utils.geometry import circle,annulus,circle_bool
import numpy as np


class GeometryFactory(typing.Callable):
    
        
    def __init__(self,V:float=1.0,r1:float=35,r2:float=50,cx:float=100,cy:float=100,relative=False,dx:float=1.0,dy:float=1.0):
        
        
        self.circles:'list[np.ndarray[np.ndarray[np.float64]], np.ndarray[np.ndarray[np.bool]]]' = None
        
        self.cx=cx
        self.cy=cy
        
        self.r1=r1
        self.r2=r2
        
        self.V =V
        
        self.dx=dx
        self.dy = dy
        
        
    def __call__(self,Grid:np.ndarray,overlay:bool=None,retoverlay:bool=False):
        V = self.V
        cx = self.cx
        cy = self.cy
        r1 = self.r1
        r2 = self.r2
        dy  = self.dy
        dx = self.dx
        temp1 = Grid.copy()
        
        if self.circles is None:
            width,height = Grid.shape
            circ1 = circle(cx,cy,r1,val=1.0,fill=True,clear=True,Grid=(width,height))
            circ2 = circle(cx,cy,r2,val=1.0,fill=True,clear=False,Grid=(width,height))
            circ3 = circle_bool(cx,cy,r2,val=True,fill=False,clear=False,Grid=Grid)
            
            self.circles = [circ1*circ2,circ3]
        temp1 = Grid*self.circles[0]
        temp1[self.circles[1]] = V
        if retoverlay:
            return temp1,None
        return temp1

    def calculateField(self, Grid:np.ndarray[np.float64]=None):
        # Parameters
        r1 = self.r1  # Inner radius for the potential region
        r2 = self.r2  # Outer radius for the potential region
        V = self.V   # Potential scaling constant

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
        
        mask_grid = np.logical_and((r_2_grid>= (r1**2)) , (r_2_grid <= r2**2))
        r_grid=np.sqrt(r_2_grid)

        # Initialize the potential and electric field arrays
        u_v = np.zeros((*pot.shape,2),dtype=np.float64)
        v = np.zeros_like(pot)
        E_r =np.zeros_like(pot)
        theta = np.zeros_like(pot)

        pot[mask_grid] = ((V * np.log(r1) - V * np.log(r_grid)) / (np.log(r1) - np.log(r2)))[mask_grid]
        E_r[mask_grid] = (V / (np.log(r2 / r1) * r_grid))[mask_grid]

        
        
        theta[mask_grid] = np.arctan2(y_grid-cy, x_grid-cx)[mask_grid]
        x_y= np.array((E_r * np.abs([np.cos(theta),np.sin(theta)]))[:,mask_grid]) # x-component of electric field
        u_v[mask_grid]=x_y.T
        pot=self(pot)
        return pot,u_v