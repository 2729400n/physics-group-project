import tkinter as tk
import tkinter.filedialog
import turtle

import numpy as np




class ShapeDisplay(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setup()

    def setup(self):
        self.paint_canvas = tk.BooleanVar(self,False,name='paint_canvas')

        self.heatMap = tk.Canvas(self,)
        self.heatMap.bind('<ButtonPress-1>',self.begin_paint,add=True)
        self.heatMap.bind('<ButtonRelease-1>',self.end_paint,add=True)
        self.heatMap.pack()
        self.reload()
    
    def begin_paint(self,event,*args, **kwargs):
        if not self.getvar('paint_canvas'):
            self.paint_canvas.set(True)
            self.rectangles=[]
            self.tracer=self.heatMap.bind('<Motion>',self.canvas_mouse,add=True)
        self.pos0 = self.setvar(name='pos0',value=f'{event.x},{event.y}')
        
    def canvas_mouse(self,motion:tk.Event,*args,**kwargs):
        if self.getvar('paint_canvas'):
            pos0 = [int(i.strip()) for i in self.getvar('pos0').split(',')]
            # base = np.array((-.5*self.heatMap.canvwidth,-.5*self.heatMap.canvheight))
            self.heatMap.delete(*self.rectangles)
            self.rectangles+=[self.heatMap.create_rectangle(*pos0,motion.x,motion.y)]
            
            print(pos0[0],pos0[1],motion.x,motion.y)
            print(motion.x,motion.y)
        
    def end_paint(self,event,*args,**kwargs):
        if self.getvar('paint_canvas'):
            if(self.rectangles.__len__()>1):
                self.heatMap.delete(self.rectangles[:-1])
            self.paint_canvas.set(False)
            self.heatMap.unbind('<Motion>',self.tracer)
    def reload(self):
        self.update()
        self.pack()
    def reshape(self):
        self.reload()

class ControlPanel(tk.Frame):
    def __init__(self):
        super().__init__()
    def init_controls(self):
        self.shape=tk.Radiobutton(
            self,command="Shape"
        )
class scene_SetFieldPage(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(args,kwargs)
    def setup(self):
        self.controlPanel= ControlPanel(self,)
        self.fieldPanel=ShapeDisplay(self)
    pass

if __name__ == '__main__':
    shaper = ShapeDisplay()
    tk.mainloop()