# License: None
# Author: P3 Comp. 2025 Lab Group B ( Electrostatics )
# Description: The geometry module handles the creation of non-simple geometries in a finitely expressable way

import numpy as np


# TODO Fix all Circular constraints : The cirlce seems to have an r value that is 1 greater than expected

def circle(cx: float, cy: float, r: float, dx: float = 1, dy: float = 1, val: float = 1.0,
           fill: bool = False, clear: bool = False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None, thickness:float=1.0):
    # First solve for a qudrant the apply rotations
    operations = [[lambda x, y, z:np.abs(
        x-y) <= z]*2, [lambda x, y, z:x <= y, lambda x, y, z:x >= y]]
    grid_class = type(Grid)

    # if all we want is a  circle
    x = 2*int(r//dx)+5
    y = 2*int(r//dy)+5

    if type(Grid) == tuple:
        Grid = np.full(Grid, 1)

    # if we inplace into a grid
    if Grid is not None:
        y, x = Grid.shape
        # print(x,y)

    grid_y,grid_x = np.mgrid[:y, :x]

    # TODO Variate Tolerance : the cirlces tolerance for a non filled circle should be a function of the radius
    # Currently not implemented correctly it causes a band instead of a line this band width can variet based on the tolerance
    tolerance = r  # Ensure tolerance does not dominate
    print(r)
    circle_mask = operations[bool(fill)][bool(clear)](
        (grid_x-cx)**2 + (grid_y-cy)**2, r**2, thickness*tolerance)
    # Apply anti-aliasing using Gaussian blur
    # blurred_circle = gaussian_filter(circle_mask.astype(float), sigma=antialias_sigma)
    vals = (val,0) if not isinstance(val,bool) else (val,not val)
    # Threshold to create a binary image (0 or 1)
    pixelated_circle = np.where(circle_mask == True, *vals)

    # mul mask
    if Grid is not None:
        if (grid_class != tuple):
            return Grid*pixelated_circle

    return pixelated_circle

def circle_bool(cx: float, cy: float, r: float, dx: float = 1, dy: float = 1, val: float = 1.0,
                fill: bool = False, clear: bool = False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None, thickness:float=1.0):
    # First solve for a qudrant the apply rotations
    operations = [[lambda x, y, z:np.abs(
        x-y) <= z]*2, [lambda x, y, z:x <= y, lambda x, y, z:x >= y]]
    

    if isinstance(Grid,tuple):
        Grid = np.full(Grid, 1)

    # if we inplace into a grid
    if Grid is not None:
        y, x = Grid.shape
        y=y/dy
        x=x/dx
        # print(x,y)
    else:
        # if all we want is a  circle
        x = 2*int(r//dx)+5
        y = 2*int(r//dy)+5

    grid_y, grid_x  = np.mgrid[:y:dy, :x:dx]
    # TODO Variate Tolerance : the cirlces tolerance for a non filled circle should be a function of the radius
    # Currently not implemented correctly it causes a band instead of a line this band width can variet based on the tolerance
    tolerance = r  # Ensure tolerance does not dominate
    # print(r)
    circle_mask = operations[bool(fill)][bool(clear)](
        (grid_x-cx)**2 + (grid_y-cy)**2, r**2, thickness*tolerance)
    
    pixelated_circle = circle_mask

    return pixelated_circle


def annulus(cx, cy, r1, r2, dx=1, dy=1, val=1.0, fill=False, clear=False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None):
    # First solve for a qudrant the apply rotations
    # TODO Add Finer Control: Could someone add finer controls to allow for control over the inner and outer values of the annulus
    operations = [[lambda w, x, y, z, zz:np.logical_or(np.abs(w-x) <= z, np.abs(w-y) <= zz)]*2, [
        lambda w, x, y, z, zz:np.logical_and(x <= w, w <= y), lambda w, x, y, z, zz:(np.logical_or(x > w, w > y))]]

    grid_class = type(Grid)

    if type(Grid) == tuple:
        Grid = np.full(Grid, 1)
    # if we inplace into a grid
    if Grid is not None:
        y, x = Grid.shape
        # print(x,y)

    grid_x, grid_y = np.mgrid[:y, :x]
    annulus_mask = operations[bool(fill)][bool(clear)](
        ((grid_x-cx)**2 + (grid_y-cy)**2), r1**2, r2**2, r1, r2)
    
    vals = (1, 0)
    # Threshold to create a binary image (0 or 1)
    pixelated_annulus = np.where(annulus_mask == True, *vals)

    # mul mask
    if Grid is not None:
        if (grid_class != tuple):
            return Grid*pixelated_annulus

    return pixelated_annulus


def rectangle_smooth(x0:np.float64, y0:np.float64, x1:np.float64, y1:np.float64, dx:float=1.0, dy:float=1.0, val: float = 1.0, fill: bool = False, clear: bool = False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None, blocking=False, thickness=1):

    if y1 < y0:
        y0, y1 = y1, y0
    if x1 < x0:
        x0, x1 = x1, x0

    grid_class = type(Grid)

    if type(Grid) == tuple:
        Grid = np.full(Grid, 1)

    if Grid is not None:
        y, x = Grid.shape
    
    y0=y0/dy
    y1=y1/dy
    x0=x0/dx
    x1=x1/dx

    if (not blocking) and (not fill):
        x1 = None if x1 > x else x1
        x0 = None if x0 < 0 else x0

        y1 = None if y1 > y else y1
        y0 = None if y0 < 0 else y0
    else:
        x1 = min(max(x-1, 0), x1)
        x0 = max(0, x0)

        y1 = min(max(y-1, 0), y1)
        y0 = max(0, y0)

    mul_mask = np.full_like(Grid, 1)
    sets_masks = [np.full_like(Grid,False,dtype=bool),np.ones_like(Grid,dtype=np.float64)]
    
    
    if fill:
        
        # print([y0,y1,x0,x1])
        y0_ceil,y1_ceil,x0_ceil,x1_ceil =[int(np.ceil(i)) for i in [y0,y1,x0,x1]]
        y0_floor,y1_floor,x0_floor,x1_floor=[int(np.floor(i)) for i in [y0,y1,x0,x1]]
        mul_mask[y0_ceil:y1_ceil, x0_ceil:x1_ceil] = 0 if clear else 1
        # print([y0_ceil,y1_ceil,x0_ceil,x1_ceil])
        # print([y0_floor,y1_floor,x0_floor,x1_floor])
        
        sets_masks[1][y0_floor, x0_ceil:x1_floor+1] = np.abs(y0_floor-y0)
        sets_masks[1][y1_ceil, x0_ceil:x1_floor+1] = np.abs(y1_ceil-y1)
        sets_masks[1][y0_ceil:y1_floor+1, x0_floor] = np.abs(x0_floor-x0)
        sets_masks[1][y0_ceil:y1_floor+1, x1_ceil] = np.abs(x1_ceil-x1)
        
        # print(np.abs(y0_floor-y0))
        # print(np.abs(y1_ceil-y1))
        # print(np.abs(x0_floor-x0))
        # print(np.abs(x1_ceil-x1))
        
        
        sets_masks[1][y0_floor, x0_floor] = np.sqrt(((x0_floor-x0)**2+(y0_floor-y0)**2)/2)
        sets_masks[1][y0_floor, x1_ceil] = np.sqrt(((x1_ceil-x1)**2+(y0_floor-y0)**2)/2)
        sets_masks[1][y1_ceil, x0_floor] = np.sqrt(((x0_floor-x0)**2+(y1_ceil-y1)**2)/2)
        sets_masks[1][y1_ceil, x1_ceil] = np.sqrt(((x1_ceil-x1)**2+(y1_ceil-y1)**2)/2)
        
        sets_masks[0][(y0_floor,y1_ceil), x0_floor:x1_ceil+1] = True 
        sets_masks[0][y0_floor:y1_ceil+1, (x0_floor,x1_ceil)] = True
        
    else:

        mul_mask[tuple([i for i in (y0, y1) if i is not None]), x0:x1] = mul_mask[y0:y1, tuple(
            [i for i in (x0, x1) if i is not None])] = 0 if clear else 1
    
    sets_masks[0]= sets_masks[0]==True
    # print(sets_masks[0],sets_masks[1],sep='\n')
    if Grid is not None:
        if (grid_class != tuple):
            out = Grid*mul_mask
            out[sets_masks[0]]= out[sets_masks[0]]*sets_masks[1][sets_masks[0]]
            return out
        
    out = mul_mask
    out[sets_masks[0]]= out[sets_masks[0]]*sets_masks[sets_masks[0]]
    return out

# A wrapper function for Rectangle


def rectangle_w_h_smooth(x, y, w, h, dx=1, dy=1, val=1.0, fill=False, clear=False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None):

    x0 = x
    x1 = x+w
    y0 = y
    y1 = y+h
    return rectangle_smooth(x0=x0, x1=x1, y0=y0, y1=y1, dx=dx, dy=dy, val=val, fill=fill, clear=clear, Grid=Grid)


def rectangle_gpt(x0: float, y0: float, x1: float, y1: float, dx: float = 1.0, dy: float = 1.0, val: float = 1.0, fill: bool = False, clear: bool = False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None):
    """Generate a rectangle or update an existing grid with the rectangle."""
    
    if y1 < y0:
        y0, y1 = y1, y0
    if x1 < x0:
        x0, x1 = x1, x0

    if isinstance(Grid, tuple):
        Grid = np.full(Grid, 1)

    if Grid is not None:
        y, x = Grid.shape
    else:
        y, x = int((y1 - y0) // dy) + 5, int((x1 - x0) // dx) + 5

    y0, y1, x0, x1 = [int(round(coord / step)) for coord, step in [(y0, dy), (y1, dy), (x0, dx), (x1, dx)]]

    mask = np.zeros((y, x), dtype=bool)
    
    if fill:
        mask[y0:y1, x0:x1] = True
    else:
        mask[y0, x0:x1] = mask[y1 - 1, x0:x1] = True
        mask[y0:y1, x0] = mask[y0:y1, x1 - 1] = True

    pixelated_rectangle = np.where(mask, val, 0)

    if Grid is not None:
        return Grid * pixelated_rectangle

    return pixelated_rectangle


def rectangle_w_h_gpt(x: float, y: float, w: float, h: float, dx=1, dy=1, val=1.0, fill=False, clear=False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None):
    """Wrapper for rectangle using width and height."""
    return rectangle(x, y, x + w, y + h, dx, dy, val, fill, clear, Grid)



def rectangle(x0, y0, x1, y1, dx=1, dy=1, val:float=1.0, fill:bool=False, clear:bool=False, Grid:'np.ndarray[np.ndarray[np.float64]]'=None,blocking=False,thickness=1):
    
    if y1<y0:
        y0,y1 = y1,y0
    if x1<x0:
        x0,x1 = x1,x0
        
    grid_class = type(Grid)
    
    if type(Grid) == tuple:
        Grid = np.full(Grid,1)
    
    if Grid is not None:
        y,x = Grid.shape
        
    if not blocking:
        x1 = None if x1 > x else x1
        x0 = None if x0 < 0 else x0

        y1 = None if y1 > y else y1
        y0 = None if y0 < 0 else y0
    else:
        x1 = min(max(x-1,0),x1)
        x0 = max(0,x0)

        y1 = min(max(y-1,0),y1)
        y0 = max(0,y0)
    
    mul_mask = np.full_like(Grid,1)
    
    if fill:
        mul_mask[y0:y1,x0:x1] = 0 if clear else 1
    else:
        
        mul_mask[tuple( [i for i in (y0,y1) if i is not None]  ),x0:x1] = mul_mask[y0:y1, tuple( [i for i in (x0,x1) if i is not None]  )] = 0 if clear else 1
    if Grid is not  None:
        if(grid_class!=tuple):
            return Grid*mul_mask
    
    return mul_mask

# A wrapper function for Rectangle 
def rectangle_w_h(x,y,w,h,dx=1,dy=1,val=1.0,fill=False,clear=False,Grid:'np.ndarray[np.ndarray[np.float64]]'=None):
    
    x0=x
    x1=x+w
    y0 = y
    y1 =y+h
    return rectangle(x0=x0, x1=x1, y0=y0, y1=y1, dx=dx, dy=dy,val=val,fill=fill,clear=clear,Grid=Grid) 


def rectangle_bool(x0, y0, x1, y1, dx=1, dy=1, val:float=1.0, fill:bool=False, clear:bool=False, Grid:'np.ndarray[np.ndarray[np.float64]]'=None,blocking=False,thickness=1):
    
    if y1 < y0:
        y0, y1 = y1, y0
    if x1 < x0:
        x0, x1 = x1, x0

    grid_class = type(Grid)

    if type(Grid) == tuple:
        Grid = np.full(Grid, 1)

    if Grid is not None:
        y, x = Grid.shape
    
    y0=y0/dy
    y1=y1/dy
    x0=x0/dx
    x1=x1/dx

    if (not blocking) and (not fill):
        x1 = None if x1 > x else x1
        x0 = None if x0 < 0 else x0

        y1 = None if y1 > y else y1
        y0 = None if y0 < 0 else y0
    else:
        x1 = min(max(x-1, 0), x1)
        x0 = max(0, x0)

        y1 = min(max(y-1, 0), y1)
        y0 = max(0, y0)
        
    sets_masks = [np.full_like(Grid,False,dtype=bool),np.ones_like(Grid,dtype=np.float64)]
    
    
    if fill:
        
        # print([y0,y1,x0,x1])
        y0_ceil,y1_ceil,x0_ceil,x1_ceil =[int(np.ceil(i)) for i in [y0,y1,x0,x1]]
        y0_floor,y1_floor,x0_floor,x1_floor=[int(np.floor(i)) for i in [y0,y1,x0,x1]]
        
        sets_masks[0][y0_ceil:y1_ceil, x0_floor:x1_ceil] = False if clear else True
        sets_masks[0][y0_floor:y1_ceil, x0_floor:x1_ceil] = False  if clear else True 
        
        # sets_masks[0][(y0_floor,y1_ceil), x0_floor:x1_ceil+1] = True 
        # sets_masks[0][y0_floor:y1_ceil+1, (x0_floor,x1_ceil)] = True
        
    else:

        sets_masks[:,tuple([i for i in (y0, y1) if i is not None]), x0:x1] = sets_masks[:,y0:y1, tuple(
            [i for i in (x0, x1) if i is not None])] = False if clear else True
    
    sets_masks[0]= sets_masks[0]==True
    
    return sets_masks[0]

 
def rectangle_w_h_bool(x,y,w,h,dx=1,dy=1,val=1.0,fill=False,clear=False,Grid:'np.ndarray[np.ndarray[np.float64]]'=None):
    
    x0=x
    x1=x+w
    y0 = y
    y1 =y+h
    return rectangle_bool(x0=x0, x1=x1, y0=y0, y1=y1, dx=dx, dy=dy,val=val,fill=fill,clear=clear,Grid=Grid) 

def identityOverlay(Grid: np.ndarray):
    """Returns an identity overlay for the given grid."""
    return np.full_like(Grid, 1)

# if __name__ == '__main__':
#     import matplotlib.artist,matplotlib.patches,matplotlib.path,matplotlib.pyplot as plt
#     grid = np.zeros((500,500))
#     grid[:,:]=1
#     circ=annulus(100,100,25,100,2,fill=False,clear=False,Grid=grid)

#     plt.imshow(circ, cmap='gray')
#     plt.colorbar()
#     plt.title('Pixelated Circle with Anti-aliasing')
#     plt.show()

if __name__ == '__main__':
    import matplotlib.artist
    import matplotlib.patches
    import matplotlib.path
    import matplotlib.pyplot as plt
    grid = np.zeros((100, 100))
    grid[:, :] = 1
    circ = rectangle_w_h_smooth(1.5, 7.89, 79.83323, 20.332, fill=True,
                         clear=True, Grid=grid)
    plt.imshow(circ, cmap='gray')
    plt.colorbar()
    plt.title('Pixelated Circle with Anti-aliasing')
    plt.show()
