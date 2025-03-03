from matplotlib.colorbar import Colorbar
from matplotlib.quiver import Quiver
import numpy as np
from .boundary import geometryFactory as Boundary
from ...Solvers import laplace_ode_solver, findUandV,laplace_ode_solver_step,laplace_ode_solver_continue
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from ..task import Task
import io

class TripleCircle(Task):
    '''
        Task1:
            description: Task one is the first task given to solve the anulus situation.
            The class defines the standard task interface methods.
    '''
    
    name = "Anulus_Extended"

    def __init__(self, axes: 'Axes' = None, *args, **kwargs):
        super().__init__(axes=axes, *args, **kwargs)
        self._Image = None
        self._quivers = None
        self._cbar = None
        self.grid = None

    def setup(self, x1: float, y1: float, r1: float, r2: float,r3:float, cx: float,
              cy: float, v1: float = 1.0,v2: float = 1.0,v3: float = 1.0, x0: float = 0.0, y0: float = 0.0,
              dy: float = 1.0, dx: float = 1.0):
        '''Setup the grid and boundary condition, display the initial potential.'''
        x0, x1 = (x0, x1) if x0 <= x1 else (x1, x0)
        y0, y1 = (y0, y1) if y0 <= y1 else (y1, y0)
        
        print(x0, x1, dx)
        Ys=self.Xs = np.arange(x0, x1+dx, dx)
        Xs=self.Ys = np.arange(y0, y1+dy, dy)

        grid = np.zeros(shape=(Ys.shape[0], Xs.shape[0]), dtype=np.float64)
        self.boundaryCondition = Boundary(val1=v1,val2=v2,val3=v3, r1=r1, r2=r2,r3=r3, cx=cx, cy=cy)
        self.grid = grid = self.boundaryCondition(Grid=grid, retoverlay=False)
        self.Xs, self.Ys = np.mgrid[:grid.shape[1], :grid.shape[0]]
        self.resXs = Xs
        self.resYs = Ys
        self.resdx = dx
        self.resdy = dy

        # Remove old image if it exists
        if self._Image:
            self._Image.remove()

        axes = self.axes
        self._Image = axes.imshow(grid, )
        # self._Image.set_clim(vmin=np.min(0), vmax=np.max(self.grid))  # Set color limits
        axes.set_title('Electrostatic Potential')

        # Update the figure canvas to reflect changes
        self.figure.canvas.draw_idle()

    def redraw(self):
        '''Redraw the grid and other plot elements.'''
        if self.grid is None:
            return
        self.axes.clear()
        self._Image = self.axes.imshow(self.grid, )
        # self._Image.set_clim(vmin=0, vmax=np.max(self.grid))  # Set color limits

    def _show_Efield(self):
        '''Display the electric field as quivers.'''
        u_v = findUandV(grid=self.grid)[::5, ::5]
        axes = self.axes
        Xs, Ys = self.Xs[::5, ::5], self.Ys[::5, ::5]
        
        # Remove previous quivers if they exist
        if self._quivers:
            self._quivers.remove()

        # Draw new quivers
        self._quivers = axes.quiver(Xs, Ys, u_v[:, :, 0], u_v[:, :, 1], color='b', scale=1, scale_units='xy')

    def run(self,maxruns:int=1000,stencil:int=5,gamma:float=0.0,abs_tol:float=1e-9,rel_tol:float=1e-6,wrap:bool=False,wrap_axis:str='none'):
        '''Solve the Laplace equation and update the grid and electric field.'''
        Xs, Ys, self.grid = laplace_ode_solver_continue(self.grid, self.boundaryCondition,max_iterations=maxruns,abs_tol=abs_tol,
                                                        rel_tol=rel_tol,stencil=stencil,gamma=gamma,wrap=wrap,wrap_direction=wrap_axis)
        
        # Remove the previous colorbar and reset it
        if self._cbar is not None:
            try:
                self._cbar.remove()
            except:
                pass

        self.axes.imshow(self.grid, )
        self._cbar = self.figure.colorbar(self._Image, ax=self.axes)

        self.figure.canvas.draw()

    def _cleanup(self):
        '''Remove all artists from the axes and reset class attributes.'''
        if self._Image:
            try:
                self._Image.remove()
            except:
                pass
        if self._quivers is not None:
            try:
                self._quivers.remove()
            except:
                pass
        if self._cbar is not None:
            try:
                self._cbar.remove()
            except:
                pass

        self._Image = None
        self._quivers = None
        self._cbar = None
        self.grid = None

    def reset(self):
        '''Reset the grid and boundary condition to initial state.'''
        if self.grid is not None:
            self.grid[:, :] = 0

    def save_grid(self):
        '''Save the grid to a file.'''
        if self.grid is None:
            return (None, None)
        outfile = io.BytesIO()
        np.save(outfile, self.grid, allow_pickle=True)
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_grid.npy', outfile.read()

    def save_figure(self):
        '''Save the current figure to a file.'''
        if self.figure is None:
            return
        outfile = io.BytesIO()
        self.figure.savefig(outfile, format='png')
        try:
            outfile.flush()
        except:
            pass
        outfile.seek(0)
        return 'Task1_figure.png', outfile.read()

