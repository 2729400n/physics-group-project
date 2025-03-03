# License: None
# Author: P3 Comp. 2025 Lab Group B (Electrostatics)
# Description: The geometry module handles the creation of non-simple geometries in a finitely expressible way.

import numpy as np


def circle(cx: float, cy: float, r: float, dx: float = 1, dy: float = 1, val: float = 1.0, fill: bool = False, clear: bool = False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None):
    """Generate a pixelated circle or update an existing grid with the circle."""
    
    def condition(x, y, z):
        return np.abs(x - y) <= z if fill else (x <= y if clear else x >= y)

    # Determine grid size
    if isinstance(Grid, tuple):
        Grid = np.full(Grid, 1)

    if Grid is not None:
        y, x = Grid.shape
    else:
        x = 2 * int(r // dx) + 5
        y = 2 * int(r // dy) + 5

    # Generate coordinate grids
    grid_y, grid_x = np.mgrid[:y, :x]

    # Apply circular mask
    circle_mask = condition((grid_x - cx) ** 2 + (grid_y - cy) ** 2, r ** 2, r)
    
    # Apply values
    pixelated_circle = np.where(circle_mask, val, 0) if not isinstance(val, bool) else circle_mask

    if Grid is not None:
        return Grid * pixelated_circle

    return pixelated_circle


def circle_bool(cx: float, cy: float, r: float, dx: float = 1, dy: float = 1, fill: bool = False, clear: bool = False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None):
    """Boolean mask version of the circle function."""
    
    def condition(x, y, z):
        return np.abs(x - y) <= z if fill else (x <= y if clear else x >= y)

    if isinstance(Grid, tuple):
        Grid = np.full(Grid, 1)

    if Grid is not None:
        y, x = Grid.shape
    else:
        x = 2 * int(r // dx) + 5
        y = 2 * int(r // dy) + 5

    grid_y, grid_x = np.mgrid[:y, :x]

    circle_mask = condition((grid_x - cx) ** 2 + (grid_y - cy) ** 2, r ** 2, r)
    
    return circle_mask


def annulus(cx, cy, r1, r2, dx=1, dy=1, val=1.0, fill=False, clear=False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None):
    """Generate an annulus (ring shape) or update an existing grid with it."""
    
    def condition(w, x, y, z, zz):
        if fill:
            return np.logical_or(np.abs(w - x) <= z, np.abs(w - y) <= zz)
        return np.logical_and(x <= w, w <= y) if not clear else np.logical_or(x > w, w > y)

    if isinstance(Grid, tuple):
        Grid = np.full(Grid, 1)

    if Grid is not None:
        y, x = Grid.shape
    else:
        x = 2 * int(r2 // dx) + 5
        y = 2 * int(r2 // dy) + 5

    grid_y, grid_x = np.mgrid[:y, :x]
    annulus_mask = condition((grid_x - cx) ** 2 + (grid_y - cy) ** 2, r1 ** 2, r2 ** 2, r1, r2)
    
    pixelated_annulus = np.where(annulus_mask, val, 0)

    if Grid is not None:
        return Grid * pixelated_annulus

    return pixelated_annulus


def rectangle(x0: float, y0: float, x1: float, y1: float, dx: float = 1.0, dy: float = 1.0, val: float = 1.0, fill: bool = False, clear: bool = False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None):
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


def rectangle_w_h(x: float, y: float, w: float, h: float, dx=1, dy=1, val=1.0, fill=False, clear=False, Grid: 'np.ndarray[np.ndarray[np.float64]]' = None):
    """Wrapper for rectangle using width and height."""
    return rectangle(x, y, x + w, y + h, dx, dy, val, fill, clear, Grid)


def identityOverlay(Grid: np.ndarray):
    """Returns an identity overlay for the given grid."""
    return np.full_like(Grid, 1)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    grid = np.ones((100, 100))
    circ = rectangle_w_h(10, 10, 40, 40, fill=True, clear=True, Grid=grid)

    plt.imshow(circ, )
    plt.colorbar()
    plt.title('Pixelated Shape')
    plt.show()
