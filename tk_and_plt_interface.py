import matplotlib as mplib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tk_agg
from matplotlib.figure import  Figure
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.constants as tk_const
import matplotlib.backend_bases as mplib_bbases
import matplotlib.backend_managers as mplib_bmngrs
import matplotlib.backend_tools as mplib_btools

class SomeClass(ttk.Frame):
    def __init__(self,master=None,*args,**kwargs):
        super().__init__(master=master,*args,**kwargs)
        self.canvas = tk.Canvas(self,)
        canvas =self.canvas_ex=tk_agg.FigureCanvasTkAgg(master=self)
        fig_man=self.fig_man=tk_agg.FigureManagerTk(self.canvas,0,self.master)
        
        # plt.switch_backend('tkagg')
        