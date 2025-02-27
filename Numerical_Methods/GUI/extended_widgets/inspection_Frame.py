from tkinter import Canvas,Text,Event,EventType
from tkinter.ttk import Frame,Button
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import (
    _Backend, FigureCanvasBase, FigureManagerBase, NavigationToolbar2,
    TimerBase, ToolContainerBase, cursors, _Mode, MouseButton,
    CloseEvent, KeyEvent, LocationEvent, MouseEvent, ResizeEvent)
import tkinter as tk
from ...Solvers import errors

import numpy as np


# for semmantic porpuses
class EventFullNavigationToolbar2Tk(NavigationToolbar2Tk):
    def zoom(self, *args):
        print('zoom', args)
        self.master.event_generate("<<Zoom-Clicked>>")
        return super().zoom(*args)
    def drag_zoom(self, evt:MouseEvent,*args):
        print('drag_zoom', evt,args)
        self.master.event_generate("<<Zoom-Drag>>")
        
        return super().drag_zoom(evt,*args)
    def press_zoom(self, *args):
        print('press_zoom', args)
        # self.master.event_generate("<<Zoom>>")
        return super().press_zoom(*args)
    def release_zoom(self, *args):
        print('release_zoom', args[0])
        # self.master.event_generate("<<Zoom>>")
        return super().release_zoom(*args)
    
    def mouse_move(self, event):
        print('mouse_move', event)
        return super().mouse_move(event)
    def mouse_press(self, event):
        print('mouse_press', event)
        return super().mouse_press(event)
    def mouse_release(self, event):
        print('release_mouse', event)
        return super().mouse_release(event)    
    
    def pan(self, *args):
        print('pan', args)
        # self.master.event_generate("<<Pan>>")
        return super().pan(*args)
    def drag_pan(self, event):
        print('drag_zoom', event)
        return super().drag_pan(event)
    def press_pan(self, *args):
        print('press_pan', args)
        # self.master.event_generate("<<Pan>>")
        return super().press_pan(*args)
    def release_pan(self, *args):
        print('release_pan', args)
        # self.master.event_generate("<<Pan>>")
        return super().release_pan(*args)
    


    

class InspectFrame(Frame):
    
    def __init__(self,parent,Grid_obj,dx:float,dy:float,*args,**frame_kwargs):
        super().__init__(master=parent,**frame_kwargs)
        fig=self.fig = Figure(figsize=(8, 8),)
        ax=self.ax = fig.add_subplot(111)
        self.Grid_obj = np.array(Grid_obj,copy=True)
        self.dx = dx
        self.dy = dy
        mainframe=self.mainframe = Frame(self)
        plot_frame=self.plot_frame = Frame(mainframe)
        button_frame = self.button_frame = Frame(mainframe)
        
        self.propagate(True)
        mainframe.propagate(True)
        plot_frame.propagate(True)
        button_frame.propagate(True)
        
        plot_frame.columnconfigure(0,weight=1)
        plot_frame.rowconfigure(0,weight=1)
        plot_frame.columnconfigure(0,weight=1)
        plot_frame.rowconfigure(1,weight=1)
        # Plot data
        mainframe.columnconfigure(0,weight=1)
        mainframe.rowconfigure(0,weight=1)
        mainframe.columnconfigure(0,weight=1)
        mainframe.rowconfigure(1,weight=1)
        # Embed figure into Tkinter canvas
        canvas = self.canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas_widget = self.canvas = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew")
        canvas_widget.configure(width=640,height=480)
        canvas.draw()
        # Add Navigation Toolbar
        toolbar = self.toolbar = EventFullNavigationToolbar2Tk(canvas, plot_frame,pack_toolbar=False)
        
        toolbar.update()
        toolbar.grid(row=1, column=0, sticky="ew")
        
        
        
        
        
        plot_frame.grid(column=1,row=0)
        button_frame.grid(column=0,row=0)
        
        mainframe.pack(anchor=tk.NW,side=tk.TOP,fill=tk.BOTH,expand=True)
        
        
        
        ax.set_title("The Laplacian Absolute Error")
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        # self.ax.legend()
        
        resi,absresi=errors.laplaceify(self.Grid_obj,self.dx,self.dy)
        ax.imshow(Grid_obj)
    
    def select_Smallgrid(self,evt):
        pass
    
    def calculatePolyNomial(self, event:Event):
        pass
        


if __name__ == '__main__':
    
    grid = np.full((10,10), fill_value=1)
    grid[(0,-1),:] = grid[:,(0,-1)]  = 9
    newErrorWindow =tk.Tk()
    iframe=InspectFrame(newErrorWindow,grid,1,1)
    iframe.pack()
    newErrorWindow.mainloop()