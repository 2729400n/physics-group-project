import inspect
import numpy as np


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

    def polyProduct(x, y, xcoeffs=None, ycoeffs=None):
        return XLin(x, *xcoeffs) * YLin(y, ycoeffs)

    XLin.__signature__ = inspect.Signature(
        [
            inspect.Parameter(
                f"a{i}",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            )
            for i in range(0, n, 1)
        ],
        return_annotation=np.float64,
        __validate_parameters__=True,
    )
    YLin.__signature__ = inspect.Signature(
        [
            inspect.Parameter(
                f"a{i}",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            )
            for i in range(0, n, 1)
        ],
        return_annotation=np.float64,
        __validate_parameters__=True,
    )
    polyProduct.__signature__ = inspect.Signature(
        [
            inspect.Parameter(
                f"a{i}",
                inspect._ParameterKind.POSITIONAL_OR_KEYWORD,
                default=0,
                annotation=np.float64,
            )
            for i in range(0, n, 1)
        ],
        return_annotation=np.float64,
        __validate_parameters__=True,
    )
    return XLin, YLin, polyProduct
