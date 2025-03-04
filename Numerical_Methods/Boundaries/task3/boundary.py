import numpy as np
from ...utils.geometry import rectangle,rectangle_w_h,rectangle_w_h_bool,rectangle_bool

def geometryFactory(val=1.0, pad_w=30, pad_h=30, gap=40, relative=False,NNCount=1):
    Gridder = None
    
    def powerGeometry(Grid: np.ndarray, overlay=None, retoverlay=False, *args, **kwargs):
        nonlocal Gridder
        temp1 = Grid.copy()
        # Set the top and bottom ground lines
        temp1[:2, :] = 0  # Top GND line
        temp1[-2:, :] = 0  # Bottom GND line
        
        # Define the positions of the voltage pads
        center_x = temp1.shape[1] / 2
        center_y = temp1.shape[0] / 2
        
        if Gridder is None:
            pad_positions = [
                (center_x - 2*(gap+pad_w),     center_y-pad_h/2,    0),  # GND Pad
                (center_x - (gap/2+pad_w), center_y-pad_h/2,  val),  # +V Pad
                (center_x + gap/2, center_y-pad_h/2, -val),  # -V Pad
                (center_x + (2*gap+pad_w),     center_y-pad_h/2,    0)  # GND Pad
            ]
        
            Gridder = []
            # Create the voltage pads       
            for (px, py,vv) in pad_positions:
                # print(px,py,vv)
                indexes = rectangle_w_h_bool(px, py, pad_w, pad_h, fill=True, clear=False, Grid=Grid)
                temp1[indexes] = vv
                Gridder+=[[indexes,vv]]
        else:
            for j in Gridder:
                temp1[j[0]] = j[1]
        if retoverlay:
            return temp1,Gridder
        return temp1
    
    return powerGeometry
