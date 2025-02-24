import typing
from ...utils import geometry
import numpy as np

class GeometryFactory(typing.Callable):
    def __int__(self,seperation, plate_seperation, V, cx, cy:'float|str'='centre'):
        self.grnd1:'str' = None
        self.V_plus: 'str' = None
        self.grnd2:'str' = None
        self.V_negative: 'str' = None
    
    def __call__(self,*args,**kwargs):pass

def highSpeedFactory(
    Grid:np.ndarray[np.float64],
    width,
    height,
    cx:'float|str'='center',
    cy:'float|str'='center',
    spacings:'float'=None,
    padding: "np.ndarray" = None,
    dx:float = 1.0,
    dy:float = 1.0,
):
    gheight:float
    gwidth:float
    
    gheight,gwidth=np.array(Grid.shape,dtype=np.float64,copy=True,order='C')*(dy,dx)
    if height>gheight or width>gwidth:
        raise ValueError('Cannot have the width greater than the established width')
    width/2
    geometry.rectangle_w_h()
    for i in range(4):pass
        
        



if __name__ == "__main__":
    EGrid = np.ones((500,500))
    EGrid=bounds(EGrid,40,40,90,5,100,'centre',True,0,0,3)
    plt.figure(figsize=(15,15))
    plt.imshow(EGrid)
    plt.colorbar()
    plt.show()