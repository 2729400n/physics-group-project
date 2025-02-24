import pathlib
import numpy.lib.npyio as nio
import numpy as np

def saveArrays(name:str,*array:np.ndarray,compressed:bool=True,pickle:bool=False,**karray):
    fname=pathlib.Path(name)
    fname=fname.with_suffix('.npz').absolute()
    match (compressed):
        
        case(True):
            np.savez_compressed(fname,*array,allow_pickle=pickle,fix_imports=True,**karray)
        case(False):
            np.savez(fname,*array,allow_pickle=pickle,fix_imports=True,**karray)
    
    return None


def saveArray(name:str,array:np.ndarray=None,compressed:bool=True,pickle:bool=False,*args,**karray):
    fname=pathlib.Path(name)
    fname=fname.with_suffix('.npy').absolute()
    np.save(fname,*array,allow_pickle=pickle)
    
    return None

def save(name:str,is_multi:bool=True,*array:np.ndarray,compressed:bool=True,pickle:bool=False,**karray):
    try:
        if is_multi:
            saveArrays(name,*array,compressed=compressed,pickle=pickle,**karray)
        else:
            saveArray(name,array[0],compressed=compressed,pickle=pickle,**karray)
    except Exception as e:
        raise e
    
    return True
    

def loadArray(name:str,array:np.ndarray,compressed:bool=True,as_Text:bool=False,fname:str=None,pickle:bool=False):
    np.load(name,'c',allow_pickle=True,fix_imports=True)
    return None

fileOps = {'open':None,'save':save_Figure}
name = 'Figure'
extensions = ['.npz','.npy','.txt']