import importlib, importlib.machinery, importlib.abc, importlib.metadata, importlib.readers, importlib.resources, importlib.util, importlib.simple, importlib._bootstrap, importlib._bootstrap_external
import builtins,sys

ldr = importlib.machinery.SourceFileLoader
finder =importlib.machinery.FileFinder('.',(ldr,['.py','.pyc']))
spec= finder.find_spec(r'Numerical_Methods')
mod = importlib.util.module_from_spec(spec)
print(spec,file=sys.stderr)
print(mod)

# print(sys.path_hooks)