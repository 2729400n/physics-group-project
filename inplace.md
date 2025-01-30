## The Real way to solve this problem

Being stuck on the original problems posed is no good for anyone dealing with a finite difference scheme we can instead of solving the next point outward in space solve for the current point.
Not fully Knowledgable abou this myself i had issues like it is mae of points that aren't correct yet. However with futher testing it surley converges over time as expected;

Step one:
    Identify the given problem.
    from the fact we have a an equlibruim pstate we an solve for the laplace solution using the electric potential as  the potential function.
$$ \nabla^{2}\phi = 0$$
We expand this os we can easilty turn ito into a F.D.S we will be using FTCS in a weird way
we know that $\frac{\partial\phi}{\partial t} = 0$ so we evolve the system over a sequence giving a close FTCS approach as the state reaches equilibruim. The trick will be revealed later so keep reading.
$$\cfrac{\partial^{2}\phi}{\partial x^{2}}+\cfrac{\partial^{2}\phi}{\partial y^{2}}+\cfrac{\partial^{2}\phi}{\partial z^{2}} + ... = 0 $$

We first rid ourselves of the higher dimesional terms as they are not necassary for what we are doing so *\*poof\** . |$\cfrac{\partial^{2}\phi}{\partial x^{2}}+\cfrac{\partial^{2}\phi}{\partial y^{2}} = 0$ | Gone like the wind that helps now we can solve this by using a cheap approxiamtion much like we do with accelaration. we get

$$ \cfrac{\phi_{i+1\text{, }j}-2 \phi_{i\text{, }j}+\phi_{i-1\text{, }j}}{\partial x^{2}}+ \cfrac{\phi_{i\text{, }j+1}-2\phi_{i\text{, }j}+\phi_{i\text{, }j-1}}{\partial y^{2}} = 0$$

$$ \cfrac{\phi_{i+1\text{, }j} + \phi_{i-1\text{, }j}}{\partial x^{2}} + \cfrac{\phi_{i\text{, }j+1} + \phi_{i\text{, }j-1}}{\partial y^{2}} = 4\cdot(\cfrac{\phi_{i\text{, }j}}{\partial x^{2}}+ \cfrac{\phi_{i\text{, }j}}{\partial y^{2}})$$

we can play the trick of $dx=dy$ now get

$$ \cfrac{\phi_{i+1\text{, }j} + \phi_{i-1\text{, }j}}{\partial x^{2}} + \cfrac{\phi_{i\text{, }j+1} + \phi_{i\text{, }j-1}}{\partial x^{2}} = 4 \cdot(\cfrac{\phi_{i\text{, }j}}{\partial x^{2}}+ \cfrac{\phi_{i\text{, }j}}{\partial x^{2}})$$
Simplifying time

$$ \cfrac{\phi_{i+1\text{, }j} + \phi_{i-1\text{, }j} +\phi_{i\text{, }j+1} + \phi_{i\text{, }j-1}}{4} = \phi_{i\text{, }j}$$

Now the trick we make the assumption that all imediate again pixels are correct (basically they dont change). If the nearby pixels don't change then we can move our current point through time to attain a more sutaible measurment. this means we move everything though time we denote this as a superscript after the variable e.g. There are constraint swe place mathematically they are $\phi^{n+\epsilon}_{i+k,j+l} =\phi^{n}_{i+k,j+l}$ for this we need epsilon to only equal one but this is  our assumption such that epsilon is in the set of integers.

### How do we stop

This is where you all get annoyed at me we stop when the going gets good when the precision needed is high when the mountain climbed is great. $\cfrac{🥺}{👉👈}$ you got me i just stop when the max absolute difference in the frames is less than 6 decimal placing in magnitude. I'm really sorry guys I wanted C compatibility. oh btw we say $dx=dy$ for this reason though its not neccassary.

### Step 3 : We Enforce the Rules we don't make em

Okay now for the part that gave me the most trouble circles and none rectilinear shapes.
We jeust make em rectilinear use a scheme that picks pointswe want ( gonna index an array with an boolean array *am I a genius or what*). This works thanks to numpy's array views structure which create a view of arrays when sliced not copies. we can assign values to th elements indexed this way and it reflects in the array.

### The circle

> ["ALL these squares make a circle"](https://youtu.be/Qe2FaWzlquM?t=444) ~ Mr.Popo Dragon Ball Z &nbsp;*\*Abriged\** &nbsp; Viewer discresion advised quite explicit content.

If you didn't watch the above video it partially explains my thoughts. 

> I can make a cirlce
> 
although as you may guess it can be done you see circles all the time.  

> Me: You don't see real circles.
> 
> You (wise guy): Okay I understand they ain't perfect circles I get their approxiamtion but they look good enough when I take a picture of round objects.
>
> Me: tell me one truly round object that is perfectly smooth, didn't think so. To elaborate no I cant not create a perfect edge smooting function without dabbling into statistics that to much and it would involve anti-aliasing point on the curve that should be split between nearest neighbours.
>
> You (wise guy): Well my computer had rounded corners
>
> Me: That's my plan.
>
> Us : 🤝 Profit

I hope that helps