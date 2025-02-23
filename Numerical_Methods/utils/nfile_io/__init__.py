
import pathlib



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


def saveFile(gui:bool=False):
    pass

def saveFileCLI(data:bytes):
    currpth = input(f"Where Would you like to save the file : relative to {pathlib.Path.cwd().as_posix()}\n>>>")
    currpath =pathlib.Path(currpth).resolve()
    try:  
        fout =open(currpth,'wb')
    except (FileExistsError,FileNotFoundError):
        fout=None
    if fout is None:
        return False
    if not (fout.writable()):
        raise FileExistsError('Make sure file can be written to and can exist')
    fout.write(data)
    fout.close()
    return True

def saveFileCurses(data:bytes):
    import curses,curses.ascii,curses.has_key,curses.panel,curses.textpad
    stdo = curses.initscr()
    stdscr=curses.initscr()
    curses.nocbreak()
    
    stdscr.clear()
    stdscr.box()
    stdscr.addstr(0,0,f"Where Would you like to save the file : relative to {pathlib.Path.cwd().as_posix()}")
    stdscr.addstr(1,0,'>>>')
    stdscr.refresh()
    
    
    stdo.addstr(2,0,'Second screen!')
    path=stdo.getstr()
    stdo.addstr(4,0,path)
    
    stdo.getstr(9,0)
    return True

def saveFileGui(data:bytes,ftypes=None,initname:str=None):
    import tkinter.filedialog as fdiag
    fout=fdiag.asksaveasfile(mode='wb',confirmoverwrite=True,defaultextension='.npy',initialdir=SAVEDIR,filetypes=ftypes, title="Choose Outputfile",initialfile=initname)
    if fout is None:
        return False
    if not (fout.writable()):
        raise FileExistsError('Make sure file can be written to and can exist')
    fout.write(data)
    fout.close()
    return True

if __name__== '__main__':
    saveFileCurses(b'Helllo\r\n')
    