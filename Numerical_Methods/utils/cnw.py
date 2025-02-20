import numpy.linalg as linalg

import numpy as np


def createConvMatrix(gamma) : 
    return (1-gamma)*np.reshape(np.array(
                    [
                     0, 1, 0,
                     1, -4, 1,
                     0,  1, 1
                     ],dtype=np.float64),(3,3),"C") + gamma*np.reshape(np.array(
                    [
                     1/2, 0, 1/2,
                     0, -2, 0,
                     1/2,  0, 1/2
                     ],dtype=np.float64),(3,3),"C")
                     
                     

