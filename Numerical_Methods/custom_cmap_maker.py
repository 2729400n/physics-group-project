# Description: This script generates a custom colormap for the heatmap
import binascii,zlib,gzip
import matplotlib.colors as mcolors, numpy as np
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

def storeCMap():
    cmap = makeCustomCmap()
    with open('custom_cmap.dat','wb') as file:
        np.savez_compressed(file,cmap=cmap)
    

def loadCMap():
    print('Loading')
    with open('custom_cmap.dat','rb') as file:
        cmap = np.load(file,allow_pickle=True).get('cmap',[])
    return cmap



if __name__ == '__main__':
    storeCMap()
    print('Custom Colormap has been generated and stored in custom_cmap.dat')

colors = loadCMap()


if __name__ != '__main__':
    rollerCoaster = mcolors.ListedColormap(colors,name='mapper',N=len(colors))
else:
    print(colors)