import importlib.util
import importlib.machinery
import importlib.metadata
import importlib.simple
from importlib.machinery import ModuleSpec,SourceFileLoader,PathFinder,SourcelessFileLoader
from importlib.util import find_spec,module_from_spec
import importlib
from . import naming
import os
import os.path as pth
import pathlib
import sys
from .realtime import modular
# from .naming import slugify

# A library to load plugins from


def import_from_path(path: str,mod_name:str=None,is_pacakge:bool=False,package_suffix:str=None,load_spec:bool=False,make_updateable:bool=False):
    path_=pathlib.Path(path)
    
    if mod_name is None:
        mod_name=naming.slugify(path_.stem)
        if mod_name=='__init__':
            mod_name=naming.slugify(path_.parent.stem)
            print(mod_name)
        if package_suffix is not None:
            package_suffix=package_suffix.strip()
            if not package_suffix.endswith('.'):
                package_suffix+='.'
            mod_name=f"{package_suffix}{mod_name}"
        
    modorigin = str(path_.resolve().absolute())
    if path_.suffix=='.pyc':
        mod = ModuleSpec(mod_name, origin=modorigin, loader=SourcelessFileLoader(mod_name,modorigin), is_package=is_pacakge)
    else:
        mod = ModuleSpec(mod_name, origin=modorigin, loader=SourceFileLoader(mod_name,modorigin), is_package=is_pacakge)
    if is_pacakge:
        mod.submodule_search_locations=[str(pathlib.Path(modorigin).parent.resolve().absolute())]
        if(package_suffix):
            package_suffix=package_suffix.removesuffix('.')
            modparent=sys.modules.get(package_suffix)
            try:
                spec=modparent.__spec__
                mod.submodule_search_locations.append(spec.submodule_search_locations)
            except Exception as e:
                print('Failed with add paent submodules with',e)
        print(mod.submodule_search_locations)
    module_=importlib.util.module_from_spec(mod)
    
    module_.__file__ = modorigin
    
    importlib.machinery.SourcelessFileLoader.exec_module(module_.__loader__,module_)
    sys.modules[module_.__name__]= module_
    if load_spec:
        module_.__spec__=mod
    if not make_updateable:
        modular.BLACKLIST.add(module_.__name__)
    else:
        modular.WHITELIST.add(module_.__name__)
    
    
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
