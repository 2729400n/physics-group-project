import gzip
import tkinter as tk
import tkinter.commondialog as tkcommon
import os, os.path as pth
import sys

import numpy as np

def loadCMap(file):
    print('Loading',file)
    with open(file,'rb') as file:
        cmap = np.load(file,allow_pickle=True)
        cmaps = dict()
        for key in cmap.files:
            cmaps[key] = cmap[key]

    return cmaps

class CMapper(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        
        self.createWidgets()
        self.config(height=480,width=640)
        self.update()
        tk.Wm.geometry(self.winfo_toplevel(),'640x480')

    def getAvailableCMaps(self):
        print('Available CMaps')
        if(pth.isdir('../cmaps')):
            print('Loading Available CMaps')
            self.ftype = 'dir'
            self.loc = '../cmaps'
            return os.listdir('../cmaps')
        elif(pth.isfile(pth.join(pth.dirname(__file__),'../custom_cmap.dat'))):
            print('Loading Available CMaps')
            self.ftype = 'file_single'
            self.loc = pth.join(pth.dirname(__file__),'../custom_cmap.dat')
            self.file = loadCMap(self.loc)

            return [*self.file.keys()]
        else:
            print('No Available CMaps')
            self.ftype=''
            self.loc=''
            return []
    def createWidgets(self):
        L1 = tk.Label(self, text='Color Map')
        cmaps=self.cmaps=tk.Listbox(self, selectmode=tk.SINGLE)
        cmapsList=self.getAvailableCMaps()
        cmaps.insert(0,*cmapsList)
        cmaps.pack()
        cmaps.bind('<<ListboxSelect>>',self.selected_cmap,add='+')
        self.current_sel = cmaps.get(0,0)
        self.key = None
        L1.pack()
        self.homebutton = tk.Button(self, text='Home', command=self.quit)
        self.homebutton.pack()
        button = tk.Button(self, text='Select Color Map', command=self.submit)
        button.pack()

    def selected_cmap(self,*args):
        index:tuple = self.cmaps.curselection()
        if(index.__len__()==0):
            return
        self.key =self.cmaps.get(index[0])

    def submit(self,*args):
        if self.key is None:
            return
        if self.key not in self.file:
            return
        key = self.key
        if(self.current_sel!=key):
            self.current_sel=key
            if(self.ftype=='dir'):
                self.loc = pth.join('../cmaps',self.cmaps.get(self.current_sel))
            elif(self.ftype=='file_single'):
                self.file[self.current_sel]
        print(args)
root = tk.Tk()
frame = CMapper(master=root)
frame2 = tk.Frame()
root.mainloop()