from tkinter import ttk
from Numerical_Methods.Boundaries.task2 import Task2
from Numerical_Methods.Boundaries.task1 import Task1

import matplotlib.figure,matplotlib.pyplot as plt
import tkinter as tk
root=tk.Tk()

varFloat=tk.DoubleVar(root)
varFloat.set('9.0')
def validateEntry(textafter,*args,**kwargs):
    
    print('Validate',textafter,args,kwargs)
    try:
        float(textafter)
    except:
        return False
    return True
def substitute(textafter,*args,**kwargs):
    print('Subst',args,kwargs)
    return ['0.0' if textafter.strip()=='' else textafter ]
entryVlidation = root.register(validateEntry,substitute)
inp=ttk.Entry(root,textvariable=varFloat,validate='all',validatecommand=(entryVlidation,'%P'))
print(varFloat.get())
inp.pack(anchor=tk.NW,expand=True,fill=tk.BOTH,padx=5,pady=5)
root.mainloop()
# with plt.ion():
#     fig=plt.figure(figsize=(10,10),clear=True)
#     axes=fig.add_subplot(111)


#     task1=Task1(axes)
#     task1.setup(200,200)
#     task1.run()
#     # task1._show_Efield()
    
#     plt.show(block=True)
    