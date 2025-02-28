from typing import Literal
import numpy as np

from .interpolation_stuff import functionMaker,InterpolateGrid_fastest

def laplaceify(grid:'np.ndarray[np.ndarray[np.float64]]',dx,dy,wrap=False,wrap_direction:Literal['x','y','both','none']='none'):
    errors = np.zeros_like(grid)
    dphi_dx_2 = ((grid[:,:-2] - 2*grid[:,1:-1]+ grid[:,2:])/(dx**2))[1:-1]
    dphi_dy_2 = ((grid[:-2,:] - 2*grid[1:-1,:]+ grid[2:,:])/(dy**2))[:,1:-1]
    
    if wrap:
        pass
        
    residuals =dphi_dx_2+dphi_dy_2
    abs_residuals = np.abs(residuals)
    
    return residuals, abs_residuals
class ErrorCalculator:
    def __init__(self,valuesA, valuesB,func:'function'=lambda x:x):
        self.Avals:np.ndarray = valuesA
        self.Bvals:np.ndarray = valuesB
        self._error:np.ndarray = None
        self._abserror  =None
        self._relativeError = None
        
        
        return
    
    def _getabsError(self):
        return
    
    def _getRelativeError(self):
        if self._relativeError is not None:
            return self._relativeError
        
        absA = np.abs(self.Avals)
        
        self._getabsError()
        
    
    
    
    def findError(self):
        self.error=(self.Avals-self.Bvals)

