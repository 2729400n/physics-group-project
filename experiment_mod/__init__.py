from importlib.machinery import ModuleSpec,SourceFileLoader
from importlib.util import module_from_spec
import sys
print('loaded',__name__)
if __name__=='__main__':
    __name__ = 'experiment_mod'
    __package__= 'experiment_mod'
    import os, os.path as pth
    __base__ = pth.abspath(pth.dirname(__file__))
    __path__ = [__base__]
    __loader__:SourceFileLoader = SourceFileLoader('experiment_mod',pth.join(__base__,'__init__.py'))
    __spec__:ModuleSpec = ModuleSpec(name=__name__,
                                    loader=__loader__,
                                    origin=__file__,
                                    is_package=True,
                                    )
    __spec__.submodule_search_locations.append(__base__)
    sys.modules[__name__] = module_from_spec(spec=__spec__)
print(__loader__.name,__loader__.path)
# print(__name__)
# print(__loader__,__package__,__path__,__cached__,__spec__,sep='\r\n')
from . import inner_mod