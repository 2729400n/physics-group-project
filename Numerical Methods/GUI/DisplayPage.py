import tkinter as tk
import tkinter.filedialog
import turtle


class ShapeDisplay(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setup()
    def setup(self):
        self.heatMap = turtle.ScrolledCanvas(self,)
        self.heatMap.bind('<Motion>',self.canvas_mouse,add=True)
        self.heatMap.pack()
        self.reload()
    def canvas_mouse(self,*args,**kwargs):
        print(args,kwargs)
    def reload(self):
        self.update()
        self.pack()
    def reshape(self):
        self.reload()

shaper = ShapeDisplay()
tk.mainloop()