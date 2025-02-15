import ast
import typing
import collections.abc as abc
import collections
import types
import numpy as np
import socket

# Task Abstract base class


class Task(type):
    def __new__(self, *args, **kwargs):
        return super().__new__(self, *args, **kwargs)


class TaskModule(types.ModuleType):
    __start__: "np.ndarray" = ...
    __starter__: "typing.Callable[[int,int],np.ndarray]" = ...

    def __init__(
        self, moduleNameSpace: 'types.ModuleType'
    ) -> None: ...
    __runner__: "typing.Callable[[int,int],np.ndarray]" = ...
    @property
    def __settings__(self,) -> dict: ...
