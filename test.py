import inspect
import numpy as np
import scipy.optimize as optimist
import numpy.linalg as linalg




def functionMaker(n: int, m: int, dx: int = 1, dy: int = 1):
    def XLin(x, *args):
        result = 0
        for i in range(1, n + dx, dx):
            result += args[-i] * (x ** (i))
        return np.float64(result)

    def YLin(y, *args):
        result = 0
        for i in range(1, m + dy, dy):
            result += args[-i] * (y ** (i))
        return np.float64(result)

    
    
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
    
    
    def polyProduct(x, y, xcoeffs:'list[float]'=None, ycoeffs:'list[float]'=None,*coeffs):
        coeff_len = len(coeffs)
        return XLin(x, *xcoeffs) * YLin(y, ycoeffs) + sum([i for i in range(coeff_len)])
    
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
    return XLin, YLin, polyProduct


def InterpolateGrid(Grid:'np.ndarray'):
    (n,m) = Grid.shape
    