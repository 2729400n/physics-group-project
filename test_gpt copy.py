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
        for i in range(0, n + dx, dx):
            result += args[i] * (x ** (n - i))
        # Constrain to a widely availible floating point representation
        return np.float64(result)

    # Defines a polynomial function dependent only on y given m parameters
    # Does the same thing that the XLin does
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
    
        # Join the parameters
    fullSuiteParams = mixedParam + mixedParams

    def polyProduct(point: np.ndarray, xcoeffs: list = None, ycoeffs: list = None, *coeffs):
        # Extract x and y from point array. Expecting last dimension size 2.
        if point.ndim == 3:
            x = point[:, :, 1]
            y = point[:, :, 0]
        elif point.ndim == 2:
            x = point[:, 1]
            y = point[:, 0]
        elif point.ndim==1:
            x = point[:, 1]
            y = point[:, 0]
        
        # Evaluate the separable part
        
        interpolated_func = XLin(x, *xcoeffs) * YLin(y, *ycoeffs)
        
        # Create Vandermonde matrices for x and y.
        # Note: Using np.vander on a 1d array.
        xs = np.vander(x, N=n+1, increasing=False)  # shape: (len(x), n)
        ys = np.vander(y, N=m+1, increasing=False)  # shape: (len(y), m)
        # print(x,y)
        # print(xs,xs.shape)
        # print(ys,ys.shape)
        # input('...')
        coeffs=np.array(coeffs)
        # Combine the two polynomial bases. A simple approach is to use outer product for each point.
        # We assume here that coeffs has length n*m. Adjust if needed.
        fixingProduct = (xs.T@ys)
        # print(f'VanderMonde Product = {fixingProduct}')
        # # If lengths differ, you might need to adjust dimensions.
        # input('...')
        # print(fixingProduct)
        # print(fixingProduct.shape)
        # input('...')
        fixingTerm = fixingProduct.flatten()*coeffs
        
        return interpolated_func + fixingTerm

    polyProduct.__signature__ = inspect.Signature(fullSuiteParams, return_annotation=np.float64)
    
    return XLin, YLin, polyProduct


def InterpolateGrid(Grid: np.ndarray, x0, y0, x1, y1,
                    dy: float = 1.0, dx: float = 1.0,
                    xmaxfev: int = None, ymaxfev: int = None, xymaxfev: int = None,
                    xtol: float = None, ytol: float = None, xytol: float = None):
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
    except RuntimeError as e:
        print("X curve_fit failed:", e)
        xOptimal = np.polyfit(Xs, Grid[0, :], n - 1)
    print('XOptimal=', xOptimal)
    print('XCov=', xCov)
    
    try:
        yOptimal, yCov = optimist.curve_fit(YPolyNomial, Ys, Grid[:, 0].T, maxfev=ymaxfev)
    except RuntimeError as e:
        print("Y curve_fit failed:", e)
        yOptimal = np.polyfit(Ys, Grid[:, 0].T, m - 1)
    print('YOptimal=', yOptimal)
    print('YCov=', yCov)
    
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
    
    # Now call curve_fit with our wrapper
    XYoptimal, XYcov = optimist.curve_fit(wrapper, points, Grid.flatten(), maxfev=xymaxfev)
    
    return xOptimal, yOptimal, XYoptimal



    
if __name__ == '__main__':
    def PolYproduct(x, y):
        # Example polynomial: 2x^2 + 2x + 3 (ignores y for demonstration)
        return (2 * (x**2) + 2 * (x) + 3)
    n_ = 4
    m_ = 4
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
