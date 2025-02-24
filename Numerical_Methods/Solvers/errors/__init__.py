import numpy as np



def laplaceify(grid:np.ndarray,dx,dy):
    dphi_dx_2 = (grid[:,:-2] - 2*grid[:,1:-1]+ grid[:,2:])/(dx**2)
    dphi_dy_2 = (grid[:-2,:] - 2*grid[1:-1,:]+ grid[2:,:])/(dy**2)
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

