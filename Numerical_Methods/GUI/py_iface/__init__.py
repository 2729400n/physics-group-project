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
        type = extras.get(annot)
        if(type is None):
            extras.get(val)
        if type is None:
            return str
        return type
        
    return arguments

defaultArgsToTypes = argumentToTypeFactory()

def getArgsToType(func:'function',argumetMapper = defaultArgsToTypes):
    func_info = inspect.getfullargspec(func)
    arg_types = {i:argumetMapper(func_info.annotations.get(i),(func_info.kwonlydefaults or {}).get(i)) for i in [*func_info.args,*func_info.kwonlyargs]}
    
    return arg_types
