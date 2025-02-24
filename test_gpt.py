import inspect
import numpy as np
import scipy.optimize as optimist
import numpy.linalg as linalg

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
        result = 0
        # Evaluate polynomial: assume args has length n+1 (coefficient for x^n ... x^0)
        for i in range(0, n + 1, dx):
            result += args[i] * (x ** (n - i))
        return np.float64(result)

    # Defines a polynomial function dependent only on y given m parameters
    def YLin(y, *args):
        result = 0
        for i in range(0, m + 1, dy):
            result += args[i] * (y ** (m - i))
        return np.float64(result)
    
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
    fullSuiteParams = mixedParam + mixedParams

    def polyProduct(point: np.ndarray, xcoeffs: list = None, ycoeffs: list = None, *coeffs):
        # Extract x and y from point array. Expecting last dimension size 2.
        if point.ndim == 3:
            x = point[:, :, 1]
            y = point[:, :, 0]
        else:
            x = point[:, 1]
            y = point[:, 0]
        # Evaluate the separable part
        interpolated_func = XLin(x, *xcoeffs) * YLin(y, *ycoeffs)
        
        # Create Vandermonde matrices for x and y.
        # Note: Using np.vander on a 1d array.
        xs = np.vander(x, N=n, increasing=False)  # shape: (len(x), n)
        ys = np.vander(y, N=m, increasing=False)  # shape: (len(y), m)
        # Combine the two polynomial bases. A simple approach is to use outer product for each point.
        # We assume here that coeffs has length n*m. Adjust if needed.
        fixingProduct = np.array([
            np.outer(xs[i], ys[i]).flatten() for i in range(len(x))
        ])  # shape: (len(x), n*m)
        
        # If coeffs is not a numpy array, convert it.
        coeffs = np.array(coeffs)
        # If lengths differ, you might need to adjust dimensions.
        fixingTerm = fixingProduct.dot(coeffs)
        
        return interpolated_func + fixingTerm

    polyProduct.__signature__ = inspect.Signature(fullSuiteParams, return_annotation=np.float64)
    
    return XLin, YLin, polyProduct


# A default ready-made but slow fitting function 
def InterpolateGrid(Grid: np.ndarray, x0: np.ndarray, y0: np.ndarray, x1: np.ndarray, y1: np.ndarray,
                    dy: float = 1.0, dx: float = 1.0,
                    xmaxfev: int = None, ymaxfev: int = None, xymaxfev: int = None,
                    xtol: float = None, ytol: float = None, xytol: float = None):
    (m, n) = Grid.shape
    if m < 1 or n < 1:
        raise ValueError('Cannot interpolate an empty grid')
    
    # Create polynomial functions. Here degree = number of coefficients - 1.
    XPolyNomial, YPolyNomial, XYPolyNomial = functionMaker(n - 1, m - 1)
    
    Xs = np.arange(x0, x1 + dx, dx)
    Ys = np.arange(y0, y1 + dy, dy)
    
    # Determine maximum function evaluations
    params = [xmaxfev, ymaxfev, xymaxfev]
    runtimes = [n, m, n * m]
    xmaxfev, ymaxfev, xymaxfev = [params[i] if params[i] is not None else 999 * runtimes[i] for i in range(3)]
    
    try:
        # Fit X polynomial along the first row
        xOptimal, xCov = optimist.curve_fit(XPolyNomial, Xs, Grid[0, :], maxfev=xmaxfev)
    except RuntimeError as e:
        print("X curve_fit failed:", e)
        xOptimal = np.polyfit(Xs, Grid[0, :], n - 1)
    print('XOptimal=', xOptimal)
    
    try:
        # Fit Y polynomial along the first column
        yOptimal, yCov = optimist.curve_fit(YPolyNomial, Ys, Grid[:, 0].T, maxfev=ymaxfev)
    except RuntimeError as e:
        print("Y curve_fit failed:", e)
        yOptimal = np.polyfit(Ys, Grid[:, 0].T, m - 1)
    print('YOptimal=', yOptimal)
    
    # Prepare grid points for the mixed polynomial fit
    YGrid, XGrid = np.meshgrid(Ys, Xs)
    points = np.stack((YGrid, XGrid), -1)  # Each point is (y, x)
    points = points.reshape(points.shape[0] * points.shape[1], 2)
    
    def __innerProduct():
        nonlocal xOptimal, yOptimal
        def ___innerProduct(point, *args):
            return XYPolyNomial(point, xOptimal, yOptimal, *args)
        # Use vectorize without trying to modify the signature further.
        _innerProduct = np.vectorize(___innerProduct)
        return _innerProduct

    polyProd = __innerProduct()
    
    # Fit the mixed polynomial using curve_fit.
    # p0 can be omitted if you do not have an initial guess.
    XYoptimal, XYcov = optimist.curve_fit(polyProd, points, Grid.flatten(), maxfev=xymaxfev)
    
    return xOptimal, yOptimal, XYoptimal

    
if __name__ == '__main__':
    def PolYproduct(x, y):
        # Example polynomial: 2x^2 + 2x + 3 (ignores y for demonstration)
        return (2 * (x**2) + 2 * (x) + 3)
    n_ = 10
    m_ = 10
    Ygrid, Xgrid = np.mgrid[:m_, :n_]
    print("Xgrid:\n", Xgrid, "\nYgrid:\n", Ygrid)
    input("Press Enter to continue...")
    
    grid = PolYproduct(Xgrid, Ygrid)
    print("Grid:\n", grid)
    input('Ready ?')
    
    xopt, yopt, xyopt = InterpolateGrid(grid, 0, 0, n_ - 1, m_ - 1)
    print("xopt:", xopt)
    print("yopt:", yopt)
    print("xyopt:", xyopt)
    input('Done!')
