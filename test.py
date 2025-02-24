

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
        for i in range(0, n + dx, dx):
            result += args[i] * (x ** (n-i))
        
        # constrain to a widely availible floating point representation
        return np.float64(result)

    # Defines an linear Polynomial function for X given n Parameters
    # Does the same thing that the XLin does
    def YLin(y, *args):
         
        result = 0
        
        for i in range(0, m + dy, dy):
            result += args[i] * (y ** (m-i))
            
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
            for i in range(0, n+1, 1)
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
            for i in range(0, m+1, 1)
        ]
    
    yParams = yParam+yCoeffParams
    
    YLin.__signature__ = inspect.Signature(
        yParams,
        return_annotation=np.float64,
        __validate_parameters__=True,
    )
    
    
    
    
    
    
    
    mixedParam = [
        inspect.Parameter(
                f"point",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.ndarray,
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
            for i in range(0, (n+1)*(m+1), 1)
        ]
    
    fullSuiteParams = mixedParam+mixedParams
    
    def polyProduct(point:np.ndarray, xcoeffs:'list[float]'=None, ycoeffs:'list[float]'=None,*coeffs):
        if(point.ndim)==2:
            x=point[:,:,1]
            y=point[:,:,0]
        else:
            x=point[:,1]
            y=point[:,0]
        coeff_len = len(coeffs)
        interpolated_func = XLin(x, *xcoeffs) * YLin(y, ycoeffs)
        
        xs=np.vander([x],n)
        ys=np.vander([y],m)
        fixingProduct = ((xs.T@ys).flatten())*coeffs
        
        return interpolated_func+fixingProduct
            

    
    polyProduct.__signature__ = inspect.Signature(
        fullSuiteParams,
        return_annotation=np.float64,
        __validate_parameters__=True,
    )
    
    
    
    # return the X-dependent Linear polynomial, 
    # Y Linear Polynomial and Polynomial Product function
    return XLin, YLin, polyProduct


# A default ready made but slow fitting function 
def InterpolateGrid(Grid:'np.ndarray',x0:'np.ndarray',y0:'np.ndarray',x1:'np.ndarray',y1:'np.ndarray',dy:float=1.0,dx:float=1.0,xmaxfev:int=None,ymaxfev:int=None,xymaxfev:int=None,xtol:float=None,ytol:float=None,xytol:float=None):
    (m,n) = Grid.shape
    if m<1 or n<1:
        raise 'Cannot interpolate an empty grid'
    XPolyNomial,YPolyNomial,XYPolyNomial=functionMaker(n-1,m-1)
    
    Xs=np.arange(x0,x1+dx,dx)
    Ys=np.arange(y0,y1+dy,dy)
    
    xCov=None
    yCov = None
    
    print(XPolyNomial.__signature__)
    print(YPolyNomial.__signature__)
    print(XYPolyNomial.__signature__)
    input('...')
    params =[xmaxfev,ymaxfev,xymaxfev]
    runtimes =[n,m,n*m]
    xmaxfev,ymaxfev,xymaxfev = [params[i] if params[i] is not None else 999*runtimes[i] for i in range(3)]
    try:
        # Using curve fit is lazy but its better than writing a lsq function
        xOptimal,xCov=optimist.curve_fit(XPolyNomial,Xs,Grid[0,:],maxfev=xmaxfev)
        
    except RuntimeError as e:
        print(e)
        xOptimal = np.polyfit(Xs,Grid[0,:],n-1)
    print('XOptimal=',xOptimal)
    print('XCov=',xCov) if xCov is not None else None
    try:
        yOptimal,yCov=optimist.curve_fit(YPolyNomial,Ys,Grid[:,0].T,maxfev=ymaxfev)
        
    except RuntimeError as e:
        print(e)
        yOptimal = np.polyfit(Ys,Grid[:,0].T,m-1)

    print('YOptimal=',yOptimal)
    print('YCov=',xOptimal) if yCov is not None else None
    
    YGrid,XGrid = np.meshgrid(Ys,Xs)
    points=np.stack((YGrid,XGrid),-1)
    print(points)
    points =points.reshape(points.shape[0]*points.shape[1],2)
    
    def __innerProduct():
        nonlocal xOptimal,yOptimal
        
        def ___innerProduct(point:np.ndarray[np.float64,np.float64],*args):
            nonlocal xOptimal,yOptimal
            return XYPolyNomial(point,xOptimal,yOptimal,*args)
        
        def _innerProduct(*args):
            nonlocal ___innerProduct
            return ___innerProduct(*args)
        
        sig = inspect.signature(XYPolyNomial)
        sig = inspect.Signature([sig.parameters.get(param) for param in sig.parameters if param!='xcoeffs' and param!='ycoeffs'])
        _innerProduct = np.frompyfunc(_innerProduct,2,1)
        _innerProduct.__signature__ =___innerProduct.__signature__= sig
        _innerProduct = np.vectorize(_innerProduct,signature=___innerProduct.signature)
        _innerProduct.__signature__=_innerProduct.signature=___innerProduct.__sign
        input('...')
        # TODO add a function signature to _innerProduct before returning it
        return _innerProduct
    XYoptimal = None
    XYcov = None
    polyProd = __innerProduct()
    
    if (XYoptimal is not None):
        XYoptimal,XYcov = optimist.curve_fit(polyProd,points,Grid.flatten(),p0=XYoptimal,sigma=XYcov,maxfev=999)
    else:
        XYoptimal,XYcov = optimist.curve_fit(polyProd,points,Grid.flatten(),maxfev=999)
    return xOptimal,yOptimal,XYoptimal
        
                                      
    
if __name__ == '__main__':
    def PolYproduct(x,y):
        return (2*(x**2)+2*(x)+3)
    n_ = 10
    m_ =10
    Ygrid,Xgrid = np.mgrid[:m_,:n_]

    print(Xgrid,Ygrid,sep='\n\n')
    input()

    grid = PolYproduct(Xgrid,Ygrid)
    print(grid)
    input('Ready ?')

    xopt,yopt,xyopt = InterpolateGrid(grid,0,0,n_-1,m_-1)
    print(xopt,yopt,xyopt)
    input('Done!')