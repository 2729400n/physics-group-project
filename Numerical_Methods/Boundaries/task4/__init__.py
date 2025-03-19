from .boundary import GeometryFactory as Boundary
from matplotlib.colorbar import Colorbar
from matplotlib.quiver import Quiver
import numpy as np
from ...Solvers import laplace_ode_solver, findUandV,laplace_ode_solver_step,laplace_ode_solver_continue
from ...Solvers.equations.electrostatics import energy,force,find_capacitance_per_length
from matplotlib.axes import Axes
from matplotlib.image import AxesImage
from ..task import Task
import io
from ... import Solvers
import matplotlib.colors as mcolors
class Task4(Task):
    name="MWPC"
    def __init__(self, axes: 'Axes' = None, *args, **kwargs):
        super().__init__(axes)
        self.exposed_methods+=[self.move_circle_by,self.move_circle_to]
        

    def setup(self, x1: float, y1: float, a: float, cx: float=0.0,
              cy: float=0.0, v: float = 1.0, x0: float = 0.0, y0: float = 0.0,l:float=1.0,s:float=1.0,
              dy: float = 1.0, dx: float = 1.0,centre:bool=True,max_spacing:bool=False,nncount:int=1):
        x0, x1 = (x0, x1) if x0 <= x1 else (x1, x0)
        y0, y1 = (y0, y1) if y0 <= y1 else (y1, y0)
        
        Xs=self.Xs = np.arange(x0, x1, dx)
        Ys=self.Ys = np.arange(y0, y1, dy)
        self.dx=dx
        self.dy=dy
        self.cy=cy
        self.cx=cx
        self.isCentered = centre
        if centre:
            self.cx=(x1*dx)/2
            self.cy=(y1*dy)/2
        grid = np.zeros(shape=(Ys.shape[0], Xs.shape[0]), dtype=np.float64)
        self.boundaryCondition=Boundary(radius=a,cx=cx,cy=cy,V=v,seperation=s,center=centre,plate_seperation=l,NNCount=nncount,half_plate_sep=max_spacing,dx=dx,dy=dy)
        self.grid =grid=self.boundaryCondition(Grid=grid)
        axes = self.axes
        self.Image=axes.imshow(grid)
        axes.set_title('Electrostatic Potential')
        if self.cbar is None:
            self.cbar = self.figure.colorbar(self.Image)
        
    def _show_Efield(self):
        '''Display the electric field as quivers.'''
        u_v=self.Efield = Solvers.findUandV(grid=self.grid)
        axes = self.axes
        Ys,Xs = np.meshgrid(self.Ys, self.Xs)
        
        # Remove previous quivers if they exist
        if self._quivers:
            self._quivers.remove()
            self._quivers=None

        Xs,Ys,U,V=(Xs[::5,::5], Ys[::5,::5], u_v[::5, ::5, 0], u_v[::5, ::5, 1])
            
        # Compute the magnitude of the vectors
        M = np.sqrt(U**2 + V**2)


        # Normalize the vectors (avoid division by zero)
        U_norm = U / (M + np.spacing(U))
        V_norm = V / (M + np.spacing(V))

        # Create a color map based on the magnitudes
        norm = mcolors.Normalize(vmin=M.min(), vmax=M.max())
                    
        # Plot the quiver with normalized vectors and colored by magnitude
        axes.quiver(Xs, Ys, U_norm.T, V_norm.T, M, scale=0.1, scale_units='xy', angles='uv',  norm=norm)
        
    def clear_quivers(self):
        if self.quivers is not None:
            self._quivers.remove()
            self._quivers=None
        return
    def find_capacitance(self):
        circles=self.boundaryCondition.circles
        for circle in circles:
            widths = [(True if np.array(circles[i,:],copy=False).any() else False) for i in range(circle.shape[0])]
            grid_slice=self.grid[:,widths]
            disstances=(np.abs(i-self.boundaryCondition.cy) for i in np.arange(0,self.boundaryCondition.cy,self.dy))
            
        
        
    def __call__(self, *args, **kwargs):
        pass

    def run(self,maxruns:int=1000,stencil:int=5,gamma:float=0.0,abs_tol:float=1e-9,rel_tol:float=1e-6):
        Xs, Ys, self.grid = laplace_ode_solver_continue(
            self.grid, self.boundaryCondition,max_iterations=maxruns,stencil=stencil,
            gamma=gamma,abs_tol=abs_tol,rel_tol=rel_tol,wrap=True,wrap_direction='x'
            )
        if self.cbar is not None:
            try:
                self.cbar.remove()
            except:
                pass
            self.cbar = None
            self.figure.clear()
            axes = self.figure.add_subplot(111)
            self.axes = axes
        self.Image=self.axes.imshow(self.grid)

        self.figure.draw_without_rendering()

        

        self.figure.canvas.draw()
        

        self.axes.imshow(self.grid, )
        
        if self.cbar is None:
            self.cbar = self.figure.colorbar(self.Image)

        self.figure.canvas.draw()
    
    def move_circle_to(self,cricle_index:int=0,cx:float=0.0,cy:float=0.0):
        self.boundaryCondition.shift_circle(cirlce_index=cricle_index,cx=cx,cy=cy)
        self.grid=self.boundaryCondition(self.grid)
        for j in [i for i in self.axes.images]:
            j.remove()
            
        self.axes.imshow(self.grid)
    
    def move_circle_by(self,cricle_index:int,cx:float,cy:float):
        self.boundaryCondition.shift_circle_displace(cirlce_index=cricle_index,d_x=cx,d_y=cy)
        self.grid=self.boundaryCondition(self.grid)
        for j in [i for i in self.axes.images]:
            j.remove()
            
        self.axes.imshow(self.grid)
    
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
        super()._cleanup()

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

