import sys
import os
import threading
from importlib import reload
from os import kill
from signal import SIGTERM, SIGABRT
from typing import Optional


should_run_rt_loader = False
rt_loader_thread: Optional[threading.Thread] = None


def update_modules():
    """
    Monitor and reload modified Python modules in real-time.
    """
    global should_run_rt_loader
    module_timestamps = {}
    excluded_modules = set()

    while should_run_rt_loader:
        for module_name, module in list(sys.modules.items()):
            if module_name in excluded_modules:
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
                if cache_mtime >= module_mtime:
                    continue

            # Reload if modified
            if module_name not in module_timestamps or module_timestamps[module_name] < module_mtime:
                print(f"Reloading {module_name}")
                try:
                    reload(module)
                    module_timestamps[module_name] = module_mtime
                except (SyntaxError, ImportError) as e:
                    print(f"Failed to reload {module_name}: {e}")
    pass


def init_realtime_module() -> threading.Thread:
    """
    Initialize the real-time reloading thread.
    """
    global rt_loader_thread
    if rt_loader_thread is None:
        rt_loader_thread = threading.Thread(target=update_modules, daemon=True)
    return rt_loader_thread


def start_realtime_module():
    """
    Start the real-time module reloader.
    """
    global should_run_rt_loader, rt_loader_thread
    if rt_loader_thread is None or not rt_loader_thread.is_alive():
        rt_loader_thread = init_realtime_module()

    should_run_rt_loader = True
    if not rt_loader_thread.is_alive():
        rt_loader_thread.start()


def stop_realtime_module(timeout=0.5) -> bool:
    """
    Stop the real-time module reloader gracefully.
    """
    global should_run_rt_loader, rt_loader_thread
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

    rt_loader_thread = None
    return True
