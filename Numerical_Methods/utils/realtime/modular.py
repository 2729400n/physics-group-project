<<<<<<< HEAD
import sys
import os.path as pth
from importlib import reload
import threading
import pathlib as pthlib
from os import kill
from signal import SIGTERM,SIGABRT,SIGBREAK


shouldRunRTLoader = False
rtLoaderThread:threading.Thread = None


def updateModules():
    global shouldRunRTLoader
    iptime = {}
    notSpeced = []
    copydict = {}
    while shouldRunRTLoader:
        copydict = sys.modules.copy()
        for i in copydict:
            if i in notSpeced:
                continue
            mod = sys.modules.get(i)
            
            if mod is None:
                continue
            try:
                modspec = mod.__spec__
            except Exception as e:
                notSpeced.append(i)
                print(e)
                continue
=======
import Numerical_Methods.GUI as gui
import sys
import test_Numerical.check_user_approval as check_user_approval
import threading
import os.path as pth
from importlib import reload
from os import kill
from signal import SIGTERM, SIGABRT
import trace,traceback

doLibraryUpdate:'bool' = False
updateThread:threading.Thread = None

def updateModules():
    global doLibraryUpdate
    iptime = {}
    notSpeced = []
    copydict = {}
    while doLibraryUpdate:
        copydict = sys.modules.copy()
        for i in copydict:
            mod = sys.modules.get(i)
            if mod is None:
                continue
            modspec = mod.__spec__
>>>>>>> Errors
            if modspec is None:
                if i in notSpeced:
                    continue
                notSpeced.append(i)
                print(i)
                continue
            if modspec.origin is None:
                continue
            if not pth.exists(modspec.origin):
                continue
            modtime = pth.getmtime(modspec.origin)
            if modspec.cached:
                if pth.exists(modspec.cached):
                    mtimecache = pth.getmtime(modspec.cached)
                    if mtimecache < modtime:
                        print(f'Reloaded {i}')
                        reload(mod)
                        continue
                    else:
                        continue

            imptime = iptime.get(i)
            if imptime is None:
                iptime[i] = modtime
                continue
            if imptime < modtime:
                print(f'reloaded {i}')
                try:
                    reload(mod)
<<<<<<< HEAD
                except (SyntaxError,ImportError):
                    pass
                iptime[i] = modtime
    return None


def init_realtime_module():
    global rtLoaderThread
    if(rtLoaderThread is not None):
        return rtLoaderThread
    rtLoaderThread = threading.Thread(target=updateModules)

    return rtLoaderThread



def start_realtime_module():
    global shouldRunRTLoader,rtLoaderThread
    if rtLoaderThread is None:
        rtLoaderThread = init_realtime_module()
    
    shouldRunRTLoader = True
    rtLoaderThread.start()
    

def stop_realtime_module(timeout=0.5):
    global shouldRunRTLoader,rtLoaderThread
    shouldRunRTLoader = False
    if rtLoaderThread is not None:
        rtLoaderThread.join(timeout=timeout)
        if rtLoaderThread.is_alive():
            try:
                kill(rtLoaderThread.native_id,SIGTERM)
            except:
                pass
            rtLoaderThread.join(timeout=timeout)
            if rtLoaderThread.is_alive():
                try:
                    kill(rtLoaderThread.native_id,SIGABRT)
                except:
                    pass
                rtLoaderThread.join(timeout=timeout)
                if rtLoaderThread.is_alive():
                    return False
    rtLoaderThread = None
=======
                except Exception as e:
                    traceback.print_tb(e.__traceback__)

                iptime[i] = modtime
    return None

def init_realtime_module():
    global updateThread
    if(updateThread is not None):
        return updateThread
    updateThread = threading.Thread(
        None, updateModules, 'RealtimeUpdateModule', daemon=False)

    return updateThread

def start_realtime_module():
    global updateThread,doLibraryUpdate
    if(updateThread is None):
        if(doLibraryUpdate):
            return None
        updateThread = init_realtime_module()
    doLibraryUpdate = True
    updateThread.start()
    return None

def stop_realtime_module(waittime : float = None):
    '''
    Args:
        waititme: The time to block while waiting for a thread to terminate. The time can be upto 3x this
    '''
    global doLibraryUpdate,updateThread
    if(updateThread is None):
        return True
    doLibraryUpdate = False
    updateThread.join(waittime)
    if updateThread.is_alive():
        kill(updateThread.native_id,SIGTERM)
        updateThread.join(timeout=waittime)
        if(updateThread.is_alive()):
            kill(updateThread.native_id,SIGABRT)
            updateThread.join()
            
    if updateThread.is_alive():
        return False
    
    updateThread=None
>>>>>>> Errors
    return True