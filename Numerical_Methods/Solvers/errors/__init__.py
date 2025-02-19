import numpy as np
import numba as nb

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
        
        
print(np.spacing(1))