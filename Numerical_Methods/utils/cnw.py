import numpy.linalg as linalg

import numpy as np

import scipy.signal as signal

def createConvMatrix(gamma) : 
    return (1-gamma)*np.reshape(np.array(
                    [
                     0, 1, 0,
                     1, -4, 1,
                     0,  1, 0
                     ],dtype=np.float64),(3,3),"C")/4  + gamma*np.reshape(np.array(
                    [
                     1/2,  0, 1/2,
                       0, -2,   0,
                     1/2,  0, 1/2
                     ],dtype=np.float64),(3,3),"C")
                     
def  convolveMatrixes(a:np.ndarray,b:np.ndarray,wrap=False):
    return signal.convolve2d(a,b,mode="same",boundary= 'wrap' if wrap else"fill")
