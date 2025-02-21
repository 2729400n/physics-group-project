import Numerical_Methods.GUI as gui
import sys
import test_Numerical.check_user_approval as check_user_approval
import unittest
import pytest
import sys
import threading
import os
import time
import os.path as pth
from importlib import reload
import signal

class Test_GUI():
    def test_scenes(self):
        assert(check_user_approval.didItWorkAsIntended()==0)
        return None
    def test_show(self):
        gui.start()
        # assert(check_user_approval.didItWorkAsIntendedScale()>5,'Not satisfactory')
        return None


main_thread_running = False

def updateModules():
    global main_thread_running
    iptime ={}
    notSpeced = []
    updatDictionary ={}
    copydict = {}
    while main_thread_running:
        copydict = sys.modules.copy()
        for i in copydict:
            mod = sys.modules.get(i)
            if mod is None:
                continue
            modspec = mod.__spec__
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
            modtime =pth.getmtime(modspec.origin)
            if modspec.cached:
                if  pth.exists(modspec.cached):    
                    mtimecache = pth.getmtime(modspec.cached)
                    if mtimecache<modtime:
                        print(f'Reloaded {i}')
                        reload(mod)
                        continue
                    else:
                        continue
            
            imptime = iptime.get(i)
            if imptime is None:
                iptime[i] = modtime
                continue
            if imptime<modtime:
                print(f'reloaded {i}')
                reload(mod)
                
                iptime[i] = modtime
    return None
                    

if __name__ == "__main__":
    updateThread=threading.Thread(None,updateModules,'updateModules',daemon=False)
    tester = Test_GUI()
    
    main_thread_running = True
    updateThread.start()
    try:
        tester.test_show()
        
        main_thread_running = False
        updateThread.join(9)
    except:
        main_thread_running=False
        updateThread.join(9)
    finally:
        exit(1)
    
    