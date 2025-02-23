import sys
import os.path as pth
from importlib import reload
import threading
import pathlib as pthlib

main_thread_running = False


def updateModules():
    global main_thread_running
    iptime = {}
    notSpeced = []
    copydict = {}
    while main_thread_running:
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
                except (SyntaxError,ImportError):
                    pass
                iptime[i] = modtime
    return None