# Description: This script generates a custom colormap for the heatmap
import binascii,zlib,gzip
import matplotlib.colors as mcolors
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
    cmap = '\n'.join(makeCustomCmap()).encode()
    cmap=gzip.compress(cmap)
    with open('custom_cmap.dat','wb') as file:
        file.write(cmap)
        file.close()

def loadCMap():
    with open('custom_cmap.dat','rb') as file:
        cmap = gzip.decompress(file.read())
    return cmap.decode().split('\n')



if __name__ == '__main__':
    storeCMap()
    print('Custom Colormap has been generated and stored in custom_cmap.dat')

colors = loadCMap()
print(colors)

if __name__ != '__main__':
    rollerCoaster = mcolors.ListedColormap(colors,name='mapper',N=len(colors))