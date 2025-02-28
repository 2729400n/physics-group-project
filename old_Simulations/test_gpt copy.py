import inspect
from matplotlib import pyplot as plt
import numpy as np
import scipy.optimize as optimist
import numpy.linalg as linalg
import numbers,math

Unknown = np.spacing(np.float64(2**16-1))

# A polynomial function maker and an XY Product Maker
def functionMaker(n: int, m: int, dx: int = 1, dy: int = 1):
    '''
    Args:
        n: int - The size (degree+1) of the polynomial in the X direction
        m: int - The size (degree+1) of the polynomial in the Y direction 
    Returns:
        XLin: function - A polynomial function that depends solely on x
        YLin: function - A polynomial function that depends solely on y
        polyProduct: function - A polynomial function that depends on x and y
    '''
    
    # Defines a polynomial function dependent only on x given n parameters
    def XLin(x, *args):
        # Initialize result to zero
        
        # Constrain to a widely availible floating point representation
        return np.poly1d(np.array(args))(x)

    # Defines a polynomial function dependent only on y given m parameters
    # Does the same thing that the XLin does
    def YLin(y, *args):
        return np.poly1d(np.array(args))(y)
    
    # Build signature for XLin
    xParam = [inspect.Parameter("x", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.float64)]
    xCoeffParams = [
        inspect.Parameter(f"x_{i}", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.float64)
        for i in range(0, n+1)
    ]
    XLin.__signature__ = inspect.Signature(xParam + xCoeffParams, return_annotation=np.float64)
    
    # Build signature for YLin
    yParam = [inspect.Parameter("y", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.float64)]
    yCoeffParams = [
        inspect.Parameter(f"y_{i}", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.float64)
        for i in range(0, m+1)
    ]
    YLin.__signature__ = inspect.Signature(yParam + yCoeffParams, return_annotation=np.float64)
    
    # Build signature for polyProduct
    mixedParam = [
        inspect.Parameter("point", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.ndarray),
        inspect.Parameter("xcoeffs", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=list),
        inspect.Parameter("ycoeffs", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=list),
    ]
    mixedParams = [
        inspect.Parameter(f"c_{i}", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.float64)
        for i in range(0, (n+1)*(m+1))
    ]
    
        # Join the parameters
    fullSuiteParams = mixedParam + mixedParams

    def polyProduct(point: np.ndarray, xcoeffs: list = None, ycoeffs: list = None, *coeffs,**kwargs):
        
        
        x=kwargs.get('x')
        y=kwargs.get('y')
        
        if (x is None) or (y is None):
            if((point is  None)):
                raise ValueError('Point is not defined')
            # Extract x and y from point array. Expecting last dimension size 2.
            if point.ndim == 3:
                x = point[:, :, 1]
                y = point[:, :, 0]
            else:
                x = point[:, 1]
                y = point[:, 0]
        # Evaluate the separable part
        xycoeffs = kwargs.get('xycoeffs',None)
        if xycoeffs is not None:
            coeffs = xycoeffs
            
        interpolated_func = XLin(x, *xcoeffs) * YLin(y, *ycoeffs)
        
        # Create Vandermonde matrices for x and y.
        # Note: Using np.vander on a 1d array.
        xs = np.vander(x, N=n+1,)  # shape: (len(x), n)
        ys = np.vander(y, N=m+1,)  # shape: (len(y), m)
        coeffs=np.array(coeffs)
        fixingTerms=np.zeros_like(interpolated_func)
        for i in range(xs.shape[0]):
            xz=xs[i]
            yz=ys[i]
            # print('xz,yz=',xz,yz)
            # Combine the two polynomial bases. A simple approach is to use outer product for each point.
            # We assume here that coeffs has length n*m. Adjust if needed.
            # print(xz.T.shape,yz.shape)
            fixingProduct = np.outer(xz,yz)
            # print(xz,yz)
            
            fixingProduct=fixingProduct.flatten()
            # print(fixingProduct)
            # print(fixingProduct.shape,coeffs.shape)
            fixingTerm = fixingProduct@coeffs
            # print(coeffs)
            # print(fixingTerm)
            fixingTerms[i]=fixingTerm
        # print('error=',interpolated_func-PolYproduct(x,y))
        # print(x,y)
        return interpolated_func + fixingTerms

    polyProduct.__signature__ = inspect.Signature(fullSuiteParams, return_annotation=np.float64)
    
    return XLin, YLin, polyProduct


