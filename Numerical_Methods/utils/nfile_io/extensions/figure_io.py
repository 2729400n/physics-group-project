from . import image_io
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

def save_Figure(figure_:Figure,fname:'str|io.IOBase',transparent=False,dpi='figure',rasterize=False):
    old_raster=figure_.get_rasterized()
    if rasterize!=old_raster:
        figure_.set_rasterized(rasterize)
        
    figure_.savefig(fname,transparent=transparent,dpi=dpi, format=None,
          metadata=None, bbox_inches=None, pad_inches=0.1,
          facecolor='auto', edgecolor='auto',)

    if rasterize!=old_raster:
        figure_.set_rasterized(old_raster)
        

fileOps = {'open':None,'save':save_Figure}
name = 'Figure'
extensions = []