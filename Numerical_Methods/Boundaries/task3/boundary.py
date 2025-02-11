from ...utils import geometry
import numpy as np


def highSpeedFactory(
    width,
    height,
    rects: "Rectangle_x4" = None,
    spacings=None,
    padding: "np.ndarray" = None,
):
    Gridder = None

    def highSpeedGeometry(Grid: np.ndarray, overlay=None, retoverlay=False):
        for rect in rects:
            Grid = Grid * geometry.rectangle(*rect, fill=True, clear=True, Grid=Grid)
        Grid[1:-1, (0, -1)] = 0.25 * (
            Grid[2:, (0, -1)]
            + Grid[:-2, (0, -1)]
            + Grid[1:-1, (-1, -2)]
            + Grid[1:-1, (1, 0)]
        )
        return Grid

    return highSpeedGeometry