def InterpolateGrid(Grid: np.ndarray, x0, y0, x1, y1,
                    dy: float = 1.0, dx: float = 1.0,
                    xmaxfev: int = None, ymaxfev: int = None, xymaxfev: int = None,
                    xtol: float = None, ytol: float = None, xytol: float = None,
                    savefunc:bool=True):
    (m, n) = Grid.shape
    if m < 1 or n < 1:
        raise ValueError('Cannot interpolate an empty grid')
    
    # Create the polynomial functions.
    # Note: here we use degrees n-1 for x and m-1 for y.
    XPolyNomial, YPolyNomial, XYPolyNomial = functionMaker(n - 1, m - 1)
    
    Xs = np.arange(x0, x1 + dx, dx)
    Ys = np.arange(y0, y1 + dy, dy)
    
    params = [xmaxfev, ymaxfev, xymaxfev]
    runtimes = [n, m, n * m]
    xmaxfev, ymaxfev, xymaxfev = [params[i] if params[i] is not None else 999 * runtimes[i] for i in range(3)]
    
    try:
        xOptimal, xCov = optimist.curve_fit(XPolyNomial, Xs, Grid[0, :], maxfev=xmaxfev)
        print('XCov=', xCov)
    except (RuntimeError,TypeError) as e:
        print("X curve_fit failed:", e)
        xOptimal = np.polyfit(Xs, Grid[0, :], n - 1)
    # xOptimal[np.abs(xOptimal)<1e-12]=0.0
    print('XOptimal=', xOptimal)
    
    
    try:
        yOptimal, yCov = optimist.curve_fit(YPolyNomial, Ys, Grid[:, 0].T, maxfev=ymaxfev)
        print('YCov=', yCov)
    except (RuntimeError,TypeError) as e:
        print("Y curve_fit failed:", e)
        yOptimal = np.polyfit(Ys, Grid[:, 0].T, m - 1)
    # yOptimal[np.abs(yOptimal)<1e-12]=0.0
    # yOptimal[-1]=1
    print('YOptimal=', yOptimal)
    
    
    
    
    YGrid, XGrid = np.meshgrid(Ys, Xs)
    points = np.stack((YGrid, XGrid), -1)  # shape: (num_points_y, num_points_x, 2)
    points = points.reshape(points.shape[0]*points.shape[1], 2)
    
    # Expected number of coefficients.
    # Here we assume XYPolyNomial uses (n+1)*(m+1) coefficients.
    # Adjust K as needed.
    K = (n) * (m)  # adjust to (n+1)*(m+1) if that is desired.
    
    def polyProd_fit_vector(points, *coeffs):
        preds = np.empty(points.shape[0])
        preds = XYPolyNomial(points, xOptimal, yOptimal, *coeffs)
        return preds
    
    # Create a wrapper that takes (points, c_0, c_1, ..., c_{K-1})
    def wrapper(points, *coeffs):
        if len(coeffs) != K:
            raise ValueError(f"Expected {K} coefficients, got {len(coeffs)}")
        return polyProd_fit_vector(points, *coeffs)
    
    # Now assign an explicit signature to the wrapper:
    # The signature will be: wrapper(points, c_0, c_1, ..., c_{K-1})
    params_list = [
        inspect.Parameter("points", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.ndarray)
    ]
    for i in range(K):
        params_list.append(
            inspect.Parameter(f"c_{i}", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.float64)
        )
    wrapper.__signature__ = inspect.Signature(params_list, return_annotation=np.float64)
    guess=np.full((m,n),np.spacing(0))
    if (xOptimal==0).all():
        guess[0,1:] = 1
    if (yOptimal==0).all():
        guess[1:,0] = 1
    print('guess=',guess)
    guess = guess.flatten()
    print('guess=',guess)
    # Now call curve_fit with our wrapper
    XYoptimal, XYcov = optimist.curve_fit(wrapper, points, Grid.flatten(), maxfev=xymaxfev,p0=guess,ftol=np.spacing(0.1),xtol=np.spacing(1))
    # XYoptimal[np.abs(XYoptimal)<1e-12]=0.0
    print('XYCov',XYcov)
    if savefunc:
        return xOptimal,yOptimal,XYoptimal,(XPolyNomial,YPolyNomial,XYPolyNomial)
    return xOptimal,yOptimal,XYoptimal




