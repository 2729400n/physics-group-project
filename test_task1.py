from Numerical_Methods.Boundaries.task2 import Task2
from Numerical_Methods.Boundaries.task1 import Task1

import matplotlib.figure,matplotlib.pyplot as plt

with plt.ion():
    fig=plt.figure(figsize=(10,10),clear=True)
    axes=fig.add_subplot(111)


    task1=Task1(axes)
    task1.setup(200,200)
    task1.run()
    # task1._show_Efield()
    
    plt.show(block=True)
    