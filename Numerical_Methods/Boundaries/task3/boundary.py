import numpy as np
from ...utils.geometry import rectangle,rectangle_w_h

def geometryFactory(val=1.0, pad_w=30, pad_h=30, gap=40, relative=False):
    Gridder = None
    
    def powerGeometry(Grid: np.ndarray, overlay=None, retoverlay=False, *args, **kwargs):
        nonlocal Gridder
        
        # Set the top and bottom ground lines
        Grid[:2, :] = 0  # Top GND line
        Grid[-2:, :] = 0  # Bottom GND line
        
        # Define the positions of the voltage pads
        center_x = Grid.shape[1] / 2
        center_y = Grid.shape[0] / 2
        pad_positions = [
            (center_x - gap, center_y,0),  # GND Pad
            (center_x - gap / 3, center_y,val),  # +V Pad
            (center_x + gap / 3, center_y,-val),  # -V Pad
            (center_x + gap, center_y,0)  # GND Pad
        ]
        
        # Create the voltage pads
        for (px, py,vv) in pad_positions:
            print(px,py,vv)
            Grid = rectangle_w_h(px, py, pad_w, pad_h, fill=True, clear=True, Grid=Grid,val=vv)
            
        return Grid
    
    return powerGeometry
