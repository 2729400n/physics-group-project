The current Numerical Solver Branch I will try to speed it up a little

` possibly contains a rm -rf /` bug
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

if we add som elee way for the errors in thi swe get a nice function al=s long a we linearize it

We can solve for the polynomial coeffiecients

We can solve for the polynomial coeffiecients



## Possible Idea

Issue polynomial interpolation currenltly does not work what do we need 
need a way to form good polynomial curve fit does not depend on the x parameter given we can make a grid then solve the grid for different as the xs a bit like

new_xs = np.array([x,y for i in X,y])  will be a flat array containing x,y as psuedo scalars thenpassing it as an x parameter to curve fit we 
can interpolate for polynomial shifts
# physics-group-project
The Repo for Physics Group Project


# Prequisites 
To  join the guthu repo first you will need some form of authentication.

First open settings:
![Settings](settings.png)

Then settt security keys using \(ssh-keygen  preferable\)

## Aim

To solve the Maxwells equations as a differential form.

### Task 1
Solve analytically for the given differential form


### Task 2

