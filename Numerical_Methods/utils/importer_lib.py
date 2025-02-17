import importlib.util
import importlib.machinery
import os
import os.path as pth
# from .naming import slugify

# A library to load plugins from


def import_from_path(path: str):
    ldr = importlib.machinery.SourceFileLoader
    finder = importlib.machinery.FileFinder(path, (ldr, ['.py']))
    mod = finder.find_spec(path.removesuffix('.py'))
    scene_module = importlib.util.module_from_spec(mod)
    importlib.machinery.SourcelessFileLoader.exec_module(
        scene_module.__loader__, scene_module)
    return scene_module


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
