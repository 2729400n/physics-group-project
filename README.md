# Errors

To whomever this may concern in the future you will see some files for interpolating functions in 2d this is kind of a strech

## Methodolgy

My methadology was if we have a function that has errors the errors will be a function of x and y for which we can solve using polynomial interpretationi applied some galois type thinking and thought hey we would be dealing with polynomial products.

This allows us to use either laplace interpolation  or if more inclined we could use spline interpolation 'plz cubic splines'

My idea we have an error function that aplplies in each direction given as

$X(x)$ in the $\hat x$ dirction and $Y(y)$ in the $\hat y$ direction we can then make the assumption it can be interpolated we have the error function

$\epsilon_{mutual}=X(x)Y(x)$

which is our polynomial then it becomes a problem of solving $n\cdot m$ unkowns in $n\cdot m$ equations.

My idea solve inthe respective domains then solve for each where we know a given value \(harder with non rectilinear geometries as we can no longer be sure of a given points value\)

We can solve for the polynomial coeffiecients