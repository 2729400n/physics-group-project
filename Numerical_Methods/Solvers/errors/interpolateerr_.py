import numpy as np
import scipy.optimize as optimist
import inspect
from matplotlib import pyplot as plt
import numpy.linalg as linalg
import numbers,math

def functionMaker(n: int, m: int):
    def polyProduct(point: np.ndarray = None, **kwargs):
        if point is not None:
            if point.shape[-1] != 2:
                raise ValueError("point must have shape (..., 2)")
            x, y = point[..., 0], point[..., 1]
        else:
            x, y = kwargs.get('x'), kwargs.get('y')
            if x is None or y is None:
                raise ValueError("x and y must be provided if point is None")

        xz, yz = np.vander(x, n, increasing=True), np.vander(y, m, increasing=True)
        return np.einsum('ij,ik->ijk', xz, yz).reshape(x.shape + (-1,))
    
    return polyProduct

def interpolate_2d(grid: np.ndarray, n: int, m: int):
    poly_func = functionMaker(n, m)
    x_vals, y_vals = np.meshgrid(np.arange(grid.shape[1]), np.arange(grid.shape[0]))
    points = np.stack([x_vals.ravel(), y_vals.ravel()], axis=-1)
    values = grid.ravel()
    
    def poly_model(point, *coeffs):
        basis = poly_func(point)
        return basis @ np.array(coeffs)
    
    guess = np.ones(n * m) * 0.01
    coeffs, _ = optimist.curve_fit(poly_model, points, values, p0=guess)
    
    condition_number = np.linalg.cond(poly_func(points).reshape(len(points), -1))
    print(f"Condition number: {condition_number:.2e}")
    
    interpolated_grid = poly_model(points, *coeffs).reshape(grid.shape)
    error = np.abs(grid - interpolated_grid)
    rmse = np.sqrt(np.mean(error**2))
    print(f"Interpolation RMSE: {rmse:.4e}")
    
    return interpolated_grid, coeffs,error

# Example Usage

def PolYproduct(x, y):
    # Example polynomial: 2x^2 + 2x + 3 (ignores y for demonstration)
    return  (8.5*x**1 )*(2)
n_ = 100
m_ = 100
Ygrid, Xgrid = np.mgrid[:m_, :n_]
print("Xgrid:\n", Xgrid, "\nYgrid:\n", Ygrid)
input("Press Enter to continue...")

grid = PolYproduct(Xgrid, Ygrid)
print("Grid:\n", grid)
input('Ready ?')
interpolated, coeffs,err = interpolate_2d(grid, 3,3)


print('interpolated',interpolated)
print()
print('coeefs',coeffs)
print(coeffs.shape)
print()

plt.imshow(err)
plt.colorbar()
plt.show(block=True)

