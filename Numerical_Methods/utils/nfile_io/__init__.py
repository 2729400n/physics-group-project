import tkinter.filedialog as fdiag
import pathlib


def saveFile(gui:bool=False):
    pass

def saveFileCLI():
    pass
SAVEDIR = pathlib.Path.home()

def setSaveDir(path:str):
    global SAVEDIR
    SAVEDIR = pathlib.Path(path).resolve()
    return None

def resetSaveDir():
    global SAVEDIR
    SAVEDIR = pathlib.Path.home()
    return None

def getsaveDir():
    return SAVEDIR

def saveFileGui(data:bytes,ftypes=None):
    fout=fdiag.asksaveasfile(mode='wb',confirmoverwrite=True,defaultextension='.npy',initialdir=SAVEDIR,filetypes=ftypes, title="Choose Outputfile")
    if fout is None:
        return False
    if not (fout.writable()):
        raise FileExistsError('Make sure file can be written to and can exist')
    fout.write(data)
    fout.close()
    return True

if __name__== '__main__':
    saveFileGui(b'Helllo\r\n')
    