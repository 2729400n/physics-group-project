import inspect, sys, functools
import lzma, linecache, gzip, zipfile, zlib, base64, binascii
import signal

import re

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.constants as tkconst
import tkinter.simpledialog as diag
import tkinter.messagebox as msgbox

typePattern = re.compile(r'[^\|\s]*(?=([.*])*)')
print(re.match(typePattern,"int | x").group())

class Bundler:
    def __init__(self,entry:'tk.StringVar|tk.BooleanVar|tk.IntVar|tk.DoubleVar',field:'ttk.Entry|ttk.Checkbutton',iframe:'tk.LabelFrame|ttk.Frame|tk.Frame'):
        pass

def toBytes(x:str):
    return x.encode('ascii','strict')

def gui_call_wrapper(*positional_types,**kwargs_types):
    
    def partial_decorator(func):
        pos_types  = list(positional_types).copy()
        kw_types = kwargs_types.copy()
        argspec = inspect.getfullargspec(func)
        argspec.args
        @functools.wraps(func)
        def arg_transform_wrapper(*args,**kwargs):
            nonlocal pos_types,kw_types,argspec
            print(args,kwargs)
            args = [pos_types[i](args[i].get()) for i in range(len(args))]
            pos_args= [ *args]+ [ None for i in range(max(len(argspec.args) - len(args),0)) ]
            kwargs = {i:kw_types[i](kwargs[i].get()) for i in kwargs}
            kargs={}
            for i in kwargs:
                index =argspec.args.index(i)
                if index!= -1:
                    pos_args[index]=kwargs[i]
                else:
                    kargs[i]=kwargs[i]
            if len(kargs.keys())==0:
                return func(*pos_args)
            return func(*args,**kwargs)
        arg_transform_wrapper.__signature__  = inspect.signature(func)
        return arg_transform_wrapper
    return partial_decorator
        
    

def argumentToTypeFactory(extras:dict = None):
    transTable = {bool:bool,int:int,float:float,list:list,
                  "bool":bool,"int":int,"float":float,"list":list,
                  str:str,"str":str, bytes:bytes, "bytes":bytes
                  }
    if extras is not None:
        transTable.update(**extras)
    def arguments(annot:'str|type'=None,val=None):
        nonlocal transTable
        print('Annotation Type',type(annot))
        if val is None and annot is None:
            return str
        
        if isinstance(annot,type):
            if issubclass(annot,(str,bytes)):
                if issubclass(annot,(bytes)):
                    return bytes
                else: 
                    return str
            currtype = transTable.get(annot)
        elif isinstance(annot,str,bytes):
            currtype = transTable.get(re.match(typePattern,annot).group())
        else:
            currtype = None
        if(currtype is None):
            transTable.get(type(val))
        print(currtype)
        if currtype is None:
            return str
        return currtype
        
    return arguments

defaultArgsToTypes = argumentToTypeFactory()

def getArgsToType(func:'function',argumetMapper = defaultArgsToTypes):
    func_info = inspect.getfullargspec(func)
    arg_types = {i:argumetMapper(func_info.annotations.get(i),({**(func_info.kwonlydefaults or {})}).get(i)) for i in [*func_info.args,*func_info.kwonlyargs]}
    
    if (func_info.varargs) is not None:
        arg_types[func_info.varargs]=list
    return arg_types

def  add_Field_Var(master, field_name, field_type,field_value=None):
    varname =f'val_{field_name}'
    innerFrame =tk.LabelFrame(master,text=field_name)
    if(field_type==bool):
        entry= tk.BooleanVar(master, value=field_value, name=varname)
        entry_field = ttk.Checkbutton(innerFrame,name=field_name,text=field_name, variable=entry)
    if(field_type==str):
        entry= tk.StringVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame,name=field_name,text=field_name, validate='all', textvariable=entry)
    if(field_type==int):
        entry= tk.IntVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame, name=field_name,text=field_name, validate='all',validatecommand=lambda x: x.isnumeric(), textvariable=entry)
    if(field_type==float):
        entry= tk.DoubleVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame,name=field_name,text=field_name, validate='all',validatecommand=lambda x: x.isdecimal(), textvariable=entry)
    else:
        entry= tk.StringVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame,name=field_name,text=field_name, validate='all', textvariable=entry)
    return entry,entry_field,innerFrame
def callFunc(ev:'tk.Event[ttk.Button]',func:'function',*args, **kwargs):
    form = ev.widget.master
    for i in kwargs:
        print(i,kwargs[i].get())
    msgbox.showinfo(title=func.__name__,message=f"{func(**(kwargs))}")
    return None

def makeFunctionCallable(func:'function',master=None):
    argMapping=getArgsToType(func)
    wmain=ttk.Labelframe(master=master,width=640,height=480, text=func.__name__)
    stores = {}
    for i in  argMapping:
        store,field, iframe =add_Field_Var(wmain,i,argMapping[i])
        field.grid(sticky='w')
        iframe.grid(sticky='w')
        stores.setdefault(i,store)
    btn=ttk.Button(wmain,text="Submit", class_='Submit', name='submit_button')
    btn.bind_class('Submit','<Button-1>',lambda ev:callFunc(ev,func,**stores))
    btn.grid()
    
    # root.wm_geometry('640x480')
    # wmain.master.wm_geometry('640x480')
    wmain.grid(sticky='nw',padx=5,pady=5)
    wmain.grid_columnconfigure(0,weight=1)
    wmain.grid_rowconfigure(0,weight=1)
    
    
    master.mainloop()
if __name__ == '__main__':
    bin_gui = gui_call_wrapper(int,number=int)(bin)
    makeFunctionCallable(bin_gui)
    
