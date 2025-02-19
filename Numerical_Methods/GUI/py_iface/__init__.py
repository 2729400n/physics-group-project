import inspect, sys, functools
import lzma, linecache, gzip, zipfile, zlib, base64, binascii
import signal

import re

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.constants as tkconst
import tkinter.simpledialog as diag
import tkinter.messagebox as msgbox

import numpy as np
from .. import extended_widgets

typePattern = re.compile(r'[^\|\s]*(?=([.*])*)')
print(re.match(typePattern,"int | x").group())

class Bundler:
    def __init__(self,entry:'tk.StringVar|tk.BooleanVar|tk.IntVar|tk.DoubleVar',field:'ttk.Entry|ttk.Checkbutton',iframe:'tk.LabelFrame|ttk.Frame|tk.Frame'):
        pass

def toBytes(x:str):
    return x.encode('ascii','strict')


        
    

def argumentToTypeFactory(extras:dict = None):
    transTable = {bool:bool,int:int,float:float,list:list,
                  "bool":bool,"int":int,"float":float,"list":list,
                  str:str,"str":str, bytes:bytes, "bytes":bytes
                  }
    if extras is not None:
        transTable.update(**extras)
    def arguments(annot:'str|type'=None,val=None):
        nonlocal transTable
        # print('Annotation Type',type(annot))
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
        # print(currtype)
        return currtype
        
    return arguments

defaultArgsToTypes = argumentToTypeFactory()

def getArgsToType(func:'function',argumetMapper = defaultArgsToTypes,classType=False,instance=None):
    func_info = inspect.getfullargspec(func)
    arg_types = dict()
    for i in [*func_info.args,*func_info.kwonlyargs]:
        if(classType==True and i =='self'):continue
        arg_types[i]=argumetMapper(func_info.annotations.get(i),({**(func_info.kwonlydefaults or {})}).get(i))
    
    if (func_info.varargs) is not None:
        arg_types[func_info.varargs]=list
    return arg_types

def gui_call_wrapper(*positional_types,**kwargs_types):
    pos_types  = list(positional_types).copy()
    kw_types = kwargs_types.copy()
    def partial_decorator(func):
        nonlocal pos_types,kw_types
        arg2Type = getArgsToType(func)
        
        

        
        argspec = inspect.getfullargspec(func)
        posType_len = len(pos_types)
        for i in range(len(argspec.args)):
            if argspec.args[i] not in kw_types:
                kw_types.update(**{argspec.args[i]:arg2Type.get(argspec.args[i])})
                if len(pos_types)<=i:
                    ntype = arg2Type.get(argspec.args[i])
                    if ntype is not None:
                        pos_types+=[ntype]
        for i in argspec.kwonlyargs:
            if argspec.kwonlyargs[i] not in kw_types:
                kw_types.update(**{argspec.kwonlyargs[i]:arg2Type.get(argspec.kwonlyargs[i])})
        # print('pos_types',pos_types)
        # print('kw_types',kw_types)
        
        
        @functools.wraps(func)
        def arg_transform_wrapper(*args,**kwargs):
            nonlocal pos_types,kw_types,argspec
            # print(args,kwargs)
            
            for i in range(len(args)):
                if(isinstance(i,(tk.StringVar,tk.BooleanVar,tk.IntVar,tk.DoubleVar,extended_widgets.ItemList))):
                    args+=[pos_types[i](args[i].get()) ]
                    
            pos_args= [ *args]+ [ None for i in range(max(len(argspec.args) - len(args),0)) ]
            
            
            for i in kwargs:
                if(isinstance(i,(tk.StringVar,tk.BooleanVar,tk.IntVar,tk.DoubleVar,extended_widgets.ItemList))):
                    kwargs.update(**{i:kw_types[i](kwargs[i].get())})
            # print(args,kwargs)
            kargs={}
            for i in kwargs:
                index =argspec.args.index(i)
                if index!= -1:
                    pos_args[index]=kwargs[i]
                else:
                    kargs[i]=kwargs[i]
                    
            # print(pos_args,kargs)
            if len(kargs.keys())==0:
                return func(*pos_args)
            return func(*args,**kwargs)
        arg_transform_wrapper.__signature__  = inspect.signature(func)
        return arg_transform_wrapper
    return partial_decorator

fieldToWidget = {}
def  add_Field_Var(master, field_name, field_type,field_value=None):
    varname =f'val_{field_name}'
    innerFrame =tk.LabelFrame(master,text=field_name)
    if(field_type==bool):
        entry= tk.BooleanVar(master, value=field_value, name=varname)
        entry_field = ttk.Checkbutton(innerFrame,name=field_name,text=field_name, variable=entry)
    elif(field_type==str):
        entry= tk.StringVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame,name=field_name,text=field_name, validate='all', textvariable=entry)
    elif(field_type==int):
        entry= tk.IntVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame, name=field_name,text=field_name, validate='all',validatecommand=lambda x: x.isnumeric(), textvariable=entry)
    elif(field_type==float):
        entry= tk.DoubleVar(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame,name=field_name,text=field_name, validate='all',validatecommand=lambda x: x.isdecimal(), textvariable=entry)
    elif(issubclass(field_type,list)):
        entry_field = extended_widgets.TypedItemList(innerFrame,item_type='float')
        entry= entry_field
    else:
        entry= tk.Variable(master, value=field_value, name=varname)
        entry_field = ttk.Entry(innerFrame,name=field_name,text=field_name, validate='all', textvariable=entry)
    return entry,entry_field,innerFrame


# Calling Function that begin call
def callFunc(ev:'tk.Event[ttk.Button]',func:'function',*args, **kwargs):
    form = ev.widget.master
    # print(args,kwargs)
    for i in kwargs:
        
        if isinstance(kwargs[i],(tk.Variable,tk.StringVar,tk.BooleanVar,tk.IntVar,tk.DoubleVar,extended_widgets.ItemList)):
            arg = kwargs[i].get()
            if  isinstance(kwargs[i],tk.Variable):
                try:
                    if arg.strip() =='True':
                        arg=True
                    elif arg.strip() =='False':
                        arg=False
                    else:
                        raise ValueError()

                except:
                    try:
                        arg=int(arg)
                    except:
                        print('not int')
                        try:
                            arg=np.float64(arg)
                        except:
                            print('not float')
                            arg=str(arg)
            # print('callFunc before Storing:',arg,type(arg))
            kwargs[i]=arg
    # print(kwargs)
    returnValue=func(**kwargs)
    # print(func)
    if returnValue is not None:
        msgbox.showinfo(title=func.__name__,message=f"{returnValue}")
    return None

def makeFunctionCallable(func:'function',master=None,classType=False,instance=None,direction='left'):
    argMapping=getArgsToType(func,classType=classType)
    wmain=ttk.Labelframe(master=master,width=640,height=480, text=func.__name__)
    stores = {}
    for i in  argMapping:
        print(i)
        store,field, iframe =add_Field_Var(wmain,i,argMapping[i])
        field.grid(sticky='w')
        iframe.grid(sticky='w')
    stores.update(**{i:store})
    btn=ttk.Button(wmain,text="Submit", class_='Submit', name='submit_button')
    # print(stores)
    btn.bind('<Button-1>',lambda ev:callFunc(ev,func,**stores))
    btn.grid()
    
    # root.wm_geometry('640x480')
    # wmain.master.wm_geometry('640x480')
    wmain.pack(fill=tk.BOTH,expand=True,padx=5,pady=5,side=direction,anchor=tk.NW)
    return stores


    
    
