class MultParent(type):
    
    def __init__(cls,*args,**kwargs):
        import inspect
        print('__init__',cls,args,kwargs,sep='\n\t',end='\n')
        return type.__init__(cls,*args,**kwargs)
    
    def __new__(cls,*args,**kwargs):
        print('__new__',cls,args,kwargs,sep='\n\t',end='\n')
        return super().__new__(cls,*args,**kwargs)
    @classmethod
    def __prepare__(cls,name, bases, *args, **kwargs):
        print('__prepare__',name,bases,args,kwargs,sep='\n\t',end='\n')
        return super().__prepare__(name,bases,*args,**kwargs)


class mstr(metaclass=MultParent):
    def __init__(self,*args,**kwargs):
        print(self,args,kwargs)
        
x = list[str]

print(x.__class_getitem__(int).__parameters__)
print(__builtins__.dir((type(list[int]))))

print((type(list[int])).__args__)

print(type('list[int]',(list,),{})())



from matplotlib.backends.backend_tkagg import _backend_tk,FigureCanvasTkAgg,_BackendTkAgg
 