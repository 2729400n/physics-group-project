import inspect, sys, functools


def getArgsToType():
    
print(inspect.getfullargspec(print).annotations)