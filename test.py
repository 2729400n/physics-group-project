import inspect
import numpy as np
import scipy.optimize as optimist
import numpy.linalg as linalg



# A function to make polynomial functions 
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
    
    # Defines an linear Polynomial function for X given n Parameters
    def XLin(x, *args):
        
        # initilizes the results variable
        result = 0
        
        # Evaluates te polynomial terms and adds them together
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

    def polyProduct(x, y, xcoeffs:'list[float]'=None, ycoeffs:'list[float]'=None,*coeffs):
        coeff_len = len(coeffs)
        return XLin(x, *xcoeffs) * YLin(y, ycoeffs) + sum([i for i in range(coeff_len)])

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
            )
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
    
    polyProduct.__signature__ = inspect.Signature(
        mixedParams,
        return_annotation=np.float64,
        __validate_parameters__=True,
    )
    
    # return the X-dependent Linear polynomial, 
    # Y Linear Polynomial and Polynomial Product function
    return XLin, YLin, polyProduct


# A default ready made but slow fitting function 
def InterpolateGrid(Grid:'np.ndarray',x0:'np.ndarray',y0:'np.ndarray',x1:'np.ndarray',y1:'np.ndarray'):
    (n,m) = Grid.shape
    XPolyNomial,YPolyNomial,XYPolyNomial=functionMaker(n,m)
    xOptimal,xCov=optimist.curve_fit(XPolyNomial,Grid[0,:],Grid[0,:])
    yOptimal,yCov=optimist.curve_fit(YPolyNomial,Grid[0,:],Grid[:,0].T)
    
    def __innerProduct(x:np.float64,y:np.float64):
        nonlocal xOptimal,yOptimal
        def _innerProduct(x,*args):
            nonlocal xOptimal,yOptimal
            return XYPolyNomial(x,y,xOptimal,yOptimal,*args)
        sig = inspect.signature(_innerProduct)
        
        # TODO add a function signature to _innerProduct before returning it
        return _innerProduct
    yOptimal,yCov=optimist.curve_fit(YPolyNomial,Grid[0,:],Grid[0,:])
    
    