from matplotlib.colorbar import Colorbar
from matplotlib.quiver import Quiver
import numpy as np
from .boundary import geometryFactory as Boundary
from ...Solvers import findUandV, laplace_ode_solver_continue
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from ..task import Task
import io
from PIL import Image



class Task1(Task):
    '''
        Task1:
            description: Task one is the first task given to solve the anulus situation.
            The class defines the standard task inteface methods.
    '''
    
    name = "Anulus"

    def __init__(self, axes: 'Axes' = None, *args, **kwargs):
        super().__init__()
        self.Image: AxesImage = None
        self.grid = None
        self.cbar: Colorbar = None
        self.quivers: Quiver = None
        self.savables.update(**{'Grid': self.save_grid,'Figure':self.save_figure})

    def setup(self, x1: float, y1: float, r1: float, r2: float, cx: float,
              cy: float, v: float = 1.0, x0: float = 0.0, y0: float = 0.0,
              dy: float = 1.0, dx: float = 1.0):

        x0, x1 = (x0, x1) if x0 <= x1 else (x1, x0)
        y0, y1 = (y0, y1) if y0 <= y1 else (y1, y0)
        
        print(x0, x1, dx)
        Xs = np.arange(x0, x1+dx, dx)
        Ys = np.arange(y0, y1+dy, dy)

        grid = np.zeros(shape=(Ys.shape[0], Xs.shape[0]), dtype=np.float64)
        self.boundaryCondition = Boundary(v, r1, r2, cx, cy)
        self.cbar: Colorbar = None
        self.quivers: Quiver = None
        self.grid = grid = self.boundaryCondition(Grid=grid, retoverlay=False)
        self.Xs, self.Ys = np.mgrid[:grid.shape[1], :grid.shape[0]]
        self.resXs = Xs
        self.resYs = Ys
        self.resdx = dx
        self.resdy = dy
        axes = self.axes

        axes.imshow(grid)
        axes.set_title('Electrostatic Potential')
        self.figure.canvas.figure = None
        self.figure.canvas.figure = self.figure
        self.figure.canvas.draw_idle()

    def redraw(self):
        if (self.grid) is not None:
            return
        self.axes.clear()
        # img = self.axes.imshow(self.grid)
        return

    def _show_Efield(self):
        u_v = findUandV(grid=self.grid)[::5, ::5]*25
        axes = self.axes
        Xs = self.Xs[::5, ::5]
        Ys = self.Ys[::5, ::5]
        if self.quivers is not None:
            self.quivers.set_visible(False)
            self.quivers.remove()
            self.quivers = None
        quiv = axes.quiver(Xs, Ys, u_v[:, :, 0], u_v[:, :, 1], color='b',
                           scale=0.1, scale_units='xy')
        self.quivers = quiv

    def run(self):
        Xs, Ys, self.grid = laplace_ode_solver_continue(
            self.grid, self.boundaryCondition)
        if self.cbar is not None:
            self.cbar.remove()
            self.cbar = None
            self.figure.clear()
            axes = self.figure.add_subplot(111)
            self.axes = axes
        self.axes.imshow(self.grid)

        self.figure.draw_without_rendering()
        self.figure.colorbar(self.axes.images[0])

        self.figure.canvas.draw()

    def _cleanup(self):
        self.Image: AxesImage = None
        self.grid: np.ndarray = None
        self.cbar: Colorbar = None
        self.quivers: Quiver = None

    def reset(self):
        if self.grid is not None:
            self.grid[:,:] = 0
            
    def save_grid(self):
        if self.grid is None:
            return (None,None)
        outfile = io.BytesIO()
        np.save(outfile,self.grid,allow_pickle=True)
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_grid.npy',outfile.read()
    
    def save_figure(self):
        if self.figure is None:
            return
        outfile = io.BytesIO()
        self.figure.savefig(outfile,format='png')
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_figure.png',outfile.read()

