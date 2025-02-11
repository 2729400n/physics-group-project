import tkinter as tk
import tkinter.ttk as ttk
import tkinter.colorchooser
import matplotlib.backends.backend_tkagg as backend_tk
import matplotlib.figure as figures
import numpy as np


class FigureBase(tk.Frame):
    def  __init__(self,master,fig):
        super().__init__(fig,master)
        
        

root = tk.Tk()
fig=figures.Figure()
figBase=FigureBase(root,fig)

[[axes]]=fig.subplots(1,1,squeeze=False)
axes.plot(xs:=np.arange(0,10,0.1),np.sin(xs))
figBase.get_tk_widget().pack()
root.mainloop()
# root=tk.Tk()
# img=tk.PhotoImage('::tk::images::img',file='c:\\Users\\Kevnn\\GroupProject\\physics-group-project\\BoxInBox.png',master=root)
# xdownsize = int(img.width()//640)
# ydownsize = int(img.height()//480)
# img = img.subsample(xdownsize,ydownsize)
# lab=tk.Label(image=img,master=root,width=640,height=480)
# lab.pack()
# root.update()
# root.mainloop()
# print()