def InterpolateGrid_faster(Grid: np.ndarray, x0, y0, x1, y1,
                    dy: float = 1.0, dx: float = 1.0,
                    xmaxfev: int = None, ymaxfev: int = None, xymaxfev: int = None,
                    xtol: float = None, ytol: float = None, xytol: float = None,
                    savefunc:bool=True):
    (m, n) = Grid.shape
    if m < 1 or n < 1:
        raise ValueError('Cannot interpolate an empty grid')
    
    # Create the polynomial functions.
    # Note: here we use degrees n-1 for x and m-1 for y.
    XPolyNomial, YPolyNomial, XYPolyNomial = functionMaker(n - 1, m - 1)
    
    Xs = np.arange(x0, x1 + dx, dx)
    Ys = np.arange(y0, y1 + dy, dy)
    
    params = [xmaxfev, ymaxfev, xymaxfev]
    runtimes = [n, m, n * m]
    xmaxfev, ymaxfev, xymaxfev = [params[i] if params[i] is not None else 999 * runtimes[i] for i in range(3)]
    
    try:
        xOptimal, xCov = optimist.curve_fit(XPolyNomial, Xs, Grid[0, :], maxfev=xmaxfev)
        print('XCov=', xCov)
    except (RuntimeError,TypeError) as e:
        print("X curve_fit failed:", e)
        xOptimal = np.polyfit(Xs, Grid[0, :], n - 1)
    # xOptimal[np.abs(xOptimal)<1e-12]=0.0
    print('XOptimal=', xOptimal)
    
    
    try:
        yOptimal, yCov = optimist.curve_fit(YPolyNomial, Ys, Grid[:, 0].T, maxfev=ymaxfev)
        print('YCov=', yCov)
    except (RuntimeError,TypeError) as e:
        print("Y curve_fit failed:", e)
        yOptimal = np.polyfit(Ys, Grid[:, 0].T, m - 1)
    # yOptimal[np.abs(yOptimal)<1e-12]=0.0
    # yOptimal[-1]=1
    print('YOptimal=', yOptimal)
    
    
    
    
    YGrid, XGrid = np.meshgrid(Ys, Xs)
    points = np.stack((YGrid, XGrid), -1)  # shape: (num_points_y, num_points_x, 2)
    points = points.reshape(points.shape[0]*points.shape[1], 2)
    
    # Expected number of coefficients.
    # Here we assume XYPolyNomial uses (n+1)*(m+1) coefficients.
    # Adjust K as needed.
    K = (n) * (m)  # adjust to (n+1)*(m+1) if that is desired.
    
    
    guess=np.full((m,n),np.spacing(0))
    if (xOptimal==0).all():
        guess[0,1:] = 1
    if (yOptimal==0).all():
        guess[1:,0] = 1
    print('guess=',guess)
    guess = guess.flatten()
    print('guess=',guess)
    
    xOptimal[:]=0
    yOptimal[:]=0
    
    def polyProd_fit_vector(points, *coeffs):
        preds = np.empty(points.shape[0])
        preds = XYPolyNomial(points, xOptimal, yOptimal, *coeffs)
        return preds
    
    # Create a wrapper that takes (points, c_0, c_1, ..., c_{K-1})
    def wrapper(points, *coeffs):
        if len(coeffs) != K:
            raise ValueError(f"Expected {K} coefficients, got {len(coeffs)}")
        return polyProd_fit_vector(points, *coeffs)
    
    # Now assign an explicit signature to the wrapper:
    # The signature will be: wrapper(points, c_0, c_1, ..., c_{K-1})
    params_list = [
        inspect.Parameter("points", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.ndarray)
    ]
    for i in range(K):
        params_list.append(
            inspect.Parameter(f"c_{i}", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.float64)
        )
    wrapper.__signature__ = inspect.Signature(params_list, return_annotation=np.float64)
    
    # Now call curve_fit with our wrapper
    XYoptimal, XYcov = optimist.curve_fit(wrapper, points, Grid.flatten(), maxfev=xymaxfev,ftol=np.spacing(0.1),xtol=np.spacing(1))
    # XYoptimal[np.abs(XYoptimal)<1e-12]=0.0
    print('XYCov',XYcov)
    if savefunc:
        return xOptimal,yOptimal,XYoptimal,(XPolyNomial,YPolyNomial,XYPolyNomial)
    return xOptimal,yOptimal,XYoptimal

