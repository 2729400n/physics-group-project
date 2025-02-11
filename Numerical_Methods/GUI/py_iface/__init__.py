import inspect, sys, functools

def toBytes(x:str):
    return x.encode('ascii','strict')
    

def argumentToTypeFactory(extras = None):
    if extras == None:
        extras = {bool:bool,int:int,float:float,list:list}
        
    def arguments(annot=None,val=None):
        nonlocal extras
        if val is None and annot is None:
            return str
        if issubclass(annot,(str,bytes)):
            if issubclass(annot,(bytes)):
                return bytes
            else: 
                return str
        
    return arguments

def getArgsToType():
    func_info = inspect.getfullargspec(print)
    arg_types = {i:argumentToTypeFactory(func_info.annotations.get(i),func_info.kwonlydefaults.get(i)) for i in [*func_info.args,*func_info.kwonlyargs]}
    print(arg_types)
    print()
    return 

getArgsToType()