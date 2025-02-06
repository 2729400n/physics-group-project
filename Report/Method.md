# Methodology

## Analytical

## Numerical

When creating a numerical solver there a few things to consider. Does your problem converge is it continous or is it inately discrete. Are there any coupled values to consider. Is there a less complex solution.

The pragmatic choice was using a finite difference scheme and solving by relaxation. To solve by relaxation you allow the system to evolve through some metric and compute the absolute difference between states only stopping when that difference is lower than a certain threshold. The stability of this method is affected by how quickly we propogate changes and how low we have our threshold.

### Fast Propogation and instability

If changes are propogated too quickly it can degrade the stability of the given scheme.

### Picking a good threshold

To pick a good thershold you would look through and spot key operation that may break for very small differences. When working with a finite difference scheme the two biggest obstacles are "subtraction" and "division".

Our Problem is  given as:

$$\begin{gather}
\nabla^{2}\phi = 0\\
\cfrac{\partial^{2}\phi}{\partial x^{2}}+\cfrac{\partial^{2}\phi}{\partial y^{2}}+\cfrac{\partial^{2}\phi}{\partial z^{2}} + ... = 0
\end{gather}$$
this problem has explicit dependence on the difference in x, y and z. we

### Generating Continous Geometries

Generating continous geometries that exist in $\mathbb{R}$ is a difficult task look no further than the rounded corners on GUI or even the "O" o "0" characters on computerized text displays. It is notoriusly hard and would be out of the scope of this project to establish a new solution. To solve for none rectilinear shapes I decided to base my algorithm on well established algorithms such as the Bresmahn Algorith for curves

### Enforcing boundary conditions


Okay now for the part that gave me the most trouble circles and none rectilinear shapes.
We jeust make em rectilinear use a scheme that picks pointswe want ( gonna index an array with an boolean array *am I a genius or what*). This works thanks to numpy's array views structure which create a view of arrays when sliced not copies. we can assign values to th elements indexed this way and it reflects in the array.


### Enabiling accessability

Not every one can use a cli and as such it seemed paramount that we develop a UI that is most accesible while leaving the cli interface intact and also allowing for systems that may onlyhave the bare metal python implementation or no definitive gui. To this extent we went with a CLI, GUI, and webserver interface.