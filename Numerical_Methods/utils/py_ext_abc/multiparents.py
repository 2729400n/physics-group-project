class MultParent(type):
    def __new__(cls,*args,**kwargs):
        print(cls,args,kwargs)
        return super().__new__(cls,*args,**kwargs)
    @classmethod
    def __prepare__(name, bases, *args, **kwargs):
        print(name,bases,args,kwargs)
        return super().__prepare__(name,bases,*args,**kwargs)
