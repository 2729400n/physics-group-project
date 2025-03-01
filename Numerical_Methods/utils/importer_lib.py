import importlib.util
import importlib.machinery
import importlib.metadata
import importlib.simple
from importlib.machinery import ModuleSpec,SourceFileLoader,PathFinder
from importlib.util import find_spec,module_from_spec
import importlib

import os
import os.path as pth
import pathlib
import sys

# from .naming import slugify

# A library to load plugins from


def import_from_path(path: str,mod_name:str=None,is_pacakge:bool=False):
    ldr = importlib.machinery.SourceFileLoader
    path_=pathlib.Path(path)
#     print(path_)
    
    if mod_name is None:
        mod_name=path_.stem
    modorigin = str(path_.resolve().absolute())
    
    mod = ModuleSpec(mod_name, origin=modorigin, loader=SourceFileLoader(mod_name,modorigin), is_package=is_pacakge)
    
    module_=importlib.util.module_from_spec(mod)
    
    module_.__file__ = modorigin
    
    importlib.machinery.SourcelessFileLoader.exec_module(module_.__loader__,module_)
    sys.modules[module_.__name__]= module_
    
    return module_




def import_all_from_path(path: str):
    ldr = importlib.machinery.SourceFileLoader
    finder = importlib.machinery.FileFinder(path, (ldr, ['.py']))
    mods = dict()
    for i in os.listdir(pth.abspath(path)):
        if i.endswith('.py') and i != '__init__.py':

            mod = finder.find_spec(os.path.basename(i).removesuffix('.py'))
            scene_module = importlib.util.module_from_spec(mod)
            importlib.machinery.SourcelessFileLoader.exec_module(
                scene_module.__loader__, scene_module)
            mods.setdefault(mod.name or 'k', mod)
    return mods
