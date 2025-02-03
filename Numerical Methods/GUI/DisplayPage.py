import tkinter as tk
import tkinter.filedialog
import turtle


class ShapeDisplay(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setup()
    def setup(self):
        self.paint_canvas = tk.BooleanVar(self,False,name='paint_canvas')

        self.heatMap = turtle.ScrolledCanvas(self,)
        self.heatMap.bind('<ButtonPress-1>',self.begin_paint,add=True)
        self.heatMap.bind('<ButtonRelease-1>',self.end_paint,add=True)
        self.heatMap.pack()
        self.reload()
    
    def begin_paint(self,event,*args, **kwargs):
        if not self.getvar('paint_canvas'):
            self.paint_canvas.set(True)
            self.tracer=self.heatMap.bind('<Motion>',self.canvas_mouse,add=True)
        self.pos0 = self.setvar(name='pos0',value=f'{event.x},{event.y}')
    def canvas_mouse(self,motion:tk.Event,*args,**kwargs):
        if self.getvar('paint_canvas'):
            pos0 = [int(i.strip()) for i in self.getvar('pos0').split(',')]
            self.heatMap.create_rectangle(-1.0,-1.0,motion.x/self.heatMap.canvwidth,motion.y/self.heatMap.canvheight,fill='green')
            print(pos0[0],pos0[1],motion.x,motion.y)
            print(motion.x,motion.y)
        
    def end_paint(self,event,*args,**kwargs):
        if self.getvar('paint_canvas'):
            self.paint_canvas.set(False)
            self.heatMap.unbind('<Motion>',self.tracer)
    def reload(self):
        self.update()
        self.pack()
    def reshape(self):
        self.reload()

shaper = ShapeDisplay()
tk.mainloop()