def InterpolateGrid_fastest(Grid: np.ndarray, x0, y0, x1, y1,
                    dy: float = 1.0, dx: float = 1.0,
                    xmaxfev: int = None, ymaxfev: int = None, xymaxfev: int = None,
                    xtol: float = None, ytol: float = None, xytol: float = None,
                    savefunc:bool=True):
    (m, n) = Grid.shape
    if m < 1 or n < 1:
        raise ValueError('Cannot interpolate an empty grid')
    
    # Create the polynomial functions.
    # Note: here we use degrees n-1 for x and m-1 for y.
    XPolyNomial, YPolyNomial, XYPolyNomial = functionMaker(n - 1, m - 1)
    
    Xs = np.arange(x0, x1 + dx, dx)
    Ys = np.arange(y0, y1 + dy, dy)
    
    params = [xmaxfev, ymaxfev, xymaxfev]
    runtimes = [n, m, n * m]
    xmaxfev, ymaxfev, xymaxfev = [params[i] if params[i] is not None else 999 * runtimes[i] for i in range(3)]
    
    
    
    
    YGrid, XGrid = np.meshgrid(Ys, Xs)
    points = np.stack((YGrid, XGrid), -1)  # shape: (num_points_y, num_points_x, 2)
    points = points.reshape(points.shape[0]*points.shape[1], 2)
    
    # Expected number of coefficients.
    # Here we assume XYPolyNomial uses (n+1)*(m+1) coefficients.
    # Adjust K as needed.
    K = (n) * (m)  # adjust to (n+1)*(m+1) if that is desired.
    guess=np.full((m,n),np.spacing(0))
    
    try:
        xOpti, xCov = optimist.curve_fit(XPolyNomial, Xs, Grid[0, :], maxfev=xmaxfev)
        
        if  np.logical_or(np.abs(xOpti-1)<1e-12, np.logical_not(np.isfinite(xOpti))).all():
            raise RuntimeError('Not a good looking polynomial')
        print('XCov=', xCov)
    except (RuntimeError,TypeError) as e:
        print("X curve_fit failed:", e)
        xOpti = np.polyfit(Xs, Grid[0, :], n - 1)
    print('XOpti=', xOpti)
    
    
    try:
        yOpti, yCov = optimist.curve_fit(YPolyNomial, Ys, Grid[:, 0].T, maxfev=ymaxfev)
        if  np.logical_or(np.abs(yOpti-1)<1e-12, np.logical_not(np.isfinite(yOpti))).all():
            raise RuntimeError('Not a good looking polynomial')
        
        print('YCov=', yCov)
    except (RuntimeError,TypeError) as e:
        print("Y curve_fit failed:", e)
        yOpti = np.polyfit(Ys, Grid[:, 0].T, m - 1)
    print('YOpti=', yOpti)
    # yOptimal[np.abs(yOptimal)<1e-12]=0.0
    
    guess[-1,:] = xOpti[:]
    guess[:,-1] = yOpti[:]
    
    xOptimal = np.zeros((n,),dtype=np.float64)
    yOptimal = np.zeros_like(xOptimal)
    
    
    
    def polyProd_fit_vector(points, *coeffs):
        preds = np.empty(points.shape[0])
        preds = XYPolyNomial(points, xOptimal, yOptimal, *coeffs)
        return preds
    
    # Create a wrapper that takes (points, c_0, c_1, ..., c_{K-1})
    def wrapper(points, *coeffs):
        if len(coeffs) != K:
            raise ValueError(f"Expected {K} coefficients, got {len(coeffs)}")
        return polyProd_fit_vector(points, *coeffs)
    
    # Now assign an explicit signature to the wrapper:
    # The signature will be: wrapper(points, c_0, c_1, ..., c_{K-1})
    params_list = [
        inspect.Parameter("points", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.ndarray)
    ]
    for i in range(K):
        params_list.append(
            inspect.Parameter(f"c_{i}", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.float64)
        )
    wrapper.__signature__ = inspect.Signature(params_list, return_annotation=np.float64)
    
    # Now call curve_fit with our wrapper
    XYoptimal, XYcov = optimist.curve_fit(wrapper, points, Grid.flatten(),p0=guess.flatten(), maxfev=xymaxfev)
    # XYoptimal[np.abs(XYoptimal)<1e-12]=0.0
    Unknown = 0.5#np.spacing(np.float64(2**(16)-1))*1e2
    XYOptimal=np.array(XYoptimal).reshape(m,n)
    print(np.min(np.abs(XYOptimal)))
    # input('...')
    XYOptimal[np.abs(XYOptimal)<Unknown]=0
    # can skip errors a certain amount when polynomial is small
    # TODO : Add variable rounding scheme to the solution
    XYOptimal=np.round(XYOptimal,1)
    c=1
    if 1==1:
        print('solvable')
        print('solving slowly')
        pivot = None
        for i in XYOptimal:
            if np.sum(np.abs(i)) !=0 :
                pivot = i
                break
        if pivot is not None:
            gcd:np.ndarray = None
            zeroless_pivot = pivot[np.abs(pivot)>Unknown]
            pass
            for i in range(zeroless_pivot.size-1):
                vals = zeroless_pivot[i:i+2]
                a=np.max(vals)
                b=np.min(vals)
                if a!=0 and b!=0:
                    x0,x1 = np.float64(np.abs(a/b)).as_integer_ratio() 
                    z0,z1 =  np.float64(np.abs(np.round(a/b))).as_integer_ratio() 
                    gcd_=np.round(a/z0,0)
                    if gcd is None:
                        gcd=gcd_
                    else:
                        if gcd_ > gcd:
                            gcd_=np.round(gcd_/gcd,0)
                            diff=np.abs(np.round(gcd_,0)-gcd_)
                            if not ((diff<np.abs(np.spacing(gcd_))) or (diff<np.spacing(np.round(gcd_,0)))):
                                gcd=1
                        elif gcd_<gcd:
                            gcd_=np.round(gcd/gcd_,0)
                            diff=np.abs(np.round(gcd_,0)-gcd_)
                            if ((diff<np.abs(np.spacing(gcd_))) or (diff<np.spacing(np.round(gcd_,0)))):
                                gcd=gcd_
            if gcd is not None:
                pivot=pivot/gcd
                c=gcd
                xOptimal[:]=pivot[:]
                for i in range(XYOptimal.shape[0]):
                    # TODO: SETUP RIGOROUS METHOD TO SOLVE FOR Computer errors
                    y_i=XYOptimal[i]/pivot
                    yOptimal[i] = np.round(np.mean(y_i,where=(np.isfinite(y_i))))
                    pass
                def polyProd_fit_vector(points, *coeffs):
                    preds = np.empty(points.shape[0])
                    preds = XYPolyNomial(points, xOptimal, yOptimal, *coeffs)
                    return preds
                
                # Create a wrapper that takes (points, c_0, c_1, ..., c_{K-1})
                def wrapper(points, *coeffs):
                    if len(coeffs) != K:
                        raise ValueError(f"Expected {K} coefficients, got {len(coeffs)}")
                    return polyProd_fit_vector(points, *coeffs)
                
                # Now assign an explicit signature to the wrapper:
                # The signature will be: wrapper(points, c_0, c_1, ..., c_{K-1})
                params_list = [
                    inspect.Parameter("points", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.ndarray)
                ]
                for i in range(K):
                    params_list.append(
                        inspect.Parameter(f"c_{i}", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=np.float64)
                    )
                wrapper.__signature__ = inspect.Signature(params_list, return_annotation=np.float64)
                guess[:,:]=np.spacing(0)
                ftol0=True
                if (xOptimal==0).all():
                    guess[0,1:] = 1
                    ftol0=False
                if (yOptimal==0).all():
                    guess[1:,0] = 1
                    ftol0=False
                print('guess=',guess)
                guess = guess.flatten()
                # Now call curve_fit with our wrapper
                XYoptimal, XYcov = optimist.curve_fit(wrapper, points, Grid.flatten(), maxfev=xymaxfev,p0=guess)
            else:
                print('gcd Inchoherent')
                      
    else:
        print('determinant',np.linalg.det(XYOptimal))
    print(XYOptimal)
    print('XYCov',XYcov)
    input('...')
    if savefunc:
        return c,xOptimal,yOptimal,XYoptimal,(XPolyNomial,YPolyNomial,XYPolyNomial)
    return xOptimal,yOptimal,XYoptimal
    
