import inspect, functools, itertools
import numpy as np
def functionMaker(n:int,m:int,dx:int=1,dy:int=1):
    def XLin(x,*args):
        result = 0
        for i in range(1,n+dx,dx):
            result += args[-i]*(x**(i))
        return result
    
    def YLin(y,*args):
        result = 0
        for i in range(1,n+dx,dx):
            result += args[-i]*(y**(i))
        return result
    
    def polyProduct(x,y,xcoeffs = None,ycoeffs = None):
        return XLin(x,*xcoeffs)*YLin(y,ycoeffs)
    
    return XLin,YLin,polyProduct