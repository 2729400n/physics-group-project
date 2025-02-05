# Methodology

## Analytical

## Numerical

When creating a numerical solver there a few things to consider. Does your problem converge is it continous or is it inately discrete. Is it possible to keep coupled points together when solving. Is there an easier less complex solution.

The pragmatic choice was using a finite difference scheme and solving by relaxation. To solve by relaxation you allow the system to evolve through some metric and compute the absolute difference between states only stopping when that difference is lower than a certain threshold. The stability of this method is affected by how quickly we propogate changes and how low we have our thershold.

### Fast Propogation and instability

If changes are propogated to quic=kly it can degrade the stability of theg iven scheme

### Picking a good threshold

To pick a good thershold you would look through operations and spot key operation thatmay break for very small differences

Our Problem is  given as:

$$\begin{aligned}
\nabla^{2}\phi = 0\\
\cfrac{\partial^{2}\phi}{\partial x^{2}}+\cfrac{\partial^{2}\phi}{\partial y^{2}}+\cfrac{\partial^{2}\phi}{\partial z^{2}} + ... = 0
\end{aligned}$$
this problem has explicit dependence on the difference in x, y and z. we
