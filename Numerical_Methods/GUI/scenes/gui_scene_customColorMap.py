import gzip
import tkinter as tk
import tkinter.commondialog as tkcommon
import os, os.path as pth
import sys

import numpy as np

__base__ = pth.abspath(pth.dirname(__file__))

def loadCMap(file):
    print('Loading',file)
    with open(file,'rb') as file:
        cmap = np.load(file,allow_pickle=True)
        cmaps = dict()
        for key in cmap.files:
            cmaps[key] = cmap[key]

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
        self.pack()
        
        self.createWidgets()
        self.config(height=480,width=640)
        self.update()
        tk.Wm.geometry(self.winfo_toplevel(),'640x480')

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
            return [*self.file.keys()]
        else:
            print('\tNo Available CMaps')
            self.ftype=None
            self.loc=None
            return []
    def createWidgets(self):
        L1 = tk.Label(self, text='Color Map')
        cmaps=self.cmaps=tk.Listbox(self, selectmode=tk.SINGLE)
        cmapsList=self.getAvailableCMaps()
        cmaps.insert(0,*cmapsList)
        cmaps.grid(row=1,sticky='NW')
        cmaps.bind('<<ListboxSelect>>',self.selected_cmap,add='+')
        self.current_sel = cmaps.get(0,0)
        self.key = None
        L1.grid(row=0,sticky='NW',column=0)
        button = tk.Button(self, text='Select Color Map', command=self.submit)
        button.grid(row=2,sticky='NW')
        

    def selected_cmap(self,*args):
        index:tuple = self.cmaps.curselection()
        if(index.__len__()==0):
            return
        self.key =self.cmaps.get(index[0])

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
           
        print(args)
scene = CMapper
if __name__ == '__main__':
    root = tk.Tk()
    frame = CMapper(master=root)
    frame2 = tk.Frame()
    root.mainloop()