from .boundary import geometryFactory as Boundary
import typing

class Task1(typing.Callable,typing.Protocol):
    def __init__(self):
        pass
    def _setup(self):
        pass
    def _run(self):
        pass
    def _cleanup(self):
        pass
    def __call__(self,*args,**kwargs):
        pass

    