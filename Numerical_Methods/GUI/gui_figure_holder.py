import tkinter as tk
import tkinter.ttk as ttk
import tkinter.colorchooser



class FigureBase(tk.Widget):
    def  __init__(self):
        tk.PhotoImage('::tk::images::img',file=r'c:\Users\Kevnn\GroupProject\physics-group-project\BoxInBox.png')
        
root=tk.Tk()
img=tk.PhotoImage('::tk::images::img',file='c:\\Users\\Kevnn\\GroupProject\\physics-group-project\\BoxInBox.png',master=root,width=640,height=480)
lab=tk.Label(image=img,master=root,)
lab.pack()
root.update()
root.mainloop()
print()