if __name__ == '__main__':
    def PolYproduct(x, y):
        # Example polynomial: 2x^2 + 2x + 3 (ignores y for demonstration)
        return (2 * (x**2) + 2 * (x) + 4.7+8*x**3+4*x**5)*(y**2+2)
    n_ = 10
    m_ = 10
    Ygrid, Xgrid = np.mgrid[:m_, :n_]
    print("Xgrid:\n", Xgrid, "\nYgrid:\n", Ygrid)
    input("Press Enter to continue...")
    
    grid = PolYproduct(Xgrid, Ygrid)
    print("Grid:\n", grid)
    input('Ready ?')
    
    c,xopt, yopt, xyopt,(XFunc,YFunc,XYFunc) = InterpolateGrid_fastest(grid, 0, 0, n_ - 1, m_ - 1,savefunc=True)
    
    points = np.stack((Ygrid, Xgrid), -1)  # shape: (num_points_y, num_points_x, 2)
    points = points.reshape(points.shape[0]*points.shape[1], 2)
    
    
    
    print("xopt:", xopt)
    print("yopt:", yopt)
    print("xyopt:", xyopt)
    input('...')
    err = grid-XYFunc(points,xopt,yopt,*xyopt).reshape(m_,n_)
    plt.imshow(err)
    plt.colorbar()
    plt.show(block=True)
    input('Done!')
   
