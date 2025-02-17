import matplotlib as mplib
import matplotlib.artist
import matplotlib.pyplot as plt
import matplotlib.axes
import matplotlib.quiver

import numpy as np


def _backend_plot_E_Field(potentialMap=None, E_FieldMap=None, xs=None, ys=None, *args, **kwargs):
    # Adjust figure size for better visualization
    plt.figure(figsize=(18, 18), dpi=320)
    # Set origin for consistency
    plt.imshow(potentialMap, cmap='PiYG', origin='lower')
    plt.colorbar(label='Electric Potential')
    plt.quiver(xs, ys, E_FieldMap[:, :, 0], E_FieldMap[:, :, 1],
               color='b', scale=0.1, scale_units='xy')  # Adjust scale and color

    plt.title('Electric Potential Distribution (End-to-End)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.savefig(fname='BoxInBox.png')
    plt.show(block=True)  # Enable blocking view
