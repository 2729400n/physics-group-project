import matplotlib.artist,matplotlib.patches,matplotlib.path
import numpy as np


def circleQuadrant(r):
    # First solve for a qudrant the apply rotations
    r1 = np.array([0,r])
    r2 = np.array([r,0])
    theta = np.linspace(0,np.pi/4,1000)
    