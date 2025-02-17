import tkinter as tk
from tkinter import ttk
import tkinter.commondialog as tkcommon
import os, os.path as pth
import sys, matplotlib.colors as mcolors, matplotlib as mplib , matplotlib.pyplot as plt, matplotlib.colorbar as mcolorbars, matplotlib.cm as cm

import matplotlib.backend_tools as mb_tools, matplotlib.backend_managers as mb_managers, matplotlib.backends.backend_tkagg as mb_tkagg
import matplotlib.figure
from ..extended_widgets.realtime_update_figure import RealTimeFigure

import numpy as np

__base__ = pth.abspath(pth.dirname(__file__))

def loadCMap(file=None):
    print('Loading',file)
    cmaps = dict()
    if not os.getenv('NM_NO_DEF_CMAPS',False):
        print('Using Default ColorMaps')
        for key in mplib.colormaps:
            cmaps[key] = mplib.colormaps.get_cmap(key)
    
    if file is not None:
        with open(file,'rb') as file:
            cmap = np.load(file,allow_pickle=True)
            for key in cmap.files:
                cmaps[key] = mcolors.ListedColormap(colors=cmap[key],name=key,N=cmap[key].shape[0])
        
    

    return cmaps


class CMapper(tk.Frame):
    name='ColourMaps'
    def __init__(self, master=None,*args,**kwargs):
        self._color_map_path = kwargs.get('dir',None)
        if self._color_map_path is None:
            self._color_map_path = os.getenv('NM_CMAP_DIR',None)
            if self._color_map_path is None:
                self._color_map_path = pth.abspath(pth.join(__base__,'../','../','./utils/res/default_cmaps'))
        self.ftype = None
        self.loc = None
        self.cmap=None
        tk.Frame.__init__(self, master)
        # self.pack()
        # tk.Wm.geometry(self.winfo_toplevel(),'640x480')
        # self.config(height=480,width=640)
        self.createWidgets()
        self.pack(anchor=tk.NW,fill=tk.BOTH,expand=True)
        
        self.update()
        

    def getAvailableCMaps(self):
        print('Available CMaps:')
        print('\tLoading Available CMaps')
        if(pth.isdir(self._color_map_path)):
            self.ftype = 'dir'
            self.loc = self._color_map_path
            files= os.listdir(self.loc)
            files = [loadCMap(pth.abspath(pth.join(self.loc,i))) for i in files]
            self.file = dict()
            for i in files:
                self.file.update(**i)
            return [*self.file.keys()]
        elif(pth.isfile(self._color_map_path)):
            self.ftype = 'file_single'
            self.loc = self._color_map_path
            self.file = loadCMap(self.loc)
            return 
        else:
            self.ftype = 'default_only'
            self.loc=None
            self.file = loadCMap(self.loc)
        keys = [*self.file.keys()]
        if len(keys) == 0 :
            print('\tNo Available CMaps')
        return keys
    def createWidgets(self):
        L1 = tk.Label(self, text='Color Map',justify='center')
        labelframe = tk.LabelFrame(self)
        cmaps=self.cmaps=tk.Listbox(labelframe, selectmode=tk.SINGLE)
        cmapsList=self.getAvailableCMaps()
        cmaps.insert(0,*cmapsList)
        cmaps.grid(row=1,sticky='NW')
        cmaps.bind('<<ListboxSelect>>',self.selected_cmap,add='+')
        cmaps.bind('<KeyPress-Up>',self.handle_keys,'+')
        cmaps.bind('<KeyPress-Down>',self.handle_keys,'+')
        self.cmaps.selection_handle(self.selected_cmap)
        self.current_sel = cmaps.get(0,0)
        self.key = None
        L1.grid(row=0,sticky='NE',column=0,columnspan=1,)
        L1.grid_propagate(True)
        L1.grid_columnconfigure(0,weight=1)
        button = tk.Button(labelframe, text='Select Color Map', command=self.submit)
        button.grid(row=2,sticky='NW')
        button.grid_propagate(True)
        button.grid_columnconfigure(0)
        labelframe.grid(row=1,sticky='NW',padx=5)
        
        self.example_heatmap = matplotlib.figure.Figure(figsize=(3,3),dpi=64,tight_layout=True)
        self.test_axes = None
        self.example_display = mb_tkagg.FigureCanvasTkAgg(self.example_heatmap,master=self)
        self.example_canvas=self.example_display.get_tk_widget()
        self.example_canvas.grid(row=1,column=1,sticky='NE',padx=5,pady=5)
        self.example_display.draw()
        
        self.test_grid, _ = np.mgrid[:1024,:100]
        
        
        

    def selected_cmap(self,*args):
        index:tuple = self.cmaps.curselection()
        
        if(index.__len__()==0):
            return
        
        key =self.cmaps.get(index[0])
        if self.key!=key:
            self.example_display.blit()
            if self.test_axes is None:
                self.test_axes = self.example_heatmap.add_subplot(111)
            self.test_axes.cla()
            sel_cmap = self.file.get(key,self.cmap)
            self.test_axes.imshow(self.test_grid,cmap=sel_cmap)
            label = ' '.join([ i.capitalize() for i in f"{key}".split('_')])
            self.test_axes.set_ylabel(label)
            self.test_axes.xaxis.set_visible(False)
            self.example_display.draw()
            self.key=key
    
    def handle_keys(self,evt,*args,**kwargs):
        index:tuple = self.cmaps.curselection()
        print(evt)
        if(index.__len__()==0):
            return
        index = index[0]
        
        if(evt.keysym=='Up'):
            new_index =  max(0,(index -1) % self.cmaps.size())
            self.cmaps.selection_clear(index)
            self.cmaps.selection_set(new_index)
            self.cmaps.activate(new_index)
            self.cmaps.event_generate('<<ListboxSelect>>')
            
        elif(evt.keysym=='Down'):
            new_index =  (index +1) % self.cmaps.size()
            self.cmaps.selection_clear(index)
            self.cmaps.selection_set(new_index)
            self.cmaps.activate(new_index)
            self.cmaps.event_generate('<<ListboxSelect>>')

    def submit(self,*args):
        print(self.key)
        if self.key is None:
            return
        if self.key not in self.file:
            return
        key = self.key
        if(self.current_sel!=key) or (self.cmap is None):
            self.current_sel=key
            self.cmap =  self.file[key]
            print(self.cmap)
        mplib.rc('image', cmap=self.cmap)   
        print(args)
scene = CMapper
if __name__ == '__main__':
    root = tk.Tk()
    frame = CMapper(master=root)
    frame2 = tk.Frame()
    root.mainloop()