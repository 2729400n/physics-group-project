# Description: This script generates a custom colormap for the heatmap

import matplotlib.colors as mcolors, numpy as np
import os.path as pth

res_dir = pth.join(pth.abspath(pth.dirname(__file__)),'res/')
default_cmap_path = pth.join(res_dir,'custom_cmap.dat')
del pth

def makeCustomCmap():
    colors = []
    for i in range(256):
        colors+=['#'+hex(i)[2:].upper().strip().zfill(6)]
    for k in range(256):
        colors+=['#'+hex(k*256+i)[2:].upper().strip().zfill(6)]
    for i in range(255,0,-1):
        colors+=['#'+hex(k*256+i)[2:].upper().strip().zfill(6)]
    for i in range(256):
        colors+=['#'+hex(k*256+i*65536)[2:].upper().strip().zfill(6)]
    for k in range(254,-1,-1):
        colors+=['#'+hex(k*256+i*65536)[2:].upper().strip().zfill(6)]
    return colors

def storeCMap(cmap=None,dir=None):
    if cmap is None:
        cmap = makeCustomCmap()
    if dir is None:
        dir = default_cmap_path
    with open(dir,'wb') as file:
        np.savez_compressed(file,cmap=cmap)
        
    

def loadCMap(cmap=None, dir=None):
    if cmap is None:
        cmap = makeCustomCmap()
    if dir is None:
        dir = default_cmap_path
    with open(dir,'rb') as file:
        cmap = {**np.load(file,allow_pickle=True)}
    return cmap



if __name__ == '__main__':
    print('Although this module can be run directly. \r\nIt is recommended that you run the functions after importing it!')
    storeCMap()
    print('Custom Colormap has been generated and stored in custom_cmap.dat')

colors = loadCMap()


if __name__ != '__main__':
    rollerCoaster = mcolors.ListedColormap(colors,name='mapper',N=len(colors))
else:
    print(colors)