

import inspect
import numpy as np
import scipy.optimize as optimist
import numpy.linalg as linalg



# A polynomial function maker and an XY Product Maker
def functionMaker(n: int, m: int, dx: int = 1, dy: int = 1):
    '''
    Args:
        n: int - The size of the polynomial in the Minor axis
        m: int - The size of the polynomial in the Major axis 
    Returns:
        XLin: function - A linear Polynomial function that depends soley on x
        YLin: function - A linear Polynomial function that depends soley on y
        polyProduct: function - A linear Polynomial function that depends on x and y
    Details:
    
    '''
    
    # Defines an linear Polynomial function dependent only on x given n Parameters
    def XLin(x, *args):
        '''
        XLin: A linear polynomial in one axis.
        
        We generalise the idea of unkowns.
        
            x:  The value of x at the point we want to soove the polynomial
        *args:  The polynomial coefficients in order of most important to least important 
        '''
        
        # initilizes the results variable to zero
        result = 0
        
        # Evaluates each polynomial terms and adds them together
        for i in range(1, n + dx, dx):
            result += args[-i] * (x ** (i))
        
        # constrain to a widely availible floating point representation
        return np.float64(result)

    # Defines an linear Polynomial function for X given n Parameters
    # Does the same thing that the XLin does
    def YLin(y, *args):
         
        result = 0
        
        for i in range(1, m + dy, dy):
            result += args[-i] * (y ** (i))
            
        return np.float64(result)

    

    # Everything in this function context beyond here is for compatibility with 
    # introspective curve fitter. For most people this can be ignored
    
    xParam = [inspect.Parameter(
                f"x",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            )]

    xCoeffParams = [
            inspect.Parameter(
                f"x_{i}",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            )
            for i in range(0, n, 1)
        ]
    
    xParams  = xParam+xCoeffParams
    
    XLin.__signature__ = inspect.Signature(
        xParams,
        return_annotation=np.float64,
        __validate_parameters__=True,
    )
    
    yParam = [
            inspect.Parameter(
                f"y",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            )]
    
    yCoeffParams = [
            inspect.Parameter(
                f"y_{i}",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            )
            for i in range(0, m, 1)
        ]
    
    yParams = yParam+yCoeffParams
    
    YLin.__signature__ = inspect.Signature(
        yParams,
        return_annotation=np.float64,
        __validate_parameters__=True,
    )
    
    
    
    
    
    
    
    mixedParam = [
        inspect.Parameter(
                f"x",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            ),
        inspect.Parameter(
                f"y",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            ),
        inspect.Parameter(
                f"xcoeffs",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            ),
        inspect.Parameter(
                f"ycoeffs",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            ),
    ]
    
    mixedParams = [
            inspect.Parameter(
                f"c_{i}",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            )
            for i in range(0, n*m, 1)
        ]
    
    def polyProduct(x, y, xcoeffs:'list[float]'=None, ycoeffs:'list[float]'=None,*coeffs):
        coeff_len = len(coeffs)
        interpolated_func = XLin(x, *xcoeffs) * YLin(y, ycoeffs)
        
        xs=np.vander([x],n)
        ys=np.vander([y],m)
        fixingProduct = ((xs.T@ys).flatten())*coeffs
        
        return interpolated_func+fixingProduct
            

    
    polyProduct.__signature__ = inspect.Signature(
        mixedParams,
        return_annotation=np.float64,
        __validate_parameters__=True,
    )
    
    
    
    # return the X-dependent Linear polynomial, 
    # Y Linear Polynomial and Polynomial Product function
    return XLin, YLin, polyProduct


# A default ready made but slow fitting function 
def InterpolateGrid(Grid:'np.ndarray',x0:'np.ndarray',y0:'np.ndarray',x1:'np.ndarray',y1:'np.ndarray',dy:float=1.0,dx:float=1.0):
    (n,m) = Grid.shape
    XPolyNomial,YPolyNomial,XYPolyNomial=functionMaker(n,m)
    
    Xs=np.arange(x0,x1+dx,dx)
    Ys=np.arange(y0,y1+dy,dy)
    
    # Using curve fit is lazy but its better than writing a lsq function
    xOptimal,xCov=optimist.curve_fit(XPolyNomial,Xs,Grid[0,:])
    yOptimal,yCov=optimist.curve_fit(YPolyNomial,Ys,Grid[:,0].T)
    
    def __innerProduct(y:np.float64):
        nonlocal xOptimal,yOptimal
        def _innerProduct(x:np.float64,*args):
            nonlocal xOptimal,yOptimal
            return XYPolyNomial(x,y,xOptimal,yOptimal,*args)
        sig = inspect.signature(XYPolyNomial)
        sig = inspect.Signature([sig.parameters.get(param) for param in sig.parameters if param!='y'])
        
        _innerProduct.__signature__ = sig
        
        # TODO add a function signature to _innerProduct before returning it
        return _innerProduct
    XYoptimal = None
    XYcov = None
    for i in range(0,Ys.shape[0]):
        polyProd = __innerProduct(Ys[i])
        
        if (XYoptimal is not None):
            XYoptimal,XYcov = optimist.curve_fit(polyProd,Xs,Grid[i,:],p0=XYoptimal,sigma=XYcov)
        else:
            XYoptimal,XYcov = optimist.curve_fit(polyProd,Xs,Grid[i,:])
    return xOptimal,yOptimal,XYoptimal
        
                                      
    
    
def PolYproduct(x,y):
    return (2*(x**2)+2*(x)+2)*(3*(y**2)+3*(y)+3)

Xgrid,Ygrid = np.mgrid[:100,:100]

print(Xgrid,Ygrid,sep='\n\n')
input()

grid = PolYproduct(Xgrid,Ygrid)
print(grid)
input('Ready ?')

xopt,yopt,xyopt = InterpolateGrid(grid,0,0,99,99)

print(xopt,yopt,xyopt)
