import sys
import os
import threading
from importlib import reload
from os import kill
from signal import SIGTERM, SIGABRT
import time
from typing import Optional


should_run_rt_loader = False
rt_loader_thread: Optional[threading.Thread] = None

WHITELIST = {'Numerical_Methods','Numerical_Methods.GUI.scenes.'}
BLACKLIST = {__name__,'__main__','numpy._globals','zipp','sys'}

WHITELIST_ENABLED = True
BLACKLIST_ENABLED = True

def update_modules():
    """
    Monitor and reload modified Python modules in real-time.
    """
    global should_run_rt_loader,BLACKLIST,WHITELIST
    module_timestamps = {}
    excluded_modules = set()
    included_modules = WHITELIST
    exmodule = BLACKLIST
    

    while should_run_rt_loader:
        # time.sleep(5)
        # print('F1')
        for module_name, module in list(sys.modules.items()):
            ok=False
            if WHITELIST_ENABLED and BLACKLIST:
                for i in included_modules:
                    if module_name.startswith(i):
                        break
                else:
                    continue
                for i in exmodule:
                    if module_name.startswith(i):
                        break
                else:
                    ok=True   
            elif WHITELIST_ENABLED:
                for i in included_modules:
                    if module_name.startswith(i):
                        ok=True
                        break          
            elif BLACKLIST:
                for i in exmodule:
                    if module_name.startswith(i):
                        break
                else:
                    ok=True
            
            if not ok:
                continue
            
            for i in excluded_modules:
                if module_name.startswith(i):
                    continue
            
            if module is None or not hasattr(module, "__spec__"):
                excluded_modules.add(module_name)
                continue

            spec = module.__spec__
            if spec is None or spec.origin is None or not os.path.exists(spec.origin):
                excluded_modules.add(module_name)
                continue

            module_mtime = os.path.getmtime(spec.origin)

            # Handle compiled cache
            if spec.cached and os.path.exists(spec.cached):
                cache_mtime = os.path.getmtime(spec.cached)
                if cache_mtime > module_mtime:
                    module_mtime = cache_mtime

            # Reload if modified
            if (module_name not in module_timestamps) or (module_timestamps[module_name] < module_mtime):
                print(f"Reloading {module_name}")
                try:
                    sys.modules[module_name]=reload(module)
                    module_timestamps[module_name] = module_mtime
                except (SyntaxError, ImportError) as e:
                    print(f"Failed to reload {module_name}: {e}")
                except (Exception) as re:
                    print(f"Failed to reload {module_name}: {re}")
                    excluded_modules.add(module_name)
    pass


def init_realtime_module() -> threading.Thread:
    """
    Initialize the real-time reloading thread.
    """
    global rt_loader_thread
    if rt_loader_thread is None:
        rt_loader_thread = threading.Thread(name='rtLoader',target=update_modules, daemon=True)
    return rt_loader_thread


def start_realtime_module(whitelist=None,blacklist=None,
                          shouldblackList=True,shouldwhiteList=True):
    """
    Start the real-time module reloader.
    """
    global should_run_rt_loader, rt_loader_thread,WHITELIST_ENABLED,WHITELIST,BLACKLIST,BLACKLIST_ENABLED
    if whitelist is not None:
        WHITELIST.update(whitelist)
    if blacklist is not None:
        BLACKLIST.update(BLACKLIST)
    
    BLACKLIST_ENABLED=shouldblackList
    WHITELIST_ENABLED=shouldwhiteList
    
    
    if rt_loader_thread is None or not rt_loader_thread.is_alive():
        rt_loader_thread = init_realtime_module()

    should_run_rt_loader = True
    if not rt_loader_thread.is_alive():
        rt_loader_thread.start()
        


def stop_realtime_module(timeout=0.5) -> bool:
    """
    Stop the real-time module reloader gracefully.
    """
    global should_run_rt_loader, rt_loader_thread,WHITELIST,BLACKLIST
    should_run_rt_loader = False

    if rt_loader_thread is not None:
        rt_loader_thread.join(timeout=timeout)
        if rt_loader_thread.is_alive():
            try:
                kill(rt_loader_thread.native_id, SIGTERM)
            except ProcessLookupError:
                pass
            rt_loader_thread.join(timeout=timeout)
            if rt_loader_thread.is_alive():
                try:
                    kill(rt_loader_thread.native_id, SIGABRT)
                except ProcessLookupError:
                    pass
                rt_loader_thread.join(timeout=timeout)
                if rt_loader_thread.is_alive():
                    return False
    WHITELIST = {'Numerical_Methods',}
    BLACKLIST = {__name__,'__main__','numpy._globals','zipp','sys'}
    rt_loader_thread = None
    return True
