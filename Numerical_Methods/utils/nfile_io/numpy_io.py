import numpy.lib.npyio as nio
import numpy as np

def saveArray(name:str,array:np.ndarray,compressed:bool=True,as_Text:bool=False,fname:str=None,pickle:bool=False):
    match (compressed,as_Text):
        case (True,True):
            nio.savetxt(f"{name.removeprefix('.gz')}.gz",array,allow_pickle=pickle,fix_imports=True)
        case(True,False):
            np.save(name,array,allow_pickle=pickle,fix_imports=True)
        case(False,True):
            np.savetxt(name,array,allow_pickle=pickle,fix_imports=True)
        case(False,False):
            np.savez(name,array,allow_pickle=pickle,fix_imports=True)
    return None

def saveArray(name:str,array:np.ndarray,compressed:bool=True,as_Text:bool=False,fname:str=None,pickle:bool=False):
    match (compressed,as_Text):
        case (True,True):
            nio.savetxt(f"{name.removeprefix('.gz')}.gz",array,allow_pickle=pickle,fix_imports=True)
        case(True,False):
            np.save(name,array,allow_pickle=pickle,fix_imports=True)
        case(False,True):
            np.savetxt(name,array,allow_pickle=pickle,fix_imports=True)
        case(False,False):
            np.savez(name,array,allow_pickle=pickle,fix_imports=True)
    return None